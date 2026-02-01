---
name: intent-router
layer: foundation
type: system
triggers: [路由, 调度, 分发, 选择skill]
---

# 意图路由器 (Intent Router)

> 轻量级路由层，用规则和关键词匹配优先，减少LLM路由开销。
> 解决批评指出的"信息素通信延迟"问题。

---

## 设计原则

```
批评原文：
"每一次'信息素广播'实际上都是一次LLM推理"
"一个简单的'A做完给B'的动作，可能有10秒+的纯延迟"

解决方案：
分层路由 = 规则优先 + 关键词匹配 + LLM兜底

Layer 1: 硬编码规则（0延迟）
Layer 2: 关键词匹配（<100ms）
Layer 3: LLM语义理解（仅复杂场景）
```

---

## 路由架构

```
用户输入
    │
    ▼
┌─────────────────────────────────────────────┐
│  Layer 1: 规则路由（硬编码，0延迟）           │
│  - 文件扩展名 → 对应处理器                    │
│  - 命令前缀 → 对应skill                      │
│  - 上下文继承 → 继续当前skill                 │
└─────────────────┬───────────────────────────┘
                  │ 未匹配
                  ▼
┌─────────────────────────────────────────────┐
│  Layer 2: 关键词路由（registry匹配，<100ms）  │
│  - 扫描triggers列表                          │
│  - 计算匹配度分数                            │
│  - 返回Top-1或Top-3候选                      │
└─────────────────┬───────────────────────────┘
                  │ 低置信度 或 多候选
                  ▼
┌─────────────────────────────────────────────┐
│  Layer 3: LLM语义路由（复杂场景兜底）         │
│  - 仅当Layer 1&2失败时触发                   │
│  - 使用轻量prompt进行意图分类                 │
└─────────────────────────────────────────────┘
```

---

## Layer 1: 规则路由

### 文件扩展名规则

| 扩展名 | 目标Skill |
|--------|-----------|
| .docx, .doc | docx |
| .pdf | pdf |
| .pptx, .ppt | pptx |
| .xlsx, .xls, .csv | xlsx |
| .py, .js, .ts | code-analysis |
| .json, .yml, .yaml | config-validation |
| .md | knowledge-explorer |

### 命令前缀规则

| 前缀 | 目标Skill |
|------|-----------|
| /plan | plan-first |
| /verify | verification-loop |
| /skill | skill-curator |
| /create-skill | skill-forge |
| /academic | academic-forge |
| /agent | ai-agent-architect |
| /gemini | gemini-cli-integration |

### 上下文继承

如果用户说"继续"、"然后呢"、"下一步"，则继承上一轮使用的skill。

---

## Layer 2: 关键词路由

### 匹配算法

1. 从registry.yml加载所有skill的triggers
2. 计算用户输入与每个trigger的匹配度
3. 返回得分最高的1-3个候选

### 决策阈值

| 条件 | 动作 |
|------|------|
| Top-1 得分 ≥ 50 | 直接路由 |
| Top-1 得分 ≥ 30 且 Top-2 < 20 | 路由到Top-1 |
| Top-1 与 Top-2 差距 < 10 | 请求用户澄清 |
| 无匹配 | 进入Layer 3 |

---

## Layer 3: LLM语义路由

### 触发条件

- Layer 1&2 均无匹配
- 多个高分候选需要消歧
- 用户输入高度抽象

### 轻量Prompt

```
用户意图："{user_input}"
候选技能：{candidates}
请选择最匹配的技能，输出skill_id即可。
```

---

## 性能目标

| 路由层 | 延迟 | 准确率 |
|--------|------|--------|
| L1 规则 | <10ms | 100% |
| L2 关键词 | <100ms | >85% |
| L3 LLM | <3s | >95% |

---

## 兜底机制

如果所有路由层都失败，默认路由到 `cognitive-architect`（蜂后），由它进行任务分解和技能分配。
