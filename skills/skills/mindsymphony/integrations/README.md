---
name: integrations
type: system
description: 外部Skill快捷入口，统一调用接口
version: 1.0
---

# MindSymphony 集成层 (Integrations)

> 为所有外部Skill提供统一的调用入口，避免用户需要记住多个skill的具体路径。

---

## 架构定位

```
用户
  │
  ▼
┌─────────────────────────────────────────┐
│          MindSymphony 主入口            │
│             (SKILL.md)                  │
├─────────────────────────────────────────┤
│          Intent Router                  │
│         (意图路由器)                     │
├─────────────────────────────────────────┤
│                                         │
│    ┌─────────┐  ┌─────────┐            │
│    │  Core   │  │Extension│            │
│    │ Skills  │  │ Skills  │            │
│    └─────────┘  └─────────┘            │
│                                         │
│    ┌─────────────────────────────────┐ │
│    │      Integrations Layer         │ │  ← 本层
│    │  ┌───────┐ ┌───────┐ ┌───────┐ │ │
│    │  │acad-  │ │agent- │ │gemini │ │ │
│    │  │forge  │ │arch   │ │-cli   │ │ │
│    │  └───────┘ └───────┘ └───────┘ │ │
│    └─────────────────────────────────┘ │
│                                         │
└─────────────────────────────────────────┘
```

---

## 已集成Skill

### 1. academic-forge（学术研究）

```yaml
name: academic-forge
location: /mnt/skills/user/academic-forge
status: active
version: latest

# 快捷触发
triggers:
  - "学术研究"
  - "研究设计"
  - "统计方法"
  - "NHANES分析"
  - "队列研究"

# 能力概述
capabilities:
  - 研究设计与报告标准选择
  - 统计方法选择与实施
  - 预测模型开发
  - 学术写作指导
  - 审稿意见回复

# 调用示例
examples:
  - input: "设计一个BRI与全因死亡率的队列研究"
    action: "加载academic-forge，启动研究设计流程"
    
  - input: "NHANES数据应该用什么统计方法分析"
    action: "加载academic-forge，进入统计方法选择模块"
```

### 2. academic-manuscript（学术写作）

```yaml
name: academic-manuscript
location: /mnt/skills/user/academic-manuscript
status: active
version: latest

triggers:
  - "写论文"
  - "学术写作"
  - "SCI投稿"
  - "审稿意见"
  - "修改稿件"

capabilities:
  - Methods/Results/Discussion撰写
  - 表格图形制作
  - 投稿准备
  - 审稿意见回复
  - 格式规范检查

examples:
  - input: "帮我写这篇论文的Methods部分"
    action: "加载academic-manuscript，进入Methods写作模块"
```

### 3. ai-agent-architect（Agent设计）

```yaml
name: ai-agent-architect
location: /mnt/skills/user/ai-agent-architect
status: active
version: latest

triggers:
  - "agent设计"
  - "智能体架构"
  - "ReAct模式"
  - "认知架构"
  - "AI代理开发"

capabilities:
  - Language Agent架构设计
  - ReAct/ToT/Reflexion实现
  - 评估基准设计
  - CoALA框架应用
  - 训练与推理权衡

examples:
  - input: "设计一个能自主完成研究任务的agent"
    action: "加载ai-agent-architect，进入架构设计模块"
```

### 4. skill-creator-meta（Skill创建）

```yaml
name: skill-creator-meta
location: /mnt/skills/user/skill-creator-meta
status: active
version: 2.2

triggers:
  - "创建skill"
  - "skill开发"
  - "技能设计"
  - "skill架构"

capabilities:
  - Skill架构设计
  - 文档结构规范
  - 验证与测试
  - 打包发布

examples:
  - input: "帮我创建一个医学诊断的skill"
    action: "加载skill-creator-meta，进入需求分析阶段"
```

### 5. gemini-cli-integration（多模态）

