"""
工作流路由器 - 双路径系统
实现 Quick Flow 和 Full Planning 两条工作流路径
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Callable, Any
from datetime import datetime
import json

from .complexity_evaluator import ComplexityScore, ComplexityEvaluator


class WorkflowPath(Enum):
    """工作流路径类型"""
    QUICK = "quick"
    FULL = "full"
    PARTY = "party"


@dataclass
class WorkflowStage:
    """工作流阶段"""
    name: str
    skill: str
    config: Dict[str, Any] = field(default_factory=dict)
    estimated_duration: int = 5  # 分钟
    required: bool = True


@dataclass
class WorkflowDefinition:
    """工作流定义"""
    name: str
    description: str
    path_type: WorkflowPath
    stages: List[WorkflowStage]
    characteristics: Dict[str, Any]
    entry_points: List[str]  # 触发命令


@dataclass
class WorkflowExecution:
    """工作流执行状态"""
    workflow_id: str
    path_type: WorkflowPath
    current_stage: int
    stages_completed: List[str]
    stages_pending: List[str]
    context: Dict[str, Any]
    started_at: datetime
    completed_at: Optional[datetime] = None
    metrics: Dict[str, Any] = field(default_factory=dict)


class WorkflowRouter:
    """
    工作流路由器

    根据复杂度评估结果，自动选择并执行合适的工作流:
    - Quick Flow: 简单任务，快速完成
    - Full Planning: 复杂任务，完整规划
    - Party Mode: 超复杂任务，多Agent协作
    """

    def __init__(self, lightning_integration: Optional[Any] = None):
        """
        初始化工作流路由器

        Args:
            lightning_integration: 可选的 Lightning Layer 集成
        """
        self.complexity_evaluator = ComplexityEvaluator()
        self.lightning = lightning_integration
        self.active_executions: Dict[str, WorkflowExecution] = {}
        self._register_default_workflows()

    def _register_default_workflows(self):
        """注册默认工作流定义"""
        self.workflows: Dict[WorkflowPath, WorkflowDefinition] = {}

        # Quick Flow 定义
        self.workflows[WorkflowPath.QUICK] = WorkflowDefinition(
            name="快速流程",
            description="适合bug修复、小功能、文档更新等简单任务",
            path_type=WorkflowPath.QUICK,
            stages=[
                WorkflowStage(
                    name="意图识别",
                    skill="intent-router",
                    config={"depth": "shallow", "fast_mode": True},
                    estimated_duration=1
                ),
                WorkflowStage(
                    name="技能匹配",
                    skill="auto-select",
                    config={"max_skills": 2, "strategy": "best_match"},
                    estimated_duration=1
                ),
                WorkflowStage(
                    name="执行",
                    skill="executor",
                    config={"mode": "direct"},
                    estimated_duration=5
                ),
                WorkflowStage(
                    name="轻量验证",
                    skill="quality-gate",
                    config={"level": "basic", "checks": ["syntax", "lint"]},
                    estimated_duration=2
                )
            ],
            characteristics={
                "planning_depth": "minimal",
                "agent_count": "1-2",
                "session_time": "< 15 min",
                "output": "直接可执行",
                "user_interaction": "minimal"
            },
            entry_points=["/ms-quick", "/fix", "/patch", "/docs"]
        )

        # Full Planning 定义
        self.workflows[WorkflowPath.FULL] = WorkflowDefinition(
            name="完整规划",
            description="适合产品功能、架构设计、复杂重构等",
            path_type=WorkflowPath.FULL,
            stages=[
                WorkflowStage(
                    name="需求理解",
                    skill="cognitive-architect",
                    config={"depth": "deep", "ask_clarifying": True},
                    estimated_duration=5
                ),
                WorkflowStage(
                    name="复杂度分析",
                    skill="complexity-analyzer",
                    config={"detailed": True},
                    estimated_duration=3
                ),
                WorkflowStage(
                    name="方案设计",
                    skill="solution-designer",
                    config={
                        "alternatives": 2,
                        "evaluation_criteria": ["feasibility", "maintainability", "performance"]
                    },
                    estimated_duration=10
                ),
                WorkflowStage(
                    name="任务分解",
                    skill="task-decomposer",
                    config={"granularity": "story", "track_dependencies": True},
                    estimated_duration=8
                ),
                WorkflowStage(
                    name="执行规划",
                    skill="execution-planner",
                    config={"prioritize": True, "estimate_effort": True},
                    estimated_duration=5
                ),
                WorkflowStage(
                    name="执行",
                    skill="executor",
                    config={"mode": "planned", "checkpoint": True},
                    estimated_duration=15
                ),
                WorkflowStage(
                    name="综合验证",
                    skill="quality-gate",
                    config={
                        "level": "comprehensive",
                        "checks": ["syntax", "tests", "security", "performance"]
                    },
                    estimated_duration=10
                )
            ],
            characteristics={
                "planning_depth": "comprehensive",
                "agent_count": "3-6",
                "session_time": "30+ min",
                "output": "完整方案+执行计划",
                "user_interaction": "collaborative"
            },
            entry_points=["/ms-deep", "/plan", "/arch", "/design"]
        )

        # Party Mode 定义
        self.workflows[WorkflowPath.PARTY] = WorkflowDefinition(
            name="多Agent协作",
            description="适合超复杂任务、跨领域问题、需要多角度讨论",
            path_type=WorkflowPath.PARTY,
            stages=[
                WorkflowStage(
                    name="启动Party",
                    skill="party-orchestrator",
                    config={"select_roles": "auto", "briefing": True},
                    estimated_duration=3
                ),
                WorkflowStage(
                    name="需求理解",
                    skill="party-session",
                    config={"phase": "understanding", "all_participate": True},
                    estimated_duration=5
                ),
                WorkflowStage(
                    name="观点发散",
                    skill="party-session",
                    config={"phase": "divergence", "brainstorm": True},
                    estimated_duration=8
                ),
                WorkflowStage(
                    name="观点收敛",
                    skill="party-session",
                    config={"phase": "convergence", "debate": True},
                    estimated_duration=8
                ),
                WorkflowStage(
                    name="方案综合",
                    skill="consensus-synthesizer",
                    config={"create_unified_plan": True},
                    estimated_duration=5
                ),
                WorkflowStage(
                    name="任务分配",
                    skill="execution-planner",
                    config={"assign_to_agents": True},
                    estimated_duration=3
                ),
                WorkflowStage(
                    name="并行执行",
                    skill="parallel-executor",
                    config={"coordinate": True, "sync_interval": "5min"},
                    estimated_duration=20
                ),
                WorkflowStage(
                    name="集成验证",
                    skill="quality-gate",
                    config={"level": "comprehensive", "integration_focus": True},
                    estimated_duration=10
                )
            ],
            characteristics={
                "planning_depth": "exhaustive",
                "agent_count": "4-8",
                "session_time": "45+ min",
                "output": "综合方案+并行执行",
                "user_interaction": "facilitated"
            },
            entry_points=["/ms-party", "/collab", "/discuss"]
        )

    def route(
        self,
        user_input: str,
        context: Optional[Dict] = None,
        force_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        路由用户请求到合适的工作流

        执行流程:
        1. 评估任务复杂度 (或使用强制路径)
        2. 选择合适的工作流 (Quick/Full/Party)
        3. 创建工作流执行实例
        4. 返回执行计划

        Args:
            user_input: 用户描述的任务
            context: 可选的上下文信息
            force_path: 强制指定路径 ("quick", "full", "party")

        Returns:
            包含工作流选择和执行计划的字典:
            {
                "execution_id": str,
                "workflow_type": "quick" | "full" | "party",
                "complexity_score": ComplexityScore,
                "stages": [...],
                "total_estimated_duration": int
            }

        Example:
            >>> router = WorkflowRouter()
            >>> result = router.route("fix typo")
            >>> result["workflow_type"]
            'quick'
        """
        context = context or {}

        # 步骤1: 确定工作流路径
        # 方式A: 用户强制指定路径
        if force_path:
            # 创建强制路径的复杂度评分
            path = WorkflowPath(force_path)
            complexity_score = ComplexityScore(
                total_score=0, domain_score=0, scale_score=0, impact_score=0,
                domain_type="forced", scale_type="forced", impact_type="forced",
                recommended_path=force_path, confidence=1.0,
                reasoning=[f"用户强制指定 {force_path} 路径"]
            )
        else:
            # 方式B: 自动评估复杂度
            complexity_score = self.complexity_evaluator.evaluate(user_input, context)
            path = WorkflowPath(complexity_score.recommended_path)

        # 步骤2: 获取选定工作流的定义
        workflow = self.workflows[path]

        # 步骤3: 创建工作流执行实例
        execution_id = f"wf_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{id(user_input) % 10000}"
        execution = WorkflowExecution(
            workflow_id=execution_id,
            path_type=path,
            current_stage=0,
            stages_completed=[],
            stages_pending=[s.name for s in workflow.stages],
            context={
                "user_input": user_input,
                "complexity_score": complexity_score.to_dict(),
                **context
            },
            started_at=datetime.now()
        )
        self.active_executions[execution_id] = execution

        # 步骤4: 记录追踪数据 (如果 Lightning 可用)
        if self.lightning:
            self._emit_workflow_event("workflow_started", execution, complexity_score)

        # 步骤5: 返回执行计划
        return {
            "execution_id": execution_id,
            "workflow_type": path.value,
            "workflow_name": workflow.name,
            "complexity_score": complexity_score.to_dict(),
            "stages": [
                {
                    "name": s.name,
                    "skill": s.skill,
                    "estimated_duration": s.estimated_duration
                }
                for s in workflow.stages
            ],
            "total_estimated_duration": sum(s.estimated_duration for s in workflow.stages),
            "characteristics": workflow.characteristics,
            "explanation": self.complexity_evaluator.explain_decision(complexity_score)
        }

    def get_next_stage(self, execution_id: str) -> Optional[Dict]:
        """
        获取工作流的下一个阶段

        Args:
            execution_id: 工作流执行ID

        Returns:
            下一阶段信息，如果完成则返回None
        """
        execution = self.active_executions.get(execution_id)
        if not execution:
            return None

        workflow = self.workflows[execution.path_type]

        if execution.current_stage >= len(workflow.stages):
            # 工作流已完成
            self._complete_workflow(execution_id)
            return None

        stage = workflow.stages[execution.current_stage]

        return {
            "stage_index": execution.current_stage,
            "stage_name": stage.name,
            "skill": stage.skill,
            "config": stage.config,
            "estimated_duration": stage.estimated_duration,
            "context": execution.context
        }

    def complete_stage(
        self,
        execution_id: str,
        stage_result: Dict[str, Any],
        metrics: Optional[Dict] = None
    ) -> Optional[Dict]:
        """
        完成当前阶段并推进到下一阶段

        Args:
            execution_id: 工作流执行ID
            stage_result: 阶段执行结果
            metrics: 可选的性能指标

        Returns:
            下一阶段信息，如果完成则返回总结
        """
        execution = self.active_executions.get(execution_id)
        if not execution:
            return {"error": "Execution not found"}

        workflow = self.workflows[execution.path_type]
        current_stage = workflow.stages[execution.current_stage]

        # 记录完成
        execution.stages_completed.append(current_stage.name)
        execution.stages_pending.pop(0)
        execution.context[f"result_{current_stage.name}"] = stage_result

        if metrics:
            execution.metrics[current_stage.name] = metrics

        execution.current_stage += 1

        # 检查是否完成
        if execution.current_stage >= len(workflow.stages):
            return self._complete_workflow(execution_id)

        # 返回下一阶段
        return self.get_next_stage(execution_id)

    def _complete_workflow(self, execution_id: str) -> Dict:
        """完成工作流"""
        execution = self.active_executions.get(execution_id)
        if not execution:
            return {"error": "Execution not found"}

        execution.completed_at = datetime.now()
        duration = (execution.completed_at - execution.started_at).total_seconds() / 60

        summary = {
            "status": "completed",
            "execution_id": execution_id,
            "workflow_type": execution.path_type.value,
            "stages_completed": execution.stages_completed,
            "total_duration_minutes": duration,
            "context": execution.context,
            "metrics": execution.metrics
        }

        # 记录到 Lightning
        if self.lightning:
            self._emit_workflow_event("workflow_completed", execution)

        # 清理执行状态
        del self.active_executions[execution_id]

        return summary

    def _emit_workflow_event(
        self,
        event_type: str,
        execution: WorkflowExecution,
        complexity_score: Optional[ComplexityScore] = None
    ):
        """发送工作流事件到 Lightning Layer"""
        if not self.lightning:
            return

        try:
            event_data = {
                "event_type": event_type,
                "workflow_id": execution.workflow_id,
                "workflow_type": execution.path_type.value,
                "timestamp": datetime.now().isoformat(),
                "context": {
                    "stages_count": len(self.workflows[execution.path_type].stages),
                    "complexity_score": complexity_score.to_dict() if complexity_score else None
                }
            }

            # 使用 Lightning Tracer
            tracer = getattr(self.lightning, 'tracer', None)
            if tracer:
                tracer.emit_custom_event("bmad_workflow", event_data)

        except Exception as e:
            print(f"[BMAD] Failed to emit lightning event: {e}")

    def get_active_workflows(self) -> List[Dict]:
        """获取所有活跃的工作流"""
        return [
            {
                "execution_id": ex.workflow_id,
                "type": ex.path_type.value,
                "current_stage": ex.current_stage,
                "stages_pending": ex.stages_pending,
                "started_at": ex.started_at.isoformat()
            }
            for ex in self.active_executions.values()
        ]

    def cancel_workflow(self, execution_id: str) -> bool:
        """取消工作流"""
        if execution_id in self.active_executions:
            del self.active_executions[execution_id]
            return True
        return False


# 便捷函数
def route_request(
    user_input: str,
    context: Optional[Dict] = None,
    force_path: Optional[str] = None
) -> Dict:
    """便捷函数：路由请求到工作流"""
    router = WorkflowRouter()
    return router.route(user_input, context, force_path)
