"""
Skill Hub - Local Source Adapter
本地文件系统数据源适配器
"""

import os
import re
import yaml
from pathlib import Path
from typing import List, Optional

from models import SkillMetadata, SourceType, SearchResult
from sources.base import BaseSource


class LocalSource(BaseSource):
    """本地数据源适配器

    扫描本地 skills 目录
    """

    def __init__(self, config=None):
        super().__init__(config)
        self.skills_path = config.integration.skills_path if config else None
        if not self.skills_path:
            self.skills_path = os.path.expanduser("~/.claude/skills")

    def _get_cli_name(self) -> str:
        """本地数据源不需要 CLI 工具"""
        return ""

    @property
    def source_type(self) -> SourceType:
        return SourceType.LOCAL

    async def search(self, query: str, **kwargs) -> List[SearchResult]:
        """搜索本地 skills"""
        results = []
        query_lower = query.lower()

        for skill_path in self._iter_skill_dirs():
            metadata = await self._load_skill_from_path(skill_path)
            if metadata:
                # 匹配名称或描述
                if (query_lower in metadata.name.lower() or
                    query_lower in metadata.description.lower()):
                    results.append(SearchResult(
                        name=metadata.name,
                        source=SourceType.LOCAL,
                        description=metadata.description,
                        url=skill_path,
                        metadata=metadata,
                    ))

        return results

    async def get_metadata(self, name: str, url: str = "") -> Optional[SkillMetadata]:
        """获取本地 skill 元数据"""
        if url:
            return await self._load_skill_from_path(url)

        # 通过名称查找
        for skill_path in self._iter_skill_dirs():
            if Path(skill_path).name == name:
                return await self._load_skill_from_path(skill_path)

        return None

    async def download(self, name: str, dest_path: str) -> bool:
        """本地 source 不需要下载"""
        print("本地 skill 无需下载")
        return True

    async def list(self) -> List[SearchResult]:
        """列出所有本地 skills"""
        results = []

        for skill_path in self._iter_skill_dirs():
            metadata = await self._load_skill_from_path(skill_path)
            if metadata:
                results.append(SearchResult(
                    name=metadata.name,
                    source=SourceType.LOCAL,
                    description=metadata.description,
                    url=skill_path,
                    metadata=metadata,
                ))

        return results

    def _iter_skill_dirs(self):
        """迭代所有 skill 目录"""
        if not os.path.exists(self.skills_path):
            return

        for entry in os.listdir(self.skills_path):
            path = os.path.join(self.skills_path, entry)
            if os.path.isdir(path) and not entry.startswith('.'):
                yield path

    async def _load_skill_from_path(self, path: str) -> Optional[SkillMetadata]:
        """从路径加载 skill 元数据"""
        skill_name = os.path.basename(path)

        # 查找 SKILL.md
        skill_file = os.path.join(path, "SKILL.md")
        if not os.path.exists(skill_file):
            # 尝试小写
            skill_file = os.path.join(path, "skill.md")

        if not os.path.exists(skill_file):
            # 没有 SKILL.md，返回基本信息
            return SkillMetadata(
                name=skill_name,
                source=SourceType.LOCAL,
                description=f"Local skill: {skill_name}",
                url=path,
            )

        try:
            with open(skill_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # 解析 frontmatter
            frontmatter, body = self._parse_frontmatter(content)

            # 提取描述
            description = frontmatter.get('description', '')
            if not description and body:
                # 取第一段作为描述
                first_para = body.split('\n\n')[0].strip()
                description = first_para[:200]

            # 提取触发词
            triggers = frontmatter.get('triggers', {})
            if isinstance(triggers, list):
                triggers = {'zh': triggers, 'en': []}

            # 提取标签
            tags = frontmatter.get('tags', [])
            if isinstance(tags, str):
                tags = [tags]

            return SkillMetadata(
                name=skill_name,
                source=SourceType.LOCAL,
                description=description,
                author=frontmatter.get('author', ''),
                url=path,
                triggers=triggers,
                tags=tags,
                frontmatter=frontmatter,
                readme_content=body[:1000],  # 前1000字符
                file_list=self._list_files(path),
            )

        except Exception as e:
            print(f"Error loading {skill_name}: {e}")
            return None

    def _parse_frontmatter(self, content: str) -> tuple:
        """解析 frontmatter"""
        frontmatter = {}
        body = content

        # 检查是否有 YAML frontmatter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                try:
                    frontmatter = yaml.safe_load(parts[1]) or {}
                    body = parts[2].strip()
                except:
                    body = content

        return frontmatter, body

    def _list_files(self, path: str) -> List[str]:
        """列出目录中的文件"""
        files = []
        try:
            for root, dirs, filenames in os.walk(path):
                # 跳过隐藏目录和 venv
                dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'venv']

                for filename in filenames:
                    if not filename.startswith('.'):
                        rel_path = os.path.relpath(
                            os.path.join(root, filename),
                            path
                        )
                        files.append(rel_path)
        except Exception:
            pass

        return files
