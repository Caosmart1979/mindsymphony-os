"""
Lightning 集成模块

提供与外部系统的集成适配器
"""

from .mindsymphony_adapter import (
    MindSymphonyAdapter,
    get_adapter,
    trace_skill,
    record_feedback,
    get_optimized_prompt
)

__all__ = [
    'MindSymphonyAdapter',
    'get_adapter',
    'trace_skill',
    'record_feedback',
    'get_optimized_prompt'
]
