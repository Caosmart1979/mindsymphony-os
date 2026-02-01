# MindSymphony v21.2 - Lightning 进化层升级计划

> 受 Microsoft Agent Lightning 启发，构建非侵入式智能进化系统
>
> "ZERO CODE CHANGE (almost)" — 让进化成为基础设施，而非侵入式重构

---

## 一、核心架构

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    MindSymphony v21.2 "Lightning"                       │
│                    进化智能体 + 训练基础设施层                           │
├─────────────────────────────────────────────────────────────────────────┤
│  Layer 8: Lightning Training Layer ⭐ 新增                               │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐       │
│  │   Tracer    │ │   Reward    │ │  Lightning  │ │    APO      │       │
│  │  (emit_xxx) │ │   Engine    │ │    Store    │ │  Pipeline   │       │
│  └──────┬──────┘ └──────┬──────┘ └──────┬──────┘ └──────┬──────┘       │
│         │               │               │               │              │
│         └───────────────┴───────────────┴───────────────┘              │
│                              │                                          │
│                    ┌─────────▼─────────┐                                │
│                    │  Evolution Bus    │  ← 事件总线，解耦各组件         │
│                    └─────────┬─────────┘                                │
├──────────────────────────────┼──────────────────────────────────────────┤
│  Layer 7: 现有 MindSymphony  │                                          │
│  ├─ cognitive-architect ◄────┤  ← 选择性优化目标                        │
│  ├─ knowledge-explorer ◄─────┤  ← 选择性优化目标                        │
│  ├─ 其他核心技能 ◄───────────┤  ← 可选择性优化                          │
│  └─ ...                      │                                          │
└──────────────────────────────┴──────────────────────────────────────────┘
```

---

## 二、实施阶段

### Phase 1: Tracer 追踪层（Week 1-2）

**目标**: 实现非侵入式事件追踪，零代码变更（almost）

#### 1.1 核心组件
```python
# lightning/tracer.py
class LightningTracer:
    """非侵入式追踪器 - 通过装饰器和钩子自动收集事件"""

    def emit_skill_invocation(self, skill_name, input_context, output_result)
    def emit_tool_execution(self, tool_name, params, result, latency)
    def emit_user_feedback(self, feedback_type, sentiment_score)
    def emit_cross_skill_handoff(self, from_skill, to_skill, handoff_context)
```

#### 1.2 无侵入集成方式
```yaml
# 通过配置启用追踪，无需修改技能代码
tracer:
  enabled: true

  # 自动追踪点（通过包装器/钩子）
  auto_instrument:
    - pattern: "skills/*/__init__.py"
      hook: "invoke"
    - pattern: "core/cognitive-architect"
      hook: "decompose"

  # 采样率（避免性能影响）
  sampling:
    rate: 1.0  # 开发阶段100%，生产可降至0.1
```

### Phase 2: Lightning Store（Week 2-3）

**目标**: 中心化的任务、资源、轨迹存储

#### 2.1 数据模型
```yaml
# 存储结构
lightning_store/
├── spans/              # 原始追踪数据
├── episodes/           # 完整任务序列
├── rewards/            # 奖励信号
├── prompts/            # 提示词版本历史
├── policies/           # 策略权重（RL）
└── metrics/            # 聚合指标
```

#### 2.2 核心表结构
```sql
-- spans 表
CREATE TABLE spans (
    span_id TEXT PRIMARY KEY,
    trace_id TEXT,
    parent_id TEXT,
    skill_name TEXT,
    span_type TEXT,  -- 'invocation', 'tool_call', 'reasoning'
    input_hash TEXT,
    output_hash TEXT,
    latency_ms INTEGER,
    timestamp REAL,
    metadata JSON
);

-- rewards 表
CREATE TABLE rewards (
    episode_id TEXT,
    span_id TEXT,
    reward_type TEXT,  -- 'explicit', 'implicit', 'computed'
    reward_value REAL,
    confidence REAL,
    timestamp REAL
);

