# MiroThinker × MindSymphony 集成方案

**版本**: 21.0.0-evolution
**日期**: 2025-01-11
**架构**: API + Skill 双层集成

---

## 🎯 集成架构总览

```
┌─────────────────────────────────────────────────────────────────┐
│              MiroThinker × MindSymphony 集成架构                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │           用户交互层 (User Interface)                    │   │
│  │                                                         │   │
│  │  自然语言 | CLI | API                                     │   │
│  └────────────────────┬────────────────────────────────────┘   │
│                       │                                        │
│  ┌────────────────────▼────────────────────────────────────┐   │
│  │         MindSymphony v21.0 (智能路由层)                  │   │
│  │                                                         │   │
│  │  ┌─────────────────────────────────────────────────┐   │   │
│  │  │ 统一触发层 (Unified Triggers)                    │   │   │
│  │  │  • 命令: /miro, /research                        │   │   │
│  │  │  • 语义: "深度分析这篇论文"                       │   │   │
│  │  │  • 模式: "文献综述", "深度推理"                   │   │   │
│  │  └─────────────────────────────────────────────────┘   │   │
│  │                         │                                │   │
│  │  ┌──────────────────────▼──────────────────────────┐   │   │
│  │  │ 智能路由 (Intelligent Router)                    │   │   │
│  │  │  • 需要深度推理? → MiroThinker                   │   │   │
│  │  │  • 需要长文档? → MiroThinker                     │   │   │
│  │  │  • 需要协作? → Skills + n8n                      │   │   │
│  │  └─────────────────────────────────────────────────┘   │   │
│  └────────────────────┬────────────────────────────────────┘   │
│                       │                                        │
│  ┌────────────────────▼────────────────────────────────────┐   │
│  │          集成层 (Integration Layer)                      │   │
│  │                                                          │   │
│  │  ┌──────────────────────────────────────────────────┐   │   │
│  │  │ 方案 1: MCP 服务器 (推荐)                          │   │   │
│  │  │  • mcp-mirothinker-server                         │   │   │
│  │  │  • 标准化接口                                     │   │   │
│  │  │  • 双向通信                                       │   │   │
│  │  └──────────────────────────────────────────────────┘   │   │
│  │                                                         │   │
│  │  ┌──────────────────────────────────────────────────┐   │   │
│  │  │ 方案 2: Skill 封装                                 │   │   │
│  │  │  • miro-researcher.skill                          │   │   │
│  │  │  • 统一技能接口                                   │   │   │
│  │  │  • 可进化优化                                     │   │   │
│  │  └──────────────────────────────────────────────────┘   │   │
│  │                                                         │   │
│  │  ┌──────────────────────────────────────────────────┐   │   │
│  │  │ 方案 3: 直接 API 调用                              │   │   │
│  │  │  • REST API                                       │   │   │
│  │  │  • 快速响应                                       │   │   │
│  │  │  • 简单直接                                       │   │   │
│  │  └──────────────────────────────────────────────────┘   │   │
│  └────────────────────┬────────────────────────────────────┘   │
│                       │                                        │
│  ┌────────────────────▼────────────────────────────────────┐   │
│  │          MiroThinker 服务层                              │   │
│  │                                                          │   │
│  │  • MiroEngine (推理引擎)                                 │   │
│  │  • ThoughtChain (思维链)                                 │   │
│  │  • Pure RAG (零向量DB)                                   │   │
│  │  • ContextManager (长上下文)                              │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 方案 1: MCP 服务器集成（推荐）

### 架构设计

```yaml
# MCP 服务器配置
mcp_mirothinker_server:
  name: "mcp-mirothinker"
  version: "1.0.0"
  description: "MiroThinker MCP Server for MindSymphony"

  # 服务器配置
  server:
    type: "python"
    host: "localhost"
    port: 3001
    endpoint: "/mcp"

  # 可用工具
  tools:
    # 1. 深度推理
    - name: "deep_reasoning"
      description: "使用思维链进行深度推理"
      parameters:
        - name: "query"
          type: "string"
          required: true
        - name: "documents"
          type: "array"
          required: false
        - name: "reasoning_depth"
          type: "integer"
          default: 3

    # 2. 长文档分析
    - name: "analyze_document"
      description: "深度分析长文档"
      parameters:
        - name: "document_path"
          type: "string"
          required: true
        - name: "analysis_type"
          type: "string"
          enum: ["summary", "extraction", "analysis"]
        - name: "output_format"
          type: "string"
          default: "structured"

    # 3. 纯 RAG 查询
    - name: "pure_rag_query"
      description: "无向量数据库的 RAG 查询"
      parameters:
        - name: "query"
          type: "string"
          required: true
        - name: "documents"
          type: "array"
          required: true
        - name: "top_k"
          type: "integer"
          default: 5

    # 4. 思维链生成
    - name: "generate_thought_chain"
      description: "生成结构化思维链"
      parameters:
        - name: "problem"
          type: "string"
          required: true
        - name: "chain_type"
          type: "string"
          enum: ["linear", "tree", "graph"]
