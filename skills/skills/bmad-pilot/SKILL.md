---
name: bmad-pilot
description: BMAD敏捷开发工作流编排器 - 自动编排6个角色完成端到端开发
version: 1.0.0
category: workflow
tags: [agile, bmad, workflow, enterprise, orchestration]
author: MindSymphony Team
license: MIT
---

# BMAD Pilot - 敏捷开发工作流编排器

## 🎯 概述

BMAD Pilot是MindSymphony的企业级敏捷开发工作流编排器，灵感来自myclaude的BMAD模式，但充分利用MindSymphony丰富的技能生态。

**BMAD** = **B**uild **M**easure **A**nalyze **D**eploy

自动编排6个专业角色，执行完整的软件开发生命周期。

---

## 🚀 快速开始

### 触发方式

```bash
/bmad "功能需求描述"
```

### 示例

```bash
/bmad "添加用户登录功能，支持邮箱和手机号登录"
```

```bash
/bmad "重构支付模块，提升性能和安全性"
```

```bash
/bmad "实现实时聊天功能，支持文本、图片、文件"
```

---

## 📋 工作流程

### Phase 1: 需求分析 (Product Owner)
**调用技能**: `c-06-knowledge-explorer`

**职责**:
- 📝 分析用户需求
- ✅ 定义验收标准
- 🎯 确定优先级
- 👥 识别利益相关者
- 📊 评估业务价值

**输出**:
```markdown
## 需求文档
### 用户故事
作为[角色]，我想要[功能]，以便[价值]

### 验收标准
- [ ] 标准1
- [ ] 标准2
- [ ] 标准3

### 优先级
P0 - 必须 / P1 - 重要 / P2 - 可选
```

---

### Phase 2: 架构设计 (Architect)
**调用技能**: `b-07-codebase-ecologist`

**职责**:
- 🏗️ 系统架构设计
- 🔧 技术选型
- 📐 数据模型设计
- 🔒 安全架构
- 🔗 集成方案

**输出**:
```markdown
## 架构设计
### 系统架构图
[组件图、序列图、类图]

### 技术栈
- 前端: React / Vue / ...
- 后端: Node.js / Python / ...
- 数据库: PostgreSQL / MongoDB / ...

### 安全考虑
- 认证: JWT / OAuth2
- 数据加密: AES-256
- API安全: Rate limiting

### 性能目标
- 响应时间: <200ms
- 并发: 1000 req/s
- 可用性: 99.9%
```

---

### Phase 3: Sprint规划 (Tech Lead)
**调用技能**: `m-03-cognitive-architect`

**职责**:
- 📅 任务分解
- ⏱️ 工作量估算
- 🔗 依赖分析
- 🎯 里程碑规划
- ⚠️ 风险识别

**输出**:
```markdown
## Sprint计划
### 任务分解
#### Epic 1: 用户认证
- Task 1.1: 数据库表设计 (2h)
- Task 1.2: 后端API开发 (4h)
- Task 1.3: 前端页面 (3h)
- Task 1.4: 单元测试 (2h)

### 依赖关系
Task 1.1 → Task 1.2 → Task 1.3

### 风险
- ⚠️ 第三方OAuth可能不稳定
- 🔴 数据库迁移需要停机时间

### 时间线
- Week 1: 核心功能
- Week 2: 集成测试
- Week 3: 上线准备
```

---

### Phase 4: 开发实现 (Developer)
**调用技能**: `b-08-intelligent-refactor`

**职责**:
- 💻 编码实现
- 🧪 单元测试
- 📝 代码文档
- 🎨 代码规范
- ♻️ 重构优化

**输出**:
```markdown
## 实现代码
### 文件清单
- src/auth/login.ts
- src/auth/register.ts
- src/models/User.ts
- tests/auth.test.ts

### 测试覆盖率
85% (目标: ≥80%)

### 代码质量
- 无lint错误
- 通过静态分析
- 遵循团队规范
```

---

### Phase 5: 代码审查 (Code Reviewer)
**调用技能**: MindSymphony内置代码审查能力 或 `superpowers:code-reviewer`（如果可用）

**职责**:
- 🔍 代码质量检查
- 🛡️ 安全漏洞扫描
- 📐 架构一致性
- 📚 文档完整性
- ✨ 最佳实践验证

**输出**:
```markdown
## 代码审查报告
### 总体评分: 8.5/10

### 优点
✅ 代码结构清晰
✅ 测试覆盖充分
✅ 文档完善

### 改进建议
📝 建议1: 添加错误处理
📝 建议2: 优化数据库查询
📝 建议3: 补充边界条件测试

### 安全检查
✅ 无SQL注入风险
✅ 无XSS漏洞
⚠️ 建议添加rate limiting

### 批准状态
✅ APPROVED (需minor修改)
```

---

### Phase 6: 测试验证 (QA Engineer)
**调用技能**: `testing-strategy-planner`

**职责**:
- 🧪 测试策略制定
- ✅ 功能测试
- 🔄 集成测试
- 🚀 性能测试
- 📊 质量报告

