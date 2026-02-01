# 使用 Gemini API Key 生成科研汇报图片

## 配置检查

您已配置的 Gemini API Keys：
- **主Key**: `AIzaSyBHRUSDCraCH_cCBG0KUVSP4wQpkt17sCg`
- **备用Key**: `AIzaSyDs_alnQ2BNI9ge2Z0bw2PrJxCzEn9lH_U`

⚠️ **注意**：主 Key 最后是 `Cg` 不是 `Gg`！

## 生成命令

### 图片1：封面图
```bash
cd /d/claudecode

GOOGLE_API_KEY=AIzaSyBHRUSDCraCH_cCBG0KUVSP4wQpkt17sCg \
npx -y bun "C:\\Users\\13466\\.claude\\skills\\mindsymphony\\integrations\\baoyu-ai\\baoyu-image-gen\\scripts\\main.ts" \
  --prompt "Professional scientific research presentation cover with title '老年胃肠肿瘤精准诊疗科研工作汇报', subtitle '曹祥龙医生团队 | 北京医院/塔里木大学', medical theme with DNA helix and molecular structures, deep blue color scheme, clean modern style, 16:9 aspect ratio, high quality" \
  --image slide-images/01-cover.png \
  --provider google \
  --ar 16:9
```

### 图片2：科研体系图
```bash
GOOGLE_API_KEY=AIzaSyBHRUSDCraCH_cCBG0KUVSP4wQpkt17sCg \
npx -y bun "C:\\Users\\13466\\.claude\\skills\\mindsymphony\\integrations\\baoyu-ai\\baoyu-image-gen\\scripts\\main.ts" \
  --prompt "Scientific research system diagram showing three tiers: 上游精准评估(NHANES大数据), 中游机制解析(脂质组学+肠道菌群), 下游微创干预(机器人手术+专利), clean flowchart with arrows, deep blue color scheme, professional medical research style, Chinese labels, 16:9 aspect ratio" \
  --image slide-images/02-research-system.png \
  --provider google \
  --ar 16:9
```

### 图片3：成果总结图
```bash
GOOGLE_API_KEY=AIzaSyBHRUSDCraCH_cCBG0KUVSP4wQpkt17sCg \
npx -y bun "C:\\Users\\13466\\.claude\\skills\\mindsymphony\\integrations\\baoyu-ai\\baoyu-image-gen\\scripts\\main.ts" \
  --prompt "Scientific achievement summary slide showing six key points: 2项兵团课题, 脂组学项目结题(超额完成), 维生素项目按期执行, 2篇SCI论文, 2项专利, 全链条诊疗体系, professional summary with icons, clean layout, deep blue theme, Chinese text, 16:9 aspect ratio" \
  --image slide-images/03-achievements.png \
  --provider google \
  --ar 16:9
```

### 图片4：专利技术图
```bash
GOOGLE_API_KEY=AIzaSyBHRUSDCraCH_cCBG0KUVSP4wQpkt17sCg \
npx -y bun "C:\\Users\\13466\\.claude\\skills\\mindsymphony\\integrations\\baoyu-ai\\baoyu-image-gen\\scripts\\main.ts" \
  --prompt "Medical device illustration showing 免还纳回肠造口专利技术 with T-shaped drainage component, comparison: traditional surgery 25000元 vs this technology 1000元 (96% cost reduction), technical schematic style, professional medical device presentation, deep blue color scheme, Chinese labels, 16:9 aspect ratio" \
  --image slide-images/04-patent-tech.png \
  --provider google \
  --ar 16:9
```

### 图片5：未来规划图
```bash
GOOGLE_API_KEY=AIzaSyBHRUSDCraCH_cCBG0KUVSP4wQpkt17sCg \
npx -y bun "C:\\Users\\13466\\.claude\\skills\\mindsymphony\\integrations\\baoyu-ai\\baoyu-image-gen\\scripts\\main.ts" \
  --prompt "Strategic roadmap for 2026年三大重点任务: 1)推数据-STARS-GC09多中心研究(300例), 2)推转化-免还纳技术推广(吻合口漏率≤5%), 3)推结题-兵团课题结题(高分SCI), professional timeline infographic with three parallel tracks, milestone markers, deep blue color scheme, Chinese text, 16:9 aspect ratio" \
  --image slide-images/05-future-roadmap.png \
  --provider google \
  --ar 16:9
```

### 图片6：脂质组学技术图
```bash
GOOGLE_API_KEY=AIzaSyBHRUSDCraCH_cCBG0KUVSP4wQpkt17sCg \
npx -y bun "C:\\Users\\13466\\.claude\\skills\\mindsymphony\\integrations\\baoyu-ai\\baoyu-image-gen\\scripts\\main.ts" \
  --prompt "Technical workflow diagram showing 脂质组学技术路线: 外泌体分离→质谱检测→数据分析→标志物发现. Key findings: HexCer棕榈酰脂肪酸(ZDHHC4机制), TRG-5菌属, 谷氨酰胺/丁酸代谢通路. Clean scientific workflow with icons, professional research style, deep blue color scheme, Chinese labels, 16:9 aspect ratio" \
  --image slide-images/06-lipidomics-tech.png \
  --provider google \
  --ar 16:9
```

## 批量执行

### Windows PowerShell
```powershell
# 设置 API Key
$env:GOOGLE_API_KEY="AIzaSyBHRUSDCraCH_cCBG0KUVSP4wQpkt17sCg"

# 进入目录
cd D:\claudecode

# 依次生成图片（或并行执行）
npx -y bun "C:\Users\13466\.claude\skills\mindsymphony\integrations\baoyu-ai\baoyu-image-gen\scripts\main.ts" --prompt "..." --image slide-images/01-cover.png --provider google --ar 16:9
# ... 重复其他图片
```

## 注意事项

1. **每张图片生成时间**：约30-90秒
2. **总时间**：约5-10分钟（6张图片）
3. **如果API限流**：等待后重试
4. **图片质量**：Gemini 3 Pro（高质量）

## 验证生成

```bash
# 查看生成的图片
ls -lh slide-images/

# 应该看到：
# 01-cover.png
# 02-research-system.png
# 03-achievements.png
# 04-patent-tech.png
# 05-future-roadmap.png
# 06-lipidomics-tech.png
```
