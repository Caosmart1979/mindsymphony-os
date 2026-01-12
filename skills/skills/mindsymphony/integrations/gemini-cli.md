---
name: gemini-cli
type: integration
external_path: /mnt/skills/user/gemini-cli-integration
priority: medium
triggers:
  zh: [gemini, 视频分析, 音频转录, 大文件, 100万token, 多模态, 图片分析, 仓库扫描]
  en: [gemini, video, audio, large file, multimodal, million token, image, repo]
security_level: external_call
---

# Gemini CLI集成 快捷入口

> 补齐Claude Code的多模态短板：视频、音频、超大文件处理。

---

## 核心能力

1. **视频分析** - 总结、提取关键帧、生成时间线
2. **音频转录** - 会议录音、访谈记录
3. **图片分析** - UI截图审查、图表提取
4. **大文件处理** - 100万token上下文，整仓库分析

---

## 触发词

### 中文
- 用Gemini、分析视频、转录音频
- 大文件、超大上下文
- 图片分析、仓库扫描

### English
- gemini, video summary, audio transcription
- large file, million token context
- image analysis, repo scan

---

## 命令前缀

```
/gemini [你的多模态任务]
```

---

## 能力对比

| 能力 | Claude Code | Gemini CLI |
|------|-------------|------------|
| 文本处理 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 图片分析 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 视频理解 | ❌ | ⭐⭐⭐⭐⭐ |
| 音频转录 | ❌ | ⭐⭐⭐⭐⭐ |
| 上下文窗口 | 200K | 1M |
| 代码执行 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

**协同策略**：Claude Code编排 + Gemini CLI多模态

---

## 使用示例

### 示例1：视频总结

```
用户：用Gemini总结这个产品演示视频 demo.mp4

激活：gemini-cli
执行：gemini -p "总结这个视频的关键功能点" demo.mp4 --yolo
返回：结构化的功能清单和时间线
```

### 示例2：代码仓库分析

```
用户：Gemini帮我分析整个项目的架构

激活：gemini-cli
执行：gemini -p "分析项目架构，输出技术栈和模块依赖" . --yolo
返回：架构概览、技术栈、依赖图
```

### 示例3：UI截图审查

```
用户：用Gemini检查这个UI截图的问题 screenshot.png

激活：gemini-cli
执行：gemini -p "审查UI设计，列出潜在问题" screenshot.png --yolo
返回：设计问题清单、优化建议
```

---

## ⚠️ 重要提醒

```bash
# 必须加 --yolo 参数！否则命令会卡住
gemini -p "你的prompt" file.ext --yolo
```

---

## 详细文档

完整文档位置：`/mnt/skills/user/gemini-cli-integration/SKILL.md`

包含：
- 安装配置指南
- 5大使用场景详解
- 故障排查指南
- Subagent定义
