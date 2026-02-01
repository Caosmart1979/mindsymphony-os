"""
GitHub Skills Integration
MindSymphony集成模块 - 将GitHub技能系统整合到现有架构

功能:
- 与Skill系统整合
- 与BMAD工作流整合
- 与认知建筑师整合
- 快捷命令注册
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

from .github_skill_distiller import GitHubSkillDistiller
from .skill_knowledge_graph import SkillKnowledgeGraph, SkillNode, RelationType
from .skill_dna import SkillDNA
from .dynamic_skill_generator import DynamicSkillGenerator, GenerationRequest


class GitHubSkillsIntegration:
    """
    GitHub技能系统集成器

    将GitHub技能系统整合到MindSymphony架构中
    """

    def __init__(self, config: Optional[Dict] = None):
        """
        初始化集成

        Args:
            config: 配置选项
        """
        self.config = config or {}
        self.storage_dir = Path(self.config.get(
            'storage_dir',
            '~/.mindsymphony/github_skills'
        )).expanduser()
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        # 初始化核心组件
        self.distiller = GitHubSkillDistiller(config)
        self.skill_graph = SkillKnowledgeGraph(
            storage_path=str(self.storage_dir / 'skill_graph.json')
        )
        self.skill_dna = None  # 按需初始化
        self.generator = DynamicSkillGenerator(
            skill_graph=self.skill_graph
        )

    def initialize_for_user(self, user_id: str):
        """
        为用户初始化系统

        Args:
            user_id: 用户ID
        """
        self.user_id = user_id
        self.skill_dna = SkillDNA(
            user_id=user_id,
            storage_dir=str(self.storage_dir / 'dna')
        )
        self.generator.skill_dna = self.skill_dna

        print(f"✅ GitHub技能系统已为用户 {user_id} 初始化")

    def distill_and_register(
        self,
        repo_url: str,
        tags: Optional[List[str]] = None,
        auto_link: bool = True
    ) -> Dict:
        """
        蒸馏仓库并注册到技能库

        Args:
            repo_url: 仓库URL
            tags: 自定义标签
            auto_link: 自动建立关系

        Returns:
            注册结果
        """
        print(f"🔬 蒸馏并注册: {repo_url}")

        # 1. 蒸馏仓库
        result = self.distiller.distill(repo_url)

        # 2. 创建技能节点
        skill_node = SkillNode(
            name=result.skill_name,
            source=f"github:{result.source_repo}",
            description=result.metadata.get('source', {}).get('description', ''),
            type='distilled',
            tags=tags or result.metadata.get('source', {}).get('topics', []),
            metadata={
                'distillation_confidence': result.confidence,
                'distilled_at': result.distillation_time.isoformat(),
                'stars': result.metadata.get('source', {}).get('stars', 0),
                'language': result.metadata.get('source', {}).get('language', 'Unknown'),
                'content_path': str(self._save_skill_content(result)),
            }
        )

        skill_id = self.skill_graph.add_skill(skill_node)

        # 3. 自动建立关系
        if auto_link:
            self._auto_link_skill(skill_node, result.patterns)

        # 4. 记录到DNA
        if self.skill_dna:
            self.skill_dna.record_skill_usage(
                skill_id=skill_id,
                skill_name=result.skill_name,
                success=True,
                context={'tags': ['distilled', 'github']}
            )

        print(f"✅ 技能已注册: {skill_node.name} (ID: {skill_id})")

        return {
            'skill_id': skill_id,
            'skill_name': result.skill_name,
            'confidence': result.confidence,
            'content_path': skill_node.metadata['content_path'],
        }

    def _save_skill_content(self, result) -> Path:
        """保存技能内容"""
        skills_dir = self.storage_dir / 'skills'
        skills_dir.mkdir(exist_ok=True)

        skill_file = skills_dir / f"{result.skill_name}.md"

        with open(skill_file, 'w', encoding='utf-8') as f:
            f.write(result.skill_content)

        return skill_file

    def _auto_link_skill(self, skill_node: SkillNode, patterns: List[Dict]):
        """自动建立技能关系"""
        # 查找相似技能并建立关系
        similar_skills = self.skill_graph.search(skill_node.name, limit=5)

        for similar in similar_skills:
            if similar.id == skill_node.id:
                continue

            # 检查标签相似度
            common_tags = set(skill_node.tags) & set(similar.tags)
            if common_tags:
                similarity = len(common_tags) / max(len(skill_node.tags), len(similar.tags))
                if similarity > 0.3:
                    self.skill_graph.add_relation(
                        skill_node.id,
                        similar.id,
                        RelationType.RELATED,
                        strength=similarity
                    )

    def generate_skill_on_demand(
        self,
        task_description: str,
        context: Optional[Dict] = None
    ) -> Dict:
        """
        按需生成技能

        Args:
            task_description: 任务描述
            context: 上下文

        Returns:
            生成的技能信息
        """
        print(f"🎯 按需生成技能: {task_description[:50]}...")

        request = GenerationRequest(
            task_description=task_description,
            context=context
        )

        skill = self.generator.generate(request, persist=True)

        return {
            'skill_id': skill.skill_id,
            'name': skill.name,
            'confidence': skill.confidence,
            'content': skill.content,
            'is_temporary': skill.is_temporary,
        }

    def get_skill_for_task(self, task_description: str) -> Optional[Dict]:
        """
        为任务获取最合适的技能

        搜索现有技能或生成新技能

        Args:
            task_description: 任务描述

        Returns:
            技能信息或None
        """
        # 1. 先搜索现有技能
        existing_skills = self.skill_graph.search(task_description, limit=5)

        if existing_skills:
            # 检查是否有高匹配度的技能
            for skill in existing_skills:
                # 名称包含查询词认为是高匹配
                if skill.name.lower() in task_description.lower():
                    return {
                        'source': 'existing',
                        'skill': skill,
                        'confidence': 0.9,
                    }

            # 返回最佳匹配
            return {
                'source': 'existing',
                'skill': existing_skills[0],
                'confidence': 0.7,
            }

        # 2. 没有匹配的技能，动态生成
        generated = self.generate_skill_on_demand(task_description)

        return {
            'source': 'generated',
            'skill': generated,
            'confidence': generated['confidence'],
        }

    def recommend_skills_for_project(
        self,
        project_description: str,
        tech_stack: Optional[List[str]] = None
    ) -> List[Dict]:
        """
        为项目推荐技能组合

        Args:
            project_description: 项目描述
            tech_stack: 技术栈

        Returns:
            推荐的技能列表
        """
        # 分析项目需求
        domains = self._extract_domains(project_description)

        # 搜索相关技能
        recommended = []

        for domain in domains:
            domain_skills = self.skill_graph.search(domain, limit=3)
            for skill in domain_skills:
                recommended.append({
                    'skill': skill,
                    'reason': f'匹配领域: {domain}',
                    'relevance': 0.8,
                })

        # 基于DNA个性化推荐
        if self.skill_dna:
            for domain in domains:
                if domain in self.skill_dna.profile.expertise_domains:
                    proficiency = self.skill_dna.profile.expertise_domains[domain]
                    if proficiency < 0.5:
                        # 推荐学习路径
                        path = self.skill_dna.recommend_learning_path(domain)
                        for rec in path[:2]:
                            recommended.append({
                                'skill': {'name': rec['name']},
                                'reason': f'学习建议: {rec["reason"]}',
                                'relevance': 0.6,
                                'is_recommendation': True,
                            })

        # 去重并排序
        seen = set()
        unique_recommended = []
        for rec in recommended:
            name = rec['skill']['name'] if isinstance(rec['skill'], dict) else rec['skill'].name
            if name not in seen:
                seen.add(name)
                unique_recommended.append(rec)

        unique_recommended.sort(key=lambda x: x['relevance'], reverse=True)

        return unique_recommended[:10]

    def _extract_domains(self, description: str) -> List[str]:
        """提取领域"""
        domain_keywords = {
            'web_development': ['web', 'frontend', 'backend', 'api'],
            'data_science': ['data', 'analysis', 'analytics'],
            'machine_learning': ['ml', 'ai', 'machine learning', 'model'],
            'devops': ['devops', 'deployment', 'ci/cd', 'docker'],
            'mobile': ['mobile', 'app', 'android', 'ios'],
            'security': ['security', 'auth', 'encryption'],
        }

        description_lower = description.lower()
        found_domains = []

        for domain, keywords in domain_keywords.items():
            if any(kw in description_lower for kw in keywords):
                found_domains.append(domain)

        return found_domains

    def create_skill_composition(
        self,
        skill_ids: List[str],
        composition_name: str,
        description: str
    ) -> str:
        """
        创建技能组合

        Args:
            skill_ids: 技能ID列表
            composition_name: 组合名称
            description: 组合描述

        Returns:
            组合技能ID
        """
        # 创建组合技能节点
        composition = SkillNode(
            name=composition_name,
            source='composition',
            description=description,
            type='composition',
            metadata={
                'composed_from': skill_ids,
                'created_at': datetime.now().isoformat(),
            }
        )

        composition_id = self.skill_graph.add_skill(composition)

        # 建立组合关系
        for skill_id in skill_ids:
            self.skill_graph.add_relation(
                composition_id,
                skill_id,
                RelationType.COMPOSES,
                strength=1.0
            )

        print(f"✅ 技能组合已创建: {composition_name}")

        return composition_id

    def export_to_mindsymphony_skill(
        self,
        skill_id: str,
        output_dir: Optional[str] = None
    ) -> Path:
        """
        导出为MindSymphony标准技能格式

        Args:
            skill_id: 技能ID
            output_dir: 输出目录

        Returns:
            输出路径
        """
        skill = self.skill_graph.get_skill(skill_id)
        if not skill:
            raise ValueError(f"技能不存在: {skill_id}")

        output_dir = Path(output_dir or '~/.mindsymphony/skills').expanduser()
        skill_dir = output_dir / f"github-{skill.name}"
        skill_dir.mkdir(parents=True, exist_ok=True)

        # 读取原始内容
        content = ""
        content_path = skill.metadata.get('content_path')
        if content_path and Path(content_path).exists():
            with open(content_path, 'r', encoding='utf-8') as f:
                content = f.read()

        # 生成SKILL.md
        skill_md = skill_dir / 'SKILL.md'
        with open(skill_md, 'w', encoding='utf-8') as f:
            f.write(content or f"# {skill.name}\n\n从GitHub蒸馏的技能\n")

        # 生成INTEROP.yml
        interop_yml = skill_dir / 'INTEROP.yml'
        interop_content = f"""apiVersion: mindsymphony.io/v1
