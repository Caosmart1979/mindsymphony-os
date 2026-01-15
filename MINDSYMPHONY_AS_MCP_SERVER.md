# MindSymphony 与 agent-cowork 的整合方式分析

**文档版本**: 5.0 (最终推荐方案)
**创建日期**: 2026-01-15
**核心问题**: 如果直接使用 agent-cowork，MindSymphony 应该以什么形式存在？

---

## 执行摘要

### 核心洞察

**不应该改造 agent-cowork，而应该让 MindSymphony 作为标准的能力提供者**。

```
agent-cowork (保持原样)
       ↓ 通过标准协议调用
MindSymphony (以某种标准形式提供能力)
```

---

## 三种整合方案对比

### 方案 A: MindSymphony 作为 MCP 服务器 ⭐⭐⭐⭐⭐

```
┌────────────────────────────────────────┐
│      agent-cowork (原生应用)           │
│  ┌──────────────────────────────────┐  │
│  │ Claude Agent SDK                 │  │
│  │ • 内置工具: Read/Write/Edit/Bash │  │
│  │ • MCP 客户端 (内置)              │  │
│  └──────────────────────────────────┘  │
│              ↓ MCP 协议                │
└──────────────┼────────────────────────┘
               ↓
┌──────────────────────────────────────┐
│  MindSymphony MCP Server             │
│  ┌────────────────────────────────┐  │
│  │ 工具暴露 (Tools)               │  │
│  │ ├─ mindsymphony.invoke_skill   │  │
│  │ ├─ mindsymphony.route_intent   │  │
│  │ ├─ mindsymphony.bmad_workflow  │  │
│  │ └─ ... (90+ 技能)              │  │
│  └────────────────────────────────┘  │
│              ↓                        │
│  ┌────────────────────────────────┐  │
│  │ MindSymphony Core (Python)     │  │
│  │ • skill_router                 │  │
│  │ • skill_index                  │  │
│  │ • 90+ 技能生态                 │  │
│  └────────────────────────────────┘  │
└──────────────────────────────────────┘
```

**工作原理**:
1. 用户在 agent-cowork 中输入："用 frontend-design 技能设计登录页面"
2. Claude Agent 识别需要调用 `mindsymphony.invoke_skill` 工具
3. 通过 MCP 协议调用 MindSymphony MCP Server
4. MindSymphony 执行技能并返回结果
5. Agent 将结果展示给用户

**优势**:
- ✅ **零侵入** - 无需修改 agent-cowork 代码
- ✅ **标准协议** - MCP 是 Claude Code 生态的标准
- ✅ **即插即用** - 只需配置 MCP 服务器路径
- ✅ **双向兼容** - 同时支持 Claude Code CLI 和 agent-cowork
- ✅ **官方推荐** - Anthropic 官方推荐的扩展方式

**劣势**:
- ⚠️ 需要开发 MCP 服务器（但工作量不大）
- ⚠️ MCP 协议相对简单，高级功能可能受限

**适用场景**: ✅ **强烈推荐** - 这是最标准、最优雅的方案

---

### 方案 B: MindSymphony 作为 agent-cowork 的自定义工具

```
┌────────────────────────────────────────┐
│  agent-cowork (需要修改)               │
│  ┌──────────────────────────────────┐  │
│  │ Claude Agent SDK                 │  │
│  │ • 内置工具: Read/Write/Edit/Bash │  │
│  │ • 自定义工具 (需添加):           │  │
│  │   ├─ InvokeSkill                 │  │
│  │   ├─ RouteIntent                 │  │
│  │   └─ BMADWorkflow                │  │
│  └──────────────────────────────────┘  │
│              ↓ HTTP/IPC                │
└──────────────┼────────────────────────┘
               ↓
┌──────────────────────────────────────┐
│  MindSymphony Backend (FastAPI)      │
│  • /api/skills/invoke                │
│  • /api/skills/route                 │
│  • /api/workflows/bmad               │
└──────────────────────────────────────┘
```

**工作原理**:
1. 在 agent-cowork 代码中注册自定义工具
2. 工具通过 HTTP 调用 MindSymphony 后端
3. 返回结果

**优势**:
- ✅ 灵活性高 - 可以自定义工具接口
- ✅ 性能好 - 直接 HTTP 调用

