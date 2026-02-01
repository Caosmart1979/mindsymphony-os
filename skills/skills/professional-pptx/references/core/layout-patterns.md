# Layout Patterns Guide

PPT布局模式库，包含常用布局的代码模板和使用场景。

---

## 画布与安全区域

### 标准尺寸 (16:9)

```
总尺寸: 960px × 540px

┌─────────────────────────────────────────────────┐
│ 20px                                       20px │
│ ┌─────────────────────────────────────────────┐ │
│ │          SAFE AREA (920 × 500)              │ │
│ │                                             │ │
│ │  实际内容区域                                │ │
│ │                                             │ │
│ │                                             │ │
│ └─────────────────────────────────────────────┘ │
│ 20px                                       20px │
└─────────────────────────────────────────────────┘
```

### 垂直分区 (540px高度)

```
┌─────────────────────────────────────────┐
│  标题区域 (Title Zone)                   │ 0-100px
│  - 标题文字                              │
│  - 可选副标题                            │
├─────────────────────────────────────────┤ 100px
│  10px 缓冲                               │
├─────────────────────────────────────────┤ 110px
│                                         │
│  主内容区域 (Content Zone)               │ 110-490px
│  - 图表、文字、卡片                      │ (380px可用)
│                                         │
├─────────────────────────────────────────┤ 490px
│  10px 缓冲                               │
├─────────────────────────────────────────┤ 500px
│  脚注区域 (Footer Zone)                  │ 500-540px
│  - 来源、页码、版权                      │ (40px)
└─────────────────────────────────────────┘
```

---

## 标题页布局

### Layout: title-centered（居中标题）

**适用场景**: 正式学术演讲、商务报告封面

```html
<body class="col bg-surface" style="width: 960px; height: 540px; 
      justify-content: center; align-items: center; text-align: center;">
  
  <!-- 主标题 -->
  <h1 style="font-size: 40px; color: var(--color-primary); 
       margin-bottom: 16px; font-weight: bold;">
    研究标题：副标题说明
  </h1>
  
  <!-- 作者信息 -->
  <p style="font-size: 18px; color: var(--color-text); margin-bottom: 8px;">
    张三<sup>1</sup>, 李四<sup>1,2</sup>, 王五<sup>2*</sup>
  </p>
  
  <!-- 机构 -->
  <p style="font-size: 14px; color: var(--color-muted);">
    <sup>1</sup>北京医院普通外科 &nbsp;&nbsp;
    <sup>2</sup>北京大学医学部
  </p>
  
  <!-- 会议/日期 -->
  <p style="font-size: 12px; color: var(--color-muted); 
       margin-top: 40px;">
    第X届全国XXX学术会议 | 2025年X月
  </p>
  
</body>
```

### Layout: title-editorial（编辑风格标题）

**适用场景**: 创业路演、产品发布、TED风格演讲

```html
<body style="width: 960px; height: 540px; position: relative;">
  
  <!-- 左侧大色块 -->
  <div style="position: absolute; left: 0; top: 0; 
       width: 40%; height: 100%; 
       background: var(--color-primary);">
  </div>
  
  <!-- 右侧内容 -->
  <div style="position: absolute; right: 40px; top: 50%; 
       transform: translateY(-50%); width: 50%;">
    
    <h1 style="font-size: 48px; font-weight: bold; 
         color: var(--color-primary); line-height: 1.2;">
      颠覆性的<br>产品标题
    </h1>
    
    <p style="font-size: 20px; color: var(--color-muted); 
         margin-top: 24px;">
      一句话价值主张
    </p>
    
  </div>
  
</body>
```

---

## 内容页布局

### Layout: bullets（标题+要点列表）

**适用场景**: 常规内容页、总结页、方法说明

