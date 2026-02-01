"""
Party Mode - 多Agent协作会话
实现BMAD的Party Mode：多个Agent同时参与结构化协作
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Callable, Any
from datetime import datetime
import uuid


class CollaborationPhase(Enum):
    """协作阶段"""
    UNDERSTANDING = "understanding"      # 需求理解
    DIVERGENCE = "divergence"            # 观点发散
    CONVERGENCE = "convergence"          # 观点收敛
    SYNTHESIS = "synthesis"              # 方案综合
    EXECUTION = "execution"              # 执行阶段


class AgentRole(Enum):
    """Agent角色定义"""
    ARCHITECT = "architect"
    DEVELOPER = "developer"
    TESTER = "tester"
    DESIGNER = "designer"
    PRODUCT_MANAGER = "product_manager"
    DEVOPS = "devops"
    SECURITY = "security"
    DATA_SCIENTIST = "data_scientist"


@dataclass
class AgentPersona:
    """Agent人格定义"""
    role: AgentRole
    name: str
    skill_mapping: str
    responsibilities: List[str]
    opening_prompt: str
    concern_prompt: str
    expertise_areas: List[str]


@dataclass
class Contribution:
    """Agent贡献"""
    agent_role: str
    phase: CollaborationPhase
    content: str
    timestamp: datetime
    contribution_type: str  # "idea", "concern", "question", "suggestion"


@dataclass
class ConsensusPoint:
    """共识点"""
    topic: str
    agreed_points: List[str]
    disagreements: List[Dict[str, str]]  # [{role: str, view: str}]
    resolution: Optional[str] = None
    confidence: float = 0.0


@dataclass
class UnifiedPlan:
    """综合方案"""
    summary: str
    approved_approach: str
    rejected_alternatives: List[Dict[str, str]]
    open_questions: List[str]
    action_items: List[Dict[str, Any]]
    success_criteria: List[str]
    estimated_effort: str
    risk_mitigation: List[str]


class PartySession:
    """
    Party Mode 多Agent协作会话

    特点:
    - 多个Agent同时参与
    - 结构化协作流程
    - 自动共识整合
    - 冲突解决机制
    """

    # 角色定义
    ROLE_DEFINITIONS = {
        AgentRole.ARCHITECT: AgentPersona(
            role=AgentRole.ARCHITECT,
            name="系统架构师",
            skill_mapping="cognitive-architect",
            responsibilities=["整体结构", "技术选型", "接口设计", "可扩展性"],
            opening_prompt="从架构角度分析这个需求，关注系统的整体结构和技术选型...",
            concern_prompt="特别关注可扩展性、可维护性、技术债务",
            expertise_areas=["系统设计", "架构模式", "技术决策", "性能优化"]
        ),
        AgentRole.DEVELOPER: AgentPersona(
            role=AgentRole.DEVELOPER,
            name="代码工程师",
            skill_mapping="code-engineer",
            responsibilities=["实现方案", "代码质量", "性能优化", "技术可行性"],
            opening_prompt="从实现角度考虑，这个需求如何用最优雅的方式实现...",
            concern_prompt="关注实现可行性、代码复杂度、测试覆盖",
            expertise_areas=["编码实践", "重构技术", "设计模式", "代码审查"]
        ),
        AgentRole.TESTER: AgentPersona(
            role=AgentRole.TESTER,
            name="测试专家",
            skill_mapping="testing-agent",
            responsibilities=["测试策略", "边界情况", "质量保证", "风险识别"],
            opening_prompt="从测试角度审视这个需求，考虑边界条件和质量保证...",
            concern_prompt="关注可测试性、边界条件、风险点",
            expertise_areas=["测试策略", "边界分析", "自动化测试", "质量保证"]
        ),
        AgentRole.DESIGNER: AgentPersona(
            role=AgentRole.DESIGNER,
            name="体验设计师",
            skill_mapping="ux-designer",
            responsibilities=["用户体验", "交互流程", "可用性", "一致性"],
            opening_prompt="从用户体验角度思考，这个需求如何设计最符合用户直觉...",
            concern_prompt="关注易用性、一致性、用户反馈",
            expertise_areas=["用户体验", "交互设计", "可用性", "设计系统"]
        ),
        AgentRole.PRODUCT_MANAGER: AgentPersona(
            role=AgentRole.PRODUCT_MANAGER,
            name="产品经理",
            skill_mapping="product-analyst",
            responsibilities=["业务价值", "优先级", "范围控制", "用户价值"],
            opening_prompt="从业务价值角度评估这个需求，考虑ROI和用户影响...",
            concern_prompt="关注ROI、用户需求、交付时间、范围控制",
            expertise_areas=["需求分析", "优先级管理", "用户研究", "产品策略"]
        ),
        AgentRole.DEVOPS: AgentPersona(
            role=AgentRole.DEVOPS,
            name="DevOps工程师",
            skill_mapping="devops-engineer",
            responsibilities=["部署策略", "监控", "基础设施", "自动化"],
            opening_prompt="从部署和运维角度考虑这个需求的影响...",
            concern_prompt="关注部署复杂度、监控需求、基础设施影响",
            expertise_areas=["CI/CD", "基础设施", "监控", "自动化"]
        ),
        AgentRole.SECURITY: AgentPersona(
            role=AgentRole.SECURITY,
            name="安全专家",
            skill_mapping="security-reviewer",
            responsibilities=["安全审查", "风险评估", "合规性", "漏洞预防"],
            opening_prompt="从安全角度审查这个需求，识别潜在的安全风险...",
            concern_prompt="关注安全风险、合规要求、数据保护",
            expertise_areas=["安全审查", "风险评估", "合规性", "威胁建模"]
        )
    }

    # 阶段配置
    PHASE_CONFIG = {
        CollaborationPhase.UNDERSTANDING: {
            "duration": 5,
            "instructions": "阅读上下文，识别关键需求，提出澄清问题",
            "output_format": "需求理解摘要"
        },
        CollaborationPhase.DIVERGENCE: {
            "duration": 8,
            "instructions": "提出不同解决方案，分析优缺点，暂不做评判",
            "output_format": "方案选项列表"
        },
        CollaborationPhase.CONVERGENCE: {
            "duration": 8,
            "instructions": "讨论权衡，解决分歧，寻求共识",
            "output_format": "讨论摘要和决策"
        },
        CollaborationPhase.SYNTHESIS: {
            "duration": 5,
            "instructions": "整合所有观点，形成统一方案",
            "output_format": "综合方案"
        }
    }

    def __init__(
        self,
        roles: List[AgentRole],
        facilitator: str = "queen_bee",
        lightning_integration: Optional[Any] = None
    ):
        """
        初始化Party会话

        Args:
            roles: 参与的角色列表
            facilitator: 协调者标识
            lightning_integration: Lightning Layer集成
        """
        self.session_id = f"party_{uuid.uuid4().hex[:8]}"
        self.roles = [self.ROLE_DEFINITIONS[r] for r in roles]
        self.facilitator = facilitator
        self.lightning = lightning_integration

        self.current_phase: Optional[CollaborationPhase] = None
        self.contributions: List[Contribution] = []
        self.phase_history: Dict[CollaborationPhase, Dict] = {}
        self.started_at: Optional[datetime] = None
        self.completed_at: Optional[datetime] = None

        # 状态
        self.phase_status: Dict[CollaborationPhase, str] = {
            phase: "pending" for phase in CollaborationPhase
        }

    def start_session(self, context: Dict[str, Any]) -> Dict:
        """
        启动Party会话

        Args:
            context: 任务上下文

        Returns:
            会话启动信息
        """
        self.started_at = datetime.now()

        # 构建角色简报
        role_briefings = []
        for role in self.roles:
            briefing = {
                "role": role.role.value,
                "name": role.name,
                "expertise": role.expertise_areas,
                "responsibilities": role.responsibilities,
                "opening": role.opening_prompt
            }
            role_briefings.append(briefing)

        start_info = {
            "session_id": self.session_id,
            "status": "started",
            "roles": [r.role.value for r in self.roles],
            "role_details": role_briefings,
            "phases": list(self.PHASE_CONFIG.keys()),
            "estimated_duration": sum(
                cfg["duration"] for cfg in self.PHASE_CONFIG.values()
            ),
            "context": context
        }

        # 记录到 Lightning
        if self.lightning:
            self._emit_event("party_started", start_info)

        return start_info

    def run_phase(
        self,
        phase: CollaborationPhase,
        phase_input: Optional[Dict] = None
    ) -> Dict:
        """
        运行一个协作阶段

        Args:
            phase: 阶段类型
            phase_input: 阶段输入

        Returns:
            阶段结果
        """
        if phase not in self.PHASE_CONFIG:
            return {"error": f"Unknown phase: {phase}"}

        self.current_phase = phase
        self.phase_status[phase] = "running"

        config = self.PHASE_CONFIG[phase]

        # 构建阶段提示
        phase_prompt = self._build_phase_prompt(phase, phase_input)

        # 模拟各角色的贡献 (实际实现中会调用对应的skills)
        role_contributions = []
        for role in self.roles:
            contribution = self._generate_role_contribution(role, phase, phase_prompt)
            role_contributions.append(contribution)

            # 记录贡献
            self.contributions.append(Contribution(
                agent_role=role.role.value,
                phase=phase,
                content=contribution["content"],
                timestamp=datetime.now(),
                contribution_type=contribution["type"]
            ))

        # 阶段总结
        phase_result = {
            "phase": phase.value,
            "status": "completed",
            "duration": config["duration"],
            "contributions": role_contributions,
            "summary": self._synthesize_phase_contributions(phase, role_contributions)
        }

        self.phase_history[phase] = phase_result
        self.phase_status[phase] = "completed"

        # 记录到 Lightning
        if self.lightning:
            self._emit_event("phase_completed", {
                "phase": phase.value,
                "contributions_count": len(role_contributions)
            })

        return phase_result

    def _build_phase_prompt(
        self,
        phase: CollaborationPhase,
        phase_input: Optional[Dict]
    ) -> str:
        """构建阶段提示"""
        config = self.PHASE_CONFIG[phase]

        prompt = f"""