-- prompt_versions 表（APO用）
CREATE TABLE prompt_versions (
    skill_name TEXT,
    version_id TEXT,
    prompt_template TEXT,
    performance_score REAL,
    sample_count INTEGER,
    is_active BOOLEAN,
    created_at REAL
);
```

### Phase 3: 奖励信号工程（Week 3-4）

**目标**: 多维度奖励模型，自动提取显式和隐式反馈

#### 3.1 奖励类型
```yaml
reward_engine:
  # 显式奖励（用户直接反馈）
  explicit:
    - thumbs_up/down
    - rating_1_to_5
    - text_feedback_sentiment

  # 隐式奖励（从交互模式推断）
  implicit:
    task_completion:
      - "用户说'完成'" → +1.0
      - "用户未要求重做" → +0.3
      - "用户中途打断" → -0.5

    engagement_quality:
      - "连续多轮交互" → +0.2/轮
      - "用户追问细节" → +0.3
      - "长时间无响应" → -0.2

    efficiency:
      - token_efficiency: 1 - (used / baseline)
      - time_efficiency: 1 - (elapsed / expected)

  # 计算奖励（跨任务聚合）
  computed:
    - synergy_score: 多技能协作流畅度
    - novelty_score: 新模式探索奖励
    - consistency_score: 输出一致性
```

### Phase 4: 自动提示词优化 (APO)（Week 4-5）

**目标**: 自动改进提示词，A/B 测试验证

#### 4.1 APO 流程
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Monitor   │ -> │  Identify   │ -> │  Optimize   │ -> │  Validate   │
│ Performance │    │  Underperf  │    │  Prompt     │    │  A/B Test   │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       ^                                                    │
       └────────────────────────────────────────────────────┘
                     (Feedback Loop)
```

#### 4.2 优化策略
```yaml
apo_pipeline:
  # 触发条件
  trigger:
    min_samples: 20
    success_rate_threshold: 0.7

  # 优化算法
  strategies:
    - type: "lightning-rag"
      description: "基于成功案例检索增强"

    - type: "chain-of-thought"
      description: "自动添加推理步骤"

    - type: "constraint-clarification"
      description: "明确化隐性约束"

    - type: "example-augmentation"
      description: "添加 golden examples"

  # A/B 测试配置
  ab_test:
    traffic_split: 0.5
    min_test_duration: "7d"
    significance_level: 0.05
```

### Phase 5: 集成与上线（Week 5-6）

**目标**: 与现有 MindSymphony 无缝集成

#### 5.1 配置更新
```yaml
# mindsymphony-v21.2.config.yml
system:
  version: "21.2.0-lightning"
  codename: "Evolutionary Synapse + Training Infrastructure"

lightning_layer:
  enabled: true

  tracer:
    enabled: true
    store_path: "~/.claude/mindsymphony-v21/lightning/spans.db"

  reward_engine:
    enabled: true
    weights:
      explicit: 1.0
      implicit: 0.6
      computed: 0.4

  apo:
    enabled: true
    target_skills:
      - "cognitive-architect"
      - "knowledge-explorer"
      - "concept-singularity"
    auto_apply: false  # 人工确认后应用
```

---

## 三、实施优先级

| 优先级 | 组件 | 影响 | 工作量 |
|--------|------|------|--------|
| P0 | Tracer 基础层 | 数据收集基础 | 2d |
| P0 | Lightning Store | 存储基础设施 | 2d |
| P1 | 奖励信号工程 | 学习质量关键 | 3d |
| P1 | 显式反馈收集 | 高质量奖励数据 | 1d |
| P2 | APO 核心管道 | 自动进化 | 4d |
| P2 | 选择性优化 | 资源效率 | 2d |
| P3 | 高级算法 | 性能提升 | 5d |

---

## 四、成功指标

| 指标 | 当前 | 目标 | 测量方式 |
|------|------|------|----------|
| 技能成功率 | 75% | 85% | 任务完成率 |
| 用户满意度 | - | 4.2/5 | 显式反馈 |
| 提示词优化频率 | 手动 | 自动周更 | APO触发次数 |
| 数据收集覆盖率 | 0% | 100% | 追踪覆盖率 |
| 优化迭代周期 | 月 | 周 | 版本迭代速度 |

---

## 五、风险控制

| 风险 | 缓解措施 |
|------|----------|
| 性能开销 | 采样率可调，生产环境10%采样 |
| 存储膨胀 | 自动清理旧数据，保留摘要 |
| 优化回退 | A/B测试验证，人工确认后应用 |
| 隐私泄露 | PII自动脱敏，本地存储优先 |

---

## 六、下一步行动

1. **立即开始**: Phase 1 Tracer 层实现
2. **并行准备**: Lightning Store 数据库设计
3. **一周后**: 奖励信号工程
4. **两周后**: APO 管道
5. **三周后**: 集成测试
6. **四周后**: 上线 v21.2

---

*计划制定: 2026-02-01*
*预期完成: 2026-03-01*
