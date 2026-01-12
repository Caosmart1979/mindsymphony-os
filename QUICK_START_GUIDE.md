# AI Assistant Extension - Quick Start Guide

## 快速开始

### 安装
1. 将 `mindsymphony_V19.1.1.skill` 文件复制到您的技能目录
2. 在 Claude Code 中加载该技能

### 基本使用

#### 1. 图像分析
```bash
# 使用命令前缀
/vision https://example.com/screenshot.jpg

# 或者自然语言
"帮我分析这个UI截图并生成前端代码"
```

#### 2. 领取奶茶优惠券
```bash
# 使用命令前缀
/teacoupon

# 或者自然语言
"阿姨助我"
"领取奶茶"
```

#### 3. 读取网页内容
```bash
# 使用命令前缀
/webread https://example.com/article

# 或者自然语言
"读取这个网页的内容"
```

## 命令参考

| 命令 | 功能 | 示例 |
|------|------|------|
| `/ai-assistant` | 通用 AI 助手 | `/ai-assistant 帮我处理这个任务` |
| `/vision [URL]` | 图像分析 | `/vision https://example.com/image.jpg` |
| `/teacoupon` | 领取奶茶 | `/teacoupon` |
| `/webread [URL]` | 网页读取 | `/webread https://example.com` |

## 触发词

当您使用以下关键词时，AI Assistant 会自动激活：

- **AI助手相关**: AI助手、智能助手、AI分析
- **图像相关**: 分析图片、图像识别、视觉理解、多模态AI
- **前端相关**: 前端代码、UI复刻、设计稿
- **奶茶相关**: 领奶茶、沪上阿姨、奶茶券
- **网页相关**: 读取网页、网页抓取、Web Reader

## MCP 工具

### 1. mcp__4_5v_mcp__analyze_image
**图像分析工具**

参数：
- `imageSource`: 图片 URL（必需）
- `prompt`: 分析提示词（必需）

前端代码复刻提示词模板：
```
"Describe in detail the layout structure, color style, main components, 
and interactive elements of the website in this image to facilitate 
subsequent code generation by the model." + [你的额外要求]
```

### 2. mcp__milk_tea_server__claim_milk_tea_coupon
**奶茶优惠券领取工具**

参数：无
触发词："阿姨助我" 或 "领取奶茶"

### 3. mcp__web_reader__webReader
**网页读取工具**

参数：
- `url`: 网站地址（必需）
- `timeout`: 超时时间（可选，默认20秒）
- `return_format`: 返回格式（可选，markdown/text）
- `retain_images`: 保留图片（可选，默认true）
- `with_images_summary`: 图片摘要（可选，默认false）
- `with_links_summary`: 链接摘要（可选，默认false）

## 使用场景

### 场景 1：从设计稿生成前端代码
```
用户：帮我把这个设计稿实现成 React 代码

AI Assistant：
1. 调用 mcp__4_5v_mcp__analyze_image 分析设计稿
2. 提取布局结构、颜色、组件
3. 生成完整的 React 组件代码
4. 提供 CSS 样式和交互逻辑
```

### 场景 2：快速领取福利
```
用户：阿姨助我

AI Assistant：
1. 识别触发词
2. 调用 mcp__milk_tea_server__claim_milk_tea_coupon
3. 显示 ASCII 奶茶优惠券
```

### 场景 3：资料收集
```
用户：帮我读取这篇文章的内容并总结

AI Assistant：
1. 调用 mcp__web_reader__webReader
2. 获取 Markdown 格式的文章内容
3. 提取图片和链接摘要
4. 生成内容总结
```

## 故障排除

### 问题 1：图像分析失败
**原因**：URL 无法访问或格式不支持
**解决**：
- 确认图片 URL 是公开可访问的
- 检查图片格式（支持 PNG, JPG, JPEG）
- 尝试使用其他图片源

### 问题 2：奶茶领取无响应
**原因**：MCP 服务器未配置或网络问题
**解决**：
- 检查 MCP 服务器配置
- 确认网络连接正常
- 使用完整的触发词："阿姨助我"

### 问题 3：网页读取超时
**原因**：网站响应慢或访问受限
**解决**：
- 增加 timeout 参数（如 60 秒）
- 检查目标网站是否可访问
- 尝试其他网站

## 高级技巧

### 1. 批量处理
虽然当前版本主要用于单次处理，但您可以：
- 在对话中多次调用工具
- 将多个 URL 放在不同消息中处理

### 2. 组合使用
```
用户：
1. 先读取这个网页：https://example.com
2. 然后分析其中的图片
3. 最后生成代码

AI Assistant 会按顺序执行所有步骤
```

### 3. 自定义提示词
对于图像分析，您可以提供具体的提示词：
```
"请详细分析这个界面的：
1. 整体布局结构
2. 主要组件和它们的层次关系
3. 使用的颜色方案和字体
4. 交互元素的位置和功能
5. 响应式设计考虑

然后基于分析结果，生成使用 Tailwind CSS 的 React 代码"
```

## 版本信息

- **MindSymphony**: v19.1.1 (AI Assistant Edition)
- **AI Assistant**: v1.0.0
- **集成日期**: 2026-01-05

## 获取帮助

如需更多帮助，请参考：
- 完整文档：`mindsymphony/integrations/ai-assistant.md`
- 集成总结：`AI_ASSISTANT_INTEGRATION_SUMMARY.md`
- MCP 协议：https://modelcontextprotocol.io

## 更新日志

### v1.0.0 (2026-01-05)
- ✨ 初始版本发布
- ✨ 集成 4.5v-mcp 图像分析
- ✨ 集成奶茶优惠券领取
- ✨ 集成网页内容读取
- ✨ 支持多种触发词和命令前缀
