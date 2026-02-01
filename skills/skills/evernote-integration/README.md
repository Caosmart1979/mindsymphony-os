# 印象笔记 (Evernote) 集成 - 完整功能指南

> 让 Claude Code 可以访问你的印象笔记，实现智能笔记管理和知识检索。
> 支持 8 大功能模块，满足专业笔记管理需求。

---

## 功能概览

| 模块 | 功能 | 说明 |
|------|------|------|
| **标签管理** | 创建、删除、重命名、搜索标签 | 组织笔记的利器 |
| **笔记本管理** | 创建、删除、重命名笔记本 | 知识库结构化管理 |
| **高级搜索** | 多维度过滤、排序、组合查询 | 精准定位所需内容 |
| **批量操作** | 批量移动、打标签、删除 | 高效整理大量笔记 |
| **附件支持** | 上传、下载、导出附件 | 管理笔记中的资源 |
| **导入导出** | Markdown/HTML/JSON 互转 | 数据迁移与备份 |
| **笔记链接** | 生成内部/外部链接 | 快速跳转关联笔记 |
| **统计分析** | 笔记统计、活动分析 | 了解使用习惯 |

---

## 快速开始

### 第一步：获取开发者令牌

1. 登录印象笔记官网：https://app.yinxiang.com
2. 访问开发者令牌页面：https://app.yinxiang.com/api/DeveloperToken.action
3. 复制你的开发者令牌（类似：S=s1:U=...:E=...:C=...:P=...:A=...）

### 第二步：安装依赖

```bash
pip install evernote3 oauth2
```

### 第三步：配置认证

```bash
# 方式 1：使用命令行配置
cd D:\claudecode\skills\skills\evernote-integration
python cli.py config -t "你的开发者令牌"

# 方式 2：设置环境变量
export EVERNOTE_TOKEN="你的开发者令牌"  # Linux/Mac
set EVERNOTE_TOKEN=你的开发者令牌      # Windows
```

### 第四步：验证连接

```bash
python cli.py verify
```

如果成功，你会看到：
```
✓ 连接成功

用户信息:
  用户名: your_name
  邮箱: your_email@example.com

笔记本数量: 59
标签数量: 363
笔记总数: 6,026
```

---

## 命令参考

### 基础操作

#### 搜索笔记

```bash
# 基础搜索
python cli.py search "机器学习"

# 在特定笔记本中搜索
python cli.py search "项目" -n "工作"

# 按标签搜索
python cli.py search -t "重要,待办"

# 组合搜索
python cli.py search "会议" -n "工作" -t "重要" -l 20

# 搜索特定时间范围
python cli.py search "AI" --created-after "2024-01-01"

# 搜索包含待办的笔记
python cli.py search --has-todo

# 搜索包含附件的笔记
python cli.py search --has-attachment
```

#### 笔记操作

```bash
# 获取笔记详情
python cli.py get <GUID>

# 创建笔记
python cli.py create -t "会议纪要" -c "今天讨论了项目进度..."

# 从文件创建
python cli.py create -t "学习笔记" -f notes.md -n "学习" --tags "AI,机器学习"

# 从管道创建
echo "这是一条测试笔记" | python cli.py create -t "测试"

# 更新笔记
python cli.py update <GUID> -c "更新后的内容"

# 删除笔记
python cli.py delete <GUID>
```

#### 笔记本管理

```bash
# 列出所有笔记本
python cli.py list

# 创建笔记本
python cli.py notebooks create "新项目"

# 删除笔记本（需先清空笔记）
python cli.py notebooks delete "旧项目"

# 重命名笔记本
python cli.py notebooks rename "旧名称" "新名称"

# 获取笔记本中的笔记
python cli.py notebooks notes "工作"
```

---

## 高级功能

### 1. 标签管理

```bash
# 列出所有标签
python cli.py tags list

# 创建标签
python cli.py tags create "重要"

# 删除标签
python cli.py tags delete <TAG_GUID>

# 重命名标签
python cli.py tags rename <TAG_GUID> "新名称"

# 为笔记添加标签
python cli.py tags add <NOTE_GUID> --tags "重要,待办"

# 从笔记移除标签
python cli.py tags remove <NOTE_GUID> --tags "旧标签"

# 搜索包含特定标签的笔记
python cli.py search -t "标签名"

# 搜索无标签笔记
python cli.py search --untagged
```

### 2. 高级搜索

