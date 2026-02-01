"""
Skill Hub - GitHub Source Adapter
GitHub 数据源适配器（直接搜索 GitHub 上的 skills）
"""

import asyncio
import re
from typing import List, Optional
from datetime import datetime

try:
    import httpx
    HAS_HTTPX = True
except ImportError:
    HAS_HTTPX = False

from models import SkillMetadata, SourceType, SearchResult, GitHubStats
from sources.base import BaseSource


class GitHubSource(BaseSource):
    """GitHub 数据源适配器

    直接从 GitHub 搜索 skill 仓库
    """

    API_BASE = "https://api.github.com"
    SEARCH_QUERY = "claude skill in:readme filename:SKILL.md"

    def __init__(self, config=None):
        super().__init__(config)
        self.enabled = HAS_HTTPX

    def _get_cli_name(self) -> str:
        """GitHub 数据源需要 git 工具"""
        return "git"

    @property
    def source_type(self) -> SourceType:
        return SourceType.GITHUB

    async def search(self, query: str, **kwargs) -> List[SearchResult]:
        """从 GitHub 搜索 skills"""
        if not HAS_HTTPX:
            print("❌ 需要安装 httpx: pip install httpx")
            return []

        search_query = f"{query} {self.SEARCH_QUERY}"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.API_BASE}/search/repositories",
                    params={"q": search_query, "per_page": 30},
                    timeout=30.0
                )

                if response.status_code == 200:
                    data = response.json()
                    return self._parse_search_results(data.get('items', []))
                else:
                    print(f"GitHub API 错误: {response.status_code}")
                    return []

        except Exception as e:
            print(f"搜索错误: {e}")
            return []

    def _parse_search_results(self, items: List[dict]) -> List[SearchResult]:
        """解析 GitHub 搜索结果"""
        results = []

        for item in items:
            results.append(SearchResult(
                name=item['name'],
                source=SourceType.GITHUB,
                description=item.get('description', ''),
                url=item['html_url'],
            ))

        return results

    async def get_metadata(self, name: str, url: str = "") -> Optional[SkillMetadata]:
        """获取 GitHub 仓库的 skill 元数据"""
        if not HAS_HTTPX:
            return None

        # 从 URL 提取 owner/repo
        if not url:
            return None

        match = re.search(r'github\.com/([^/]+)/([^/]+)', url)
        if not match:
            return None

        owner, repo = match.groups()
        repo = repo.replace('.git', '')

        try:
            async with httpx.AsyncClient() as client:
                # 获取仓库信息
                repo_response = await client.get(
                    f"{self.API_BASE}/repos/{owner}/{repo}",
                    timeout=10.0
                )

                if repo_response.status_code != 200:
                    return None

                repo_data = repo_response.json()

                # 尝试获取 SKILL.md
                skill_content = await self._fetch_file_content(
                    client, owner, repo, "SKILL.md"
                )

                # 尝试获取 README
                readme_content = await self._fetch_file_content(
                    client, owner, repo, "README.md"
                )

                return self._build_metadata(
                    name,
                    url,
                    repo_data,
                    skill_content,
                    readme_content
                )

        except Exception as e:
            print(f"获取元数据错误: {e}")
            return None

    async def _fetch_file_content(
        self, client: httpx.AsyncClient,
        owner: str, repo: str, path: str
    ) -> Optional[str]:
        """获取文件内容"""
        try:
            response = await client.get(
                f"{self.API_BASE}/repos/{owner}/{repo}/contents/{path}",
                timeout=10.0
            )

            if response.status_code == 200:
                data = response.json()
                # 如果是 base64 编码
                if data.get('encoding') == 'base64':
                    import base64
                    return base64.b64decode(data['content']).decode('utf-8')
                # 如果是直接内容
                return data.get('content', '')
        except:
            pass

        return None

    def _build_metadata(
        self, name: str, url: str,
        repo_data: dict, skill_content: Optional[str],
        readme_content: Optional[str]
    ) -> SkillMetadata:
        """构建元数据对象"""

        # 解析 frontmatter
        frontmatter = {}
        description = repo_data.get('description', '')
        triggers = {}
        tags = []

        if skill_content:
            frontmatter, body = self._parse_frontmatter(skill_content)
            description = frontmatter.get('description', description) or body[:200]
            triggers = frontmatter.get('triggers', {})
            tags = frontmatter.get('tags', [])

        # GitHub 统计
        github_stats = GitHubStats(
            stars=repo_data.get('stargazers_count', 0),
            forks=repo_data.get('forks_count', 0),
            watchers=repo_data.get('watchers_count', 0),
            open_issues=repo_data.get('open_issues_count', 0),
            license=repo_data.get('license', {}).get('name') if repo_data.get('license') else None,
        )

        # 最后提交时间
        if repo_data.get('pushed_at'):
            try:
                github_stats.last_commit = datetime.fromisoformat(
                    repo_data['pushed_at'].replace('Z', '+00:00')
                )
            except:
                pass

        return SkillMetadata(
            name=name,
            source=SourceType.GITHUB,
            description=description,
            author=repo_data.get('owner', {}).get('login', ''),
            url=url,
            repo_url=url,
            triggers=triggers,
            tags=tags,
            frontmatter=frontmatter,
            github_stats=github_stats,
            readme_content=readme_content or "",
        )

    def _parse_frontmatter(self, content: str) -> tuple:
        """解析 frontmatter"""
        import yaml

        frontmatter = {}
        body = content

        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                try:
                    frontmatter = yaml.safe_load(parts[1]) or {}
                    body = parts[2].strip()
                except:
                    body = content

        return frontmatter, body

    async def download(self, name: str, dest_path: str) -> bool:
        """克隆 GitHub 仓库"""
        import subprocess

        try:
            # dest_path 应该是最终 skill 的路径
            # 如果是 GitHub 仓库，需要克隆后提取 skill 目录
            result = subprocess.run(
                ["git", "clone", "--depth", "1", f"https://github.com/{name}", dest_path],
                capture_output=True,
                text=True,
                timeout=120
            )

            return result.returncode == 0

        except subprocess.TimeoutExpired:
            print("克隆超时")
            return False
        except Exception as e:
            print(f"克隆错误: {e}")
            return False

    async def list(self) -> List[SearchResult]:
        """列出（通过搜索空字符串）"""
        return await self.search("")
