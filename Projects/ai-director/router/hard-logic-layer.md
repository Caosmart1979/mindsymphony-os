---
name: hard-logic-layer
layer: foundation
type: system
triggers: [模板, 预设, 硬编码, 确定性]
---

# Hard Logic层 (Hard Logic Layer)

> 将确定性逻辑从Prompt中分离，用预设模板+参数化调用替代直接生成。
> 解决批评指出的"概率性大脑与确定性世界的阻抗不匹配"问题。

---

## 设计原则

```
批评原文：
"n8n的JSON结构非常严格。Claude作为一个概率模型，
哪怕多写了一个逗号，整个自动化链路就会直接崩塌。"

"系统缺乏一个'中间编译层'。直接用Prompt生成复杂的
执行逻辑（如n8n workflow JSON）是极其脆弱的。"

解决方案：
Hard Logic = 预设模板 + 参数提取 + 模板填充 + 格式验证

Prompt的职责：理解意图 → 提取参数
Hard Logic的职责：参数 → 确定性输出
```

---

## 架构

```
用户请求
    │
    ▼
┌─────────────────────────────────────────────┐
│  LLM层：理解意图，提取参数                    │
│  输入："创建一个每天9点发飞书消息的工作流"      │
│  输出：{                                     │
│    "template": "scheduled_feishu_message",  │
│    "params": {                              │
│      "cron": "0 9 * * *",                   │
│      "channel": "default",                  │
│      "message": "..."                       │
│    }                                        │
│  }                                          │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│  Hard Logic层：模板填充，格式验证             │
│  - 加载预设模板                              │
│  - 填充参数                                  │
│  - 验证JSON格式                              │
│  - 输出确定性结果                            │
└─────────────────────────────────────────────┘
                  │
                  ▼
              确定性输出
```

---

## 模板库

### n8n工作流模板

```yaml
templates:
  n8n:
    scheduled_feishu_message:
      description: "定时发送飞书消息"
      params:
        - name: cron
          type: string
          required: true
          validation: cron_expression
        - name: channel
          type: string
          required: true
        - name: message
          type: string
          required: true
      template_file: templates/n8n/scheduled_feishu.json
      
    webhook_to_feishu:
      description: "Webhook触发发送飞书"
      params:
        - name: webhook_path
          type: string
          required: true
        - name: channel
          type: string
          required: true
      template_file: templates/n8n/webhook_feishu.json
      
    data_sync:
      description: "数据同步工作流"
      params:
        - name: source
          type: enum
          options: [mysql, postgres, api]
          required: true
        - name: destination
          type: enum
          options: [feishu_sheet, google_sheet]
          required: true
        - name: schedule
          type: string
          required: false
      template_file: templates/n8n/data_sync.json
```

### 文档模板

```yaml
templates:
  documents:
    research_report:
      description: "研究报告模板"
      params:
        - name: title
          type: string
          required: true
        - name: sections
          type: array
          required: true
        - name: style
          type: enum
          options: [academic, business, casual]
          default: academic
      template_file: templates/docs/research_report.md
      
    weekly_report:
      description: "周报模板"
      params:
        - name: period
          type: string
          required: true
        - name: accomplishments
          type: array
          required: true
        - name: plans
          type: array
          required: true
        - name: blockers
          type: array
          required: false
      template_file: templates/docs/weekly_report.md
```

---

## 参数提取Prompt

### 设计原则

```yaml
param_extraction_principles:
  - 明确输出格式为JSON
  - 列出所有可能的参数
  - 提供参数类型和约束
  - 失败时返回null而非猜测
```

### 通用模板

```markdown
## 任务：参数提取

用户请求："{user_input}"

### 目标模板
{template_name}: {template_description}

### 需要提取的参数
{param_definitions}

### 输出格式
```json
{
  "template": "{template_name}",
  "params": {
    "param1": "value1",
    "param2": "value2"
  },
  "confidence": "high|medium|low",
  "missing_params": ["param_name"]  // 如果有必需参数无法提取
}
```

### 注意
- 如果无法确定参数值，设为null
- 如果缺少必需参数，列在missing_params中
- 不要猜测，不确定就标注
```

---

## 格式验证

### JSON验证