**劣势**:
- ❌ **需要修改 agent-cowork 源码** - 侵入性强
- ❌ 不利于维护 - agent-cowork 更新时需要重新修改
- ❌ 不标准 - 偏离 Claude Code 生态的标准做法

**适用场景**: ⚠️ 不推荐 - 除非有特殊需求

---

### 方案 C: MindSymphony 作为独立的技能管理器

```
┌────────────────────────────────────────┐
│      agent-cowork (原生应用)           │
│  用户输入自然语言指令                  │
└──────────────┬────────────────────────┘
               ↓
┌──────────────────────────────────────┐
│  MindSymphony Skill Manager          │
│  (作为中间层)                        │
│  ┌────────────────────────────────┐  │
│  │ 1. 接收用户输入                │  │
│  │ 2. 智能路由 → 推荐技能         │  │
│  │ 3. 生成优化后的 Prompt         │  │
│  │ 4. 发送给 agent-cowork         │  │
│  └────────────────────────────────┘  │
└──────────────────────────────────────┘
```

**工作原理**:
1. 用户不直接使用 agent-cowork
2. 通过 MindSymphony UI 输入需求
3. MindSymphony 智能路由推荐技能
4. 自动生成优化的 Prompt
5. 调用 agent-cowork 执行

**优势**:
- ✅ MindSymphony 保持独立性
- ✅ 可以完全控制用户体验

**劣势**:
- ❌ 架构复杂 - 多了一层中间层
- ❌ 用户体验割裂 - 不是在 agent-cowork 中直接使用

**适用场景**: ⚠️ 不推荐 - 过于复杂

---

## 推荐方案：MCP 服务器方案

### 为什么选择 MCP？

**1. 官方标准**

MCP (Model Context Protocol) 是 Anthropic 为 Claude Code 生态设计的标准协议。

官方文档明确说明：
> MCP 允许开发者将外部工具和数据源连接到 Claude，扩展其能力。

**2. 零侵入**

只需要在 agent-cowork 的配置文件中添加 MCP 服务器配置：

```json
// ~/.claude/settings.json
{
  "mcpServers": {
    "mindsymphony": {
      "command": "node",
      "args": ["/path/to/mindsymphony-mcp-server/dist/index.js"]
    }
  }
}
```

**3. 双向兼容**

同一个 MCP 服务器可以被以下客户端使用：
- ✅ agent-cowork
- ✅ Claude Code CLI
- ✅ Claude Desktop (如果支持 MCP)
- ✅ 任何支持 MCP 的客户端

**4. 标准化工具定义**

MCP 协议定义了标准的工具格式：

```typescript
// MCP 工具定义
{
  name: "mindsymphony_invoke_skill",
  description: "Invoke a MindSymphony skill for specialized tasks",
  inputSchema: {
    type: "object",
    properties: {
      skillName: {
        type: "string",
        description: "The skill to invoke (e.g., frontend-design, code-refactoring-expert)"
      },
      skillArgs: {
        type: "string",
        description: "Arguments to pass to the skill"
      }
    },
    required: ["skillName"]
  }
}
```

---

## MindSymphony MCP 服务器实现

### 架构设计

```
MindSymphony MCP Server
├── MCP 协议层 (通过 stdio 通信)
│   ├── 工具列表 (tools/list)
│   ├── 工具调用 (tools/call)
│   └── 提示词列表 (prompts/list)
│
├── 适配层 (将 MCP 调用转换为 MindSymphony 调用)
│   ├── invoke_skill → skill_router.invoke()
│   ├── route_intent → skill_router.route()
│   └── bmad_workflow → bmad_orchestrator.execute()
│
└── MindSymphony Core (现有系统)
    ├── skill_router.py
    ├── skill_index.py
    └── 90+ 技能
```

---

### 代码实现

#### **1. MCP 服务器主文件**