```

### MCP 服务器实现

```python
# mcp_mirothinker_server.py
"""
MiroThinker MCP Server
为 MindSymphony 提供深度推理能力
"""

from mcp.server import Server
from mirothinker import MiroEngine, ThoughtChain, PureRAG
import asyncio

app = Server("mcp-mirothinker")

# 初始化 MiroThinker 引擎
miro_engine = MiroEngine()
thought_chain = ThoughtChain()
pure_rag = PureRAG()

@app.tool("deep_reasoning")
async def deep_reasoning(
    query: str,
    documents: list = None,
    reasoning_depth: int = 3
) -> dict:
    """
    使用思维链进行深度推理

    Args:
        query: 用户查询
        documents: 相关文档（可选）
        reasoning_depth: 推理深度（默认3）

    Returns:
        推理结果和思维链
    """
    # 构建思维链
    chain = thought_chain.build(
        query=query,
        documents=documents,
        depth=reasoning_depth
    )

    # 执行深度推理
    result = await miro_engine.reason_async(
        query=query,
        chain=chain
    )

    return {
        "answer": result.answer,
        "thought_chain": result.chain,
        "confidence": result.confidence,
        "sources": result.sources
    }

@app.tool("analyze_document")
async def analyze_document(
    document_path: str,
    analysis_type: str = "analysis",
    output_format: str = "structured"
) -> dict:
    """
    深度分析文档

    Args:
        document_path: 文档路径
        analysis_type: 分析类型
        output_format: 输出格式

    Returns:
        结构化分析结果
    """
    result = await miro_engine.analyze_document_async(
        path=document_path,
        analysis_type=analysis_type
    )

    return {
        "summary": result.summary,
        "key_points": result.key_points,
        "insights": result.insights,
        "metadata": result.metadata
    }

@app.tool("pure_rag_query")
async def pure_rag_query(
    query: str,
    documents: list,
    top_k: int = 5
) -> dict:
    """
    无向量数据库的 RAG 查询

    Args:
        query: 查询问题
        documents: 文档列表
        top_k: 返回结果数量

    Returns:
        RAG 查询结果
    """
    # 使用纯 RAG（无需向量数据库）
    results = await pure_rag.query_async(
        query=query,
        documents=documents,
        top_k=top_k
    )

    return {
        "answer": results.answer,
        "relevant_chunks": results.chunks,
        "confidence_scores": results.scores
    }

@app.tool("generate_thought_chain")
async def generate_thought_chain(
    problem: str,
    chain_type: str = "linear"
) -> dict:
    """
    生成结构化思维链

    Args:
        problem: 待解决问题
        chain_type: 思维链类型

    Returns:
        结构化思维链
    """
    chain = await thought_chain.generate_async(
        problem=problem,
        chain_type=chain_type
    )

    return {
        "steps": chain.steps,
        "logic_flow": chain.logic_flow,
        "decision_points": chain.decisions
    }

# 启动服务器
if __name__ == "__main__":
    app.run(port=3001)
```

### MindSymphony 配置集成

```yaml
# mindsymphony.config.yml 添加
mcp:
  servers:
    # ... 其他 MCP 服务器

    # MiroThinker MCP 服务器
    mcp-mirothinker:
      description: "深度推理和长文档分析"
      enabled: true
      endpoint: "http://localhost:3001/mcp"
      capabilities:
        - "deep_reasoning"
        - "document_analysis"
        - "pure_rag"
        - "thought_chain"

