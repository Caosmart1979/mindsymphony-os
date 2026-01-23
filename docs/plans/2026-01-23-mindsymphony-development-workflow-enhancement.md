# MindSymphony 技能体系开发工作流程增强计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task.

**Goal:** 增强 MindSymphony 技能体系在开发工作流程支持方面的功能，借鉴 everything-claude-code 的专业化和实用性特点。

**Architecture:** 通过补充专门的开发代理、完善编程技能、优化命令系统和钩子系统，使 MindSymphony 既保持全面性又具备强大的开发工作流程支持能力。

**Tech Stack:** 技能体系架构、Markdown 文档、YAML 配置、Node.js 脚本

---

## 1. 补充专门的开发代理

### Task 1: 创建代码审查代理
**Files:**
- Create: `C:\Users\13466\.claude\mindsymphony-v21\extensions\coding\code-reviewer\SKILL.md`

**Step 1: 编写技能文档**
```markdown
---
name: code-reviewer
description: 使用此技能进行代码质量和安全审查。提供详细的审查检查清单和模式识别。
---

# 代码审查代理

此技能确保所有代码遵循最佳实践，并识别潜在的质量和安全问题。

## 使用时机

- 完成功能开发后
- 创建 PR 前
- 重构代码后
- 审查关键业务逻辑时

## 代码审查检查清单

### 1. 代码质量

#### 可读性
- [ ] 变量和函数命名清晰易懂
- [ ] 代码注释恰当
- [ ] 函数长度适中（不超过 50 行）
- [ ] 代码结构清晰，逻辑分明

#### 可维护性
- [ ] 避免重复代码
- [ ] 使用适当的数据结构
- [ ] 错误处理完善
- [ ] 单元测试覆盖重要功能

### 2. 安全审查

#### 输入验证
- [ ] 所有用户输入都经过验证
- [ ] 使用参数化查询防止 SQL 注入
- [ ] 避免 eval() 等危险函数
- [ ] 文件上传验证（大小、类型、扩展名）

#### 认证与授权
- [ ] 敏感操作需要适当的权限检查
- [ ] JWT 令牌存储在 HttpOnly cookies 中
- [ ] 会话管理安全
- [ ] 密码哈希存储

### 3. 性能优化

#### 代码优化
- [ ] 避免不必要的计算
- [ ] 适当使用缓存
- [ ] 减少网络请求
- [ ] 优化数据库查询

## 代码审查步骤

### 1. 初始检查
- 查看变更文件列表
- 了解功能实现
- 识别潜在风险区域

### 2. 详细审查
- 逐行审查代码
- 检查安全漏洞
- 评估代码质量
- 验证测试覆盖

### 3. 反馈与改进
- 提出改进建议
- 标记需要修复的问题
- 验证修复方案

## 输出格式

```markdown
# 代码审查报告

## 变更文件
- [ ] file1.js
- [ ] file2.ts
- [ ] file3.py

## 问题识别

### 高优先级
1. [ ] SQL 注入风险 - file1.js:123
2. [ ] 未验证的用户输入 - file2.ts:45

### 中等优先级
1. [ ] 重复代码 - file1.js:67-89
2. [ ] 函数过长 - file3.py:10-50

### 低优先级
1. [ ] 变量命名不清晰 - file2.ts:78
2. [ ] 缺少代码注释 - file3.py:34

## 建议改进

1. 使用参数化查询代替字符串拼接
2. 添加输入验证逻辑
3. 重构重复代码
4. 拆分过长的函数

## 结论

代码质量：[良好/中等/需要改进]
安全风险：[低/中/高]
建议：[批准/需要改进后重新审查/拒绝]
```
```

**Step 2: 保存技能文档**
Run: `mkdir -p "C:\Users\13466\.claude\mindsymphony-v21\extensions\coding\code-reviewer" && cat > "C:\Users\13466\.claude\mindsymphony-v21\extensions\coding\code-reviewer\SKILL.md" << 'EOF'
[上述技能文档内容]
EOF`

**Step 3: 验证文件创建成功**
Run: `ls -la "C:\Users\13466\.claude\mindsymphony-v21\extensions\coding\code-reviewer"`
Expected: SKILL.md 文件存在

**Step 4: 提交到版本控制**
```bash
git add "C:\Users\13466\.claude\mindsymphony-v21\extensions\coding\code-reviewer\SKILL.md"
git commit -m "feat: add code reviewer skill"
```

---

### Task 2: 创建安全审查代理
**Files:**
- Create: `C:\Users\13466\.claude\mindsymphony-v21\extensions\coding\security-reviewer\SKILL.md`

**Step 1: 编写技能文档**
```markdown
---
name: security-reviewer
description: 使用此技能进行全面的安全审查。提供详细的安全检查清单和漏洞识别。
---

# 安全审查代理

此技能确保所有代码遵循安全最佳实践，并识别潜在的安全漏洞。

## 使用时机

- 实现认证或授权功能时
- 处理用户输入或文件上传时
- 创建新的 API 端点时
- 处理机密信息或敏感数据时
- 集成第三方 API 时

## 安全检查清单

### 1. 机密信息管理

#### ❌ 禁止做法
```typescript
const apiKey = "sk-proj-xxxxx"  // 硬编码机密
const dbPassword = "password123" // 在源代码中
```

#### ✅ 正确做法
```typescript
const apiKey = process.env.OPENAI_API_KEY
const dbUrl = process.env.DATABASE_URL

// 验证机密存在
if (!apiKey) {
  throw new Error('OPENAI_API_KEY 未配置')
}
```

#### 验证步骤
- [ ] 无硬编码 API 密钥、令牌或密码
- [ ] 所有机密在环境变量中
- [ ] `.env.local` 在 .gitignore 中
- [ ] 机密不在 git 历史中
- [ ] 生产环境机密在托管平台（Vercel、Railway）中

### 2. 输入验证

#### 验证用户输入
```typescript
import { z } from 'zod'

// 定义验证模式
const CreateUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(100),
  age: z.number().int().min(0).max(150)
})

