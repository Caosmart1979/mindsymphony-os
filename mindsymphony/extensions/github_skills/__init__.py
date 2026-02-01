"""
GitHub Skills Distiller for MindSymphony v21.4
将GitHub仓库压缩为个人超级技能库

核心理念: "将整个GitHub压缩成你自己的超级技能库"

架构组件:
- GitHubSkillDistiller: 蒸馏GitHub仓库为结构化技能
- SkillKnowledgeGraph: 技能知识图谱管理系统
- SkillDNA: 个人技能DNA追踪系统
- DynamicSkillGenerator: 动态技能生成器
- GitHubSkillsIntegration: MindSymphony集成层

Usage:
    # 基础用法
    from mindsymphony.extensions.github_skills import GitHubSkillDistiller

    distiller = GitHubSkillDistiller()
    result = distiller.distill("bmad-code-org/BMAD-METHOD")
    print(result.skill_content)

    # 快速生成技能
    from mindsymphony.extensions.github_skills import generate_skill_for_task

    skill = generate_skill_for_task("分析生物信息学数据集")

    # 完整集成
    from mindsymphony.extensions.github_skills import initialize_github_skills

    github_skills = initialize_github_skills(user_id="user_001")
    result = github_skills.distill_and_register("microsoft/ai-examples")
"""

__version__ = "1.0.0"
__mindsymphony_version__ = "v21.4"
__author__ = "MindSymphony Team"

# 核心类
from .github_skill_distiller import GitHubSkillDistiller, DistillationResult, ExtractedPattern
from .skill_knowledge_graph import (
    SkillKnowledgeGraph,
    SkillNode,
    SkillRelation,
    RelationType
)
from .skill_dna import SkillDNA, UserProfile, SkillUsagePattern
from .dynamic_skill_generator import (
    DynamicSkillGenerator,
    GenerationRequest,
    GeneratedSkill
)
from .integration import (
    GitHubSkillsIntegration,
    GitHubSkillsCommandHandler,
    initialize_github_skills,
    get_integration
)

# CLI
from .cli import main as cli_main

# MindSymphony适配器
from .skill_adapter import (
    GitHubSkillAdapter,
    SkillManifest,
    Pheromone,
    PheromoneType,
    Layer,
    create_github_skill_adapter,
    distill_skill,
    search_skill_library,
    generate_skill_for_task as adapter_generate_skill,
)

__all__ = [
    # 元数据
    "__version__",
    "__mindsymphony_version__",

    # 蒸馏器
    "GitHubSkillDistiller",
    "DistillationResult",
    "ExtractedPattern",

    # 知识图谱
    "SkillKnowledgeGraph",
    "SkillNode",
    "SkillRelation",
    "RelationType",

    # 技能DNA
    "SkillDNA",
    "UserProfile",
    "SkillUsagePattern",

    # 动态生成器
    "DynamicSkillGenerator",
    "GenerationRequest",
    "GeneratedSkill",

    # 集成
    "GitHubSkillsIntegration",
    "GitHubSkillsCommandHandler",
    "initialize_github_skills",
    "get_integration",

    # CLI
    "cli_main",

    # MindSymphony适配器
    "GitHubSkillAdapter",
    "SkillManifest",
    "Pheromone",
    "PheromoneType",
    "Layer",
    "create_github_skill_adapter",
    "distill_skill",
    "search_skill_library",
    "adapter_generate_skill",

    # 便捷函数
    "distill_github_repo",
    "search_skills",
    "generate_skill_for_task",
    "analyze_github_profile",
    "get_skill_recommendations",
]


def distill_github_repo(repo_url: str, **kwargs) -> DistillationResult:
    """
    便捷函数：蒸馏GitHub仓库为技能

    Args:
        repo_url: 仓库URL或标识符 (如 "owner/repo")
        **kwargs: 额外选项
            - extract_patterns: 是否提取代码模式 (默认True)
            - include_code_examples: 是否包含代码示例 (默认True)
            - personalize: 是否个性化 (默认False)

    Returns:
        DistillationResult: 蒸馏结果

    Example:
        >>> result = distill_github_repo("microsoft/ai-examples")
        >>> print(result.skill_name)
        >>> print(result.confidence)
    """
    distiller = GitHubSkillDistiller()
    return distiller.distill(repo_url, **kwargs)


def search_skills(query: str, limit: int = 10) -> list:
    """
    便捷函数：搜索技能知识图谱

    Args:
        query: 搜索关键词
        limit: 返回数量限制

    Returns:
        list: 匹配的技能列表

    Example:
        >>> skills = search_skills("machine learning", limit=5)
        >>> for skill in skills:
        ...     print(skill.name)
    """
    graph = SkillKnowledgeGraph()
    return graph.search(query, limit=limit)


def generate_skill_for_task(task_description: str, **kwargs) -> dict:
    """
    便捷函数：为任务动态生成技能

    Args:
        task_description: 任务描述
        **kwargs: 额外选项
            - persist: 是否持久化 (默认False)
            - required_capabilities: 必需能力列表

    Returns:
        dict: 生成的技能信息

    Example:
        >>> skill = generate_skill_for_task(
        ...     "分析生物信息学数据集",
        ...     required_capabilities=["data_analysis", "visualization"]
        ... )
        >>> print(skill['name'])
        >>> print(skill['confidence'])
    """
    generator = DynamicSkillGenerator()
    return generator.generate_from_query(task_description, **kwargs)


def analyze_github_profile(github_username: str, user_id: Optional[str] = None) -> dict:
    """
    便捷函数：分析GitHub用户档案

    Args:
        github_username: GitHub用户名
        user_id: 用户ID (默认使用github_username)

    Returns:
        dict: 分析报告

    Example:
        >>> report = analyze_github_profile("octocat")
        >>> print(report['expertise_domains'])
    """
    dna = SkillDNA(user_id=user_id or github_username)
    analysis = dna.analyze_github_profile(github_username)
    report = dna.get_expertise_report()
    return {**analysis, **report}


def get_skill_recommendations(
    target_domain: str,
    user_id: Optional[str] = None
) -> list:
    """
    便捷函数：获取技能推荐

    Args:
        target_domain: 目标领域
        user_id: 用户ID

    Returns:
        list: 推荐的学习路径

    Example:
        >>> recs = get_skill_recommendations("machine_learning")
        >>> for rec in recs:
        ...     print(f"{rec['name']}: {rec['reason']}")
    """
    dna = SkillDNA(user_id=user_id or "default")
    return dna.recommend_learning_path(target_domain)


# 类型提示
from typing import Optional
