# BMAD Pilot 快速上手指南

**创建时间**: 2026-01-12
**投入时间**: 30分钟
**状态**: ✅ 已完成并推送

---

## 🎉 恭喜！BMAD Pilot已成功创建

你现在拥有了MindSymphony的企业级敏捷开发工作流编排器！

---

## 🚀 立即开始使用

### 1. 基础用法

在Claude Code中，直接输入：

```bash
/bmad "添加用户登录功能，支持邮箱和手机号登录"
```

**预期输出**：完整的6阶段交付包（5-15分钟）

---

### 2. 工作流程

```
📋 Phase 1: 需求分析 (Product Owner)
   ↓ 调用: c-06-knowledge-explorer
   ✓ 用户故事、验收标准、优先级

🏗️ Phase 2: 架构设计 (Architect)
   ↓ 调用: b-07-codebase-ecologist
   ✓ 系统设计、技术选型、安全架构

📅 Phase 3: Sprint规划 (Tech Lead)
   ↓ 调用: m-03-cognitive-architect
   ✓ 任务分解、工作量估算、依赖分析

💻 Phase 4: 开发实现 (Developer)
   ↓ 调用: b-08-intelligent-refactor
   ✓ 代码实现、单元测试、文档

🔍 Phase 5: 代码审查 (Code Reviewer)
   ↓ 内置代码审查能力
   ✓ 质量检查、安全扫描、改进建议

🧪 Phase 6: 测试验证 (QA Engineer)
   ↓ 调用: testing-strategy-planner
   ✓ 测试策略、测试执行、质量报告
```

---

## 📚 使用示例

### 示例 1: 新功能开发

```bash
/bmad "实现实时聊天功能，支持文本、图片、文件发送"
```

**适用场景**：从零开始开发新功能

---

### 示例 2: 代码重构

```bash
/bmad "重构支付模块，重点关注安全性和性能优化"
```

**适用场景**：优化现有代码，提升质量

---

### 示例 3: 快速原型

```bash
/bmad "快速验证想法 - 社交分享功能 - 跳过完整测试"
```

**适用场景**：快速验证想法，不需要完整测试

---

### 示例 4: 安全优先

```bash
/bmad "添加管理后台 - 最高安全标准，包含双因素认证"
```

**适用场景**：安全性要求高的功能

---

### 示例 5: 迭代优化

```bash
/bmad "基于上次代码审查的建议，优化登录模块的性能"
```

**适用场景**：根据反馈进行迭代改进

---

## 🎯 完整输出示例

当你运行：
```bash
/bmad "添加用户登录功能"
```

你将得到：

```markdown
# 用户登录功能 - 完整交付包

## 📋 1. 需求文档 (Product Owner)
### 用户故事
作为用户，我想要通过邮箱或手机号登录...

### 验收标准
- ✅ 支持邮箱登录
- ✅ 支持手机号登录
- ✅ 密码强度验证
- ✅ 错误提示友好

---

## 🏗️ 2. 架构设计 (Architect)
### 系统架构图
[完整的架构图]

### 技术栈
- 前端: React + TypeScript
- 后端: Node.js + Express
- 数据库: PostgreSQL
- 认证: JWT + bcrypt

---

## 📅 3. Sprint计划 (Tech Lead)
### 任务分解
- Task 1: 数据库表设计 (2h)
- Task 2: 后端API开发 (4h)
- Task 3: 前端登录页面 (3h)
- Task 4: 单元测试 (2h)

### 总工作量: 14小时 / 4天

---

## 💻 4. 实现代码 (Developer)
### 核心代码
```typescript
// src/auth/login.ts
export async function login(
  identifier: string,
  password: string
): Promise<AuthToken> {
  // 完整实现...
}
```

### 测试代码
```typescript
// tests/auth.test.ts
describe('Login', () => {
  it('should login with email', async () => {
    // 完整测试...
  });
});
```

---

## 🔍 5. 代码审查报告 (Code Reviewer)
### 总体评分: 9/10 ⭐

### 优点
✅ 代码结构清晰
✅ 测试覆盖率85%
✅ 安全性良好

### 改进建议
📝 建议添加rate limiting
📝 建议记录登录失败日志

---

## 🧪 6. 测试报告 (QA Engineer)
### 测试结果
- 单元测试: 15/15 通过 ✅
- 集成测试: 8/8 通过 ✅
- E2E测试: 5/5 通过 ✅

### 质量评估
✅ 所有测试通过
✅ 性能符合预期
✅ **可以上线！**
```

