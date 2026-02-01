# MindSymphony + BMAD 使用指南

**版本**: v21.3
**文档日期**: 2026-02-01

---

## 快速开始

### 1. 激活 BMAD 集成

```python
# 在 Python 中使用
from mindsymphony.extensions.bmad import get_bmad_integration

bmad = get_bmad_integration()
```

或在配置中启用：

```yaml
# mindsymphony-v21.3.config.yml
bmad_integration:
  enabled: true
```

---

## 快捷指令参考

### 🚀 工作流命令

#### `/ms-quick` - 快速流程
适合：bug修复、文档更新、小功能

```
/ms-quick 修复登录页面的样式问题
/ms-quick 更新API文档 --skill=doc-writer
```

**特点**:
- 1-4 个阶段
- 预计时间 < 15 分钟
- 1-2 个 Agent 参与

---

#### `/ms-deep` - 深度规划
适合：产品功能、架构设计、复杂重构

```
/ms-deep 设计新的用户认证系统
/ms-deep 重构核心模块 --plan-only
```

**特点**:
- 7 个完整阶段
- 预计时间 30+ 分钟
- 3-6 个 Agent 参与

---

### 🎉 Party Mode 命令

#### `/ms-party` - 多Agent协作
适合：超复杂任务、跨领域问题、需要多角度讨论

```
/ms-party 设计微服务架构
/ms-party 重构支付系统 --roles=architect,developer,tester,security
```

**特点**:
- 4-8 个 Agent 同时协作
- 结构化讨论流程
- 自动生成共识方案

**可用角色**:
- `architect` - 系统架构师
- `developer` - 代码工程师
- `tester` - 测试专家
- `designer` - 体验设计师
- `product_manager` - 产品经理
- `devops` - DevOps工程师
- `security` - 安全专家

---

### ℹ️ 系统命令

#### `/ms-help` - 自适应帮助
```
/ms-help           # 显示所有命令
/ms-help party     # Party Mode 详细帮助
```

#### `/ms-status` - 系统状态
```
/ms-status
```
输出：
- 活跃工作流数量
- Party 会话状态
- Lightning 指标

#### `/ms-cancel` - 取消工作流
```
/ms-cancel wf_20260201_123456  # 取消特定工作流
/ms-cancel --all               # 取消所有工作流
```

---

## 自动路由

如果不使用命令前缀，MindSymphony 会自动评估复杂度并选择工作流：

```
修复一个拼写错误                    → 自动选择 Quick Flow
设计新的用户系统                    → 自动选择 Full Planning
重构整个核心架构，涉及多个服务      → 自动建议 Party Mode
```

**复杂度评估维度**:
- 领域复杂度 (Domain)
- 规模复杂度 (Scale)
- 影响范围 (Impact)

总分 1-10:
- 1-3: Quick Flow
- 4-5: Full Planning
- 6+: Party Mode

---

## Party Mode 详细指南

### 启动 Party 会话

```python
from mindsymphony.extensions.bmad import get_bmad_integration

bmad = get_bmad_integration()

# 启动 Party
result = bmad.process_request("/ms-party 设计新的API网关 --roles=architect,developer,devops")

# 获取会话ID
session_id = result["session_id"]
```

### 运行协作阶段

```python
# 阶段1: 需求理解
bmad.run_party_phase(session_id, "understanding")

# 阶段2: 观点发散
bmad.run_party_phase(session_id, "divergence")

# 阶段3: 观点收敛
bmad.run_party_phase(session_id, "convergence")

# 阶段4: 方案综合
bmad.run_party_phase(session_id, "synthesis")
```

### 生成综合方案

```python
# 完成会话并获取统一方案
result = bmad.complete_party_session(session_id)

print(result["unified_plan"]["summary"])
print(result["unified_plan"]["action_items"])
```

---

## 程序化使用

### 复杂度评估

```python
from mindsymphony.extensions.bmad import evaluate_complexity

score = evaluate_complexity("设计一个新的用户认证系统")

print(f"总评分: {score.total_score}")
print(f"推荐路径: {score.recommended_path}")
print(f"置信度: {score.confidence}")

# 获取详细解释
print(score.explain_decision())
```

### 工作流路由

```python
from mindsymphony.extensions.bmad import route_request

# 自动路由
result = route_request("修复登录bug")

# 强制指定路径
result = route_request("设计新功能", force_path="full")

# 查看执行计划
print(f"工作流类型: {result['workflow_type']}")
print(f"预计时长: {result['total_estimated_duration']} 分钟")
print(f"阶段数: {len(result['stages'])}")
```