## 当前阶段: {phase.value}

**阶段目标**: {config["instructions"]}
**预计时长**: {config["duration"]} 分钟

"""

        if phase_input:
            prompt += f"""
**阶段输入**:
```
{phase_input.get('summary', 'N/A')}
```
"""

        # 添加上一阶段的总结（如果有）
        prev_phase = self._get_previous_phase(phase)
        if prev_phase and prev_phase in self.phase_history:
            prev_summary = self.phase_history[prev_phase].get("summary", "")
            prompt += f"""
**上一阶段总结**:
{prev_summary}
"""

        return prompt

    def _get_previous_phase(self, phase: CollaborationPhase) -> Optional[CollaborationPhase]:
        """获取上一阶段"""
        phases = list(CollaborationPhase)
        idx = phases.index(phase)
        return phases[idx - 1] if idx > 0 else None

    def _generate_role_contribution(
        self,
        role: AgentPersona,
        phase: CollaborationPhase,
        prompt: str
    ) -> Dict:
        """
        生成角色的贡献
        注意: 这是模拟实现，实际应调用对应的 skill
        """
        # 基于角色和阶段生成贡献模板
        contribution_types = {
            CollaborationPhase.UNDERSTANDING: ["question", "observation"],
            CollaborationPhase.DIVERGENCE: ["idea", "alternative"],
            CollaborationPhase.CONVERGENCE: ["argument", "synthesis"],
            CollaborationPhase.SYNTHESIS: ["approval", "refinement"]
        }

        types = contribution_types.get(phase, ["suggestion"])

        return {
            "role": role.role.value,
            "role_name": role.name,
            "type": types[0],
            "content": f"[{role.name}] 基于'{role.opening_prompt[:30]}...'的视角分析",
            "concerns": role.concern_prompt,
            "expertise_applied": role.expertise_areas[:2]
        }

    def _synthesize_phase_contributions(
        self,
        phase: CollaborationPhase,
        contributions: List[Dict]
    ) -> str:
        """综合阶段贡献"""
        # 提取关键观点
        key_points = []
        for contrib in contributions:
            key_points.append(f"- {contrib['role_name']}: {contrib['content'][:50]}...")

        return f"""
