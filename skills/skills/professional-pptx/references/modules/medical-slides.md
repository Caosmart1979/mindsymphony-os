# Medical Slides Module

医学/临床研究演讲的专用设计指南。

---

## 医学PPT特殊要求

```
医学演讲的特点:
1. 数据必须准确，不能有误导
2. 统计结果呈现有规范
3. 伦理声明不能省略
4. 利益冲突必须披露
5. 患者信息必须脱敏
```

---

## 医学设计系统

### 配色方案

```css
:root {
  /* 主色系 - 医疗蓝 */
  --medical-primary: #0077b6;
  --medical-secondary: #00a896;
  
  /* 功能色 */
  --color-success: #38a169;    /* 阳性结果/显著 */
  --color-warning: #ed8936;    /* 需关注 */
  --color-danger: #e53e3e;     /* 风险/不良事件 */
  --color-neutral: #718096;    /* 无显著差异 */
  
  /* 生存曲线配色 */
  --survival-group1: #2b6cb0;  /* 实验组 */
  --survival-group2: #c53030;  /* 对照组 */
  
  /* 安全性信号 */
  --ae-mild: #48bb78;          /* 轻度AE */
  --ae-moderate: #ed8936;      /* 中度AE */
  --ae-severe: #e53e3e;        /* 重度AE */
}
```

### 统计结果显示规范

```html
<!-- p值显示 -->
<span class="p-significant">p < 0.001</span>    <!-- 显著 -->
<span class="p-nonsig">p = 0.234</span>         <!-- 不显著 -->

<!-- 置信区间 -->
<span>HR: 0.65 (95%CI: 0.48-0.88)</span>

<!-- 效应量高亮 -->
<span class="effect-size">OR: 2.35</span>
```

### CSS样式

```css
.p-significant {
  color: #38a169;
  font-weight: bold;
  font-family: "Courier New", monospace;
}

.p-nonsig {
  color: #718096;
  font-family: "Courier New", monospace;
}

.effect-size {
  color: #2b6cb0;
  font-weight: bold;
}

/* 风险分层 */
.risk-low { background: #c6f6d5; color: #276749; }
.risk-moderate { background: #fefcbf; color: #975a16; }
.risk-high { background: #fed7d7; color: #c53030; }
```

---

## 常用医学图表

### 1. 患者流程图 (CONSORT)

```html
<body class="col" style="width: 960px; height: 540px; padding: 20px;">
  
  <h1 style="font-size: 24px; margin-bottom: 16px;">患者筛选流程</h1>
  
  <div class="col center grow">
    
    <!-- 评估 -->
    <div style="padding: 12px 24px; background: #ebf8ff; 
         border: 2px solid #4299e1; border-radius: 8px;">
      <div style="font-size: 14px; color: #718096;">评估资格</div>
      <div style="font-size: 20px; font-weight: bold;">n = 1,250</div>
    </div>
    
    <div style="font-size: 24px; margin: 8px 0;">↓</div>
    
    <!-- 排除 - 分支 -->
    <div class="row" style="align-items: flex-start; gap: 80px;">
      
      <!-- 左侧继续 -->
      <div class="col center">
        <div style="padding: 12px 24px; background: #e6fffa;
             border: 2px solid #38b2ac; border-radius: 8px;">
          <div style="font-size: 14px; color: #718096;">纳入研究</div>
          <div style="font-size: 20px; font-weight: bold;">n = 768</div>
        </div>
      </div>
      
      <!-- 右侧排除 -->
      <div style="padding: 12px 20px; background: #fff5f5;
           border: 2px solid #fc8181; border-radius: 8px;
           font-size: 12px; color: #718096;">
        <div style="font-weight: bold; color: #e53e3e; margin-bottom: 8px;">
          排除 (n=482)
        </div>
        <div>• 不符合纳入标准 (n=312)</div>
        <div>• 拒绝参与 (n=98)</div>
        <div>• 数据缺失 (n=72)</div>
      </div>
      
    </div>
    
    <div style="font-size: 24px; margin: 8px 0;">↓</div>
    
    <!-- 分组 -->
    <div class="row" style="gap: 40px;">
      <div style="padding: 12px 20px; background: #ebf8ff;
           border: 2px solid #4299e1; border-radius: 8px; text-align: center;">
        <div style="font-size: 12px; color: #718096;">实验组</div>
        <div style="font-size: 18px; font-weight: bold;">n = 384</div>
      </div>
      <div style="padding: 12px 20px; background: #faf5ff;
           border: 2px solid #9f7aea; border-radius: 8px; text-align: center;">
        <div style="font-size: 12px; color: #718096;">对照组</div>
        <div style="font-size: 18px; font-weight: bold;">n = 384</div>
      </div>
    </div>
    
  </div>
  
</body>
```