# 统一触发器配置
unified_triggers:
  skill_triggers:
    # MiroThinker 深度推理技能
    - skill: "mcp-mirothinker/deep_reasoning"
      priority: "high"
      category: "reasoning"

      triggers:
        - type: "command"
          patterns: ["/miro", "/深度推理", "/deep"]
          weight: 10.0

        - type: "semantic"
          intent: "deep_reasoning"
          keywords: ["深度分析", "推理", "思维链"]
          examples:
            - "深度分析这个问题"
            - "用思维链推理"
            - "给我详细的推理过程"
          weight: 8.0

        - type: "pattern"
          regex: "深度.*推理|思维链|详细.*分析"
          weight: 6.0

    # MiroThinker 文档分析技能
    - skill: "mcp-mirothinker/analyze_document"
      priority: "high"
      category: "analysis"

      triggers:
        - type: "command"
          patterns: ["/文档分析", "/doc_analyze"]
          weight: 10.0

        - type: "semantic"
          intent: "document_analysis"
          examples:
            - "深度分析这篇论文"
            - "提取文档关键信息"
            - "生成文档摘要"
          weight: 8.0

    # MiroThinker 纯 RAG 技能
    - skill: "mcp-mirothinker/pure_rag_query"
      priority: "medium"
      category: "retrieval"

      triggers:
        - type: "semantic"
          intent: "pure_rag_query"
          examples:
            - "查询这些文档"
            - "不用向量库搜索"
          weight: 7.0
```

---

## 方案 2: Skill 封装

### Skill 文件结构

```
mindsymphony-v15.6/skills/
└── mirothinker-integration/
    ├── SKILL.md
    ├── skill.yml
    ├── README.md
    └── examples/
        ├── basic_usage.md
        ├── advanced_usage.md
        └── integration_patterns.md
```

### SKILL.md

```markdown
# MiroThinker 深度推理技能

## 技能概述

本技能将 MiroThinker 的深度推理能力集成到 MindSymphony 中，
提供无向量数据库的 RAG、思维链推理、长文档分析等功能。

## 核心能力

1. **深度推理** (Deep Reasoning)
   - 思维链推理
   - 多步逻辑推导
   - 可解释的推理过程

2. **纯 RAG** (Pure RAG)
   - 无需向量数据库
   - 智能文档匹配
   - 上下文感知

3. **长文档分析** (Long Document Analysis)
   - 超长文档处理
   - 关键信息提取
   - 结构化摘要

4. **思维链生成** (Thought Chain Generation)
   - 问题分解
   - 逻辑流程
   - 决策点识别

## 使用方式

### 命令触发
```
/miro 深度分析这个问题
/文档分析 分析这篇论文
/推理 用思维链推理
```

### 语义触发
```
"深度分析这个研究问题"
"用思维链帮我推理"
"详细分析这篇长文档"
```

## 与其他技能的协作

- 与 `scientific-writing` 协作：深度分析文献
- 与 `literature-review` 协作：智能文献综述
- 与 `knowledge-explorer` 协作：深度知识探索

## 配置要求

- Python 3.10+
- MiroThinker 安装
- MCP 服务器运行（可选）
```

### skill.yml

```yaml
name: "mirothinker-integration"
version: "1.0.0"
description: "MiroThinker 深度推理集成技能"
author: "MindSymphony"
category: "reasoning"

# 依赖
dependencies:
  python:
    - "mirothinker>=0.2.0"
    - "langchain>=0.1.0"

  mcp_servers:
    - "mcp-mirothinker"

# 技能配置
config:
  # 默认推理深度
  default_reasoning_depth: 3

  # 文档大小限制
  max_document_size: "100MB"

  # 输出格式
  default_output_format: "structured"

# 触发器
triggers:
  - type: "command"
    patterns: ["/miro", "/深度推理"]

  - type: "semantic"
    intent: "deep_reasoning"

# 协作
collaboration:
  works_with:
    - "scientific-writing"
    - "literature-review"
    - "knowledge-explorer"
