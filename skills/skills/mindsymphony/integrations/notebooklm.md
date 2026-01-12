---
name: notebooklm
type: integration
external_path: /mnt/skills/user/notebooklm-skill
priority: medium
triggers:
  zh: [NotebookLM, 知识库, 文档查询, 笔记本, 研究资料, 查阅文档]
  en: [NotebookLM, knowledge base, document query, notebook, research docs]
security_level: external_system
requires:
  - playwright_or_patchright
  - google_authentication
  - browser_visible_for_setup
---

# NotebookLM 知识检索 快捷入口

> 连接Google NotebookLM，让Claude Code可以查询你的私有知识库。
> 基于来源的可靠回答，大幅减少幻觉。

---

## 核心价值

```
传统方式：
Claude直接回答 → 可能幻觉 → 无法验证来源

NotebookLM方式：
Claude → 查询NotebookLM → 基于你上传的文档回答 → 每句话都有来源
```

### 适用场景

| 场景 | 说明 |
|------|------|
| **专业领域学习** | 上传顶尖专家的文章，构建可对话的知识库 |
| **项目文档查询** | 上传项目文档，直接提问 |
| **研究资料整合** | 多个来源的资料，统一查询 |
| **内容创作辅助** | 基于可靠来源写作，减少事实错误 |

---

## 能力边界

### ✅ 可以做

| 功能 | 说明 |
|------|------|
| 查询已有Notebook | 向NotebookLM提问，获取基于文档的回答 |
| 管理Notebook库 | 添加、删除、激活、搜索本地Notebook索引 |
| 多轮追问 | 连续提问，深入挖掘文档内容 |
| 本地缓存 | 记住你的Notebook列表和认证状态 |

### ❌ 不能做

| 限制 | 原因 |
|------|------|
| **自动上传文件** | 需要手动在NotebookLM网页上传 |
| **创建新Notebook** | 需要手动在网页创建 |
| **生成播客/视频** | NotebookLM Studio功能，需手动 |
| **在Claude.ai使用** | 需要本地Python环境+浏览器 |

---

## 触发词

### 中文
- NotebookLM、知识库查询
- 查阅我的文档、问我的笔记本
- 基于文档回答

### English
- NotebookLM, query my docs
- check my notebook, research my documents
- source-grounded answer

---

## 命令前缀

```
/notebook [你的问题]
```

---

## 使用流程

### 首次设置（一次性）

```
Step 1: 认证
─────────────────
在Claude Code中输入：
> Set up NotebookLM authentication

系统会打开浏览器，你需要手动登录Google账号。
登录后认证信息会保存，后续不需要重复登录。

Step 2: 准备知识库（手动）
─────────────────
1. 打开 notebooklm.google.com
2. 创建新Notebook
3. 上传你的资料（PDF、网页链接、YouTube、文本等）
4. 复制Notebook的URL

Step 3: 添加到索引
─────────────────
在Claude Code中：
> Add this NotebookLM: https://notebooklm.google.com/notebook/xxx

系统会自动查询Notebook内容，提取主题，添加到本地索引。
```

### 日常使用

```
直接提问：
> Ask my NotebookLM: 这些AI创业者如何管理精力？

或者指定Notebook：
> Query notebook "seo-guide": 什么是长尾关键词？

列出所有Notebook：
> List my notebooks
```

---

## 工作流集成

### Gemini + NotebookLM 学习神器

这是PDF中描述的高效学习方法：

```
┌─────────────────────────────────────────────────────────────┐
│  Step 1: Gemini找内容                                        │
│  ──────────────────                                         │
│  提示词：                                                    │
│  "帮我找20篇讲[主题]的文章，                                   │
│   要求：作者是领域顶尖专家，                                    │
│   内容来自blog/YouTube/Twitter，                              │
│   提供原始链接，用表格呈现"                                    │
│                                                             │
│  输出：高质量内容清单                                          │
├─────────────────────────────────────────────────────────────┤
│  Step 2: 人工校验 + 建知识库（手动）                           │
│  ──────────────────                                         │
│  1. 点开链接验证有效性                                        │
│  2. 在NotebookLM创建笔记本                                   │
│  3. 把有效链接丢进去                                         │
│                                                             │
│  输出：一个顶尖主题知识库                                      │
├─────────────────────────────────────────────────────────────┤
│  Step 3: 向知识库提问（本Skill自动化）                         │
│  ──────────────────                                         │
│  > Ask my NotebookLM: 总结这些专家的核心方法                   │
│  > Ask my NotebookLM: 他们在[具体问题]上有什么共识？             │
│                                                             │
│  输出：基于可靠来源的、可验证的结论                             │
└─────────────────────────────────────────────────────────────┘
```