// 处理前验证
export async function createUser(input: unknown) {
  try {
    const validated = CreateUserSchema.parse(input)
    return await db.users.create(validated)
  } catch (error) {
    if (error instanceof z.ZodError) {
      return { success: false, errors: error.errors }
    }
    throw error
  }
}
```

#### 文件上传验证
```typescript
function validateFileUpload(file: File) {
  // 大小检查（最大 5MB）
  const maxSize = 5 * 1024 * 1024
  if (file.size > maxSize) {
    throw new Error('文件太大（最大 5MB）')
  }

  // 类型检查
  const allowedTypes = ['image/jpeg', 'image/png', 'image/gif']
  if (!allowedTypes.includes(file.type)) {
    throw new Error('无效的文件类型')
  }

  // 扩展名检查
  const allowedExtensions = ['.jpg', '.jpeg', '.png', '.gif']
  const extension = file.name.toLowerCase().match(/\.[^.]+$/)?.[0]
  if (!extension || !allowedExtensions.includes(extension)) {
    throw new Error('无效的文件扩展名')
  }

  return true
}
```

#### 验证步骤
- [ ] 所有用户输入通过模式验证
- [ ] 文件上传受限制（大小、类型、扩展名）
- [ ] 不在查询中直接使用用户输入
- [ ] 使用白名单验证（而非黑名单）
- [ ] 错误消息不泄露敏感信息

### 3. SQL 注入预防

#### ❌ 禁止拼接 SQL
```typescript
// 危险 - SQL 注入漏洞
const query = `SELECT * FROM users WHERE email = '${userEmail}'`
await db.query(query)
```

#### ✅ 正确使用参数化查询
```typescript
// 安全 - 参数化查询
const { data } = await supabase
  .from('users')
  .select('*')
  .eq('email', userEmail)

// 或使用原始 SQL
await db.query(
  'SELECT * FROM users WHERE email = $1',
  [userEmail]
)
```

#### 验证步骤
- [ ] 所有数据库查询使用参数化查询
- [ ] SQL 中无字符串拼接
- [ ] ORM/查询构建器正确使用
- [ ] Supabase 查询适当净化

### 4. 认证与授权

#### JWT 令牌处理
```typescript
// ❌ 错误：localStorage（易受 XSS 攻击）
localStorage.setItem('token', token)

// ✅ 正确：httpOnly cookies
res.setHeader('Set-Cookie',
  `token=${token}; HttpOnly; Secure; SameSite=Strict; Max-Age=3600`)
```

#### 授权检查
```typescript
export async function deleteUser(userId: string, requesterId: string) {
  // 始终首先验证授权
  const requester = await db.users.findUnique({
    where: { id: requesterId }
  })

  if (requester.role !== 'admin') {
    return NextResponse.json(
      { error: '未授权' },
      { status: 403 }
    )
  }

  // 继续删除操作
  await db.users.delete({ where: { id: userId } })
}
```

#### 验证步骤
- [ ] 令牌存储在 httpOnly cookies 中（而非 localStorage）
- [ ] 敏感操作前有授权检查
- [ ] 角色基于访问控制实现
- [ ] 会话管理安全

## 安全测试

### 自动化安全测试
```typescript
// 测试认证
test('需要认证', async () => {
  const response = await fetch('/api/protected')
  expect(response.status).toBe(401)
})

// 测试授权
test('需要管理员角色', async () => {
  const response = await fetch('/api/admin', {
    headers: { Authorization: `Bearer ${userToken}` }
  })
  expect(response.status).toBe(403)
})

// 测试输入验证
test('拒绝无效输入', async () => {
  const response = await fetch('/api/users', {
    method: 'POST',
    body: JSON.stringify({ email: 'not-an-email' })
  })
  expect(response.status).toBe(400)
})

// 测试速率限制
test('执行速率限制', async () => {
  const requests = Array(101).fill(null).map(() =>
    fetch('/api/endpoint')
  )

  const responses = await Promise.all(requests)
  const tooManyRequests = responses.filter(r => r.status === 429)

  expect(tooManyRequests.length).toBeGreaterThan(0)
})
```

## 部署前安全检查清单

在任何生产部署前：

- [ ] **机密信息**：无硬编码机密，全部在环境变量中
- [ ] **输入验证**：所有用户输入已验证
- [ ] **SQL 注入**：所有查询参数化
- [ ] **XSS**：用户内容已净化
- [ ] **CSRF**：保护已启用
- [ ] **认证**：正确的令牌处理
- [ ] **授权**：角色检查已到位
- [ ] **速率限制**：所有端点已启用
- [ ] **HTTPS**：生产环境强制使用
- [ ] **安全头**：CSP、X-Frame-Options 已配置
- [ ] **错误处理**：错误中无敏感数据
- [ ] **日志记录**：日志中无敏感数据
- [ ] **依赖项**：最新，无漏洞
- [ ] **CORS**：正确配置
- [ ] **文件上传**：已验证（大小、类型）

## 资源

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Next.js Security](https://nextjs.org/docs/security)
- [Supabase Security](https://supabase.com/docs/guides/auth)
- [Web Security Academy](https://portswigger.net/web-security)
```

**Step 2: 保存技能文档**
Run: `mkdir -p "C:\Users\13466\.claude\mindsymphony-v21\extensions\coding\security-reviewer" && cat > "C:\Users\13466\.claude\mindsymphony-v21\extensions\coding\security-reviewer\SKILL.md" << 'EOF'
[上述技能文档内容]
EOF`

**Step 3: 验证文件创建成功**
Run: `ls -la "C:\Users\13466\.claude\mindsymphony-v21\extensions\coding\security-reviewer"`
Expected: SKILL.md 文件存在

**Step 4: 提交到版本控制**
```bash
git add "C:\Users\13466\.claude\mindsymphony-v21\extensions\coding\security-reviewer\SKILL.md"
git commit -m "feat: add security reviewer skill"
```

---

## 2. 完善编程技能

### Task 3: 创建 TDD 工作流程技能
**Files:**
- Create: `C:\Users\13466\.claude\mindsymphony-v21\extensions\coding\tdd-workflow\SKILL.md`

