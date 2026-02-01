# Skill Hub

> Claude Skills 市场发现与管理中枢

搜索、评估、下载和管理来自多个来源的 Claude Skills。

## 特性

- **多源聚合搜索** - 并发搜索 skillslm、42plugin、GitHub 和本地 skills
- **智能预评估** - 不下载即可评估质量、重复度和安全性
- **决策建议** - 自动建议直接使用、改造适配、增强吸收或跳过
- **MindSymphony 集成** - 自动适配并注册到 MindSymphony 生态系统

## 安装

```bash
# 克隆或下载 Skill_Hub 目录
cd Skill_Hub

# 安装依赖
pip install -r requirements.txt

# 初始化配置
python cli.py init
```

## 使用

### 搜索技能

```bash
# 搜索所有市场
python cli.py search <关键词>

# 搜索特定来源
python cli.py search latex --source github

# 搜索并预评估
python cli.py search writer --evaluate
```

### 预评估技能

```bash
# 评估但不下载
python cli.py evaluate <skill-name>

# 查看详细报告
python cli.py evaluate latex-assistant --from skillslm
```

### 获取并安装

```bash
# 自动选择最佳来源
python cli.py fetch <skill-name>

# 指定来源
python cli.py fetch latex-assistant --source skillslm

# 指定目标目录
python cli.py fetch latex-assistant --dest ~/.claude/skills/
```

### 管理已安装技能

```bash
# 列出所有已安装
python cli.py list

# 查看统计信息
python cli.py stats

# 清理旧缓存
python cli.py cleanup --days 7
```

## 配置

编辑 `skill-hub.config.yml`:

```yaml
sources:
  skillslm:
    enabled: true
    priority: 1
    auto_update: true

  local:
    enabled: true
    path: ~/.claude/skills
    scan_on_startup: true

  fortytwoplugin:
    enabled: true
    api_key: ${FORTY_TWO_PLUGIN_KEY}

  github:
    enabled: true

evaluation:
  overlap_threshold: 0.8
  quality_threshold: 0.6
  auto_adapt: true

integration:
  mindsymphony:
    path: ~/.claude/skills
    router_path: mindsymphony/router/intent-router.md
    auto_register: true

security:
  scan_on_install: true
  allow_unknown_sources: false
  max_dependency_count: 20
```

## 项目结构

```
Skill_Hub/
├── cli.py              # 命令行入口
├── models.py           # 数据模型
├── config.py           # 配置管理
├── database.py         # SQLite 数据库
├── evaluation.py       # 评估引擎
├── sources/            # 数据源适配器
│   ├── __init__.py
│   ├── base.py
│   ├── skillslm.py
│   ├── local.py
│   ├── fortytwoplugin.py
│   └── github.py
├── requirements.txt
└── README.md
```

## 预评估说明

Skill Hub 的预评估会在不下载完整 skill 的情况下，基于远程元数据进行评估：

### 评估维度

| 维度 | 权重 | 说明 |
|------|------|------|
| 重复度 | 40% | 与本地 skills 的名称、描述、触发词、结构相似度 |
| 质量 | 35% | 文档完整性、社区验证、维护活跃度、代码健康度、兼容性 |
| 安全 | 25% | 来源可信度、文件名异常、README 风险模式 |

### 决策输出

- **ADOPT** - 质量合格，无重复，直接使用
- **ADAPT** - 质量良好，需适配 MindSymphony 格式
- **ABSORB** - 重复但更优，提取优点融合到现有 skill
- **SKIP** - 重复且质量不如本地
- **REJECT** - 安全风险过高
- **INSPECT** - 质量较低，建议人工审查

## 依赖工具

Skill Hub 集成了以下 CLI 工具（需单独安装）：

- **skillslm** - 访问 anthropics/skills 官方库
  ```bash
  npm install -g skillslm
  ```

- **42plugin** - 访问 42plugin.com 市场
  ```bash
  bun add -g @42ailab/42plugin
  ```

## 开发状态

当前版本: MVP (Minimum Viable Product)

- [x] 核心架构
- [x] 数据模型
- [x] 配置管理
- [x] 数据库层
- [x] 数据源适配器
- [x] 评估引擎
- [x] CLI 入口
- [ ] 完整的 GitHub API 集成
- [ ] 42plugin API 集成
- [ ] 自动适配脚本
- [ ] Intent Router 自动注册

## 许可证

MIT