### 解析命令

```python
from mindsymphony.extensions.bmad import parse_command

cmd = parse_command("/ms-party 重构系统 --roles=architect,developer")

print(cmd.command)          # /ms-party
print(cmd.args)             # ["重构系统"]
print(cmd.flags)            # {"roles": "architect,developer"}
print(cmd.execution_params) # 执行参数
```

---

## 与 Lightning Layer 集成

BMAD 自动利用 Lightning Layer 进行数据追踪和优化：

### 追踪的指标

- 不同工作流的成功率
- Party Mode 各阶段效率
- 最佳角色组合
- 用户满意度

### 自适应优化

系统自动：
- 调整复杂度阈值
- 推荐最佳 Party 配置
- 优化工作流提示词

```python
# 查看优化建议
from mindsymphony.extensions.bmad import get_bmad_integration
from mindsymphony.lightning import get_store

bmad = get_bmad_integration()
store = get_store()

# 获取工作流统计
stats = store.get_workflow_stats()
print(f"Quick Flow 成功率: {stats['quick']['success_rate']}")
print(f"Party Mode 平均时长: {stats['party']['avg_duration']} 分钟")
```

---

## 实际场景示例

### 场景1: 紧急Bug修复

```
用户: /ms-quick 修复用户无法登录的问题

系统:
⚡ 启动 Quick Flow
复杂度评估: 2/10 (简单)
阶段:
  1. 意图识别 ✓
  2. 技能匹配 → debug-agent
  3. 执行修复
  4. 轻量验证 ✓

预计时间: 10 分钟
```

### 场景2: 新功能设计

```
用户: /ms-deep 设计用户积分系统

系统:
🔍 启动 Full Planning
复杂度评估: 6/10 (中等)
阶段:
  1. 需求理解 ✓
  2. 复杂度分析 ✓
  3. 方案设计 (进行中)
     - 备选方案A: 基于事件的积分系统
     - 备选方案B: 基于批处理的积分系统
  4. 任务分解
  5. 执行规划
  6. 执行
  7. 综合验证

预计时间: 45 分钟
```

### 场景3: 架构重构

```
用户: /ms-party 从单体迁移到微服务

系统:
🎉 启动 Party Mode
复杂度评估: 9/10 (复杂)
参与角色: 架构师、开发者、DevOps、安全专家

阶段1 - 需求理解:
  [架构师] 关注服务边界划分...
  [开发者] 关注代码重构复杂度...
  [DevOps] 关注部署流程...
  [安全] 关注服务间通信安全...

阶段2 - 观点发散:
  提出了4种不同的迁移策略...

阶段3 - 观点收敛:
  讨论后达成共识: 采用 strangler fig 模式

阶段4 - 方案综合:
  ✓ 统一方案已生成
  ✓ 12个行动项已分配
  ✓ 风险缓解计划已制定

预计时间: 2 小时
```

---

## 故障排除

### 问题: 命令无法识别

**解决方案**:
```bash
# 检查命令格式
/ms-help                    # 查看所有命令
/ms-help quick              # 查看特定命令帮助
```

### 问题: Party Mode 角色冲突

**解决方案**:
```python
# 手动指定角色组合
/ms-party 任务描述 --roles=architect,developer

# 使用推荐的角色组合
/ms-party 任务描述  # 自动选择最佳组合
```

### 问题: 工作流卡住

**解决方案**:
```
/ms-status                  # 查看活跃工作流
/ms-cancel <execution_id>   # 取消卡住的工作流
```

---

## 进阶配置

### 自定义复杂度阈值

```yaml
# mindsymphony-v21.3.config.yml
bmad_integration:
  complexity_evaluator:
    thresholds:
      quick_flow_max: 4      # 调高阈值
      party_mode_min: 7      # 更保守地使用Party
```

### 禁用特定功能

```yaml
bmad_integration:
  party_mode:
    enabled: false           # 禁用Party Mode

  quick_commands:
    commands:
      party:
        enabled: false       # 仅禁用party命令
```

---

## 总结

MindSymphony + BMAD 整合提供了:

1. **智能路由** - 自动选择最适合的工作流
2. **快捷指令** - 快速启动常用模式
3. **Party Mode** - 多Agent协作解决复杂问题
4. **持续进化** - Lightning Layer 驱动自我优化

**开始使用**:
```
/ms-help
```

---

*文档版本: v1.0*
*最后更新: 2026-02-01*