**Step 1: 编写技能文档**
```markdown
---
name: tdd-workflow
description: 使用此技能进行测试驱动开发。强制执行测试先行、全面覆盖的开发流程。
---

# 测试驱动开发工作流程

此技能确保所有代码开发遵循 TDD 原则，并提供全面的测试覆盖。

## 使用时机

- 编写新功能或功能
- 修复错误或问题
- 重构现有代码
- 添加 API 端点
- 创建新组件

## 核心原则

### 1. 测试先行
始终先编写测试，然后实现代码以通过测试。

### 2. 覆盖要求
- 最低 80% 覆盖率（单元 + 集成 + E2E）
- 覆盖所有边缘情况
- 测试错误场景
- 验证边界条件

### 3. 测试类型

#### 单元测试
- 单个函数和工具
- 组件逻辑
- 纯函数
- 助手和工具函数

#### 集成测试
- API 端点
- 数据库操作
- 服务交互
- 外部 API 调用

#### E2E 测试（Playwright）
- 关键用户流程
- 完整工作流程
- 浏览器自动化
- UI 交互

## TDD 工作流程步骤

### 步骤 1: 编写用户旅程
```
作为 [角色]，我想要 [动作]，以便 [好处]

示例：
作为用户，我想要语义搜索市场，
以便即使没有确切的关键词，我也能找到相关市场。
```

### 步骤 2: 生成测试用例
为每个用户旅程创建全面的测试用例：

```typescript
describe('语义搜索', () => {
  it('为查询返回相关市场', async () => {
    // 测试实现
  })

  it('优雅处理空查询', async () => {
    // 测试边缘情况
  })

  it('当 Redis 不可用时，回退到子字符串搜索', async () => {
    // 测试回退行为
  })

  it('按相似度分数排序结果', async () => {
    // 测试排序逻辑
  })
})
```

### 步骤 3: 运行测试（它们应该失败）
```bash
npm test
# 测试应该失败 - 我们还没有实现
```

### 步骤 4: 实现代码
编写最少的代码来通过测试：

```typescript
// 由测试指导的实现
export async function searchMarkets(query: string) {
  // 实现在这里
}
```

### 步骤 5: 再次运行测试
```bash
npm test
# 现在测试应该通过
```

### 步骤 6: 重构
在保持测试绿色的同时提高代码质量：
- 去除重复
- 改进命名
- 优化性能
- 增强可读性

### 步骤 7: 验证覆盖
```bash
npm run test:coverage
# 验证达到 80%+ 覆盖
```

## 测试模式

### 单元测试模式（Jest/Vitest）
```typescript
import { render, screen, fireEvent } from '@testing-library/react'
import { Button } from './Button'

describe('Button Component', () => {
  it('渲染正确的文本', () => {
    render(<Button>Click me</Button>)
    expect(screen.getByText('Click me')).toBeInTheDocument()
  })

  it('点击时调用 onClick', () => {
    const handleClick = jest.fn()
    render(<Button onClick={handleClick}>Click</Button>)

    fireEvent.click(screen.getByRole('button'))

    expect(handleClick).toHaveBeenCalledTimes(1)
  })

  it('当 disabled 属性为 true 时禁用', () => {
    render(<Button disabled>Click</Button>)
    expect(screen.getByRole('button')).toBeDisabled()
  })
})
```

### API 集成测试模式
```typescript
import { NextRequest } from 'next/server'
import { GET } from './route'

describe('GET /api/markets', () => {
  it('成功返回市场', async () => {
    const request = new NextRequest('http://localhost/api/markets')
    const response = await GET(request)
    const data = await response.json()

    expect(response.status).toBe(200)
    expect(data.success).toBe(true)
    expect(Array.isArray(data.data)).toBe(true)
  })

  it('验证查询参数', async () => {
    const request = new NextRequest('http://localhost/api/markets?limit=invalid')
    const response = await GET(request)

    expect(response.status).toBe(400)
  })

  it('优雅处理数据库错误', async () => {
    // 模拟数据库失败
    const request = new NextRequest('http://localhost/api/markets')
    // 测试错误处理
  })
})
```

### E2E 测试模式（Playwright）
```typescript
import { test, expect } from '@playwright/test'

test('用户可以搜索和筛选市场', async ({ page }) => {
  // 导航到市场页面
  await page.goto('/')
  await page.click('a[href="/markets"]')

  // 验证页面加载
  await expect(page.locator('h1')).toContainText('Markets')

  // 搜索市场
  await page.fill('input[placeholder="Search markets"]', 'election')

  // 等待防抖和结果
  await page.waitForTimeout(600)

  // 验证搜索结果显示
  const results = page.locator('[data-testid="market-card"]')
  await expect(results).toHaveCount(5, { timeout: 5000 })

  // 验证结果包含搜索词
  const firstResult = results.first()
  await expect(firstResult).toContainText('election', { ignoreCase: true })

  // 按状态筛选
  await page.click('button:has-text("Active")')

  // 验证筛选结果
  await expect(results).toHaveCount(3)
})

test('用户可以创建新市场', async ({ page }) => {
  // 首先登录
  await page.goto('/creator-dashboard')

  // 填写市场创建表单
  await page.fill('input[name="name"]', 'Test Market')
  await page.fill('textarea[name="description"]', 'Test description')
  await page.fill('input[name="endDate"]', '2025-12-31')

  // 提交表单
  await page.click('button[type="submit"]')

  // 验证成功消息
  await expect(page.locator('text=Market created successfully')).toBeVisible()

  // 验证重定向到市场页面
  await expect(page).toHaveURL(/\/markets\/test-market/)
})
```

## 测试文件组织

```
src/
├── components/
│   ├── Button/
│   │   ├── Button.tsx
│   │   ├── Button.test.tsx          # 单元测试
│   │   └── Button.stories.tsx       # Storybook
│   └── MarketCard/
│       ├── MarketCard.tsx
│       └── MarketCard.test.tsx
├── app/
│   └── api/
│       └── markets/
│           ├── route.ts
│           └── route.test.ts         # 集成测试
└── e2e/
    ├── markets.spec.ts               # E2E 测试
    ├── trading.spec.ts
    └── auth.spec.ts
