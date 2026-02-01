# Design Systems Guide

PPT视觉设计系统的完整指南，包含预设风格和自定义方法。

---

## 设计系统选择器

```
你的场景是什么？
│
├─► 学术演讲
│   ├─► 国际会议 (英文)
│   │   └─► Minimal Academic
│   │       简约、专业、数据导向
│   │
│   ├─► 国内学术 (中文)
│   │   └─► Classic Academic
│   │       稳重、清晰、信息密集
│   │
│   └─► 毕业答辩
│       └─► Thesis Defense
│       正式、结构清晰、易于follow
│
├─► 商业汇报
│   ├─► 高管决策层
│   │   └─► Executive
│   │       精炼、结论导向、高对比
│   │
│   ├─► 投资/路演
│   │   └─► Bold Startup
│   │       现代、大胆、品牌感强
│   │
│   └─► 团队内部
│       └─► Clean Corporate
│       清爽、实用、易于协作
│
├─► 医学/科研
│   ├─► 临床研究汇报
│   │   └─► Medical Professional
│   │       专业蓝、数据严谨、可信度
│   │
│   └─► 科普/患者教育
│       └─► Science Communication
│       友好、清晰、易于理解
│
└─► 技术分享
    └─► Technical
    工程感、代码友好、信息密集
```

---

## 预设设计系统

### 1. Minimal Academic（简约学术）

**适用场景**: 国际学术会议、SCI期刊演讲、学术海报

```css
:root {
  /* 色彩系统 */
  --color-primary: #1a365d;      /* 深海蓝 - 标题、强调 */
  --color-secondary: #2b6cb0;    /* 学术蓝 - 次要元素 */
  --color-accent: #ed8936;       /* 暖橙 - 高亮、重点数据 */
  --color-text: #2d3748;         /* 深灰 - 正文 */
  --color-muted: #718096;        /* 中灰 - 说明文字 */
  --color-background: #ffffff;   /* 纯白背景 */
  --color-surface: #f7fafc;      /* 浅灰 - 卡片背景 */
  
  /* 字体系统 */
  --font-heading: Georgia, serif;           /* 标题 - 衬线 */
  --font-body: Arial, Helvetica, sans-serif; /* 正文 - 无衬线 */
  --font-mono: Courier New, monospace;       /* 代码/数据 */
  
  /* 字号层级 */
  --size-title: 36px;
  --size-h2: 24px;
  --size-body: 16px;
  --size-small: 12px;
  
  /* 间距 */
  --spacing-page: 40px;
  --spacing-section: 24px;
  --spacing-element: 12px;
}
```

**视觉特征**:
- 大量留白
- 单色系为主（蓝色梯度）
- 衬线标题 + 无衬线正文
- 数据用橙色高亮

**示例布局**:
```
┌─────────────────────────────────────────┐
│                 40px margin              │
│  ┌───────────────────────────────────┐  │
│  │ Title (Georgia, 36px, #1a365d)    │  │
│  └───────────────────────────────────┘  │
│                 24px                     │
│  ┌─────────────┐  12px  ┌─────────────┐ │
│  │   图表区域   │       │   要点区域   │ │
│  │  (#f7fafc)  │       │  (#ffffff)  │ │
│  └─────────────┘       └─────────────┘ │
│                 40px                     │
│  Source: xxx (12px, #718096)            │
└─────────────────────────────────────────┘
```

---

### 2. Medical Professional（医学专业）

**适用场景**: 临床研究汇报、学会演讲、病例讨论

```css
:root {
  /* 色彩系统 - 医疗蓝+生命绿 */
  --color-primary: #0077b6;      /* 医疗蓝 */
  --color-secondary: #00a896;    /* 医学绿 */
  --color-accent: #f77f00;       /* 警示橙 - 重要数据 */
  --color-danger: #d62828;       /* 风险红 */
  --color-success: #38a169;      /* 成功绿 */
  --color-text: #1a202c;
  --color-muted: #4a5568;
  --color-background: #ffffff;
  --color-surface: #f0f4f8;
  
  /* 字体系统 - 清晰可读 */
  --font-heading: Arial, Helvetica, sans-serif;
  --font-body: Arial, Helvetica, sans-serif;
  --font-mono: Courier New, monospace;
  
  /* 强调数据可读性 */
  --size-big-number: 48px;  /* 关键数据大字 */
  --size-title: 32px;
  --size-h2: 22px;
  --size-body: 16px;
  --size-caption: 11px;
}
```

**医学PPT特殊元素**:
- p值/CI高亮框
- 生存曲线配色
- 风险分层色块
- 安全性信号标记

**p值显示规范**:
```html
<!-- p < 0.05 显著 -->
<span class="p-significant">p < 0.001***</span>

<!-- p > 0.05 不显著 -->
<span class="p-nonsig">p = 0.234</span>
```

---

### 3. Executive（高管汇报）

**适用场景**: CEO汇报、董事会、投资者会议

```css
:root {
  /* 色彩系统 - 高对比、权威感 */
  --color-primary: #1a202c;      /* 近黑 */
  --color-secondary: #2d3748;    /* 深灰 */
  --color-accent: #3182ce;       /* 商务蓝 */
  --color-highlight: #48bb78;    /* 增长绿 */
  --color-warning: #ed8936;      /* 警示橙 */
  --color-text: #1a202c;
  --color-background: #ffffff;
  
  /* 字体 - 现代无衬线 */
  --font-heading: Arial, Helvetica, sans-serif;
  --font-body: Arial, Helvetica, sans-serif;
  
  /* 大字号层级 */
  --size-hero: 56px;    /* 核心数字 */
  --size-title: 40px;
  --size-h2: 28px;
  --size-body: 18px;
}
```

