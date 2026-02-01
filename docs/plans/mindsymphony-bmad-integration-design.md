# MindSymphony + BMAD 整合设计文档

**版本**: v21.3-bmad
**代号**: "Collaborative Evolution"
**设计日期**: 2026-02-01

---

## 一、整合愿景

将 BMAD 的**结构化协作方法论**与 MindSymphony 的**进化型智能架构**融合，打造世界上第一个**自适应、自进化的多Agent协作开发系统**。

**核心价值主张**:
- 不是替代开发者思考，而是**激发最佳思考**
- 从简单bug修复到企业级架构，**自动适应复杂度**
- 多Agent**并行协作**而非顺序执行
- 每次协作都**学习和进化**

---

## 二、架构设计

### 2.1 整体架构图

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        用户界面层 (CLI/Hook)                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   /ms-quick  │  │   /ms-deep   │  │  /ms-party   │  │   /ms-help   │ │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘ │
└─────────┼────────────────┼────────────────┼────────────────┼───────────┘
          │                │                │                │
          └────────────────┴────────────────┴────────────────┘
                                   │
                         ┌─────────▼─────────┐
                         │   快捷指令解析器    │
                         └─────────┬─────────┘
                                   │
┌──────────────────────────────────┼──────────────────────────────────────┐
│                    MindSymphony 核心层                                  │
│                                                                          │
│  ┌───────────────────────────────┐    ┌───────────────────────────────┐  │
│  │      复杂度评估引擎            │    │       路径选择器              │  │
│  │  ┌─────────┐  ┌───────────┐   │    │  ┌──────────┐  ┌──────────┐   │  │
│  │  │ 关键词   │  │  上下文    │   │    │  │ QUICK    │  │  FULL    │   │  │
│  │  │ 分析    │  │  分析     │   │───▶│  │ PATH     │  │  PATH    │   │  │
│  │  └─────────┘  └───────────┘   │    │  └──────────┘  └──────────┘   │  │
│  │         ▼                     │    │         │            │         │  │
│  │  ┌─────────────────────┐     │    │         ▼            ▼         │  │
│  │  │   复杂度评分 (1-10)  │     │    │  ┌──────────┐  ┌──────────┐   │  │
│  │  │  domain | scale     │     │    │  │轻量级调用 │  │蜂后协奏  │   │  │
│  │  └─────────────────────┘     │    │  │单技能/串行│  │多技能并行│   │  │
│  └───────────────────────────────┘    └───────────────────────────────┘  │
│                                   │                                      │
│                         ┌─────────▼─────────┐                            │
│                         │     蜂后调度器      │                            │
│                         │  (Queen Bee v2.1)   │                            │
│                         └─────────┬─────────┘                            │
│                                   │                                      │
│  ┌────────────────────────────────┼──────────────────────────────────┐   │
│  │                         Party Mode 协作层                          │   │
│  │  ┌──────────────────────────────────────────────────────────────┐ │   │
│  │  │                    协作会话管理器                              │ │   │
│  │  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐            │ │   │
│  │  │  │ 建筑师  │ │ 开发者  │ │ 测试员  │ │ 设计师  │  ...       │ │   │
│  │  │  │(并行)   │ │(并行)   │ │(并行)   │ │(并行)   │            │ │   │
│  │  │  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘            │ │   │
│  │  │       │           │           │           │                  │ │   │
│  │  │       └───────────┴─────┬─────┴───────────┘                  │ │   │
│  │  │                           ▼                                   │ │   │
│  │  │                  ┌─────────────────┐                          │ │   │
│  │  │                  │   共识整合器     │                          │ │   │
│  │  │                  │  (冲突解决→综合) │                          │ │   │
│  │  │                  └─────────────────┘                          │ │   │
│  │  └──────────────────────────────────────────────────────────────┘ │   │
│  └───────────────────────────────────────────────────────────────────┘   │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐    │
│  │                      技能执行层 (Skills Layer)                    │    │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐    │    │
│  │  │cognitive│ │ code    │ │ testing │ │  docs   │ │  ...    │    │    │
│  │  │-architect│ │-engineer│ │  -agent │ │ -writer │ │         │    │    │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘    │    │
│  └──────────────────────────────────────────────────────────────────┘    │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
                                    │
                         ┌──────────▼──────────┐
                         │    Lightning Layer   │
                         │  (追踪→学习→进化)    │
                         │                     │
                         │ ┌─────┐┌─────┐┌────┐│
                         │ │Tracer││Store││APO ││
                         │ └─────┘└─────┘└────┘│
                         └─────────────────────┘
                                    │
                         ┌──────────▼──────────┐
                         │   自适应反馈循环     │
                         │  (成功率→优化→推荐)  │
                         └─────────────────────┘
