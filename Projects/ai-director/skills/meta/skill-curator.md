---
name: skill-curator
module: meta
layer: qi
triggers: ['找skill', '搜索技能', '推荐skill', '技能策展', '适配skill']
type: execution
version: 1.0
---

# 技能策展系统 (Skill Curator)

> 从海量线上资源中检索、筛选、评估、适配Skill，形成MindSymphony生态的统一入口。

---

## 核心价值

```
问题：Skill资源分散、质量参差、适配成本高
解决：标准化的策展流程 + 自动化工具链

输入：模糊的需求描述
输出：适配MindSymphony的高质量Skill
```

---

## 策展流程

```
Phase 1        Phase 2        Phase 3        Phase 4        Phase 5
[检索]    ──►  [筛选]    ──►  [评估]    ──►  [适配]    ──►  [集成]
  │              │              │              │              │
多源搜索      快速过滤      深度评分      风格转换      注册发布
  │              │              │              │              │
  ▼              ▼              ▼              ▼              ▼
候选列表      短名单        评分报告      适配版本      MindSymphony
(20+)         (5-8)         (Top 3)       (1-2)         集成完成
```

---

## Phase 1: 检索 (Search)

### 核心资源库（按优先级排序）

| 优先级 | 仓库 | 定位 | Stars |
|--------|------|------|-------|
| ⭐⭐⭐ | anthropics/skills | 官方精选库 | 33k+ |
| ⭐⭐⭐ | ComposioHQ/awesome-claude-skills | 实用技能百科 | 14.7k+ |
| ⭐⭐ | agentskills/agentskills | 开放标准核心 | 4.4k+ |
| ⭐⭐ | muratcankoylan/Agent-Skills-for-Context-Engineering | 上下文工程 | 5.6k+ |
| ⭐ | heilcheng/awesome-agent-skills | Awesome合集 | 888 |
| ⭐ | TKassis/claude-scientific-skills | 科学计算 | 2.6k+ |
| ⭐ | gotalab/skillport | 技能管理器 | 200 |

### 检索策略

```markdown
## 检索模板

### 需求描述
[用1-2句话描述你需要什么能力]

### 关键词提取
- 领域关键词：[如 academic, finance, medical]
- 功能关键词：[如 writing, analysis, generation]
- 格式关键词：[如 docx, pdf, chart]

### 搜索命令
```bash
# GitHub搜索
gh search repos "claude skill [关键词]" --limit 20

# 或直接在以下仓库内搜索
# 1. github.com/anthropics/skills
# 2. github.com/ComposioHQ/awesome-claude-skills
# 3. github.com/agentskills/agentskills
```

### 输出
- 候选Skill列表（20+个）
- 每个记录：名称、来源、简介、链接
```

---

## Phase 2: 筛选 (Filter)

### 快速过滤清单

```markdown
## 筛选检查表

### 硬性条件（必须满足）
- [ ] 有SKILL.md或README说明
- [ ] 最近6个月有更新
- [ ] 与需求领域相关
- [ ] 许可证允许使用

### 软性条件（加分项）
- [ ] Stars > 100
- [ ] 有使用示例
- [ ] 有维护者响应issues
- [ ] 社区有正面反馈

### 排除条件（直接淘汰）
- [ ] 纯广告/营销内容
- [ ] 明显过时（依赖已废弃）
- [ ] 代码混淆/不可读
- [ ] 安全风险（如要求危险权限）
```

### 筛选输出

```markdown
## 短名单（5-8个）

| # | Skill名称 | 来源 | 相关度 | 质量初判 |
|---|-----------|------|--------|----------|
| 1 | [name] | [repo] | 高/中/低 | ⭐⭐⭐⭐ |
| 2 | ... | ... | ... | ... |
```

---

## Phase 3: 评估 (Evaluate)

### 评估维度（总分100分）

| 维度 | 权重 | 评估要点 |
|------|------|----------|
| **功能匹配** | 30% | 是否解决核心问题 |
| **代码质量** | 25% | 结构清晰、可维护 |
| **文档完整** | 20% | 说明清楚、示例充分 |
| **社区活跃** | 15% | Stars、更新频率、issue响应 |
| **适配难度** | 10% | 与MindSymphony的兼容性 |

### 评估模板

```markdown
## Skill评估报告

### 基本信息
- **名称**：[skill name]
- **来源**：[github link]
- **版本**：[version]
- **许可证**：[license]

### 功能匹配（30分）
- 核心功能覆盖：[X/10]
- 边缘场景支持：[X/10]
- 扩展潜力：[X/10]
- **小计**：[X/30]

### 代码质量（25分）
- 结构清晰度：[X/10]
- 错误处理：[X/8]
- 依赖合理性：[X/7]
- **小计**：[X/25]

### 文档完整（20分）
- SKILL.md规范：[X/8]
- 使用示例：[X/7]
- 安装说明：[X/5]
- **小计**：[X/20]

### 社区活跃（15分）
- Stars数量：[X/5]
- 更新频率：[X/5]
- Issue响应：[X/5]
- **小计**：[X/15]

### 适配难度（10分）
- 架构兼容：[X/4]
- 风格一致：[X/3]
- 改动量预估：[X/3]
- **小计**：[X/10]

### 总分：[X/100]

### 评估结论
- **推荐等级**：A/B/C/D
- **适配建议**：[具体建议]
- **风险提示**：[潜在问题]
```

