"""
BMAD Integration Adapter for MindSymphony
整合入口，将 BMAD 工作流与 MindSymphony 系统连接
"""

import os
import sys
from typing import Dict, List, Optional, Any
from datetime import datetime

# 添加 mindsymphony 到路径
sys.path.insert(0, os.path.expanduser('~/.claude/skills/mindsymphony'))

from .complexity_evaluator import ComplexityEvaluator, ComplexityScore
from .workflow_router import WorkflowRouter, WorkflowPath
from .party_session import PartySession, AgentRole
from .quick_commands import QuickCommandParser, ParsedCommand
from .lightning_bridge import BMADLightningBridge

# 尝试导入 Lightning Layer
try:
    from mindsymphony.lightning import get_tracer, get_store
    LIGHTNING_AVAILABLE = True
except ImportError:
    LIGHTNING_AVAILABLE = False


class BMADIntegration:
    """
    BMAD + MindSymphony 集成适配器

    提供统一接口，将 BMAD 方法论整合到 MindSymphony 工作流中。
    """

    def __init__(self, config: Optional[Dict] = None):
        """
        初始化 BMAD 集成

        Args:
            config: 配置选项
        """
        self.config = config or {}
        self.enabled = self.config.get('enabled', True)
        self.version = "1.0.0"

        # 初始化组件
        self.complexity_evaluator = ComplexityEvaluator()
        self.command_parser = QuickCommandParser()

        # Lightning 集成
        self.lightning = None
        self.lightning_bridge = None
        if LIGHTNING_AVAILABLE and self.config.get('lightning', True):
            try:
                self.lightning = {
                    'tracer': get_tracer(),
                    'store': get_store()
                }
                self.lightning_bridge = BMADLightningBridge(self.lightning)
            except Exception as e:
                print(f"[BMAD] Lightning integration failed: {e}")

        # 工作流路由器
        self.workflow_router = WorkflowRouter(
            lightning_integration=self.lightning
        )

        # 活跃会话追踪
        self.active_sessions: Dict[str, Any] = {}

    def process_request(
        self,
        user_input: str,
        context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        处理用户请求的主入口

        这是 BMAD 集成的核心方法，根据用户输入自动:
        1. 解析命令（如果是快捷指令）
        2. 评估复杂度
        3. 路由到合适的工作流
        4. 返回执行计划

        Args:
            user_input: 用户输入
            context: 可选的上下文

        Returns:
            执行计划
        """
        if not self.enabled:
            return {"error": "BMAD integration is disabled"}

        context = context or {}

        # 1. 解析命令
        parsed = self.command_parser.parse(user_input)

        if not parsed.should_execute:
            return {
                "status": "error",
                "error": parsed.execution_params.get("error"),
                "suggestion": parsed.execution_params.get("suggestion")
            }

        # 2. 根据命令类型处理
        if parsed.command_type.value == "workflow":
            return self._handle_workflow_command(parsed, context)

        elif parsed.command_type.value == "party":
            return self._handle_party_command(parsed, context)

        elif parsed.command_type.value == "help":
            return self._handle_help_command(parsed)

        elif parsed.command_type.value == "status":
            return self._handle_status_command()

        elif parsed.command_type.value == "cancel":
            return self._handle_cancel_command(parsed)

        else:
            return {"error": f"Unknown command type: {parsed.command_type}"}

    def _handle_workflow_command(
        self,
        parsed: ParsedCommand,
        context: Dict
    ) -> Dict:
        """处理工作流命令"""
        params = parsed.execution_params

        # 使用自动路由或指定路径
        if params.get("auto_route"):
            # 自然语言输入，需要评估复杂度
            description = params.get("description", "")
            complexity = self.complexity_evaluator.evaluate(description, context)

            # 路由到工作流
            result = self.workflow_router.route(
                description,
                context,
                force_path=None  # 让路由器根据复杂度决定
            )

            result["input_type"] = "natural_language"
            result["complexity_analysis"] = complexity.to_dict()

        else:
            # 快捷指令，使用指定路径
            description = params.get("description", "")
            force_path = params.get("force_path")

            result = self.workflow_router.route(
                description,
                context,
                force_path=force_path
            )

            result["input_type"] = "quick_command"
            result["command_used"] = parsed.command

        # 保存会话
        execution_id = result.get("execution_id")
        if execution_id:
            self.active_sessions[execution_id] = {
                "type": "workflow",
                "started_at": datetime.now(),
                "result": result
            }

        return result

    def _handle_party_command(
        self,
        parsed: ParsedCommand,
        context: Dict
    ) -> Dict:
        """处理 Party Mode 命令"""
        params = parsed.execution_params

        description = params.get("description", "")
        roles_str = params.get("roles", ["architect", "developer"])

        # 转换角色字符串到枚举
        roles = []
        for role_str in roles_str:
            try:
                roles.append(AgentRole(role_str.lower()))
            except ValueError:
                print(f"[BMAD] Unknown role: {role_str}, skipping")

        if not roles:
            roles = [AgentRole.ARCHITECT, AgentRole.DEVELOPER]

        # 创建 Party 会话
        party = PartySession(
            roles=roles,
            lightning_integration=self.lightning
        )

        # 启动会话
        start_info = party.start_session({
            "description": description,
            **context
        })

        # 保存会话
        session_id = start_info["session_id"]
        self.active_sessions[session_id] = {
            "type": "party",
            "session": party,
            "started_at": datetime.now()
        }

        return {
            "status": "party_started",
            "session_id": session_id,
            "roles": [r.value for r in roles],
            "phases": start_info["phases"],
            "estimated_duration": start_info["estimated_duration"],
            "next_step": "Run phases using run_party_phase(session_id, phase)"
        }

    def _handle_help_command(self, parsed: ParsedCommand) -> Dict:
        """处理帮助命令"""
        params = parsed.execution_params
        topic = params.get("topic")

        help_text = self.command_parser.get_help_text(topic)

        return {
            "status": "help",
            "topic": topic,
            "content": help_text
        }

    def _handle_status_command(self) -> Dict:
        """处理状态命令"""
        active_workflows = self.workflow_router.get_active_workflows()

        party_sessions = [
            {
                "session_id": sid,
                "type": info["type"],
                "started_at": info["started_at"].isoformat()
            }
            for sid, info in self.active_sessions.items()
            if info["type"] == "party"
        ]

        return {
            "status": "system_status",
            "bmad_version": self.version,
            "enabled": self.enabled,
            "lightning_available": LIGHTNING_AVAILABLE,
            "active_workflows": active_workflows,
            "party_sessions": party_sessions,
            "total_sessions": len(self.active_sessions)
        }

    def _handle_cancel_command(self, parsed: ParsedCommand) -> Dict:
        """处理取消命令"""
        params = parsed.execution_params

        if params.get("cancel_all"):
            cancelled = []
            for sid in list(self.active_sessions.keys()):
                cancelled.append(sid)
                del self.active_sessions[sid]
            return {
                "status": "cancelled",
                "cancelled_sessions": cancelled,
                "count": len(cancelled)
            }

        execution_id = params.get("execution_id")
        if execution_id and execution_id in self.active_sessions:
            del self.active_sessions[execution_id]
            self.workflow_router.cancel_workflow(execution_id)
            return {
                "status": "cancelled",
                "session_id": execution_id
            }

        return {
            "status": "error",
            "error": "Session not found",
            "active_sessions": list(self.active_sessions.keys())
        }

    def run_party_phase(
        self,
        session_id: str,
        phase: str
    ) -> Dict:
        """
        运行 Party 会话的指定阶段

        Args:
            session_id: 会话ID
            phase: 阶段名称 (understanding, divergence, convergence, synthesis)

        Returns:
            阶段结果
        """
        from .party_session import CollaborationPhase

        session_info = self.active_sessions.get(session_id)
        if not session_info or session_info["type"] != "party":
            return {"error": f"Party session {session_id} not found"}

        party = session_info["session"]

        try:
            phase_enum = CollaborationPhase(phase.lower())
        except ValueError:
            return {
                "error": f"Unknown phase: {phase}",
                "available_phases": [p.value for p in CollaborationPhase]
            }

        # 运行阶段
        phase_result = party.run_phase(phase_enum)

        return phase_result

    def complete_party_session(self, session_id: str) -> Dict:
        """
        完成 Party 会话并生成统一方案

        Args:
            session_id: 会话ID

        Returns:
            综合方案
        """
        session_info = self.active_sessions.get(session_id)
        if not session_info or session_info["type"] != "party":
            return {"error": f"Party session {session_id} not found"}

        party = session_info["session"]

        # 生成统一方案
        unified_plan = party.synthesize_consensus()

        # 移除会话（或标记为完成）
        # del self.active_sessions[session_id]

        return {
            "status": "completed",
            "session_id": session_id,
            "unified_plan": {
                "summary": unified_plan.summary,
                "approved_approach": unified_plan.approved_approach,
                "action_items": unified_plan.action_items,
                "success_criteria": unified_plan.success_criteria,
                "estimated_effort": unified_plan.estimated_effort,
                "risk_mitigation": unified_plan.risk_mitigation
            },
            "session_report": party.get_session_report()
        }

    def get_party_report(self, session_id: str) -> Dict:
        """获取 Party 会话报告"""
        session_info = self.active_sessions.get(session_id)
        if not session_info or session_info["type"] != "party":
            return {"error": f"Party session {session_id} not found"}

        party = session_info["session"]
        return party.get_session_report()

    def get_workflow_next_step(self, execution_id: str) -> Optional[Dict]:
        """获取工作流的下一步"""
        return self.workflow_router.get_next_stage(execution_id)

    def complete_workflow_stage(
        self,
        execution_id: str,
        stage_result: Dict,
        metrics: Optional[Dict] = None
    ) -> Dict:
        """完成工作流阶段"""
        return self.workflow_router.complete_stage(execution_id, stage_result, metrics)

    def get_learning_report(self, days: int = 30) -> str:
        """
        获取学习报告

        Args:
            days: 统计天数

        Returns:
            学习报告文本
        """
        if self.lightning_bridge:
            return self.lightning_bridge.export_learning_report(days)
        return "Lightning integration not available"

    def get_optimal_party_roles(self, domain: str) -> List[str]:
        """
        获取最优 Party 角色组合

        Args:
            domain: 领域名称

        Returns:
            推荐的角色列表
        """
        if self.lightning_bridge:
            return self.lightning_bridge.get_optimal_party_roles(domain)
        return ["architect", "developer"]

    def complete_workflow_stage(
        self,
        execution_id: str,
        stage_result: Dict,
        metrics: Optional[Dict] = None
    ) -> Dict:
        """完成工作流阶段"""
        return self.workflow_router.complete_stage(execution_id, stage_result, metrics)


# 全局实例
_default_integration: Optional[BMADIntegration] = None


def get_bmad_integration(config: Optional[Dict] = None) -> BMADIntegration:
    """获取 BMAD 集成实例"""
    global _default_integration
    if _default_integration is None:
        _default_integration = BMADIntegration(config)
    return _default_integration


def process(user_input: str, context: Optional[Dict] = None) -> Dict:
    """便捷函数：处理用户请求"""
    integration = get_bmad_integration()
    return integration.process_request(user_input, context)
