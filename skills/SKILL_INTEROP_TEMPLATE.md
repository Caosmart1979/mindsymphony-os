# 技能互操作模板 (Skill Interoperability Template)

> 将此模板复制到你的技能目录，填写协作信息。

---

## 快速开始

1. 复制 `INTEROP.yml` 到你的技能目录
2. 填写协作信息
3. 在 `SKILL.md` 中添加互操作章节

---

## 文件 1: INTEROP.yml

将此文件放在技能根目录：

```yaml
# 技能互操作元数据
# 填写此文件以声明你的技能的协作能力

# === 基础信息 ===
skill_id: "your-skill-name"
version: "1.0.0"

# === 分类 ===
# 选择一个主分类：design, create, document, workflow, analysis, meta
category: "design"

# === 标签 ===
# 用于技能发现的关键词
tags:
  - "frontend"
  - "ui"
  - "react"
  - "css"

# === 提供的能力 ===
# 列出此技能提供给其他技能的能力/资源
provides:
  - id: "design-tokens"
    description: "标准化的设计令牌（颜色、字体、间距）"
    format: "json"
    location: "references/tokens.json"

  - id: "component-templates"
    description: "React 组件模板"
    format: "tsx"
    location: "assets/components/"

# === 消耗的能力（可选）===
# 列出此技能可以从其他技能使用的能力/资源
consumes:
  - id: "brand-guidelines"
    description: "品牌规范（颜色、字体、标识）"
    optional: true  # true = 可选，false = 必需
    fallback: "使用默认样式"

  - id: "user-assets"
    description: "用户提供的资源（图片、图标等）"
    optional: true
    fallback: "使用占位符"

# === 相关技能 ===
# 仅用于发现，不表示依赖关系
related:
  - "brand-guidelines"
  - "canvas-design"
  - "theme-factory"

# === 参考文档 ===
see_also:
  - "SKILL_INTEROPERABILITY_PROTOCOL.md"
  - "https://example.com/guide"

# === 输入类型 ===
inputs:
  - type: "design-brief"
    description: "设计需求描述"
    required: true

  - type: "design-tokens"
    description: "设计令牌"
    required: false

# === 输出类型 ===
outputs:
  - type: "react-components"
    description: "React/TSX 组件代码"

  - type: "css-styles"
    description: "CSS 样式代码"

# === 触发条件 ===
triggers:
  - level: "high"
    keywords:
      - "前端"
      - "UI"
      - "网页"
      - "组件"
      - "React"
      - "Vue"

  - level: "medium"
    keywords:
      - "界面"
      - "视觉"
      - "设计"

# === 前置条件 ===
prerequisites:
  - condition: "如需品牌规范，应先应用 brand-guidelines 技能"
    optional: true
  - condition: "如需图标资源，应在 assets/ 目录提供"
    optional: true
```

---

## 文件 2: SKILL.md 互操作章节

在 `SKILL.md` 中添加以下章节：

```markdown
---
name: your-skill
description: "你的技能描述"

# 添加协作元数据
category: design
tags: [frontend, ui, react]
provides: [design-tokens, component-templates]
consumes: [brand-guidelines, user-assets]
related: [brand-guidelines, canvas-design]
---

# 你的技能内容

## 互操作支持

本技能支持与其他技能协作。

### 提供的能力

本技能向其他技能提供以下能力：

#### 设计令牌 (design-tokens)

提供标准化的设计令牌，包括：
- 颜色规范
- 字体规范
- 间距系统

**格式**: JSON
**位置**: `references/tokens.json`
**使用方式**: 其他技能可读取此文件获取设计令牌

#### 组件模板 (component-templates)

提供可复用的 React 组件模板。

**格式**: TSX
**位置**: `assets/components/`
**使用方式**: 其他技能可直接使用或修改这些模板

### 消耗的能力

本技能可以从其他技能使用以下能力（均为可选）：

#### 品牌规范 (brand-guidelines)

- **来源**: `brand-guidelines` 技能
- **用途**: 应用品牌颜色和字体
- **行为**: 如检测到 `brand-guidelines` 已应用，自动使用其设计令牌
- **回退**: 如无品牌规范，使用默认样式

#### 用户资源 (user-assets)

- **来源**: 用户提供的 `assets/` 目录
- **用途**: 使用自定义图片、图标等资源
- **行为**: 读取并使用 `assets/` 中的文件
- **回退**: 如无资源，使用占位符或生成式内容

### 相关技能

与以下技能有协作关系：

- **brand-guidelines**: 提供品牌规范
- **canvas-design**: 画布设计
- **theme-factory**: 主题生成

### 样式继承协议

本技能支持灵活的样式系统：

1. **检查其他技能**: 首先检查是否有 `brand-guidelines` 或其他提供设计令牌的技能
2. **应用令牌**: 如有，读取并应用其设计令牌
3. **用户覆盖**: 用户可明确指定覆盖任何样式值
4. **默认行为**: 如无其他技能提供令牌，使用本技能的默认样式

### 工作流集成

本技能可在以下工作流阶段使用：

- **设计阶段**: 创建初始设计
- **原型阶段**: 生成可交互原型
- **实现阶段**: 生成生产代码

工作流状态格式遵循 [技能互操作协议](SKILL_INTEROPERABILITY_PROTOCOL.md)。
```

