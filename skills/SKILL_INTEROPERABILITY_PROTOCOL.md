# 技能互操作协议 (Skill Interoperability Protocol v1.0)

> **"松耦合、强协作"** - 技能间通过轻量级接口协作，而非硬编码依赖。

---

## 核心原则

1. **无硬编码依赖** - 技能不应直接引用其他技能的名称
2. **声明式能力** - 通过元数据声明能力，而非通过代码逻辑
3. **可选协作** - 协作是增强，非必需
4. **版本兼容** - 接口设计向后兼容

---

## 协议层

技能协作分为三个层次：

```
┌─────────────────────────────────────────────────┐
│  Layer 3: 内容协作 (Content Collaboration)      │
│  数据格式、结构约定、令牌传递                      │
├─────────────────────────────────────────────────┤
│  Layer 2: 能力声明 (Capability Declaration)     │
│  输入/输出类型、触发条件、前置条件                  │
├─────────────────────────────────────────────────┤
│  Layer 1: 发现协议 (Discovery Protocol)         │
│  元数据、分类、标签、关系声明                      │
└─────────────────────────────────────────────────┘
```

---

## Layer 1: 发现协议

### 1.1 扩展元数据

技能的 YAML frontmatter 应包含可选的协作字段：

```yaml
---
name: my-skill
description: "技能描述"

# 协作元数据（可选）
version: "1.0.0"
category: "design"           # 分类：design, create, document, workflow, etc.
tags:                        # 标签：用于发现
  - frontend
  - ui
  - react

provides:                   # 提供的能力/资源
  - design-tokens           # 设计令牌
  - component-templates     # 组件模板

consumes:                   # 消耗的能力/资源（可选）
  - brand-guidelines        # 需要品牌规范
  - user-assets             # 需要用户资源

related:                    # 相关技能（仅用于发现）
  - brand-guidelines        # 相关技能名称
  - canvas-design
  - theme-factory

see_also:                   # 参考文档
  - "SKILL_DESIGN_PATTERNS.md"
  - "https://example.com/guide"
---
```

### 1.2 分类标准

| 分类 | 说明 | 示例技能 |
|------|------|---------|
| `design` | 视觉、设计、创意 | frontend-design, canvas-design, brand-guidelines |
| `create` | 创建工具、构建 | skill-creator, mcp-builder, doc-skill-generator |
| `document` | 文档处理 | doc-coauthoring, official-writer, docx |
| `workflow` | 工作流、流程 | mindsymphony, doc-coauthoring |
| `analysis` | 分析、研究 | knowledge-explorer, structure-analysis |
| `meta` | 元能力 | cognitive-architect, skill-creator |

### 1.3 能力/资源类型

标准化的能力标识符：

| 资源类型 | 标识符 | 说明 |
|---------|--------|------|
| 设计令牌 | `design-tokens` | 颜色、字体、间距等设计规范 |
| 品牌规范 | `brand-guidelines` | 公司/品牌视觉识别 |
| 组件模板 | `component-templates` | 可复用的 UI 组件 |
| 文档模板 | `document-templates` | 文档结构模板 |
| 工作流状态 | `workflow-state` | 工作流阶段信息 |
| 数据模式 | `data-schema` | 数据结构定义 |
| API规范 | `api-specs` | API 文档 |

---

## Layer 2: 能力声明

### 2.1 输入/输出类型

技能应声明其接受的输入和产生的输出类型：

```yaml
# 在 SKILL.md 中添加

## 输入类型

接受以下输入格式：
- **设计令牌**: JSON/YAML 格式的颜色、字体规范
- **组件规格**: 包含 props 和行为的组件描述
- **用户资源**: 图片、图标等静态资源

## 输出类型

产生以下输出：
- **React 代码**: TypeScript/TSX 组件
- **CSS 样式**: 内联样式或 CSS 模块
- **设计文档**: 设计决策说明

## 前置条件

- 如需品牌规范，应先应用 `brand-guidelines` 技能
- 如需图标资源，应在 `assets/` 目录提供

## 后置效果

- 生成的代码可直接在 React 环境运行
- 设计令牌已转换为 CSS 变量
```

### 2.2 触发条件

技能应明确其触发条件：

```yaml
## 触发条件

当以下情况时建议使用本技能：
- 用户提到 "前端"、"UI"、"网页"、"组件"
- 用户提到 "React"、"Vue"、"HTML"、"CSS"
- 用户请求构建界面、设计页面、美化 UI

## 触发优先级

- 高优先级: 明确提到前端框架或设计需求
- 中优先级: 提到界面、视觉相关
- 低优先级: 一般性开发任务
```

