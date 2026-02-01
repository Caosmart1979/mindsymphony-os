"""
BMAD Integration for MindSymphony v21.3
Breakthrough Method of Agile AI Driven Development

提供:
- 复杂度评估引擎
- 双路径工作流 (Quick Flow / Full Planning)
- Party Mode 多Agent协作
- 快捷指令系统

Usage:
    from mindsymphony.extensions.bmad import get_bmad_integration

    bmad = get_bmad_integration()
    result = bmad.process_request("/ms-quick 修复登录bug")
"""

__version__ = "1.0.0"
__bmad_version__ = "v6.0-compatible"
__mindsymphony_version__ = "v21.3"

# 核心组件
from .complexity_evaluator import ComplexityEvaluator, ComplexityScore, evaluate_complexity
from .workflow_router import WorkflowRouter, WorkflowPath, WorkflowExecution, route_request
from .party_session import PartySession, CollaborationPhase, AgentRole, UnifiedPlan, start_party
from .quick_commands import QuickCommandParser, ParsedCommand, parse_command, get_help
from .lightning_bridge import BMADLightningBridge, get_lightning_bridge
from .bmad_integration import BMADIntegration, get_bmad_integration, process

__all__ = [
    # 核心类
    "BMADIntegration",
    "BMADLightningBridge",
    "ComplexityEvaluator",
    "ComplexityScore",
    "WorkflowRouter",
    "WorkflowPath",
    "WorkflowExecution",
    "PartySession",
    "CollaborationPhase",
    "AgentRole",
    "UnifiedPlan",
    "QuickCommandParser",
    "ParsedCommand",
    # 便捷函数
    "get_bmad_integration",
    "get_lightning_bridge",
    "process",
    "evaluate_complexity",
    "route_request",
    "start_party",
    "parse_command",
    "get_help",
    # 元信息
    "__version__",
    "__bmad_version__",
    "__mindsymphony_version__",
]
