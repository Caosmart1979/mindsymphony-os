# 技能发现机制规范 (Skill Discovery Mechanism v1.0)

> 让 AI 能够自动发现和理解技能之间的关系。

---

## 核心概念

技能发现是通过元数据让 AI 系统（如 mindsymphony）能够：
1. **自动发现**技能 - 基于需求找到合适的技能
2. **理解关系** - 知道技能之间的协作关系
3. **智能路由** - 根据任务自动选择技能组合
4. **避免硬编码** - 不需要在代码中硬编码技能名称

---

## 发现层次

```
┌─────────────────────────────────────────────────┐
│  Layer 3: 关系推理 (Relationship Inference)     │
│  基于 provides/consumes 推理协作链                │
├─────────────────────────────────────────────────┤
│  Layer 2: 模式匹配 (Pattern Matching)           │
│  基于关键词、分类、标签匹配                       │
├─────────────────────────────────────────────────┤
│  Layer 1: 元数据扫描 (Metadata Scanning)        │
│  读取 SKILL.md frontmatter 和 INTEROP.yml        │
└─────────────────────────────────────────────────┘
```

---

## Layer 1: 元数据扫描

### 1.1 扫描目标

扫描每个技能的以下信息：

```yaml
# 从 SKILL.md frontmatter
name: skill-name
description: "技能描述"
category: design
tags: [frontend, ui, react]
provides: [design-tokens, component-templates]
consumes: [brand-guidelines]
related: [brand-guidelines, canvas-design]

# 从 INTEROP.yml (如果存在)
provides:
  - id: "design-tokens"
    location: "references/tokens.json"
```

### 1.2 扫描实现（伪代码）

```python
def scan_skills(skills_dir):
    """扫描所有技能，构建发现索引"""
    index = {
        'by_name': {},      # 按名称索引
        'by_category': {},  # 按分类索引
        'by_tag': {},       # 按标签索引
        'by_provides': {},  # 按提供的能力索引
        'by_consumes': {},  # 按消耗的能力索引
    }

    for skill_dir in skills_dir:
        metadata = load_skill_metadata(skill_dir)

        # 按名称索引
        index['by_name'][metadata['name']] = metadata

        # 按分类索引
        cat = metadata.get('category')
        if cat:
            index['by_category'].setdefault(cat, []).append(metadata['name'])

        # 按标签索引
        for tag in metadata.get('tags', []):
            index['by_tag'].setdefault(tag, []).append(metadata['name'])

        # 按 provides 索引
        for provides in metadata.get('provides', []):
            index['by_provides'].setdefault(provides, []).append(metadata['name'])

        # 按 consumes 索引
        for consumes in metadata.get('consumes', []):
            index['by_consumes'].setdefault(consumes, []).append(metadata['name'])

    return index
```

---

## Layer 2: 模式匹配

### 2.1 关键词匹配

基于 `triggers` 字段匹配：

```yaml
# frontend-design 的 triggers
triggers:
  - level: "high"
    keywords:
      - "前端"
      - "UI"
      - "React"
  - level: "medium"
    keywords:
      - "界面"
      - "视觉"
```

**匹配算法**：

```python
def match_by_keywords(user_input, skill_index):
    """根据用户输入匹配技能"""
    matches = []

    for skill_name, metadata in skill_index['by_name'].items():
        score = 0
        for trigger in metadata.get('triggers', []):
            for keyword in trigger['keywords']:
                if keyword in user_input:
                    if trigger['level'] == 'high':
                        score += 10
                    elif trigger['level'] == 'medium':
                        score += 5

        if score > 0:
            matches.append((skill_name, score))

    # 按分数排序
    return sorted(matches, key=lambda x: x[1], reverse=True)
```

### 2.2 分类匹配

基于 `category` 字段匹配：

```python
def match_by_category(task_type, skill_index):
    """根据任务类型匹配分类"""
    category_map = {
        'design': ['前端', 'UI', '设计', '视觉'],
        'create': ['创建', '构建', '生成'],
        'document': ['文档', '写作', '报告'],
        'workflow': ['流程', '工作流', '规划'],
    }

    for category, keywords in category_map.items():
        if any(kw in task_type for kw in keywords):
            return skill_index['by_category'].get(category, [])

    return []
```