```html
<body class="col" style="width: 960px; height: 540px; padding: 20px 40px;">
  
  <!-- 标题区 -->
  <div style="width: 100%; margin-bottom: 24px;">
    <h1 style="font-size: 32px; color: var(--color-primary);">
      研究方法
    </h1>
  </div>
  
  <!-- 要点列表 -->
  <div style="flex: 1;">
    <ul style="font-size: 20px; line-height: 1.8; color: var(--color-text);">
      <li style="margin-bottom: 16px;">
        <strong>研究设计:</strong> 回顾性队列研究 (2018-2023)
      </li>
      <li style="margin-bottom: 16px;">
        <strong>纳入标准:</strong> 接受腹腔镜胃切除术的胃癌患者
      </li>
      <li style="margin-bottom: 16px;">
        <strong>主要结局:</strong> 术后30天并发症发生率
      </li>
      <li>
        <strong>统计方法:</strong> 倾向评分匹配 + Cox回归
      </li>
    </ul>
  </div>
  
  <!-- 脚注 -->
  <div style="font-size: 10px; color: var(--color-muted);">
    IRB批准号: XXX-2023-001
  </div>
  
</body>
```

### Layout: split-image-text（左图右文/左文右图）

**适用场景**: 流程说明、图文配合、方法展示

```html
<body class="row" style="width: 960px; height: 540px; padding: 20px;">
  
  <!-- 左侧图表区 (55%) -->
  <div style="width: 55%; height: 100%; padding-right: 20px;">
    <div style="width: 100%; height: 100%; background: var(--color-surface);
         display: flex; align-items: center; justify-content: center;">
      <!-- 图表占位符 -->
      <div class="chart-placeholder" 
           data-chart-type="bar"
           style="width: 90%; height: 80%;">
      </div>
    </div>
  </div>
  
  <!-- 右侧文字区 (45%) -->
  <div class="col" style="width: 45%; height: 100%; justify-content: center;">
    
    <h2 style="font-size: 24px; color: var(--color-primary); 
         margin-bottom: 20px;">
      关键发现
    </h2>
    
    <ul style="font-size: 16px; line-height: 1.8;">
      <li style="margin-bottom: 12px;">
        手术时间显著缩短 (<span style="color: var(--color-accent);">
        -23%, p<0.001</span>)
      </li>
      <li style="margin-bottom: 12px;">
        术中出血量减少
      </li>
      <li>
        住院时间无显著差异
      </li>
    </ul>
    
  </div>
  
</body>
```

### Layout: cards（卡片网格）

**适用场景**: 多点对比、特征展示、团队介绍

```html
<body class="col" style="width: 960px; height: 540px; padding: 20px 40px;">
  
  <!-- 标题 -->
  <h1 style="font-size: 28px; color: var(--color-primary); 
       margin-bottom: 24px;">
    三个核心优势
  </h1>
  
  <!-- 卡片容器 -->
  <div class="row" style="flex: 1; gap: 20px;">
    
    <!-- 卡片1 -->
    <div style="flex: 1; background: var(--color-surface); 
         padding: 24px; border-radius: 8px;">
      <div style="font-size: 36px; margin-bottom: 12px;">🎯</div>
      <h3 style="font-size: 18px; font-weight: bold; margin-bottom: 8px;">
        精准度高
      </h3>
      <p style="font-size: 14px; color: var(--color-muted);">
        AI辅助定位准确率达98%
      </p>
    </div>
    
    <!-- 卡片2 -->
    <div style="flex: 1; background: var(--color-surface); 
         padding: 24px; border-radius: 8px;">
      <div style="font-size: 36px; margin-bottom: 12px;">⚡</div>
      <h3 style="font-size: 18px; font-weight: bold; margin-bottom: 8px;">
        速度快
      </h3>
      <p style="font-size: 14px; color: var(--color-muted);">
        处理时间缩短60%
      </p>
    </div>
    
    <!-- 卡片3 -->
    <div style="flex: 1; background: var(--color-surface); 
         padding: 24px; border-radius: 8px;">
      <div style="font-size: 36px; margin-bottom: 12px;">💰</div>
      <h3 style="font-size: 18px; font-weight: bold; margin-bottom: 8px;">
        成本低
      </h3>
      <p style="font-size: 14px; color: var(--color-muted);">
        综合成本降低40%
      </p>
    </div>
    
  </div>
  
</body>
```