```yaml
name: gemini-cli-integration
location: /mnt/skills/user/gemini-cli-integration
status: active
version: 1.0

triggers:
  - "用gemini"
  - "分析视频"
  - "音频转录"
  - "大文件分析"
  - "100万token"

capabilities:
  - 视频内容理解与总结
  - 音频转录与整理
  - 超大文件/代码库分析
  - 图片批量处理

examples:
  - input: "用gemini分析这个会议视频"
    action: "加载gemini-cli-integration，执行视频分析"

  - input: "帮我扫描整个代码仓库的架构"
    action: "加载gemini-cli-integration，执行仓库分析"

# 特殊要求
requirements:
  - "需要安装: npm install -g @google/gemini-cli"
  - "需要配置: GEMINI_API_KEY"
  - "命令必须加: --yolo"
```

### 6. planning-with-files（工作流记忆）

```yaml
name: planning-with-files
location: /skills/skills/planning-with-files
status: active
version: 1.0.0

triggers:
  - "计划"
  - "规划"
  - "工作流"
  - "任务计划"
  - "项目管理"

capabilities:
  - Manus 风格持久化记忆
  - 3文件模式 (task_plan.md, findings.md, progress.md)
  - 复杂任务分解与追踪
  - 研究发现存储
  - 进度持久化

examples:
  - input: "帮我规划这个重构项目"
    action: "加载planning-with-files，创建3文件模式，开始任务分解"

  - input: "我需要研究这个大型代码库"
    action: "激活planning-with-files，使用findings.md存储研究发现"

# 命令前缀
commands:
  - /plan [任务描述]
  - /planning [任务描述]

# 核心原则
principles:
  - 先创建计划，绝不盲目开始
  - 每2次操作保存发现
  - 记录所有错误和尝试
  - 永不重复失败
```

### 7. obsidian-plugin-dev（Obsidian 插件开发）

```yaml
name: obsidian-plugin-dev
location: /skills/skills/obsidian-plugin-dev
status: active
version: 1.0.0

triggers:
  - "Obsidian插件"
  - "obsidian plugin"
  - "插件开发"
  - "manifest.json"
  - "Obsidian API"

capabilities:
  - 27条关键插件开发规则
  - 提交验证（Bot 检查规则）
  - 内存管理与生命周期
  - 可访问性要求（MANDATORY）
  - API 最佳实践
  - 安全与 iOS 兼容性

examples:
  - input: "帮我创建一个 Obsidian 插件"
    action: "加载obsidian-plugin-dev，使用脚手架生成器创建插件"

  - input: "检查我的插件是否符合提交要求"
    action: "激活obsidian-plugin-dev，运行27条规则验证"

# 命令前缀
commands:
  - /obsidian [任务描述]
  - /plugin [任务描述]

# 核心规则
rules:
  - Plugin ID: 无 "obsidian"，不以 "plugin" 结尾
  - Plugin name: 无 "Obsidian"，不以 "Plugin" 结尾
  - Description: 必须以标点结尾，无 "This plugin"
  - 内存: 使用 registerEvent()，不存储视图引用
  - 可访问性: 所有交互元素键盘可访问
```

### 8. linear-task-manager（Linear 任务管理）

```yaml
name: linear-task-manager
location: /skills/skills/linear-task-manager
status: active
version: 1.0.0

triggers:
  - "Linear"
  - "任务管理"
  - "Epic"
  - "Story"
  - "敏捷开发"
  - "任务分解"

capabilities:
  - Epic/Story/Task 层级管理
  - 完整敏捷工作流自动化
  - Linear API 集成
  - 标准研究与最佳实践
  - 质量门与代码审查
  - 基于风险的测试策略

examples:
  - input: "帮我分解这个 Epic 为 Stories"
    action: "加载linear-task-manager，执行Epic分解，创建5-10个Stories"

  - input: "验证这个 Story 是否符合 2025 标准"
    action: "激活linear-task-manager，运行Story验证（CRITICAL PATH FIRST）"

# 命令前缀
commands:
  - /linear [action]
  - /epic [operation]
  - /story [operation]

# 工作流
workflow:
  - Epic 分解 → Story 创建 → 任务执行 → 质量门 → 完成
  - 自动化: ln-400-story-executor (完全自动)
  - 手动: 分步执行每个阶段

# 任务层级
hierarchy:
  Epic (Linear Project)
    └── Story (Issue with label: user-story)
        └── Task (Issue with parentId: storyId)
```

