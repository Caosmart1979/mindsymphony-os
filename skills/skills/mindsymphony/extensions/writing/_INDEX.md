---
name: writing-extension
description: "内容写作扩展包。4个技能覆盖多风格写作、情感设计、视觉叙事等写作任务。"
skills: 4
---

# 内容写作扩展包 (Writing Extension)

> 各类文本内容创作。多风格写作、情感设计、视觉叙事。

## 技能列表

| 技能 | 定位 | 类型 | 原编号 |
|------|------|------|--------|
| **adaptive-style** | 多风格写作 | creative | ve-10 |
| **content-strategy** | 内容战略指导 | analytical | e-01 |
| **emotional-design** | 情感共鸣设计 | creative | e-09 |
| **visual-narrative** | 分镜脚本 | creative | ve-04 |

## 使用场景

| 场景 | 推荐技能 |
|------|----------|
| "用不同风格写这段内容" | adaptive-style |
| "帮我规划内容战略" | content-strategy |
| "让这个内容更有感染力" | emotional-design |
| "写一个视频脚本" | visual-narrative |

## 与核心技能的协作

- **official-writer** (core) 负责公文报告
- **writing/** 扩展包负责创意写作

## 加载方式

```yaml
extensions:
  enabled:
    - writing
```