```yaml
json_validation:
  steps:
    - parse: "尝试解析JSON"
    - schema: "对照schema验证结构"
    - type: "验证字段类型"
    - constraint: "验证约束条件"
    
  on_failure:
    - log_error: true
    - return_template_error: true
    - suggest_fix: true
```

### 常见验证规则

```yaml
validation_rules:
  cron_expression:
    pattern: "^[\\d\\*\\-\\/,]+\\s+[\\d\\*\\-\\/,]+\\s+[\\d\\*\\-\\/,]+\\s+[\\d\\*\\-\\/,]+\\s+[\\d\\*\\-\\/,]+$"
    
  email:
    pattern: "^[^@]+@[^@]+\\.[^@]+$"
    
  url:
    pattern: "^https?://.+"
    
  feishu_channel:
    pattern: "^oc_[a-z0-9]+$"
```

---

## 示例：n8n工作流创建

### 传统方式（脆弱）

```
用户：创建一个每天早上9点发飞书消息的工作流

Claude直接生成：
{
  "nodes": [
    {
      "type": "n8n-nodes-base.cron",
      "parameters": {
        "cronExpression": "0 9 * * *"  // 可能格式错误
      }
    },
    // ...更多节点，每个都可能出错
  ]
}

问题：JSON任何位置的错误都会导致整个工作流失败
```

### Hard Logic方式（稳健）

```
用户：创建一个每天早上9点发飞书消息的工作流

Step 1: LLM参数提取
{
  "template": "scheduled_feishu_message",
  "params": {
    "cron": "0 9 * * *",
    "channel": "default",
    "message": "早安！新的一天开始了。"
  },
  "confidence": "high"
}

Step 2: Hard Logic填充模板
- 加载 templates/n8n/scheduled_feishu.json
- 用params替换占位符
- 验证JSON格式
- 输出确定性结果

优势：模板经过验证，只有参数可变，大大降低出错概率
```

---

## 模板管理

### 目录结构

```
mindsymphony/
└── templates/
    ├── n8n/
    │   ├── scheduled_feishu.json
    │   ├── webhook_feishu.json
    │   └── data_sync.json
    ├── docs/
    │   ├── research_report.md
    │   └── weekly_report.md
    └── api/
        ├── feishu_message.json
        └── slack_message.json
```

### 模板示例

```json
// templates/n8n/scheduled_feishu.json
{
  "name": "Scheduled Feishu Message",
  "nodes": [
    {
      "id": "cron_1",
      "type": "n8n-nodes-base.cron",
      "parameters": {
        "cronExpression": "{{cron}}"
      },
      "position": [250, 300]
    },
    {
      "id": "feishu_1",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "https://open.feishu.cn/open-apis/bot/v2/hook/{{channel}}",
        "method": "POST",
        "body": {
          "msg_type": "text",
          "content": {
            "text": "{{message}}"
          }
        }
      },
      "position": [450, 300]
    }
  ],
  "connections": {
    "cron_1": {
      "main": [[{"node": "feishu_1", "type": "main", "index": 0}]]
    }
  }
}
```

---

## 与MindSymphony集成

### 职责分工

```
┌─────────────────────────────────────────────┐
│  Skill层（Prompt）                          │
│  - 理解用户意图                              │
│  - 选择合适的模板                            │
│  - 提取参数                                  │
│  - 处理模糊性和歧义                          │
└─────────────────┬───────────────────────────┘
                  │ 参数化请求
                  ▼
┌─────────────────────────────────────────────┐
│  Hard Logic层                               │
│  - 模板管理                                  │
│  - 参数填充                                  │
│  - 格式验证                                  │
│  - 确定性输出                                │
└─────────────────────────────────────────────┘
```

### 调用方式

```yaml
# 在Skill中调用Hard Logic
hard_logic_call:
  action: "apply_template"
  template: "n8n/scheduled_feishu_message"
  params:
    cron: "0 9 * * *"
    channel: "oc_xxx"
    message: "早安"
  validate: true
  on_error: "return_to_user"
```

---

## 信心赋予

**"让Prompt做Prompt擅长的，让代码做代码擅长的。"**

- Prompt擅长：理解自然语言、处理模糊性、推理意图
- 代码擅长：格式化、验证、确定性输出

Hard Logic层不是要取代Prompt，而是要让两者各司其职：
- Prompt负责"理解"
- Hard Logic负责"执行"

这是从"概率性脆弱"升级为"确定性稳健"的关键一步。