---

## 数据展示布局

### Layout: chart-annotation（图表+解读）

**适用场景**: 单一重要图表的深度解读

```html
<body class="col" style="width: 960px; height: 540px; padding: 20px 40px;">
  
  <!-- 标题 -->
  <h1 style="font-size: 28px; color: var(--color-primary); 
       margin-bottom: 16px;">
    术后生存曲线分析
  </h1>
  
  <!-- 图表区 -->
  <div style="flex: 1; display: flex; align-items: stretch;">
    
    <!-- 主图表 (70%) -->
    <div style="width: 70%; padding-right: 20px;">
      <div class="chart-placeholder" data-chart-type="line"
           style="width: 100%; height: 100%; background: var(--color-surface);">
      </div>
    </div>
    
    <!-- 右侧解读 (30%) -->
    <div class="col" style="width: 30%; justify-content: center;">
      
      <!-- 关键数字 -->
      <div style="background: var(--color-primary); color: white;
           padding: 16px; border-radius: 8px; margin-bottom: 16px;
           text-align: center;">
        <div style="font-size: 36px; font-weight: bold;">89%</div>
        <div style="font-size: 12px;">5年生存率</div>
      </div>
      
      <!-- 要点 -->
      <div style="font-size: 14px; color: var(--color-text);">
        <p style="margin-bottom: 8px;">
          • HR = 0.65 (95%CI: 0.48-0.88)
        </p>
        <p style="margin-bottom: 8px;">
          • Log-rank p = 0.003
        </p>
        <p>
          • 中位随访: 48个月
        </p>
      </div>
      
    </div>
    
  </div>
  
  <!-- 脚注 -->
  <div style="font-size: 10px; color: var(--color-muted); margin-top: 12px;">
    Figure 2. Kaplan-Meier survival curves by treatment group
  </div>
  
</body>
```

### Layout: big-number（大数字突出）

**适用场景**: 展示关键指标、里程碑成就

```html
<body style="width: 960px; height: 540px; 
      display: flex; justify-content: center; align-items: center;
      background: var(--color-primary);">
  
  <div style="text-align: center; color: white;">
    
    <!-- 大数字 -->
    <div style="font-size: 120px; font-weight: bold; line-height: 1;">
      42%
    </div>
    
    <!-- 说明 -->
    <div style="font-size: 28px; margin-top: 16px; opacity: 0.9;">
      并发症发生率降低
    </div>
    
    <!-- 对比基线 -->
    <div style="font-size: 16px; margin-top: 24px; opacity: 0.7;">
      vs. 传统方法 (对照组)
    </div>
    
  </div>
  
</body>
```

### Layout: table（表格展示）

**适用场景**: 对比数据、基线特征、结果汇总

```html
<body class="col" style="width: 960px; height: 540px; padding: 20px 40px;">
  
  <h1 style="font-size: 28px; color: var(--color-primary); 
       margin-bottom: 16px;">
    基线特征比较
  </h1>
  
  <!-- 表格占位 - 实际用addTable实现 -->
  <div style="flex: 1; overflow: hidden;">
    <table style="width: 100%; border-collapse: collapse; font-size: 14px;">
      <thead>
        <tr style="background: var(--color-primary); color: white;">
          <th style="padding: 12px; text-align: left;">变量</th>
          <th style="padding: 12px; text-align: center;">实验组 (n=156)</th>
          <th style="padding: 12px; text-align: center;">对照组 (n=612)</th>
          <th style="padding: 12px; text-align: center;">p值</th>
        </tr>
      </thead>
      <tbody>
        <tr style="background: var(--color-surface);">
          <td style="padding: 10px;">年龄 (岁)</td>
          <td style="padding: 10px; text-align: center;">62.3 ± 10.2</td>
          <td style="padding: 10px; text-align: center;">58.7 ± 11.5</td>
          <td style="padding: 10px; text-align: center;">0.023</td>
        </tr>
        <!-- 更多行... -->
      </tbody>
    </table>
  </div>
  
  <div style="font-size: 10px; color: var(--color-muted);">
    Values are mean ± SD or n (%). *p < 0.05
  </div>
  
</body>
```