```

---

### 2.2 核心组件设计

#### 2.2.1 复杂度评估引擎

```yaml
# mindsymphony/extensions/bmad/complexity-evaluator.yml

complexity_evaluator:
  version: "1.0.0"

  dimensions:
    # 维度1: 领域复杂度
    domain:
      weights:
        simple: 1      # bugfix, docs, refactor
        medium: 3      # feature, api
        complex: 5     # architecture, algorithm
        expert: 8      # distributed, security, ai-model

      keywords:
        simple: ["fix", "bug", "typo", "doc", "comment", "rename", "format"]
        medium: ["add", "feature", "endpoint", "component", "page"]
        complex: ["system", "service", "platform", "redesign", "migration"]
        expert: ["distributed", "consensus", "crypto", "ml-model", "kernel"]

    # 维度2: 规模复杂度
    scale:
      metrics:
        files_changed:
          small: 1      # 1-3 files
          medium: 3     # 4-10 files
          large: 5      # 11-30 files
          xlarge: 8     # 30+ files

        lines_estimate:
          tiny: 1       # <50 lines
          small: 2      # 50-200 lines
          medium: 4     # 200-1000 lines
          large: 7      # 1000+ lines

    # 维度3: 影响范围
    impact:
      isolated: 1       # 单一模块
      module: 3         # 多个模块
      cross_team: 5     # 跨团队
      breaking: 7       # 破坏性变更

  scoring:
    # 总分 = domain + scale + impact
    # 阈值设置
    thresholds:
      quick_flow_max: 3     # <=3 走 Quick Flow
      full_flow_min: 4      # >=4 走 Full Planning
      party_mode_min: 6     # >=6 建议 Party Mode
```

#### 2.2.2 双路径工作流

```yaml
# mindsymphony/workflows/path-definitions.yml

workflows:
  quick_flow:
    name: "快速流程"
    description: "适合bug修复、小功能、文档更新"
    trigger:
      complexity_max: 3
      patterns: ["/ms-quick", "/fix", "/docs"]

    stages:
      - name: "意图识别"
        skill: "intent-router"
        config:
          depth: "shallow"

      - name: "直接执行"
        skill: "auto-select"
        config:
          max_skills: 2
          parallel: false

      - name: "轻量验证"
        skill: "quality-gate"
        config:
          level: "basic"

    characteristics:
      planning_depth: "minimal"
      agent_count: "1-2"
      session_time: "< 15 min"
      output: "直接可执行"

  full_planning:
    name: "完整规划"
    description: "适合产品功能、架构设计、复杂重构"
    trigger:
      complexity_min: 4
      patterns: ["/ms-deep", "/plan", "/arch"]

    stages:
      - name: "需求理解"
        skill: "cognitive-architect"
        config:
          depth: "deep"
          decomposition: true

      - name: "方案设计"
        skill: "solution-designer"
        config:
          alternatives: 3
          evaluation: true

      - name: "任务分解"
        skill: "task-decomposer"
        config:
          granularity: "story"
          dependencies: true

      - name: "执行计划"
        skill: "execution-planner"
        config:
          prioritize: true
          assign_agents: true

      - name: "质量验证"
        skill: "quality-gate"
        config:
          level: "comprehensive"

    characteristics:
      planning_depth: "comprehensive"
      agent_count: "3-8"
      session_time: "30+ min"
      output: "完整方案+执行计划"
