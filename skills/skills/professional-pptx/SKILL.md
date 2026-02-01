---
name: professional-pptx
description: "专业演示文稿制作技能，从内容到视觉的完整PPT工作流。Use when (1) 将学术论文/报告转化为PPT, (2) 创建会议演讲/商业汇报/学术答辩PPT, (3) 设计医学/科研领域专业幻灯片, (4) 制作内容密集型信息展示PPT, (5) 优化现有PPT的结构和视觉设计。Triggers: PPT, 幻灯片, presentation, slide deck, 演讲稿, keynote, 学术报告, 项目汇报, 答辩PPT"
---

# Professional Presentation Creator

从内容提炼到视觉呈现的端到端PPT制作系统，专注于学术/医学/商业领域的专业演示。

```
PPT制作的本质：让复杂信息在有限时间内被理解和记住

    原始内容 (论文/报告/数据)
            │
            ▼
    结构提炼 (故事线+信息层级)
            │
            ▼
    视觉转化 (布局+设计系统)
            │
            ▼
    专业输出 (.pptx文件)
```

---

## Master Navigation

```
您需要什么？
│
├─► 从零开始制作PPT
│   ├─► 有明确内容/文档 → Phase 1: 内容分析
│   ├─► 只有主题/方向 → Phase 0: 素材收集
│   └─► 参考模板制作 → 使用模板工作流
│
├─► 内容转PPT
│   ├─► 学术论文 → references/modules/academic-slides.md
│   ├─► 数据报告 → references/modules/data-presentation.md
│   ├─► 项目汇报 → references/modules/business-deck.md
│   └─► 医学演讲 → references/modules/medical-slides.md
│
├─► 设计与美化
│   ├─► 选择设计风格 → references/core/design-systems.md
│   ├─► 颜色与字体 → references/core/typography-color.md
│   ├─► 布局模式 → references/core/layout-patterns.md
│   └─► 图表可视化 → references/core/data-visualization.md
│
├─► 技术实现
│   ├─► html2pptx工作流 → references/core/technical-guide.md
│   ├─► 模板编辑 → /mnt/skills/public/pptx/SKILL.md
│   └─► 脚本工具 → scripts/
│
└─► ⚠️ 常见问题
    ├─► 内容太多装不下 → #content-overflow
    ├─► 视觉效果不专业 → #visual-polish
    ├─► 文字显示异常 → #text-rendering
    └─► 输出文件损坏 → #file-corruption
```

---

## Phase 0: 需求理解与素材准备

### Quick Decision

```
用户提供了什么？
├─► 完整文档/论文 → 直接进入Phase 1
├─► 数据表格/图表 → 评估数据故事，进入Phase 1
├─► 仅主题关键词 → 先进行素材收集
├─► 参考PPT模板 → 使用模板工作流
└─► 口头描述需求 → 先明确以下问题
```

### 必须明确的5个问题

1. **受众是谁？** 专家/决策者/普通听众 → 决定专业深度
2. **场合是什么？** 学术会议/商业汇报/内部培训 → 决定风格调性
3. **时长多少？** → 决定幻灯片数量（约1-2分钟/页）
4. **核心目的？** 说服/教育/汇报/展示 → 决定内容结构
5. **有无特殊要求？** 模板/配色/字体限制

---

## Phase 1: 内容分析与结构设计

### 学术内容的黄金结构

```
学术PPT标准结构 (15-20页)
│
├─► 开篇 (1-2页)
│   └─► 标题页 + 研究背景/问题
│
├─► 方法 (2-4页)
│   └─► 研究设计 + 关键方法
│
├─► 结果 (4-8页)
│   └─► 核心发现 + 数据可视化
│
├─► 讨论 (2-3页)
│   └─► 意义 + 局限 + 未来方向
│
└─► 结尾 (1-2页)
    └─► 结论 + 致谢/联系方式
```

### 内容精炼原则

| 原始内容 | PPT转化 | 比例 |
|---------|---------|------|
| 论文摘要 | 1-2个核心观点 | 1:5 |
| 方法章节 | 流程图+关键步骤 | 1:10 |
| 结果表格 | 精选图表+高亮数据 | 1:3 |
| 讨论段落 | 3-5个要点 | 1:8 |

