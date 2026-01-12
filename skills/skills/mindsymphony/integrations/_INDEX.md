---
name: integrations
description: "外部Skill集成层。提供统一的快捷入口，将外部skill无缝整合到MindSymphony生态。"
---

# 外部Skill集成层 (Integrations)

> 统一入口，无缝整合。让外部skill成为MindSymphony的有机组成部分。

---

## 设计理念

```
问题：Skills散落在不同位置，缺乏统一调度
解决：创建"快捷入口"，统一元数据，实现自动路由

外部Skill
    │
    ▼
[Integration Bridge]
    │
    ├─► 元数据标准化
    ├─► 触发词注册
    ├─► 路由集成
    └─► 版本追踪
    │
    ▼
MindSymphony统一调度
```

---

## 已集成Skills

| Skill | 领域 | 优先级 | 状态 |
|-------|------|--------|------|
| academic-forge | 学术研究 | ⭐⭐⭐ | ✅ 已集成 |
| ai-agent-architect | AI/Agent | ⭐⭐⭐ | ✅ 已集成 |
| gemini-cli-integration | 多模态 | ⭐⭐ | ✅ 已集成 |
| skill-creator-meta | 元能力 | ⭐⭐ | ✅ 已集成 |
| notebooklm | 知识检索 | ⭐⭐ | ✅ 已集成 |

---

## 集成文件列表

```
integrations/
├── _INDEX.md              # 本文件
├── academic-forge.md      # 学术研究快捷入口
├── ai-agent-architect.md  # AI Agent设计快捷入口
├── gemini-cli.md          # Gemini CLI快捷入口
├── skill-creator-meta.md  # Skill创建快捷入口
└── notebooklm.md          # NotebookLM知识检索快捷入口
```

---

## 快速使用

### 触发词速查

| 说这个... | 激活这个Skill |
|-----------|--------------|
| "写论文"、"研究设计"、"NHANES" | academic-forge |
| "设计agent"、"ReAct"、"认知架构" | ai-agent-architect |
| "用Gemini"、"分析视频"、"大文件" | gemini-cli |
| "创建skill"、"技能开发" | skill-creator-meta |
| "查我的文档"、"NotebookLM"、"知识库" | notebooklm |

### 命令前缀

| 命令 | 直达Skill |
|------|----------|
| /academic | academic-forge |
| /agent | ai-agent-architect |
| /gemini | gemini-cli |
| /create-skill | skill-creator-meta |
| /notebook | notebooklm |

---

## 添加新集成

### 步骤

1. 在 `integrations/` 下创建 `{skill-name}.md`
2. 按模板填写元数据和快捷入口
3. 在 `router/registry.yml` 中注册
4. 测试触发词

### 模板

```markdown
---
name: {skill-name}
type: integration
external_path: /mnt/skills/user/{skill-name}
priority: high|medium|low
---

# {Skill名称} 快捷入口

> 一句话描述

## 触发词
- 中文：[词1, 词2, ...]
- 英文：[word1, word2, ...]

## 核心能力
1. 能力1
2. 能力2
3. 能力3

## 快速导航
- 详细文档：{external_path}/SKILL.md
- 参考资料：{external_path}/references/

## 使用示例
[示例]
```