```bash
# 按更新时间排序
python cli.py search "AI" --order UPDATED --ascending

# 按创建时间排序（最新的在前）
python cli.py search "项目" --order CREATED

# 按标题排序
python cli.py search "会议" --order TITLE

# 搜索特定长度范围的笔记
python cli.py search --min-length 1000 --max-length 5000

# 搜索特定时间段创建的笔记
python cli.py search --created-after "2024-01-01" --created-before "2024-12-31"

# 搜索特定时间段更新的笔记
python cli.py search --updated-after "2024-06-01"

# 组合多个条件
python cli.py search "AI" -n "学习" -t "重要" --order CREATED --min-length 500
```

**搜索过滤器：**

| 选项 | 说明 |
|------|------|
| `--query` | 搜索关键词 |
| `--notebook, -n` | 笔记本名称 |
| `--tags, -t` | 标签列表（逗号分隔） |
| `--limit, -l` | 结果数量限制 |
| `--offset` | 跳过结果数量（分页） |
| `--order` | 排序方式：CREATED, UPDATED, TITLE, RELEVANCE |
| `--ascending` | 升序排列（默认降序） |
| `--content-search` | 搜索内容（默认true） |
| `--has-todo` | 只搜索包含待办的笔记 |
| `--has-attachment` | 只搜索包含附件的笔记 |
| `--has-reminder` | 只搜索有提醒的笔记 |
| `--min-length` | 最小内容长度 |
| `--max-length` | 最大内容长度 |
| `--created-after` | 创建时间起点 |
| `--created-before` | 创建时间终点 |
| `--updated-after` | 更新时间起点 |
| `--updated-before` | 更新时间终点 |
| `--untagged` | 只搜索无标签笔记 |

### 3. 批量操作

```bash
# 批量移动笔记到另一个笔记本
python cli.py batch move --source "待整理" --target "工作"

# 批量添加标签（基于搜索结果）
python cli.py batch tag --query "AI" --add "精选"

# 批量移除标签
python cli.py batch tag --query "旧项目" --remove "待办"

# 批量删除（谨慎使用！）
python cli.py batch delete --notebook "临时笔记"

# 批量导出
python cli.py batch export --notebook "重要资料" --output ./backup/ --format md
```

**批量操作选项：**

| 命令 | 说明 | 警告 |
|------|------|------|
| `batch move` | 移动整个笔记本的笔记 | 确认目标笔记本存在 |
| `batch tag --add` | 为搜索结果添加标签 | 搜索条件要准确 |
| `batch tag --remove` | 从搜索结果移除标签 | 会影响所有匹配笔记 |
| `batch delete` | 删除整个笔记本的笔记 | ⚠️ 不可恢复！ |
| `batch export` | 导出整个笔记本 | 确保输出目录存在 |

### 4. 附件支持

```bash
# 列出笔记的附件
python cli.py attachments list <NOTE_GUID>

# 下载附件
python cli.py attachments download <NOTE_GUID> --output ./downloads/

# 导出笔记中的所有图片
python cli.py attachments export <NOTE_GUID> --type image --output ./images/

# 获取附件信息
python cli.py attachments info <ATTACHMENT_GUID>
```

### 5. 导入导出

```bash
# 导出单条笔记为 Markdown
python cli.py export note <GUID> --format md -o note.md

# 导出单条笔记为 HTML
python cli.py export note <GUID> --format html -o note.html

# 导出单条笔记为 JSON
python cli.py export note <GUID> --format json -o note.json

# 导出整个笔记本
python cli.py export notebook "AI知识库" --output ./backup/

# 导出时包含附件
python cli.py export note <GUID> --format md --include-attachments

# 从 Markdown 文件导入
python cli.py import note -f notes.md -t "导入的笔记" -n "学习"

# 从 JSON 文件导入
python cli.py import note -f backup.json --format json
```

**导出格式支持：**

| 格式 | 扩展名 | 说明 |
|------|--------|------|
| Markdown | .md | 纯文本，适合版本控制 |
| HTML | .html | 保留格式，适合浏览器查看 |
| JSON | .json | 完整数据，适合备份和迁移 |

### 6. 笔记链接

```bash
# 生成应用内链接
python cli.py link app <GUID>

# 生成网页链接
python cli.py link web <GUID>

# 复制链接到剪贴板（需要 pyperclip）
python cli.py link app <GUID> --copy

# 获取笔记的所有链接
python cli.py links list <GUID>
```

**链接类型：**

- **应用链接**：`evernote:///view/xxxx/xxxx/xxxx/` - 在印象笔记客户端中打开
- **网页链接**：`https://app.yinxiang.com/shard/xxxx/notebook/xxxx/note/xxxx/` - 在浏览器中打开

### 7. 统计分析

