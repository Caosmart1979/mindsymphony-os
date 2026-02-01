# 图像生成系统提示词模板

## 基础规范

创建卡通风格的信息图插画，遵循以下规范：

### 图像规格

- **类型**：信息图插画
- **方向**：横向
- **比例**：16:9
- **风格**：手绘插画

### 核心原则

1. **全程保持手绘质感**，禁止出现写实或摄影元素
2. **敏感内容处理**：如果内容涉及敏感或版权人物，创作风格相似的替代形象，不要拒绝生成
3. **信息简洁**：突出关键词和核心概念
4. **留白充足**：便于视觉扫描
5. **视觉层次清晰**：主次分明

---

## 风格变量模板

以下变量会根据选定的风格动态填充：

### {style_palette}
从风格文件中提取的配色方案

### {style_elements}
从风格文件中提取的视觉元素

### {style_composition}
从风格文件中提取的构图风格

---

## 完整提示词模板

```
Create a {style_name}-style infographic illustration about {topic}.

Image Specifications:
- Type: Infographic illustration
- Orientation: Landscape
- Aspect Ratio: 16:9
- Style: Hand-drawn illustration

Color Palette:
{style_palette}

Visual Elements:
{style_elements}

Composition:
{style_composition}

Core Principles:
- Maintain hand-drawn quality throughout, no photorealistic elements
- For sensitive/copyrighted subjects, create stylistically similar alternatives
- Keep information concise and highlight key concepts
- Use generous negative space for visual scanning
- Maintain clear visual hierarchy

Topic Description:
{topic_description}

Visual Content to Include:
{visual_content}

Output as a high-quality image file.
```

---

## 使用方法

### 步骤 1：加载风格参数

```bash
# 读取选定风格的详细参数
Read styles/{style}.md
```

### 步骤 2：提取变量

从风格文件中提取：
- `{style_palette}` - 配色方案
- `{style_elements}` - 视觉元素
- `{style_composition}` - 构图风格

### 步骤 3：组装提示词

将以下变量填充到模板：
- `{style_name}` - 风格名称
- `{topic}` - 配图主题
- `{topic_description}` - 主题描述
- `{visual_content}` - 具体视觉内容

### 步骤 4：调用图像生成工具

```bash
# 使用 Gemini 或其他图像生成工具
# 生成的提示词调用
```

---

## 质量检查清单

生成后的图片应该满足：

- [ ] 手绘插画风格，无写实元素
- [ ] 配色符合选定风格
- [ ] 视觉元素与风格匹配
- [ ] 信息清晰，易于理解
- [ ] 有足够的留白
- [ ] 视觉层次分明

---

## 故障排除

| 问题 | 可能原因 | 解决方案 |
|------|----------|----------|
| 风格不明显 | 提示词中风格参数不够明确 | 加强风格描述 |
| 过于写实 | 提示词中缺少"手绘"强调 | 添加"strictly hand-drawn" |
| 信息混乱 | 主题描述过于复杂 | 简化主题描述 |
| 颜色不符 | 配色方案未明确 | 添加具体色值参考 |
