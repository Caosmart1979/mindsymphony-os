"""
技能发现系统
统一的技能发现、查询和路由 API
"""

import os
from typing import Dict, List, Any, Optional
from skill_metadata import load_all_skills, SkillMetadata
from skill_index import SkillIndex
from skill_router import SkillRouter, RouteResult
from cache_manager import CacheManager


class SkillDiscovery:
    """技能发现系统 API"""

    def __init__(self, skills_root: str, cache_path: str = 'skill_index.json'):
        """
        初始化技能发现系统

        Args:
            skills_root: 技能根目录
            cache_path: 缓存文件路径
        """
        self.skills_root = skills_root
        self.cache_path = cache_path
        self.cache_manager = CacheManager(cache_path)
        self.index = None
        self.router = None
        self._initialize()

    def _initialize(self):
        """初始化索引和路由器"""
        # 尝试从缓存加载
        if self.cache_manager.is_valid(self.skills_root):
            print("📦 从缓存加载技能索引...")
            # TODO: 实现从缓存恢复索引
            self.index = SkillIndex(self.skills_root)
        else:
            print("🔍 扫描技能并构建索引...")
            self.index = SkillIndex(self.skills_root)
            # 保存到缓存
            self.cache_manager.save(self.index)

        # 初始化路由器
        self.router = SkillRouter(self.index)

    def rebuild_index(self):
        """重建索引"""
        print("🔄 重建技能索引...")
        self.index.rebuild()
        self.cache_manager.save(self.index)

    def find_by_name(self, name: str) -> Optional[SkillMetadata]:
        """
        按名称查找技能

        Args:
            name: 技能名称

        Returns:
            技能元数据，如果未找到返回 None
        """
        return self.index.get_by_name(name)

    def find_by_category(self, category: str) -> List[str]:
        """
        按分类查找技能

        Args:
            category: 分类名称

        Returns:
            技能名称列表
        """
        return self.index.get_by_category(category)

    def find_by_tags(self, tags: List[str]) -> List[str]:
        """
        按标签查找技能

        Args:
            tags: 标签列表

        Returns:
            技能名称列表
        """
        results = []
        for tag in tags:
            results.extend(self.index.get_by_tag(tag))
        return list(set(results))

    def find_providers(self, resource: str) -> List[str]:
        """
        查找提供特定资源的技能

        Args:
            resource: 资源类型（如 design-tokens）

        Returns:
            技能名称列表
        """
        return self.index.get_providers(resource)

    def find_consumers(self, resource: str) -> List[str]:
        """
        查找消耗特定资源的技能

        Args:
            resource: 资源类型

        Returns:
            技能名称列表
        """
        return self.index.get_consumers(resource)

    def find_collaborators(self, skill_name: str) -> List[str]:
        """
        查找协作技能

        Args:
            skill_name: 技能名称

        Returns:
            协作技能列表
        """
        return self.router._infer_collaboration_chain(skill_name)

    def find_related(self, skill_name: str) -> List[str]:
        """
        查找相关技能

        Args:
            skill_name: 技能名称

        Returns:
            相关技能列表
        """
        return self.index.get_related(skill_name)

    def search(self, query: str) -> List[str]:
        """
        搜索技能

        Args:
            query: 搜索关键词

        Returns:
            匹配的技能名称列表
        """
        return self.index.search(query)

    def route(self, user_input: str) -> RouteResult:
        """
        智能路由到合适的技能

        Args:
            user_input: 用户输入

        Returns:
            路由结果
        """
        return self.router.route(user_input)

    def suggest_combination(self, task_type: str) -> Dict[str, Any]:
        """
        推荐技能组合

        Args:
            task_type: 任务类型描述

        Returns:
            技能组合方案
        """
        return self.router.suggest_combination(task_type)

    def get_all_categories(self) -> List[str]:
        """获取所有分类"""
        return self.index.get_all_categories()

    def get_all_tags(self) -> List[str]:
        """获取所有标签"""
        return self.index.get_all_tags()

    def get_all_resources(self) -> List[str]:
        """获取所有资源类型"""
        return self.index.get_all_resources()

    def get_statistics(self) -> Dict[str, Any]:
        """获取索引统计信息"""
        return self.index.get_statistics()

    def visualize_relationships(self, output_path: str = 'skill_graph.png'):
        """
        可视化技能关系图（需要 graphviz）

        Args:
            output_path: 输出文件路径
        """
        try:
            import graphviz

            dot = graphviz.Digraph(comment='Skill Relationships')
            dot.attr(rankdir='LR')

            # 添加技能节点
            for name in self.index.skills.keys():
                dot.node(name, name)

            # 添加协作关系边
            for name, metadata in self.index.skills.items():
                # consumes 关系
                for consumes in metadata.consumes():
                    providers = self.index.get_providers(consumes)
                    for provider in providers:
                        dot.edge(provider, name, label=consumes)

                # related 关系
                for related in metadata.get('related', []):
                    if related in self.index.skills:
                        dot.edge(name, related, style='dashed', color='gray')

            # 渲染
            dot.render(output_path.replace('.png', ''), format='png', view=True)
            print(f"✅ 关系图已保存到: {output_path}")

        except ImportError:
            print("⚠️  需要安装 graphviz: pip install graphviz")
        except Exception as e:
            print(f"⚠️  可视化失败: {e}")

    def export_index(self, output_path: str = 'skill_index_export.json'):
        """
        导出索引到 JSON 文件

        Args:
            output_path: 输出文件路径
        """
        import json

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.index.to_dict(), f, indent=2, ensure_ascii=False)

        print(f"✅ 索引已导出到: {output_path}")


# 便捷函数
def create_discovery_system(skills_root: str) -> SkillDiscovery:
    """
    创建技能发现系统

    Args:
        skills_root: 技能根目录

    Returns:
        SkillDiscovery 实例
    """
    return SkillDiscovery(skills_root)


if __name__ == '__main__':
    # 测试代码
    import sys
    sys.path.insert(0, os.path.dirname(__file__))

    skills_root = os.path.join(os.path.dirname(__file__), '..', 'skills')
    discovery = create_discovery_system(skills_root)

    print("\n" + "="*60)
    print("📊 技能发现系统测试")
    print("="*60)

    # 统计信息
    print("\n📈 索引统计:")
    stats = discovery.get_statistics()
    for key, value in stats.items():
        if key == 'categories':
            print(f"\n  分类:")
            for cat, skills in value.items():
                print(f"    - {cat}: {len(skills)} 个技能")
        else:
            print(f"  {key}: {value}")

    # 测试路由
    print("\n🔍 路由测试:")
    test_inputs = [
        "创建一个有品牌风格的前端组件",
        "写一个技术文档",
        "设计一个 landing page",
    ]

    for test_input in test_inputs:
        print(f"\n  输入: {test_input}")
        result = discovery.route(test_input)
        print(f"    → 主技能: {result.primary}")
        print(f"    → 协作: {result.collaborators}")
        print(f"    → 置信度: {result.confidence}%")

    # 测试协作链推理
    print("\n🔗 协作链测试:")
    for skill_name in ['frontend-design', 'doc-coauthoring']:
        collaborators = discovery.find_collaborators(skill_name)
        print(f"  {skill_name}:")
        print(f"    → {collaborators}")
