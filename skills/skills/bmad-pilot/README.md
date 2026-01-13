# BMAD Pilot - 敏捷开发工作流编排器

**版本**: 1.0.0
**类别**: 工作流编排
**投入时间**: 30分钟
**灵感来源**: [myclaude](https://github.com/emsi/myclaude) BMAD模式

---

## 🎯 一句话介绍

自动编排6个专业角色（PO、架构师、技术主管、开发、审查、QA），完成端到端的敏捷开发流程。

---

## ✨ 核心特性

- ✅ **6个专业角色**：Product Owner → Architect → Tech Lead → Developer → Code Reviewer → QA Engineer
- ✅ **完整交付包**：需求文档 + 架构设计 + Sprint计划 + 实现代码 + 审查报告 + 测试结果
- ✅ **零架构改造**：充分利用现有MindSymphony技能生态
- ✅ **灵活编排**：可根据需求调整工作流重点
- ✅ **企业级质量**：代码审查、测试覆盖、性能标准

---

## 🚀 快速开始

### 基础用法
```bash
/bmad "添加用户登录功能"
```

### 重点开发
```bash
/bmad "重构支付模块 - 重点关注安全性"
```

### 快速原型
```bash
/bmad "快速验证实时聊天想法 - 跳过完整测试"
```

---

## 📊 工作流程

```
需求分析 (PO)
    ↓
架构设计 (Architect)
    ↓
Sprint规划 (Tech Lead)
    ↓
开发实现 (Developer)
    ↓
代码审查 (Code Reviewer)
    ↓
测试验证 (QA Engineer)
    ↓
✅ 完整交付包
```

---

## 🎯 对应的MindSymphony技能

| BMAD角色 | MindSymphony技能 | 职责 |
|----------|------------------|------|
| Product Owner | `c-06-knowledge-explorer` | 需求分析 |
| Architect | `b-07-codebase-ecologist` | 架构设计 |
| Tech Lead | `m-03-cognitive-architect` | 任务分解 |
| Developer | `b-08-intelligent-refactor` | 代码实现 |
| Code Reviewer | 内置代码审查能力 | 代码审查 |
| QA Engineer | `testing-strategy-planner` | 测试验证 |

---

## 💡 与myclaude的区别

| 特性 | myclaude BMAD | MindSymphony BMAD Pilot |
|------|---------------|------------------------|
| 实现方式 | 6个固定代理 | 动态技能编排 |
| 技能生态 | ~10个 | 90+个 |
| 工作流 | 固定流程 | 灵活可调 |
| 质量门控 | 强制90% | 建议80% |
| 架构改造 | 需要 | 零改造 |

**优势**：保留MindSymphony的灵活性，同时提供企业级工作流体验。

---

## 📚 完整文档

详见 [SKILL.md](./SKILL.md)

---

## 🎓 示例输出

输入：
```bash
/bmad "添加用户登录功能"
```

输出：
```markdown
# 用户登录功能 - 完整交付包

## 📋 需求文档 (Product Owner)
- 用户故事
- 验收标准
- 优先级评估

## 🏗️ 架构设计 (Architect)
- 系统架构图
- 技术栈选型
- 安全方案

## 📅 Sprint计划 (Tech Lead)
- 任务分解（14小时 / 4天）
- 依赖分析
- 风险识别

## 💻 实现代码 (Developer)
- 完整代码实现
- 单元测试（85%覆盖）
- 文档注释

## 🔍 代码审查报告 (Code Reviewer)
- 质量评分：9/10
- 安全检查
- 改进建议

## 🧪 测试报告 (QA Engineer)
- 测试通过率：100%
- 性能评分：A+
- 质量评估：✅ 可以上线
```

---

## 🔗 相关资源

- [MindSymphony 主文档](../../mindsymphony/SKILL.md)
- [myclaude GitHub](https://github.com/emsi/myclaude)
- [敏捷开发最佳实践](https://agilemanifesto.org/)

---

## 📄 许可证

MIT License

---

**开始你的第一个BMAD工作流吧！** 🚀
