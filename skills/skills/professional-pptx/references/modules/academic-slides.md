# Academic Slides Module

学术论文转PPT的专用指南。

---

## 学术PPT的核心原则

```
学术PPT ≠ 论文朗读
学术PPT = 用视觉讲故事

关键转变:
- 从"完整信息" → "核心信息"
- 从"文字描述" → "图表展示"
- 从"被动阅读" → "主动引导"
```

---

## 标准学术PPT结构

### 会议口头报告 (12-15分钟, 15-20页)

```
1. 标题页 (1页)
   - 标题、作者、机构、会议信息

2. 背景/引言 (2-3页)
   - 研究问题的临床/科学意义
   - 现有研究的局限
   - 研究假设/目的

3. 方法 (2-3页)
   - 研究设计 (一句话 + 流程图)
   - 纳入/排除标准 (表格或图示)
   - 主要变量/结局定义
   - 统计方法 (一句话)

4. 结果 (4-6页)
   - 流程图/样本量
   - 基线特征 (关键指标)
   - 主要结果 (1-2页)
   - 次要结果 (1-2页)
   - 亚组分析 (如有)

5. 讨论 (2-3页)
   - 主要发现的意义
   - 与既往研究对比
   - 研究优势与局限

6. 结论 (1页)
   - 3个Take-home messages

7. 致谢/参考 (1页)
```

### 毕业答辩 (20-30分钟, 25-35页)

```
相比会议报告，需要增加:
- 文献综述部分 (3-5页)
- 方法细节 (4-6页)
- 完整统计分析 (5-8页)
- 创新点强调 (1-2页)
- 未来工作 (1-2页)
```

---

## 各部分设计指南

### 标题页

```html
<body class="col center" style="width: 960px; height: 540px; 
      background: linear-gradient(135deg, #1a365d 0%, #2b6cb0 100%);">
  
  <h1 style="color: white; font-size: 36px; text-align: center;
       max-width: 800px; line-height: 1.3;">
    腹腔镜胃切除术后早期并发症的<br>预测模型构建与验证
  </h1>
  
  <div style="color: rgba(255,255,255,0.9); margin-top: 40px; 
       text-align: center; font-size: 18px;">
    张三<sup>1</sup>，李四<sup>1</sup>，王五<sup>2*</sup>
  </div>
  
  <div style="color: rgba(255,255,255,0.7); margin-top: 16px;
       font-size: 14px; text-align: center;">
    <sup>1</sup>北京医院普通外科 &nbsp;&nbsp;
    <sup>2</sup>北京大学医学部
  </div>
  
  <div style="color: rgba(255,255,255,0.6); margin-top: 60px;
       font-size: 12px;">
    第X届全国XXX学术会议 | 2025年X月X日
  </div>
  
</body>
```

### 研究背景页

**模式1: 问题-影响-空白**

```html
<body class="col" style="width: 960px; height: 540px; padding: 20px 40px;">
  
  <h1 style="margin-bottom: 24px;">研究背景</h1>
  
  <div class="row grow" style="gap: 24px;">
    
    <!-- 左侧: 问题 -->
    <div style="flex: 1; padding: 20px; background: #fff5f5; 
         border-left: 4px solid #e53e3e;">
      <h3 style="color: #e53e3e; margin-bottom: 12px;">临床问题</h3>
      <p style="font-size: 16px; line-height: 1.6;">
        胃癌术后并发症发生率高达<strong>15-25%</strong>，
        严重影响患者预后和医疗资源
      </p>
    </div>
    
    <!-- 右侧: 研究空白 -->
    <div style="flex: 1; padding: 20px; background: #fffaf0;
         border-left: 4px solid #ed8936;">
      <h3 style="color: #ed8936; margin-bottom: 12px;">研究空白</h3>
      <p style="font-size: 16px; line-height: 1.6;">
        目前缺乏<strong>针对中国人群</strong>的术后并发症
        预测模型，现有模型外推性差
      </p>
    </div>
    
  </div>
  
  <!-- 研究问题 -->
  <div style="margin-top: 24px; padding: 16px; background: #ebf8ff;
       border-left: 4px solid #3182ce;">
    <strong style="color: #3182ce;">研究问题：</strong>
    能否建立准确预测腹腔镜胃切除术后早期并发症的风险模型？
  </div>
  
</body>
```

### 方法页 - 研究设计

