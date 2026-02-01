# 🎨 三种 AI 图片增强方案

## 方案对比

| 方案 | 优点 | 缺点 | 推荐度 |
|------|------|------|--------|
| **A. 手动生成关键图片** | 快速、可控、高质量 | 需要手动插入 | ⭐⭐⭐⭐⭐ |
| **B. 使用 baoyu-infographic** | 自动生成信息图 | 仅限数据页 | ⭐⭐⭐⭐ |
| **C. 完整手动流程** | 完全自定义 | 耗时长、复杂 | ⭐⭐⭐ |

---

## 📋 方案A：手动生成关键图片（推荐）

### 步骤1：生成封面图
```bash
cd /d/claudecode

# 使用 Gemini 生成封面
HTTP_PROXY=http://127.0.0.1:7897 HTTPS_PROXY=http://127.0.0.1:7897 \
/baoyu-danger-gemini-web \
  --prompt "Professional scientific presentation cover with medical theme, DNA helix, molecular structures, deep blue color scheme, Chinese title '老年胃肠肿瘤精准诊疗科研工作汇报', high quality, 16:9 aspect ratio" \
  --image slide-cover.png
```

### 步骤2：生成科研思路图
```bash
# 使用 Gemini 生成三-tier体系图
HTTP_PROXY=http://127.0.0.1:7897 HTTPS_PROXY=http://127.0.0.1:7897 \
/baoyu-danger-gemini-web \
  --prompt "Scientific research system infographic showing three tiers: Big Data Mining (NHANES) → Omics Technology (Lipidomics + Gut Microbiome) → Clinical Translation (Biomarkers + Nutrition Intervention), clean flowchart design with arrows, professional blue color scheme, Chinese labels" \
  --image slide-research-system.png
```

### 步骤3：生成技术路线图
```bash
# 生成脂质组学技术路线
HTTP_PROXY=http://127.0.0.1:7897 HTTPS_PROXY=http://127.0.0.1:7897 \
/baoyu-danger-gemini-web \
  --prompt "Lipidomics research workflow diagram showing: Exosome Isolation → Mass Spectrometry → Data Analysis → Biomarker Discovery, clean technical schematic with icons, professional scientific presentation style" \
  --image slide-lipidomics-workflow.png
```

### 步骤4：生成专利技术图
```bash
# 生成免还纳技术示意图
HTTP_PROXY=http://127.0.0.1:7897 HTTPS_PROXY=http://127.0.0.1:7897 \
/baoyu-danger-gemini-web \
  --prompt "Medical device illustration of innovative intestinal stoma technology with T-shaped drainage component, showing how it avoids second surgery, clean technical schematic with labels, professional medical device presentation style, blue color scheme" \
  --image slide-patent-tech.png
```

### 步骤5：生成未来规划图
```bash
# 生成2026年任务路线图
HTTP_PROXY=http://127.0.0.1:7897 HTTPS_PROXY=http://127.0.0.1:7897 \
/baoyu-danger-gemini-web \
  --prompt "Strategic roadmap for 2026 showing three parallel tracks: 1) Clinical Research (STARS-GC09, 300 cases), 2) Technology Promotion (cost reduction to 4%), 3) Academic Conclusion (high-impact papers), timeline infographic style, professional presentation" \
  --image slide-future-roadmap.png
```

### 步骤6：插入图片到PPT
1. 打开 `老年胃肠肿瘤科研工作汇报_自动生成版.pptx`
2. 选择对应的页面
3. 插入 → 图片 → 选择生成的图片
4. 调整大小和位置

**预计时间**：10-15分钟
**图片数量**：5-6张关键页
**效果**：专业、高质量

---

## 📊 方案B：使用 baoyu-infographic 生成信息图

### 生成成果总结信息图
```bash
# 生成科研产出信息图
/baoyu-infographic << 'EOF'
# 科研成果总结

## 课题执行
- 兵团课题一：2023AB018-131，进展顺利
- 兵团课题二：TDZKCX202210，已结题

## 学术产出
- SCI论文：2篇（总IF > 8）
- 专利：2项（免还纳技术）
- 培养人才：2名硕士

## 项目成果
- 脂组学：4篇论文（超额完成）
- 维生素项目：按期执行
- 临床转化：费用降至4%
EOF
```

### 生成科研思路信息图
```bash
# 生成全链条体系信息图
/baoyu-infographic << 'EOF'
# 老年胃肠肿瘤全链条精准诊疗体系

## 上游：精准评估
- NHANES大数据挖掘
- 识别"隐形杀手"
- 重新定义高危人群

## 中游：机制解析
- 脂质组学技术
- 肠道菌群测序
- 发现标志物和靶点

## 下游：微创干预
- 机器人手术
- 专利技术创新
- 拒绝二次伤害
EOF
```

**预计时间**：5-10分钟
**图片数量**：2-3张
**效果**：数据可视化清晰

---

## 🔧 方案C：完整手动流程（高级用户）

### 完整工作流程
1. **分析内容** → 手动完成（已有内容文档）
2. **生成大纲** → 手动创建（已在PPT中体现）
3. **生成提示词** → 使用 `关键页面图片提示词.md`
4. **生成图片** → 逐个使用 baoyu-image-gen
5. **合并到PPT** → 手动插入和调整

### 批量生成脚本示例
```python
import subprocess
import os

# 图片配置
slides = [
    {
        "name": "slide-cover.png",
        "prompt": "Professional scientific presentation cover..."
    },
    {
        "name": "slide-research-system.png",
        "prompt": "Three-tier research system infographic..."
    },
    # ... 更多配置
]

# 批量生成
for slide in slides:
    cmd = [
        "npx", "-y", "bun",
        "C:\\Users\\13466\\.claude\\skills\\mindsymphony\\integrations\\baoyu-ai\\baoyu-image-gen\\scripts\\main.ts",
        "--prompt", slide["prompt"],
        "--image", slide["name"],
        "--provider", "google"
    ]
    subprocess.run(cmd)
    print(f"✅ Generated {slide['name']}")
```

**预计时间**：30-60分钟
**图片数量**：全部页面（14张）
**效果**：完全自定义

---

## 🎯 推荐方案：方案A

### 为什么推荐方案A？
1. ✅ **快速高效**：10-15分钟完成
2. ✅ **重点突出**：只生成关键页图片
3. ✅ **质量保证**：使用 Gemini 高质量生成
4. ✅ **易于调整**：手动插入更灵活

### 立即开始
选择方案A，我可以帮您：
1. 生成5-6张关键页面的 AI 图片
2. 提供插入到 PPT 的具体指导
3. 确保视觉效果专业美观

**您想使用哪个方案？**
- 回复 "A" → 方案A（手动生成关键图片）
- 回复 "B" → 方案B（信息图自动生成）
- 回复 "C" → 方案C（完整手动流程）
- 回复 "全部" → 依次执行所有方案