```

#### 2.2.3 Party Mode 设计

```yaml
# mindsymphony/extensions/bmad/party-mode.yml

party_mode:
  version: "1.0.0"
  description: "多Agent并行协作模式"

  # 触发条件
  triggers:
    complexity_threshold: 6
    user_explicit: "/ms-party"
    cross_domain: true  # 涉及多个领域时自动建议

  # 角色模板
  roles:
    architect:
      name: "系统架构师"
      skill: "cognitive-architect"
      responsibility: ["整体结构", "技术选型", "接口设计"]
      prompts:
        opening: "从架构角度分析这个需求..."
        concern: "关注可扩展性、可维护性、技术债务"

    developer:
      name: "代码工程师"
      skill: "code-engineer"
      responsibility: ["实现方案", "代码质量", "性能优化"]
      prompts:
        opening: "从实现角度考虑..."
        concern: "关注可行性、复杂度、测试覆盖"

    tester:
      name: "测试专家"
      skill: "testing-agent"
      responsibility: ["测试策略", "边界情况", "质量保证"]
      prompts:
        opening: "从测试角度审视..."
        concern: "关注可测试性、边界条件、风险点"

    designer:
      name: "体验设计师"
      skill: "ux-designer"
      responsibility: ["用户体验", "交互流程", "可用性"]
      prompts:
        opening: "从用户体验角度思考..."
        concern: "关注易用性、一致性、用户反馈"

    product_manager:
      name: "产品经理"
      skill: "product-analyst"
      responsibility: ["业务价值", "优先级", "范围控制"]
      prompts:
        opening: "从业务价值角度评估..."
        concern: "关注ROI、用户需求、交付时间"

  # 协作流程
  collaboration_flow:
    phase_1_understanding:
      name: "需求理解"
      duration: "3-5 min"
      activities:
        - all_agents_read_context
        - each_agent_identifies_questions
        - facilitator_synthesizes_clarifications

    phase_2_divergence:
      name: "观点发散"
      duration: "5-8 min"
      activities:
        - each_agent_proposes_approach
        - agents_identify_risks_opportunities
        - no_debate_yet  # 先收集所有观点

    phase_3_convergence:
      name: "观点收敛"
      duration: "5-8 min"
      activities:
        - agents_discuss_tradeoffs
        - resolve_conflicts
        - identify_synergies

    phase_4_synthesis:
      name: "方案综合"
      duration: "3-5 min"
        - facilitator_creates_unified_plan
        - assign_action_items
        - define_success_criteria

  # 共识整合器
  consensus_engine:
    conflict_resolution:
      - rule: "技术分歧 → 架构师决策"
      - rule: "实现分歧 → 开发者决策"
      - rule: "体验分歧 → 设计师决策"
      - rule: "范围分歧 → 产品经理决策"

    output_format:
      unified_plan:
        - approved_approach
        - rejected_alternatives_with_reasons
        - open_questions
        - next_steps
        - assigned_agents
```

---

### 2.3 快捷指令系统

```yaml
# mindsymphony/router/quick-commands.yml

quick_commands:
  prefix: "/ms-"

  commands:
    quick:
      syntax: "/ms-quick [描述]"
      alias: ["/fix", "/patch", "/docs"]
      description: "快速流程 - 适合简单任务"
      action:
        type: "workflow"
        workflow: "quick_flow"
        skip_complexity_check: false

    deep:
      syntax: "/ms-deep [描述]"
      alias: ["/plan", "/arch", "/design"]
      description: "深度规划 - 适合复杂任务"
      action:
        type: "workflow"
        workflow: "full_planning"
        skip_complexity_check: false

    party:
      syntax: "/ms-party [描述] [--roles=architect,developer,tester]"
      alias: ["/collab", "/discuss"]
      description: "启动多Agent协作会话"
      action:
        type: "party_mode"
        default_roles: ["architect", "developer"]
        optional_roles: ["tester", "designer", "product_manager"]

    help:
      syntax: "/ms-help [主题?]"
      description: "自适应帮助系统"
      action:
        type: "help_system"
        adaptive: true
        consider_context: true

    status:
      syntax: "/ms-status"
      description: "查看当前系统状态"
      action:
        type: "status_report"
        include:
          - active_skills
          - lightning_metrics
          - recent_optimizations
