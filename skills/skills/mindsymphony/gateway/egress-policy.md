---
name: egress-policy
layer: foundation
type: security
triggers: [出站, 白名单, 脱敏, 安全策略]
version: "19.1"
---

# 出站流量策略 (Egress Policy)

> 网关守卫：确保数据安全地流向外部世界。
> 解决测评报告指出的"安全开放外部接口"需求。

---

## 设计原则

```
测评报告原文：
"为了安全地开放外部接口，建议在gateway/目录下新增egress-policy.md，
定义出站流量规则。"

核心原则：
1. 默认拒绝 (Default Deny) - 未明确允许的出站全部阻止
2. 最小权限 (Least Privilege) - 只开放必要的出站能力
3. 数据脱敏 (Data Sanitization) - 敏感信息发送前必须处理
4. 完整审计 (Full Audit) - 所有出站请求记录日志
```

---

## 域名白名单

### 允许的出站域名

```yaml
whitelist:
  # ========== 自动化平台 ==========
  n8n:
    domains:
      - "*.n8n.cloud"           # n8n官方云
      - "n8n.internal.company"  # 企业内部实例
    purpose: "工作流自动化"
    data_level: "general"       # 可发送一般数据
    
  # ========== 即时通讯 ==========
  feishu:
    domains:
      - "open.feishu.cn"
      - "open.larksuite.com"
    purpose: "飞书消息推送"
    data_level: "general"
    require_pii_scrub: true     # 必须脱敏
    
  slack:
    domains:
      - "hooks.slack.com"
      - "api.slack.com"
    purpose: "Slack消息推送"
    data_level: "general"
    require_pii_scrub: true
    
  # ========== 知识管理 ==========
  notion:
    domains:
      - "api.notion.com"
    purpose: "Notion页面更新"
    data_level: "general"
    
  notebooklm:
    domains:
      - "notebooklm.google.com"
    purpose: "知识库查询"
    data_level: "query_only"    # 只允许查询，不发送敏感数据
    
  # ========== AI服务 ==========
  anthropic:
    domains:
      - "api.anthropic.com"
    purpose: "Claude API调用"
    data_level: "elevated"      # 可发送较敏感数据
    
  google_ai:
    domains:
      - "generativelanguage.googleapis.com"
    purpose: "Gemini API调用"
    data_level: "elevated"
```

### 黑名单（永久禁止）

```yaml
blacklist:
  # 数据泄露风险
  - "*.pastebin.com"
  - "*.hastebin.com"
  - "*.paste.ee"
  
  # 请求捕获服务
  - "*.requestbin.com"
  - "*.webhook.site"
  - "*.pipedream.net"
  
  # 临时隧道（除非明确配置）
  - "*.ngrok.io"
  - "*.localtunnel.me"
  - "*.serveo.net"
  
  # 文件共享
  - "*.dropbox.com"
  - "*.wetransfer.com"
  
  # 社交媒体API（需要单独审批）
  - "api.twitter.com"
  - "graph.facebook.com"
```

---

## 数据分级

### 数据敏感度等级

| 等级 | 名称 | 示例 | 出站限制 |
|------|------|------|----------|
| L0 | 公开 | 天气、新闻、通用知识 | 无限制 |
| L1 | 内部 | 工作文档、会议记录 | 需要白名单 |
| L2 | 敏感 | 客户信息、财务数据 | 白名单+脱敏 |
| L3 | 机密 | 密码、API Key、个人身份 | 禁止出站 |

### 自动检测规则

```yaml
data_classification:
  L3_patterns:  # 机密 - 禁止出站
    - name: "api_key"
      pattern: "(sk-|api[_-]?key|apikey)[a-zA-Z0-9]{20,}"
      action: "block"
      
    - name: "password"
      pattern: "(password|passwd|pwd)\\s*[:=]\\s*\\S+"
      action: "block"
      
    - name: "private_key"
      pattern: "-----BEGIN (RSA |EC |)PRIVATE KEY-----"
      action: "block"
      
  L2_patterns:  # 敏感 - 需要脱敏
    - name: "email"
      pattern: "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}"
      action: "redact"
      replacement: "[EMAIL]"
      
    - name: "phone_cn"
      pattern: "1[3-9]\\d{9}"
      action: "redact"
      replacement: "[PHONE]"
      
    - name: "id_card_cn"
      pattern: "\\d{6}(19|20)\\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\\d|3[01])\\d{3}[\\dXx]"
      action: "redact"
      replacement: "[ID_CARD]"
      
    - name: "bank_card"
      pattern: "\\d{16,19}"
      action: "redact"
      replacement: "[BANK_CARD]"
```

