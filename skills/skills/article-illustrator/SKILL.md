---
name: article-illustrator
description: 分析文章内容，在需要配图的位置自动生成插画。当用户要求给文章配图、生成插画、为文章添加图片时使用。
triggers:
  zh: [给文章配图, 文章插画, 自动配图, 生成插画, 文章插图]
  en: [article illustration, auto illustrate, generate images for article]
type: creative
layer: shu
---

# 文章插画师 (Article Illustrator)

> 让 Agent 自动为文章生成精美插画，从分析到配图全程无人值守。

---

## 核心能力

### 自动化配图流程
1. **智能分析**：分析文章结构，识别需要视觉辅助的位置
2. **风格匹配**：根据文章主题自动选择最适合的插画风格
3. **提示词生成**：为每张配图生成详细的提示词
4. **图像生成**：调用图像生成工具创建图片
5. **自动插入**：将图片精准插入文章对应位置

---

## 风格库

以下9种风格可供选择。未指定风格时，Agent 将根据文章内容自动匹配。

| 风格 | 配色 | 视觉元素 | 适用场景 |
|------|------|----------|----------|
| **tech** | 蓝紫渐变、霓虹点缀 | 电路纹理、数据流、几何图形 | 科技、AI、编程、数据相关 |
| **warm** | 橙黄暖调、柔和渐变 | 手绘元素、圆润形状、生活场景 | 情感、生活、个人成长、人文 |
| **minimal** | 黑白灰 + 单点彩 | 线条、负空间、抽象符号 | 极简、设计、哲学、抽象概念 |
| **playful** | 鲜艳对比色 | 卡通元素、涂鸦风格、夸张表情 | 轻松话题、教程、趣味内容 |
| **notion** | 莫兰迪色系 | 线稿风、图标、扁平化 | 知识整理、笔记、方法论 |
| **nature** | 绿棕大地色 | 植物、有机纹理、自然形态 | 环保、户外、健康、可持续 |
| **business** | 深蓝深灰 + 金色 | 图表、商务人物、建筑剪影 | 商业、管理、职场、创业 |
| **retro** | 复古色调 | 像素风、老式插画、怀旧元素 | 怀旧、历史、复古风格内容 |
| **abstract** | 高饱和渐变 | 流体、几何、超现实组合 | 前沿概念、元宇宙、未来科技 |

### 风格详细参数

每种风格的详细参数存储在 `styles/` 目录下，按需加载：

```
styles/
├── tech.md      # 科技风格详细参数
├── warm.md      # 温暖风格详细参数
├── minimal.md   # 极简风格详细参数
├── playful.md   # 趣味风格详细参数
├── notion.md    # 线稿风格详细参数
├── nature.md    # 自然风格详细参数
├── business.md  # 商务风格详细参数
├── retro.md     # 复古风格详细参数
└── abstract.md  # 抽象风格详细参数
```

需要时使用 `Read` 工具加载对应风格文件。

---

## 自动风格选择规则

当用户未指定风格时，根据文章内容关键词自动匹配：

### 关键词映射表

| 关键词信号 | 匹配风格 |
|-----------|----------|
| AI、算法、数据、代码、编程、技术、机器学习 | tech |
| 情感、生活、成长、心情、故事、温暖 | warm |
| 设计、美学、哲学、本质、核心、原则 | minimal |
| 教程、入门、轻松、简单、有趣 | playful |
| 笔记、整理、方法、框架、模型 | notion |
| 自然、环保、健康、户外、植物 | nature |
| 商业、管理、职场、创业、营销 | business |
| 历史、回忆、经典、怀旧、传统 | retro |
| 未来、元宇宙、虚拟、前沿、想象 | abstract |

### 匹配逻辑

1. 扫描文章标题和每段首句
2. 统计各风格关键词出现频率
3. 选择频率最高的风格
4. 如果关键词稀疏，默认使用 `minimal` 风格

---

## 工作流程

### 触发条件

当用户说以下内容时激活：
- "给这篇文章配图"
- "为文章生成插画"
- "给文章添加插图"
- "article-illustrator path/to/article.md"

### 执行步骤

#### 步骤 1：读取文章

```bash
# 使用 Read 工具读取文章
Read <文章路径>
```

#### 步骤 2：分析文章结构

识别需要配图的位置，判断标准：

**需要配图的信号**：
- 抽象概念需要可视化
- 流程步骤需要图解
- 核心论点需要强化
- 数据信息需要呈现
- 技术原理需要演示

**不需要配图的信号**：
- 纯描述性内容
- 已经很直观的信息
- 过于琐碎的细节

**配图密度原则**：
- 每 500-800 字考虑一张配图
- 优先在章节开头、关键概念处配图
- 宁多勿少（用户可删除，但重新生成耗时）

#### 步骤 3：确定风格

```bash
# 如果用户指定了 --style 参数
style = user_specified_style

# 否则自动匹配
style = analyze_article_keywords(article_content)
```

#### 步骤 4：生成配图方案

为每个配图位置生成方案，包含：

| 字段 | 说明 |
|------|------|
| 位置 | 插入位置（段落前/后） |
| 目的 | 配图目的（说明概念/强化论点/展示流程） |
| 视觉内容 | 具体要画什么 |
| 文件名 | 生成图片的文件名 |
| 提示词 | 详细提示词（下一步生成） |

示例输出格式：

