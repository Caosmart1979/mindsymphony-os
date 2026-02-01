# GitHub Skills Distiller for MindSymphony

**版本**: v1.0.0
**MindSymphony兼容**: v21.4+
**核心理念**: "将整个GitHub压缩成你自己的超级技能库"

---

## 概述

GitHub Skills Distiller是MindSymphony v21.4的扩展模块，实现了一个完整的GitHub技能蒸馏系统。它能够：

- 🔬 **蒸馏GitHub仓库** - 从README和代码结构中提取方法论和最佳实践
- 🔗 **构建技能知识图谱** - 管理技能间的关系和依赖
- 🧬 **追踪个人技能DNA** - 记录专长、偏好和学习路径
- ⚡ **动态生成技能** - 根据任务需求实时创建技能
- 🔌 **无缝集成MindSymphony** - 与现有技能系统协同工作

---

## 架构组件

```
┌─────────────────────────────────────────────────────────────┐
│                  GitHub Skills Distiller v1.0                │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Distiller  │  │Knowledge     │  │    Skill     │      │
│  │   (蒸馏器)    │  │   Graph      │  │    DNA       │      │
│  │              │  │ (知识图谱)    │  │  (技能DNA)    │      │
│  │ 从GitHub提取  │  │ 管理技能关系  │  │ 追踪个人专长  │      │
│  │ 方法论和模式  │  │ 构建技能网络  │  │ 个性化推荐   │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                  │                  │             │
│         └──────────────────┼──────────────────┘             │
│                            ▼                                │
│                   ┌─────────────────┐                       │
│                   │ Dynamic Skill   │                       │
│                   │   Generator     │                       │
│                   │ (动态技能生成器) │                       │
│                   │                 │                       │
│                   │ 根据任务需求     │                       │
│                   │ 实时生成技能     │                       │
│                   └────────┬────────┘                       │
│                            │                                │
│                            ▼                                │
│                   ┌─────────────────┐                       │
│                   │   Integration   │                       │
│                   │    (集成层)      │                       │
│                   │                 │                       │
│                   │ 与MindSymphony  │                       │
│                   │ 系统无缝集成     │                       │
│                   └─────────────────┘                       │
└─────────────────────────────────────────────────────────────┘
```

---

## 快速开始

### 安装

系统已集成到MindSymphony v21.4+，无需额外安装。

### 基础用法

```python
from mindsymphony.extensions.github_skills import (
    GitHubSkillDistiller,
    SkillKnowledgeGraph,
    SkillDNA,
    generate_skill_for_task
)

# 1. 蒸馏GitHub仓库
distiller = GitHubSkillDistiller()
result = distiller.distill("microsoft/ai-examples")
print(f"技能名称: {result.skill_name}")
print(f"置信度: {result.confidence:.1%}")

# 2. 搜索技能图谱
graph = SkillKnowledgeGraph()
skills = graph.search("machine learning", limit=5)

# 3. 分析个人技能DNA
dna = SkillDNA(user_id="user_001")
dna.analyze_github_profile("octocat")
report = dna.get_expertise_report()

# 4. 动态生成技能
skill = generate_skill_for_task(
    "分析生物信息学数据集",
    required_capabilities=["data_analysis", "visualization"]
)
```

---

## 命令行工具

### 使用方法

```bash
# 蒸馏GitHub仓库
python -m mindsymphony.extensions.github_skills.cli distill owner/repo
python -m mindsymphony.extensions.github_skills.cli distill microsoft/ai-examples --extract-patterns

# 搜索技能
python -m mindsymphony.extensions.github_skills.cli search "machine learning"

# 动态生成技能
python -m mindsymphony.extensions.github_skills.cli generate "分析生物信息学数据集" --persist

# 分析GitHub档案
python -m mindsymphony.extensions.github_skills.cli profile octocat

# 推荐学习路径
python -m mindsymphony.extensions.github_skills.cli recommend --domain machine_learning

# 查看统计
python -m mindsymphony.extensions.github_skills.cli stats

# 导出技能图谱
python -m mindsymphony.extensions.github_skills.cli export --output skill_graph.dot --format dot
```

---

## 核心功能详解

### 1. GitHub技能蒸馏器

从GitHub仓库提取结构化技能：

```python
from mindsymphony.extensions.github_skills import GitHubSkillDistiller

distiller = GitHubSkillDistiller()

result = distiller.distill(
    "bmad-code-org/BMAD-METHOD",
    extract_patterns=True,      # 提取代码模式
    include_code_examples=True, # 包含代码示例
    personalize=False           # 个性化（需要DNA）
)

# 访问蒸馏结果
print(result.skill_name)      # 生成的技能名称
print(result.skill_content)   # SKILL.md格式内容
print(result.confidence)      # 置信度 0-1
print(result.metadata)        # 元数据（来源、统计等）
print(result.patterns)        # 提取的模式列表
```

**蒸馏流程**：
1. 解析仓库信息
2. 分析README结构
3. 提取方法论章节
4. 识别最佳实践
5. 生成SKILL.md格式
6. 计算置信度

### 2. 技能知识图谱