**核心原则：每页PPT只传达1个主要信息**

→ 详见 references/core/content-extraction.md

---

## Phase 2: 故事线设计

### 演讲结构模式

```
选择你的叙事结构
│
├─► 问题-解决型 (学术/商业通用)
│   问题 → 方法 → 结果 → 意义
│
├─► 时间线型 (项目汇报)
│   背景 → 过程 → 现状 → 展望
│
├─► 对比型 (方案选择)
│   现状 → 痛点 → 方案A vs B → 推荐
│
├─► 金字塔型 (商业汇报)
│   结论 → 支撑论点 → 详细数据
│
└─► 教学型 (培训)
    概念 → 原理 → 示例 → 练习
```

### 故事线工作表

```markdown
## PPT故事线

**核心信息（一句话）**: ________________

**开场钩子**: ________________

**3个关键支撑点**:
1. ________________
2. ________________
3. ________________

**高潮/转折点**: ________________

**行动呼吁/结论**: ________________
```

→ 详见 references/core/storyline-design.md

---

## Phase 3: 视觉设计系统

### Quick Decision: 选择设计方向

```
你的演讲场合？
│
├─► 学术会议
│   ├─► 国际会议 → 简约专业 (Minimal Academic)
│   └─► 国内答辩 → 稳重清晰 (Classic Academic)
│
├─► 商业汇报
│   ├─► 高层决策 → 精炼商务 (Executive)
│   ├─► 投资路演 → 现代大胆 (Bold Startup)
│   └─► 内部团队 → 清爽实用 (Clean Corporate)
│
├─► 医学/科研
│   ├─► 临床研究 → 专业医学 (Medical Professional)
│   └─► 科普教育 → 友好清晰 (Science Communication)
│
└─► 特殊场合
    ├─► 技术分享 → 工程风格 (Technical)
    └─► 创意展示 → 杂志风格 (Editorial)
```

### 设计系统三要素

| 要素 | 学术风格 | 商业风格 | 医学风格 |
|------|---------|---------|---------|
| **主色** | 深蓝#1a365d | 深灰#2d3748 | 医疗蓝#0077b6 |
| **强调** | 橙色#ed8936 | 品牌色 | 绿色#38a169 |
| **字体** | 衬线标题+无衬线正文 | 统一无衬线 | 清晰无衬线 |
| **密度** | 中等 | 稀疏 | 中等 |

→ 详见 references/core/design-systems.md

---

## Phase 4: 布局与排版

### 常用布局模式

```
布局速查 (960×540px画布)
│
├─► 标题页
│   ├─► 居中大标题 → layout-title-centered
│   └─► 左对齐+背景 → layout-title-editorial
│
├─► 内容页
│   ├─► 标题+要点列表 → layout-bullets
│   ├─► 左图右文 → layout-split-image-text
│   ├─► 2-3列卡片 → layout-cards
│   └─► 全幅图表 → layout-full-chart
│
├─► 数据页
│   ├─► 单图表+解读 → layout-chart-annotation
│   ├─► 多图表对比 → layout-chart-grid
│   └─► 表格展示 → layout-table
│
└─► 过渡页
    └─► 章节分隔 → layout-section-divider
```

### 空间分配原则

```
垂直空间分配 (540px高度)
─────────────────────────────
标题区域: 80-100px (含上边距)
─────────────────────────────
主内容区: 380-400px
─────────────────────────────
底部留白/脚注: 40-60px
─────────────────────────────

水平边距: 左右各20-40px
内容间距: 12-20px
```

→ 详见 references/core/layout-patterns.md

---

## Phase 5: 技术实现

### 工作流选择

```
选择技术路径
│
├─► 从头创建新PPT
│   └─► 使用html2pptx工作流
│       1. 设计HTML模板
│       2. 转换为PPTX
│       3. 视觉验证
│
├─► 基于模板创建
│   └─► 使用模板编辑工作流
│       1. 分析模板结构
│       2. 复制调整幻灯片
│       3. 替换内容
│
└─► 编辑现有PPT
    └─► 使用OOXML编辑工作流
        1. 解包PPT
        2. 编辑XML
        3. 重新打包
```

