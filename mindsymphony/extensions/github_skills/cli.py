"""
GitHub Skills CLI
命令行接口 - 提供便捷的命令行工具

Usage:
    python -m mindsymphony.extensions.github_skills.cli distill <repo_url>
    python -m mindsymphony.extensions.github_skills.cli search <query>
    python -m mindsymphony.extensions.github_skills.cli generate <task_description>
    python -m mindsymphony.extensions.github_skills.cli profile <github_username>
    python -m mindsymphony.extensions.github_skills.cli recommend
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

from .github_skill_distiller import GitHubSkillDistiller
from .skill_knowledge_graph import SkillKnowledgeGraph
from .skill_dna import SkillDNA
from .dynamic_skill_generator import DynamicSkillGenerator, GenerationRequest


def cmd_distill(args):
    """蒸馏GitHub仓库为技能"""
    print(f"🔬 正在蒸馏: {args.repo}")

    distiller = GitHubSkillDistiller()
    result = distiller.distill(
        args.repo,
        extract_patterns=args.extract_patterns,
        include_code_examples=args.include_code,
        personalize=args.personalize
    )

    # 保存技能文件
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    skill_file = output_dir / f"{result.skill_name}.md"
    with open(skill_file, 'w', encoding='utf-8') as f:
        f.write(result.skill_content)

    # 保存元数据
    meta_file = output_dir / f"{result.skill_name}.json"
    with open(meta_file, 'w', encoding='utf-8') as f:
        json.dump(result.metadata, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 蒸馏完成!")
    print(f"📄 技能文件: {skill_file}")
    print(f"📊 置信度: {result.confidence:.1%}")
    print(f"🔖 提取模式: {len(result.patterns)} 个")

    return result


def cmd_search(args):
    """搜索技能知识图谱"""
    print(f"🔍 搜索: {args.query}")

    graph = SkillKnowledgeGraph()
    results = graph.search(args.query, limit=args.limit)

    if not results:
        print("❌ 未找到匹配的技能")
        return

    print(f"\n📊 找到 {len(results)} 个技能:\n")

    for i, skill in enumerate(results, 1):
        print(f"{i}. {skill.name}")
        print(f"   来源: {skill.source}")
        print(f"   类型: {skill.type}")
        print(f"   标签: {', '.join(skill.tags) if skill.tags else '无'}")
        print(f"   描述: {skill.description[:100]}..." if skill.description else "")
        print()


def cmd_generate(args):
    """动态生成技能"""
    print(f"🎯 生成任务技能: {args.task[:50]}...")

    generator = DynamicSkillGenerator()

    request = GenerationRequest(
        task_description=args.task,
        required_capabilities=args.capabilities or [],
        preferred_sources=args.sources or []
    )

    skill = generator.generate(request, persist=args.persist)

    # 保存技能文件
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    skill_file = output_dir / f"{skill.skill_id}.md"
    with open(skill_file, 'w', encoding='utf-8') as f:
        f.write(skill.content)

    print(f"\n✅ 技能生成完成!")
    print(f"📄 技能文件: {skill_file}")
    print(f"📊 置信度: {skill.confidence:.1%}")
    print(f"🔗 参考来源: {len(skill.sources)} 个项目")

    if skill.confidence < 0.6:
        print("\n⚠️  置信度较低，建议人工审核后使用")


def cmd_profile(args):
    """分析GitHub用户档案"""
    print(f"👤 分析GitHub用户: {args.username}")

    dna = SkillDNA(user_id=args.user_id or args.username)
    analysis = dna.analyze_github_profile(args.username)

    print(f"\n📊 分析结果:\n")
    print(f"Starred Repos: {len(analysis.get('starred_repos', []))}")
    print(f"Top Languages: {', '.join(analysis.get('top_languages', []))}")
    print(f"Interests: {', '.join(analysis.get('interests', []))}")
    print(f"Contributions: {analysis.get('contributions', 0)}")

    # 生成专长报告
    report = dna.get_expertise_report()

    print(f"\n🎯 专长领域:")
    for domain, score in report.get('expertise_domains', {}).items():
        bar = '█' * int(score * 10) + '░' * (10 - int(score * 10))
        print(f"  {domain:20s} [{bar}] {score:.0%}")

    if args.output:
        output_file = Path(args.output)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\n💾 报告已保存: {output_file}")


def cmd_recommend(args):
    """推荐学习路径"""
    print(f"📚 生成学习推荐...")

    dna = SkillDNA(user_id=args.user_id or 'default')

    if args.domain:
        recommendations = dna.recommend_learning_path(args.domain)
        print(f"\n🎯 {args.domain} 学习路径推荐:\n")
    else:
        # 基于当前专长推荐
        report = dna.get_expertise_report()
        domains = list(report.get('expertise_domains', {}).keys())

        if not domains:
            print("❌ 暂无专长数据，请先分析GitHub档案")
            return

        target_domain = domains[0]
        recommendations = dna.recommend_learning_path(target_domain)
        print(f"\n🎯 基于您的专长，推荐学习: {target_domain}\n")

    for i, rec in enumerate(recommendations, 1):
        priority_emoji = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(rec['priority'], '⚪')
        print(f"{i}. {priority_emoji} {rec['name']}")
        print(f"   类型: {rec['type']}")
        print(f"   原因: {rec['reason']}")
        print()


def cmd_stats(args):
    """显示技能库统计"""
    print("📊 MindSymphony GitHub技能库统计\n")

    # 知识图谱统计
    graph = SkillKnowledgeGraph()
    graph_stats = graph.get_stats()

    print("知识图谱:")
    print(f"  技能节点: {graph_stats['total_nodes']}")
    print(f"  关系数量: {graph_stats['total_relations']}")
    print(f"  平均使用: {graph_stats['avg_usage']:.1f}")

    if graph_stats['relation_types']:
        print("\n  关系类型分布:")
        for rel_type, count in graph_stats['relation_types'].items():
            print(f"    {rel_type}: {count}")

    # DNA统计
    dna = SkillDNA(user_id=args.user_id or 'default')
    report = dna.get_expertise_report()

    print(f"\n个人技能DNA:")
    print(f"  技能多样性: {report.get('skill_diversity', 0)}")
    print(f"  总体成功率: {report.get('success_rate', 0):.1%}")
    print(f"  学习速度: {report.get('learning_velocity', 0):.1f}")

    if report.get('top_skills'):
        print("\n  常用技能:")
        for skill in report['top_skills'][:5]:
            print(f"    - {skill['skill_name']}: {skill['use_count']}次 ({skill['success_rate']:.0%}成功率)")


def cmd_export(args):
    """导出技能图谱"""
    print(f"📤 导出技能图谱...")

    graph = SkillKnowledgeGraph()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if args.format == 'dot':
        graph.export_to_dot(str(output_path))
        print(f"✅ 已导出为GraphViz格式: {output_path}")
        print("💡 使用 'dot -Tpng {output_path} -o graph.png' 生成图片")
    else:
        # 导出为JSON
        data = {
            'nodes': [s.to_dict() for s in graph.nodes.values()],
            'relations': [r.to_dict() for r in graph.relations],
        }
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ 已导出为JSON: {output_path}")


def main():
    """主入口"""
    parser = argparse.ArgumentParser(
        description='MindSymphony GitHub Skills - 将GitHub压缩成你的超级技能库',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 蒸馏GitHub仓库
  python -m mindsymphony.extensions.github_skills.cli distill microsoft/ai-examples

  # 搜索技能
  python -m mindsymphony.extensions.github_skills.cli search "machine learning"

  # 动态生成技能
  python -m mindsymphony.extensions.github_skills.cli generate "分析生物信息学数据"

  # 分析GitHub档案
  python -m mindsymphony.extensions.github_skills.cli profile octocat

  # 查看统计
  python -m mindsymphony.extensions.github_skills.cli stats
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # distill命令
    distill_parser = subparsers.add_parser('distill', help='蒸馏GitHub仓库为技能')
    distill_parser.add_argument('repo', help='仓库标识 (如: owner/repo)')
    distill_parser.add_argument('--output', '-o', default='./generated_skills', help='输出目录')
    distill_parser.add_argument('--extract-patterns', action='store_true', help='提取代码模式')
    distill_parser.add_argument('--include-code', action='store_true', help='包含代码示例')
    distill_parser.add_argument('--personalize', action='store_true', help='个性化生成')
    distill_parser.set_defaults(func=cmd_distill)

    # search命令
    search_parser = subparsers.add_parser('search', help='搜索技能知识图谱')
    search_parser.add_argument('query', help='搜索关键词')
    search_parser.add_argument('--limit', '-l', type=int, default=10, help='返回数量')
    search_parser.set_defaults(func=cmd_search)

    # generate命令
    generate_parser = subparsers.add_parser('generate', help='动态生成技能')
    generate_parser.add_argument('task', help='任务描述')
    generate_parser.add_argument('--output', '-o', default='./generated_skills', help='输出目录')
    generate_parser.add_argument('--capabilities', '-c', nargs='+', help='必需能力')
    generate_parser.add_argument('--sources', '-s', nargs='+', help='首选来源')
    generate_parser.add_argument('--persist', action='store_true', help='持久化到知识图谱')
    generate_parser.set_defaults(func=cmd_generate)

    # profile命令
    profile_parser = subparsers.add_parser('profile', help='分析GitHub用户档案')
    profile_parser.add_argument('username', help='GitHub用户名')
    profile_parser.add_argument('--user-id', help='用户ID')
    profile_parser.add_argument('--output', '-o', help='输出文件')
    profile_parser.set_defaults(func=cmd_profile)

    # recommend命令
    recommend_parser = subparsers.add_parser('recommend', help='推荐学习路径')
    recommend_parser.add_argument('--domain', '-d', help='目标领域')
    recommend_parser.add_argument('--user-id', help='用户ID')
    recommend_parser.set_defaults(func=cmd_recommend)

    # stats命令
    stats_parser = subparsers.add_parser('stats', help='显示技能库统计')
    stats_parser.add_argument('--user-id', help='用户ID')
    stats_parser.set_defaults(func=cmd_stats)

    # export命令
    export_parser = subparsers.add_parser('export', help='导出技能图谱')
    export_parser.add_argument('--output', '-o', required=True, help='输出文件')
    export_parser.add_argument('--format', choices=['json', 'dot'], default='json', help='导出格式')
    export_parser.set_defaults(func=cmd_export)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        args.func(args)
    except Exception as e:
        print(f"\n❌ 错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
