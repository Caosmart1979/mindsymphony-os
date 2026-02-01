---
name: evernote
type: integration
external_path: /mnt/skills/user/evernote-integration
priority: medium
triggers:
  zh: [印象笔记, evernote, 笔记查询, 笔记搜索, 笔记同步, evernote会员]
  en: [evernote, note query, note search, evernote sync]
security_level: external_api
requires:
  - evernote3_sdk
  - oauth2_authentication
  - developer_token
---

# 印象笔记 (Evernote) 集成 快捷入口

> 连接印象笔记，让 Claude Code 可以查询你的笔记库。
> 基于你的私有笔记回答问题，无缝对接现有知识管理。

---

## 核心价值

```
传统方式：
Claude 无法访问你的笔记 → 需要手动复制粘贴 → 信息碎片化

印象笔记方式：
Claude → 查询印象笔记 → 基于你的笔记回答 → 整合知识库
```

### 适用场景

| 场景 | 说明 |
|------|------|
| **笔记查询** | 直接提问，搜索笔记内容 |
| **知识整合** | 将多篇笔记整合成结构化内容 |
| **笔记管理** | 创建、更新、搜索笔记 |
| **内容创作** | 基于已有笔记生成新内容 |

---

## 能力边界

### ✅ 可以做

| 功能 | 说明 |
|------|------|
| 搜索笔记 | 按关键词、标签、笔记本搜索 |
| 读取笔记 | 获取笔记标题、内容、标签 |
| 创建笔记 | 从对话内容创建新笔记 |
| 更新笔记 | 修改现有笔记内容 |
| 列出笔记本 | 浏览所有笔记本和笔记栈 |

### ❌ 不能做

| 限制 | 原因 |
|------|------|
| **批量删除** | 需要手动确认重要操作 |
| **附件下载** | API 限制，需额外处理 |
| **笔记历史** | 需要高级 API 权限 |

---

## 触发词

### 中文
- 印象笔记、查询我的笔记
- 搜索笔记、笔记同步
- 创建笔记、保存到印象笔记

### English
- evernote, query my notes
- search notes, note sync
- create note, save to evernote

---

## 命令前缀

```
/evernote [你的操作]
```

---

## 使用流程

### 首次设置

```
Step 1: 获取开发者令牌
────────────────────────
1. 登录印象笔记
2. 访问：https://app.yinxiang.com/api/DeveloperToken.action
3. 复制你的开发者令牌

Step 2: 安装 Python SDK
────────────────────────
pip install evernote3

Step 3: 配置认证
────────────────────────
在 Claude Code 中：
> Configure Evernote authentication

输入开发者令牌，系统会保存配置。
```

### 日常使用

```
搜索笔记：
> Search my Evernote: 机器学习

列出笔记本：
> List my Evernote notebooks

创建笔记：
> Save to Evernote: 今天的会议要点...

读取笔记内容：
> Get Evernote note: [笔记标题]
```

---

## 工作流集成

### Gemini + Evernote + Claude 三剑客

```
┌─────────────────────────────────────────────────────────────┐
│  Step 1: Evernote 存储知识                                   │
│  ──────────────────                                         │
│  - 收集文章、会议记录、项目资料                               │
│  - 用标签组织：#项目 #研究 #待办                             │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│  Step 2: Claude 查询整合                                     │
│  ──────────────────                                         │
│  > Search Evernote: AI创业相关笔记                           │
│  > 整合这些笔记，生成学习路线                                 │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│  Step 3: Gemini 多模态处理                                   │
│  ──────────────────                                         │
│  > 用 Gemini 分析相关视频/图片                               │
│  > 将分析结果保存回 Evernote                                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 与 NotebookLM 协同

```yaml
# 互补使用策略
evernote:
  适用: 私人笔记、日常记录、快速收集
  优势: 会员功能强大、多端同步

notebooklm:
  适用: 深度研究、文档问答、来源验证
  优势: AI 增强搜索、基于来源的回答

pheromones:
  - on_event: "knowledge.collection"
    to: "evernote"  # 快速收集

  - on_event: "deep.research"
    to: "notebooklm"  # 深度分析