```bash
# 总览统计
python cli.py stats overview

# 活动分析（最近N天）
python cli.py stats activity --days 30

# 笔记本统计
python cli.py stats notebooks

# 标签统计
python cli.py stats tags

# 搜索趋势
python cli.py stats trends --months 12
```

**统计信息包含：**

```bash
$ python cli.py stats overview

╔═══════════════════════════════════════════════════════════════╗
║                    印象笔记统计总览                            ║
╚═══════════════════════════════════════════════════════════════╝

📊 笔记统计
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  总笔记数:        6,026
  平均笔记长度:    1,234 字符
  最长笔记:        "XXX" (50,000 字符)
  最短笔记:        "YYY" (10 字符)

📁 笔记本统计
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  笔记本数量:      59
  最大笔记本:      "工作" (125,000 笔记)
  最活跃笔记本:    "学习" (最近7天新增 123 笔记)

🏷️  标签统计
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  标签数量:        363
  最常用标签:      #重要 (45,000 使用)
  平均每笔记标签:  2.3 个

📅 活动统计
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  今日创建:        45 笔记
  本周创建:        312 笔记
  本月创建:        1,234 笔记
  平均每日创建:    41 笔记
```

---

## 与 Claude Code 集成

### 基础用法

```
你：搜索我的印象笔记中关于 AI 的内容

Claude Code：
[调用 evernote skill]
找到 5 条相关笔记：
1. AI 学习路线
   内容：...
2. AI 项目实践
   内容：...
```

```
你：把这段内容保存到印象笔记

Claude Code：
[调用 evernote create]
✓ 笔记已创建到 "工作" 笔记本
```

### 高级用法

```
你：找出我所有无标签的笔记，为其中关于"项目"的添加"待整理"标签

Claude Code：
[调用 evernote search --untagged]
[过滤包含"项目"的笔记]
[调用 batch tag --add "待整理"]
✓ 已为 45 条笔记添加"待整理"标签
```

```
你：统计我的笔记使用情况

Claude Code：
[调用 stats overview]
根据统计：
- 你有 59 个笔记本，363 个标签
- 最多使用的标签是"重要"
- 本周新增 312 条笔记
- 最活跃的笔记本是"学习"
```

---

## 工作流集成

### 工作流 1：Gemini 分析 → Evernote 保存

```bash
# 1. 用 Gemini 分析视频
gemini -p "总结视频要点" demo.mp4 --yolo > summary.txt

# 2. 保存到印象笔记
python cli.py create -t "Demo 视频总结" -f summary.txt -n "项目资料"
```

### 工作流 2：Evernote 查询 → NotebookLM 深度研究

```bash
# 1. 先在印象笔记中快速查找
python cli.py search "创业"

# 2. 将相关资料导出
python cli.py export notebook "创业资料" --output ./notebooklm/

# 3. 上传到 NotebookLM 深度分析
# （在 NotebookLM 网页手动上传）
```

### 工作流 3：定期备份

```bash
#!/bin/bash
# backup_evernote.sh

DATE=$(date +%Y%m%d)
BACKUP_DIR="./backups/$DATE"

# 创建备份目录
mkdir -p "$BACKUP_DIR"

# 导出所有笔记本
python cli.py export notebook "工作" --output "$BACKUP_DIR/"
python cli.py export notebook "学习" --output "$BACKUP_DIR/"
python cli.py export notebook "生活" --output "$BACKUP_DIR/"

# 导出统计信息
python cli.py stats overview > "$BACKUP_DIR/stats.txt"

echo "备份完成: $BACKUP_DIR"
```

### 工作流 4：标签整理

```bash
#!/bin/bash
# organize_tags.sh

# 1. 找出无标签笔记
python cli.py search --untagged --output ./untagged_notes.txt

# 2. 找出使用频率低的标签
python cli.py stats tags --min-usage 10 --output ./rare_tags.txt

# 3. 批量整理
python cli.py batch tag --query "临时" --remove "临时" --add "待整理"
```

---

## Python API

### 基础用法

```python
from evernote_client import create_client

# 创建客户端
client = create_client(developer_token="your_token", china=True)

# 基础搜索
notes = client.search_notes("AI", notebook="学习", tags=["重要"])

# 创建笔记
client.create_note(
    title="新笔记",
    content="笔记内容",
    notebook="工作",
    tags=["待办"]
)

# 获取笔记详情
note = client.get_note(note_guid)
print(note['content'])
```

### 高级搜索

```python
# 高级搜索
results = client.search_notes_advanced(
    query="机器学习",
    notebook="学习",
    tags=["重要"],
    order="CREATED",
    ascending=True,
    has_attachment=True,
    min_length=1000,
    created_after="2024-01-01"
)

# 处理搜索结果
for note in results:
    print(f"{note['title']} - {note['updated']}")
```