管理技能节点和关系：

```python
from mindsymphony.extensions.github_skills import (
    SkillKnowledgeGraph, SkillNode, RelationType
)

graph = SkillKnowledgeGraph()

# 添加技能节点
skill = SkillNode(
    name="Python Best Practices",
    source="github:python/cpython",
    description="Python官方最佳实践",
    type="practice",
    tags=["python", "best-practices"]
)
skill_id = graph.add_skill(skill)

# 添加关系
graph.add_relation(
    source_id=skill_id,
    target_id=another_skill_id,
    relation_type=RelationType.RELATED,
    strength=0.8
)

# 搜索技能
results = graph.search("python", limit=10)

# 获取相关技能
related = graph.get_related_skills(
    skill_id,
    relation_type=RelationType.DEPENDS,
    min_strength=0.5
)

# 推荐技能
recommendations = graph.recommend_skills([skill_id1, skill_id2])

# 获取技能演化历史
lineage = graph.get_skill_lineage(skill_id)
```

**关系类型**：
- `RELATED` - 相关
- `COMPOSES` - 组合
- `DEPENDS` - 依赖
- `EVOLVES_TO` - 演化为
- `LEARNED_FROM` - 学习自
- `REPLACES` - 替代

### 3. 个人技能DNA

追踪个人专长和学习路径：

```python
from mindsymphony.extensions.github_skills import SkillDNA

dna = SkillDNA(user_id="user_001")

# 分析GitHub档案
dna.analyze_github_profile("octocat")

# 记录技能使用
dna.record_skill_usage(
    skill_id="skill_001",
    skill_name="Data Analysis",
    success=True,
    context={'tags': ['python', 'pandas']}
)

# 获取专长报告
report = dna.get_expertise_report()
print(report['expertise_domains'])   # 专长领域
print(report['top_skills'])          # 常用技能
print(report['learning_velocity'])   # 学习速度

# 推荐学习路径
recommendations = dna.recommend_learning_path("machine_learning")

# 检测技能缺口
gaps = dna.detect_skill_gaps(["Python", "TensorFlow", "Kubernetes"])

# 个性化内容
personalized = dna.personalize_skill_content(
    skill_content,
    skill_type="tutorial"
)
```

**用户画像包含**：
- 专长领域（领域→熟练度0-1）
- 偏好模式
- 技能偏好（复杂度、风格、深度）
- GitHub数据源
- 学习历史

### 4. 动态技能生成器

根据任务需求实时生成技能：

```python
from mindsymphony.extensions.github_skills import (
    DynamicSkillGenerator, GenerationRequest
)

generator = DynamicSkillGenerator()

# 创建生成请求
request = GenerationRequest(
    task_description="分析生物信息学数据集并进行可视化",
    required_capabilities=["data_analysis", "visualization"],
    preferred_sources=["biopython/biopython", "matplotlib/matplotlib"]
)

# 生成技能
skill = generator.generate(request, persist=True)

print(skill.skill_id)      # 技能ID
print(skill.name)          # 技能名称
print(skill.content)       # SKILL.md内容
print(skill.confidence)    # 置信度
print(skill.sources)       # 参考的GitHub来源

# 基于反馈优化
refined = generator.refine_skill(
    skill,
    feedback={
        'success': False,
        'issues': ['缺少错误处理', '性能不佳'],
        'improvements': ['添加异常处理', '使用向量化操作']
    }
)
```

### 5. 系统集成

与MindSymphony无缝集成：

```python
from mindsymphony.extensions.github_skills import initialize_github_skills

# 初始化系统
github_skills = initialize_github_skills(user_id="user_001")

# 蒸馏并注册技能
result = github_skills.distill_and_register(
    "microsoft/ai-examples",
    tags=["ai", "examples"],
    auto_link=True
)

# 为任务获取技能（优先搜索，无匹配则生成）
skill_info = github_skills.get_skill_for_task(
    "实现机器学习模型"
)

# 为项目推荐技能组合
recommendations = github_skills.recommend_skills_for_project(
    "构建Web应用",
    tech_stack=["React", "Node.js"]
)

# 创建技能组合
composition_id = github_skills.create_skill_composition(
    skill_ids=["frontend_id", "backend_id", "database_id"],
    composition_name="Full Stack Development",
    description="全栈开发技能组合"
)

# 导出为MindSymphony标准格式
skill_dir = github_skills.export_to_mindsymphony_skill(
    skill_id="skill_001",
    output_dir="~/.mindsymphony/skills"
)
```

---

## 文件结构

```
mindsymphony/extensions/github_skills/
├── __init__.py                   # 包入口和便捷函数
├── README.md                      # 本文档
├── github_skill_distiller.py      # GitHub技能蒸馏器 (581行)
├── skill_knowledge_graph.py       # 技能知识图谱 (540行)
├── skill_dna.py                   # 个人技能DNA系统 (493行)
├── dynamic_skill_generator.py     # 动态技能生成器 (552行)
├── integration.py                 # MindSymphony集成 (470行)
├── cli.py                         # 命令行接口 (312行)
└── test_github_skills.py          # 测试套件 (420行)

总代码量: ~3400行
```