---

## 过渡页布局

### Layout: section-divider（章节分隔）

**适用场景**: 大章节之间的过渡

```html
<body style="width: 960px; height: 540px; position: relative;">
  
  <!-- 左侧色条 -->
  <div style="position: absolute; left: 0; top: 0;
       width: 8px; height: 100%; 
       background: var(--color-accent);">
  </div>
  
  <!-- 内容 -->
  <div style="position: absolute; left: 80px; top: 50%;
       transform: translateY(-50%);">
    
    <!-- 章节编号 -->
    <div style="font-size: 64px; font-weight: bold; 
         color: var(--color-muted); opacity: 0.3;">
      02
    </div>
    
    <!-- 章节标题 -->
    <h1 style="font-size: 48px; color: var(--color-primary);
         margin-top: -20px;">
      研究方法
    </h1>
    
    <!-- 简短说明 -->
    <p style="font-size: 18px; color: var(--color-muted); 
         margin-top: 16px;">
      Study Design & Statistical Analysis
    </p>
    
  </div>
  
</body>
```

---

## 布局组合建议

### 学术报告 (15页)

```
1. title-centered      - 标题页
2. section-divider     - "背景"
3. bullets             - 研究背景
4. split-image-text    - 研究问题可视化
5. section-divider     - "方法"
6. bullets             - 研究设计
7. cards               - 纳入/排除标准
8. section-divider     - "结果"
9. chart-annotation    - 主要结果1
10. chart-annotation   - 主要结果2
11. table              - 亚组分析
12. section-divider    - "讨论"
13. bullets            - 临床意义
14. bullets            - 研究局限
15. title-centered     - 结论/致谢
```

### 商业汇报 (10页)

```
1. title-editorial     - 封面
2. big-number          - 核心指标
3. cards               - 三个关键发现
4. chart-annotation    - 趋势分析
5. split-image-text    - 成功案例
6. table               - 竞品对比
7. bullets             - 战略建议
8. cards               - 下一步计划
9. big-number          - 预期目标
10. title-centered     - 谢谢/联系方式
```

---

## CSS工具类

```css
/* Flexbox工具 */
.row { display: flex; flex-direction: row; }
.col { display: flex; flex-direction: column; }
.fit { flex: 0 0 auto; }  /* 不伸缩，按内容大小 */
.grow { flex: 1 1 0; }    /* 均匀填充 */

/* 对齐 */
.center { justify-content: center; align-items: center; }
.between { justify-content: space-between; }
.around { justify-content: space-around; }

/* 背景 */
.bg-primary { background: var(--color-primary); }
.bg-surface { background: var(--color-surface); }
.bg-white { background: #ffffff; }

/* 文字 */
.text-primary { color: var(--color-primary); }
.text-muted { color: var(--color-muted); }
.text-white { color: #ffffff; }
.text-center { text-align: center; }
.bold { font-weight: bold; }
```

---

## 间距速查表

| 用途 | 像素值 | 场景 |
|-----|-------|------|
| 页面边距 | 20-40px | 内容到幻灯片边缘 |
| 标题下方 | 16-24px | 标题与内容之间 |
| 段落间距 | 12-16px | 段落之间 |
| 列表项间距 | 8-12px | 列表项之间 |
| 卡片间距 | 16-20px | 卡片之间 |
| 元素内边距 | 12-20px | 卡片/框内部 |
| 紧凑间距 | 4-8px | 相关元素紧密排列 |