```html
<body class="col" style="width: 960px; height: 540px; padding: 20px 40px;">
  
  <h1 style="margin-bottom: 20px;">研究方法</h1>
  
  <!-- 研究设计一句话 -->
  <div style="font-size: 18px; color: #2d3748; margin-bottom: 24px;">
    回顾性队列研究 | 2018年1月 - 2023年12月 | 北京医院
  </div>
  
  <!-- 流程图 -->
  <div class="row center grow" style="gap: 40px;">
    
    <!-- 纳入 -->
    <div style="text-align: center;">
      <div style="width: 160px; padding: 16px; background: #e6fffa;
           border: 2px solid #38b2ac; border-radius: 8px;">
        <div style="font-size: 14px; color: #718096;">纳入</div>
        <div style="font-size: 24px; font-weight: bold; color: #2d3748;">1,024</div>
        <div style="font-size: 12px; color: #718096;">例患者</div>
      </div>
    </div>
    
    <div style="font-size: 32px; color: #718096;">→</div>
    
    <!-- 排除 -->
    <div style="text-align: center;">
      <div style="width: 160px; padding: 16px; background: #fff5f5;
           border: 2px solid #fc8181; border-radius: 8px;">
        <div style="font-size: 14px; color: #718096;">排除</div>
        <div style="font-size: 24px; font-weight: bold; color: #2d3748;">256</div>
        <div style="font-size: 10px; color: #718096;">
          急诊手术 (120)<br>
          数据缺失 (136)
        </div>
      </div>
    </div>
    
    <div style="font-size: 32px; color: #718096;">→</div>
    
    <!-- 最终 -->
    <div style="text-align: center;">
      <div style="width: 160px; padding: 16px; background: #ebf8ff;
           border: 2px solid #4299e1; border-radius: 8px;">
        <div style="font-size: 14px; color: #718096;">最终纳入</div>
        <div style="font-size: 24px; font-weight: bold; color: #2d3748;">768</div>
        <div style="font-size: 12px; color: #718096;">例患者</div>
      </div>
    </div>
    
  </div>
  
</body>
```

### 结果页 - 主要发现

```html
<body class="col" style="width: 960px; height: 540px; padding: 20px 40px;">
  
  <h1 style="margin-bottom: 16px;">主要结果</h1>
  
  <div class="row grow" style="gap: 24px;">
    
    <!-- 图表区域 (65%) -->
    <div style="width: 65%;">
      <div class="chart-placeholder" data-placeholder-id="main-chart"
           style="width: 100%; height: 100%; background: #f7fafc;">
      </div>
    </div>
    
    <!-- 解读区域 (35%) -->
    <div class="col" style="width: 35%; justify-content: center;">
      
      <!-- 关键数字 -->
      <div style="background: #1a365d; color: white; padding: 20px;
           border-radius: 8px; text-align: center; margin-bottom: 20px;">
        <div style="font-size: 48px; font-weight: bold;">42%</div>
        <div style="font-size: 14px; opacity: 0.9;">相对风险降低</div>
      </div>
      
      <!-- 统计数据 -->
      <div style="font-size: 14px; line-height: 1.8;">
        <p><strong>OR:</strong> 0.58 (95%CI: 0.42-0.79)</p>
        <p><strong>p值:</strong> <span style="color: #38a169;">&lt;0.001</span></p>
        <p><strong>NNT:</strong> 8</p>
      </div>
      
    </div>
    
  </div>
  
  <div style="font-size: 10px; color: #718096; margin-top: 12px;">
    Figure 1. 两组术后30天并发症发生率比较
  </div>
  
</body>
```

### 讨论页

```html
<body class="col" style="width: 960px; height: 540px; padding: 20px 40px;">
  
  <h1 style="margin-bottom: 24px;">讨论</h1>
  
  <div class="row grow" style="gap: 24px;">
    
    <!-- 主要发现 -->
    <div style="flex: 1; padding: 20px; background: #e6fffa;
         border-radius: 8px;">
      <h3 style="color: #234e52; margin-bottom: 12px;">💡 主要发现</h3>
      <ul style="font-size: 14px; line-height: 1.8; color: #2d3748;">
        <li>新技术显著降低并发症风险</li>
        <li>效果在高龄患者中更明显</li>
        <li>学习曲线约30例</li>
      </ul>
    </div>
    
    <!-- 与既往研究对比 -->
    <div style="flex: 1; padding: 20px; background: #faf5ff;
         border-radius: 8px;">
      <h3 style="color: #553c9a; margin-bottom: 12px;">📚 与既往研究对比</h3>
      <ul style="font-size: 14px; line-height: 1.8; color: #2d3748;">
        <li>与Smith et al. (2022)结果一致</li>
        <li>效应量略高于日本队列</li>
        <li>首次在中国人群中验证</li>
      </ul>
    </div>
    
    <!-- 局限性 -->
    <div style="flex: 1; padding: 20px; background: #fffaf0;
         border-radius: 8px;">
      <h3 style="color: #975a16; margin-bottom: 12px;">⚠️ 研究局限</h3>
      <ul style="font-size: 14px; line-height: 1.8; color: #2d3748;">
        <li>回顾性设计的固有偏倚</li>
        <li>单中心研究</li>
        <li>随访时间较短</li>
      </ul>
    </div>
    
  </div>
  
</body>
```