kind: SkillInterop
metadata:
  name: {skill.name}
  source: {skill.source}
  created_at: {skill.created_at}
spec:
  version: "{skill.version}"
  type: {skill.type}
  tags:
{chr(10).join(['    - ' + tag for tag in skill.tags])}
  capabilities:
    - github_distilled
    - auto_generated
"""
        with open(interop_yml, 'w', encoding='utf-8') as f:
            f.write(interop_content)

        print(f"✅ 技能已导出: {skill_dir}")

        return skill_dir

    def get_stats(self) -> Dict:
        """获取集成系统统计"""
        return {
            'knowledge_graph': self.skill_graph.get_stats(),
            'dna': self.skill_dna.get_expertise_report() if self.skill_dna else None,
            'storage': {
                'path': str(self.storage_dir),
                'size_mb': self._get_directory_size(self.storage_dir),
            }
        }

    def _get_directory_size(self, path: Path) -> float:
        """获取目录大小(MB)"""
        total = 0
        for file in path.rglob('*'):
            if file.is_file():
                total += file.stat().st_size
        return total / (1024 * 1024)


# 快捷命令处理器
class GitHubSkillsCommandHandler:
    """
    命令处理器

    处理MindSymphony快捷命令
    """

    def __init__(self):
        self.integration = GitHubSkillsIntegration()

    def handle_command(self, command: str, args: List[str]) -> Dict:
        """
        处理命令

        Args:
            command: 命令名
            args: 参数列表

        Returns:
            处理结果
        """
        handlers = {
            'github-distill': self._handle_distill,
            'github-search': self._handle_search,
            'github-generate': self._handle_generate,
            'github-profile': self._handle_profile,
        }

        handler = handlers.get(command)
        if handler:
            return handler(args)

        return {'error': f'未知命令: {command}'}

    def _handle_distill(self, args: List[str]) -> Dict:
        """处理蒸馏命令"""
        if not args:
            return {'error': '需要提供仓库URL'}

        repo = args[0]
        result = self.integration.distill_and_register(repo)
        return {'success': True, 'result': result}

    def _handle_search(self, args: List[str]) -> Dict:
        """处理搜索命令"""
        if not args:
            return {'error': '需要提供搜索关键词'}

        query = ' '.join(args)
        results = self.integration.skill_graph.search(query)
        return {
            'success': True,
            'results': [
                {'name': s.name, 'source': s.source, 'type': s.type}
                for s in results
            ]
        }

    def _handle_generate(self, args: List[str]) -> Dict:
        """处理生成命令"""
        if not args:
            return {'error': '需要提供任务描述'}

        task = ' '.join(args)
        result = self.integration.generate_skill_on_demand(task)
        return {'success': True, 'result': result}

    def _handle_profile(self, args: List[str]) -> Dict:
        """处理档案命令"""
        if not args:
            return {'error': '需要提供GitHub用户名'}

        username = args[0]
        self.integration.initialize_for_user(username)
        self.integration.skill_dna.analyze_github_profile(username)
        report = self.integration.skill_dna.get_expertise_report()

        return {'success': True, 'report': report}


# 全局集成实例
_integration_instance: Optional[GitHubSkillsIntegration] = None


def get_integration() -> GitHubSkillsIntegration:
    """获取全局集成实例"""
    global _integration_instance
    if _integration_instance is None:
        _integration_instance = GitHubSkillsIntegration()
    return _integration_instance


def initialize_github_skills(user_id: Optional[str] = None) -> GitHubSkillsIntegration:
    """
    初始化GitHub技能系统

    Args:
        user_id: 用户ID

    Returns:
        集成实例
    """
    integration = get_integration()

    if user_id:
        integration.initialize_for_user(user_id)

    return integration
