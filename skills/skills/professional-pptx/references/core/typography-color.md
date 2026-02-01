# Typography & Color Guide

字体选择与配色系统详解。

---

## Web安全字体列表

### 衬线字体 (Serif)

| 字体 | 特点 | 适用场景 |
|-----|------|---------|
| **Georgia** | 优雅可读 | 学术标题、正式场合 |
| **Times New Roman** | 经典传统 | 正式文档 |
| **Palatino Linotype** | 优美 | 高端设计 |
| **Book Antiqua** | 古典 | 传统风格 |

### 无衬线字体 (Sans-serif)

| 字体 | 特点 | 适用场景 |
|-----|------|---------|
| **Arial** | 通用清晰 | 正文、数据 |
| **Arial Black** | 粗重醒目 | 大标题 |
| **Helvetica** | 现代专业 | 商业设计 |
| **Verdana** | 屏幕友好 | 长文本 |
| **Tahoma** | 紧凑 | 小字号 |
| **Trebuchet MS** | 现代 | 创意设计 |
| **Impact** | 极粗 | 标语 |

### 等宽字体 (Monospace)

| 字体 | 适用场景 |
|-----|---------|
| **Courier New** | 代码、数据 |
| **Lucida Console** | 技术内容 |
| **Consolas** | 代码 |

---

## 字体组合推荐

### 学术风格
```
标题: Georgia (serif)
正文: Arial (sans-serif)
数据: Courier New (mono)
```

### 商务风格
```
标题: Arial Black (sans-serif)
正文: Arial (sans-serif)
强调: Arial Bold
```

### 现代风格
```
标题: Helvetica Bold
正文: Helvetica
数据: Consolas
```

### 技术风格
```
标题: Arial
正文: Verdana
代码: Courier New
```

---

## 字号层级系统

### 标准层级 (推荐)

```
层级1 (标题):     32-40px
层级2 (副标题):   24-28px
层级3 (小标题):   18-20px
层级4 (正文):     16-18px
层级5 (说明):     12-14px
层级6 (脚注):     10px
```

### 信息密集型

```
层级1 (标题):     28-32px
层级2 (副标题):   20-24px
层级3 (小标题):   14-16px
层级4 (正文):     12-14px
层级5 (说明):     10-11px
层级6 (脚注):     9-10px
```

### 极简/演讲型

```
层级1 (标题):     48-72px
层级2 (副标题):   28-36px
层级3 (正文):     20-24px
层级4 (脚注):     12px
```

---

## 行高与间距

### 行高规则

```
标题:    1.1 - 1.2
正文:    1.4 - 1.6
列表:    1.6 - 1.8
```

### 字间距

```css
/* 全大写标题增加字间距 */
letter-spacing: 2px;

/* 正文保持默认 */
letter-spacing: normal;
```

---

## 配色系统

### 构建配色的步骤

```
1. 选择主色 (1个)
   └─► 品牌色/机构色/情感色

2. 生成色阶
   └─► 主色 → 浅色(+50%) → 深色(-20%)

3. 选择强调色 (1个)
   └─► 与主色对比/互补

4. 定义功能色
   └─► 成功(绿)、警示(橙)、错误(红)

5. 确定中性色
   └─► 文字、背景、边框
```

### 中性色体系

```
深色文字:   #1a202c (近黑)
正文文字:   #2d3748 (深灰)
次要文字:   #4a5568 (中灰)
说明文字:   #718096 (浅灰)
禁用/占位:  #a0aec0 (淡灰)
边框:       #e2e8f0 (极浅灰)
浅背景:     #f7fafc (几乎白)
纯白背景:   #ffffff
```

### 语义色彩

| 语义 | 浅色背景 | 主色 | 深色文字 |
|-----|---------|------|---------|
| 成功/正面 | #c6f6d5 | #38a169 | #22543d |
| 信息/默认 | #bee3f8 | #3182ce | #2c5282 |
| 警示/注意 | #fefcbf | #ed8936 | #975a16 |
| 错误/负面 | #fed7d7 | #e53e3e | #c53030 |

---

## 对比度要求

### WCAG标准

| 文字类型 | 最小对比度 |
|---------|-----------|
| 正文 (<18px) | 4.5:1 |
| 大文字 (≥18px) | 3:1 |
| 非文字元素 | 3:1 |

### 常见组合对比度

| 前景色 | 背景色 | 对比度 | 可用性 |
|-------|-------|--------|-------|
| #1a202c | #ffffff | 16.1:1 | ✅ 优秀 |
| #2d3748 | #ffffff | 11.7:1 | ✅ 优秀 |
| #4a5568 | #ffffff | 7.0:1 | ✅ 良好 |
| #718096 | #ffffff | 4.5:1 | ✅ 及格 |
| #a0aec0 | #ffffff | 2.7:1 | ❌ 不足 |

---

## CSS变量模板

```css
:root {
  /* 主色系 */
  --color-primary: #1a365d;
  --color-primary-light: #2b6cb0;
  --color-primary-dark: #0f2942;
  
  /* 强调色 */
  --color-accent: #ed8936;
  
  /* 功能色 */
  --color-success: #38a169;
  --color-warning: #ed8936;
  --color-error: #e53e3e;
  --color-info: #3182ce;
  
  /* 中性色 */
  --color-text: #2d3748;
  --color-text-muted: #718096;
  --color-border: #e2e8f0;
  --color-surface: #f7fafc;
  --color-background: #ffffff;
  
  /* 字体 */
  --font-heading: Georgia, serif;
  --font-body: Arial, Helvetica, sans-serif;
  --font-mono: Courier New, monospace;
  
  /* 字号 */
  --size-h1: 36px;
  --size-h2: 24px;
  --size-h3: 18px;
  --size-body: 16px;
  --size-small: 12px;
  --size-footnote: 10px;
  
  /* 行高 */
  --leading-tight: 1.2;
  --leading-normal: 1.5;
  --leading-relaxed: 1.8;
}
```

---

## 常见错误

| 错误 | 修正 |
|-----|-----|
| 使用非安全字体 | 仅用Web安全字体 |
| 字号层级太多 | 限制3-4级 |
| 颜色超过5种 | 精简配色 |
| 对比度不足 | 检查WCAG |
| 行高太紧 | 正文至少1.4 |
| 字间距过大 | 只在大写时使用 |

---

## 快速检查

- [ ] 只使用Web安全字体
- [ ] 字体不超过3种
- [ ] 字号层级清晰
- [ ] 最小字号≥10px
- [ ] 配色不超过5种
- [ ] 文字对比度≥4.5:1
- [ ] 语义色彩一致
