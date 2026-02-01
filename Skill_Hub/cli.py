"""
Skill Hub - CLI Entry Point
命令行界面入口
"""

import asyncio
import sys
import os

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import click
    HAS_CLICK = True
except ImportError:
    HAS_CLICK = False

from config import ConfigManager, get_config
from database import Database, get_database
from models import SourceType
from sources import SkillslmSource, LocalSource, FortyTwoPluginSource, GitHubSource
from evaluation import EvaluationEngine
from adapt import AutoAdaptOrchestrator, adapt_skill_from_metadata


# 全局配置和数据库
config = None
db = None


def init_context():
    """初始化上下文"""
    global config, db
    if config is None:
        config = get_config()
    if db is None:
        os.makedirs(os.path.dirname(config.db_path) or ".", exist_ok=True)
        db = get_database(config.db_path)


def get_sources():
    """获取启用的数据源"""
    sources = []

    if config.skillslm.enabled:
        sources.append(SkillslmSource(config))

    if config.local.enabled:
        sources.append(LocalSource(config))

    if config.fortytwoplugin.enabled:
        sources.append(FortyTwoPluginSource(config))

    if config.github.enabled:
        sources.append(GitHubSource(config))

    return sources


def _evaluate_results(results, config_obj, db_obj, requirement):
    """辅助函数：评估搜索结果"""
    async def do_evaluate():
        # 获取本地 skills
        local_source = LocalSource(config_obj)
        local_skills = await local_source.list()
        local_metadata = [r.metadata for r in local_skills if r.metadata]

        # 创建评估引擎
        engine = EvaluationEngine(config_obj)

        # 评估每个结果
        for result in results:
            if result.metadata:
                report = await engine.evaluate(
                    result.metadata,
                    local_metadata,
                    requirement or ""
                )
                result.evaluation = report

    asyncio.run(do_evaluate())

    # 显示评估结果
    for result in results:
        if result.evaluation:
            click.echo(result.evaluation.display())
            click.echo("")


