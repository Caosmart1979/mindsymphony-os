"""
Skill Hub - Base Source Adapter
数据源适配器基类
"""

import subprocess
from abc import ABC, abstractmethod
from typing import List, Optional
from models import SkillMetadata, SourceType, SearchResult


class BaseSource(ABC):
    """数据源适配器基类"""

    def __init__(self, config=None):
        self.config = config
        self.enabled = True

    @abstractmethod
    def _get_cli_name(self) -> str:
        """返回 CLI 工具名称（子类实现）"""
        pass

    @abstractmethod
    async def search(self, query: str, **kwargs) -> List[SearchResult]:
        """搜索技能"""
        pass

    @abstractmethod
    async def get_metadata(self, name: str, url: str = "") -> Optional[SkillMetadata]:
        """获取技能元数据（不下载本体）"""
        pass

    @abstractmethod
    async def download(self, name: str, dest_path: str) -> bool:
        """下载技能到指定目录"""
        pass

    @abstractmethod
    async def list(self) -> List[SearchResult]:
        """列出所有可用技能"""
        pass

    @property
    @abstractmethod
    def source_type(self) -> SourceType:
        """返回数据源类型"""
        pass

    def _check_cli(self) -> bool:
        """检查 CLI 工具是否可用（通用方法）"""
        cli_name = self._get_cli_name()
        if not cli_name:
            # 本地数据源不需要 CLI
            self.enabled = True
            return True

        try:
            import shutil
            # 首先检查命令是否存在，并获取完整路径
            cli_path = shutil.which(cli_name)
            if not cli_path:
                self.enabled = False
                return False

            result = subprocess.run(
                [cli_path, "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            self.enabled = result.returncode == 0
            return self.enabled
        except (FileNotFoundError, subprocess.TimeoutExpired):
            self.enabled = False
            return False

    def normalize_name(self, name: str) -> str:
        """标准化技能名称"""
        return name.strip().lower().replace(' ', '-')

    def is_available(self) -> bool:
        """检查数据源是否可用"""
        return self.enabled
