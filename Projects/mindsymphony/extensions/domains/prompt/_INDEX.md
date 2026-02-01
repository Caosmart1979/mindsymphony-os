---
name: prompt-extension
description: "提示词工程扩展包。4个专项技能覆盖提示词精炼、认知优化、价值对齐等。"
skills: 4
domain: prompt
---

# 提示词工程扩展包 (Prompt Extension)

> 提示词的精炼、优化、价值对齐。

## 技能列表

| 技能 | 定位 | 原编号 |
|------|------|--------|
| **prompt-refine** | 提示词精炼 | e-03 |
| **cognitive-load** | 认知负担优化 | e-04 |
| **value-optimize** | 价值传达优化 | e-05 |
| **value-align** | 价值对齐设计 | e-06 |

## 与核心技能的协作

- **prompt-pharmacist** (core) 负责提示词诊断
- **domains/prompt/** 扩展包负责深度优化

## 加载方式

```yaml
extensions:
  enabled:
    - domains/prompt
```