---

## 出站请求处理流程

```
出站请求发起
    │
    ▼
┌─────────────────────────────────────────────┐
│  Step 1: 目标检查                            │
│  - 解析目标域名                              │
│  - 检查白名单/黑名单                         │
│  - 黑名单 → 立即阻止                         │
│  - 非白名单 → 默认阻止                       │
└─────────────────┬───────────────────────────┘
                  │ 白名单通过
                  ▼
┌─────────────────────────────────────────────┐
│  Step 2: 数据分类                            │
│  - 扫描请求体                                │
│  - 识别数据敏感度                            │
│  - L3数据 → 阻止并告警                       │
└─────────────────┬───────────────────────────┘
                  │ 无L3数据
                  ▼
┌─────────────────────────────────────────────┐
│  Step 3: 数据脱敏                            │
│  - 如果目标要求脱敏                          │
│  - 处理L2数据（替换为占位符）                 │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│  Step 4: 审计记录                            │
│  - 记录时间戳、目标、数据摘要                 │
│  - 不记录完整请求体（隐私保护）               │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
              执行出站请求
```

---

## 审计日志格式

```yaml
egress_audit_log:
  timestamp: "2026-01-05T12:00:00Z"
  request_id: "uuid"
  
  # 来源
  source:
    unit: "Scholar-Unit"
    event: "research.completed"
    correlation_id: "task-uuid"
    
  # 目标
  target:
    domain: "open.feishu.cn"
    path: "/open-apis/bot/v2/hook/xxx"
    method: "POST"
    
  # 安全处理
  security:
    whitelist_matched: "feishu"
    data_level_detected: "L1"
    pii_scrubbed: true
    patterns_redacted: ["email", "phone_cn"]
    
  # 结果
  result:
    status: "success"
    http_code: 200
    latency_ms: 234
```

---

## 异常处理

### 阻止场景

| 场景 | 原因 | 处理 |
|------|------|------|
| 目标在黑名单 | 安全风险 | 阻止+告警 |
| 目标不在白名单 | 默认拒绝 | 阻止+记录 |
| 检测到L3数据 | 机密泄露风险 | 阻止+告警+通知 |
| 脱敏失败 | 处理异常 | 阻止+重试 |

### 告警配置

```yaml
alerts:
  l3_data_detected:
    severity: "critical"
    channels: ["log", "feishu"]
    message: "⚠️ 检测到机密数据尝试出站！请求已阻止。"
    
  blacklist_hit:
    severity: "high"
    channels: ["log"]
    message: "🚫 尝试向黑名单域名发送数据"
    
  repeated_blocks:
    severity: "medium"
    threshold: 5  # 5分钟内5次
    channels: ["log", "feishu"]
    message: "⚠️ 重复的出站阻止，可能存在配置问题"
```

---

## 配置示例

### 企业环境配置

```yaml
# egress-policy.yml
environment: "production"

defaults:
  allow_unknown_domains: false
  require_pii_scrub: true
  log_level: "info"
  
whitelist_overrides:
  # 添加企业内部服务
  - domain: "api.internal.company.com"
    purpose: "内部API"
    data_level: "elevated"
    
rate_limits:
  # 防止滥用
  per_domain:
    default: "100/hour"
    "open.feishu.cn": "50/hour"
    
  per_unit:
    default: "200/hour"
```

### 开发环境配置

```yaml
# egress-policy.dev.yml
environment: "development"

defaults:
  allow_unknown_domains: false  # 即使开发也要白名单
  require_pii_scrub: true       # 始终脱敏
  log_level: "debug"
  
whitelist_overrides:
  # 开发环境允许localhost
  - domain: "localhost:*"
    purpose: "本地测试"
    data_level: "general"
    
  # 允许ngrok用于测试
  - domain: "*.ngrok.io"
    purpose: "开发隧道"
    data_level: "general"
    require_approval: true  # 每次需要确认
```

---

## 与External Synapse集成

```yaml
# 在external-synapse中引用egress-policy
external_dispatch:
  pre_dispatch_hooks:
    - "egress-policy:check_whitelist"
    - "egress-policy:classify_data"
    - "egress-policy:scrub_pii"
    - "egress-policy:audit_log"
    
  on_block:
    action: "log_and_notify"
    fallback: "queue_for_review"  # 可选：排队等待人工审核
```

---

## 信心赋予

**"开放但不裸露，连接但有边界。"**

Egress Policy确保MindSymphony在与外部世界通信时：
- 只向可信目标发送数据
- 敏感信息得到保护
- 所有行为可追溯
- 异常及时告警

这是"安全开放"而非"盲目开放"的关键保障。