### html2pptx快速参考

```javascript
// 基本工作流
const pptxgen = require("pptxgenjs");
const { html2pptx } = require("./html2pptx");

const pptx = new pptxgen();
pptx.layout = "LAYOUT_16x9";

// 添加HTML幻灯片
await html2pptx("slide1.html", pptx);

// 添加带图表的幻灯片
const { slide, placeholders } = await html2pptx("slide2.html", pptx);
slide.addChart(pptx.charts.BAR, chartData, placeholders[0]);

await pptx.writeFile("output.pptx");
```

**⚠️ 关键提醒**:
- 必须先解压html2pptx库: `tar -xzf skills/public/pptx/html2pptx.tgz -C html2pptx`
- HTML画布尺寸: 960×540px (16:9)
- 颜色代码不带#: `"4472C4"` 而非 `"#4472C4"`

→ 详见 references/core/technical-guide.md 和 /mnt/skills/public/pptx/SKILL.md

---

## Phase 6: 质量验证

### 视觉检查清单

```bash
# 1. 转换为图片验证
soffice --headless --convert-to pdf output.pptx
pdftoppm -jpeg -r 150 output.pdf slide

# 2. 逐页检查
```

### 验证要点

| 检查项 | 标准 | 常见问题 |
|-------|------|---------|
| 文字可读性 | 最小14pt，高对比度 | 字号过小、对比不足 |
| 内容溢出 | 无裁切、无重叠 | 内容超出边界 |
| 对齐一致 | 元素对齐、间距一致 | 参差不齐 |
| 视觉层级 | 标题>副标题>正文 | 层级不清 |
| 品牌一致 | 配色/字体统一 | 风格混乱 |

---

## Resources

### Core References

| File | Purpose |
|------|---------|
| references/core/content-extraction.md | 内容精炼与信息层级 |
| references/core/storyline-design.md | 故事线设计与叙事结构 |
| references/core/design-systems.md | 设计系统与风格指南 |
| references/core/layout-patterns.md | 布局模式与空间分配 |
| references/core/typography-color.md | 字体与配色方案 |
| references/core/data-visualization.md | 数据可视化最佳实践 |
| references/core/technical-guide.md | 技术实现详细指南 |

### Domain Modules

| File | When to Use |
|------|-------------|
| references/modules/academic-slides.md | 学术论文转PPT |
| references/modules/medical-slides.md | 医学演讲专用 |
| references/modules/business-deck.md | 商业汇报模板 |
| references/modules/data-presentation.md | 数据驱动型演示 |

### Assets

| File | Purpose |
|------|---------|
| assets/templates/academic-template.html | 学术风格HTML模板 |
| assets/templates/business-template.html | 商业风格HTML模板 |
| assets/color-palettes.md | 预设配色方案 |

---

## Quick Start Checklist

- [ ] 明确受众、场合、时长、目的
- [ ] 提炼核心信息（一句话总结）
- [ ] 设计故事线（开头-主体-结尾）
- [ ] 选择设计系统（风格/配色/字体）
- [ ] 规划每页内容（1页1信息）
- [ ] 技术实现（html2pptx或模板）
- [ ] 视觉验证（转图片检查）

---

## ⚠️ 常见问题

<a id="content-overflow"></a>
### 内容太多装不下
- **症状**: 文字拥挤、溢出边界
- **方案**: 
  1. 拆分为多页
  2. 精简文字（目标：每页<50字）
  3. 用图表替代文字
  4. 降低字号（最小12pt）

<a id="visual-polish"></a>
### 视觉效果不专业
- **症状**: 看起来像"AI生成的"
- **方案**:
  1. 选择大胆的设计方向
  2. 使用统一的设计系统
  3. 增加留白
  4. 减少颜色数量（2-3种）

<a id="text-rendering"></a>
### 文字显示异常
- **症状**: 字体替换、乱码
- **方案**:
  1. 只使用Web安全字体
  2. 检查字体名称拼写
  3. 使用通用字体族

<a id="file-corruption"></a>
### 输出文件损坏
- **症状**: 无法打开PPTX
- **方案**:
  1. 颜色代码去掉#号
  2. 验证XML结构
  3. 检查图片路径
