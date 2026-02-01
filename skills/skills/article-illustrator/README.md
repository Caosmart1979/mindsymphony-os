# Article Illustrator Skill

> 自动为文章生成精美插画的 Agent Skill

## 简介

`article-illustrator` 是一个 Claude Code Skill，可以自动分析文章内容，在需要配图的位置生成符合主题风格的插画。

## 功能特性

- **智能分析**：自动识别文章中需要配图的位置
- **风格匹配**：根据文章主题自动选择最适合的插画风格
- **提示词生成**：为每张配图生成详细的图像生成提示词
- **图像生成**：调用图像生成工具创建图片
- **自动插入**：将图片精准插入文章对应位置

## 支持的风格

| 风格 | 适用场景 |
|------|----------|
| tech | 科技、AI、编程、数据 |
| warm | 情感、生活、个人成长 |
| minimal | 设计、哲学、抽象概念 |
| playful | 教程、入门、趣味内容 |
| notion | 知识整理、笔记、方法论 |
| nature | 环保、户外、健康 |
| business | 商业、管理、职场 |
| retro | 怀旧、历史、复古 |
| abstract | 前沿概念、元宇宙、未来 |

## 使用方法

### 基础用法

```
请用 article-illustrator skill 给这篇文章配图：path/to/article.md
```

### 指定风格

```
请用 article-illustrator skill 给这篇文章配图，使用 tech 风格：path/to/article.md
```

### 生成后调整

```
配图太少，再加两张
把第二张配图添加一点文字说明
在第二章加一张流程图
```

## 安装

将此技能放入你的 Claude Code skills 目录：

```bash
cp -r article-illustrator ~/.claude/skills/
```

## 依赖

- Claude Code
- 图像生成工具（Gemini CLI 或其他支持 MCP 的图像生成工具）

## 目录结构

```
article-illustrator/
├── SKILL.md              # 主文件
├── styles/               # 风格库
│   ├── tech.md
│   ├── warm.md
│   └── ...
├── prompts/              # 提示词模板
│   └── system.md
└── examples/             # 示例文章
    └── sample-article.md
```

## 输出示例

```markdown
## 配图完成

- 使用风格：tech
- 生成图片：5 张
- 插入位置：已插入文章对应位置

### 配图清单
1. imgs/001-progressive-loading.png - 第3段 - 可视化"渐进式加载"概念
2. imgs/002-skill-architecture.png - 第6段 - 展示 Skill 架构
3. imgs/003-style-selection.png - 第10段 - 说明风格选择逻辑
4. imgs/004-workflow-diagram.png - 第15段 - 配图工作流程图
5. imgs/005-skill-potential.png - 第20段 - 展示 Skill 应用潜力
```

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| 图像生成失败 | 检查图像生成工具是否可用 |
| 风格文件缺失 | 确保 styles/ 目录完整 |
| 插入位置错误 | 手动调整或重新指定 |

## 原文链接

本 Skill 基于 JimLiu 的文章设计：
https://mp.weixin.qq.com/s/v2ZSlprwT9IGD_S98listg

## 许可

MIT License
