# MindSymphony OS 🧠

> 统一AI认知操作系统 - 整合式技能生态系统

[![Version](https://img.shields.io/badge/version-21.0.0--evolution-blue)](https://github.com/yourusername/mindsymphony-os)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-30+-purple)](skills/skills/)

---

## 📖 项目简介

MindSymphony OS 是一个统一的 AI 认知操作系统，通过技能生态系统为 Claude Code 提供强大的能力扩展。

### 核心特性

- 🧠 **统一认知架构** - 蜂后协奏系统，多技能智能调度
- 🔌 **技能生态** - 30+ 领域技能，覆盖开发、设计、研究、写作
- 📋 **工作流记忆** - Manus 风格持久化记忆系统
- 🎯 **任务管理** - Linear 集成的敏捷开发工作流
- 🔌 **插件开发** - Obsidian 插件开发专家（27 条规则）
- 🌐 **多模态支持** - Gemini CLI 集成，处理视频/音频/大文件

---

## 🚀 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/mindsymphony-os.git
cd mindsymphony-os

# 将 skills 链接到你的 Claude Code
# Windows
mklink /D "C:\Users\YourUsername\.claude\skills" "D:\mindsymphony-os\skills\skills"

# macOS/Linux
ln -s "$(pwd)/skills/skills" ~/.claude/skills
```

### 基本使用

在 Claude Code 中，技能会根据你的需求自动激活：

```bash
# 创建任务计划
/plan 我需要重构认证系统

# 开发 Obsidian 插件
/obsidian 创建一个任务管理插件

# Linear 任务管理
/linear 分解这个 Epic 为 Stories
```

---

## 📁 项目结构

```
mindsymphony-os/
├── skills/                    # 技能生态系统
│   └── skills/
│       ├── mindsymphony/      # 核心协奏系统
│       │   ├── SKILL.md       # 主入口
│       │   ├── integrations/  # 集成层
│       │   ├── extensions/    # 扩展技能
│       │   ├── router/        # 意图路由
│       │   └── registry/      # 技能注册
│       ├── planning-with-files/      # 工作流记忆
│       ├── obsidian-plugin-dev/      # Obsidian 插件开发
│       ├── linear-task-manager/      # 任务管理系统
│       ├── frontend-design/          # 前端设计
│       ├── mcp-builder/              # MCP 服务器构建
│       └── [30+ skills]              # 更多技能...
├── docs/                      # 文档
├── tests/                    # 测试
├── scripts/                  # 工具脚本
└── README.md                 # 本文件
```

---

## 🎯 核心技能

### 1. MindSymphony（核心）

统一认知操作系统，提供：
- 意图路由与技能调度
- 蜂后协奏模式
- 信息素协作机制
- 价值对齐原则

### 2. Planning with Files

Manus 风格持久化记忆：
- task_plan.md - 任务计划与阶段追踪
- findings.md - 研究发现存储
- progress.md - 会话日志与进度

### 3. Obsidian Plugin Dev

Obsidian 插件开发专家：
- 27 条关键开发规则
- 提交验证（Bot 检查）
- 内存管理与可访问性
- ESLint 集成

### 4. Linear Task Manager

敏捷开发工作流：
- Epic/Story/Task 层级管理
- 完整工作流自动化
- 质量门与代码审查
- 标准研究与最佳实践

---

## 🔌 集成技能

| 技能 | 描述 | 状态 |
|------|------|------|
| academic-forge | 学术研究锻造 | ✅ |
| academic-manuscript | 学术写作 | ✅ |
| ai-agent-architect | Agent 设计 | ✅ |
| gemini-cli-integration | 多模态集成 | ✅ |
| planning-with-files | 工作流记忆 | ✅ |
| obsidian-plugin-dev | Obsidian 插件 | ✅ |
| linear-task-manager | 任务管理 | ✅ |
| skill-creator-meta | 技能创建 | ✅ |
| frontend-design | 前端设计 | ✅ |
| mcp-builder | MCP 构建 | ✅ |
| code-refactoring-expert | 代码重构 | ✅ |
| doc-coauthoring | 文档协作 | ✅ |
| pdf | PDF 处理 | ✅ |
| docx | Word 文档 | ✅ |
| pptx | PowerPoint | ✅ |
| ... | ... | ... |

---

## 🛠️ 开发

### 技能创建

```bash
# 使用 skill-creator-meta 创建新技能
/skill create 我需要一个新技能来处理 X 任务
```

### 技能验证

```bash
# 验证技能结构
python scripts/validate_skill.py skills/skills/your-skill/
```

---

## 📚 文档

- [MindSymphony v21.0 迁移指南](MINDSYMPHONY_V21_MIGRATION_GUIDE.md)
- [技能发现与路由系统](PROJECT_SUMMARY.md)
- [技能协作总结](SKILL_COLLABORATION_SUMMARY.md)
- [集成实现报告](INTEROP_IMPLEMENTATION_REPORT.md)

---

## 🤝 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](docs/CONTRIBUTING.md) 了解详情。

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 🙏 致谢

- **Anthropic** - Claude Code 平台
- **OthmanAdi** - planning-with-files 原型
- **gapmiss** - obsidian-plugin-skill
- **levnikolaevich** - claude-code-skills (84 生产级 skills)
- **MindSymphony 社区** - 所有贡献者

---

## 📮 联系

- GitHub: [yourusername](https://github.com/yourusername)
- Issues: [提交问题](https://github.com/yourusername/mindsymphony-os/issues)

---

**Made with ❤️ by the MindSymphony community**