```

---

## 技术细节

### 依赖项

```python
# requirements.txt
evernote3>=1.0.0  # 印象笔记 Python SDK
oauthlib>=3.0.0   # OAuth 认证支持
```

### API 配置

```python
# config.py
EVERNOTE_CONFIG = {
    # 中国区服务器
    "china": {
        "host": "app.yinxiang.com",
        "api_url": "https://app.yinxiang.com/shard/s1/notestore"
    },
    # 国际区服务器
    "international": {
        "host": "www.evernote.com",
        "api_url": "https://www.evernote.com/edam/note/"
    },
    # 认证
    "developer_token": "YOUR_TOKEN_HERE",
    "note_store_url": "自动获取"
}
```

### 数据存储

```
~/.claude/skills/evernote-integration/data/
├── config.json       # API 配置
├── auth_info.json    # 认证信息（敏感）
├── cache/            # 笔记缓存
└── logs/             # API 日志
```

---

## API 限制

| 限制 | 免费版 | 会员版 |
|------|--------|--------|
| 每月上传 | 60MB | 10GB |
| 笔记数量 | 10万 | 无限 |
| 每月 API 调用 | 5000 | 100万 |
| 搜索速度 | 基础 | 高级 |

**会员优势**：你已有的会员可以充分利用高级 API 功能！

---

## 命令参考

### 笔记搜索

```python
# 按关键词搜索
search_notes(query="机器学习")

# 按标签搜索
search_notes(tag="项目A")

# 按笔记本搜索
search_notes(notebook="工作")

# 组合搜索
search_notes(query="AI", tag="重要", notebook="研究")
```

### 笔记操作

```python
# 创建笔记
create_note(
    title="会议纪要",
    content="会议内容...",
    notebook="工作",
    tags=["会议", "重要"]
)

# 更新笔记
update_note(
    note_guid="xxx",
    content="更新后的内容..."
)

# 删除笔记
delete_note(note_guid="xxx")
```

### 笔记本管理

```python
# 列出所有笔记本
list_notebooks()

# 创建笔记本
create_notebook(name="新项目")

# 获取笔记本中的笔记
get_notes_in_notebook("工作")
```

---

## Python 集成示例

### 基础客户端

```python
from evernote.api.client import EvernoteClient

class EvernoteClientWrapper:
    def __init__(self, developer_token, china=True):
        self.client = EvernoteClient(
            token=developer_token,
            service_host="app.yinxiang.com" if china else "www.evernote.com"
        )
        self.note_store = self.client.get_note_store()

    def search_notes(self, query, notebook=None, tags=None):
        """搜索笔记"""
        filter = NoteFilter()
        filter.words = query
        if notebook:
            filter.notebookGuid = self._get_notebook_guid(notebook)

        result_spec = NotesMetadataResultSpec()
        result_spec.includeTitle = True
        result_spec.includeContent = True

        return self.note_store.findNotesMetadata(
            self.client.token, filter, 0, 100, result_spec
        )

    def create_note(self, title, content, notebook=None, tags=None):
        """创建笔记"""
        note = Note()
        note.title = title
        note.content = self._make_content(content)

        if notebook:
            note.notebookGuid = self._get_notebook_guid(notebook)
        if tags:
            note.tagNames = tags

        return self.note_store.createNote(self.client.token, note)
```

---

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| 认证失败 | 检查开发者令牌是否有效 |
| API 限流 | 等待或使用会员高级配额 |
| 搜索无结果 | 检查搜索语法和权限 |
| 内容乱码 | 确保使用正确的编码 (UTF-8) |

---

## 与现有集成对比

| 功能 | Evernote | NotebookLM | Gemini |
|------|----------|------------|--------|
| 笔记存储 | ✅ | ❌ | ❌ |
| 智能问答 | ❌ | ✅ | ❌ |
| 多模态 | ❌ | ❌ | ✅ |
| 来源验证 | ❌ | ✅ | ❌ |
| 快速记录 | ✅ | ❌ | ❌ |

**最佳实践**：三工具协同
1. Evernote：收集和存储
2. NotebookLM：深度研究和问答
3. Gemini：多模态分析

---

## 安全提醒

```yaml
security_considerations:
  - 开发者令牌等同密码，勿泄露
  - 笔记内容可能包含敏感信息
  - API 日志注意过滤敏感数据
  - 建议使用只读令牌用于查询
```

---

## 信心赋予

**"你的印象笔记会员，是 Claude Code 的私有知识库基石。"**

Evernote 集成让 MindSymphony：
- 访问你多年积累的知识资产
- 无缝对接现有笔记工作流
- 会员高级功能发挥最大价值

这是从"通用助手"升级为"个人知识助理"的关键一步。