### 2.3 标签匹配

基于 `tags` 字段匹配：

```python
def match_by_tags(user_tags, skill_index):
    """根据标签匹配技能"""
    matches = []
    for tag in user_tags:
        if tag in skill_index['by_tag']:
            matches.extend(skill_index['by_tag'][tag])

    # 去重并返回
    return list(set(matches))
```

---

## Layer 3: 关系推理

### 3.1 协作链推理

基于 `provides/consumes` 推理技能协作链：

```python
def infer_collaboration_chain(target_skill, skill_index):
    """推理到达目标技能的协作链"""
    chain = []

    # 检查目标技能消耗什么
    target_metadata = skill_index['by_name'][target_skill]

    for consumes in target_metadata.get('consumes', []):
        # 找到提供这个能力的技能
        providers = skill_index['by_provides'].get(consumes, [])
        if providers:
            # 选择最佳提供者（可基于优先级、相关性等）
            best_provider = select_best_provider(providers, target_skill)
            if best_provider:
                chain.append({
                    'consumer': target_skill,
                    'provider': best_provider,
                    'resource': consumes
                })

    return chain
```

**示例**：

```python
# 用户请求: "创建一个有品牌风格的前端组件"

# 1. 匹配到 frontend-design
# 2. 检查 frontend-design 的 consumes: [brand-guidelines]
# 3. 找到 brand-guidelines 提供品牌规范
# 4. 推理出协作链:
#    brand-guidelines → frontend-design
```

### 3.2 关系图谱

构建技能关系图谱：

```python
def build_relationship_graph(skill_index):
    """构建技能关系图谱"""
    graph = {}

    for skill_name, metadata in skill_index['by_name'].items():
        graph[skill_name] = {
            'provides': metadata.get('provides', []),
            'consumes': metadata.get('consumes', []),
            'related': metadata.get('related', []),
            'category': metadata.get('category'),
        }

    return graph
```

**可视化示例**：

```
brand-guidelines ──[provides design-tokens]──> frontend-design
                                                          │
                                                          ├─[related]─> canvas-design
                                                          └─[related]─> theme-factory

skill-creator ──[provides skill-templates]──> mcp-builder
                                                        │
                                                        └─[related]─> doc-skill-generator
```

---

## 智能路由决策

### 决策流程

```
用户输入
    │
    ▼
关键词匹配 ──→ 高置信度匹配 → 直接路由
    │
    ▼
分类匹配 ──→ 中等置信度匹配 → 候选技能
    │
    ▼
关系推理 ──→ 检查协作需求 → 构建技能链
    │
    ▼
输出技能组合方案
```

### 路由算法

```python
def intelligent_router(user_input, skill_index):
    """智能路由决策"""

    # 1. 关键词匹配
    keyword_matches = match_by_keywords(user_input, skill_index)
    if keyword_matches and keyword_matches[0][1] >= 10:  # 高置信度
        primary_skill = keyword_matches[0][0]
    else:
        # 2. 分类匹配
        category_matches = match_by_category(user_input, skill_index)
        if category_matches:
            primary_skill = category_matches[0]
        else:
            # 3. 标签匹配
            tag_matches = match_by_tags(user_input, skill_index)
            if tag_matches:
                primary_skill = tag_matches[0]
            else:
                return None

    # 3. 推理协作链
    collaboration_chain = infer_collaboration_chain(primary_skill, skill_index)

    # 4. 构建技能组合方案
    result = {
        'primary': primary_skill,
        'collaborators': [c['provider'] for c in collaboration_chain],
        'chain': collaboration_chain,
        'reasoning': f"根据用户输入匹配到 {primary_skill}，" +
                     f"需要协作技能: {', '.join(result['collaborators'])}"
    }

    return result
```

---

## 发现 API

### 查询接口

