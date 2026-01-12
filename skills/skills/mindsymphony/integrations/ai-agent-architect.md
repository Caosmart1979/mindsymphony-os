---
name: ai-agent-architect
type: integration
external_path: /mnt/skills/user/ai-agent-architect
priority: high
triggers:
  zh: [agent, 智能体, 认知架构, ReAct, CoALA, 评估, 语言代理, 推理, 行动]
  en: [agent, cognitive architecture, ReAct, CoALA, evaluation, language agent, reasoning, action]
---

# AI智能体架构师 (AI Agent Architect) 快捷入口

> 基于姚顺雨研究范式的AI Agent设计框架。

---

## 核心能力

1. **认知架构设计** - CoALA框架、记忆/推理/行动系统
2. **推理模式实现** - ReAct、Tree of Thoughts、Reflexion
3. **评估体系构建** - 真实世界效用基准、能力边界测试
4. **缩放决策** - 训练vs推理compute权衡

---

## 触发词

### 中文
- agent、智能体、认知架构
- ReAct、思维链、反思
- 评估框架、基准测试
- 语言代理、推理行动循环

### English
- agent, cognitive architecture
- ReAct, tree of thoughts, reflexion
- evaluation, benchmark
- language agent, reasoning

---

## 命令前缀

```
/agent [你的Agent设计问题]
```

---

## 模块导航

| 需求 | 去这里 |
|------|--------|
| 理论基础 | references/01-foundations/ |
| 推理模式 | references/02-reasoning/ |
| 行动系统 | references/03-action/ |
| 记忆系统 | references/04-memory/ |
| 评估方法 | references/05-evaluation/ |
| 缩放策略 | references/06-scaling/ |

---

## 核心概念速查

### 姚顺雨范式三支柱

| 支柱 | 核心问题 | 关键洞见 |
|------|----------|----------|
| 推理 | 如何思考？ | ReAct > 纯CoT，交错推理行动 |
| 行动 | 如何执行？ | 工具使用、环境交互、反馈循环 |
| 评估 | 如何衡量？ | 真实世界效用 > 静态基准 |

### CoALA框架

```
┌─────────────────────────────────────┐
│  认知架构 (CoALA)                    │
├─────────────────────────────────────┤
│  记忆系统                            │
│  ├─ 工作记忆（当前上下文）            │
│  ├─ 长期记忆（知识库）               │
│  └─ 程序记忆（技能/工具）            │
├─────────────────────────────────────┤
│  决策过程                            │
│  ├─ 感知 → 推理 → 行动               │
│  └─ 反馈 → 学习 → 适应               │
└─────────────────────────────────────┘
```

---

## 使用示例

### 示例1：Agent架构设计

```
用户：我想设计一个能自主完成代码审查的Agent

激活：ai-agent-architect
响应：
- 推荐认知架构：CoALA变体
- 记忆系统：代码规范库 + 审查历史
- 推理模式：ReAct（读代码→分析→输出建议）
- 行动空间：读取文件、查询规范、生成评论
- 评估方法：与人类审查对比
```

### 示例2：推理模式选择

```
用户：什么时候用ReAct，什么时候用Tree of Thoughts？

激活：ai-agent-architect
响应：
- ReAct：需要与环境交互的任务（搜索、工具使用）
- ToT：需要探索多条路径的复杂推理（数学证明）
- 可以组合：ToT做规划，ReAct做执行
```

### 示例3：评估框架设计

```
用户：如何评估我的Agent的真实能力？

激活：ai-agent-architect
响应：
- 避免单一指标，构建能力矩阵
- 区分：稳定能力 vs 边界能力
- 设计对抗测试用例
- 测量真实世界效用，不只是基准分数
```

---

## 详细文档

完整文档位置：`/mnt/skills/user/ai-agent-architect/SKILL.md`

包含：
- 14个详细模块
- 姚顺雨论文精华提炼
- 设计模式库
- 评估清单