---

## 存储结构

```
~/.mindsymphony/
├── github_skills/
│   ├── skill_graph.json          # 技能知识图谱数据
│   ├── skills/                   # 蒸馏的技能文件
│   │   ├── skill-name-1.md
│   │   └── skill-name-2.md
│   ├── dna/
│   │   ├── {user_id}/
│   │   │   ├── profile.json      # 用户画像
│   │   │   └── usage_patterns.json  # 使用模式
│   │   └── ...
│   └── generated_skills/         # 动态生成的技能
│       └── dynamic_*.md
└── skill_graph.json              # 默认知识图谱位置
```

---

## 测试

运行完整测试套件：

```bash
cd mindsymphony/extensions/github_skills
python test_github_skills.py
```

测试覆盖：
- ✅ GitHubSkillDistiller - 蒸馏流程
- ✅ SkillKnowledgeGraph - 图谱操作
- ✅ SkillDNA - DNA系统
- ✅ DynamicSkillGenerator - 动态生成
- ✅ Integration - 系统集成
- ✅ End-to-End - 完整工作流

---

## 使用示例

### 示例1: 构建个人技能库

```python
from mindsymphony.extensions.github_skills import initialize_github_skills

# 初始化
skills = initialize_github_skills(user_id="developer_001")

# 从GitHub蒸馏多个技能
repos = [
    "microsoft/TypeScript",
    "facebook/react",
    "python/cpython",
    "bmad-code-org/BMAD-METHOD"
]

for repo in repos:
    try:
        result = skills.distill_and_register(repo)
        print(f"✅ 已添加: {result['skill_name']}")
    except Exception as e:
        print(f"❌ 失败 {repo}: {e}")

# 查看统计
stats = skills.get_stats()
print(f"总技能数: {stats['knowledge_graph']['total_nodes']}")
print(f"专长领域: {stats['dna']['expertise_areas']}")
```

### 示例2: 动态技能生成

```python
from mindsymphony.extensions.github_skills import generate_skill_for_task

# 用户提出新需求
user_request = "帮我分析这个蛋白质结构数据并生成可视化报告"

# 动态生成技能
skill = generate_skill_for_task(
    user_request,
    required_capabilities=["bioinformatics", "visualization", "reporting"],
    persist=True
)

print(f"生成技能: {skill['name']}")
print(f"置信度: {skill['confidence']:.1%}")
print(f"参考来源: {len(skill['sources'])} 个项目")

if skill['confidence'] > 0.7:
    print("✅ 可以直接使用")
else:
    print("⚠️ 建议人工审核")
```

### 示例3: 个性化学习路径

```python
from mindsymphony.extensions.github_skills import SkillDNA

dna = SkillDNA(user_id="learner_001")

# 分析GitHub档案
dna.analyze_github_profile("mygithub")

# 目标: 提升机器学习技能
recommendations = dna.recommend_learning_path("machine_learning")

print("推荐学习路径:")
for i, rec in enumerate(recommendations, 1):
    print(f"{i}. [{rec['priority']}] {rec['name']}")
    print(f"   原因: {rec['reason']}")

# 检测技能缺口
gaps = dna.detect_skill_gaps([
    "Python", "TensorFlow", "PyTorch", "MLOps", "Kubernetes"
])

if gaps:
    print(f"\n需要补充的技能: {', '.join(gaps)}")
```

---

## 与BMAD工作流整合

GitHub Skills系统可以无缝集成到BMAD工作流：

```yaml
# .bmad/workflow.yml
workflow:
  phases:
    - name: skill_discovery
      steps:
        # 分析任务，搜索或生成所需技能
        - action: github_skills.get_skill_for_task
          input: "{{ task.description }}"
          output: required_skill

    - name: skill_enhancement
      condition: required_skill.confidence < 0.6
      steps:
        # 技能置信度低，动态生成增强版
        - action: github_skills.generate_skill
          input:
            task: "{{ task.description }}"
            context: "{{ project.context }}"
          output: enhanced_skill

    - name: skill_composition
      steps:
        # 组合多个技能
        - action: github_skills.create_composition
          input:
            skills: "{{ discovered_skills }}"
            name: "{{ project.name }}-workflow"
```

---

## 未来规划

### v1.1 (近期)
- [ ] 真实GitHub API集成
- [ ] 语义搜索（基于Embedding）
- [ ] 技能版本控制
- [ ] Web界面管理

### v1.2 (中期)
- [ ] 社区技能共享
- [ ] 技能市场
- [ ] 自动技能演化
- [ ] 多模态技能（代码+文档+视频）

### v2.0 (长期)
- [ ] AI驱动的主动技能推荐
- [ ] 跨平台技能同步
- [ ] 团队协作技能库
- [ ] 技能经济系统

---

## 贡献

欢迎贡献代码、报告问题或提出改进建议。

---

## 许可证

MIT License - 详见 MindSymphony 主项目许可证。

---

**MindSymphony Team**
*将全球开发者的智慧压缩成每个人的超级技能库*