```

## 模拟外部服务

### Supabase 模拟
```typescript
jest.mock('@/lib/supabase', () => ({
  supabase: {
    from: jest.fn(() => ({
      select: jest.fn(() => ({
        eq: jest.fn(() => Promise.resolve({
          data: [{ id: 1, name: 'Test Market' }],
          error: null
        }))
      }))
    }))
  }
}))
```

### Redis 模拟
```typescript
jest.mock('@/lib/redis', () => ({
  searchMarketsByVector: jest.fn(() => Promise.resolve([
    { slug: 'test-market', similarity_score: 0.95 }
  ])),
  checkRedisHealth: jest.fn(() => Promise.resolve({ connected: true }))
}))
```

### OpenAI 模拟
```typescript
jest.mock('@/lib/openai', () => ({
  generateEmbedding: jest.fn(() => Promise.resolve(
    new Array(1536).fill(0.1) // 模拟 1536 维嵌入
  ))
}))
```

## 测试覆盖验证

### 运行覆盖报告
```bash
npm run test:coverage
```

### 覆盖阈值
```json
{
  "jest": {
    "coverageThresholds": {
      "global": {
        "branches": 80,
        "functions": 80,
        "lines": 80,
        "statements": 80
      }
    }
  }
}
```

## 常见测试错误

### ❌ 错误：测试实现细节
```typescript
// 不测试内部状态
expect(component.state.count).toBe(5)
```

### ✅ 正确：测试用户可见行为
```typescript
// 测试用户看到的内容
expect(screen.getByText('Count: 5')).toBeInTheDocument()
```

### ❌ 错误：脆弱的选择器
```typescript
// 容易断裂
await page.click('.css-class-xyz')
```

### ✅ 正确：语义选择器
```typescript
// 对变化有弹性
await page.click('button:has-text("Submit")')
await page.click('[data-testid="submit-button"]')
```

## 持续测试

### 开发期间的监视模式
```bash
npm test -- --watch
# 文件更改时自动运行测试
```

### 预提交钩子
```bash
# 在每次提交前运行
npm test && npm run lint
```

### CI/CD 集成
```yaml
# GitHub Actions
- name: 运行测试
  run: npm test -- --coverage
- name: 上传覆盖报告
  uses: codecov/codecov-action@v3
```

## 最佳实践

1. **测试先行** - 始终 TDD
2. **每个测试一个断言** - 专注于单一行为
3. **描述性测试名称** - 解释测试内容
4. **Arrange-Act-Assert** - 清晰的测试结构
5. **模拟外部依赖** - 隔离单元测试
6. **测试边缘情况** - null、undefined、空、大值
7. **测试错误路径** - 不只是快乐路径
8. **保持测试快速** - 单元测试 < 50ms 每个
9. **测试后清理** - 无副作用
10. **查看覆盖报告** - 识别差距

## 成功指标

- 实现 80%+ 代码覆盖率
- 所有测试通过（绿色）
- 无跳过或禁用的测试
- 快速测试执行（单元测试 < 30 秒）
- E2E 测试覆盖关键用户流程
- 测试在生产前捕获错误
```

**Step 2: 保存技能文档**
Run: `mkdir -p "C:\Users\13466\.claude\mindsymphony-v21\extensions\coding\tdd-workflow" && cat > "C:\Users\13466\.claude\mindsymphony-v21\extensions\coding\tdd-workflow\SKILL.md" << 'EOF'
[上述技能文档内容]
EOF`

**Step 3: 验证文件创建成功**
Run: `ls -la "C:\Users\13466\.claude\mindsymphony-v21\extensions\coding\tdd-workflow"`
Expected: SKILL.md 文件存在

**Step 4: 提交到版本控制**
```bash
git add "C:\Users\13466\.claude\mindsymphony-v21\extensions\coding\tdd-workflow\SKILL.md"
git commit -m "feat: add TDD workflow skill"
```

---

### Task 4: 创建验证循环技能
**Files:**
- Create: `C:\Users\13466\.claude\mindsymphony-v21\extensions\coding\verification-loop\SKILL.md`

**Step 1: 编写技能文档**
```markdown
---
name: verification-loop
description: 使用此技能进行全面的验证。确保代码质量、安全和功能符合要求。
---

# 验证循环技能

Claude Code 会话的全面验证系统。

## 使用时机

- 完成功能或重大代码变更后
- 创建 PR 前
- 想要确保质量门通过时
- 重构后

## 验证阶段

### 阶段 1: 构建验证
```bash
# 检查项目是否构建
npm run build 2>&1 | tail -20
# OR
pnpm build 2>&1 | tail -20
```

如果构建失败，停止并修复后继续。

### 阶段 2: 类型检查
```bash
# TypeScript 项目
npx tsc --noEmit 2>&1 | head -30

# Python 项目
pyright . 2>&1 | head -30
```

报告所有类型错误。修复关键错误后继续。

### 阶段 3: Lint 检查
```bash
# JavaScript/TypeScript
npm run lint 2>&1 | head -30

# Python
ruff check . 2>&1 | head -30
```

### 阶段 4: 测试套件
```bash
# 运行带有覆盖的测试
npm run test -- --coverage 2>&1 | tail -50

# 检查覆盖阈值
# 目标：最低 80%
```

报告：
- 总测试数：X
- 通过：X
- 失败：X
- 覆盖：X%

### 阶段 5: 安全扫描
```bash
# 检查机密信息
grep -rn "sk-" --include="*.ts" --include="*.js" . 2>/dev/null | head -10
grep -rn "api_key" --include="*.ts" --include="*.js" . 2>/dev/null | head -10

# 检查 console.log
grep -rn "console.log" --include="*.ts" --include="*.tsx" src/ 2>/dev/null | head -10
```

### 阶段 6: 差异审查
```bash
# 显示变更内容
git diff --stat
git diff HEAD~1 --name-only
```

审查每个变更文件：
- 意外变更
- 缺少错误处理
- 潜在边缘情况

## 输出格式

运行所有阶段后，生成验证报告：

```
验证报告
==================