### 标签管理

```python
# 列出所有标签
tags = client.list_tags()

# 创建标签
client.create_tag("新标签")

# 重命名标签
client.rename_tag(tag_guid, "新名称")

# 删除标签
client.delete_tag(tag_guid)
```

### 笔记本管理

```python
# 列出所有笔记本
notebooks = client.list_notebooks()

# 创建笔记本
client.create_notebook("新项目")

# 重命名笔记本
client.rename_notebook("旧名称", "新名称")

# 删除笔记本
client.delete_notebook("旧项目")
```

### 批量操作

```python
# 批量移动笔记
client.batch_move_notes(
    source_notebook="待整理",
    target_notebook="工作"
)

# 批量添加标签
client.batch_tag_notes(
    query="AI",
    tags_to_add=["精选"]
)

# 批量导出
client.batch_export_notebook(
    notebook="重要资料",
    output_dir="./backup/",
    format="md"
)
```

### 导入导出

```python
# 导出笔记
client.export_note(
    note_guid=guid,
    output_file="note.md",
    format="markdown",
    include_attachments=True
)

# 导出笔记本
client.export_notebook(
    notebook="AI知识库",
    output_dir="./backup/",
    format="markdown"
)

# 导入笔记
client.import_note(
    file="note.md",
    title="导入的笔记",
    notebook="学习",
    tags=["导入"]
)
```

### 统计分析

```python
# 获取统计信息
stats = client.get_statistics()

print(f"总笔记数: {stats['total_notes']}")
print(f"笔记本数: {stats['notebook_count']}")
print(f"标签数: {stats['tag_count']}")

# 活动分析
activity = client.get_activity_analysis(days=30)

print(f"最近30天创建: {activity['created_count']}")
print(f"最近30天更新: {activity['updated_count']}")
```

---

## 配置文件位置

```
~/.claude/skills/evernote-integration/data/
├── config.json       # API 配置
├── auth_info.json    # 认证信息（敏感）
└── cache/            # 笔记缓存
```

---

## API 限制参考

| 功能 | 免费版 | 会员版 |
|------|--------|--------|
| 每月上传 | 60MB | 10GB |
| 笔记数量 | 10万 | 无限 |
| 每月 API 调用 | 5000 | 100万 |
| 同步设备 | 2台 | 无限 |
| 搜索速度 | 基础 | 高级 |

**会员优势**：你已有的会员可以充分利用高级 API 配额！

---

## 故障排除

### 问题：ModuleNotFoundError: No module named 'evernote'

**解决方案**：
```bash
pip install evernote3 oauth2
```

### 问题：认证失败 (EDAMErrorCode.INVALID_AUTH)

**解决方案**：
1. 检查开发者令牌是否正确
2. 确认使用的是正确的服务器（中国区 vs 国际区）
3. 重新获取令牌

### 问题：搜索无结果

**解决方案**：
1. 使用 `python cli.py list` 确认笔记本存在
2. 检查搜索关键词是否正确
3. 尝试不带关键词搜索：`python cli.py search`

### 问题：连接超时

**解决方案**：
1. 检查网络连接
2. 确认可以访问 app.yinxiang.com
3. 如果使用代理，需要配置系统代理

### 问题：批量操作中断

**解决方案**：
1. 使用 `--limit` 参数分批处理
2. 检查 API 调用频率限制
3. 增加重试间隔时间

---

## 安全提醒

1. **开发者令牌等同于密码**，请妥善保管
2. **不要提交到版本控制系统**（已加入 .gitignore）
3. **建议使用只读令牌**用于查询场景
4. **敏感笔记内容**注意脱敏
5. **批量删除操作**务必先确认
6. **定期备份**重要笔记

---

## 技术支持

- 印象笔记 API 文档：https://dev.yinxiang.com/
- Python SDK 文档：https://github.com/evernote/evernote-sdk-python
- 问题反馈：在项目中提 Issue

---

## 更新日志

### v2.0.0 (2025-01-16)
- ✅ 新增标签管理功能
- ✅ 新增笔记本管理功能
- ✅ 新增高级搜索功能
- ✅ 新增批量操作功能
- ✅ 新增附件支持功能
- ✅ 新增导入导出功能
- ✅ 新增笔记链接功能
- ✅ 新增统计分析功能
- ✅ 支持中国区和国际区
- ✅ Python 3.14 兼容性修复

### v1.0.0 (2025-01-16)
- ✅ 初始版本
- ✅ 支持搜索、创建、更新、删除笔记
- ✅ 基础笔记本管理
- ✅ 命令行工具
- ✅ Claude Code 集成