---

## 调用协议

### 统一调用格式

```markdown
## 当识别到外部skill需求时

1. 确认skill已注册且可用
2. 显示将要调用的skill
3. 提供简要说明
4. 执行调用

## 示例输出

检测到你的需求涉及【学术研究】领域。

📦 **调用**: academic-forge
📝 **能力**: 研究设计、统计方法、学术写作
🔗 **位置**: /mnt/skills/user/academic-forge

正在加载skill...

---

[academic-forge 接管]
```

### 上下文传递

```yaml
# 从MindSymphony传递给外部skill的上下文
context_handover:
  - user_intent: "用户的原始意图"
  - extracted_keywords: ["关键词1", "关键词2"]
  - session_history: "相关的对话历史"
  - mindsymphony_state: "当前系统状态"
```

---

## 集成新Skill的流程

### Step 1: 评估（使用skill-curator）

```markdown
1. 运行skill-curator的评估流程
2. 确认skill质量达标（>70分）
3. 确认与现有skill不冲突
```

### Step 2: 注册

```yaml
# 在 registry/skills.yml 中添加
external_skills:
  new-skill-name:
    path: /mnt/skills/user/new-skill
    type: domain
    triggers:
      zh: [触发词1, 触发词2]
      en: [trigger1, trigger2]
    priority: 80
    description: 简要描述
```

### Step 3: 创建入口

```markdown
# 在 integrations/ 目录下创建 new-skill.md
# 包含：触发器、能力、示例
```

### Step 4: 更新路由

```python
# 在 router/intent-router.md 中添加触发词
EXACT_TRIGGERS["新触发词"] = "new-skill-name"
```

### Step 5: 测试

```markdown
测试用例：
1. 精确触发词能否正确路由
2. 领域关键词能否识别
3. 上下文传递是否完整
4. 返回结果是否正确整合
```

---

## 错误处理

### Skill不可用

```markdown
⚠️ **Skill不可用**

请求的skill【gemini-cli-integration】当前不可用。

可能原因：
- 未安装依赖
- 配置缺失
- 路径错误

建议操作：
1. 检查skill是否存在于 /mnt/skills/user/
2. 查看skill的安装要求
3. 使用替代方案（如有）
```

### 路由失败

```markdown
🤔 **需要澄清**

你的请求涉及多个可能的领域：
1. 【学术研究】- academic-forge
2. 【内容写作】- official-writer

请告诉我更具体的需求，或选择一个方向。
```

---

## 性能考量

### 延迟优化

```markdown
## 原则

1. 路由层0延迟（关键词匹配）
2. Skill加载按需（不预加载）
3. 上下文精简传递（只传必要信息）

## 对比

| 操作 | 传统方式 | 优化后 |
|------|----------|--------|
| 路由 | 3-5s (LLM) | 0ms (关键词) |
| 加载 | 全量加载 | 按需加载 |
| 传递 | 完整历史 | 精简上下文 |
```

---

## 当前集成状态

| Skill | 状态 | 测试 | 文档 |
|-------|------|------|------|
| academic-forge | ✅ Active | ✅ | ✅ |
| academic-manuscript | ✅ Active | ✅ | ✅ |
| ai-agent-architect | ✅ Active | ✅ | ✅ |
| skill-creator-meta | ✅ Active | ✅ | ✅ |
| gemini-cli-integration | ✅ Active | ✅ | ✅ |
| planning-with-files | ✅ Active | ⏳ | ✅ |
| obsidian-plugin-dev | ✅ Active | ⏳ | ✅ |
| linear-task-manager | ✅ Active | ⏳ | ✅ |

---

## 待集成列表

| Skill | 来源 | 优先级 | 状态 |
|-------|------|--------|------|
| TKassis/scientific-skills | GitHub | 中 | 待评估 |
| anthropics/infographics | 官方 | 高 | 待适配 |