```markdown
## 配图方案

### 配图 1
- 位置：第2段后
- 目的：可视化"渐进式加载"概念
- 视觉内容：一个分层加载的示意图
- 文件名：imgs/progressive-loading-01.png
```

#### 步骤 5：生成提示词

为每张图生成详细提示词，使用模板：

```
参考模板：prompts/system.md
风格参数：styles/{style}.md
具体内容：配图方案的"视觉内容"字段
```

生成的提示词保存到 `imgs/prompts/` 目录：

```bash
# 创建提示词目录
mkdir -p imgs/prompts

# 保存每张图的提示词
prompt_file = imgs/prompts/{文件名}.txt
```

#### 步骤 6：生成图片

使用统一图像生成接口（优先 Vertex AI Imagen 4，智谱 CogView 备用）：

```bash
# 方法 1：批量生成（推荐）
python scripts/batch_generate.py imgs/prompts/ --output imgs/

# 方法 2：单张生成
python scripts/generate_unified.py "{提示词}" --output imgs/001.png --model vertex-ultra
```

**重试机制**：
- 自动指数退避重试（默认 2 次）
- Vertex AI 失败自动切换智谱 CogView
- 统计成功/失败数量

**可选模型**：
- `vertex-ultra` - Vertex AI Imagen 4 Ultra（最高质量，默认）
- `vertex-std` - Vertex AI Imagen 4（标准质量）
- `vertex-fast` - Vertex AI Imagen 4 Fast（快速）
- `zhipu` - 智谱 CogView（备用）

#### 步骤 7：插入图片

将生成的图片插入文章对应位置：

```markdown
![图片描述](imgs/xxx.png)
```

**插入原则**：
- 精准插入到方案指定的位置
- 添加简洁的图片描述
- 保持原有文章结构

#### 步骤 8：输出总结

```markdown
## 配图完成

- 使用风格：{style}
- 生成图片：{count} 张
- 插入位置：{列表}

### 配图清单
1. imgs/xxx.png - 第N段 - 可视化{概念}
2. imgs/yyy.png - 第M段 - 展示{流程}
...
```

---

## 文件管理规范

### 目录结构

```
article-illustrator/
├── SKILL.md                 # 主文件（本文件）
├── styles/                  # 风格库
│   ├── tech.md
│   ├── warm.md
│   └── ...
├── prompts/                 # 提示词模板
│   └── system.md            # 通用系统提示词
└── examples/                # 示例文章
    ├── sample-article.md
    └── ...
```

### 输出文件结构

```
{文章目录}/
├── {原文章}.md              # 已插入图片的文章
└── imgs/
    ├── prompts/             # 提示词存档
    │   ├── 001.txt
    │   └── ...
    ├── 001.png             # 生成的图片
    └── ...
```

### 命名规范

- 图片文件：`{序号:03d}-{关键词}.png`
- 提示词文件：`{序号:03d}-{关键词}.txt`
- 序号从 001 开始递增

---

## 配图原则

### 核心原则

**配图服务于内容**：
- 补充信息
- 具象概念
- 引导想象

**避免**：
- 重复文章中已经很直观的信息
- 为了配图而配图
- 与内容无关的装饰性图片

### 质量标准

好的配图应该：
- 帮助读者理解内容
- 风格统一协调
- 视觉清晰美观
- 与上下文呼应

---

## 用户交互

### 初始命令

```bash
# 基础用法
article-illustrator path/to/article.md

# 指定风格
article-illustrator path/to/article.md --style tech

# 指定配图数量
article-illustrator path/to/article.md --count 5
```

### 调整指令

生成后用户可以要求调整：

```bash
# 调整数量
"配图太少，再加两张"
"配图太多，删掉第3张"

# 调整内容
"把第二张配图添加一点文字说明"
"在第二章加一张流程图"

# 调整风格
"风格太冷了，换成 warm 风格"
"重新生成，用 playful 风格"
```

---

## 依赖技能

本技能依赖以下技能或工具：

1. **统一图像生成接口** (scripts/)
   - `generate_unified.py` - 单张图像生成
   - `batch_generate.py` - 批量图像生成
   - 支持 Vertex AI Imagen 4 和智谱 CogView
   - 自动重试和提供商切换

2. **图像生成凭证**
   - Vertex AI: `VERTEX_ACCESS_TOKEN` (OAuth 2.0, 1小时有效)
   - 智谱: `ZHIPU_API_KEY` (JWT 格式)

3. **文件操作技能**
   - Read 工具（读取文章）
   - Write 工具（插入图片）

### 配置说明

图像生成凭证配置在 `.env` 文件中：

```bash
# Vertex AI OAuth Token (运行 scripts/get_token.py 获取)
VERTEX_ACCESS_TOKEN=ya29.a0AUMWg_...

# 智谱 API Key
ZHIPU_API_KEY=id.secret
```

**刷新 Vertex AI Token**：
```bash
cd C:\Users\13466\.claude\skills\gemini-image-gen
python scripts/get_token.py
```

4. **目录操作**
   - Bash 工具（创建目录）

---

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| 图像生成失败 | 检查图像生成工具是否可用，尝试重试 |
| 风格文件缺失 | 使用 `Read` 工具加载 `styles/{style}.md` |
| 图片插入位置错误 | 手动调整或重新指定位置 |
| 提示词质量不佳 | 检查 `prompts/system.md` 模板 |

---

## 版本历史

### v1.0.0 (2025-01-16)
- 初始版本
- 支持9种预设风格
- 自动风格匹配
- 完整配图流程