if HAS_CLICK:

    @click.group()
    @click.option('--config', '-c', help='配置文件路径')
    @click.pass_context
    def cli(ctx, config):
        """Skill Hub - 技能市场发现与管理中枢

        搜索、评估、下载和管理来自多个来源的 Claude Skills。
        """
        ctx.ensure_object(dict)
        config_manager = ConfigManager(config)
        ctx.obj['config'] = config_manager.load()

        # 初始化数据库
        db_path = ctx.obj['config'].db_path
        os.makedirs(os.path.dirname(db_path) or ".", exist_ok=True)
        ctx.obj['db'] = Database(db_path)


    @cli.command()
    @click.argument('query')
    @click.option('--source', '-s', help='指定数据源 (skillslm|local|42plugin|github)')
    @click.option('--evaluate', '-e', is_flag=True, help='同时进行预评估')
    @click.option('--requirement', '-r', help='用户需求描述（用于功能匹配评估）')
    @click.pass_context
    def search(ctx, query, source, evaluate, requirement):
        """搜索技能（所有市场）"""
        import time

        config_obj = ctx.obj['config']
        db_obj = ctx.obj['db']

        # 确定要搜索的数据源
        sources_to_search = []
        if source:
            source_map = {
                'skillslm': SkillslmSource,
                'local': LocalSource,
                '42plugin': FortyTwoPluginSource,
                'github': GitHubSource,
            }
            if source in source_map:
                sources_to_search = [source_map[source](config_obj)]
        else:
            # 使用 config_obj 而不是全局 config
            if config_obj.skillslm.enabled:
                sources_to_search.append(SkillslmSource(config_obj))
            if config_obj.local.enabled:
                sources_to_search.append(LocalSource(config_obj))
            if config_obj.fortytwoplugin.enabled:
                sources_to_search.append(FortyTwoPluginSource(config_obj))
            if config_obj.github.enabled:
                sources_to_search.append(GitHubSource(config_obj))

        click.echo(f"[SEARCH] Query: {query}")
        if requirement:
            click.echo(f"[REQUIREMENT] {requirement}")
        click.echo("")

        # 并发搜索所有数据源
        async def do_search():
            all_results = []
            tasks = [s.search(query) for s in sources_to_search if s.is_available()]

            if not tasks:
                click.echo("[ERROR] No available sources")
                return []

            results = await asyncio.gather(*tasks, return_exceptions=True)

            for r in results:
                if isinstance(r, Exception):
                    continue
                all_results.extend(r)

            return all_results

        results = asyncio.run(do_search())

        # 保存搜索历史
        db_obj.save_search(
            query,
            [s.source_type.value for s in sources_to_search],
            len(results)
        )

        # 显示结果
        if not results:
            click.echo("No results found")
            return

        click.echo(f"Found {len(results)} results:\n")

        for i, result in enumerate(results, 1):
            source_icon = {
                SourceType.SKILLSLM: "[skillslm]",
                SourceType.LOCAL: "[local]",
                SourceType.FORTY_TWO_PLUGIN: "[42plugin]",
                SourceType.GITHUB: "[github]",
            }.get(result.source, "[?]")

            click.echo(f"{i}. {source_icon} {result.name}")
            click.echo(f"   Source: {result.source.value}")
            desc = result.description or "No description"
            click.echo(f"   Description: {desc[:100]}...")
            click.echo("")

        # 可选：进行评估
        if evaluate and results:
            click.echo("Pre-assessing...\n")
            _evaluate_results(results, config_obj, db_obj, requirement)


    @cli.command()
    @click.argument('name')
    @click.option('--source', '-s', default='skillslm', help='数据源')
    @click.pass_context
    def info(ctx, name, source):
        """查看技能详情"""
        click.echo(f"[INFO] Getting details for {name}...")


    @cli.command()
    @click.argument('name')
    @click.option('--source', '-s', help='指定数据源')
    @click.option('--requirement', '-r', help='用户需求描述（用于功能匹配评估）')
    @click.pass_context
    def evaluate(ctx, name, source, requirement):
        """预评估技能（不下载）"""
        config_obj = ctx.obj['config']
        db_obj = ctx.obj['db']

        click.echo(f"[EVALUATE] Pre-assessing: {name}")
        if requirement:
            click.echo(f"[REQUIREMENT] {requirement}")
        click.echo("")

        # 获取本地 skills 用于对比
        local_source = LocalSource(config_obj)
        local_skills = asyncio.run(local_source.list())
        local_metadata = [r.metadata for r in local_skills if r.metadata]

        # 获取远程 skill 元数据
        # TODO: 实现获取逻辑

        click.echo("Pre-assessment feature under development...")


    @cli.command()
    @click.argument('path')
    @click.option('--requirement', '-r', help='用户需求描述')
    @click.option('--auto-register', is_flag=True, help='自动注册到 Intent Router')
    @click.pass_context
    def adapt(ctx, path, requirement, auto_register):
        """适配技能到 MindSymphony 格式

        将外部 Skill 转换为符合 MindSymphony 标准的格式
        """
        config_obj = ctx.obj['config']

        click.echo(f"[ADAPT] Adapting skill from: {path}")
        if requirement:
            click.echo(f"[REQUIREMENT] {requirement}")
        click.echo("")

        # 创建适配编排器
        orchestrator = AutoAdaptOrchestrator(config_obj)

        # TODO: 获取元数据和内容
        click.echo("Adapt feature under development...")


    @cli.command()
    @click.argument('name')
    @click.option('--source', '-s', help='指定数据源')
    @click.option('--dest', '-d', help='目标目录')
    @click.option('--adapt', is_flag=True, help='获取后自动适配')
    @click.option('--requirement', '-r', help='用户需求描述')
    @click.pass_context
    def fetch(ctx, name, source, dest, adapt, requirement):
        """获取并安装技能"""
        config_obj = ctx.obj['config']

        click.echo(f"[FETCH] Downloading: {name}...")
        if adapt:
            click.echo("[ADAPT] Will adapt to MindSymphony format after download")

        # TODO: 实现下载逻辑
        click.echo("Download feature under development...")


    @cli.command()
    @click.option('--category', '-c', help='按类别筛选')
    @click.option('--source', '-s', help='按来源筛选')
    @click.pass_context
    def list(ctx, category, source):
        """列出已安装的技能"""
        db_obj = ctx.obj['db']

        local_skills = db_obj.list_local_skills()

        if not local_skills:
            click.echo("No installed skills")
            return

        click.echo(f"Installed {len(local_skills)} skills:\n")

        for skill in local_skills:
            click.echo(f"• {skill['name']}")
            if skill['description']:
                click.echo(f"  {skill['description'][:60]}...")
            click.echo("")


    @cli.command()
    @click.pass_context
    def stats(ctx):
        """显示统计信息"""
        db_obj = ctx.obj['db']

        stats = db_obj.get_stats()

        click.echo("[STATS] Skill Hub Statistics\n")
        click.echo(f"Remote skills: {stats.get('remote_skills', 0)}")
        click.echo(f"Local skills: {stats.get('local_skills', 0)}")
        click.echo(f"Searches: {stats.get('searches', 0)}")
        click.echo("")

        click.echo("By source:")
        for key in ['remote_skillslm', 'remote_42plugin', 'remote_github']:
            if key in stats:
                source_name = key.replace('remote_', '')
                click.echo(f"  - {source_name}: {stats[key]}")


    @cli.command()
    @click.pass_context
    def init(ctx):
        """初始化配置文件"""
        config_manager = ConfigManager()
        config_manager.init_default_config()
        click.echo("[OK] Initialization complete")


    @cli.command()
    @click.option('--days', '-d', default=7, help='清理多少天前的缓存')
    @click.pass_context
    def cleanup(ctx, days):
        """清理旧缓存"""
        db_obj = ctx.obj['db']

        count = db_obj.cleanup_old_cache(days)
        click.echo(f"[OK] Cleaned {count} old cache entries")


    # 主入口
    def main():
        cli()


else:
    # 没有 click 时的简化版本
    def main():
        print("[ERROR] Need to install click library")
        print("   pip install click")


if __name__ == '__main__':
    main()
