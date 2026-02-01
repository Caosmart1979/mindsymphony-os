# GitHub Skills Distiller

## 基本信息

- **名称**: github-skills-distiller
- **层级**: 【术】The Technique - 方法与创造
- **类型**: execution
- **版本**: 1.0.0
- **作者**: MindSymphony Team

## 核心价值主张

> **"将整个GitHub压缩成你自己的超级技能库"**

从GitHub仓库中提取方法论、最佳实践和模式，转化为可复用的结构化技能，构建个人化的知识图谱。

## 触发条件

### 关键词
- github, skill, distill, extract, methodology
- 蒸馏技能, 提取方法论, 构建技能库
- 超级技能库, github学习

### 场景
- 需要从GitHub项目学习方法
- 想将优秀实践转化为可复用技能
- 构建个人知识管理系统
- 动态生成特定任务的执行技能

## 能力边界

### 能做什么
- ✅ 分析GitHub仓库README和代码结构
- ✅ 提取方法论、工作流和最佳实践
- ✅ 生成标准SKILL.md格式
- ✅ 构建个人技能知识图谱
- ✅ 追踪个人技能DNA和学习路径
- ✅ 根据任务需求动态生成技能
- ✅ 推荐技能组合和学习路径

### 不能做什么
- ❌ 直接修改GitHub仓库
- ❌ 访问私有仓库（无token时）
- ❌ 自动执行代码（仅提取方法论）
- ❌ 替代专业领域知识判断

## 输入输出

### 输入
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| repo_url | string | 是* | GitHub仓库URL或owner/repo |
| task_description | string | 是* | 任务描述（用于生成模式） |
| github_username | string | 否 | 用于分析个人档案 |
| domain | string | 否 | 目标领域（用于推荐） |

*注: distill模式需要repo_url，generate模式需要task_description

### 输出
| 产出 | 格式 | 说明 |
|------|------|------|
| distilled_skill | SKILL.md | 蒸馏的技能文档 |
| skill_graph | JSON | 技能知识图谱数据 |
| expertise_report | JSON | 个人专长分析报告 |
| learning_path | List | 推荐的学习路径 |

## 使用示例

### 示例1: 蒸馏GitHub仓库

```python
# 使用技能适配器
from mindsymphony.extensions.github_skills import create_github_skill_adapter

adapter = create_github_skill_adapter(user_id="user_001")
result = adapter.execute('distill', {
    'repo_url': 'bmad-code-org/BMAD-METHOD',
    'extract_patterns': True,
})

print(f"技能名称: {result['skill_name']}")
print(f"置信度: {result['confidence']:.1%}")
```

### 示例2: 动态生成技能

```python
result = adapter.execute('generate', {
    'task': '分析生物信息学数据集并生成可视化报告',
    'required_capabilities': ['bioinformatics', 'visualization'],
})

print(result['skill_name'])
print(result['content'])  # 完整的SKILL.md内容
```

### 示例3: 分析个人GitHub档案

```python
result = adapter.execute('profile', {
    'github_username': 'octocat',
})

report = result['expertise_report']
print(f"技能多样性: {report['skill_diversity']}")
print(f"常用技能: {report['top_skills']}")
```

### 示例4: 获取学习推荐

```python
result = adapter.execute('recommend', {
    'domain': 'machine_learning',
})

for rec in result['recommendations']:
    print(f"[{rec['priority']}] {rec['name']}: {rec['reason']}")
```

## 蜂后协奏集成

### 作为子任务被调用

当蜂后(cognitive-architect)分解任务时，本技能可响应以下意图：

```yaml
# 蜂后分解示例
task_decomposition:
  - phase: 技能获取
    intent: distill
    skill: github-skills-distiller
    input:
      repo_url: "{{ project.reference_repo }}"
    output: reference_skill

  - phase: 动态补充
    intent: generate
    skill: github-skills-distiller
    input:
      task: "{{ missing_capability }}"
    output: dynamic_skill
```

### 发射的信息素

本技能在执行过程中会发射以下信息素：

| 信息素类型 | 触发时机 | 载荷内容 |
|-----------|---------|---------|
| INTENT | 开始执行 | 执行意图和上下文 |
| DELIVERABLE | 技能生成完成 | skill_id, skill_name, confidence |
| INSIGHT | 发现知识模式 | 搜索洞察、专长分析 |
| EVOLUTION | 接收反馈 | 改进建议、学习信号 |

## 道法术器定位

### 【术】层特性

本技能属于**【术】The Technique** 层，专注于：

- **方法论提取**: 从具体项目中抽象可复用的方法
- **知识结构化**: 将非结构化文档转为结构化技能
- **技能管理**: 构建可查询、可推荐的知识图谱

### 与上下层的关系

```
【法】战略层 ← 需要技能库支持战略决策
      ↕
【术】本技能 → github-skills-distiller
      ↕
【器】执行层 → 输出SKILL.md供具体使用
```

## 协同进化

### 从使用中学习

本技能支持协同进化第一性原理：

1. **使用反馈**: 每次技能使用可记录成功/失败
2. **DNA更新**: 根据个人使用模式更新专长图谱
3. **推荐优化**: 基于历史数据改进推荐准确度
4. **置信度调整**: 根据反馈调整技能可靠性评分

### 进化接口

```python
# 提交反馈
adapter.evolve_from_feedback({
    'skill_id': 'skill_001',
    'success': True,
    'confidence_delta': 0.1,
    'improvement_area': 'better_code_examples',
})

# 查看进化报告
report = adapter.export_evolution_report()
```

## 价值对齐

### 显性意图处理

用户明确说出的需求：
- "帮我从GitHub学习这个项目" → distill
- "生成一个处理X的技能" → generate
- "分析我的GitHub档案" → profile

### 隐性意图挖掘

用户未明说但可能想要的：
- 技能的可复用性 → 自动生成标准SKILL.md
- 与个人专长的关联 → DNA追踪和推荐
- 与现有技能的整合 → 知识图谱自动关联

## 安全与边界

### 安全检查点

| 操作 | 风险等级 | 确认要求 |
|------|---------|---------|
| 蒸馏公开仓库 | 低 | 无需确认 |
| 保存技能到本地 | 中 | 确认磁盘空间 |
| 清空知识图谱 | 高 | 必须二次确认 |

### 隐私保护

- 个人DNA数据仅存储在本地
- GitHub分析不发送敏感信息
- 技能图谱可导出但不上传云端

## 依赖关系

### 必需依赖
- Python 3.8+
- 标准库: json, pathlib, dataclasses

### 可选依赖
- requests (用于真实GitHub API调用)
- PyGithub (高级GitHub操作)

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-02-01 | 初始发布，完整实现核心功能 |

## 相关技能

| 技能 | 关系 | 说明 |
|------|------|------|
| cognitive-architect | 调用者 | 蜂后分解任务时调用本技能 |
| knowledge-explorer | 协作 | 技能生成后可使用knowledge-explorer研究 |
| doc-skill-generator | 类似 | 从文档生成技能，本技能从GitHub生成 |

## 元数据

```yaml
apiVersion: mindsymphony.io/v1
kind: SkillInterop
metadata:
  name: github-skills-distiller
  layer: shu
  version: "1.0.0"
spec:
  capabilities:
    - github_repo_analysis
    - skill_distillation
    - knowledge_graph_mgmt
    - personal_dna_tracking
    - dynamic_skill_generation
  composable: true
  autonomous: true
  pheromone_compatible: true
```

---

*本技能是MindSymphony v21.4+的【术】层核心组件，遵循第一性原理和蜂后协奏协议。*
