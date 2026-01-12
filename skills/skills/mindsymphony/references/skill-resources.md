# Skill 资源索引 (Skill Resource Index)

> 截至 2026年1月，主流Skill仓库速查表

---

## 🏆 核心仓库（必查）

### 1. anthropics/skills（官方精选）
- **链接**：https://github.com/anthropics/skills
- **Stars**：33k+
- **定位**：Anthropic官方维护的Agent Skills公共库
- **特点**：
  - 16+ 个官方skill
  - 文档处理（docx/pdf/pptx/xlsx）
  - 创意设计、自动化
  - skill-creator等元能力
- **推荐指数**：⭐⭐⭐⭐⭐

### 2. ComposioHQ/awesome-claude-skills（实用百科）
- **链接**：https://github.com/ComposioHQ/awesome-claude-skills
- **Stars**：14.7k+
- **定位**：由Composio维护的社区精选集
- **特点**：
  - 分类齐全：文档、Git、代码、设计、研究、取证
  - 安装指南完整
  - 入门门槛低
- **推荐指数**：⭐⭐⭐⭐⭐

### 3. agentskills/agentskills（开放标准）
- **链接**：https://github.com/agentskills/agentskills
- **Stars**：4.4k+
- **定位**：Agent Skills标准的核心库
- **特点**：
  - 支持多平台（Claude/Cursor/Copilot）
  - 规范、示例、贡献指南
  - 被视为"标准起点"
- **推荐指数**：⭐⭐⭐⭐

---

## 🌟 专项仓库

### 4. muratcankoylan/Agent-Skills-for-Context-Engineering
- **链接**：https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering
- **Stars**：5.6k+
- **定位**：专注"上下文工程"的MCP技能集
- **特点**：
  - 退化避免、多智能体协调
  - 内存系统设计
  - 评估框架
- **适合**：构建复杂Agent系统
- **推荐指数**：⭐⭐⭐⭐

### 5. TKassis/claude-scientific-skills
- **链接**：https://github.com/TKassis
- **Stars**：2.6k+
- **定位**：科学计算、数据分析、ML、金融
- **特点**：
  - 数值稳定性
  - 模拟计算
  - ML工程
- **适合**：科研、量化分析
- **推荐指数**：⭐⭐⭐⭐

### 6. kirodotdev/powers
- **链接**：https://github.com/kirodotdev/powers
- **Stars**：新兴
- **定位**：Claude Skills强化版（Powers）
- **特点**：
  - 按需加载上下文
  - 避免上下文过载
  - 专为Kiro代理设计
- **推荐指数**：⭐⭐⭐

---

## 📚 Awesome合集

### 7. heilcheng/awesome-agent-skills
- **链接**：https://github.com/heilcheng/awesome-agent-skills
- **Stars**：888
- **定位**：Curated各种Skill的教程和工具
- **特点**：
  - 支持多平台（Claude/Copilot/VSCode）
  - 一站式查找
- **推荐指数**：⭐⭐⭐

### 8. skillmatic-ai/awesome-agent-skills
- **链接**：https://github.com/skillmatic-ai/awesome-agent-skills
- **定位**：强调可组合架构的榜单
- **特点**：
  - 模块化能力
  - 架构优化导向
- **推荐指数**：⭐⭐⭐

---

## 🛠️ 工具类

### 9. gotalab/skillport
- **链接**：https://github.com/gotalab/skillport
- **Stars**：200
- **定位**：Skill管理神器
- **特点**：
  - 从GitHub/Repo搜索、添加、同步
  - 支持Claude Code/Cursor
- **推荐指数**：⭐⭐⭐

---

## 快速检索命令

```bash
# 1. 搜索GitHub上的claude skill
gh search repos "claude skill" --sort stars --limit 20

# 2. 搜索特定领域
gh search repos "claude skill medical" --limit 10
gh search repos "claude skill finance" --limit 10
gh search repos "claude skill academic" --limit 10

# 3. 查看官方库内容
gh api repos/anthropics/skills/contents | jq '.[].name'

# 4. 克隆整个官方库
git clone https://github.com/anthropics/skills.git ~/.claude/skills/anthropic-official
```

---

## 分类速查

| 需求领域 | 优先查找 | 备选 |
|----------|----------|------|
| 文档处理 | anthropics/skills | ComposioHQ |
| 代码开发 | agentskills | muratcankoylan |
| 科学计算 | TKassis | - |
| 创意设计 | anthropics/skills | ComposioHQ |
| Agent开发 | muratcankoylan | agentskills |
| 法律/金融 | ComposioHQ | awesome合集 |

---

## MindSymphony已集成

| 来源 | 已集成Skill | 状态 |
|------|-------------|------|
| anthropics/skills | docx, pdf, pptx, xlsx | ✅ v18.2 |
| anthropics/skills | skill-creator | ✅ 融合为skill-forge |
| 原创 | 90个核心+扩展技能 | ✅ v18.3 |

---

## 待评估清单

| 仓库 | Skill | 优先级 | 状态 |
|------|-------|--------|------|
| TKassis | scientific-skills | 高 | 待评估 |
| muratcankoylan | context-engineering | 中 | 待评估 |
| kirodotdev | powers | 低 | 观望 |

---

*更新时间：2026年1月*