---

## 示例：完整的 frontend-design INTEROP.yml

```yaml
# frontend-design 技能互操作元数据
skill_id: "frontend-design"
version: "1.0.0"

category: "design"

tags:
  - "frontend"
  - "ui"
  - "web"
  - "react"
  - "vue"
  - "html"
  - "css"

provides:
  - id: "design-tokens"
    description: "自适应设计令牌"
    format: "json"
    location: "references/design-tokens.json"

  - id: "component-templates"
    description: "React/Vue 组件模板"
    format: "tsx/vue"
    location: "assets/components/"

consumes:
  - id: "brand-guidelines"
    description: "品牌规范"
    optional: true
    fallback: "使用自适应设计系统"

  - id: "design-tokens"
    description: "外部设计令牌"
    optional: true
    fallback: "生成设计令牌"

related:
  - "brand-guidelines"
  - "canvas-design"
  - "theme-factory"
  - "artifacts-builder"
  - "algorithmic-art"

inputs:
  - type: "design-brief"
    description: "设计需求描述"
    required: true

  - type: "design-tokens"
    description: "设计令牌"
    required: false

  - type: "component-specs"
    description: "组件规格说明"
    required: false

outputs:
  - type: "react-components"
    description: "React/TSX 组件代码"

  - type: "vue-components"
    description: "Vue/SFC 组件代码"

  - type: "html-css"
    description: "HTML/CSS 代码"

triggers:
  - level: "high"
    keywords:
      - "前端"
      - "UI"
      - "网页"
      - "网站"
      - "组件"
      - "React"
      - "Vue"
      - "HTML"
      - "CSS"
      - "界面"
      - "dashboard"
      - "landing page"

  - level: "medium"
    keywords:
      - "设计"
      - "视觉"
      - "样式"
      - "美化"

prerequisites:
  - condition: "品牌规范: 使用 brand-guidelines 技能以获得一致的品牌样式"
    optional: true
  - condition: "设计令牌: 从其他技能获取设计令牌以保持一致性"
    optional: true
```

---

## 示例：完整的 brand-guidelines INTEROP.yml

```yaml
# brand-guidelines 技能互操作元数据
skill_id: "brand-guidelines"
version: "1.0.0"

category: "design"

tags:
  - "brand"
  - "design"
  - "style"
  - "colors"
  - "typography"

provides:
  - id: "brand-guidelines"
    description: "Anthropic 官方品牌规范"
    format: "json"
    location: "references/brand-tokens.json"

  - id: "design-tokens"
    description: "品牌设计令牌"
    format: "json"
    location: "references/brand-tokens.json"

consumes: []  # 无依赖

related:
  - "frontend-design"
  - "canvas-design"
  - "pptx"
  - "docx"

inputs:
  - type: "brand-identity"
    description: "品牌标识信息"
    required: false

outputs:
  - type: "design-tokens"
    description: "设计令牌（颜色、字体等）"

  - type: "styled-document"
    description: "应用品牌样式的文档"

triggers:
  - level: "high"
    keywords:
      - "品牌"
      - "品牌规范"
      - "样式"
      - "Anthropic"
      - "brand colors"

  - level: "medium"
    keywords:
      - "颜色"
      - "字体"
      - "样式规范"

prerequisites: []  # 无前置条件
```

---

## 验证清单

使用此清单确保你的技能正确实现了互操作：

- [ ] `INTEROP.yml` 文件存在且格式正确
- [ ] `SKILL.md` frontmatter 包含协作元数据
- [ ] `SKILL.md` 包含"互操作支持"章节
- [ ] 所有 `provides` 资源在指定位置存在
- [ ] 所有 `consumes` 资源都有回退方案
- [ ] `related` 技能确实相关
- [ ] 触发关键词准确反映技能用途
- [ ] 文档说明清晰完整

---

## 下一步

1. 填写 `INTEROP.yml`
2. 更新 `SKILL.md`
3. 运行验证工具（如可用）
4. 测试与其他技能的协作

---

## 需要帮助？

- 查看完整协议: [SKILL_INTEROPERABILITY_PROTOCOL.md](SKILL_INTEROPERABILITY_PROTOCOL.md)
- 查看示例技能: `frontend-design/`, `brand-guidelines/`
- 提交问题: 在技能仓库创建 issue
