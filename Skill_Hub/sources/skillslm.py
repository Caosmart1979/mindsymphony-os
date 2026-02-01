"""
Skill Hub - Skillslm Source Adapter
skillslm CLI 的数据源适配器
"""

import asyncio
import subprocess
import json
import re
from typing import List, Optional
from pathlib import Path

from models import SkillMetadata, SourceType, SearchResult
from sources.base import BaseSource


class SkillslmSource(BaseSource):
    """skillslm 数据源适配器

    skillslm 是访问 anthropics/skills 官方库的 CLI 工具
    """

    CLI_NAME = "skillslm"

    def __init__(self, config=None):
        super().__init__(config)
        self._cli_available = self._check_cli()
        self._cli_path = None
        if self._cli_available:
            import shutil
            self._cli_path = shutil.which(self.CLI_NAME)

    def _get_cli_name(self) -> str:
        """返回 CLI 工具名称"""
        return self.CLI_NAME

    @property
    def source_type(self) -> SourceType:
        return SourceType.SKILLSLM

    async def search(self, query: str, **kwargs) -> List[SearchResult]:
        """从 anthropics/skills 搜索

        由于 skillslm 没有 search 命令，我们使用 list 命令获取所有技能，然后在本地过滤
        """
        if not self._cli_available:
            return []

        # 获取所有技能
        all_skills = await self.list()

        # 在本地过滤匹配的技能
        query_lower = query.lower()
        results = []
        for skill in all_skills:
            if (query_lower in skill.name.lower() or
                (skill.description and query_lower in skill.description.lower())):
                results.append(skill)

        return results

    async def get_metadata(self, name: str, url: str = "") -> Optional[SkillMetadata]:
        """获取 skill 元数据

        从 GitHub 获取 SKILL.md 和 README 内容
        """
        if not self._cli_available:
            return None

        # 构建官方仓库 URL
        repo_url = f"https://github.com/anthropics/skills/tree/main/{name}"

        try:
            # 这里需要使用 GitHub API 获取文件内容
            # 简化实现：返回基础元数据
            return SkillMetadata(
                name=name,
                source=SourceType.SKILLSLM,
                url=f"https://github.com/anthropics/skills/tree/main/{name}",
                repo_url=repo_url,
                description=f"Official skill: {name}",
                author="anthropics",
            )
        except Exception as e:
            print(f"Error fetching metadata for {name}: {e}")
            return None

    async def download(self, name: str, dest_path: str) -> bool:
        """使用 skillslm CLI 下载 skill"""
        if not self._cli_available:
            print("❌ skillslm CLI 不可用")
            return False

        try:
            # skillslm install 会安装到默认位置
            # 我们需要复制到目标位置
            result = subprocess.run(
                [self._cli_path, "install", name],
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0:
                # 查找安装位置并复制到 dest_path
                # 这需要根据 skillslm 的实际行为来实现
                print(f"✓ 已下载 {name}")
                return True
            else:
                print(f"❌ 下载失败: {result.stderr}")
                return False

        except subprocess.TimeoutExpired:
            print("❌ 下载超时")
            return False
        except Exception as e:
            print(f"❌ 下载错误: {e}")
            return False

    async def list(self) -> List[SearchResult]:
        """列出 anthropics/skills 中的所有 skills

        使用 skillslm list 命令
        """
        if not self._cli_available:
            return []

        try:
            result = subprocess.run(
                [self._cli_path, "list"],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                # 解析输出
                return self._parse_list_output(result.stdout)
            return []

        except Exception as e:
            print(f"Error listing skills: {e}")
            return []

    def _parse_list_output(self, output: str) -> List[SearchResult]:
        """解析 skillslm list 的输出"""
        results = []
        for line in output.strip().split('\n'):
            line = line.strip()
            if line and not line.startswith('🎯') and not line.startswith('💡') and not line.startswith('📚'):
                # 技能名称以多个空格分隔，需要分割
                parts = line.split()
                for name in parts:
                    if name:
                        results.append(SearchResult(
                            name=name,
                            source=SourceType.SKILLSLM,
                            description=f"Official skill: {name}",
                            url=f"https://github.com/anthropics/skills/tree/main/{name}",
                        ))
        return results

    async def install_from_url(self, url: str, dest_path: str) -> bool:
        """从 GitHub URL 直接安装"""
        try:
            # 解析 URL 获取 skill 名称
            # 例如: https://github.com/user/repo/tree/main/skill-name
            match = re.search(r'/tree/main/([^/]+)', url)
            if match:
                name = match.group(1)
                return await self.download(name, dest_path)
            return False
        except Exception as e:
            print(f"Error installing from URL: {e}")
            return False