```

---

## 方案 3: 直接 API 调用

### Python API 封装

```python
# mirothinker_api.py
"""
MiroThinker API 封装
供 MindSymphony 直接调用
"""

import requests
from typing import List, Dict, Any

class MiroThinkerAPI:
    """MiroThinker API 客户端"""

    def __init__(self, base_url: str = "http://localhost:3001"):
        self.base_url = base_url

    def deep_reasoning(
        self,
        query: str,
        documents: List[str] = None,
        reasoning_depth: int = 3
    ) -> Dict[str, Any]:
        """
        深度推理

        Args:
            query: 查询问题
            documents: 文档列表
            reasoning_depth: 推理深度

        Returns:
            推理结果
        """
        response = requests.post(
            f"{self.base_url}/api/reasoning",
            json={
                "query": query,
                "documents": documents,
                "depth": reasoning_depth
            }
        )
        return response.json()

    def analyze_document(
        self,
        document_path: str,
        analysis_type: str = "analysis"
    ) -> Dict[str, Any]:
        """
        文档分析

        Args:
            document_path: 文档路径
            analysis_type: 分析类型

        Returns:
            分析结果
        """
        response = requests.post(
            f"{self.base_url}/api/analyze",
            json={
                "document": document_path,
                "type": analysis_type
            }
        )
        return response.json()

    def pure_rag(
        self,
        query: str,
        documents: List[str],
        top_k: int = 5
    ) -> Dict[str, Any]:
        """
        纯 RAG 查询

        Args:
            query: 查询
            documents: 文档列表
            top_k: 返回数量

        Returns:
            RAG 结果
        """
        response = requests.post(
            f"{self.base_url}/api/rag",
            json={
                "query": query,
                "documents": documents,
                "top_k": top_k
            }
        )
        return response.json()

# 在 MindSymphony 中使用
from mirothinker_api import MiroThinkerAPI

# 初始化客户端
miro_api = MiroThinkerAPI()

# 深度推理
result = miro_api.deep_reasoning(
    query="分析这个研究的核心贡献",
    reasoning_depth=5
)

print(result["answer"])
print(result["thought_chain"])
```

---

## 使用示例

### 示例 1: 深度文献分析

```yaml
# 工作流：文献深度分析
workflow:
  name: "深度文献分析"

  steps:
    # Step 1: 使用 MiroThinker 深度分析
    - tool: "mcp-mirothinker/analyze_document"
      input:
        document: "research_paper.pdf"
        analysis_type: "deep"
      output: "analysis_result"

    # Step 2: 生成文献综述
    - skill: "literature-review"
      input:
        analysis: "{{analysis_result}}"
      output: "review_draft"

    # Step 3: 写作润色
    - skill: "scientific-writing"
      input:
        draft: "{{review_draft}}"
      output: "final_review"
```

### 示例 2: 思维链推理

```yaml
# 工作流：复杂问题推理
workflow:
  name: "思维链推理"

  steps:
    # Step 1: 生成思维链
    - tool: "mcp-mirothinker/generate_thought_chain"
      input:
        problem: "如何提高深度学习模型的泛化能力？"
        chain_type: "tree"
      output: "thought_chain"

    # Step 2: 执行深度推理
    - tool: "mcp-mirothinker/deep_reasoning"
      input:
        query: "{{problem}}"
        reasoning_chain: "{{thought_chain}}"
      output: "reasoning_result"

    # Step 3: 综合答案
    - skill: "scientific-writing"
      input:
        reasoning: "{{reasoning_result}}"
      output: "final_answer"
```

### 示例 3: 纯 RAG 文档检索

```yaml
# 工作流：无向量库的智能检索
workflow:
  name: "纯 RAG 检索"

  steps:
    # Step 1: 收集文档
    - tool: "filesystem"
      action: "read_documents"
      input:
        path: "./documents/"
      output: "documents"

    # Step 2: 纯 RAG 查询
    - tool: "mcp-mirothinker/pure_rag_query"
      input:
        query: "什么是模型蒸馏？"
        documents: "{{documents}}"
      output: "rag_result"

    # Step 3: 生成答案
    - skill: "knowledge-explorer"
      input:
        rag_result: "{{rag_result}}"
      output: "final_answer"