构建:     [PASS/FAIL]
类型:     [PASS/FAIL] (X 错误)
Lint:      [PASS/FAIL] (X 警告)
测试:     [PASS/FAIL] (X/Y 通过, Z% 覆盖)
安全:  [PASS/FAIL] (X 问题)
差异:      [X 文件变更]

总体:   [准备好/未准备好] 用于 PR

需要修复的问题:
1. ...
2. ...
```

## 持续模式

对于长时间会话，每 15 分钟或重大变更后运行验证：

```markdown
设置心理检查点：
- 完成每个函数后
- 完成组件后
- 移动到下一个任务前

运行: /verify
```

## 与钩子集成

此技能补充了 PostToolUse 钩子，但提供更深入的验证。
钩子立即捕获问题；此技能提供全面审查。
```

**Step 2: 保存技能文档**
Run: `mkdir -p "C:\Users\13466\.claude\mindsymphony-v21\extensions\coding\verification-loop" && cat > "C:\Users\13466\.claude\mindsymphony-v21\extensions\coding\verification-loop\SKILL.md" << 'EOF'
[上述技能文档内容]
EOF`

**Step 3: 验证文件创建成功**
Run: `ls -la "C:\Users\13466\.claude\mindsymphony-v21\extensions\coding\verification-loop"`
Expected: SKILL.md 文件存在

**Step 4: 提交到版本控制**
```bash
git add "C:\Users\13466\.claude\mindsymphony-v21\extensions\coding\verification-loop\SKILL.md"
git commit -m "feat: add verification loop skill"
```

---

## 3. 优化命令系统

### Task 5: 创建开发相关命令
**Files:**
- Modify: `C:\Users\13466\.claude\mindsymphony-v21\commands\commands.yml`

**Step 1: 查看当前命令配置**
Run: `cat "C:\Users\13466\.claude\mindsymphony-v21\commands\commands.yml"`

**Step 2: 添加开发相关命令**
```yaml
- name: tdd
  description: 执行测试驱动开发工作流程。先编写测试，然后实现代码，确保 80%+ 覆盖。
  prompt: 使用 tdd-workflow 技能执行测试驱动开发。

- name: code-review
  description: 执行代码质量和安全审查。提供详细的审查检查清单和模式识别。
  prompt: 使用 code-reviewer 技能进行代码质量和安全审查。

- name: security-review
  description: 执行全面的安全审查。提供详细的安全检查清单和漏洞识别。
  prompt: 使用 security-reviewer 技能进行全面的安全审查。

- name: verify
  description: 运行全面的验证循环。检查构建、类型、lint、测试、安全和差异。
  prompt: 使用 verification-loop 技能运行全面的验证。

- name: build-fix
  description: 修复构建错误。分析构建失败并提供解决方案。
  prompt: 分析构建错误并提供解决方案。

- name: refactor-clean
  description: 清理死代码和重构。识别并移除未使用的代码。
  prompt: 识别并移除未使用的代码，优化代码结构。

- name: test-coverage
  description: 检查测试覆盖率。确保达到 80%+ 覆盖。
  prompt: 检查测试覆盖率，确保达到 80%+ 覆盖。
```

**Step 3: 合并到现有配置**
Run: `cat "C:\Users\13466\.claude\mindsymphony-v21\commands\commands.yml" | head -20 && echo -e "[上述新增命令内容]" >> "C:\Users\13466\.claude\mindsymphony-v21\commands\commands.yml"`

**Step 4: 验证配置更新成功**
Run: `cat "C:\Users\13466\.claude\mindsymphony-v21\commands\commands.yml"`
Expected: 新增命令已添加到配置中

**Step 5: 提交到版本控制**
```bash
git add "C:\Users\13466\.claude\mindsymphony-v21\commands\commands.yml"
git commit -m "feat: add development-related commands"
```

---

## 4. 提升钩子系统功能

### Task 6: 增强钩子系统
**Files:**
- Create: `C:\Users\13466\.claude\mindsymphony-v21\hooks\session-evaluation.js`
- Create: `C:\Users\13466\.claude\mindsymphony-v21\hooks\pattern-extraction.js`

**Step 1: 创建会话评估钩子**
```javascript
// session-evaluation.js
const fs = require('fs');
const path = require('path');

// 评估会话质量和性能
function evaluateSession(sessionData) {
  console.log('Evaluating session...');

  // 检查会话长度
  const duration = sessionData.endTime - sessionData.startTime;
  console.log(`Session duration: ${Math.round(duration / 1000)} seconds`);

  // 检查使用的技能
  const skillsUsed = new Set(sessionData.messages.map(m => m.skill));
  console.log(`Skills used: ${Array.from(skillsUsed).join(', ')}`);

  // 检查任务完成情况
  const completedTasks = sessionData.messages.filter(m =>
    m.content.includes('✅') || m.content.includes('完成')
  ).length;
  console.log(`Completed tasks: ${completedTasks}`);

  // 检查错误和警告
  const errors = sessionData.messages.filter(m =>
    m.content.includes('❌') || m.content.includes('错误')
  ).length;
  const warnings = sessionData.messages.filter(m =>
    m.content.includes('⚠️') || m.content.includes('警告')
  ).length;
  console.log(`Errors: ${errors}, Warnings: ${warnings}`);

  // 保存评估报告
  const report = {
    duration,
    skillsUsed: Array.from(skillsUsed),
    completedTasks,
    errors,
    warnings,
    timestamp: new Date().toISOString()
  };

  const reportPath = path.join(__dirname, 'session-reports');
  if (!fs.existsSync(reportPath)) {
    fs.mkdirSync(reportPath, { recursive: true });
  }

  const reportFile = path.join(reportPath, `session-${sessionData.id}-evaluation.json`);
  fs.writeFileSync(reportFile, JSON.stringify(report, null, 2));

  console.log('Session evaluation complete');
}

// 导出函数
module.exports = { evaluateSession };
```

