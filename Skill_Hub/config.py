"""
Skill Hub - Configuration Management
配置管理模块
"""

import os
import yaml
from pathlib import Path
from typing import Optional, Dict, Any
from dataclasses import dataclass, field


@dataclass
class SourceConfig:
    """数据源配置"""
    enabled: bool = True
    priority: int = 1
    api_key: Optional[str] = None
    auto_update: bool = True


@dataclass
class EvaluationConfig:
    """评估配置"""
    overlap_threshold: float = 0.8      # 重复度阈值
    quality_threshold: float = 0.6       # 质量阈值 (0-1)
    auto_adapt: bool = True             # 自动适配


@dataclass
class IntegrationConfig:
    """MindSymphony 集成配置"""
    skills_path: str = ""
    router_path: str = ""
    auto_register: bool = True          # 自动注册到 Intent Router
    scan_on_startup: bool = True


@dataclass
class SecurityConfig:
    """安全配置"""
    scan_on_install: bool = True        # 安装前安全扫描
    allow_unknown_sources: bool = False
    max_dependency_count: int = 20      # 最大依赖数量


@dataclass
class Config:
    """主配置"""
    # 数据源配置
    skillslm: SourceConfig = field(default_factory=SourceConfig)
    local: SourceConfig = field(default_factory=lambda: SourceConfig(
        enabled=True, priority=0, auto_update=False
    ))
    fortytwoplugin: SourceConfig = field(default_factory=SourceConfig)
    github: SourceConfig = field(default_factory=SourceConfig)

    # 功能配置
    evaluation: EvaluationConfig = field(default_factory=EvaluationConfig)
    integration: IntegrationConfig = field(default_factory=IntegrationConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)

    # 缓存配置
    cache_dir: str = ""
    db_path: str = ""

    def __post_init__(self):
        """初始化默认路径"""
        if not self.cache_dir:
            self.cache_dir = os.path.expanduser("~/.skill-hub/cache")
        if not self.db_path:
            self.db_path = os.path.expanduser("~/.skill-hub/skills.db")
        if not self.integration.skills_path:
            # 默认使用 MindSymphony skills 目录
            self.integration.skills_path = os.path.expanduser("~/.claude/skills")


class ConfigManager:
    """配置管理器"""

    DEFAULT_CONFIG_PATHS = [
        "./skill-hub.config.yml",
        os.path.expanduser("~/.skill-hub/config.yml"),
        os.path.expanduser("~/.claude/skill-hub.config.yml"),
    ]

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path
        self.config = Config()

    def load(self) -> Config:
        """加载配置"""
        # 尝试多个路径
        paths_to_try = [self.config_path] + self.DEFAULT_CONFIG_PATHS
        paths_to_try = [p for p in paths_to_try if p]

        for path in paths_to_try:
            if os.path.exists(path):
                return self._load_from_file(path)

        # 没找到配置文件，使用默认配置
        return self.config

    def _load_from_file(self, path: str) -> Config:
        """从文件加载配置"""
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f) or {}

        return self._parse_config(data)

    def _parse_config(self, data: Dict[str, Any]) -> Config:
        """解析配置数据"""
        config = Config()

        # 解析数据源配置
        if 'sources' in data:
            sources = data['sources']
            for name, src_data in sources.items():
                if hasattr(config, name):
                    src_cfg = SourceConfig(
                        enabled=src_data.get('enabled', True),
                        priority=src_data.get('priority', 1),
                        api_key=src_data.get('api_key'),
                        auto_update=src_data.get('auto_update', True)
                    )
                    setattr(config, name, src_cfg)

        # 解析评估配置
        if 'evaluation' in data:
            eval_data = data['evaluation']
            config.evaluation = EvaluationConfig(
                overlap_threshold=eval_data.get('overlap_threshold', 0.8),
                quality_threshold=eval_data.get('quality_threshold', 0.6),
                auto_adapt=eval_data.get('auto_adapt', True)
            )

        # 解析集成配置
        if 'integration' in data:
            int_data = data['integration']
            if 'mindsymphony' in int_data:
                ms_data = int_data['mindsymphony']
                config.integration = IntegrationConfig(
                    skills_path=ms_data.get('path', config.integration.skills_path),
                    router_path=ms_data.get('router_path', ""),
                    auto_register=ms_data.get('auto_register', True),
                    scan_on_startup=ms_data.get('scan_on_startup', True)
                )

        # 解析安全配置
        if 'security' in data:
            sec_data = data['security']
            config.security = SecurityConfig(
                scan_on_install=sec_data.get('scan_on_install', True),
                allow_unknown_sources=sec_data.get('allow_unknown_sources', False),
                max_dependency_count=sec_data.get('max_dependency_count', 20)
            )

        # 解析缓存配置
        if 'cache' in data:
            cache_data = data['cache']
            config.cache_dir = cache_data.get('dir', config.cache_dir)
            config.db_path = cache_data.get('db_path', config.db_path)

        return config

    def save(self, path: Optional[str] = None) -> None:
        """保存配置到文件"""
        save_path = path or self.config_path or "./skill-hub.config.yml"

        # 确保目录存在
        os.makedirs(os.path.dirname(save_path) or ".", exist_ok=True)

        data = {
            'sources': {
                'skillslm': {
                    'enabled': self.config.skillslm.enabled,
                    'priority': self.config.skillslm.priority,
                    'auto_update': self.config.skillslm.auto_update,
                },
                'local': {
                    'enabled': self.config.local.enabled,
                    'path': self.config.integration.skills_path,
                    'scan_on_startup': self.config.integration.scan_on_startup,
                },
                'fortytwoplugin': {
                    'enabled': self.config.fortytwoplugin.enabled,
                    'api_key': self.config.fortytwoplugin.api_key or '${FORTY_TWO_PLUGIN_KEY}',
                },
                'github': {
                    'enabled': self.config.github.enabled,
                }
            },
            'evaluation': {
                'overlap_threshold': self.config.evaluation.overlap_threshold,
                'quality_threshold': self.config.evaluation.quality_threshold,
                'auto_adapt': self.config.evaluation.auto_adapt,
            },
            'integration': {
                'mindsymphony': {
                    'path': self.config.integration.skills_path,
                    'router_path': self.config.integration.router_path,
                    'auto_register': self.config.integration.auto_register,
                    'scan_on_startup': self.config.integration.scan_on_startup,
                }
            },
            'security': {
                'scan_on_install': self.config.security.scan_on_install,
                'allow_unknown_sources': self.config.security.allow_unknown_sources,
                'max_dependency_count': self.config.security.max_dependency_count,
            },
            'cache': {
                'dir': self.config.cache_dir,
                'db_path': self.config.db_path,
            }
        }

        with open(save_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True)

    def init_default_config(self, path: str = "./skill-hub.config.yml") -> None:
        """初始化默认配置文件"""
        self.config = Config()
        self.save(path)
        print(f"[OK] Created default config: {path}")


def get_config(config_path: Optional[str] = None) -> Config:
    """获取配置的便捷函数"""
    manager = ConfigManager(config_path)
    return manager.load()