### 2. 基线特征表

```javascript
// 标准基线表格
const baselineTable = [
  // 表头
  [
    { text: "特征", options: { fill: "0077b6", color: "ffffff", bold: true } },
    { text: "实验组 (n=384)", options: { fill: "0077b6", color: "ffffff", bold: true } },
    { text: "对照组 (n=384)", options: { fill: "0077b6", color: "ffffff", bold: true } },
    { text: "p值", options: { fill: "0077b6", color: "ffffff", bold: true } }
  ],
  // 数据行
  ["年龄 (岁), mean ± SD", "62.3 ± 10.2", "61.8 ± 11.5", "0.542"],
  ["男性, n (%)", "245 (63.8)", "238 (62.0)", "0.605"],
  ["BMI (kg/m²), mean ± SD", "24.5 ± 3.8", "24.2 ± 4.1", "0.301"],
  ["糖尿病, n (%)", "89 (23.2)", "92 (24.0)", "0.803"],
  ["高血压, n (%)", "156 (40.6)", "148 (38.5)", "0.563"],
  [
    "ASA分级, n (%)", "", "", ""
  ],
  ["  I-II", "312 (81.3)", "305 (79.4)", "0.528"],
  ["  III-IV", "72 (18.7)", "79 (20.6)", ""]
];

slide.addTable(baselineTable, {
  x: 0.3, y: 1.3, w: 9.4, h: 4.5,
  colW: [2.8, 2.2, 2.2, 1.2],
  fontSize: 11,
  border: { pt: 0.5, color: "cccccc" },
  align: "center",
  valign: "middle"
});
```

### 3. 生存曲线

```javascript
// Kaplan-Meier曲线数据
const survivalData = [
  {
    name: "实验组",
    labels: ["0", "12", "24", "36", "48", "60"],
    values: [100, 92, 85, 78, 72, 68]
  },
  {
    name: "对照组",
    labels: ["0", "12", "24", "36", "48", "60"],
    values: [100, 88, 76, 65, 55, 48]
  }
];

slide.addChart(pptx.charts.LINE, survivalData, {
  x: 0.5, y: 1.2, w: 6.5, h: 4,
  lineSize: 3,
  showCatAxisTitle: true,
  catAxisTitle: "随访时间 (月)",
  showValAxisTitle: true,
  valAxisTitle: "无事件生存率 (%)",
  valAxisMinVal: 0,
  valAxisMaxVal: 100,
  valAxisMajorUnit: 20,
  chartColors: ["2b6cb0", "c53030"],
  showLegend: true,
  legendPos: "t"
});

// Number at risk 表格
slide.addText([
  { text: "Number at risk\n", options: { bold: true, fontSize: 9 } },
  { text: "实验组: 384  353  327  299  276  261\n", options: { fontSize: 9 } },
  { text: "对照组: 384  338  292  250  211  184", options: { fontSize: 9 } }
], { x: 0.5, y: 5.3, w: 6.5 });

// 统计结果框
slide.addText([
  { text: "HR: 0.58 (95%CI: 0.44-0.76)\n", options: { fontSize: 12 } },
  { text: "Log-rank p < 0.001", options: { fontSize: 12, color: "38a169", bold: true } }
], { x: 7.2, y: 2.5, w: 2.5, h: 1,
     fill: { color: "f7fafc" },
     line: { color: "e2e8f0", pt: 1 } });
```

### 4. 森林图 (亚组分析)

