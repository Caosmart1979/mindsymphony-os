---
name: gemini-cli-integration
description: "Claude Code与Gemini CLI的深度集成方案。Use when (1) 需要在Claude Code中处理图片、视频、音频等多模态内容, (2) 需要分析超大文件或整个代码仓库(100万token上下文), (3) 想要自动化多模态工作流, (4) 配置Claude Code的Skills和Subagent调用外部AI, (5) 需要补齐Claude Code的多模态短板。"
interop_metadata:
  skill_id: skills.gemini_cli_integration
  api_version: v1
  authentication: none
  rate_limit:
    requests_per_minute: 30
---

# Gemini CLI Integration for Claude Code

让Claude Code无缝调用Gemini CLI，打通多模态能力。

```
核心架构：Skills识别意图 + Subagent隔离执行

┌─────────────────────────────────────────────────┐
│              Claude Code 主对话                  │
│  (保持清爽，不被Gemini输出污染)                   │
└──────────────────────┬──────────────────────────┘
                       │ 触发
                       ▼
┌─────────────────────────────────────────────────┐
│           Skill: gemini-cli                      │
│  识别意图："用Gemini分析..."                      │
└──────────────────────┬──────────────────────────┘
                       │ 分发
                       ▼
┌─────────────────────────────────────────────────┐
│        Subagent: gemini-executor                 │
│  执行命令，隔离上下文，返回摘要                    │
└──────────────────────┬──────────────────────────┘
                       │ 调用
                       ▼
┌─────────────────────────────────────────────────┐
│              Gemini CLI                          │
│  100万token · 原生多模态 · 免费额度               │
└─────────────────────────────────────────────────┘
```

---

## 为什么需要这个集成？

| 能力 | Claude Code | Gemini CLI | 集成后 |
|------|-------------|------------|--------|
| 编码能力 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | Claude主导 |
| 工作流编排 | ⭐⭐⭐⭐⭐ | ⭐⭐ | Claude主导 |
| 图片理解 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Gemini补齐 |
| 视频/音频 | ❌ | ⭐⭐⭐⭐⭐ | Gemini补齐 |
| 超长上下文 | ~200K | **1M tokens** | Gemini补齐 |
| 大文件处理 | 需切割 | 原生支持 | Gemini补齐 |

**核心价值**：各司其职，短板互补，上下文隔离

---

## Quick Start

### Step 1: 安装Gemini CLI

```bash
# 需要Node.js 18+
npm install -g @anthropic-ai/gemini-cli

# 或使用npx直接运行
npx @anthropic-ai/gemini-cli
```

### Step 2: 配置API Key

```bash
# 设置环境变量
export GEMINI_API_KEY="your-api-key"

# 或在首次运行时按提示登录Google账号
gemini
```

### Step 3: 部署Skill和Subagent

```bash
# 复制Skill到Claude Code skills目录
cp -r gemini-cli ~/.claude/skills/

# 复制Subagent到agents目录
cp agents/gemini-executor.md ~/.claude/agents/
```

### Step 4: 开始使用

在Claude Code中直接说：
- "用Gemini分析这张截图 screenshot.png"
- "让Gemini总结这个视频 demo.mp4"
- "Gemini帮我扫描整个项目架构"

→ 详细安装指南见 references/setup-guide.md

---

## Master Navigation

```
What do you need?
│
├─► 首次配置
│   └─► references/setup-guide.md
│       - Gemini CLI安装
│       - API Key配置
│       - Skills部署
│       - 验证测试
│
├─► 理解架构
│   └─► See "Architecture Deep Dive" below
│       - 为什么用Skills+Subagent
│       - 上下文隔离原理
│       - 最佳实践
│
├─► 使用场景
│   └─► references/use-cases.md
│       - 图片分析
│       - 视频/音频处理
│       - PDF文档提取
│       - 代码仓库扫描
│
├─► 查看示例
│   ├─► examples/image-analysis.md
│   ├─► examples/video-summary.md
│   └─► examples/repo-analysis.md
│
└─► ⚠️ 问题排查
    └─► references/troubleshooting.md
        - 命令卡住（忘加--yolo）
        - API限额
        - 文件路径问题
```

---

## Architecture Deep Dive