```

---

## 配置文件完整示例

```yaml
# mindsymphony-mirothinker.config.yml

system:
  version: "21.0.0-evolution-miro"
  description: "MindSymphony v21.0 + MiroThinker 集成"

# MCP 服务器配置
mcp:
  servers:
    mcp-mirothinker:
      description: "MiroThinker 深度推理服务"
      enabled: true
      endpoint: "http://localhost:3001/mcp"
      capabilities:
        - "deep_reasoning"
        - "document_analysis"
        - "pure_rag"
        - "thought_chain"

# 统一触发器
unified_triggers:
  skill_triggers:
    # MiroThinker 核心技能
    - skill: "mcp-mirothinker/deep_reasoning"
      priority: "critical"
      category: "reasoning"

      triggers:
        - type: "command"
          patterns: ["/miro", "/深度推理"]
          weight: 10.0

        - type: "semantic"
          intent: "deep_reasoning"
          examples:
            - "深度分析这个问题"
            - "用思维链推理"
          weight: 8.0

    - skill: "mcp-mirothinker/analyze_document"
      priority: "high"
      category: "analysis"

      triggers:
        - type: "semantic"
          intent: "document_analysis"
          examples:
            - "深度分析这篇论文"
            - "提取文档核心内容"
          weight: 8.0

# 进化协议
evolution_protocol:
  self_learning:
    usage_tracking:
      enabled: true

    # MiroThinker 特定学习
    miro_learning:
      track_reasoning_quality: true
      optimize_depth: true
      learn_from_feedback: true

# Skills-n8n 协作
skills_n8n_collaboration:
  enabled: true

  # MiroThinker 协作模式
  miro_collaboration:
    mode: "hybrid"

    patterns:
      # MiroThinker 推理 + n8n 自动化
      - name: "reasoning_and_automation"
        description: "MiroThinker 深度推理，n8n 自动执行"
        example:
          - MiroThinker: 分析需求
          - n8n: 自动执行任务

      # n8n 收集 + MiroThinker 分析
      - name: "collection_and_analysis"
        description: "n8n 收集数据，MiroThinker 深度分析"
        example:
          - n8n: 收集文档
          - MiroThinker: 深度分析

# 协作模板
templates:
  miro_research_workflow:
    name: "MiroThinker 研究工作流"
    description: "使用 MiroThinker 进行深度研究"

    steps:
      - step: 1
        tool: "mcp-mirothinker/analyze_document"
        task: "深度分析文献"

      - step: 2
        skill: "literature-review"
        task: "生成综述"

      - step: 3
        skill: "scientific-writing"
        task: "撰写论文"
```

---

## 快速开始

### 1. 安装 MiroThinker

```bash
# 克隆项目
git clone https://github.com/MiroMindAI/MiroThinker.git
cd MiroThinker

# 安装依赖
pip install -r requirements.txt

# 启动 MCP 服务器
python mcp_mirothinker_server.py
```

### 2. 配置 MindSymphony

```bash
# 复制集成配置
cp mindsymphony-mirothinker.config.yml \
   C:/Users/13466/.claude/mindsymphony-v15.6/mindsymphony.config.yml
```

### 3. 测试集成

```bash
# 测试深度推理
/miro 深度分析: 机器学习模型的可解释性

# 测试文档分析
/文档分析 深度分析这篇论文的价值

# 测试语义触发
"用思维链推理如何提高模型泛化能力"
```

---

## 总结

### 三种集成方案对比

| 方案 | 优势 | 劣势 | 推荐度 |
|------|------|------|--------|
| **MCP 服务器** | 标准化、可扩展、双向通信 | 需要部署服务 | ⭐⭐⭐⭐⭐ |
| **Skill 封装** | 统一接口、易于使用 | 功能受限 | ⭐⭐⭐⭐ |
| **直接 API** | 简单直接 | 缺少标准化 | ⭐⭐⭐ |

### 推荐架构

**生产环境**: MCP 服务器 + Skill 封装
**开发测试**: 直接 API 调用
**混合模式**: 三种方案结合使用

---

**文档版本**: 1.0.0
**最后更新**: 2025-01-11
