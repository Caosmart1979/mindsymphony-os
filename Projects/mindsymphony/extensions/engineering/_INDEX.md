---
name: engineering-extension
description: "技术开发扩展包。8个技能覆盖代码分析、重构、性能优化等技术任务。"
skills: 8
---

# 技术开发扩展包 (Engineering Extension)

> 代码分析、重构、架构设计。技术开发全流程支持。

## 技能列表

| 技能 | 定位 | 类型 | 原编号 |
|------|------|------|--------|
| **code-analysis** | 代码库分析 | execution | b-07 |
| **code-refactor** | 代码重构 | execution | b-08 |
| **terminal-ops** | 终端操作 | execution | b-06 |
| **sdk-packaging** | SDK封装 | execution | b-11 |
| **performance** | 性能调优 | execution | b-05 |
| **frontend-arch** | 前端架构 | execution | ve-09 |
| **ux-design** | 用户体验设计 | analytical | b-02 |
| **logic-architect** | 逻辑架构 | execution | e-07 |

## 使用场景

| 场景 | 推荐技能 |
|------|----------|
| "帮我分析这个代码库" | code-analysis |
| "重构这段代码" | code-refactor |
| "优化性能" | performance |
| "设计前端架构" | frontend-arch |
| "设计用户体验" | ux-design |

## 加载方式

```yaml
extensions:
  enabled:
    - engineering
```
