"""
缓存管理模块
管理技能索引的持久化缓存
"""

import os
import json
import time
from typing import Dict, Any, Optional
from pathlib import Path

from skill_index import SkillIndex
from validation import validate_cache_path
from exceptions import CacheError, PathTraversalError


class CacheManager:
    """缓存管理器"""

    def __init__(self, cache_path: str = 'skill_index.json', project_root: str = None):
        """
        初始化缓存管理器

        Args:
            cache_path: 缓存文件路径（可以是文件名或完整路径）
            project_root: 项目根目录（默认为当前目录）

        Raises:
            PathTraversalError: 路径遍历检测
        """
        if project_root is None:
            project_root = os.getcwd()

        self.project_root = project_root

        try:
            # 验证并规范化缓存路径
            self.cache_path = validate_cache_path(cache_path, project_root)
        except Exception as e:
            raise CacheError(f"Invalid cache path '{cache_path}': {e}")

        self.cache_data = None

    def load(self) -> Optional[Dict[str, Any]]:
        """
        从缓存加载索引

        Returns:
            缓存的索引数据，如果缓存不存在或过期返回 None

        Raises:
            CacheError: 缓存读取失败
        """
        if not self.cache_path.exists():
            return None

        try:
            with self.cache_path.open('r', encoding='utf-8') as f:
                self.cache_data = json.load(f)

            # 检查缓存是否过期（24小时）
            cache_time = self.cache_data.get('_cache_time', 0)
            if time.time() - cache_time > 86400:  # 24小时
                return None

            return self.cache_data
        except json.JSONDecodeError as e:
            raise CacheError(f"Invalid JSON in cache file: {e}")
        except IOError as e:
            raise CacheError(f"Failed to read cache file: {e}")

    def save(self, index: SkillIndex):
        """
        保存索引到缓存

        Args:
            index: 技能索引对象

        Raises:
            CacheError: 缓存保存失败
        """
        cache_data = {
            '_cache_time': time.time(),
            '_version': '1.0',
            'index': index.to_dict(),
        }

        try:
            # 确保目录存在
            self.cache_path.parent.mkdir(parents=True, exist_ok=True)

            with self.cache_path.open('w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            raise CacheError(f"Failed to save cache: {e}")

    def is_valid(self, skills_root: str) -> bool:
        """
        检查缓存是否有效（优化版）

        Args:
            skills_root: 技能根目录

        Returns:
            缓存是否有效
        """
        if not self.cache_path.exists():
            return False

        try:
            # 检查缓存时间
            cache_data = self.load()
            if not cache_data:
                return False

            cache_time = cache_data.get('_cache_time', 0)

            # 提前检查：如果缓存太旧，直接返回
            if time.time() - cache_time > 86400:  # 24小时
                return False

            # 使用Path和生成器，减少文件系统调用
            skills_path = Path(skills_root)

            # 只检查SKILL.md文件，使用glob一次性获取
            skill_files = skills_path.glob('*/SKILL.md')

            # 懒加载：找到第一个过期的就返回
            return not any(
                f.stat().st_mtime > cache_time
                for f in skill_files
            )
        except (OSError, PermissionError) as e:
            print(f"⚠️  缓存验证失败: {e}")
            return False

    def clear(self):
        """
        清除缓存

        Raises:
            CacheError: 缓存删除失败
        """
        try:
            if self.cache_path.exists():
                self.cache_path.unlink()
            self.cache_data = None
        except OSError as e:
            raise CacheError(f"Failed to delete cache file: {e}")

    def get_age(self) -> float:
        """
        获取缓存年龄（秒）

        Returns:
            缓存年龄，如果缓存不存在返回 -1
        """
        if not self.cache_path.exists():
            return -1

        try:
            return time.time() - self.cache_path.stat().st_mtime
        except OSError:
            return -1


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
