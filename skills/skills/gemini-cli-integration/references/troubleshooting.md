# Gemini CLI 问题排查指南

常见问题的诊断与解决方案。

---

## 快速诊断流程

```
问题发生
│
├─► 命令完全没响应？
│   └─► 检查1: --yolo参数
│
├─► 报API错误？
│   └─► 检查2: API Key配置
│
├─► 报文件错误？
│   └─► 检查3: 文件路径
│
├─► Claude Code不触发？
│   └─► 检查4: Skill配置
│
└─► 结果不符预期？
    └─► 检查5: Prompt优化
```

---

## 问题1: 命令卡住无响应

### 症状

```
$ gemini -p "hello"
[光标闪烁，无任何输出]
```

### 原因

99%的情况是**没加 `--yolo`**。

Gemini CLI默认需要确认，非交互场景会卡住。

### 解决

```bash
# ❌ 错误
gemini -p "hello"

# ✅ 正确
gemini -p "hello" --yolo
```

### 验证

```bash
gemini -p "说个笑话" --yolo
# 应该立即返回结果
```

---

## 问题2: API Key 错误

### 症状

```
Error: Invalid API key
Error: API key not found
Error: Authentication failed
```

### 诊断

```bash
# 检查环境变量
echo $GEMINI_API_KEY

# 应该输出你的key，如果为空说明没设置
```

### 解决

#### 方法A: 设置环境变量

```bash
# 临时设置（当前会话）
export GEMINI_API_KEY="your-key-here"

# 永久设置
echo 'export GEMINI_API_KEY="your-key-here"' >> ~/.bashrc
source ~/.bashrc
```

#### 方法B: 重新获取Key

1. 访问 https://aistudio.google.com/
2. 登录Google账号
3. API Keys → Create API Key
4. 复制新Key

#### 方法C: 使用OAuth登录

```bash
# 交互式登录
gemini --login
# 按提示在浏览器中授权
```

### 验证

```bash
gemini -p "hello" --yolo
# 应该正常返回
```

---

## 问题3: 文件路径错误

### 症状

```
Error: File not found: image.png
Error: Cannot read file: ~/Documents/report.pdf
```

### 诊断

```bash
# 检查文件是否存在
ls -la image.png

# 检查完整路径
realpath image.png
```

### 常见原因

| 原因 | 错误示例 | 正确示例 |
|------|----------|----------|
| 相对路径问题 | `image.png` | `/home/user/image.png` |
| 波浪号未展开 | `~/doc.pdf`(在某些情况) | `$HOME/doc.pdf` |
| 空格未转义 | `my file.png` | `"my file.png"` |
| 路径不存在 | `/wrong/path/file` | 使用`ls`确认 |

### 解决

```bash
# 使用绝对路径
gemini -p "分析" /home/user/images/screenshot.png --yolo

# 或使用变量展开
gemini -p "分析" "$HOME/images/screenshot.png" --yolo

# 带空格的文件名
gemini -p "分析" "my file with spaces.png" --yolo
```

### 最佳实践

```bash
# 在执行前确认文件存在
FILE="/path/to/file.png"
if [[ -f "$FILE" ]]; then
    gemini -p "分析" "$FILE" --yolo
else
    echo "文件不存在: $FILE"
fi
```

---

## 问题4: Claude Code 不触发 Skill

### 症状

- 说"用Gemini分析"但Claude Code没有调用Gemini
- 直接用Claude Code自己处理了

### 诊断

```bash
# 检查Skill文件是否存在
ls ~/.claude/skills/gemini-cli/SKILL.md

# 检查文件内容
cat ~/.claude/skills/gemini-cli/SKILL.md
```

### 常见原因

#### 原因1: 文件位置不对

```bash
# 正确位置
~/.claude/skills/gemini-cli/SKILL.md

# 常见错误
~/.claude/gemini-cli/SKILL.md  # 缺少skills目录
~/.claude/skills/SKILL.md      # 缺少skill名称目录
```

#### 原因2: Frontmatter格式错误

```yaml
# ❌ 错误：缺少---
name: gemini-cli
description: ...

# ❌ 错误：name缩进不对
---
  name: gemini-cli
---

# ✅ 正确
---
name: gemini-cli
description: "当用户提到Gemini时触发"
---
```

#### 原因3: 触发词不匹配

确保description中包含会触发的词：
- "Gemini"
- "用Gemini"
- "让Gemini"