---

## Phase 4: 适配 (Adapt)

### MindSymphony风格规范

```markdown
## 适配检查清单

### 1. Frontmatter标准化
```yaml
---
name: [小写-连字符]
module: [所属模块]
layer: [dao/fa/shu/qi]
triggers: [触发词列表]
type: [execution/analytical/creative]
source: [原始来源]
---
```

### 2. 文档结构统一
- 标题：中英文双语
- 开头：一句话定位 + 引用格式
- 核心能力：3个主要能力
- 工作流程：分阶段描述
- 使用示例：至少2个
- 质量标准：DO/DON'T
- 信心赋予：结尾鼓励语

### 3. 命名规范
- 文件名：小写-连字符.md
- 目录：归入正确的extensions分类
- 触发词：中英文都要有

### 4. 风格调整
- 移除营销语言
- 统一术语表达
- 添加MindSymphony特有元素
```

### 适配模板

```markdown
## 适配转换记录

### 原始信息
- 来源：[original repo]
- 原名：[original name]
- 原结构：[描述]

### 转换决策
| 原始 | 适配后 | 理由 |
|------|--------|------|
| [原名] | [新名] | [理由] |
| [原结构] | [新结构] | [理由] |

### 改动清单
1. [ ] Frontmatter重写
2. [ ] 文档结构调整
3. [ ] 示例本地化
4. [ ] 触发词添加
5. [ ] 质量标准补充

### 验证
- [ ] 通过validate_skill.py
- [ ] 触发词测试
- [ ] 功能测试
```

---

## Phase 5: 集成 (Integrate)

### 集成到MindSymphony

```bash
# 1. 放置文件
cp adapted-skill.md ~/.claude/skills/mindsymphony/extensions/[module]/

# 2. 更新INDEX
# 编辑 extensions/[module]/_INDEX.md，添加新skill

# 3. 验证
python3 validate_skill.py ~/.claude/skills/mindsymphony

# 4. 测试
# 在Claude Code中测试触发词
```

### 注册表更新

```yaml
# mindsymphony/registry.yml (新增)
external_skills:
  - name: [skill-name]
    source: [github-url]
    adapted_at: [date]
    version: [version]
    location: extensions/[module]/[skill-name].md
```

---

## 快速参考

### 一键检索命令

```bash
# 搜索官方库
curl -s "https://api.github.com/repos/anthropics/skills/contents" | jq '.[] | .name'

# 搜索awesome列表
curl -s "https://raw.githubusercontent.com/ComposioHQ/awesome-claude-skills/main/README.md" | grep -E "^\-\s\[" 
```

### 评估快速打分

```
90-100: A级 - 直接适配
70-89:  B级 - 小幅修改后适配
50-69:  C级 - 需要较大改动
<50:    D级 - 不推荐，重新寻找
```

### 适配时间估算

| 原始质量 | 适配时间 |
|----------|----------|
| A级 | 15-30分钟 |
| B级 | 30-60分钟 |
| C级 | 1-2小时 |

---

## 使用示例

### 示例1：寻找图表生成skill

```markdown
**需求**：需要一个能生成信息图的skill

**检索**：
- 关键词：infographic, chart, visualization
- 搜索范围：anthropics/skills, awesome-claude-skills

**筛选结果**：
1. anthropics/skills/infographics ⭐⭐⭐⭐⭐
2. some-repo/chart-maker ⭐⭐⭐

**评估**：
- infographics: 92分 (A级)
- chart-maker: 68分 (C级)

**决策**：选择infographics，直接适配

**适配**：
- 重命名为 visual-infographic.md
- 归入 extensions/creative/
- 添加中文触发词
```

### 示例2：寻找法律文档skill

```markdown
**需求**：需要处理合同审查的skill

**检索**：
- 关键词：legal, contract, review
- 搜索范围：全部核心仓库

**筛选结果**：
1. composio/legal-docs ⭐⭐⭐
2. agentskills/contract-analyzer ⭐⭐

**评估**：
- legal-docs: 75分 (B级)
- contract-analyzer: 58分 (C级)

**决策**：选择legal-docs，需小幅修改

**适配**：
- 重命名为 legal-contract.md
- 归入 extensions/domains/legal/
- 补充中国法律相关示例
```

---

## 与MindSymphony的协同

| 阶段 | 调用的MindSymphony能力 |
|------|------------------------|
| 检索 | knowledge-explorer |
| 筛选 | quality-gate |
| 评估 | efficacy-evaluator |
| 适配 | skill-forge |
| 集成 | config-validation |

---

## 信心赋予

**"站在巨人的肩膀上，但要穿自己的鞋。"**

外部Skill是宝贵的资源，但需要：
- 严格筛选，确保质量
- 深度适配，融入体系
- 持续迭代，形成生态

通过标准化的策展流程，让每一个引入的Skill都成为MindSymphony的有机组成部分。
