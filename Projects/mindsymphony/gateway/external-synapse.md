---
name: external-synapse
layer: foundation
type: system
triggers: [webhook, n8n, 外部调度, 出站, 集成]
version: "19.1"
---

# 外部神经突触 (External Synapse)

> 打破蜂巢的封闭性，让MindSymphony与外部世界双向通信。
> 解决测评报告指出的"Air-Gapped Hive"问题。

---

## 设计背景

```
测评报告原文：
"系统像一个封闭的蜂巢，内部工蜂忙碌协作，
但没有设计'采蜜口'（Input Webhook）和'分发口'（Output Webhook）。"

"如果不解决这一接口缺失问题，MindSymphony将只能作为一辅助思考工具存在，
而无法成为自动化业务流程（Business Process Automation, BPA）的核心引擎。"

解决方案：
External Synapse = 入站接口 + 出站接口 + 协议适配层
```

---

## 架构

```
                    ┌─────────────────────────────────────┐
                    │         MindSymphony Core           │
                    │  ┌─────────────────────────────┐    │
外部世界            │  │      Pheromone Bus          │    │            外部世界
   │                │  │    (内部信息素总线)          │    │                │
   │                │  └──────────┬──────────────────┘    │                │
   │                │             │                       │                │
   ▼                │             ▼                       │                ▼
┌──────┐         ┌──┴─────────────────────────────────┴──┐         ┌──────┐
│Input │ ──────► │         External Synapse              │ ──────► │Output│
│Webhook│        │  ┌─────────┐  ┌─────────┐  ┌────────┐ │        │Webhook│
│(n8n) │         │  │Ingress  │  │Protocol │  │Egress  │ │        │(n8n) │
│      │         │  │Gateway  │  │Adapter  │  │Gateway │ │        │      │
└──────┘         │  └─────────┘  └─────────┘  └────────┘ │        └──────┘
                 └────────────────────────────────────────┘
```

---

## 入站接口 (Ingress Gateway)

### 支持的入站源

| 来源 | 类型 | 触发方式 |
|------|------|----------|
| n8n Webhook | HTTP POST | 接收n8n工作流触发 |
| 飞书消息 | Event | 飞书机器人消息 |
| Slack | Event | Slack App消息 |
| 定时任务 | Cron | 系统调度器 |
| CLI命令 | stdin | 命令行直接输入 |

### 入站消息标准格式

```yaml
ingress_message:
  # 元数据
  message_id: "uuid"
  source: "n8n|feishu|slack|cron|cli"
  timestamp: "ISO8601"
  
  # 安全信息
  auth:
    type: "api_key|oauth|none"
    verified: true|false
    trust_level: "TRUSTED|VERIFIED|UNTRUSTED"
  
  # 负载
  payload:
    intent: "task|query|notification"
    content: "用户消息内容"
    context: {}  # 附加上下文
    
  # 回调配置
  callback:
    type: "webhook|none"
    url: "回调地址"
    method: "POST"
```

### 入站处理流程

```
外部消息到达
    │
    ▼
┌─────────────────────────────────────────────┐
│  Step 1: 身份验证 (Authentication)           │
│  - 验证API Key / OAuth Token               │
│  - 检查来源白名单                            │
└─────────────────┬───────────────────────────┘
                  │ 通过
                  ▼
┌─────────────────────────────────────────────┐
│  Step 2: 消毒处理 (Sanitization)             │
│  - 调用 security-gateway 检测注入           │
│  - 移除危险内容                              │
└─────────────────┬───────────────────────────┘
                  │ 安全
                  ▼
┌─────────────────────────────────────────────┐
│  Step 3: 协议转换 (Protocol Adaptation)      │
│  - 转换为内部信息素格式                       │
│  - 注入追踪ID                               │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
          发布到信息素总线
```

---

## 出站接口 (Egress Gateway)

### 支持的出站目标

| 目标 | 类型 | 用途 |
|------|------|------|
| n8n Webhook | HTTP POST | 触发n8n工作流 |
| 飞书机器人 | HTTP POST | 发送消息到飞书 |
| Slack Webhook | HTTP POST | 发送消息到Slack |
| Notion API | HTTP PATCH | 更新Notion页面 |
| Email (via n8n) | 间接 | 通过n8n发送邮件 |
| 文件系统 | File I/O | 保存到本地文件 |

### 出站消息标准格式

```yaml
egress_message:
  # 元数据
  message_id: "uuid"
  correlation_id: "关联的入站消息ID"
  timestamp: "ISO8601"
  
  # 目标配置
  target:
    type: "webhook|file|api"
    endpoint: "目标地址"
    method: "POST|PUT|PATCH"
    headers: {}
    
  # 负载
  payload:
    event_type: "task.completed|research.completed|..."
    content: "输出内容"
    metadata:
      source_unit: "Scholar-Unit"
      duration_ms: 1234
      
  # 安全选项
  security:
    pii_scrub: true  # 是否脱敏
    encrypt: false   # 是否加密
```

### 增强的信息素配置

```yaml
# 扩展的信息素定义，支持外部调度
pheromones:
  - on_event: "research.completed"
    from_unit: "Scholar-Unit"
    action:
      # 内部动作（原有）
      trigger_unit: "Creator-Unit"
      with_task: "Visualize the key findings"
      
      # 外部调度（新增）
      external_dispatch:
        enabled: true
        targets:
          - type: "webhook"
            name: "n8n-research-handler"
            url: "${N8N_WEBHOOK_URL}/research-completed"
            method: "POST"
            payload_map:
              report_content: "$last_output"
              author_agent: "$unit_name"
              timestamp: "$event_time"
              correlation_id: "$task_id"
            on_failure: "log_and_continue"  # 或 "retry" 或 "abort"
            
          - type: "feishu"
            name: "notify-team"
            channel: "${FEISHU_CHANNEL_ID}"
            message_template: |
              📚 研究报告完成
              单元：{{unit_name}}
              耗时：{{duration}}
              摘要：{{summary}}
```