---

## Layer 3: 内容协作

### 3.1 设计令牌协议

设计类技能应支持标准化的设计令牌格式：

```json
{
  "version": "1.0",
  "tokens": {
    "color": {
      "primary": "#141413",
      "secondary": "#d97757",
      "accent": "#6a9bcc"
    },
    "typography": {
      "heading": "Poppins",
      "body": "Lora"
    },
    "spacing": {
      "xs": "4px",
      "sm": "8px",
      "md": "16px",
      "lg": "24px"
    }
  }
}
```

### 3.2 样式覆盖协议

技能应支持从其他技能继承和覆盖样式：

```yaml
## 样式继承

本技能支持以下样式继承机制：

1. **读取设计令牌**: 检查 `brand-guidelines` 技能是否已应用
2. **应用默认值**: 如无设计令牌，使用默认样式
3. **允许覆盖**: 用户可明确指定覆盖任何令牌

### 实现

```python
# 伪代码示例
def get_design_tokens():
    if has_skill_context('brand-guidelines'):
        return load_skill_tokens('brand-guidelines')
    return default_tokens
```

### 3.3 工作流状态协议

工作流类技能应使用标准化的状态表示：

```yaml
## 工作流状态

本技能使用以下状态机：

```
context_gathering → refinement → reader_testing → complete
         ↓              ↓           ↓
      (可跳过)      (迭代)      (可跳过)
```

### 状态令牌

状态信息存储在以下格式中：

```yaml
workflow:
  stage: "refinement"
  current_section: "technical_approach"
  iteration: 2
  completed_sections:
    - "introduction"
    - "background"
```

### 3.4 文档互操作协议

文档类技能应支持文档状态的传递：

```yaml
## 文档状态

### 输入文档状态

接受以下文档状态信息：

```yaml
document:
  stage: "draft"  # draft, review, final
  sections:
    - name: "introduction"
      status: "complete"
    - name: "technical_approach"
      status: "in_progress"
  metadata:
    template: "technical-spec"
    version: "1.0"
```

### 输出文档状态

输出包含更新状态的文档信息，供后续技能使用。

---

## 互操作最佳实践

### DO ✅

1. **使用 `provides/consumes` 声明能力** - 让其他技能能发现你
2. **标准化数据格式** - 使用 JSON/YAML 等可交换格式
3. **支持可选协作** - 技能应能独立工作，协作是增强
4. **文档化接口** - 在 SKILL.md 中清晰说明输入/输出
5. **使用分类和标签** - 帮助技能发现

### DON'T ❌

1. **硬编码技能名称** - 不要直接引用其他技能
2. **强制依赖** - 不要让其他技能成为必需
3. **破坏性变更** - 接口变更应保持向后兼容
4. **过度设计** - 协作接口应简单实用
5. **循环依赖** - 避免技能间的循环依赖

---

## 示例：重构 frontend-design

### Before (硬编码)

```markdown
## 品牌支持

本技能支持 Anthropic 品牌规范。使用 Poppins 和 Lora 字体...
```

### After (松耦合)

```yaml
---
name: frontend-design
description: "..."
category: design
tags: [frontend, ui, react]
provides: [component-templates, design-tokens]
consumes: [brand-guidelines, user-assets]
related: [brand-guidelines, canvas-design]
---

## 样式系统

本技能支持灵活的样式系统：

### 默认样式

如无其他技能提供设计令牌，使用以下默认值：
- 颜色: 自适应选择
- 字体: 系统字体栈

### 协作支持

当 `brand-guidelines` 技能已应用时，自动使用其设计令牌：
- 读取 `brand-guidelines` 提供的颜色和字体规范
- 应用到所有生成的组件

用户也可明确指定覆盖任何样式值。
```

---

## 工具支持

### 技能发现工具

```bash
# 查找所有提供 design-tokens 的技能
skill-registry query --provides design-tokens

# 查找所有 brand-guidelines 相关技能
skill-registry query --related brand-guidelines

# 查找所有 design 分类技能
skill-registry query --category design
```

### 验证工具

```bash
# 验证技能互操作元数据
skill-validator check-interoperability frontend-design/

# 检测循环依赖
skill-validator check-circular-dependencies
```

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2025-01-08 | 初始版本 |