**Step 2: 创建模式提取钩子**
```javascript
// pattern-extraction.js
const fs = require('fs');
const path = require('path');

// 从会话中提取模式
function extractPatterns(sessionData) {
  console.log('Extracting patterns from session...');

  const patterns = {};

  // 提取代码模式
  const codePatterns = [];
  sessionData.messages.forEach(msg => {
    if (msg.content.includes('```')) {
      // 提取代码块
      const codeBlocks = msg.content.match(/```[\s\S]*?```/g) || [];
      codeBlocks.forEach(block => {
        // 去除语言标记
        const code = block.replace(/```[a-z]*\n?/, '').replace(/```$/, '').trim();
        if (code.length > 50) {  // 只提取有意义的代码块
          codePatterns.push({
            type: 'code',
            length: code.length,
            content: code.substring(0, 200) + (code.length > 200 ? '...' : '')
          });
        }
      });
    }
  });
  patterns.code = codePatterns;

  // 提取任务模式
  const taskPatterns = [];
  sessionData.messages.forEach(msg => {
    if (msg.content.includes('任务') || msg.content.includes('Task')) {
      const taskMatches = msg.content.match(/任务\s*\d+:\s*[^\n]+/g) || [];
      taskMatches.forEach(task => {
        taskPatterns.push({
          type: 'task',
          content: task.trim()
        });
      });
    }
  });
  patterns.tasks = taskPatterns;

  // 提取问题模式
  const problemPatterns = [];
  sessionData.messages.forEach(msg => {
    if (msg.content.includes('问题') || msg.content.includes('错误')) {
      const problemMatches = msg.content.match(/问题\s*\d+:\s*[^\n]+/g) || [];
      problemMatches.forEach(problem => {
        problemPatterns.push({
          type: 'problem',
          content: problem.trim()
        });
      });
    }
  });
  patterns.problems = problemPatterns;

  // 保存模式报告
  const reportPath = path.join(__dirname, 'pattern-reports');
  if (!fs.existsSync(reportPath)) {
    fs.mkdirSync(reportPath, { recursive: true });
  }

  const reportFile = path.join(reportPath, `session-${sessionData.id}-patterns.json`);
  fs.writeFileSync(reportFile, JSON.stringify(patterns, null, 2));

  console.log(`Pattern extraction complete: ${codePatterns.length} code blocks, ${taskPatterns.length} tasks, ${problemPatterns.length} problems`);
}

// 导出函数
module.exports = { extractPatterns };
```

**Step 3: 更新钩子配置**
Run: `cat "C:\Users\13466\.claude\mindsymphony-v21\hooks\hooks.yml" | head -20 && echo -e "
- name: session-evaluation
  description: 会话结束时评估会话质量和性能
  type: session-end
  script: session-evaluation.js

- name: pattern-extraction
  description: 会话结束时从会话中提取模式
  type: session-end
  script: pattern-extraction.js
" >> "C:\Users\13466\.claude\mindsymphony-v21\hooks\hooks.yml"`

**Step 4: 验证钩子配置更新成功**
Run: `cat "C:\Users\13466\.claude\mindsymphony-v21\hooks\hooks.yml"`
Expected: 新增钩子已添加到配置中

**Step 5: 提交到版本控制**
```bash
git add "C:\Users\13466\.claude\mindsymphony-v21\hooks\session-evaluation.js" "C:\Users\13466\.claude\mindsymphony-v21\hooks\pattern-extraction.js" "C:\Users\13466\.claude\mindsymphony-v21\hooks\hooks.yml"
git commit -m "feat: enhance hooks system with session evaluation and pattern extraction"
```

---

## 5. 完善规则系统

### Task 7: 创建规则系统
**Files:**
- Create: `C:\Users\13466\.claude\mindsymphony-v21\rules\README.md`
- Create: `C:\Users\13466\.claude\mindsymphony-v21\rules\security.md`
- Create: `C:\Users\13466\.claude\mindsymphony-v21\rules\coding-style.md`
- Create: `C:\Users\13466\.claude\mindsymphony-v21\rules\testing.md`
- Create: `C:\Users\13466\.claude\mindsymphony-v21\rules\git-workflow.md`

**Step 1: 编写规则系统概述**
```markdown
# MindSymphony 规则系统

此规则系统定义了 MindSymphony 技能体系的开发规范和最佳实践。

## 规则分类

### 1. 安全规则 (security.md)
- 机密信息管理
- 输入验证
- SQL 注入预防
- 认证与授权
- XSS 预防
- CSRF 保护
- 速率限制
- 敏感数据暴露

### 2. 编码风格规则 (coding-style.md)
- 变量和函数命名
- 代码注释
- 函数长度
- 代码结构
- 错误处理
- 类型安全

### 3. 测试规则 (testing.md)
- 测试驱动开发
- 测试覆盖要求
- 测试类型
- 测试文件组织
- 模拟外部服务
- 持续测试

### 4. Git 工作流程规则 (git-workflow.md)
- 提交格式
- PR 流程
- 分支策略
- 代码审查
- 持续集成

## 使用方式

在开发过程中，应该：
1. 遵循规则系统的要求
2. 使用相关技能进行验证
3. 在 PR 前运行验证循环
4. 定期更新规则系统

## 维护

规则系统应该：
1. 定期更新以反映最佳实践
2. 根据反馈进行改进
3. 与技能体系保持同步
```

