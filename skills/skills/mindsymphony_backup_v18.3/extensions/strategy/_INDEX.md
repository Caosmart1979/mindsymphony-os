---
name: strategy-extension
description: "战略规划扩展包。7个技能覆盖行动规划、学习路径、工作流设计等战略层面任务。"
skills: 7
---

# 战略规划扩展包 (Strategy Extension)

> 回答"做什么"和"怎么规划"的问题。

## 技能列表

| 技能 | 定位 | 类型 | 原编号 |
|------|------|------|--------|
| **action-planning** | 战略→行动计划转化 | execution | a-00 |
| **learning-path** | 学习路径设计 | analytical | a-01 |
| **paradigm-shift** | 产业变革战略 | analytical | a-03 |
| **research-planning** | 科研方向规划 | analytical | a-06 |
| **workflow-design** | 工作流编排 | execution | b-04 |
| **workflow-visual** | 流程可视化 | execution | m-07 |
| **insight-capture** | 洞察→指令转化 | analytical | a-05 |

## 使用场景

| 场景 | 推荐技能 |
|------|----------|
| "帮我规划这个项目" | cognitive-architect (core) → action-planning |
| "我想学习XX，帮我设计学习路径" | learning-path |
| "这个行业有什么变革机会" | paradigm-shift |
| "帮我规划研究方向" | research-planning |
| "设计一个工作流程" | workflow-design + workflow-visual |

## 与核心技能的协作

- **cognitive-architect** (core) 负责任务分解
- **strategy/** 扩展包负责深度规划

## 加载方式

```yaml
extensions:
  enabled:
    - strategy
```
