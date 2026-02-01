---
name: n8n-extension
description: "n8n自动化工作流扩展包。5个专项技能覆盖从架构设计到节点配置的完整流程。"
skills: 5
domain: n8n
---

# n8n 自动化扩展包 (n8n Extension)

> 从业务需求到自动化工作流的完整技能组。

## 技能列表

| 技能 | 定位 | 原编号 |
|------|------|--------|
| **workflow-architect** | 工作流架构设计 | h-01 |
| **node-configuration** | 节点配置专家 | h-02 |
| **mcp-tools** | MCP工具使用 | h-03 |
| **expression-syntax** | 表达式语法 | h-04 |
| **feishu-connector** | 飞书集成 | h-05 |

## 协作流程

```
业务需求
    ↓
workflow-architect（整体架构）
    ↓
node-configuration（节点配置）
    ↓
expression-syntax（表达式调试）
    ↓
mcp-tools / feishu-connector（特定集成）
```

## 加载方式

```yaml
extensions:
  enabled:
    - domains/n8n
```
