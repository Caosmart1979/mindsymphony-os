"""
技能索引模块
构建和管理多维度技能索引
"""

from typing import Dict, List, Set, Any
from collections import defaultdict
from skill_metadata import SkillMetadata, load_all_skills


class SkillIndex:
    """技能索引类"""

    def __init__(self, skills_root: str):
        self.skills_root = skills_root
        self.skills: Dict[str, SkillMetadata] = {}
        self._indexes = {
            'by_name': {},
            'by_category': defaultdict(list),
            'by_tag': defaultdict(list),
            'by_provides': defaultdict(list),
            'by_consumes': defaultdict(list),
            'by_related': defaultdict(list),
        }
        self._build()

    def _build(self):
        """构建索引"""
        # 加载所有技能
        self.skills = load_all_skills(self.skills_root)

        # 清空现有索引
        for index in self._indexes.values():
            if isinstance(index, dict):
                index.clear()
            elif isinstance(index, defaultdict):
                for key in list(index.keys()):
                    del index[key]

        # 构建新索引
        for name, metadata in self.skills.items():
            # 按名称索引
            self._indexes['by_name'][name] = metadata

            # 按分类索引
            category = metadata.get('category')
            if category:
                self._indexes['by_category'][category].append(name)

            # 按标签索引
            for tag in metadata.get('tags', []):
                self._indexes['by_tag'][tag].append(name)

            # 按 provides 索引（处理字符串或字典）
            for provides in metadata.provides():
                if isinstance(provides, dict):
                    provides_id = provides.get('id', str(provides))
                else:
                    provides_id = provides
                self._indexes['by_provides'][provides_id].append(name)

            # 按 consumes 索引（处理字符串或字典）
            for consumes in metadata.consumes():
                if isinstance(consumes, dict):
                    consumes_id = consumes.get('id', str(consumes))
                else:
                    consumes_id = consumes
                self._indexes['by_consumes'][consumes_id].append(name)

            # 按 related 索引
            for related in metadata.get('related', []):
                self._indexes['by_related'][related].append(name)

    def rebuild(self):
        """重建索引"""
        self._build()

    def incremental_update(self):
        """增量更新索引（只重新扫描变更的技能）"""
        for name, metadata in list(self.skills.items()):
            if metadata.is_stale():
                # 重新加载这个技能
                new_metadata = load_skill_metadata(metadata.get('_path'))
                if new_metadata:
                    self.skills[name] = new_metadata

        # 重建索引
        self._build()

    def get_by_name(self, name: str) -> SkillMetadata:
        """按名称获取技能"""
        return self._indexes['by_name'].get(name)

    def get_by_category(self, category: str) -> List[str]:
        """按分类获取技能列表"""
        return self._indexes['by_category'].get(category, []).copy()

    def get_by_tag(self, tag: str) -> List[str]:
        """按标签获取技能列表"""
        return self._indexes['by_tag'].get(tag, []).copy()

    def get_providers(self, resource: str) -> List[str]:
        """查找提供特定资源的技能"""
        return self._indexes['by_provides'].get(resource, []).copy()

    def get_consumers(self, resource: str) -> List[str]:
        """查找消耗特定资源的技能"""
        return self._indexes['by_consumes'].get(resource, []).copy()

    def get_related(self, skill_name: str) -> List[str]:
        """查找相关技能"""
        related_skills = self._indexes['by_related'].get(skill_name, [])
        # 同时检查技能的 related 字段
        metadata = self.get_by_name(skill_name)
        if metadata:
            skill_related = metadata.get('related', [])
            related_skills.extend(skill_related)
        return list(set(related_skills))

    def search(self, query: str) -> List[str]:
        """
        搜索技能

        在名称、描述、标签中搜索
        """
        query = query.lower()
        results = set()

        for name, metadata in self.skills.items():
            # 搜索名称
            if query in name.lower():
                results.add(name)
                continue

            # 搜索描述
            description = metadata.get('description', '')
            if query in description.lower():
                results.add(name)
                continue

            # 搜索标签
            for tag in metadata.get('tags', []):
                if query in tag.lower():
                    results.add(name)
                    break

        return list(results)

    def get_all_categories(self) -> List[str]:
        """获取所有分类"""
        return list(self._indexes['by_category'].keys())

    def get_all_tags(self) -> List[str]:
        """获取所有标签"""
        return list(self._indexes['by_tag'].keys())

    def get_all_resources(self) -> List[str]:
        """获取所有资源类型（provides + consumes）"""
        resources = set(self._indexes['by_provides'].keys())
        resources.update(self._indexes['by_consumes'].keys())
        return list(resources)

    def get_statistics(self) -> Dict[str, Any]:
        """获取索引统计信息"""
        return {
            'total_skills': len(self.skills),
            'categories': dict(self._indexes['by_category']),
            'tags_count': len(self._indexes['by_tag']),
            'resources_count': len(self.get_all_resources()),
        }

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典（用于序列化）"""
        return {
            'skills': {name: metadata.to_dict() for name, metadata in self.skills.items()},
            'statistics': self.get_statistics(),
        }


if __name__ == '__main__':
    # 测试代码
    import os
    skills_root = os.path.join(os.path.dirname(__file__), '..', 'skills')
    index = SkillIndex(skills_root)

    print("📊 技能索引统计:")
    stats = index.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")

    print("\n🏷️  所有分类:")
    for category in index.get_all_categories():
        print(f"  - {category}: {len(index.get_by_category(category))} 个技能")

    print("\n🔍 搜索 'design':")
    results = index.search('design')
    for result in results:
        print(f"  - {result}")