---

## 💡 高级技巧

### 1. 调整工作流重点

```bash
# 重点关注安全性
/bmad "支付功能 - 重点关注安全性"

# 重点关注性能
/bmad "数据查询优化 - 重点关注性能"

# 快速原型，跳过详细设计
/bmad "快速验证想法 - AI推荐系统"
```

---

### 2. 与其他技能协作

BMAD会自动调用相关技能：

```bash
/bmad "创建设计系统和组件库"
# 自动调用: brand-guidelines, theme-factory, canvas-design
```

---

### 3. 控制质量标准

```bash
# 高质量标准
/bmad "核心支付模块 - 90%测试覆盖率，最高安全标准"

# 快速迭代
/bmad "实验性功能 - 快速原型，70%覆盖率即可"
```

---

## 🎯 与myclaude的对比

### myclaude BMAD
```python
# 需要安装和配置
python3 install.py --module bmad
# 固定6个代理
# 强制90%覆盖率
# 需要Codex后端
```

### MindSymphony BMAD Pilot
```bash
# 零配置，立即可用
/bmad "需求描述"
# 灵活的技能编排
# 建议80%覆盖率（可调）
# 纯Claude驱动
```

**优势**：
- ✅ 更简单：零配置，即插即用
- ✅ 更灵活：动态调整工作流
- ✅ 更丰富：90+技能生态支持
- ✅ 零改造：不破坏现有架构

---

## 🔧 故障排除

### Q1: BMAD执行时间很长？
**A**: 正常现象！完整的企业级工作流需要编排6个技能，通常5-15分钟。

### Q2: 可以跳过某些阶段吗？
**A**: 可以！在提示词中说明：
```bash
/bmad "功能描述 - 跳过详细架构设计"
```

### Q3: 如何调整质量标准？
**A**: 在需求中明确：
```bash
/bmad "功能 - 90%测试覆盖，最高安全标准"
```

### Q4: 输出太长怎么办？
**A**: 要求简化版本：
```bash
/bmad "功能描述 - 提供简化版交付包"
```

---

## 📊 适用场景

### ✅ 适合BMAD的场景
- 新功能开发
- 代码重构
- 快速原型验证
- 企业项目交付
- Sprint规划

### ❌ 不太适合的场景
- 简单bug修复（太重了）
- 微调代码格式（用refactor更快）
- 探索性研究（用knowledge-explorer）

---

## 📈 下一步

### 1. 立即尝试
```bash
/bmad "你的第一个需求"
```

### 2. 查看完整文档
```bash
cat skills/skills/bmad-pilot/SKILL.md
```

### 3. 探索相关技能
- `c-06-knowledge-explorer` - 深度研究
- `b-07-codebase-ecologist` - 代码库分析
- `m-03-cognitive-architect` - 复杂任务分解
- `testing-strategy-planner` - 测试策略

### 4. 提供反馈
使用后，记录：
- ✅ 哪些部分很有用
- ⚠️ 哪些需要改进
- 💡 新功能建议

---

## 🎉 总结

**你刚刚用30分钟**：
- ✅ 获得了企业级敏捷工作流能力
- ✅ 零架构改造，完全兼容
- ✅ 保留了MindSymphony的灵活性
- ✅ 吸收了myclaude的最佳实践

**投入**: 30分钟
**收益**: 企业级工作流编排
**风险**: 零（只添加，不修改）

---

## 🔗 相关资源

- **BMAD Pilot文档**: `skills/skills/bmad-pilot/SKILL.md`
- **INTEROP配置**: `skills/skills/bmad-pilot/INTEROP.yml`
- **myclaude项目**: https://github.com/emsi/myclaude
- **MindSymphony主文档**: `skills/skills/mindsymphony/SKILL.md`

---

## 📄 文件清单

```
skills/skills/bmad-pilot/
├── SKILL.md         # 920行完整文档
├── INTEROP.yml      # 智能路由配置
└── README.md        # 快速参考
```

---

**开始你的第一个BMAD工作流吧！** 🚀

```bash
/bmad "你的需求描述"
```
