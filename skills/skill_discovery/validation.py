"""
输入验证框架
Input Validation Framework for Skill Discovery System
"""

import os
import re
from pathlib import Path
from typing import Union

from exceptions import InvalidInputError, PathTraversalError


def validate_skill_name(name: str) -> str:
    """
    验证技能名称格式

    Args:
        name: 技能名称

    Returns:
        验证后的技能名称

    Raises:
        InvalidInputError: 名称格式无效
    """
    if not name:
        raise InvalidInputError("Skill name cannot be empty")

    if not isinstance(name, str):
        raise InvalidInputError(f"Skill name must be a string, got {type(name)}")

    # 只允许小写字母、数字、连字符和下划线
    if not re.match(r'^[a-z0-9_-]+$', name):
        raise InvalidInputError(
            f"Invalid skill name format: '{name}'. "
            "Only lowercase letters, numbers, hyphens and underscores are allowed."
        )

    if len(name) > 100:
        raise InvalidInputError(f"Skill name too long: {len(name)} > 100 characters")

    if len(name) < 2:
        raise InvalidInputError(f"Skill name too short: {len(name)} < 2 characters")

    return name


def validate_file_path(
    path: Union[str, Path],
    base_dir: Union[str, Path],
    must_exist: bool = False,
    file_type: str = None
) -> Path:
    """
    验证文件路径，防止路径遍历攻击

    Args:
        path: 要验证的文件路径
        base_dir: 允许的基础目录
        must_exist: 是否必须存在
        file_type: 期望的文件类型（如 '.json', '.yml'）

    Returns:
        验证后的绝对路径（Path对象）

    Raises:
        InvalidInputError: 路径为空或格式无效
        PathTraversalError: 检测到路径遍历
        FileNotFoundError: 文件不存在（当must_exist=True时）
    """
    if not path:
        raise InvalidInputError("File path cannot be empty")

    # 转换为Path对象
    try:
        path_obj = Path(path)
        base_obj = Path(base_dir)
    except (TypeError, ValueError) as e:
        raise InvalidInputError(f"Invalid path format: {e}")

    # 解析为绝对路径
    try:
        abs_path = path_obj.resolve()
        abs_base = base_obj.resolve()
    except (OSError, RuntimeError) as e:
        raise InvalidInputError(f"Cannot resolve path: {e}")

    # 检查是否在允许的目录内
    try:
        abs_path.relative_to(abs_base)
    except ValueError:
        raise PathTraversalError(str(path), str(base_dir))

    # 检查路径中是否包含 ".."
    if '..' in str(path):
        raise PathTraversalError(str(path), str(base_dir))

    # 检查是否存在
    if must_exist and not abs_path.exists():
        raise FileNotFoundError(f"Path does not exist: {abs_path}")

    # 检查文件类型
    if file_type and abs_path.suffix != file_type:
        raise InvalidInputError(
            f"Invalid file type: expected {file_type}, got {abs_path.suffix}"
        )

    return abs_path


def validate_cache_path(cache_path: str, project_root: str = None) -> Path:
    """
    验证缓存文件路径

    Args:
        cache_path: 缓存文件路径
        project_root: 项目根目录（默认为当前目录）

    Returns:
        验证后的缓存文件路径

    Raises:
        InvalidInputError: 路径无效
        PathTraversalError: 路径遍历检测
    """
    if project_root is None:
        project_root = os.getcwd()

    # 只允许文件名，不允许路径
    if os.path.dirname(cache_path):
        # 如果包含目录，则验证完整路径
        return validate_file_path(cache_path, project_root, must_exist=False, file_type='.json')

    # 只有文件名，构建在项目根目录下
    cache_dir = Path(project_root) / 'cache'
    cache_dir.mkdir(exist_ok=True)

    cache_file = cache_dir / Path(cache_path).name

    # 确保扩展名是 .json
    if not cache_file.suffix:
        cache_file = cache_file.with_suffix('.json')
    elif cache_file.suffix != '.json':
        raise InvalidInputError(f"Cache file must be .json, got {cache_file.suffix}")

    return cache_file


def validate_query_string(query: str, max_length: int = 1000) -> str:
    """
    验证查询字符串

    Args:
        query: 查询字符串
        max_length: 最大长度

    Returns:
        验证后的查询字符串

    Raises:
        InvalidInputError: 查询无效
    """
    if not query:
        raise InvalidInputError("Query string cannot be empty")

    if not isinstance(query, str):
        raise InvalidInputError(f"Query must be a string, got {type(query)}")

    if len(query) > max_length:
        raise InvalidInputError(f"Query too long: {len(query)} > {max_length} characters")

    # 移除首尾空白
    query = query.strip()

    if not query:
        raise InvalidInputError("Query string cannot be only whitespace")

    return query


def validate_category(category: str) -> str:
    """
    验证分类名称

    Args:
        category: 分类名称

    Returns:
        验证后的分类名称

    Raises:
        InvalidInputError: 分类名称无效
    """
    if not category:
        raise InvalidInputError("Category cannot be empty")

    if not isinstance(category, str):
        raise InvalidInputError(f"Category must be a string, got {type(category)}")

    # 允许字母、数字、连字符、下划线和空格
    if not re.match(r'^[a-zA-Z0-9_\- ]+$', category):
        raise InvalidInputError(
            f"Invalid category format: '{category}'. "
            "Only letters, numbers, hyphens, underscores and spaces are allowed."
        )

    if len(category) > 50:
        raise InvalidInputError(f"Category name too long: {len(category)} > 50 characters")

    return category.strip()


def validate_resource_name(resource: str) -> str:
    """
    验证资源名称

    Args:
        resource: 资源名称

    Returns:
        验证后的资源名称

    Raises:
        InvalidInputError: 资源名称无效
    """
    if not resource:
        raise InvalidInputError("Resource name cannot be empty")

    if not isinstance(resource, str):
        raise InvalidInputError(f"Resource name must be a string, got {type(resource)}")

    # 允许字母、数字、连字符
    if not re.match(r'^[a-z0-9-]+$', resource):
        raise InvalidInputError(
            f"Invalid resource name format: '{resource}'. "
            "Only lowercase letters, numbers and hyphens are allowed."
        )

    if len(resource) > 100:
        raise InvalidInputError(f"Resource name too long: {len(resource)} > 100 characters")

    return resource


def sanitize_filename(filename: str) -> str:
    """
    清理文件名，移除不安全字符

    Args:
        filename: 原始文件名

    Returns:
        清理后的安全文件名
    """
    # 移除路径分隔符和其他危险字符
    unsafe_chars = ['/', '\\', '..', '\0', ':', '*', '?', '"', '<', '>', '|']

    safe_name = filename
    for char in unsafe_chars:
        safe_name = safe_name.replace(char, '_')

    # 限制长度
    if len(safe_name) > 255:
        name, ext = os.path.splitext(safe_name)
        safe_name = name[:255 - len(ext)] + ext

    return safe_name


# 便捷的验证装饰器
def validate_inputs(**validators):
    """
    参数验证装饰器

    Usage:
        @validate_inputs(name=validate_skill_name, path=validate_file_path)
        def my_function(name, path):
            pass
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            # 验证kwargs
            for param, validator in validators.items():
                if param in kwargs:
                    kwargs[param] = validator(kwargs[param])
            return func(*args, **kwargs)
        return wrapper
    return decorator
