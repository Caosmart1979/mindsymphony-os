# MindSymphony 可迁移架构设计 - 支持 agent-cowork 和 claude-cowork

**文档版本**: 4.0 (Migration-Ready Architecture)
**创建日期**: 2026-01-15
**战略定位**: agent-cowork 是基础设施，claude-cowork 是未来迁移目标

---

## 执行摘要

### 核心战略

```
现在：基于 agent-cowork 开发
  ↓ (设计抽象层)
未来：平滑迁移到 claude-cowork
  ↓ (或者)
理想：双轨支持，用户可选
```

**关键原则**：
1. **依赖抽象而非具体实现** - 适配器模式
2. **保持迁移能力** - 无缝切换
3. **最大化灵活性** - 支持多种执行引擎

---

## 目录

1. [架构分层设计](#1-架构分层设计)
2. [适配器模式实现](#2-适配器模式实现)
3. [迁移策略](#3-迁移策略)
4. [实施路线图](#4-实施路线图)
5. [风险与机遇](#5-风险与机遇)

---

## 1. 架构分层设计

### 1.1 五层架构

```
┌─────────────────────────────────────────────────────────┐
│  Layer 5: MindSymphony 应用层 (Application Layer)       │
│  ┌───────────────────────────────────────────────────┐  │
│  │ • 技能浏览器 (Skill Explorer)                     │  │
│  │ • BMAD 工作流面板 (BMAD Workflow Dashboard)       │  │
│  │ • 智能推荐引擎 (Smart Recommendation Engine)      │  │
│  │ • 会话管理器 (Session Manager)                    │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                         ↕ 调用
┌─────────────────────────────────────────────────────────┐
│  Layer 4: MindSymphony 业务逻辑层 (Business Logic)      │
│  ┌───────────────────────────────────────────────────┐  │
│  │ • skill_router (技能路由)                         │  │
│  │ • skill_index (技能索引)                          │  │
│  │ • bmad_orchestrator (BMAD 编排器)                 │  │
│  │ • interop_manager (互操作管理器)                  │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                         ↕ 通过抽象接口
┌─────────────────────────────────────────────────────────┐
│  Layer 3: Agent 抽象层 (Agent Abstraction Layer) ⭐     │
│  ┌───────────────────────────────────────────────────┐  │
│  │ IAgentExecutor (接口)                             │  │
│  │  ├─ invoke_tool(tool_name, params)                │  │
│  │  ├─ stream_response(message)                      │  │
│  │  ├─ request_permission(tool_use)                  │  │
│  │  ├─ manage_session(session_id)                    │  │
│  │  └─ register_custom_tools(tools)                  │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
          ↕                            ↕
┌───────────────────────┐    ┌────────────────────────────┐
│ Layer 2A: 适配器层    │    │ Layer 2B: 适配器层         │
│ (agent-cowork)        │    │ (claude-cowork)            │
├───────────────────────┤    ├────────────────────────────┤
│ AgentCoworkAdapter    │    │ ClaudeCoworkAdapter        │
│ • 实现 IAgentExecutor │    │ • 实现 IAgentExecutor      │
│ • 调用 agent-cowork   │    │ • 调用 claude-cowork       │
│   SDK                 │    │   API                      │
└───────────────────────┘    └────────────────────────────┘
          ↕                            ↕
┌───────────────────────┐    ┌────────────────────────────┐
│ Layer 1A: 执行引擎    │    │ Layer 1B: 执行引擎         │
│ (agent-cowork)        │    │ (claude-cowork)            │
├───────────────────────┤    ├────────────────────────────┤
│ • Claude Agent SDK    │    │ • Claude Cowork API        │
│ • 开源实现            │    │ • 官方实现                 │
│ • 跨平台              │    │ • macOS/Windows            │
│ • 多模型支持          │    │ • 固定模型                 │
└───────────────────────┘    └────────────────────────────┘
```

**关键设计**：Layer 3 的抽象层使得 MindSymphony 完全独立于底层实现。

---

### 1.2 核心接口定义

#### **IAgentExecutor 接口**

```typescript
// mindsymphony-core/interfaces/IAgentExecutor.ts

/**
 * Agent 执行引擎的抽象接口
 * 任何实现（agent-cowork, claude-cowork, 或其他）都必须实现此接口
 */
export interface IAgentExecutor {
  /**
   * 初始化 Agent 执行引擎
   * @param config 配置选项
   */
  initialize(config: AgentConfig): Promise<void>;

  /**
   * 调用工具
   * @param toolName 工具名称
   * @param params 工具参数
   * @returns 工具执行结果
   */
  invokeTool(toolName: string, params: Record<string, any>): Promise<ToolResult>;

  /**
   * 发送消息并流式接收响应
   * @param message 用户消息
   * @param sessionId 会话ID
   * @param onChunk 接收响应片段的回调
   */
  streamResponse(
    message: string,
    sessionId: string,
    onChunk: (chunk: ResponseChunk) => void
  ): Promise<void>;

  /**
   * 请求用户权限
   * @param toolUse 工具使用请求
   * @returns 用户决策
   */
  requestPermission(toolUse: ToolUseRequest): Promise<PermissionDecision>;

  /**
   * 会话管理
   */
  createSession(config: SessionConfig): Promise<string>;
  getSession(sessionId: string): Promise<Session>;
  deleteSession(sessionId: string): Promise<void>;

  /**
   * 注册自定义工具
   * @param tools 工具定义数组
   */
  registerCustomTools(tools: CustomTool[]): Promise<void>;

  /**
   * 获取引擎信息
   */
  getEngineInfo(): EngineInfo;
}

/**
 * 通用类型定义
 */
export interface AgentConfig {
  apiKey?: string;
  model?: string;
  workingDirectory?: string;
  allowedTools?: string[];
}

export interface ToolResult {
  success: boolean;
  output: any;
  error?: string;
}

export interface ResponseChunk {
  type: 'text' | 'tool_use' | 'error' | 'done';
  content: string;
  metadata?: Record<string, any>;
}

export interface ToolUseRequest {
  toolUseId: string;
  toolName: string;
  input: Record<string, any>;
}

export interface PermissionDecision {
  status: 'allow' | 'deny';
  modifiedInput?: Record<string, any>;
  reason?: string;
}

export interface SessionConfig {
  workingDirectory: string;
  title?: string;
}

export interface Session {
  id: string;
  title: string;
  status: 'idle' | 'running' | 'completed' | 'error';
  createdAt: Date;
  updatedAt: Date;
}

export interface CustomTool {
  name: string;
  description: string;
  schema: any;  // zod schema 或 JSON schema
  handler: (params: any) => Promise<any>;
}

export interface EngineInfo {
  name: string;
  version: string;
  capabilities: string[];
}
```

---

## 2. 适配器模式实现

### 2.1 agent-cowork 适配器

```typescript
// mindsymphony-core/adapters/AgentCoworkAdapter.ts

import { IAgentExecutor, AgentConfig, ToolResult, /* ... */ } from '../interfaces/IAgentExecutor';
import { spawn } from 'child_process';

/**
 * agent-cowork 执行引擎的适配器实现
 */
export class AgentCoworkAdapter implements IAgentExecutor {
  private config: AgentConfig | null = null;
  private activeSessions: Map<string, any> = new Map();

  async initialize(config: AgentConfig): Promise<void> {
    this.config = config;
    // 验证 agent-cowork 是否可用
    // 初始化连接等
    console.log('[AgentCoworkAdapter] Initialized with config:', config);
  }

  async invokeTool(toolName: string, params: Record<string, any>): Promise<ToolResult> {
    try {
      // 调用 agent-cowork 的工具系统
      // 这里的实现取决于 agent-cowork 的具体 API

      // 示例：通过 IPC 调用
      const result = await this.sendIPC('tool.invoke', {
        toolName,
        params
      });

      return {
        success: true,
        output: result
      };
    } catch (error) {
      return {
        success: false,
        output: null,
        error: error.message
      };
    }
  }

  async streamResponse(
    message: string,
    sessionId: string,
    onChunk: (chunk: ResponseChunk) => void
  ): Promise<void> {
    // 使用 agent-cowork 的流式 API
    // 将事件转换为标准的 ResponseChunk 格式

    const session = this.activeSessions.get(sessionId);
    if (!session) {
      throw new Error(`Session ${sessionId} not found`);
    }

    // 示例实现
    await this.sendIPC('session.start', {
      sessionId,
      message
    });

    // 监听流式事件
    this.onIPCEvent('stream.message', (data) => {
      onChunk({
        type: 'text',
        content: data.content,
        metadata: data.metadata
      });
    });

    this.onIPCEvent('stream.done', () => {
      onChunk({
        type: 'done',
        content: ''
      });
    });
  }

  async requestPermission(toolUse: ToolUseRequest): Promise<PermissionDecision> {
    // agent-cowork 的权限请求机制
    return new Promise((resolve) => {
      // 发送权限请求
      this.sendIPC('permission.request', toolUse);

      // 等待用户响应
      this.onIPCEvent('permission.response', (decision) => {
        resolve(decision);
      });
    });
  }

  async createSession(config: SessionConfig): Promise<string> {
    const sessionId = this.generateSessionId();
    const session = {
      id: sessionId,
      title: config.title || 'New Session',
      status: 'idle',
      createdAt: new Date(),
      updatedAt: new Date(),
      workingDirectory: config.workingDirectory
    };

    this.activeSessions.set(sessionId, session);

    // 通知 agent-cowork 创建会话
    await this.sendIPC('session.create', session);

    return sessionId;
  }

  async getSession(sessionId: string): Promise<Session> {
    const session = this.activeSessions.get(sessionId);
    if (!session) {
      throw new Error(`Session ${sessionId} not found`);
    }
    return session;
  }

  async deleteSession(sessionId: string): Promise<void> {
    this.activeSessions.delete(sessionId);
    await this.sendIPC('session.delete', { sessionId });
  }

  async registerCustomTools(tools: CustomTool[]): Promise<void> {
    // 将 MindSymphony 的工具注册到 agent-cowork
    await this.sendIPC('tools.register', { tools });
  }

  getEngineInfo(): EngineInfo {
    return {
      name: 'agent-cowork',
      version: '0.0.2',
      capabilities: [
        'streaming',
        'tool_use',
        'permission_control',
        'session_management',
        'custom_tools'
      ]
    };
  }

  // 私有方法
  private generateSessionId(): string {
    return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  private async sendIPC(event: string, data: any): Promise<any> {
    // IPC 通信实现
    // 这取决于 agent-cowork 的具体实现
    // 可能是 Electron IPC、HTTP API、或其他机制

    // 示例：通过 HTTP
    const response = await fetch(`http://localhost:3000/api/${event}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return await response.json();
  }

  private onIPCEvent(event: string, handler: (data: any) => void): void {
    // 事件监听实现
    // 这取决于 agent-cowork 的具体实现
  }
}
```

---

### 2.2 claude-cowork 适配器

```typescript
// mindsymphony-core/adapters/ClaudeCoworkAdapter.ts

import { IAgentExecutor, AgentConfig, ToolResult, /* ... */ } from '../interfaces/IAgentExecutor';

/**
 * claude-cowork 执行引擎的适配器实现
 * 注意：此实现基于预期的 API，实际 API 可能不同
 */
export class ClaudeCoworkAdapter implements IAgentExecutor {
  private config: AgentConfig | null = null;
  private apiClient: any = null;

  async initialize(config: AgentConfig): Promise<void> {
    this.config = config;

    // 初始化 claude-cowork API 客户端
    // 实际实现取决于官方 API
    this.apiClient = await this.createClaudeCoworkClient(config);

    console.log('[ClaudeCoworkAdapter] Initialized with config:', config);
  }

  async invokeTool(toolName: string, params: Record<string, any>): Promise<ToolResult> {
    try {
      // 调用 claude-cowork 的 API
      // 实际 API 路径待官方文档确认
      const result = await this.apiClient.tools.invoke({
        tool: toolName,
        parameters: params
      });

      return {
        success: true,
        output: result.output
      };
    } catch (error) {
      return {
        success: false,
        output: null,
        error: error.message
      };
    }
  }

  async streamResponse(
    message: string,
    sessionId: string,
    onChunk: (chunk: ResponseChunk) => void
  ): Promise<void> {
    // 使用 claude-cowork 的流式 API
    const stream = await this.apiClient.sessions.stream({
      sessionId,
      message
    });

    for await (const chunk of stream) {
      // 转换为标准格式
      onChunk(this.convertToResponseChunk(chunk));
    }
  }

  async requestPermission(toolUse: ToolUseRequest): Promise<PermissionDecision> {
    // claude-cowork 可能有不同的权限模型
    // 这里需要适配

    // 假设 claude-cowork 使用文件夹级别的权限
    // 而不是工具级别的权限
    // 我们需要将工具请求映射到文件夹权限

    return {
      status: 'allow',  // 或通过其他机制请求
      modifiedInput: undefined,
      reason: undefined
    };
  }

  async createSession(config: SessionConfig): Promise<string> {
    const session = await this.apiClient.sessions.create({
      workingDirectory: config.workingDirectory,
      title: config.title
    });
    return session.id;
  }

  async getSession(sessionId: string): Promise<Session> {
    const session = await this.apiClient.sessions.get(sessionId);
    return this.convertToSession(session);
  }

  async deleteSession(sessionId: string): Promise<void> {
    await this.apiClient.sessions.delete(sessionId);
  }

  async registerCustomTools(tools: CustomTool[]): Promise<void> {
    // claude-cowork 可能通过 MCP 注册工具
    // 而不是直接注册

    for (const tool of tools) {
      await this.registerMCPTool(tool);
    }
  }

  getEngineInfo(): EngineInfo {
    return {
      name: 'claude-cowork',
      version: '1.0.0',  // 假设版本
      capabilities: [
        'streaming',
        'tool_use',
        'vm_sandbox',
        'mcp_integration',
        'folder_permissions'
      ]
    };
  }

  // 私有方法
  private async createClaudeCoworkClient(config: AgentConfig): Promise<any> {
    // 创建 claude-cowork API 客户端
    // 实际实现取决于官方 SDK

    // 示例：假设有官方 SDK
    // const { ClaudeCoworkClient } = require('@anthropic/claude-cowork');
    // return new ClaudeCoworkClient({ apiKey: config.apiKey });

    return {
      tools: { invoke: async () => {} },
      sessions: {
        create: async () => ({ id: 'session_id' }),
        get: async () => ({}),
        delete: async () => {},
        stream: async function* () {}
      }
    };
  }

  private convertToResponseChunk(chunk: any): ResponseChunk {
    // 将 claude-cowork 的响应格式转换为标准格式
    return {
      type: chunk.type || 'text',
      content: chunk.content || '',
      metadata: chunk.metadata || {}
    };
  }

  private convertToSession(session: any): Session {
    return {
      id: session.id,
      title: session.title,
      status: session.status,
      createdAt: new Date(session.createdAt),
      updatedAt: new Date(session.updatedAt)
    };
  }

  private async registerMCPTool(tool: CustomTool): Promise<void> {
    // 通过 MCP 协议注册工具
    // 实际实现取决于 MCP 集成方式
  }
}
```

---

### 2.3 适配器工厂

```typescript
// mindsymphony-core/AdapterFactory.ts

import { IAgentExecutor } from './interfaces/IAgentExecutor';
import { AgentCoworkAdapter } from './adapters/AgentCoworkAdapter';
import { ClaudeCoworkAdapter } from './adapters/ClaudeCoworkAdapter';

export type ExecutorType = 'agent-cowork' | 'claude-cowork' | 'auto';

export class AdapterFactory {
  /**
   * 创建适配器实例
   * @param type 执行引擎类型
   * @returns Agent 执行器实例
   */
  static create(type: ExecutorType = 'auto'): IAgentExecutor {
    if (type === 'auto') {
      type = this.detectAvailableExecutor();
    }

    switch (type) {
      case 'agent-cowork':
        return new AgentCoworkAdapter();

      case 'claude-cowork':
        return new ClaudeCoworkAdapter();

      default:
        throw new Error(`Unknown executor type: ${type}`);
    }
  }

  /**
   * 自动检测可用的执行引擎
   */
  private static detectAvailableExecutor(): ExecutorType {
    // 优先选择官方 claude-cowork（如果可用）
    if (this.isClaudeCoworkAvailable()) {
      return 'claude-cowork';
    }

    // 否则使用 agent-cowork
    if (this.isAgentCoworkAvailable()) {
      return 'agent-cowork';
    }

    throw new Error('No agent executor available');
  }

  private static isClaudeCoworkAvailable(): boolean {
    // 检测 claude-cowork 是否可用
    // 例如：检查是否安装了 Claude Desktop
    // 或者检查是否有 claude-cowork API 访问权限

    try {
      // 示例检测逻辑
      const fs = require('fs');
      const os = require('os');

      if (os.platform() === 'darwin') {
        // macOS: 检查 Claude Desktop 是否安装
        return fs.existsSync('/Applications/Claude.app');
      }

      // 其他平台暂不支持
      return false;
    } catch {
      return false;
    }
  }

  private static isAgentCoworkAvailable(): boolean {
    // 检测 agent-cowork 是否可用
    // 例如：检查是否启动了 agent-cowork 服务

    try {
      // 示例：检查端口是否监听
      const net = require('net');
      return new Promise((resolve) => {
        const client = net.connect({ port: 3000 }, () => {
          client.end();
          resolve(true);
        });
        client.on('error', () => resolve(false));
      });
    } catch {
      return false;
    }
  }
}
```

---

### 2.4 使用示例

```typescript
// mindsymphony-desktop/src/services/agent-service.ts

import { AdapterFactory } from 'mindsymphony-core/AdapterFactory';
import { IAgentExecutor } from 'mindsymphony-core/interfaces/IAgentExecutor';

export class AgentService {
  private executor: IAgentExecutor;

  constructor(executorType: 'agent-cowork' | 'claude-cowork' | 'auto' = 'auto') {
    // 自动选择或手动指定执行引擎
    this.executor = AdapterFactory.create(executorType);
  }

  async initialize(config: any) {
    await this.executor.initialize(config);
    console.log('Agent executor initialized:', this.executor.getEngineInfo());
  }

  async invokeMindSymphonySkill(skillName: string, args: string) {
    // 调用 MindSymphony 技能
    const result = await this.executor.invokeTool('InvokeSkill', {
      skillName,
      skillArgs: args
    });

    return result.output;
  }

  async startConversation(message: string, sessionId: string) {
    await this.executor.streamResponse(
      message,
      sessionId,
      (chunk) => {
        // 处理流式响应
        if (chunk.type === 'text') {
          console.log('Received:', chunk.content);
        } else if (chunk.type === 'tool_use') {
          console.log('Tool use:', chunk.content);
        } else if (chunk.type === 'done') {
          console.log('Conversation done');
        }
      }
    );
  }

  // 注册 MindSymphony 工具
  async registerMindSymphonyTools() {
    await this.executor.registerCustomTools([
      {
        name: 'InvokeSkill',
        description: 'Invoke a MindSymphony skill',
        schema: {
          type: 'object',
          properties: {
            skillName: { type: 'string' },
            skillArgs: { type: 'string' }
          }
        },
        handler: async (params) => {
          // 调用 MindSymphony 后端
          const response = await fetch('http://localhost:8000/api/skills/invoke', {
            method: 'POST',
            body: JSON.stringify(params)
          });
          return await response.json();
        }
      },
      // 其他工具...
    ]);
  }
}
```

---

## 3. 迁移策略

### 3.1 迁移路径

```
阶段 0: 当前状态（纯 MindSymphony）
  ├─ CLI 工具
  ├─ Python 后端
  └─ 无 GUI

阶段 1: 集成 agent-cowork（短期：0-3 个月）
  ├─ 实现 AgentCoworkAdapter
  ├─ 开发 MindSymphony UI
  ├─ 注册 MindSymphony 工具
  └─ 生产环境部署

阶段 2: 准备迁移（中期：3-6 个月）
  ├─ 监控 claude-cowork 开放进度
  ├─ 实现 ClaudeCoworkAdapter（预先开发）
  ├─ 编写迁移测试套件
  └─ 准备用户通知

阶段 3: 双轨支持（长期：6-12 个月）
  ├─ claude-cowork 正式可用时切换
  ├─ 保留 agent-cowork 作为备选
  ├─ 用户可选择执行引擎
  └─ 平滑迁移现有用户

阶段 4: 优化与统一（1+ 年）
  ├─ 根据用户使用情况优化
  ├─ 可能统一到 claude-cowork
  └─ 或继续双轨支持
```

---

### 3.2 迁移清单

#### **代码层面**

- [ ] **抽象接口定义完成** - `IAgentExecutor`
- [ ] **agent-cowork 适配器实现** - `AgentCoworkAdapter`
- [ ] **claude-cowork 适配器框架** - `ClaudeCoworkAdapter`
- [ ] **适配器工厂实现** - `AdapterFactory`
- [ ] **配置管理支持多引擎** - 用户可选择引擎

#### **测试层面**

- [ ] **接口合约测试** - 确保两个适配器遵守相同接口
- [ ] **模拟测试** - 使用 Mock 测试 claude-cowork 适配器
- [ ] **端到端测试** - 完整的用户流程测试
- [ ] **性能测试** - 比较两种引擎的性能
- [ ] **迁移测试** - 模拟从 agent-cowork 切换到 claude-cowork

#### **文档层面**

- [ ] **架构文档** - 详细说明抽象层设计
- [ ] **API 文档** - `IAgentExecutor` 接口文档
- [ ] **迁移指南** - 用户如何切换引擎
- [ ] **开发者指南** - 如何添加新的适配器

#### **用户体验层面**

- [ ] **引擎选择器** - UI 中提供引擎选择选项
- [ ] **平滑切换** - 会话可以跨引擎恢复
- [ ] **功能检测** - 自动检测引擎能力并调整 UI
- [ ] **错误处理** - 引擎不可用时的降级方案

---

### 3.3 配置示例

```typescript
// mindsymphony.config.ts

export interface MindSymphonyConfig {
  // 执行引擎配置
  executor: {
    // 默认引擎：'auto' | 'agent-cowork' | 'claude-cowork'
    default: 'auto';

    // 引擎优先级（用于自动选择）
    priority: ['claude-cowork', 'agent-cowork'];

    // agent-cowork 配置
    agentCowork: {
      host: 'localhost';
      port: 3000;
      apiKey?: string;
    };

    // claude-cowork 配置
    claudeCowork: {
      // 待官方文档确定
      subscription: 'max';
      apiEndpoint?: string;
    };
  };

  // MindSymphony 配置
  mindSymphony: {
    backendUrl: 'http://localhost:8000';
    skillsPath: '~/mindsymphony-os/skills';
  };

  // 功能开关
  features: {
    enableBMAD: true;
    enableSmartRecommendations: true;
    enableSkillMarketplace: false;
  };
}
```

**用户配置文件**:

```json
// ~/.mindsymphony/config.json
{
  "executor": {
    "default": "auto",
    "priority": ["claude-cowork", "agent-cowork"]
  },
  "mindSymphony": {
    "backendUrl": "http://localhost:8000"
  }
}
```

---

## 4. 实施路线图

### 4.1 Phase 1: 抽象层与 agent-cowork 集成（4-6 周）

#### **Week 1-2: 抽象层设计**

**任务**:
- [ ] 定义 `IAgentExecutor` 接口
- [ ] 定义所有类型（`AgentConfig`, `ToolResult` 等）
- [ ] 创建适配器基类
- [ ] 实现 `AdapterFactory`

**产出**:
```
mindsymphony-core/
├── interfaces/
│   └── IAgentExecutor.ts
├── adapters/
│   ├── BaseAdapter.ts
│   ├── AgentCoworkAdapter.ts
│   └── ClaudeCoworkAdapter.ts (skeleton)
├── AdapterFactory.ts
└── types.ts
```

---

#### **Week 3-4: agent-cowork 适配器实现**

**任务**:
- [ ] 实现 `AgentCoworkAdapter`
- [ ] 集成 agent-cowork 的 IPC 机制
- [ ] 实现工具调用
- [ ] 实现流式响应
- [ ] 实现权限系统

**测试**:
```typescript
// 单元测试
describe('AgentCoworkAdapter', () => {
  it('should initialize successfully', async () => {
    const adapter = new AgentCoworkAdapter();
    await adapter.initialize({ apiKey: 'test' });
    expect(adapter.getEngineInfo().name).toBe('agent-cowork');
  });

  it('should invoke tool successfully', async () => {
    const adapter = new AgentCoworkAdapter();
    const result = await adapter.invokeTool('Read', { filePath: 'test.txt' });
    expect(result.success).toBe(true);
  });
});
```

---

#### **Week 5-6: MindSymphony 工具注册**

**任务**:
- [ ] 实现 `InvokeSkill` 工具
- [ ] 实现 `RouteIntent` 工具
- [ ] 实现 `BMADWorkflow` 工具
- [ ] 注册到 agent-cowork

**验证**:
```typescript
// 集成测试
const agentService = new AgentService('agent-cowork');
await agentService.initialize({ apiKey: 'test' });
await agentService.registerMindSymphonyTools();

// 测试调用
const result = await agentService.invokeMindSymphonySkill(
  'frontend-design',
  'Create a login page'
);

expect(result).toContain('login page design');
```

**里程碑**: **Phase 1 完成** - MindSymphony 可以通过 agent-cowork 运行

---

### 4.2 Phase 2: UI 开发（4 周）

#### **Week 7-8: 核心 UI**

**任务**:
- [ ] 技能浏览器
- [ ] 会话管理器
- [ ] 流式输出显示

---

#### **Week 9-10: 高级功能**

**任务**:
- [ ] 智能推荐面板
- [ ] BMAD 工作流面板
- [ ] 设置面板（包括引擎选择）

**里程碑**: **Phase 2 完成** - 完整的桌面应用

---

### 4.3 Phase 3: claude-cowork 适配器（预先开发）（2-3 周）

#### **Week 11-13: ClaudeCoworkAdapter 框架**

**任务**:
- [ ] 研究 claude-cowork API（基于官方文档）
- [ ] 实现适配器骨架
- [ ] 编写 Mock 测试
- [ ] 准备迁移脚本

**注意**: 此阶段可能无法完全测试，因为 claude-cowork 尚未开放。但我们可以：
- 基于预期 API 编写代码
- 使用 Mock 测试
- 准备好随时集成

---

### 4.4 Phase 4: 双轨支持与迁移（2 周）

#### **Week 14-15: 完善双轨支持**

**任务**:
- [ ] 实现引擎自动检测
- [ ] 实现引擎切换 UI
- [ ] 会话跨引擎迁移
- [ ] 用户通知系统

**用户体验**:
```
设置 > 执行引擎
  ○ 自动选择（推荐）
  ○ agent-cowork
  ○ claude-cowork [当前不可用]

[测试连接] [保存]
```

---

### 4.5 总时间线

```
Phase 1: 抽象层 + agent-cowork (6 周)
Phase 2: UI 开发 (4 周)
Phase 3: claude-cowork 适配器框架 (3 周)
Phase 4: 双轨支持 (2 周)

总计: 15 周 (约 3.5 个月)
```

---

## 5. 风险与机遇

### 5.1 风险分析

| 风险 | 影响 | 可能性 | 缓解措施 |
|------|------|--------|----------|
| **claude-cowork API 与预期不同** | 高 | 高 | 使用抽象层，修改适配器即可 |
| **claude-cowork 长期不开放** | 中 | 中 | agent-cowork 作为长期方案 |
| **适配器性能开销** | 低 | 低 | 抽象层很薄，开销可忽略 |
| **双引擎维护成本** | 中 | 中 | 共享测试套件，自动化测试 |

---

### 5.2 机遇分析

| 机遇 | 价值 | 实现难度 |
|------|------|---------|
| **平台无关性** | 极高 | 中（已通过抽象层实现）|
| **用户选择自由** | 高 | 低（引擎切换简单）|
| **快速适应新引擎** | 高 | 低（添加新适配器）|
| **独立于单一供应商** | 极高 | 低（已解耦）|

---

### 5.3 成功标准

**技术标准**:
- [ ] MindSymphony 可以在 agent-cowork 上运行
- [ ] 抽象层性能开销 < 5%
- [ ] 适配器接口测试覆盖率 > 90%
- [ ] 可以在 1 小时内添加新适配器

**用户体验标准**:
- [ ] 用户无需了解底层引擎
- [ ] 引擎切换无需重新配置
- [ ] 会话可以跨引擎恢复
- [ ] 错误信息清晰易懂

---

## 6. 总结

### 6.1 核心价值

**可迁移架构的三大优势**:

1. **平台独立性** ✅
   - 不锁定在单一实现
   - 可以随时切换引擎

2. **风险规避** ✅
   - agent-cowork 停止维护？切换到 claude-cowork
   - claude-cowork 不开放？继续使用 agent-cowork
   - 出现更好的选择？添加新适配器

3. **用户自由** ✅
   - 用户可以选择引擎
   - 根据需求（性能、成本、功能）选择

---

### 6.2 立即行动

**本周可以开始**:

1. **创建抽象层**:
   ```bash
   mkdir -p mindsymphony-core/interfaces
   mkdir -p mindsymphony-core/adapters
   # 编写 IAgentExecutor.ts
   ```

2. **实现 AgentCoworkAdapter**:
   ```bash
   # 研究 agent-cowork 的 API
   # 实现适配器
   ```

3. **编写测试**:
   ```bash
   # 接口合约测试
   # 适配器单元测试
   ```

---

### 6.3 未来愿景

```
2026 Q1: 基于 agent-cowork 发布 MindSymphony Desktop
2026 Q2-Q3: claude-cowork 开放后，增加支持
2026 Q4: 双轨成熟，用户可自由选择
2027+: 可能支持更多引擎（如 Gemini、GPT 等）
```

---

**文档版本**: 4.0 (Migration-Ready Architecture)
**最后更新**: 2026-01-15
**作者**: Claude (Sonnet 4.5)
**战略定位**: agent-cowork 是基础设施，claude-cowork 是未来迁移目标

---

**许可证**: 本文档采用 CC BY 4.0 许可证发布。