### 结论页

```html
<body class="col center" style="width: 960px; height: 540px; padding: 40px;">
  
  <h1 style="margin-bottom: 40px;">结论</h1>
  
  <div style="max-width: 700px;">
    
    <!-- Take-home messages -->
    <div style="display: flex; align-items: flex-start; margin-bottom: 24px;">
      <div style="width: 40px; height: 40px; background: #1a365d; 
           color: white; border-radius: 50%; display: flex;
           align-items: center; justify-content: center;
           font-weight: bold; margin-right: 16px; flex-shrink: 0;">1</div>
      <p style="font-size: 20px; line-height: 1.5;">
        新型腹腔镜技术可<strong>显著降低术后并发症风险</strong>
      </p>
    </div>
    
    <div style="display: flex; align-items: flex-start; margin-bottom: 24px;">
      <div style="width: 40px; height: 40px; background: #2b6cb0; 
           color: white; border-radius: 50%; display: flex;
           align-items: center; justify-content: center;
           font-weight: bold; margin-right: 16px; flex-shrink: 0;">2</div>
      <p style="font-size: 20px; line-height: 1.5;">
        高龄患者可能从中<strong>获益更多</strong>
      </p>
    </div>
    
    <div style="display: flex; align-items: flex-start;">
      <div style="width: 40px; height: 40px; background: #38a169; 
           color: white; border-radius: 50%; display: flex;
           align-items: center; justify-content: center;
           font-weight: bold; margin-right: 16px; flex-shrink: 0;">3</div>
      <p style="font-size: 20px; line-height: 1.5;">
        需要<strong>多中心RCT</strong>进一步验证
      </p>
    </div>
    
  </div>
  
</body>
```

---

## 学术PPT常见错误

| 错误 | 问题 | 修正 |
|-----|------|-----|
| 全文复制 | 把论文段落直接粘贴 | 提取关键词重新组织 |
| 数据堆砌 | 每页放3+图表 | 每页1图表+解读 |
| p值过多 | 列出所有统计结果 | 只保留关键p值 |
| 方法过详 | 事无巨细描述 | 一句话+流程图 |
| 缺乏故事 | 罗列事实 | 建立逻辑主线 |

---

## 学术图表规范

### 生存曲线 (Kaplan-Meier)

```javascript
slide.addChart(pptx.charts.LINE, [
  { name: "实验组", labels: months, values: survivalExp },
  { name: "对照组", labels: months, values: survivalCtrl }
], {
  x: 0.5, y: 1.5, w: 6, h: 4,
  lineSize: 3,
  showCatAxisTitle: true,
  catAxisTitle: "随访时间 (月)",
  showValAxisTitle: true,
  valAxisTitle: "生存率 (%)",
  valAxisMinVal: 0,
  valAxisMaxVal: 100,
  chartColors: ["2b6cb0", "e53e3e"]
});

// 添加风险表 (Number at risk)
slide.addText([
  { text: "Number at risk", options: { bold: true } },
  { text: "\n实验组: 156  142  128  115" },
  { text: "\n对照组: 612  580  521  467" }
], { x: 0.5, y: 5.5, fontSize: 10 });
```

### 森林图样式表格

```javascript
// 使用表格模拟森林图
const forestData = [
  ["亚组", "HR (95%CI)", "p值", "效应图"],
  ["年龄 <65岁", "0.72 (0.55-0.94)", "0.015", "●——[——]——●"],
  ["年龄 ≥65岁", "0.51 (0.38-0.69)", "<0.001", "●—[—]—●"],
  ["男性", "0.65 (0.50-0.84)", "0.001", "●——[——]——●"]
];
```

---

## 参考资源

- /mnt/skills/public/pptx/SKILL.md - 技术实现
- references/core/layout-patterns.md - 布局模式
- references/core/design-systems.md - 设计系统
