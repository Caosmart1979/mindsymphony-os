# Data Visualization Guide

数据可视化最佳实践。

---

## 图表选择决策树

```
你要展示什么？
│
├─► 单个数字/KPI
│   └─► 大数字展示 (Big Number)
│
├─► 随时间变化
│   ├─► 连续数据 → 折线图 (Line)
│   └─► 离散时段 → 柱状图 (Bar)
│
├─► 类别比较
│   ├─► 2-4类别 → 纵向柱状图
│   ├─► 5-8类别 → 横向条形图
│   └─► 9+类别 → 考虑分组或表格
│
├─► 占比/构成
│   ├─► 2-5部分 → 饼图/环形图
│   └─► 6+部分 → 堆叠柱状图
│
├─► 关系/相关性
│   └─► 散点图 (Scatter)
│
├─► 分布
│   └─► 直方图/箱线图
│
└─► 流程/层级
    └─► 流程图/树状图
```

---

## 常用图表代码

### 柱状图 (Bar Chart)

```javascript
// 纵向柱状图
slide.addChart(pptx.charts.BAR, [
  {
    name: "并发症率",
    labels: ["实验组", "对照组"],
    values: [12.5, 18.3]
  }
], {
  x: 1, y: 1.5, w: 8, h: 4,
  barDir: "col",  // 纵向
  showValue: true,
  showCatAxisTitle: true,
  catAxisTitle: "组别",
  showValAxisTitle: true,
  valAxisTitle: "发生率 (%)",
  chartColors: ["2b6cb0", "718096"]
});
```

```javascript
// 横向条形图
slide.addChart(pptx.charts.BAR, [
  {
    name: "手术时间",
    labels: ["医院A", "医院B", "医院C", "医院D", "医院E"],
    values: [125, 142, 118, 156, 133]
  }
], {
  x: 1, y: 1.5, w: 8, h: 4,
  barDir: "bar",  // 横向
  showValue: true,
  chartColors: ["2b6cb0"]
});
```

### 折线图 (Line Chart)

```javascript
slide.addChart(pptx.charts.LINE, [
  {
    name: "实验组",
    labels: ["0", "6", "12", "18", "24"],
    values: [100, 95, 88, 82, 78]
  },
  {
    name: "对照组",
    labels: ["0", "6", "12", "18", "24"],
    values: [100, 92, 80, 68, 58]
  }
], {
  x: 0.5, y: 1.5, w: 7, h: 4,
  lineSize: 3,
  lineSmooth: false,  // Kaplan-Meier应用阶梯
  showCatAxisTitle: true,
  catAxisTitle: "随访时间 (月)",
  showValAxisTitle: true,
  valAxisTitle: "生存率 (%)",
  valAxisMinVal: 0,
  valAxisMaxVal: 100,
  chartColors: ["2b6cb0", "e53e3e"],
  showLegend: true,
  legendPos: "b"
});
```

### 饼图 (Pie Chart)

```javascript
slide.addChart(pptx.charts.PIE, [
  {
    name: "肿瘤分期",
    labels: ["I期", "II期", "III期", "IV期"],
    values: [15, 35, 38, 12]
  }
], {
  x: 3, y: 1.5, w: 4, h: 4,
  showPercent: true,
  showLegend: true,
  legendPos: "r",
  chartColors: ["48bb78", "4299e1", "ed8936", "e53e3e"]
});
```

### 分组柱状图

```javascript
slide.addChart(pptx.charts.BAR, [
  {
    name: "术前",
    labels: ["BMI", "血红蛋白", "白蛋白"],
    values: [25.2, 12.5, 3.8]
  },
  {
    name: "术后",
    labels: ["BMI", "血红蛋白", "白蛋白"],
    values: [23.1, 11.8, 3.5]
  }
], {
  x: 1, y: 1.5, w: 8, h: 4,
  barDir: "col",
  barGrouping: "clustered",
  showCatAxisTitle: true,
  catAxisTitle: "指标",
  chartColors: ["2b6cb0", "ed8936"],
  showLegend: true
});
```

---

## 图表设计原则

### 1. 数据墨水比

**好**: 每一滴"墨水"都传递信息
**坏**: 装饰性元素喧宾夺主

```
✅ 去掉网格线背景
✅ 简化图例
✅ 移除3D效果
❌ 渐变填充
❌ 阴影效果
❌ 过多颜色
```

### 2. 颜色使用

```
规则1: 主数据用主色，对比/基准用灰色
规则2: 正面数据绿色，负面数据红色
规则3: 当前/重点用深色，历史/参考用浅色
规则4: 同类数据用同色系渐变
```

### 3. 标签与注释

```
必须有:
- 清晰的图表标题
- Y轴单位说明
- X轴类别/时间标签
- 图例 (多系列时)

可选:
- 数据标签 (数值不多时)
- 趋势线
- 基准线
- 注释框
```

---

## 医学图表特殊规范

### 生存曲线

```
必须包含:
- Number at risk 表格
- HR + 95%CI
- Log-rank p值
- 中位生存时间 (如达到)

配色建议:
- 实验组: 蓝色 #2b6cb0
- 对照组: 红色 #c53030
```

### 森林图

```
必须包含:
- 效应量 + 95%CI
- 权重 (如meta分析)
- 整体效应
- 异质性统计 (I², p)

布局:
- 左侧: 研究标识
- 中间: 图形化CI
- 右侧: 数值
```

### ROC曲线

```
必须包含:
- AUC值 + 95%CI
- 最优截断值
- 敏感度/特异度
- 参考线 (AUC=0.5)
```

---

## 数据展示检查清单

- [ ] 图表类型适合数据类型
- [ ] 标题清晰描述内容
- [ ] Y轴有单位说明
- [ ] X轴标签可读
- [ ] 颜色有语义意义
- [ ] 图例位置不遮挡数据
- [ ] 字体大小足够(≥10pt)
- [ ] 关键数据被突出
- [ ] 没有3D/渐变等装饰
- [ ] 来源/脚注清晰

---

## 常见错误

| 错误 | 问题 | 修正 |
|-----|------|-----|
| 饼图太多分类 | 超过5-6个难以区分 | 改用条形图或合并小类 |
| 双Y轴误导 | 不同量纲难以比较 | 分成两个图 |
| 3D图表 | 视觉扭曲数据 | 使用2D |
| 截断Y轴 | 放大差异误导 | 从0开始或明确标注 |
| 颜色太多 | 视觉混乱 | 限制3-5种 |