**Step 2: 创建安全规则文档**
```markdown
# 安全规则

## 1. 机密信息管理

### 禁止
- 硬编码 API 密钥、令牌或密码
- 将机密信息存储在源代码中
- 将机密信息提交到版本控制

### 要求
- 所有机密信息必须存储在环境变量中
- 使用 .env 文件管理开发环境机密
- .env 文件必须在 .gitignore 中
- 生产环境机密必须存储在托管平台中
- 在使用前验证机密信息存在

## 2. 输入验证

### 禁止
- 直接使用未验证的用户输入
- 使用黑名单验证
- 泄露敏感信息在错误消息中

### 要求
- 所有用户输入必须通过模式验证
- 使用白名单验证
- 文件上传必须验证（大小、类型、扩展名）
- 错误消息必须通用，不泄露敏感信息

## 3. SQL 注入预防

### 禁止
- 使用字符串拼接构建 SQL 查询
- 直接在 SQL 中使用用户输入

### 要求
- 所有数据库查询必须使用参数化查询
- 使用 ORM 或查询构建器
- 避免使用动态 SQL

## 4. 认证与授权

### 禁止
- 将 JWT 令牌存储在 localStorage 中
- 不验证用户权限就执行敏感操作

### 要求
- 使用 HttpOnly cookies 存储令牌
- 在执行敏感操作前验证权限
- 实现角色基于访问控制
- 确保会话管理安全

## 5. XSS 预防

### 禁止
- 直接渲染未净化的用户提供的 HTML
- 使用危险的 DOM 操作

### 要求
- 净化所有用户提供的 HTML
- 配置 CSP 头
- 使用 React 的内置 XSS 保护
- 避免使用 dangerouslySetInnerHTML 除非必要

## 6. CSRF 保护

### 要求
- 在状态改变操作上使用 CSRF 令牌
- 配置 SameSite=Strict cookies
- 实现双重提交 cookie 模式

## 7. 速率限制

### 要求
- 对所有 API 端点实施速率限制
- 对昂贵操作实施更严格的限制
- 实现基于 IP 和用户的限制

## 8. 敏感数据暴露

### 禁止
- 在日志中记录敏感信息
- 在错误消息中暴露内部细节

### 要求
- 过滤敏感信息在日志中
- 提供通用的错误消息给用户
- 在服务器日志中只记录详细错误
```

**Step 3: 创建编码风格规则文档**
```markdown
# 编码风格规则

## 1. 命名规范

### 变量命名
- 使用 camelCase 命名变量和函数
- 使用有意义的名称，避免缩写
- 布尔变量应该以 is/has/should 等前缀开头

### 示例
```typescript
// ❌ 错误
const x = 5;
const tmp = 'value';
const flg = true;

// ✅ 正确
const itemCount = 5;
const tempValue = 'value';
const isActive = true;
```

### 函数命名
- 使用 camelCase 命名函数
- 函数名应该描述其功能
- 动作函数应该以动词开头

### 示例
```typescript
// ❌ 错误
function doStuff() {}
function getVal() {}

// ✅ 正确
function calculateTotal() {}
function fetchUserData() {}
```

## 2. 代码结构

### 函数长度
- 函数长度不应超过 50 行
- 如果函数太长，应拆分成更小的函数

### 代码块
- 每个代码块不应超过 20 行
- 使用空行分隔逻辑块
- 保持代码缩进一致

### 示例
```typescript
// ❌ 错误
function processData(data) {
  if (data) {
    // 长代码块
    // ...
  } else {
    // 另一个长代码块
    // ...
  }
}

// ✅ 正确
function processData(data) {
  if (data) {
    processValidData(data);
  } else {
    processInvalidData();
  }
}

function processValidData(data) {
  // 逻辑块 1
  // ...
}

function processInvalidData() {
  // 逻辑块 2
  // ...
}
```

## 3. 代码注释

### 要求
- 对复杂逻辑添加注释
- 注释应该解释为什么这样做，而不是做什么
- 使用 JSDoc 注释函数和类型

### 示例
```typescript
// ❌ 错误
// 计算总和
function calculateSum(a, b) {
  return a + b;
}

// ✅ 正确
/**
 * 计算两个数字的总和
 *
 * @param a 第一个数字
 * @param b 第二个数字
 * @returns 总和
 */
function calculateSum(a: number, b: number): number {
  return a + b;
}
```

## 4. 错误处理

### 要求
- 捕获所有可能的错误
- 提供有意义的错误消息
- 不要在错误中泄露敏感信息

### 示例
```typescript
// ❌ 错误
function fetchData() {
  return fetch('/api/data');
}

