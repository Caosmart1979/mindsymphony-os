"""
Skill Hub - 42Plugin Source Adapter
42plugin.com 市场数据源适配器
"""

import asyncio
import subprocess
from typing import List, Optional

from models import SkillMetadata, SourceType, SearchResult
from sources.base import BaseSource


class FortyTwoPluginSource(BaseSource):
    """42plugin 数据源适配器

    连接 42plugin.com 技能市场
    """

    BASE_URL = "https://42plugin.com/api"
    WEB_URL = "https://42plugin.com"
    CLI_NAME = "42plugin"

    def __init__(self, config=None):
        super().__init__(config)
        self._cli_available = self._check_cli()
        self.api_key = config.fortytwoplugin.api_key if config else None
        self._cli_path = None
        if self._cli_available:
            import shutil
            self._cli_path = shutil.which(self.CLI_NAME)

    def _get_cli_name(self) -> str:
        """返回 CLI 工具名称"""
        return self.CLI_NAME

    @property
    def source_type(self) -> SourceType:
        return SourceType.FORTY_TWO_PLUGIN

    async def search(self, query: str, **kwargs) -> List[SearchResult]:
        """从 42plugin 市场搜索

        参数:
            query: 搜索关键词
            plugin_type: 插件类型 (skill|command|hook|agent)
        """
        if self._cli_available:
            return await self._search_via_cli(query, **kwargs)
        else:
            return await self._search_via_api(query, **kwargs)

    async def _search_via_cli(self, query: str, **kwargs) -> List[SearchResult]:
        """通过 CLI 搜索"""
        try:
            # 构建命令
            cmd = [self._cli_path, "search", query, "--type", "skill", "--json"]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                return self._parse_search_output(result.stdout)
            return []

        except subprocess.TimeoutExpired:
            print("搜索超时")
            return []
        except Exception as e:
            print(f"搜索错误: {e}")
            return []

    async def _search_via_api(self, query: str, **kwargs) -> List[SearchResult]:
        """通过 API 搜索"""
        # 需要实现 HTTP 请求
        # TODO: 实现完整的 API 调用
        return []

    def _parse_search_output(self, output: str) -> List[SearchResult]:
        """解析 CLI 搜索输出（JSON 格式）"""
        results = []

        try:
            import json
            data = json.loads(output)

            # 解析插件列表
            for plugin in data.get('plugins', []):
                results.append(SearchResult(
                    name=plugin.get('name', ''),
                    source=SourceType.FORTY_TWO_PLUGIN,
                    description=plugin.get('description', ''),
                    url=f"{self.WEB_URL}/plugins/{plugin.get('fullName', '')}",
                ))

        except json.JSONDecodeError:
            # 如果不是 JSON，尝试解析纯文本输出
            for line in output.strip().split('\n'):
                if line.strip() and not line.startswith('-'):
                    # 尝试提取有用信息
                    results.append(SearchResult(
                        name=line.strip(),
                        source=SourceType.FORTY_TWO_PLUGIN,
                        description="Plugin from 42plugin",
                        url=f"{self.WEB_URL}/search?q={line.strip()}",
                    ))

        return results

    async def get_metadata(self, name: str, url: str = "") -> Optional[SkillMetadata]:
        """获取插件元数据"""
        # TODO: 实现 API 调用获取详情
        return SkillMetadata(
            name=name,
            source=SourceType.FORTY_TWO_PLUGIN,
            description=f"Plugin from 42plugin: {name}",
            url=url or f"{self.WEB_URL}/plugins/{name}",
        )

    async def download(self, name: str, dest_path: str) -> bool:
        """使用 42plugin CLI 下载"""
        if not self._cli_available:
            print("❌ 42plugin CLI 不可用")
            return False

        try:
            result = subprocess.run(
                [self._cli_path, "install", name],
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0:
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
        """列出所有插件（类型为 skill）"""
        if self._cli_available:
            # 搜索空字符串以获取所有技能
            try:
                cmd = [self._cli_path, "search", "", "--type", "skill", "--json"]
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                if result.returncode == 0:
                    return self._parse_search_output(result.stdout)
            except Exception:
                pass
        return []
