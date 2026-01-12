---
name: meta-extension
description: "系统元能力扩展包。9个技能覆盖技能创建、复盘、质量把关等系统自身能力，包含融合版skill-forge。"
skills: 9
---

# 系统元能力扩展包 (Meta Extension)

> 系统自身的运行和进化。技能创建、复盘、质量把关。

## 技能列表

| 技能 | 定位 | 类型 | 原编号 |
|------|------|------|--------|
| **skill-creation** | 技能铸造（MindSymphony原版） | execution | m-01 |
| **skill-forge** | 融合版技能铸造（MindSymphony × skill-creator-meta） | execution | 新增 |
| **idea-incubation** | 想法孵化 | creative | m-02 |
| **session-review** | 复盘提炼 | execution | m-04 |
| **quality-gate** | 质量把关 | execution | m-06 |
| **config-validation** | 配置验证 | execution | m-08 |
| **nl-config** | 自然语言配置 | execution | b-10 |
| **deployment** | 智能体部署 | execution | a-04 |
| **efficacy-evaluator** | 效能评估 | execution | e-08 |

## 使用场景

| 场景 | 推荐技能 |
|------|----------|
| "创建一个新技能" | skill-creation |
| "复盘这次会话" | session-review |
| "检查质量" | quality-gate |
| "评估效能" | efficacy-evaluator |

## 加载方式

```yaml
extensions:
  enabled:
    - meta
```
