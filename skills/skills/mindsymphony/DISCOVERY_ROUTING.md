# 技能发现与智能路由系统

## 概述

基于INTEROP.yml的技能发现与智能路由系统,实现自动化技能选择和A/B测试能力。

## 架构设计

```
用户输入
    ↓
[1] 关键词匹配 (INTEROP.yml discovery.routing_patterns)
    ↓
[2] 置信度计算 (pattern confidence scores)
    ↓
[3] 技能排序 (by priority + confidence)
    ↓
[4] A/B测试分支 (ab_testing.variants)
    ↓
[5] 执行技能
    ↓
[6] 性能记录 (performance metrics)
```

## 核心组件

### 1. 发现引擎 (Discovery Engine)

每个技能的INTEROP.yml包含:
```yaml
discovery:
  auto_route: true
  confidence_threshold: 0.7
  routing_patterns:
    - pattern: "regex_pattern"
      confidence: 0.8
  related_skills: []
```

### 2. A/B测试框架

```yaml
ab_testing:
  enabled: true
  variants:
    - name: "variant_a"
      weight: 0.5
  metrics: ["success_rate", "execution_time", "user_satisfaction"]
```

## Top 20核心技能路由表

| 技能 | 优先级 | 核心Patterns | 置信度 |
|------|--------|-------------|--------|
| mindsymphony | critical | orchestrat|coordinat|complex task | 0.9 |
| skill-creator | critical | create skill|skill development | 0.95 |
| cognitive-architect | high | cognitive|architecture|thinking | 0.85 |
| frontend-design | high | frontend|ui|web|react|vue | 0.9 |
| doc-coauthoring | high | documentation|docs|technical writing | 0.9 |
| docx | medium | docx|word|document | 0.9 |
| pdf | medium | pdf|extract pdf|pdf form | 0.95 |
| pptx | medium | pptx|presentation|slides | 0.95 |
| mcp-builder | high | mcp|mcp server|integration | 0.95 |
| api-integration-designer | medium | api|rest|graphql|webhook | 0.9 |
| code-refactoring-expert | medium | refactor|clean up|technical debt | 0.9 |
| database-schema-architect | medium | database|schema|sql|nosql | 0.9 |
| devops-workflow-designer | medium | devops|cicd|pipeline | 0.9 |
| gemini-cli-integration | medium | gemini|multimodal|video|audio | 0.9 |
| brand-guidelines | medium | brand|branding|guidelines | 0.9 |
| canvas-design | medium | poster|art|design|canvas | 0.9 |
| algorithmic-art | low | algorithmic art|generative art|p5.js | 0.95 |
| theme-factory | low | theme|color scheme|design system | 0.85 |
| internal-comms | medium | internal comms|status report|update | 0.9 |
| knowledge-explorer | medium | research|explore|knowledge | 0.85 |

## 使用示例

用户输入: "帮我创建一个react组件,设计风格要大胆前卫"

发现流程:
1. frontend-design: 0.8 × 0.8 = 0.64
2. brand-guidelines: 0.85 × 0.6 = 0.51
→ 选择frontend-design
