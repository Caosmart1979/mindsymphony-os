# Gemini CLI 安装配置指南

从零开始配置Claude Code与Gemini CLI的集成。

---

## 前置要求

| 要求 | 说明 |
|------|------|
| Node.js | 18.0+ |
| Claude Code | 已安装并正常使用 |
| Google账号 | 用于Gemini API（免费） |

---

## Step 1: 安装 Gemini CLI

### 方法A: 全局安装（推荐）

```bash
npm install -g @google/gemini-cli
```

验证安装：
```bash
gemini --version
```

### 方法B: 使用npx（无需安装）

```bash
npx @google/gemini-cli -p "hello" --yolo
```

### 方法C: 从源码安装

```bash
git clone https://github.com/google-gemini/gemini-cli.git
cd gemini-cli
npm install
npm link
```

---

## Step 2: 配置 API Key

### 方法A: 环境变量（推荐用于自动化）

```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
export GEMINI_API_KEY="your-api-key-here"

# 立即生效
source ~/.bashrc
```

获取API Key：
1. 访问 https://aistudio.google.com/
2. 登录Google账号
3. 创建API Key
4. 复制Key

### 方法B: 交互式登录

```bash
# 首次运行，按提示登录
gemini

# 会打开浏览器进行Google OAuth授权
```

### 验证配置

```bash
gemini -p "说你好" --yolo
```

应该返回一个正常的问候响应。

---

## Step 3: 部署 Skill

### 3.1 创建Skills目录（如果不存在）

```bash
mkdir -p ~/.claude/skills/gemini-cli
```

### 3.2 创建Skill文件

创建 `~/.claude/skills/gemini-cli/SKILL.md`：

```markdown
---
name: gemini-cli
description: 当用户提到"用Gemini分析"、"Gemini帮我看"、"让Gemini处理"等时触发。
---

# Gemini CLI 助手

## 触发场景

- "用Gemini分析这个文件"
- "Gemini帮我看看这张图"
- "让Gemini总结这个视频"
- "用Gemini扫描项目架构"
- "Gemini处理这段录音"

## 工作流程

1. 识别用户意图和目标文件
2. 调用 gemini-executor 子代理执行
3. 将结果摘要返回给用户

## 注意事项

- 确保文件路径正确
- 大文件处理可能需要较长时间
- 敏感信息不要发送给Gemini
```

---

## Step 4: 部署 Subagent

### 4.1 创建Agents目录（如果不存在）

```bash
mkdir -p ~/.claude/agents
```

### 4.2 复制Subagent定义

将 `agents/gemini-executor.md` 复制到：

```bash
cp agents/gemini-executor.md ~/.claude/agents/
```

或手动创建 `~/.claude/agents/gemini-executor.md`（内容见本skill的agents目录）

---

## Step 5: 验证集成

### 测试1: 直接CLI调用

```bash
# 测试文本
gemini -p "用一句话介绍你自己" --yolo

# 测试图片（准备一张测试图片）
gemini -p "描述这张图片" test.png --yolo
```

### 测试2: Claude Code中触发

启动Claude Code，输入：

```
用Gemini帮我分析当前目录的结构
```

如果配置正确，Claude Code应该：
1. 识别到Gemini触发词
2. 调用gemini-executor
3. 返回分析结果

---

## 目录结构总结

```
~/.claude/
├── skills/
│   └── gemini-cli/
│       └── SKILL.md          # Skill定义
└── agents/
    └── gemini-executor.md    # Subagent定义

~/.bashrc (或 ~/.zshrc)
└── export GEMINI_API_KEY="..." # API Key配置
```

---

## 常见安装问题

### 问题1: npm安装失败

```bash
# 尝试使用sudo
sudo npm install -g @google/gemini-cli

# 或修复npm权限
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

### 问题2: API Key无效

```
错误: Invalid API key

排查:
1. 确认Key是否完整复制（无空格）
2. 确认环境变量已生效: echo $GEMINI_API_KEY
3. 尝试重新生成Key
```

### 问题3: Claude Code不触发Skill

```
可能原因:
1. SKILL.md路径不对
2. frontmatter格式错误
3. 触发词不匹配

排查:
1. 确认文件在 ~/.claude/skills/gemini-cli/SKILL.md
2. 检查YAML frontmatter格式
3. 使用明确的触发语如"用Gemini..."
```

### 问题4: Subagent执行失败

```
可能原因:
1. gemini命令不在PATH中
2. 忘记加--yolo
3. 文件路径错误

排查:
1. which gemini 确认命令存在
2. 检查命令是否包含--yolo
3. 使用绝对路径
```

---

## 升级与卸载

### 升级Gemini CLI

```bash
npm update -g @google/gemini-cli
```

### 卸载

```bash
# 卸载CLI
npm uninstall -g @google/gemini-cli

# 移除Skill和Subagent
rm -rf ~/.claude/skills/gemini-cli
rm ~/.claude/agents/gemini-executor.md

# 移除环境变量（编辑~/.bashrc删除相关行）
```

---

## 下一步

配置完成后，查看：
- `references/use-cases.md` - 了解各种使用场景
- `examples/` - 查看具体示例
