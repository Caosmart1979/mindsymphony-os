---
name: creative-extension
description: "创意设计扩展包。8个技能覆盖创意突破、视觉表达、人格塑造等创意任务。所有技能保留完整人格设定。"
skills: 8
persona: full
---

# 创意设计扩展包 (Creative Extension)

> 从概念到视觉的创意涌现。所有技能保留完整人格设定（内在冲突 + 美学追求 + 独特视角）。

## 技能列表

| 技能 | 定位 | 人格设定 | 原编号 |
|------|------|----------|--------|
| **idea-connection** | 强制连接创意 | ✅ 完整 | d-02 |
| **visual-poetry** | 视觉诗意表达 | ✅ 完整 | d-06 |
| **aesthetic-edge** | 美学边界突破 | ✅ 完整 | d-07 |
| **edge-narrative** | 边缘视角叙事 | ✅ 完整 | d-03 |
| **voice-selection** | 叙事声音选择 | ✅ 完整 | d-04 |
| **character-depth** | 人格深度构建 | ✅ 完整 | d-05 |
| **character-visual** | 角色视觉设计 | ✅ 完整 | ve-08 |
| **illustration-guide** | 插画风格指导 | ✅ 完整 | ve-11 |

## 使用场景

| 场景 | 推荐技能 |
|------|----------|
| "创意太平庸，帮我突破" | idea-connection |
| "把这个概念视觉化" | visual-poetry |
| "设计一个有深度的角色" | character-depth + character-visual |
| "从不同角度讲这个故事" | edge-narrative + voice-selection |

## 与核心技能的协作

- **concept-singularity** (core) 负责视觉概念涌现
- **brand-alchemist** (core) 负责品牌价值挖掘
- **creative/** 扩展包负责深度创意延展

## 加载方式

```yaml
extensions:
  enabled:
    - creative
```