---

## 协议适配层 (Protocol Adapter)

### 外部格式 → 内部信息素

```yaml
adapter_rules:
  # n8n → MindSymphony
  n8n_to_pheromone:
    input_format:
      body: "JSON from n8n webhook"
    transform:
      pheromone_id: "uuid()"
      source_unit: "External-Gateway"
      event_type: "external.request"
      payload:
        content: "$.body.message"
        context: "$.body.context"
        callback_url: "$.body.callback"
    output_format: "internal_pheromone"
    
  # 飞书 → MindSymphony
  feishu_to_pheromone:
    input_format:
      event: "Feishu event callback"
    transform:
      pheromone_id: "uuid()"
      source_unit: "External-Gateway"
      event_type: "external.feishu_message"
      payload:
        content: "$.event.message.content"
        user_id: "$.event.sender.sender_id"
        chat_id: "$.event.message.chat_id"
```

### 内部信息素 → 外部格式

```yaml
adapter_rules:
  # MindSymphony → n8n
  pheromone_to_n8n:
    input_format: "internal_pheromone"
    transform:
      status: "success"
      data:
        event: "$.event_type"
        content: "$.payload.content"
        metadata:
          source: "$.source_unit"
          timestamp: "$.timestamp"
    output_format: "JSON for n8n"
    
  # MindSymphony → 飞书
  pheromone_to_feishu:
    input_format: "internal_pheromone"
    transform:
      msg_type: "text"
      content:
        text: "$.payload.content"
    output_format: "Feishu message API"
```

---

## 安全策略

### 出站白名单

```yaml
egress_whitelist:
  # 只允许向以下域名发送数据
  allowed_domains:
    - "*.n8n.cloud"           # n8n官方云
    - "primary.n8n.webhook"   # 内部n8n实例
    - "open.feishu.cn"        # 飞书API
    - "hooks.slack.com"       # Slack Webhook
    - "api.notion.com"        # Notion API
    
  # 禁止向以下域名发送数据
  blocked_domains:
    - "*.pastebin.com"
    - "*.requestbin.com"
    - "*.ngrok.io"  # 除非明确配置
    
  # 未知域名处理
  unknown_domain_action: "block_and_log"
```

### PII脱敏规则

```yaml
pii_scrubbing:
  enabled: true
  patterns:
    - name: "email"
      regex: "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}"
      replacement: "[EMAIL_REDACTED]"
      
    - name: "phone_cn"
      regex: "1[3-9]\\d{9}"
      replacement: "[PHONE_REDACTED]"
      
    - name: "id_card_cn"
      regex: "\\d{17}[\\dXx]"
      replacement: "[ID_REDACTED]"
      
    - name: "api_key"
      regex: "sk-[a-zA-Z0-9]{32,}"
      replacement: "[API_KEY_REDACTED]"
```

---

## 与MindSymphony集成

### 新增工蜂单元：External-Gateway-Unit

```yaml
worker_units:
  - name: "External-Gateway-Unit"
    description: "负责外部通信的网关单元"
    souls:
      - "[M-08] 配置管家"      # 路由管理
      - "security-gateway"     # 安全检查
    capabilities:
      - "ingress_handling"
      - "egress_dispatch"
      - "protocol_adaptation"
    security_level: "elevated"
```

### 信息素订阅

```yaml
# External-Gateway-Unit 订阅所有需要外发的事件
pheromone_subscriptions:
  - event_pattern: "*.completed"
    subscriber: "External-Gateway-Unit"
    filter:
      has_external_dispatch: true
      
  - event_pattern: "*.failed"
    subscriber: "External-Gateway-Unit"
    filter:
      notify_external: true
```

---

## 环境变量配置

```bash
# n8n集成
N8N_WEBHOOK_URL=https://your-n8n-instance.com/webhook
N8N_API_KEY=your-api-key

# 飞书集成
FEISHU_APP_ID=cli_xxx
FEISHU_APP_SECRET=xxx
FEISHU_CHANNEL_ID=oc_xxx

# Slack集成
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/xxx

# 安全配置
EGRESS_WHITELIST_ENABLED=true
PII_SCRUBBING_ENABLED=true
```

---

## 使用示例

### 示例1：n8n触发研究任务

```
n8n工作流 → MindSymphony
─────────────────────────────

n8n发送：
POST /webhook/mindsymphony
{
  "intent": "task",
  "content": "研究2024年AI Agent发展趋势",
  "callback": "https://n8n.xxx/callback/123"
}

MindSymphony处理：
1. Ingress Gateway 接收
2. Security Gateway 检查
3. 转换为内部信息素
4. 路由到 Scholar-Unit
5. 执行研究任务
6. 完成后通过 Egress Gateway 回调n8n
```

### 示例2：研究完成通知飞书

```
research.completed → 飞书群
─────────────────────────────

配置：
pheromones:
  - on_event: "research.completed"
    action:
      external_dispatch:
        targets:
          - type: "feishu"
            channel: "oc_xxx"
            message_template: "📚 研究完成：{{summary}}"

效果：
研究完成后，自动发送消息到指定飞书群
```

---

## 信心赋予

**"蜂巢不再封闭，神经触及世界。"**

External Synapse 让MindSymphony从"数字孤岛"升级为"生态参与者"：
- 可以被n8n工作流触发
- 可以将结果推送到外部系统
- 可以与企业现有工具链集成

这是从"辅助思考工具"升级为"自动化业务引擎"的关键一步。
