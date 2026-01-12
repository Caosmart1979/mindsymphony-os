"""
统一异常处理框架
Unified Exception Handling Framework for Skill Discovery System
"""


class SkillDiscoveryError(Exception):
    """技能发现系统基础异常类"""
    pass


class SkillNotFoundError(SkillDiscoveryError):
    """技能未找到异常"""

    def __init__(self, skill_name: str):
        self.skill_name = skill_name
        super().__init__(f"Skill not found: {skill_name}")


class SkillLoadError(SkillDiscoveryError):
    """技能加载失败异常"""

    def __init__(self, skill_name: str, reason: str):
        self.skill_name = skill_name
        self.reason = reason
        super().__init__(f"Failed to load skill '{skill_name}': {reason}")


class InvalidInputError(SkillDiscoveryError):
    """无效输入异常"""
    pass


class PathTraversalError(SkillDiscoveryError):
    """路径遍历安全异常"""

    def __init__(self, path: str, base_dir: str = None):
        self.path = path
        self.base_dir = base_dir
        msg = f"Path traversal detected: {path}"
        if base_dir:
            msg += f" (must be within {base_dir})"
        super().__init__(msg)


class CacheError(SkillDiscoveryError):
    """缓存操作异常"""
    pass


class IndexError(SkillDiscoveryError):
    """索引操作异常"""
    pass


class RoutingError(SkillDiscoveryError):
    """路由操作异常"""
    pass