### {phase.value} 阶段总结

**主要观点**:
{chr(10).join(key_points)}

**待解决问题**: {len([c for c in contributions if c['type'] == 'question'])}
**提出的方案**: {len([c for c in contributions if c['type'] in ['idea', 'alternative']])}
"""

    def synthesize_consensus(self) -> UnifiedPlan:
        """
        综合所有阶段的贡献，生成统一方案

        Returns:
            UnifiedPlan: 综合方案
        """
        # 分析所有贡献
        all_ideas = []
        all_concerns = []
        consensus_topics = {}

        for contrib in self.contributions:
            if contrib.contribution_type in ["idea", "suggestion"]:
                all_ideas.append(contrib.content)
            elif contrib.contribution_type == "concern":
                all_concerns.append(contrib.content)

        # 生成统一方案 (模拟)
        unified_plan = UnifiedPlan(
            summary=self._generate_summary(),
            approved_approach=self._identify_approved_approach(),
            rejected_alternatives=self._identify_rejected_alternatives(),
            open_questions=self._identify_open_questions(),
            action_items=self._generate_action_items(),
            success_criteria=[
                "实现所有功能需求",
                "通过所有测试用例",
                "代码审查通过",
                "性能指标达标"
            ],
            estimated_effort="基于讨论，估计需要3-5天",
            risk_mitigation=all_concerns[:3]
        )

        self.completed_at = datetime.now()

        # 记录到 Lightning
        if self.lightning:
            self._emit_event("party_completed", {
                "duration": (self.completed_at - self.started_at).total_seconds() / 60,
                "contributions_count": len(self.contributions),
                "phases_completed": list(self.phase_history.keys())
            })

        return unified_plan

    def _generate_summary(self) -> str:
        """生成会话总结"""
        return f"""