// ✅ 正确
async function fetchData(): Promise<Data> {
  try {
    const response = await fetch('/api/data');
    if (!response.ok) {
      throw new Error(`HTTP error: ${response.status}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Failed to fetch data:', error);
    throw new Error('Failed to fetch data. Please try again later.');
  }
}
```

## 5. 类型安全

### 要求
- 避免使用 any 类型
- 定义明确的类型
- 使用类型检查工具

### 示例
```typescript
// ❌ 错误
function processData(data: any) {
  return data.value;
}

// ✅ 正确
interface ProcessDataInput {
  value: string;
  count: number;
}

function processData(data: ProcessDataInput): string {
  return data.value;
}
```
```

**Step 4: 创建测试规则文档**
```markdown
# 测试规则

## 1. 测试驱动开发

### 要求
- 始终先编写测试，然后实现代码
- 测试应该覆盖所有功能和边缘情况
- 在实现代码前验证测试失败

### 示例
```typescript
// 1. 先写测试
test('calculateSum returns correct sum', () => {
  expect(calculateSum(2, 3)).toBe(5);
});

// 2. 运行测试（失败）
// 3. 实现代码
function calculateSum(a: number, b: number): number {
  return a + b;
}

// 4. 运行测试（通过）
```

## 2. 测试覆盖要求

### 最低要求
- 所有代码覆盖至少 80%
- 单元测试覆盖 80%+
- 集成测试覆盖 60%+
- E2E 测试覆盖关键用户流程

### 关键代码
- 金融计算：100% 覆盖
- 认证逻辑：100% 覆盖
- 安全关键代码：100% 覆盖
- 核心业务逻辑：100% 覆盖

## 3. 测试类型

### 单元测试
- 测试单个函数或组件
- 隔离测试，模拟外部依赖
- 每个测试应该是独立的

### 集成测试
- 测试组件之间的交互
- 测试 API 端点
- 测试数据库操作

### E2E 测试
- 测试完整的用户流程
- 模拟真实用户交互
- 覆盖关键用户路径

## 4. 测试文件组织

### 要求
- 测试文件与源代码文件位于同一目录
- 测试文件命名为 `<filename>.test.ts`
- 集成测试命名为 `<filename>.integration.test.ts`
- E2E 测试存储在 e2e/ 目录中

### 示例
```
src/
├── components/
│   ├── Button/
│   │   ├── Button.tsx
│   │   └── Button.test.tsx
│   └── MarketCard/
│       ├── MarketCard.tsx
│       └── MarketCard.test.tsx
├── app/
│   └── api/
│       └── markets/
│           ├── route.ts
│           └── route.integration.test.ts
└── e2e/
    ├── markets.spec.ts
    └── auth.spec.ts
```

## 5. 测试模式

### 禁止
- 测试实现细节
- 使用脆弱的选择器
- 测试相互依赖

### 要求
- 测试用户可见行为
- 使用语义选择器
- 保持测试独立

### 示例
```typescript
// ❌ 错误
test('component state updates', () => {
  expect(component.state.count).toBe(5);
});

// ✅ 正确
test('count display updates', () => {
  expect(screen.getByText('Count: 5')).toBeInTheDocument();
});
```

## 6. 模拟外部服务

### 要求
- 在单元测试中模拟外部依赖
- 使用合适的模拟库
- 确保模拟真实的行为

### 示例
```typescript
jest.mock('@/lib/supabase', () => ({
  supabase: {
    from: jest.fn(() => ({
      select: jest.fn(() => ({
        eq: jest.fn(() => Promise.resolve({
          data: [{ id: 1, name: 'Test Market' }],
          error: null
        }))
      }))
    }))
  }
}));
```

## 7. 持续测试

### 要求
- 使用监视模式进行开发
- 使用预提交钩子运行测试
- 在 CI/CD 中运行测试

### 示例
```yaml
# GitHub Actions
- name: 运行测试
  run: npm test -- --coverage
- name: 上传覆盖报告
  uses: codecov/codecov-action@v3
```
```

**Step 5: 创建 Git 工作流程规则文档**
```markdown
# Git 工作流程规则

## 1. 分支策略

### 主分支
- `main`：生产就绪代码
- `develop`：开发代码

### 功能分支
- 从 `develop` 分支创建功能分支
- 分支命名：`feature/<功能名称>`
- 功能完成后合并到 `develop`

### 修复分支
- 从 `main` 分支创建修复分支
- 分支命名：`hotfix/<问题描述>`
- 修复完成后合并到 `main` 和 `develop`

## 2. 提交格式

### 要求
- 使用语义化提交格式
- 提交消息应该清晰明确

### 格式
```
<类型>(<范围>): <简短描述>

[可选的详细描述]

[可选的关联问题]
```

### 类型
- `feat`：新功能
- `fix`：修复错误
- `docs`：文档更新
- `style`：代码风格调整
- `refactor`：重构
- `test`：测试更新
- `chore`：构建或工具更新

### 示例
```
feat: 添加市场搜索功能

- 实现语义搜索
- 添加搜索结果分页
- 优化搜索性能

关联问题：#123
```

## 3. PR 流程

### 要求
- 所有变更必须通过 PR 合并
- PR 必须有明确的标题和描述
- PR 必须通过所有检查

### 流程
1. 创建 PR 前运行验证循环
2. 在 PR 中描述变更内容
3. 等待代码审查
4. 解决审查反馈
5. 合并 PR

## 4. 代码审查

### 要求
- 所有 PR 必须经过至少一个审查
- 审查应该关注代码质量和安全
- 审查应该在 24 小时内完成

### 审查内容
- 代码质量
- 安全问题
- 测试覆盖
- 性能优化
- 架构决策

## 5. 持续集成

### 要求
- 所有 PR 必须通过 CI 检查
- CI 应该运行测试、lint 和构建
- CI 应该检查代码覆盖

### 示例
```yaml
name: CI

on: [pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - name: 检出代码
      uses: actions/checkout@v3
    - name: 安装依赖
      run: npm install
    - name: 运行 lint
      run: npm run lint
    - name: 运行测试
      run: npm test -- --coverage
    - name: 构建项目
      run: npm run build
```

## 6. 版本控制

### 要求
- 使用语义化版本控制
- 版本格式：`MAJOR.MINOR.PATCH`
- 发布前更新 CHANGELOG

### 版本升级规则
- `MAJOR`：不兼容的 API 变更
- `MINOR`：向后兼容的功能添加
- `PATCH`：向后兼容的错误修复

## 7. 代码复用

### 要求
- 避免重复代码
- 提取共享功能到公用库
- 使用适当的依赖管理

### 依赖管理
- 定期更新依赖
- 避免不必要的依赖
- 使用最小版本范围
```

**Step 6: 保存所有规则文档**
Run: `mkdir -p "C:\Users\13466\.claude\mindsymphony-v21\rules" && cat > "C:\Users\13466\.claude\mindsymphony-v21\rules\README.md" << 'EOF'
[规则系统概述内容]
EOF`

Run: `cat > "C:\Users\13466\.claude\mindsymphony-v21\rules\security.md" << 'EOF'
[安全规则内容]
EOF`

Run: `cat > "C:\Users\13466\.claude\mindsymphony-v21\rules\coding-style.md" << 'EOF'
[编码风格规则内容]
EOF`

Run: `cat > "C:\Users\13466\.claude\mindsymphony-v21\rules\testing.md" << 'EOF'
[测试规则内容]
EOF`

Run: `cat > "C:\Users\13466\.claude\mindsymphony-v21\rules\git-workflow.md" << 'EOF'
[Git 工作流程规则内容]
EOF`

**Step 7: 验证文件创建成功**
Run: `ls -la "C:\Users\13466\.claude\mindsymphony-v21\rules"`
Expected: README.md、security.md、coding-style.md、testing.md、git-workflow.md 文件存在

**Step 8: 提交到版本控制**
```bash
git add "C:\Users\13466\.claude\mindsymphony-v21\rules\README.md" "C:\Users\13466\.claude\mindsymphony-v21\rules\security.md" "C:\Users\13466\.claude\mindsymphony-v21\rules\coding-style.md" "C:\Users\13466\.claude\mindsymphony-v21\rules\testing.md" "C:\Users\13466\.claude\mindsymphony-v21\rules\git-workflow.md"
git commit -m "feat: add rules system"
```

---

## 执行选择

计划已完成并保存到 `docs/plans/2026-01-23-mindsymphony-development-workflow-enhancement.md`。两个执行选项：

**1. 子代理驱动（当前会话）** - 我为每个任务调度新的子代理，任务间进行审查，快速迭代

**2. 并行会话（单独）** - 打开新会话使用 executing-plans，批量执行并带有检查点

**选择子代理驱动方式**。