**高管PPT原则**:
- 每页一个核心信息
- 数字要大、结论要明确
- 最少的文字、最多的留白
- 颜色用于传递信息（红跌绿涨）

**Executive Summary 模板**:
```
┌─────────────────────────────────────────┐
│                                         │
│         +23%                            │
│   (56px, #48bb78, bold)                 │
│                                         │
│   Revenue Growth YoY                    │
│   (28px, #2d3748)                       │
│                                         │
│   ─────────────────────────────────     │
│                                         │
│   • Key driver: Product X launch        │
│   • Expanded into 3 new markets         │
│   • Customer retention up 15%           │
│                                         │
└─────────────────────────────────────────┘
```

---

### 4. Bold Startup（大胆创业）

**适用场景**: 融资路演、产品发布、品牌展示

```css
:root {
  /* 大胆配色 - 可根据品牌调整 */
  --color-primary: #6b46c1;      /* 紫色主调 */
  --color-secondary: #38b2ac;    /* 青色辅助 */
  --color-accent: #ed64a6;       /* 粉红强调 */
  --color-dark: #1a202c;
  --color-light: #f7fafc;
  
  /* 现代字体 */
  --font-heading: Arial Black, sans-serif;
  --font-body: Arial, sans-serif;
  
  /* 大胆字号 */
  --size-hero: 72px;
  --size-title: 48px;
  --size-subtitle: 24px;
  --size-body: 16px;
}
```

**大胆设计技巧**:
- 色块分割（50%背景色填充）
- 超大标题（72px+）
- 不对称布局
- 品牌色贯穿

---

### 5. Technical（技术分享）

**适用场景**: 技术会议、代码走查、架构设计

```css
:root {
  /* 暗色系统 */
  --color-primary: #1a1a2e;      /* 深蓝黑 */
  --color-secondary: #16213e;
  --color-accent: #0f3460;
  --color-highlight: #e94560;    /* 代码高亮红 */
  --color-code-bg: #282c34;      /* 代码块背景 */
  --color-text: #e2e8f0;
  --color-text-muted: #a0aec0;
  
  /* 等宽字体主导 */
  --font-heading: Arial, sans-serif;
  --font-body: Arial, sans-serif;
  --font-code: Courier New, Consolas, monospace;
  
  /* 信息密集 */
  --size-title: 28px;
  --size-code: 14px;
  --spacing-tight: 8px;
}
```

**技术PPT元素**:
- 代码块（暗色背景 + 语法高亮）
- 架构图（方框 + 箭头）
- 终端输出风格
- 版本号/Git hash显示

---

## 配色方案速查

### 学术论文配色

| 用途 | 颜色代码 | 示例 |
|-----|---------|------|
| 主色调 | #1a365d | 标题、框线 |
| 实验组 | #3182ce | 图表-组1 |
| 对照组 | #718096 | 图表-组2 |
| 显著性 | #38a169 | p<0.05标记 |
| 无显著 | #a0aec0 | p>0.05标记 |
| 警示 | #e53e3e | 风险/副作用 |

### 生存分析曲线配色

```javascript
// Kaplan-Meier曲线推荐配色
const survivalColors = [
  "#2b6cb0",  // 组1 - 蓝
  "#c53030",  // 组2 - 红
  "#2f855a",  // 组3 - 绿
  "#975a16",  // 组4 - 棕
];
```

### 商业图表配色

| 含义 | 颜色 | 使用场景 |
|-----|------|---------|
| 增长/正面 | #48bb78 | 收入增长、成功率 |
| 下降/负面 | #f56565 | 成本、流失率 |
| 中性/基准 | #718096 | 对照、去年同期 |
| 强调/当前 | #4299e1 | 本期、重点 |

---

## 自定义设计系统

### 从零创建步骤

1. **定义主色** (1个)
   - 考虑品牌/机构色
   - 确保足够深可做文字

2. **生成色阶** 
   ```
   主色 → 浅化20% (hover)
        → 浅化50% (背景)
        → 深化20% (强调)
   ```

3. **选择强调色** (1-2个)
   - 与主色互补或对比
   - 用于数据高亮、CTA

4. **确定中性色**
   ```
   文字: #1a202c (深)
   次要: #4a5568 (中)
   浅色: #a0aec0 (说明)
   背景: #f7fafc (浅灰)
   ```

5. **选择字体组合**
   | 风格 | 标题 | 正文 |
   |-----|------|------|
   | 传统学术 | Georgia | Arial |
   | 现代商务 | Arial Black | Arial |
   | 友好亲切 | Verdana | Verdana |
   | 技术风格 | Arial | Courier New |

---

## Web安全字体完整列表

### 可放心使用的字体

**衬线字体 (Serif)**:
- Georgia
- Times New Roman
- Palatino Linotype
- Book Antiqua

**无衬线 (Sans-serif)**:
- Arial
- Arial Black
- Helvetica
- Verdana
- Tahoma
- Trebuchet MS
- Impact

**等宽 (Monospace)**:
- Courier New
- Lucida Console
- Consolas

⚠️ **绝对不要使用**:
- 系统专属字体 (San Francisco, Segoe UI)
- 需要安装的字体 (Roboto, Open Sans)
- 中文艺术字体

---

## 设计一致性检查表

- [ ] 全PPT只用2-3种颜色
- [ ] 标题字号统一
- [ ] 正文字号统一
- [ ] 间距使用4px倍数
- [ ] 所有图表配色一致
- [ ] 强调色使用规则一致
- [ ] 没有混用不同风格
