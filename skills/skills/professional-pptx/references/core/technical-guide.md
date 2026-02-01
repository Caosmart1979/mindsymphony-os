# Technical Implementation Guide

从HTML到PPTX的完整技术实现流程。

---

## 工作流概览

```
1. 准备工作
   ├─► 解压html2pptx库
   └─► 确认依赖安装

2. 设计阶段
   ├─► 创建CSS变量文件
   └─► 设计HTML模板

3. 实现阶段
   ├─► 编写HTML幻灯片
   ├─► 编写转换脚本
   └─► 添加图表/表格

4. 验证阶段
   ├─► 转换为图片
   ├─► 视觉检查
   └─► 修复问题

5. 输出
   └─► 生成最终PPTX
```

---

## Step 1: 环境准备

### 解压html2pptx库

```bash
# 在工作目录创建html2pptx子目录
mkdir -p html2pptx
tar -xzf /mnt/skills/public/pptx/html2pptx.tgz -C html2pptx
```

### 验证依赖

```bash
# 检查Node.js
node --version

# 检查全局包
npm list -g pptxgenjs playwright
```

---

## Step 2: 创建设计系统CSS

创建 `styles.css`:

```css
:root {
  --color-primary: #1a365d;
  --color-secondary: #2b6cb0;
  --color-accent: #ed8936;
  --color-text: #2d3748;
  --color-muted: #718096;
  --color-surface: #f7fafc;
  --font-heading: Georgia, serif;
  --font-body: Arial, Helvetica, sans-serif;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  font-family: var(--font-body);
  color: var(--color-text);
}

.row { display: flex; flex-direction: row; }
.col { display: flex; flex-direction: column; }
.fit { flex: 0 0 auto; }
.grow { flex: 1 1 0; }

h1 {
  font-family: var(--font-heading);
  font-size: 32px;
  color: var(--color-primary);
}
```

---

## Step 3: HTML幻灯片模板

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="styles.css">
</head>
<body class="col" style="width: 960px; height: 540px; padding: 20px 40px;">
  
  <div class="fit" style="margin-bottom: 20px;">
    <h1>幻灯片标题</h1>
  </div>
  
  <div class="grow">
    <!-- 内容 -->
  </div>
  
  <div class="fit" style="font-size: 10px; color: var(--color-muted);">
    来源: xxx
  </div>
  
</body>
</html>
```

---

## Step 4: 转换脚本

创建 `create-pptx.js`:

```javascript
const pptxgen = require("pptxgenjs");
const { html2pptx } = require("./html2pptx");

async function createPresentation() {
  const pptx = new pptxgen();
  pptx.layout = "LAYOUT_16x9";
  
  // 添加HTML幻灯片
  await html2pptx("slide01.html", pptx);
  
  // 带图表的幻灯片
  const { slide, placeholders } = await html2pptx("slide02.html", pptx);
  slide.addChart(pptx.charts.BAR, [
    { name: "数据", labels: ["A", "B"], values: [10, 20] }
  ], {
    ...placeholders[0],
    chartColors: ["2b6cb0"]  // 不带#号
  });
  
  await pptx.writeFile("output.pptx");
}

createPresentation().catch(console.error);
```

运行: `NODE_PATH="$(npm root -g)" node create-pptx.js`

---

## Step 5: 图表参考

### 柱状图
```javascript
slide.addChart(pptx.charts.BAR, [
  { name: "系列1", labels: ["A", "B", "C"], values: [10, 20, 15] }
], {
  x: 1, y: 1.5, w: 8, h: 4,
  barDir: "col",  // 纵向
  showValue: true,
  chartColors: ["2b6cb0"]
});
```

### 折线图
```javascript
slide.addChart(pptx.charts.LINE, [
  { name: "组1", labels: ["M1", "M2", "M3"], values: [85, 78, 72] },
  { name: "组2", labels: ["M1", "M2", "M3"], values: [84, 68, 55] }
], {
  x: 0.5, y: 1.5, w: 9, h: 4,
  lineSize: 3,
  chartColors: ["2b6cb0", "e53e3e"]
});
```

### 饼图
```javascript
slide.addChart(pptx.charts.PIE, [
  { name: "分布", labels: ["A", "B", "C"], values: [40, 35, 25] }
], {
  x: 3, y: 1.5, w: 4, h: 4,
  showPercent: true,
  chartColors: ["48bb78", "4299e1", "ed8936"]
});
```

---

## Step 6: 表格参考

```javascript
slide.addTable([
  [
    { text: "变量", options: { fill: "1a365d", color: "ffffff", bold: true } },
    { text: "值", options: { fill: "1a365d", color: "ffffff", bold: true } }
  ],
  ["年龄", "62.3 ± 10.2"],
  ["BMI", "24.5 ± 3.8"]
], {
  x: 0.5, y: 1.5, w: 9, h: 2,
  border: { pt: 0.5, color: "cccccc" },
  fontSize: 12,
  align: "center"
});
```

---

## Step 7: 视觉验证

```bash
# 转PDF
soffice --headless --convert-to pdf output.pptx

# PDF转图片
pdftoppm -jpeg -r 150 output.pdf slide

# 检查生成的 slide-1.jpg, slide-2.jpg ...
```

### 检查清单

- [ ] 文字无裁切
- [ ] 元素无重叠
- [ ] 对齐一致
- [ ] 颜色正确
- [ ] 图表数据准确

---

## 常见错误

| 问题 | 原因 | 解决 |
|-----|------|-----|
| 颜色不显示 | 颜色代码带#号 | 去掉# |
| 字体替换 | 使用了非安全字体 | 改用Web安全字体 |
| 布局错乱 | HTML尺寸不对 | 确保960×540px |
| 图表位置偏移 | 未使用placeholders | 使用返回的placeholders |
| 文件损坏 | XML格式错误 | 检查特殊字符 |

---

## 完整示例项目结构

```
project/
├── html2pptx/           # 解压的库文件
├── styles.css           # 设计系统
├── slide01-title.html   # 标题页
├── slide02-intro.html   # 介绍页
├── slide03-data.html    # 数据页
├── create-pptx.js       # 转换脚本
└── output.pptx          # 输出文件
```