```python
class SkillDiscovery:
    """技能发现 API"""

    def __init__(self, skills_dir):
        self.index = scan_skills(skills_dir)
        self.graph = build_relationship_graph(self.index)

    def find_by_name(self, name):
        """按名称查找"""
        return self.index['by_name'].get(name)

    def find_by_category(self, category):
        """按分类查找"""
        return self.index['by_category'].get(category, [])

    def find_by_tags(self, tags):
        """按标签查找"""
        results = []
        for tag in tags:
            results.extend(self.index['by_tag'].get(tag, []))
        return list(set(results))

    def find_providers(self, resource):
        """查找提供特定资源的技能"""
        return self.index['by_provides'].get(resource, [])

    def find_consumers(self, resource):
        """查找消耗特定资源的技能"""
        return self.index['by_consumes'].get(resource, [])

    def find_collaborators(self, skill_name):
        """查找协作技能"""
        chain = infer_collaboration_chain(skill_name, self.index)
        return [c['provider'] for c in chain]

    def find_related(self, skill_name):
        """查找相关技能"""
        metadata = self.index['by_name'].get(skill_name)
        return metadata.get('related', []) if metadata else []

    def route(self, user_input):
        """智能路由"""
        return intelligent_router(user_input, self.index)
```

### 使用示例

```python
# 初始化发现系统
discovery = SkillDiscovery('/path/to/skills')

# 查找提供设计令牌的技能
providers = discovery.find_providers('design-tokens')
# → ['brand-guidelines', 'frontend-design']

# 查找 frontend-design 的协作技能
collaborators = discovery.find_collaborators('frontend-design')
# → ['brand-guidelines']

# 智能路由
result = discovery.route("创建一个有品牌风格的前端组件")
# → {
#      'primary': 'frontend-design',
#      'collaborators': ['brand-guidelines'],
#      'reasoning': '...'
#    }
```

---

## mindsymphony 集成

### 替换硬编码路由

**Before (硬编码)**：

```markdown
| 关键词 | 路由到 | 置信度 |
|--------|--------|--------|
| 前端/UI/React | frontend-design | 100% |
```

**After (动态发现)**：

```python
# mindsymphony 使用发现系统
from skill_discovery import SkillDiscovery

discovery = SkillDiscovery('/path/to/skills')

def route_to_skill(user_input):
    """动态路由到技能"""
    result = discovery.route(user_input)
    if result:
        return invoke_skill(result['primary'], result['collaborators'])
    else:
        return invoke_cognitive_architect(user_input)
```

### 更新技能组合模式

**Before (硬编码)**：

```markdown
| 场景 | 推荐组合 | 协作方式 |
|------|---------|---------|
| 品牌视觉项目 | brand-alchemist → concept-singularity | 价值挖掘 → 视觉转化 |
```

**After (动态推理)**：

```python
def recommend_skill_combination(project_type):
    """动态推荐技能组合"""
    # 1. 发现主技能
    primary = discovery.route(project_type)['primary']

    # 2. 推理协作链
    collaborators = discovery.find_collaborators(primary)

    # 3. 构建组合方案
    return {
        'primary': primary,
        'collaborators': collaborators,
        'order': determine_execution_order(primary, collaborators)
    }
```

---

## 缓存策略

### 缓存层级

```
┌─────────────────────────────────────────────────┐
│  L1: 内存缓存 (运行时)                            │
│  已扫描的技能元数据                               │
├─────────────────────────────────────────────────┤
│  L2: 文件缓存 (skill_index.json)                 │
│  持久化的发现索引                                 │
├─────────────────────────────────────────────────┤
│  L3: 技能文件 (SKILL.md, INTEROP.yml)            │
│  原始元数据                                       │
└─────────────────────────────────────────────────┘
```

### 缓存失效

```python
def should_rebuild_cache(skill_index_path, skills_dir):
    """检查是否需要重建缓存"""
    if not os.path.exists(skill_index_path):
        return True

    # 检查技能文件是否更新
    cache_mtime = os.path.getmtime(skill_index_path)
    for skill_dir in os.listdir(skills_dir):
        skill_md = os.path.join(skills_dir, skill_dir, 'SKILL.md')
        if os.path.exists(skill_md):
            if os.path.getmtime(skill_md) > cache_mtime:
                return True

    return False
```

---

## 性能优化

### 1. 延迟加载

只加载技能元数据，不加载完整内容：

