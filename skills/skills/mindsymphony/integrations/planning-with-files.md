---
name: planning-with-files
type: integration
external_path: /skills/skills/planning-with-files
priority: high
triggers:
  zh: [计划, 规划, 工作流, 任务计划, 项目管理, 复杂任务, 研究]
  en: [plan, planning, workflow, task plan, project management]
commands:
  - /plan [任务描述]
  - /planning [任务描述]
---

# Planning with Files - 工作流记忆集成

> **像 Manus 一样工作** — 使用文件系统作为 AI 的持久化记忆

---

## 核心能力

### Manus 风格持久化记忆

```yaml
核心理念:
  context_window: "RAM (易失、有限)"
  filesystem: "Disk (持久、无限)"
  rule: "任何重要信息都写入磁盘"
```

### 3文件模式

```
task_plan.md      → 阶段和进度追踪
findings.md       → 研究和发现存储
progress.md       → 会话日志和测试结果
```

---

## 触发词

### 中文
- 计划、规划、工作流
- 任务计划、项目管理
- 复杂任务、研究

### English
- plan, planning, workflow
- task plan, project management
- complex task

---

## 命令前缀

```
/plan [你的任务描述]
/planning [你的任务描述]
```

---

## 使用示例

### 示例1：复杂重构任务

```
用户：帮我规划这个大型项目的认证系统重构

激活：planning-with-files
响应：
1. 创建 .planning/ 目录
2. 生成 task_plan.md（阶段分解）
3. 初始化 findings.md（代码结构发现）
4. 初始化 progress.md（操作日志）
5. 开始扫描和分析代码
```

### 示例2：代码库研究

```
用户：我需要研究这个项目的架构

激活：planning-with-files
响应：
1. 创建3文件模式
2. 扫描项目结构 → findings.md
3. 记录关键文件和依赖
4. 生成架构洞察
5. 持续更新 findings.md
```

---

## 与其他 Skill 协作

### 与 cognitive-architect 配合

```yaml
场景：复杂任务规划
planning-with-files:
  - 创建3文件模式
  - 持久化计划
cognitive-architect:
  - 任务分解
  - 协调其他 skills
结果：计划持久化 + 智能分解
```

### 与 knowledge-explorer 配合

```yaml
场景：深度研究
planning-with-files:
  - findings.md 存储发现
knowledge-explorer:
  - 系统化研究方法
  - 多维度分析
结果：研究成果持久化
```

### 与 code-refactoring-expert 配合

```yaml
场景：代码重构
planning-with-files:
  - task_plan.md 追踪重构阶段
  - progress.md 记录操作历史
code-refactoring-expert:
  - 重构策略
  - 代码改进建议
结果：重构过程可追溯
```

---

## 核心规则 (四大原则)

### 1. 先创建计划

```markdown
识别复杂任务 → 创建 task_plan.md → 定义阶段 → 开始执行
```

### 2. 2动作规则

```markdown
每2次查看/浏览器操作 → 保存到 findings.md
```

### 3. 记录所有错误

```markdown
task_plan.md → 尝试记录表
| 尝试 | 方法 | 结果 | 下一步 |
```

### 4. 永不重复失败

```markdown
追踪尝试 → 分析失败 → 变更方法 → 再次尝试
```

---

## 何时使用

### ✅ 使用此模式

- 多步骤任务 (3+ 步骤)
- 研究任务
- 构建/创建项目
- 跨越多工具调用的任务

### ❌ 跳过此模式

- 简单问题
- 单文件编辑
- 快速查询

---

## 模板位置

```
/skills/skills/planning-with-files/templates/
├── task_plan.md      # 任务计划模板
├── findings.md       # 研究发现模板
└── progress.md       # 进度日志模板
```

---

## 初始化脚本

```bash
# 使用 Python 脚本初始化
python /skills/skills/planning-with-files/init_planning.py \
  --task "重构认证系统" \
  --objective "提高安全性和可维护性"
```

---

## 文件结构

```
.planning/
├── task_plan.md      # 阶段和进度追踪
├── findings.md       # 研究和发现存储
└── progress.md       # 会话日志和测试结果
```

---

## 详细文档

完整文档位置：`/skills/skills/planning-with-files/SKILL.md`

包含：
- 3文件模式详解
- 工作流程图
- 最佳实践
- 模板文件
- 初始化脚本