**输出**:
```markdown
## 测试报告
### 测试覆盖
- 单元测试: 85% ✅
- 集成测试: 75% ✅
- E2E测试: 60% ⚠️

### 测试结果
| 测试类型 | 通过 | 失败 | 跳过 |
|---------|------|------|------|
| 单元测试 | 120  | 0    | 2    |
| 集成测试 | 35   | 1    | 0    |
| E2E测试  | 15   | 0    | 5    |

### 发现的问题
🐛 Bug #1: 邮箱验证逻辑错误 (P1)
🐛 Bug #2: 响应时间超标 (P2)

### 质量评估
✅ 可以上线 (修复P1 Bug后)
```

---

## 🎯 完整工作流示例

### 输入
```bash
/bmad "添加用户登录功能，支持邮箱和手机号登录"
```

### 输出（完整交付物）

```markdown
# 用户登录功能 - 完整交付包

## 📋 1. 需求文档 (Product Owner)
### 用户故事
作为用户，我想要通过邮箱或手机号登录，以便安全访问我的账户。

### 验收标准
- ✅ 支持邮箱登录
- ✅ 支持手机号登录
- ✅ 密码强度验证
- ✅ 错误提示友好
- ✅ 支持"记住我"功能

---

## 🏗️ 2. 架构设计 (Architect)
### 系统组件
```
┌─────────┐      ┌─────────┐      ┌──────────┐
│ 前端UI  │ ───→ │ API网关 │ ───→ │ 认证服务 │
└─────────┘      └─────────┘      └──────────┘
                                        │
                                        ↓
                                   ┌─────────┐
                                   │ 数据库  │
                                   └─────────┘
```

### 技术选型
- 前端: React + TypeScript
- 后端: Node.js + Express
- 数据库: PostgreSQL
- 认证: JWT + bcrypt

---

## 📅 3. Sprint计划 (Tech Lead)
### 任务列表
- [x] Task 1: 数据库表设计 (2h) - Day 1
- [x] Task 2: 后端API开发 (4h) - Day 1-2
- [x] Task 3: 前端登录页面 (3h) - Day 2
- [x] Task 4: 单元测试 (2h) - Day 3
- [x] Task 5: 集成测试 (2h) - Day 3
- [ ] Task 6: 部署上线 (1h) - Day 4

### 总工作量: 14小时 / 4天

---

## 💻 4. 实现代码 (Developer)
### 核心代码
```typescript
// src/auth/login.ts
export async function login(
  identifier: string,  // email or phone
  password: string
): Promise<AuthToken> {
  // 1. 验证输入
  validateIdentifier(identifier);
  validatePassword(password);

  // 2. 查询用户
  const user = await findUserByIdentifier(identifier);
  if (!user) {
    throw new Error('用户不存在');
  }

  // 3. 验证密码
  const isValid = await bcrypt.compare(password, user.passwordHash);
  if (!isValid) {
    throw new Error('密码错误');
  }

  // 4. 生成JWT
  const token = jwt.sign(
    { userId: user.id },
    process.env.JWT_SECRET,
    { expiresIn: '7d' }
  );

  return { token, user };
}
```

### 测试代码
```typescript
// tests/auth.test.ts
describe('Login', () => {
  it('should login with email', async () => {
    const result = await login('user@example.com', 'password123');
    expect(result.token).toBeDefined();
  });

  it('should login with phone', async () => {
    const result = await login('+86-13812345678', 'password123');
    expect(result.token).toBeDefined();
  });

  it('should reject invalid password', async () => {
    await expect(
      login('user@example.com', 'wrong')
    ).rejects.toThrow('密码错误');
  });
});
```

---

## 🔍 5. 代码审查报告 (Code Reviewer)
### 总体评分: 9/10 ⭐

### 优点
✅ 代码结构清晰，职责分明
✅ 错误处理完善
✅ 测试覆盖率85%
✅ TypeScript类型安全

### 改进建议
📝 建议添加rate limiting防止暴力破解
📝 建议记录登录失败日志

### 安全检查
✅ 密码使用bcrypt加密
✅ JWT签名安全
⚠️ 建议添加双因素认证（未来版本）

### 批准状态: ✅ APPROVED

---

## 🧪 6. 测试报告 (QA Engineer)
### 测试结果
- 单元测试: 15/15 通过 ✅
- 集成测试: 8/8 通过 ✅
- E2E测试: 5/5 通过 ✅

### 性能测试
- 登录响应时间: 45ms (目标: <200ms) ✅
- 并发支持: 500 req/s ✅

### 质量评估
✅ 所有测试通过
✅ 性能符合预期
✅ **可以上线！**

---

## 🚀 7. 部署清单
- [ ] 数据库迁移
- [ ] 环境变量配置
- [ ] 负载均衡配置
- [ ] 监控告警设置
- [ ] 备份策略确认

---

## 📊 8. 项目总结
- **开发时间**: 4天
- **代码质量**: 9/10
- **测试覆盖**: 85%
- **性能评分**: A+
- **安全评分**: A

✅ **项目完成，可以部署！**
```

