# Baoyu Skills 快速开始指南

## ✅ 已配置的 API Keys

| 服务 | API Key | 状态 |
|------|---------|------|
| **Gemini CLI** | `AIzaSyBHRUS...17sCg` | ✅ 已配置 |
| **Gemini Nano** | `AIzaSyDs_a...lH_U` | ✅ 已配置 |

---

## 🔧 配置文件位置

| 级别 | 路径 | 说明 |
|------|------|------|
| **用户级** | `C:\Users\13466\.baoyu-skills\.env` | 全局默认配置 ✅ |
| **项目级** | `D:\claudecode\.baoyu-skills\.env` | 项目特定配置（可选） |

---

## 🚀 快速测试

### 测试 1: Gemini Web 文本生成
```bash
# 带代理
HTTP_PROXY=http://127.0.0.1:7897 HTTPS_PROXY=http://127.0.0.1:7897 /baoyu-danger-gemini-web "你好，Gemini！"

# 不带代理（如果网络允许）
/baoyu-danger-gemini-web "Hello, Gemini!"
```

### 测试 2: AI 图像生成
```bash
# 基础测试
/baoyu-image-gen --prompt "A cute cat" --image test-cat.png

# 使用 Gemini Nano API Key
GOOGLE_API_KEY=AIzaSyDs_alnQ2BNI9ge2Z0bw2PrJxCzEn9lH_U /baoyu-image-gen --prompt "A sunset" --image test-sunset.png
```

### 测试 3: 小红书图片生成
```bash
/baoyu-xhs-images "今日星座运势" --style cute --layout balanced
```

---

## 📝 使用示例

### 示例 1: 生成小红书信息图
```bash
# 从文件生成
/baoyu-xhs-images posts/article.md --style notion --layout list

# 直接输入内容
/baoyu-xhs-images "人工智能的未来发展趋势"
```

### 示例 2: 创建专业信息图
```bash
# 自动推荐布局和风格
/baoyu-infographic data.md

# 指定布局和风格
/baoyu-infographic data.md --layout pyramid --style technical-schematic --aspect portrait
```

### 示例 3: 生成文章封面
```bash
# 自动选择所有维度
/baoyu-cover-image article.md

# 快速模式（跳过确认）
/baoyu-cover-image article.md --quick

# 自定义维度
/baoyu-cover-image article.md --type conceptual --style blueprint --mood bold --aspect 16:9
```

### 示例 4: 生成幻灯片
```bash
# 基础生成
/baoyu-slide-deck presentation.md

# 指定风格和幻灯片数量
/baoyu-slide-deck presentation.md --style corporate --slides 15 --audience executives

# 只生成大纲（不生成图片）
/baoyu-slide-deck presentation.md --outline-only
```

### 示例 5: 生成漫画
```bash
# 自动选择风格和基调
/baoyu-comic story.md

# 指定艺术风格和基调
/baoyu-comic story.md --art manga --tone warm

# 使用预设风格
/baoyu-comic story.md --style ohmsha --layout webtoon
```

---

## 🌐 代理配置

### 方式 1: 临时设置（推荐用于测试）
```bash
HTTP_PROXY=http://127.0.0.1:7897 HTTPS_PROXY=http://127.0.0.1:7897 /baoyu-danger-gemini-web "测试"
```

### 方式 2: 永久设置（添加到 .env）
编辑 `~/.baoyu-skills/.env`，取消注释：
```bash
HTTP_PROXY=http://127.0.0.1:7897
HTTPS_PROXY=http://127.0.0.1:7897
```

### 方式 3: PowerShell 环境变量
```powershell
$env:HTTP_PROXY="http://127.0.0.1:7897"
$env:HTTPS_PROXY="http://127.0.0.1:7897"
```

---

## 🔑 API Key 切换

### 使用 Gemini CLI (默认)
```bash
# 已在 .env 中配置，直接使用
/baoyu-danger-gemini-web "测试"
```

### 使用 Gemini Nano
```bash
# 临时切换
GOOGLE_API_KEY=AIzaSyDs_alnQ2BNI9ge2Z0bw2PrJxCzEn9lH_U /baoyu-danger-gemini-web "测试"

# 或创建项目级 .env 覆盖
mkdir -p .baoyu-skills
echo "GOOGLE_API_KEY=AIzaSyDs_alnQ2BNI9ge2Z0bw2PrJxCzEn9lH_U" > .baoyu-skills/.env
```

---

## ⚠️ 故障排除

### 问题 1: 网络连接失败
**解决方案**: 设置代理
```bash
HTTP_PROXY=http://127.0.0.1:7897 HTTPS_PROXY=http://127.0.0.1:7897 [命令]
```

### 问题 2: API Key 无效
**检查**:
1. 访问 https://aistudio.google.com/api-keys
2. 确认 Key 状态为启用
3. 检查项目配额

### 问题 3: 找不到技能
**检查**:
```bash
# 验证技能路径
ls ~/.claude/skills/mindsymphony/extensions/creative/baoyu-visual/
ls ~/.claude/skills/mindsymphony/integrations/baoyu-ai/
```

---

## 📚 更多资源

- **完整文档**: `mindsymphony/BAOYU_INTEGRATION.md`
- **各技能索引**: 见对应子目录的 `_INDEX.md`
- **原始仓库**: https://github.com/JimLiu/baoyu-skills
- **API 管理**: https://aistudio.google.com/api-keys?projectFilter=gen-lang-client-0521395556

---

## 🎯 推荐工作流

### 内容创作 → 小红书发布
```bash
# 1. 生成内容
echo "今日AI趋势分析..." > article.md

# 2. 生成小红书图片
/baoyu-xhs-images article.md --style fresh --layout dense

# 3. 查看生成的图片
ls xhs-images/
```

### 数据可视化工作流
```bash
# 1. 准备数据
echo "# 销售数据
- Q1: 100万
- Q2: 150万
- Q3: 200万
- Q4: 250万" > data.md

# 2. 生成信息图
/baoyu-infographic data.md --layout pyramid --style corporate-memphis

# 3. 压缩图片
/baoyu-compress-image infographic-*.png
```

---

**配置完成时间**: 2026-01-24
**配置状态**: ✅ 就绪