```typescript
// mindsymphony-mcp-server/src/index.ts

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  Tool
} from '@modelcontextprotocol/sdk/types.js';
import { spawn } from 'child_process';
import path from 'path';

// MindSymphony 后端路径（用户可配置）
const MINDSYMPHONY_PATH = process.env.MINDSYMPHONY_PATH ||
                          path.join(process.env.HOME!, 'mindsymphony-os');

/**
 * MindSymphony MCP Server
 * 将 MindSymphony 的 90+ 技能暴露为 MCP 工具
 */
class MindSymphonyMCPServer {
  private server: Server;
  private skillsList: any[] = [];

  constructor() {
    this.server = new Server(
      {
        name: 'mindsymphony',
        version: '1.0.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.setupHandlers();
  }

  private setupHandlers() {
    // 列出所有可用工具
    this.server.setRequestHandler(ListToolsRequestSchema, async () => {
      // 加载 MindSymphony 技能列表
      await this.loadSkillsList();

      const tools: Tool[] = [
        // 工具 1: 调用单个技能
        {
          name: 'mindsymphony_invoke_skill',
          description: 'Invoke a MindSymphony skill to perform specialized tasks. ' +
                       'MindSymphony has 90+ professional skills covering frontend design, ' +
                       'code refactoring, API integration, database schema design, and more.',
          inputSchema: {
            type: 'object',
            properties: {
              skillName: {
                type: 'string',
                description: `The skill to invoke. Available skills: ${this.getSkillNames().join(', ')}`,
                enum: this.getSkillNames()
              },
              skillArgs: {
                type: 'string',
                description: 'Arguments or instructions for the skill'
              }
            },
            required: ['skillName']
          }
        },

        // 工具 2: 智能路由推荐
        {
          name: 'mindsymphony_route_intent',
          description: 'Get skill recommendations based on user intent using intelligent routing',
          inputSchema: {
            type: 'object',
            properties: {
              query: {
                type: 'string',
                description: 'The user\'s intent or query (e.g., "I want to design a frontend interface")'
              }
            },
            required: ['query']
          }
        },

        // 工具 3: BMAD 工作流
        {
          name: 'mindsymphony_bmad_workflow',
          description: 'Start a BMAD enterprise-grade 6-phase agile workflow for complex projects. ' +
                       'Phases: Requirements → Architecture → Sprint Planning → Development → Code Review → Testing',
          inputSchema: {
            type: 'object',
            properties: {
              projectDescription: {
                type: 'string',
                description: 'Description of the project to build'
              }
            },
            required: ['projectDescription']
          }
        }
      ];

      return { tools };
    });

    // 调用工具
    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      try {
        switch (name) {
          case 'mindsymphony_invoke_skill':
            return await this.invokeSkill(args.skillName, args.skillArgs);

          case 'mindsymphony_route_intent':
            return await this.routeIntent(args.query);

          case 'mindsymphony_bmad_workflow':
            return await this.startBMADWorkflow(args.projectDescription);

          default:
            throw new Error(`Unknown tool: ${name}`);
        }
      } catch (error: any) {
        return {
          content: [
            {
              type: 'text',
              text: `Error: ${error.message}`
            }
          ],
          isError: true
        };
      }
    });
  }

  /**
   * 加载 MindSymphony 技能列表
   */
  private async loadSkillsList(): Promise<void> {
    if (this.skillsList.length > 0) return;

    return new Promise((resolve, reject) => {
      const python = spawn('python3', [
        '-m', 'skill_discovery.skill_index',
        '--list'
      ], {
        cwd: path.join(MINDSYMPHONY_PATH, 'skills')
      });

      let output = '';
      python.stdout.on('data', (data) => output += data.toString());
      python.on('close', (code) => {
        if (code === 0) {
          try {
            this.skillsList = JSON.parse(output).skills;
            resolve();
          } catch (error) {
            reject(error);
          }
        } else {
          reject(new Error('Failed to load skills list'));
        }
      });
    });
  }

  /**
   * 获取所有技能名称
   */
  private getSkillNames(): string[] {
    return this.skillsList.map(skill => skill.name);
  }

  /**
   * 调用 MindSymphony 技能
   */
  private async invokeSkill(skillName: string, skillArgs?: string): Promise<any> {
    return new Promise((resolve, reject) => {
      const python = spawn('python3', [
        '-m', 'skill_discovery.skill_router',
        '--invoke', skillName,
        ...(skillArgs ? ['--args', skillArgs] : [])
      ], {
        cwd: path.join(MINDSYMPHONY_PATH, 'skills')
      });

      let output = '';
      let error = '';

      python.stdout.on('data', (data) => output += data.toString());
      python.stderr.on('data', (data) => error += data.toString());

      python.on('close', (code) => {
        if (code === 0) {
          resolve({
            content: [
              {
                type: 'text',
                text: output
              }
            ]
          });
        } else {
          reject(new Error(`Skill execution failed: ${error}`));
        }
      });
    });
  }

  /**
   * 智能路由推荐
   */
  private async routeIntent(query: string): Promise<any> {
    return new Promise((resolve, reject) => {
      const python = spawn('python3', [
        '-m', 'skill_discovery.skill_router',
        '--route', query
      ], {
        cwd: path.join(MINDSYMPHONY_PATH, 'skills')
      });

      let output = '';
      python.stdout.on('data', (data) => output += data.toString());

      python.on('close', (code) => {
        if (code === 0) {
          const recommendations = JSON.parse(output);
          const formattedText = this.formatRecommendations(recommendations);
          resolve({
            content: [
              {
                type: 'text',
                text: formattedText
              }
            ]
          });
        } else {
          reject(new Error('Intent routing failed'));
        }
      });
    });
  }

  /**
   * 启动 BMAD 工作流
   */
  private async startBMADWorkflow(projectDescription: string): Promise<any> {
    return new Promise((resolve, reject) => {
      const python = spawn('python3', [
        '-m', 'workflows.bmad',
        '--start',
        projectDescription
      ], {
        cwd: path.join(MINDSYMPHONY_PATH, 'skills')
      });

      let output = '';
      python.stdout.on('data', (data) => output += data.toString());

      python.on('close', (code) => {
        if (code === 0) {
          resolve({
            content: [
              {
                type: 'text',
                text: output
              }
            ]
          });
        } else {
          reject(new Error('BMAD workflow failed'));
        }
      });
    });
  }

  /**
   * 格式化推荐结果
   */
  private formatRecommendations(recommendations: any[]): string {
    let text = '## Recommended Skills:\n\n';
    recommendations.forEach((rec, index) => {
      text += `${index + 1}. **${rec.skill.name}** (${Math.round(rec.confidence * 100)}% match)\n`;
      text += `   - ${rec.skill.description}\n`;
      text += `   - Reasoning: ${rec.reasoning}\n\n`;
    });
    return text;
  }

  /**
   * 启动服务器
   */
  async start() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('MindSymphony MCP Server started');
  }
}

// 启动服务器
const server = new MindSymphonyMCPServer();
server.start().catch(console.error);
```