---

## 🔧 高级用法

### 1. 自定义工作流

你可以通过提示词调整工作流重点：

```bash
/bmad "重构支付模块 - 重点关注安全性和性能"
```

```bash
/bmad "快速原型 - 跳过完整测试，快速验证想法"
```

### 2. 与其他技能协作

BMAD可以无缝集成其他MindSymphony技能：

```bash
/bmad "添加数据分析仪表板"
# 自动调用: frontend-design, database-schema-architect, 等
```

### 3. 迭代开发

```bash
/bmad "基于上次审查意见，修复安全问题"
```

---

## 🎯 与myclaude的对比

| 特性 | myclaude BMAD | MindSymphony BMAD Pilot |
|------|---------------|------------------------|
| 角色数量 | 6个固定代理 | 6个动态技能（可扩展到90+） |
| 工作流 | 固定流程 | 灵活编排 |
| 测试覆盖 | 强制90% | 建议80%（灵活） |
| 多模态 | 基础 | Gemini CLI深度集成 |
| 技能生态 | ~10个 | 90+个 |
| 后端支持 | Codex/Claude/Gemini | Claude主导 |

**MindSymphony BMAD Pilot的优势**:
- ✅ 更灵活的技能编排
- ✅ 更丰富的技能生态
- ✅ 保留MindSymphony的核心优势
- ✅ 零架构改造，即插即用

---

## 🚦 质量标准

### 代码质量
- ✅ 无lint错误
- ✅ 通过静态分析
- ✅ 遵循团队规范
- ⚠️ 测试覆盖 ≥ 80%（建议，不强制）

### 安全标准
- ✅ 无已知漏洞
- ✅ 输入验证
- ✅ 敏感数据加密
- ✅ 安全依赖版本

### 性能标准
- ✅ 响应时间达标
- ✅ 内存使用合理
- ✅ 并发支持符合预期

---

## 📚 最佳实践

### 1. 清晰的需求描述
```bash
✅ 好: /bmad "添加用户登录功能，支持邮箱和手机号，要求双因素认证"
❌ 差: /bmad "做个登录"
```

### 2. 渐进式开发
```bash
# Sprint 1: 核心功能
/bmad "实现基础登录功能"

# Sprint 2: 增强功能
/bmad "添加OAuth第三方登录"

# Sprint 3: 安全加固
/bmad "实施双因素认证和安全审计"
```

### 3. 充分利用技能生态
```bash
/bmad "创建设计系统"
# 自动调用: brand-guidelines, theme-factory, canvas-design
```

---

## 🔗 相关技能

BMAD Pilot会自动调用这些技能：
- `c-06-knowledge-explorer` - 需求研究
- `b-07-codebase-ecologist` - 架构分析
- `m-03-cognitive-architect` - 任务分解
- `b-08-intelligent-refactor` - 代码重构
- `testing-strategy-planner` - 测试策略

可选扩展技能：
- `frontend-design` - UI/UX设计
- `database-schema-architect` - 数据库设计
- `devops-workflow-designer` - CI/CD配置
- `api-integration-designer` - API设计

---

## 🎓 教程：第一次使用BMAD

### Step 1: 准备需求
明确你要开发什么功能，包括：
- 功能描述
- 目标用户
- 期望结果

### Step 2: 调用BMAD
```bash
/bmad "你的需求描述"
```

### Step 3: 审查输出
BMAD会生成完整的交付包，包括：
- 需求文档
- 架构设计
- Sprint计划
- 实现代码
- 审查报告
- 测试结果

### Step 4: 迭代优化
根据输出结果，进行调整和优化：
```bash
/bmad "基于上次设计，优化性能"
```

---

## 🐛 故障排除

### Q: BMAD执行时间很长？
A: 这是正常的！BMAD需要编排6个技能，完整的企业级工作流需要时间。通常5-15分钟。

### Q: 可以跳过某些阶段吗？
A: 可以！在提示词中指定：
```bash
/bmad "快速实现登录功能 - 跳过详细架构设计"
```

### Q: 如何自定义工作流？
A: 直接在需求中说明：
```bash
/bmad "重点关注安全性的支付模块重构"
```

---

## 📈 版本历史

### v1.0.0 (2026-01-12)
- ✅ 初始发布
- ✅ 支持6个标准角色
- ✅ 完整的企业级工作流
- ✅ 灵活的技能编排

---

## 📄 许可证

MIT License - 自由使用和修改

---

## 🙏 致谢

灵感来自[myclaude](https://github.com/emsi/myclaude)的BMAD模式，但充分利用MindSymphony的技能生态，提供更灵活、更强大的工作流编排能力。

---

## 🎯 快速参考

```bash
# 基础用法
/bmad "需求描述"

# 重点开发
/bmad "功能 - 重点关注性能"

# 快速原型
/bmad "快速验证想法 - 跳过完整测试"

# 安全优先
/bmad "功能 - 最高安全标准"

# 迭代优化
/bmad "基于上次反馈优化"
```

---

**开始你的第一个BMAD工作流吧！** 🚀