### 解决

重新创建Skill文件：

```bash
mkdir -p ~/.claude/skills/gemini-cli

cat > ~/.claude/skills/gemini-cli/SKILL.md << 'EOF'
---
name: gemini-cli
description: "当用户提到'用Gemini'、'Gemini分析'、'Gemini帮我'时触发"
---

# Gemini CLI 助手

识别Gemini相关请求，调用gemini-executor执行。
EOF
```

---

## 问题5: 结果不符预期

### 症状

- Gemini返回的内容太简短
- 没有按要求的格式返回
- 遗漏了重要信息

### 解决方案

#### 优化Prompt结构

```bash
# ❌ 模糊的prompt
gemini -p "分析这个" file.png --yolo

# ✅ 结构化prompt
gemini -p "请分析这张图片，包括：
1. 图片主要内容
2. 布局和结构
3. 发现的问题
4. 改进建议

请用markdown格式输出。" file.png --yolo
```

#### 使用Heredoc处理复杂Prompt

```bash
gemini file.png --yolo << 'EOF'
你是一个UI/UX专家。请分析这张界面截图：

## 分析维度
1. 视觉设计（色彩、排版、间距）
2. 交互设计（按钮、表单、导航）
3. 用户体验（信息架构、操作流程）

## 输出要求
- 先给总体评分(1-10)
- 然后列出问题（按严重程度排序）
- 最后给出具体改进建议

## 格式
使用markdown，问题用表格呈现
EOF
```

---

## 问题6: 超出免费额度

### 症状

```
Error: Rate limit exceeded
Error: Quota exceeded
```

### 诊断

免费账户限制：
- 每分钟请求数
- 每天总请求数
- 每次请求的token数

### 解决

#### 短期

```bash
# 等待一分钟后重试
sleep 60
gemini -p "..." --yolo
```

#### 长期

1. 升级到付费账户
2. 申请更高配额
3. 优化请求，减少不必要调用

---

## 问题7: 大文件处理失败

### 症状

```
Error: File too large
Error: Request timeout
```

### 解决

#### 视频文件

```bash
# 压缩视频
ffmpeg -i large.mp4 -vf scale=720:-1 -c:a copy smaller.mp4

# 截取片段
ffmpeg -i large.mp4 -ss 00:00:00 -t 00:02:00 -c copy clip.mp4
```

#### PDF文件

```bash
# 提取特定页面
pdftk large.pdf cat 1-20 output first20pages.pdf

# 压缩PDF
gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook \
   -dNOPAUSE -dQUIET -dBATCH -sOutputFile=compressed.pdf large.pdf
```

---

## 问题8: Subagent 执行失败

### 症状

- Skill触发了但命令没执行
- 返回空结果

### 诊断

```bash
# 检查Subagent文件
ls ~/.claude/agents/gemini-executor.md

# 手动测试命令
gemini -p "test" --yolo
```

### 常见原因

1. **gemini不在PATH中**
   ```bash
   which gemini  # 应该返回路径
   ```

2. **Subagent文件格式错误**
   ```bash
   cat ~/.claude/agents/gemini-executor.md
   # 检查frontmatter格式
   ```

3. **权限问题**
   ```bash
   ls -la $(which gemini)  # 检查执行权限
   ```

---

## 调试技巧

### 启用详细输出

```bash
# 查看完整错误信息
gemini -p "test" --yolo --verbose 2>&1
```

### 检查环境

```bash
# 全面检查
echo "Node版本: $(node --version)"
echo "Gemini位置: $(which gemini)"
echo "API Key设置: $([ -n "$GEMINI_API_KEY" ] && echo '是' || echo '否')"
echo "Skills目录: $(ls ~/.claude/skills/ 2>/dev/null || echo '不存在')"
echo "Agents目录: $(ls ~/.claude/agents/ 2>/dev/null || echo '不存在')"
```

### 最小化测试

```bash
# 最简单的测试
gemini -p "say hello" --yolo

# 如果这个失败，问题在CLI本身
# 如果这个成功，问题在集成配置
```

---

## 获取帮助

如果以上都不能解决：

1. **Gemini CLI Issues**: https://github.com/google-gemini/gemini-cli/issues
2. **Claude Code 文档**: 查看官方Skills文档
3. **检查更新**: `npm update -g @google/gemini-cli`
