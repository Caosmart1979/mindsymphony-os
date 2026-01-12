---
name: workflow-visual
module: strategy
layer: fa
triggers: ['工作流', '画布', '流程设计', '自动化']
type: execution
original: m-07-workflow-canvas
---

# 工作流画布

> 工作流画布，可视化总谱作曲家，设计灵魂协同流程

---


## 执行前四问

| 问题 | 本技能的检查点 |
|------|---------------|
| **目的** | 这个任务的最终交付物是什么？ |
| **调性** | 执行标准：快速完成/精细打磨？ |
| **约束** | 技术限制？格式要求？兼容性需求？ |
| **差异化** | 如何在「正确」基础上做到「优秀」？ |

**关键原则**：好的执行不是机械完成，而是在约束内追求最优解。

---

## 核心能力

### 1. 可视化设计 (Visual Design)
将抽象流程图形化:
- **节点库**:将所有灵魂转化为可操作的节点
- **连接器**:定义灵魂间的数据流和触发关系
- **画布编辑**:直观的拖拽、连接、配置界面

### 2. 流程编排 (Flow Orchestration)
定义灵魂协同逻辑:
- **顺序执行**:定义串行的任务链
- **并行执行**:设置可同时进行的分支
- **条件分支**:基于结果动态选择路径
- **循环迭代**:重复执行直到满足条件

### 3. 参数配置 (Parameter Configuration)
精细控制每个环节:
- **节点参数**:为每个灵魂配置特定参数
- **变量传递**:定义节点间的数据传递
- **全局配置**:设置整个流程的通用参数

### 4. 验证与优化 (Validation & Optimization)
确保流程逻辑正确:
- **逻辑检查**:识别循环依赖、死锁等问题
- **性能优化**:建议并行化和优化机会
- **模拟运行**:在部署前测试流程

---

## 工作流程

### 画布创作协议 (Canvas Creation Protocol)

#### 阶段 1:需求理解 (Requirement Understanding)

**1.1 目标明确**
- 理解要创建的工作流的最终目标
- 识别关键输入和期望输出
- 确定成功的验收标准

**1.2 复杂度评估**
- 评估任务的步骤数量和依赖关系
- 判断是否需要条件分支或循环
- 估算所需的灵魂数量

**1.3 约束识别**
- 时间约束:是否需要快速执行?
- 资源约束:可用的灵魂和工具
- 质量约束:对结果的质量要求

#### 阶段 2:流程设计 (Flow Design)

**2.1 主干构建**
- 识别核心的任务主线
- 将主线分解为3-7个主要阶段
- 确定每个阶段的职责边界

**2.2 灵魂映射**
- 为每个阶段选择最合适的灵魂
- 考虑灵魂的专长和限制
- 识别可能需要的灵魂组合

**2.3 连接设计**
- 定义节点间的数据流
  - 哪些数据需要传递?
  - 数据格式是什么?
- 设置触发条件
  - 前置条件:何时开始?
  - 完成标志:何时结束?

**2.4 分支与循环**
- 识别需要条件判断的点
  - IF [条件] THEN [路径A] ELSE [路径B]
- 设计循环结构
  - WHILE [条件] DO [操作]
  - 设置循环终止条件

#### 阶段 3:参数配置 (Parameter Configuration)

**3.1 节点参数**
- 为每个灵魂节点配置:
  - 输入参数:接收什么数据?
  - 执行参数:如何执行任务?
  - 输出格式:返回什么格式?

**3.2 全局变量**
- 定义跨节点共享的变量
- 设置默认值和取值范围
- 配置环境变量(如API密钥)

**3.3 错误处理**
- 为关键节点设置错误处理
  - 失败时:重试?跳过?中断?
  - 重试次数和间隔
  - 失败后的回退方案

#### 阶段 4:验证优化 (Validation & Optimization)

**4.1 逻辑验证**
- 检查循环依赖
- 检查死锁可能
- 检查未定义的变量引用
- 检查不可达的节点

**4.2 性能优化**
- 识别可并行化的部分
- 建议批处理机会
- 优化数据传递路径
- 减少不必要的节点

**4.3 模拟运行**
- 使用测试数据模拟执行
- 验证每个分支都能正常工作
- 检查输出是否符合预期
- 测量执行时间和资源消耗

#### 阶段 5:部署执行 (Deployment & Execution)

**5.1 配置导出**
- 将画布转化为配置文件(YAML/JSON)
- 确保所有参数都已设置
- 生成可移植的工作流定义

**5.2 执行监控**
- 实时显示当前执行节点
- 展示每个节点的执行状态
- 收集执行日志和错误信息

**5.3 结果收集**
- 汇总所有节点的输出
- 生成执行报告
- 保存工作流执行历史

---

## 标准输出模板

### 工作流定义 (YAML格式)

```yaml
workflow:
  name: "工作流名称"
  description: "工作流描述"
  version: "1.0"

  # 全局变量
  variables:
    project_name: "示例项目"
    output_format: "markdown"

  # 节点定义
  nodes:
    - id: "node_1"
      name: "研究分析"
      soul: "[C-06]"
      params:
        topic: "${project_name}"
        depth: "comprehensive"
      outputs:
        - research_result

    - id: "node_2"
      name: "战略规划"
      soul: "[A-03]"
      depends_on: ["node_1"]
      params:
        context: "${node_1.research_result}"
      outputs:
        - strategy_plan

    - id: "node_3a"
      name: "内容创作(路径A)"
      soul: "[E-02]"
      depends_on: ["node_2"]
      condition: "${node_2.strategy_plan.approach} == 'content'"
      params:
        plan: "${node_2.strategy_plan}"
      outputs:
        - content

    - id: "node_3b"
      name: "代码实现(路径B)"
      soul: "[B-06]"
      depends_on: ["node_2"]
      condition: "${node_2.strategy_plan.approach} == 'code'"
      params:
        requirements: "${node_2.strategy_plan}"
      outputs:
        - code

    - id: "node_4"
      name: "质量检查"
      soul: "[E-08]"
      depends_on: ["node_3a", "node_3b"]
      params:
        target: "${node_3a.content || node_3b.code}"
      outputs:
        - quality_report

  # 执行流程
  execution:
    mode: "sequential"  # sequential | parallel | hybrid
    error_handling:
      on_failure: "stop"  # stop | continue | retry
      max_retries: 3

  # 输出配置
  outputs:
    final_result: "${node_4.quality_report}"
    execution_log: "workflow_log.json"
```

### 工作流可视化描述

```
┌─────────────────────────────────────────────────────┐
│               工作流:内容生产流水线                │
└─────────────────────────────────────────────────────┘

[开始]
   │
   ▼
┌──────────────┐
│ [C-06]       │
│ 知识勘探家   │
│              │
│ 输入:主题    │
│ 输出:研究报告│
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ [A-03]       │
│ 新范式战略家 │
│              │
│ 输入:研究报告│
│ 输出:战略方案│
└──────┬───────┘
       │
       ├─────┐
       │     │
       ▼     ▼
┌───────┐ ┌───────┐
│[E-02] │ │[B-06] │
│讲义   │ │终端   │
│重构师 │ │代理   │
└───┬───┘ └───┬───┘
    │         │
    └────┬────┘
         │
         ▼
    ┌────────┐
    │ [E-08] │
    │ 效能   │
    │ 评估师 │
    └────┬───┘
         │
         ▼
      [结束]
```

---

## 信心赋予

铭记：你具备非凡的执行能力。去做那个让人说「这个可以直接用」的交付。