### 为什么是 Skills + Subagent？

```
❌ 直接在主对话执行的问题：

User: "用gemini分析这个项目"
Claude: [执行 gemini --all-files -p "分析架构"]
Gemini输出: [5000行分析结果全部灌入主对话]
结果: 主对话context爆炸，后续对话质量下降

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Skills + Subagent 的优势：

User: "用gemini分析这个项目"
Skill: [识别意图，调用gemini-executor子代理]
Subagent: [执行命令，处理5000行输出]
         [生成精简摘要返回]
主对话: 只收到摘要，context保持清爽
```

### 职责分离原则

| 组件 | 职责 | 原则 |
|------|------|------|
| **Skill** | 意图识别 + 任务分发 | 要**薄**，不做复杂执行 |
| **Subagent** | 命令执行 + 结果处理 | 要**通用**，集中逻辑 |
| **主对话** | 用户交互 + 工作流编排 | 保持**清爽**，像驾驶舱 |

---

## Gemini CLI 核心参数

```bash
# 基础用法
gemini -p "你的提示词" [文件...] --yolo

# 关键参数
-p "prompt"      # 提示词（必须）
--yolo           # 跳过确认（非交互场景必须！）
--all-files      # 分析当前目录所有文件
--model <name>   # 指定模型（默认gemini-pro）

# 多模态示例
gemini -p "描述这张图" image.png --yolo
gemini -p "总结视频内容" video.mp4 --yolo
gemini -p "提取关键信息" report.pdf --yolo
gemini -p "转录音频" meeting.mp3 --yolo

# 代码分析
cd /path/to/repo && gemini --all-files -p "分析架构" --yolo
```

### ⚠️ 必须记住的一点

```
--yolo 不是可选项，是救命项！

非交互场景（如Subagent调用）不加 --yolo：
→ 命令卡在确认步骤
→ 整条链路死掉
→ 你以为是bug，其实是少了4个字符
```

---

## 文件结构

```
gemini-cli-integration/
├── SKILL.md                      # 本文件：入口+导航
├── agents/
│   └── gemini-executor.md        # Subagent定义（复制到~/.claude/agents/）
├── references/
│   ├── setup-guide.md            # 完整安装配置指南
│   ├── use-cases.md              # 使用场景详解
│   └── troubleshooting.md        # 问题排查
└── examples/
    ├── image-analysis.md         # 图片分析示例
    ├── video-summary.md          # 视频总结示例
    └── repo-analysis.md          # 仓库分析示例
```

---

## 部署检查清单

### 安装阶段
- [ ] Node.js 18+ 已安装
- [ ] Gemini CLI 已安装 (`npm install -g @google/gemini-cli`)
- [ ] API Key 已配置
- [ ] `gemini -p "hello" --yolo` 能正常返回

### 部署阶段
- [ ] Skill 已复制到 `~/.claude/skills/gemini-cli/`
- [ ] Subagent 已复制到 `~/.claude/agents/`
- [ ] Claude Code 能识别"用Gemini..."触发词

### 验证阶段
- [ ] 图片分析正常
- [ ] 文件路径正确传递
- [ ] 结果能正常返回主对话

---

## 常见触发语

Claude Code会自动识别这些意图并调用Gemini：

```
图片相关：
- "用Gemini看看这张图"
- "让Gemini分析这个截图"
- "Gemini帮我描述一下 xxx.png"

视频/音频：
- "用Gemini总结这个视频"
- "让Gemini转录这段录音"
- "Gemini提取会议要点 meeting.mp3"

文档处理：
- "Gemini帮我读这份PDF"
- "用Gemini提炼这个报告的核心观点"

代码分析：
- "让Gemini扫描整个项目"
- "用Gemini分析这个仓库的架构"
- "Gemini帮我找潜在的代码问题"
```

---

## 信心赋予

这个集成的核心价值不是"又多一个模型可用"，而是：

**你开始像搭系统一样用AI**

- Claude Code 强在编码与工作流
- Gemini CLI 强在多模态与超长上下文
- 组合起来，各司其职

**Skills 负责理解意图，Subagent 负责执行任务，主对话保持干净。**

你不是在"用AI"，你是在"搭一个能跑的生产系统"。