### 与MindSymphony协同

```yaml
# 信息素配置示例
pheromones:
  - on_event: "research.need_verification"
    from_unit: "Scholar-Unit"
    action:
      trigger_unit: "NotebookLM-Query"
      with_task: "Verify these findings against uploaded documents"
      
  - on_event: "notebooklm.query_completed"
    from_unit: "External-Gateway-Unit"
    action:
      trigger_unit: "Creator-Unit"
      with_task: "Synthesize the source-grounded answer with research"
```

---

## 技术细节

### 依赖项

```
- Python 3.10+
- patchright (Playwright变体，反检测)
- Google账号认证
- 可见浏览器窗口（仅首次认证）
```

### 数据存储

```
~/.claude/skills/notebooklm-skill/data/
├── library.json      # Notebook索引
├── auth_info.json    # 认证状态
└── browser_state/    # 浏览器Cookie（敏感）
```

### 限制

| 限制 | 值 | 说明 |
|------|-----|------|
| 每日查询 | ~50次 | Google免费账号限制 |
| 每次延迟 | 5-15秒 | 浏览器启动+页面加载 |
| 并发查询 | 1 | 单浏览器实例 |

---

## 命令参考

### 认证管理

```bash
# 检查认证状态
python scripts/run.py auth_manager.py status

# 首次认证（需要浏览器可见）
python scripts/run.py auth_manager.py setup

# 重新认证
python scripts/run.py auth_manager.py reauth

# 清除认证
python scripts/run.py auth_manager.py clear
```

### Notebook管理

```bash
# 列出所有Notebook
python scripts/run.py notebook_manager.py list

# 添加Notebook（推荐：先查询内容）
python scripts/run.py ask_question.py \
  --question "What is the content of this notebook?" \
  --notebook-url "https://notebooklm.google.com/notebook/xxx"

# 然后添加
python scripts/run.py notebook_manager.py add \
  --url "https://notebooklm.google.com/notebook/xxx" \
  --name "SEO学习指南" \
  --description "Ahrefs等顶级SEO资源汇编" \
  --topics "SEO,关键词,链接建设,页面优化"

# 激活某个Notebook
python scripts/run.py notebook_manager.py activate --id seo-学习指南

# 搜索Notebook
python scripts/run.py notebook_manager.py search --query "SEO"

# 删除Notebook
python scripts/run.py notebook_manager.py remove --id notebook-id
```

### 查询

```bash
# 基本查询（使用当前激活的Notebook）
python scripts/run.py ask_question.py --question "你的问题"

# 指定Notebook ID
python scripts/run.py ask_question.py \
  --question "你的问题" \
  --notebook-id seo-学习指南

# 直接使用URL
python scripts/run.py ask_question.py \
  --question "你的问题" \
  --notebook-url "https://notebooklm.google.com/notebook/xxx"

# 显示浏览器（调试用）
python scripts/run.py ask_question.py \
  --question "你的问题" \
  --show-browser
```

---

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| ModuleNotFoundError | 必须使用 `python scripts/run.py [script]` |
| 认证失败 | 确保浏览器可见，手动完成Google登录 |
| Rate limit | 等待或换Google账号 |
| 找不到Notebook | 用 `notebook_manager.py list` 检查 |
| 浏览器崩溃 | `python scripts/run.py cleanup_manager.py --preserve-library` |

---

## 详细文档

完整文档位置：`/mnt/skills/user/notebooklm-skill/SKILL.md`

参考资料：
- `references/api_reference.md` - API详细说明
- `references/troubleshooting.md` - 故障排除指南
- `references/usage_patterns.md` - 使用模式最佳实践

---

## 安全提醒

```yaml
security_considerations:
  - 浏览器状态包含Google登录Cookie，勿泄露
  - 查询内容可能包含敏感信息，注意日志
  - 建议使用专用Google账号，而非主账号
```

---

## 信心赋予

**"基于来源的回答，是减少AI幻觉的最有效方式。"**

NotebookLM集成让MindSymphony：
- 可以查询你精心策划的知识库
- 每个回答都有文档来源支撑
- 从"可能正确"升级为"可验证正确"

这是从"智能助手"升级为"可靠研究伙伴"的关键一步。