Party Session {self.session_id} 总结:
- 参与角色: {', '.join(r.name for r in self.roles)}
- 讨论阶段: {len(self.phase_history)} 个
- 总贡献数: {len(self.contributions)} 条
- 达成共识: 已就主要方案达成一致
"""

    def _identify_approved_approach(self) -> str:
        """确定通过的方案"""
        # 从SYNTHESIS阶段提取
        synthesis = self.phase_history.get(CollaborationPhase.SYNTHESIS, {})
        return synthesis.get("summary", "基于多角色讨论的综合方案")[:200]

    def _identify_rejected_alternatives(self) -> List[Dict[str, str]]:
        """识别被否决的替代方案"""
        # 从DIVERGENCE和CONVERGENCE阶段提取
        alternatives = []
        divergence = self.phase_history.get(CollaborationPhase.DIVERGENCE, {})
        for contrib in divergence.get("contributions", []):
            if contrib.get("type") == "alternative":
                alternatives.append({
                    "approach": contrib["content"][:100],
                    "rejection_reason": "与主方案相比复杂度较高"
                })
        return alternatives[:3]

    def _identify_open_questions(self) -> List[str]:
        """识别未解决的问题"""
        questions = []
        for contrib in self.contributions:
            if contrib.contribution_type == "question":
                questions.append(contrib.content[:100])
        return questions[:5] or ["性能基准测试标准", "用户验收测试安排"]

    def _generate_action_items(self) -> List[Dict[str, Any]]:
        """生成行动项"""
        return [
            {"task": "创建技术设计文档", "assignee": "architect", "priority": "high"},
            {"task": "实现核心功能", "assignee": "developer", "priority": "high"},
            {"task": "编写单元测试", "assignee": "tester", "priority": "high"},
            {"task": "设计用户界面", "assignee": "designer", "priority": "medium"},
            {"task": "配置CI/CD管道", "assignee": "devops", "priority": "medium"}
        ]

    def get_session_report(self) -> Dict:
        """获取完整会话报告"""
        duration = 0
        if self.started_at:
            end = self.completed_at or datetime.now()
            duration = (end - self.started_at).total_seconds() / 60

        return {
            "session_id": self.session_id,
            "status": "completed" if self.completed_at else "in_progress",
            "roles": [r.role.value for r in self.roles],
            "phases_completed": [p.value for p in self.phase_history.keys()],
            "phases_status": {k.value: v for k, v in self.phase_status.items()},
            "total_contributions": len(self.contributions),
            "duration_minutes": duration,
            "contributions_by_role": self._count_contributions_by_role(),
            "contributions_by_phase": self._count_contributions_by_phase()
        }

    def _count_contributions_by_role(self) -> Dict[str, int]:
        """按角色统计贡献"""
        counts = {}
        for contrib in self.contributions:
            counts[contrib.agent_role] = counts.get(contrib.agent_role, 0) + 1
        return counts

    def _count_contributions_by_phase(self) -> Dict[str, int]:
        """按阶段统计贡献"""
        counts = {}
        for contrib in self.contributions:
            phase = contrib.phase.value
            counts[phase] = counts.get(phase, 0) + 1
        return counts

    def _emit_event(self, event_type: str, data: Dict):
        """发送事件到 Lightning"""
        if not self.lightning:
            return

        try:
            tracer = getattr(self.lightning, 'tracer', None)
            if tracer:
                tracer.emit_custom_event("party_mode", {
                    "event_type": event_type,
                    "session_id": self.session_id,
                    "timestamp": datetime.now().isoformat(),
                    "data": data
                })
        except Exception as e:
            print(f"[PartyMode] Failed to emit event: {e}")


# 便捷函数
def start_party(
    roles: List[str],
    context: Dict[str, Any],
    lightning: Optional[Any] = None
) -> PartySession:
    """便捷函数：启动Party会话"""
    role_enums = [AgentRole(r) for r in roles]
    session = PartySession(role_enums, lightning_integration=lightning)
    session.start_session(context)
    return session