```python
def load_skill_metadata(skill_dir):
    """只加载 frontmatter，不加载 body"""
    skill_md = os.path.join(skill_dir, 'SKILL.md')
    with open(skill_md, 'r', encoding='utf-8') as f:
        content = f.read()

    # 只解析 frontmatter
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if match:
        return yaml.safe_load(match.group(1))

    return {}
```

### 2. 并行扫描

并行扫描多个技能：

```python
from concurrent.futures import ThreadPoolExecutor

def scan_skills_parallel(skills_dir, max_workers=4):
    """并行扫描技能"""
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for skill_dir in os.listdir(skills_dir):
            future = executor.submit(load_skill_metadata,
                                     os.path.join(skills_dir, skill_dir))
            futures.append(future)

        return [f.result() for f in futures]
```

### 3. 增量更新

只重新扫描变更的技能：

```python
def incremental_scan(old_index, skills_dir):
    """增量扫描技能"""
    new_index = old_index.copy()

    for skill_dir in os.listdir(skills_dir):
        skill_path = os.path.join(skills_dir, skill_dir)
        skill_mtime = os.path.getmtime(os.path.join(skill_path, 'SKILL.md'))

        # 检查是否需要更新
        cached = old_index['by_name'].get(skill_dir)
        if not cached or cached.get('_mtime', 0) < skill_mtime:
            # 重新扫描
            metadata = load_skill_metadata(skill_path)
            metadata['_mtime'] = skill_mtime
            new_index['by_name'][skill_dir] = metadata

    return new_index
```

---

## 工具脚本

### 扫描脚本

```bash
#!/bin/bash
# scan_skills.sh - 扫描技能并生成索引

python3 << EOF
from skill_discovery import SkillDiscovery
import json

discovery = SkillDiscovery('.')
index = discovery.index

# 保存索引
with open('skill_index.json', 'w') as f:
    json.dump(index, f, indent=2)

print(f"✅ 扫描完成: {len(index['by_name'])} 个技能")
EOF
```

### 查询脚本

```bash
#!/bin/bash
# query_skills.sh - 查询技能

query="$1"

python3 << EOF
from skill_discovery import SkillDiscovery

discovery = SkillDiscovery('.')
result = discovery.route("$query")

if result:
    print(f"主技能: {result['primary']}")
    print(f"协作技能: {', '.join(result['collaborators'])}")
    print(f"推理: {result['reasoning']}")
else:
    print("未找到匹配的技能")
EOF
```

### 可视化脚本

```bash
#!/bin/bash
# visualize_skills.sh - 可视化技能关系

python3 << EOF
from skill_discovery import SkillDiscovery
import graphviz

discovery = SkillDiscovery('.')
graph = discovery.graph

dot = graphviz.Digraph()
for skill, relations in graph.items():
    for provides in relations['provides']:
        dot.edge(skill, f"resource:{provides}", label="provides")
    for consumes in relations['consumes']:
        dot.edge(f"resource:{consumes}", skill, label="consumes")

dot.render('skill_graph', format='png', view=True)
EOF
```

---

## 测试

### 单元测试

```python
import unittest

class TestSkillDiscovery(unittest.TestCase):

    def setUp(self):
        self.discovery = SkillDiscovery('./test_skills')

    def test_find_by_name(self):
        skill = self.discovery.find_by_name('test-skill')
        self.assertIsNotNone(skill)
        self.assertEqual(skill['name'], 'test-skill')

    def test_find_providers(self):
        providers = self.discovery.find_providers('design-tokens')
        self.assertIn('brand-guidelines', providers)

    def test_route(self):
        result = self.discovery.route("创建前端组件")
        self.assertEqual(result['primary'], 'frontend-design')
```

---

## 最佳实践

### DO ✅

1. **提供清晰的元数据** - 让发现更准确
2. **使用标准化分类** - 提高可发现性
3. **添加相关标签** - 支持多维度发现
4. **声明协作关系** - 让 AI 能推理协作链
5. **定期更新缓存** - 保持索引新鲜

### DON'T ❌

1. **不要过度标签化** - 只保留最相关的标签
2. **不要忽略分类** - 分类是发现的基础
3. **不要忘记更新** - 技能变更时更新元数据
4. **不要硬编码路由** - 使用发现系统
5. **不要绕过缓存** - 缓存提升性能

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2025-01-08 | 初始版本 |