---

#### **2. 配置文件**

```json
// mindsymphony-mcp-server/package.json
{
  "name": "mindsymphony-mcp-server",
  "version": "1.0.0",
  "description": "MCP server exposing MindSymphony's 90+ professional skills",
  "type": "module",
  "main": "dist/index.js",
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js",
    "dev": "tsx src/index.ts"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^0.5.0"
  },
  "devDependencies": {
    "typescript": "^5.3.0",
    "tsx": "^4.7.0"
  }
}
```

```json
// mindsymphony-mcp-server/tsconfig.json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "Node16",
    "moduleResolution": "Node16",
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

---

#### **3. 用户配置**

```json
// ~/.claude/settings.json
{
  "apiKey": "sk-ant-...",
  "model": "claude-sonnet-4-5",

  "mcpServers": {
    "mindsymphony": {
      "command": "node",
      "args": ["/Users/username/mindsymphony-mcp-server/dist/index.js"],
      "env": {
        "MINDSYMPHONY_PATH": "/Users/username/mindsymphony-os"
      }
    }
  }
}
```

---

## 使用示例

### 在 agent-cowork 中使用

```
用户: "用 frontend-design 技能设计一个登录页面"

Agent 思考:
  我需要调用 mindsymphony_invoke_skill 工具

Agent 调用:
  Tool: mindsymphony_invoke_skill
  Arguments: {
    skillName: "frontend-design",
    skillArgs: "Design a login page with email and password fields"
  }

MindSymphony 返回:
  [详细的前端设计方案...]

Agent 展示:
  根据 MindSymphony 的 frontend-design 技能，这里是登录页面设计...
```

### 在 Claude Code CLI 中使用

```bash
claude

> 我需要重构代码，请先推荐合适的技能

# Agent 自动调用 mindsymphony_route_intent
# 返回推荐的技能列表

> 使用 code-refactoring-expert 技能重构这个文件

