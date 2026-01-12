"""
缓存管理模块
管理技能索引的持久化缓存
"""

import os
import json
import time
from typing import Dict, Any, Optional
from skill_index import SkillIndex


class CacheManager:
    """缓存管理器"""

    def __init__(self, cache_path: str = 'skill_index.json'):
        self.cache_path = cache_path
        self.cache_data = None

    def load(self) -> Optional[Dict[str, Any]]:
        """
        从缓存加载索引

        Returns:
            缓存的索引数据，如果缓存不存在或过期返回 None
        """
        if not os.path.exists(self.cache_path):
            return None

        try:
            with open(self.cache_path, 'r', encoding='utf-8') as f:
                self.cache_data = json.load(f)

            # 检查缓存是否过期（24小时）
            cache_time = self.cache_data.get('_cache_time', 0)
            if time.time() - cache_time > 86400:  # 24小时
                return None

            return self.cache_data
        except (json.JSONDecodeError, IOError):
            return None

    def save(self, index: SkillIndex):
        """
        保存索引到缓存

        Args:
            index: 技能索引对象
        """
        cache_data = {
            '_cache_time': time.time(),
            '_version': '1.0',
            'index': index.to_dict(),
        }

        try:
            with open(self.cache_path, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"⚠️  保存缓存失败: {e}")

    def is_valid(self, skills_root: str) -> bool:
        """
        检查缓存是否有效

        Args:
            skills_root: 技能根目录

        Returns:
            缓存是否有效
        """
        if not os.path.exists(self.cache_path):
            return False

        # 检查缓存时间
        cache_data = self.load()
        if not cache_data:
            return False

        # 检查技能文件是否更新
        cache_time = cache_data.get('_cache_time', 0)

        for item in os.listdir(skills_root):
            skill_dir = os.path.join(skills_root, item)
            if not os.path.isdir(skill_dir):
                continue

            skill_md = os.path.join(skill_dir, 'SKILL.md')
            if os.path.exists(skill_md):
                if os.path.getmtime(skill_md) > cache_time:
                    return False  # 技能文件已更新，缓存失效

        return True

    def clear(self):
        """清除缓存"""
        if os.path.exists(self.cache_path):
            os.remove(self.cache_path)
        self.cache_data = None

    def get_age(self) -> float:
        """
        获取缓存年龄（秒）

        Returns:
            缓存年龄，如果缓存不存在返回 -1
        """
        if not os.path.exists(self.cache_path):
            return -1

        return time.time() - os.path.getmtime(self.cache_path)


if __name__ == '__main__':
    # 测试代码
    cache = CacheManager('test_cache.json')

    # 测试保存和加载
    from skill_index import SkillIndex
    import os

    skills_root = os.path.join(os.path.dirname(__file__), '..', 'skills')
    index = SkillIndex(skills_root)

    print("💾 保存缓存...")
    cache.save(index)

    print("📖 加载缓存...")
    cached_data = cache.load()
    if cached_data:
        print(f"✅ 缓存加载成功")
        print(f"   缓存时间: {cached_data.get('_cache_time')}")
        print(f"   技能数量: {len(cached_data['index']['skills'])}")

    print(f"\n⏱️  缓存年龄: {cache.get_age():.2f} 秒")

    print(f"\n✓ 缓存有效: {cache.is_valid(skills_root)}")
