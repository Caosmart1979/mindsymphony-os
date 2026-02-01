---
name: research-extension
description: "知识研究扩展包。4个技能覆盖概念考古、结构分析、学术研究等知识探索任务。"
skills: 4
---

# 知识研究扩展包 (Research Extension)

> 回答"是什么"和"为什么"的问题。深度研究、结构分析、学术支持。

## 技能列表

| 技能 | 定位 | 类型 | 原编号 |
|------|------|------|--------|
| **concept-archaeology** | 概念词源考古 | analytical | c-01 |
| **structure-analysis** | 复杂系统拆解 | analytical | b-03 |
| **academic-research** | 学术论文研究 | execution | b-09 |
| **knowledge-structure** | 知识→讲义结构化 | execution | e-02 |

## 使用场景

| 场景 | 推荐技能 |
|------|----------|
| "这个概念的本质是什么" | concept-archaeology |
| "帮我分析这个系统的结构" | structure-analysis |
| "帮我做文献调研" | academic-research |
| "把这些知识整理成讲义" | knowledge-structure |

## 与核心技能的协作

- **knowledge-explorer** (core) 负责通用知识研究
- **research/** 扩展包负责专项深度研究

## 加载方式

```yaml
extensions:
  enabled:
    - research
```