# Agent 调用 mindsymphony_invoke_skill
```

---

## 实施路线图

### Phase 1: MCP 服务器开发（2-3 周）

**Week 1: 基础框架**
- [ ] 搭建 MCP 服务器项目
- [ ] 实现基础的工具列表和调用
- [ ] 测试与 agent-cowork 的连接

**Week 2: 核心功能**
- [ ] 实现 `invoke_skill` 工具
- [ ] 实现 `route_intent` 工具
- [ ] 实现 `bmad_workflow` 工具

**Week 3: 优化与测试**
- [ ] 错误处理
- [ ] 性能优化
- [ ] 端到端测试

**里程碑**: MCP 服务器可用，agent-cowork 可以调用 MindSymphony 技能

---

### Phase 2: 增强功能（1-2 周）

**Week 4: 动态技能注册**
- [ ] 自动扫描所有技能
- [ ] 为每个技能生成独立的 MCP 工具
- [ ] 提供技能详情和文档

**Week 5: 高级功能**
- [ ] 技能使用统计
- [ ] 缓存优化
- [ ] 日志和监控

---

## 优势总结

### ✅ 对用户的优势

1. **零配置** - 只需添加一行配置
2. **即插即用** - 下载 agent-cowork，添加 MCP 配置，立即可用
3. **标准体验** - 在 agent-cowork 中无缝使用 MindSymphony
4. **跨平台** - 同一个 MCP 服务器可用于 CLI 和 GUI

### ✅ 对开发的优势

1. **无需改造 agent-cowork** - 保持原版
2. **易于维护** - MCP 服务器独立维护
3. **易于升级** - agent-cowork 更新不影响 MindSymphony
4. **易于测试** - 可以独立测试 MCP 服务器

### ✅ 对生态的优势

1. **官方标准** - 遵循 Claude Code 生态标准
2. **可复用** - 其他 MCP 客户端也可以使用
3. **可扩展** - 未来可以添加更多工具
4. **可组合** - 可以与其他 MCP 服务器组合使用

---

## 最终推荐

**强烈推荐：MindSymphony 作为 MCP 服务器**

### 用户使用流程

```
1. 下载 agent-cowork
   git clone https://github.com/DevAgentForge/agent-cowork.git

2. 下载 MindSymphony MCP Server
   git clone https://github.com/yourname/mindsymphony-mcp-server.git
   cd mindsymphony-mcp-server
   npm install
   npm run build

3. 配置 MCP 服务器
   编辑 ~/.claude/settings.json
   添加 mcpServers.mindsymphony 配置

4. 启动 agent-cowork
   cd agent-cowork
   npm install
   npm start

5. 开始使用！
   在 agent-cowork 中输入：
   "用 frontend-design 技能设计登录页面"
```

### 开发工作量

- MCP 服务器开发：2-3 周
- 测试与优化：1 周
- 文档编写：几天

**总计**: 约 1 个月

---

## 与之前方案的对比

| 维度 | v1.0-v4.0 (改造方案) | v5.0 (MCP 方案) ⭐ |
|------|---------------------|-------------------|
| **侵入性** | 需要改造 agent-cowork | **零侵入** |
| **标准化** | 自定义实现 | **MCP 标准协议** |
| **开发时间** | 3-4 个月 | **1 个月** |
| **维护成本** | 高（需跟随 agent-cowork 更新）| **低（独立维护）** |
| **跨平台** | 仅限 agent-cowork | **所有 MCP 客户端** |
| **用户体验** | 需要特定版本的 agent-cowork | **原版 agent-cowork** |
| **可行性** | 8-9/10 | **10/10** |

---

## 立即行动

**本周可以开始**:

```bash
# 1. 创建 MCP 服务器项目
mkdir mindsymphony-mcp-server
cd mindsymphony-mcp-server
npm init -y

# 2. 安装依赖
npm install @modelcontextprotocol/sdk

# 3. 创建源文件
mkdir src
touch src/index.ts

# 4. 开始编写代码
# 按照上面的代码示例实现
```

---

**文档版本**: 5.0 (MCP Server Solution)
**最后更新**: 2026-01-15
**作者**: Claude (Sonnet 4.5)
**核心结论**: MindSymphony 作为 MCP 服务器，agent-cowork 保持原样

---

**许可证**: 本文档采用 CC BY 4.0 许可证发布。