```javascript
// 使用表格+文本模拟森林图
const forestData = [
  // 表头
  [
    { text: "亚组", options: { fill: "0077b6", color: "ffffff", bold: true, align: "left" } },
    { text: "n", options: { fill: "0077b6", color: "ffffff", bold: true } },
    { text: "HR (95%CI)", options: { fill: "0077b6", color: "ffffff", bold: true } },
    { text: "p值", options: { fill: "0077b6", color: "ffffff", bold: true } }
  ],
  // 总体
  [
    { text: "总体", options: { bold: true } },
    "768",
    { text: "0.58 (0.44-0.76)", options: { bold: true } },
    { text: "<0.001", options: { color: "38a169", bold: true } }
  ],
  // 亚组
  ["年龄 <65岁", "412", "0.72 (0.52-0.99)", "0.045"],
  [
    { text: "年龄 ≥65岁", options: {} },
    "356",
    { text: "0.41 (0.28-0.60)", options: { color: "2b6cb0", bold: true } },
    { text: "<0.001", options: { color: "38a169", bold: true } }
  ],
  ["男性", "483", "0.55 (0.39-0.77)", "0.001"],
  ["女性", "285", "0.64 (0.42-0.98)", "0.039"],
  ["BMI <25", "398", "0.52 (0.36-0.75)", "<0.001"],
  ["BMI ≥25", "370", "0.67 (0.46-0.97)", "0.033"]
];

slide.addTable(forestData, {
  x: 0.3, y: 1.5, w: 9.4, h: 4,
  colW: [3, 1, 2.8, 1.2],
  fontSize: 12,
  border: { pt: 0.5, color: "cccccc" },
  align: "center"
});

// 交互作用提示
slide.addText("P for interaction = 0.024 (年龄)", {
  x: 0.5, y: 5.5, fontSize: 10, color: "718096", italic: true
});
```

### 5. 安全性表格 (AE)

```javascript
const aeTable = [
  [
    { text: "不良事件", options: { fill: "0077b6", color: "ffffff", bold: true, align: "left" } },
    { text: "实验组 n(%)", options: { fill: "0077b6", color: "ffffff", bold: true } },
    { text: "对照组 n(%)", options: { fill: "0077b6", color: "ffffff", bold: true } },
    { text: "p值", options: { fill: "0077b6", color: "ffffff", bold: true } }
  ],
  // 总体AE
  [
    { text: "任何AE", options: { bold: true } },
    "156 (40.6)",
    "198 (51.6)",
    { text: "0.003", options: { color: "38a169", bold: true } }
  ],
  // 分级
  [
    { text: "  Grade 1-2", options: { color: "718096" } },
    "128 (33.3)",
    "152 (39.6)",
    "0.076"
  ],
  [
    { text: "  Grade 3-4", options: { color: "e53e3e" } },
    { text: "28 (7.3)", options: { color: "e53e3e" } },
    { text: "46 (12.0)", options: { color: "e53e3e" } },
    { text: "0.028", options: { color: "38a169", bold: true } }
  ],
  // 具体AE
  ["出血", "23 (6.0)", "35 (9.1)", "0.106"],
  ["感染", "45 (11.7)", "62 (16.1)", "0.082"],
  ["吻合口瘘", "12 (3.1)", "28 (7.3)", "0.011"]
];

slide.addTable(aeTable, {
  x: 0.5, y: 1.5, w: 9, h: 3.5,
  fontSize: 11,
  border: { pt: 0.5, color: "cccccc" }
});
```

---

## 医学PPT必备元素

### 1. 利益冲突声明

```html
<div style="position: absolute; bottom: 20px; left: 40px; right: 40px;
     font-size: 10px; color: #718096; border-top: 1px solid #e2e8f0;
     padding-top: 8px;">
  <strong>利益冲突声明:</strong> 
  本研究由XXX基金资助 (批准号: XXX)。作者声明无其他利益冲突。
</div>
```

### 2. 伦理声明

```html
<div style="font-size: 11px; color: #718096; margin-top: 16px;
     padding: 8px 12px; background: #f7fafc; border-radius: 4px;">
  本研究经北京医院伦理委员会批准 (批准号: 2023-XXX)，
  所有患者签署知情同意书。
</div>
```

### 3. 临床试验注册

```html
<div style="font-size: 10px; color: #718096;">
  ClinicalTrials.gov: NCT12345678
</div>
```

---

## 医学演讲检查清单

### 内容检查
- [ ] 所有数字经过核对
- [ ] p值保留适当位数 (通常3位)
- [ ] 置信区间格式正确
- [ ] 样本量前后一致

### 伦理合规
- [ ] 伦理批准号
- [ ] 知情同意声明
- [ ] 利益冲突披露
- [ ] 临床试验注册号 (如适用)

### 患者隐私
- [ ] 无患者可识别信息
- [ ] 影像学图片已脱敏
- [ ] 病例号已隐藏

### 统计规范
- [ ] 正确使用显著性符号 (*<0.05, **<0.01, ***<0.001)
- [ ] 连续变量报告mean±SD或median(IQR)
- [ ] 分类变量报告n(%)