```

---

### 2.4 Lightning Layer 集成

```yaml
# mindsymphony/extensions/bmad/lightning-integration.yml

lightning_integration:
  # 追踪 BMAD 工作流的使用
  workflow_tracking:
    events:
      - workflow_started:
          fields: [workflow_type, complexity_score, user_id, timestamp]

      - party_mode_initiated:
          fields: [roles_involved, complexity_score, domain_tags]

      - workflow_completed:
          fields: [workflow_type, success, duration, user_satisfaction]

      - agent_contribution:
          fields: [agent_role, contribution_type, acceptance_rate]

  # 自适应优化
  adaptive_learning:
    # 基于成功率自动调整阈值
    threshold_optimization:
      metric: "workflow_success_rate"
      adjustment_strategy:
        if_quick_flow_success < 0.7:
          action: "increase_quick_flow_threshold"
          delta: +0.5

        if_full_flow_success > 0.9:
          action: "decrease_full_flow_threshold"
          delta: -0.5

    # 最佳 Party 配置学习
    party_optimization:
      track: [role_combination, task_domain, success_rate]
      recommend:
        for_domain: "backend_api"
        best_roles: ["architect", "developer", "tester"]
        success_rate: 0.94

  # APO 集成
  apo_integration:
    # 优化工作流提示词
    optimize_workflows:
      - target: "quick_flow_prompt"
        trigger: success_rate < 0.75
        min_samples: 20

      - target: "party_mode_consensus"
        trigger: conflict_resolution_time > 5min
        min_samples: 15
```

---

## 三、实施计划

### 阶段1: 核心基础设施 (v21.3-beta1)
- [ ] 复杂度评估引擎
- [ ] 双路径路由系统
- [ ] 基础快捷指令 (/ms-quick, /ms-deep)

### 阶段2: Party Mode (v21.3-beta2)
- [ ] 多Agent协作框架
- [ ] 共识整合器
- [ ] Party Mode 指令 (/ms-party)

### 阶段3: 自适应系统 (v21.3-release)
- [ ] 帮助系统 (/ms-help)
- [ ] Lightning 数据闭环
- [ ] 阈值自动优化

---

## 四、接口定义

### 4.1 内部 API

```python
# 复杂度评估
class ComplexityEvaluator:
    def evaluate(self, user_input: str, context: dict) -> ComplexityScore:
        """
        Returns: {
            total_score: int (1-10),
            dimensions: {
                domain: str,
                scale: str,
                impact: str
            },
            recommended_path: "quick" | "full",
            confidence: float
        }
        """

# Party Mode 管理
class PartySession:
    def __init__(self, roles: list[str], facilitator: str = "queen_bee"): ...
    def start_phase(self, phase: CollaborationPhase): ...
    def add_contribution(self, agent: str, content: str): ...
    def synthesize_consensus(self) -> UnifiedPlan: ...
    def end_session(self) -> SessionReport: ...
```

---

## 五、成功指标

| 指标 | 目标 | 测量方式 |
|------|------|----------|
| 路径选择准确率 | >85% | 用户反馈 + 回溯验证 |
| Party Mode 满意度 | >4.0/5 | 会话后评分 |
| 平均任务完成时间 | 减少 20% | Lightning 追踪 |
| 技能调用优化率 | >30% | APO 统计 |

---

**设计完成** - 准备进入实施阶段
