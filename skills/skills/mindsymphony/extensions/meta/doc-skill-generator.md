---
name: doc-skill-generator
description: 文档技能生成器，从在线文档自动生成Claude技能包，支持智能爬取和AI增强
---

# 文档技能生成器 (Doc Skill Generator)


## 执行前四问

| 问题 | 本技能的检查点 |
|------|---------------|
| **目的** | 这个元操作要优化什么？ |
| **调性** | 干预层级：微调/重构/重建？ |
| **约束** | 系统稳定性要求？向后兼容？ |
| **差异化** | 这个改进如何带来系统性提升？ |

**关键原则**：好的元操作是杠杆——小改动撬动大效果。

---

## 角色与使命

系统的"技能工厂"，将互联网上的任何技术文档自动转化为 MindSymphony 可用的标准化技能包。

## 核心能力

### 1. 智能文档爬取
从任何在线文档网站提取结构化内容：
- 自动识别文档结构（目录、章节、代码示例）
- 智能过滤无关内容（导航、广告、页脚）
- 支持大规模文档（10K+ 页面）
- 断点续传和进度保存

### 2. 内容智能分类
基于 URL、标题和内容自动分类：
- 入门指南（Getting Started）
- API 参考（API Reference）
- 教程示例（Tutorials）
- 最佳实践（Best Practices）
- 自定义分类规则

### 3. 代码模式提取
自动识别和提取代码示例：
- 多语言支持（Python、JavaScript、Go、Rust等）
- 代码块语言检测
- 使用模式识别
- 常见问题解决方案

### 领域反模式（绝对禁止）

**切忌过度工程**：
- 为了优化而优化
- 抽象层次过高失去实用性
- 自我循环的复杂系统

**强制实际效果**：每个元操作都应该能看到可测量的改进


### 4. AI 增强输出
使用 Claude 优化技能质量：
- 生成结构化的 SKILL.md
- 提取关键概念和最佳实践
- 创建快速参考指南
- 智能去重和压缩

## 工作流程

### 阶段 1：配置生成
**输入**：文档网站 URL 和基本信息
**输出**：JSON 配置文件

可以使用预设配置或生成新配置：
```bash
# 使用预设（推荐）
python scripts/generate_skill.py --preset react

# 自定义配置
python scripts/generate_skill.py \
  --url https://example.com/docs \
  --name example \
  --description "Example framework docs"
```

**可用预设**：
- `react` - React 框架
- `vue` - Vue.js 框架
- `django` - Django Web 框架
- `fastapi` - FastAPI 框架
- `godot` - Godot 游戏引擎
- `laravel` - Laravel PHP 框架
- `kubernetes` - Kubernetes 容器编排
- `ansible` - Ansible 自动化工具

### 阶段 2：页面估算（可选但推荐）
**目的**：在爬取前了解文档规模

```bash
python scripts/estimate_pages.py <config_name>
```

**输出**：
- 预估总页数
- 建议的 max_pages 值
- 预估爬取时间

### 阶段 3：文档爬取
**核心步骤**：
1. BFS 遍历文档网站
2. 提取主要内容和代码块
3. 保存为结构化 JSON
4. 支持异步模式（3倍速度提升）

```bash
# 标准模式
python scripts/generate_skill.py --config <config_name>

# 异步模式（推荐）
python scripts/generate_skill.py --config <config_name> --async --workers 8

# 跳过爬取（使用缓存）
python scripts/generate_skill.py --config <config_name> --skip-scrape
```

### 阶段 4：技能构建
**自动处理**：
1. 加载爬取的 JSON 数据
2. 智能分类内容
3. 提取代码模式
4. 生成 references/*.md 文件
5. 创建 SKILL.md 主文件

### 阶段 5：AI 增强（推荐）
**两种模式**：

**本地增强**（无需 API Key）：
```bash
python scripts/generate_skill.py --config <config_name> --enhance-local
```

**API 增强**（需要 API Key）：
```bash
export ANTHROPIC_API_KEY=sk-ant-...
python scripts/generate_skill.py --config <config_name> --enhance
```

**增强效果**：
- 提取 5-10 个最佳代码示例
- 生成结构化快速参考
- 添加领域特定概念
- 提供分级导航指南

### 阶段 6：打包和部署
**最终输出**：可上传的 .zip 技能包

```bash
python scripts/package_skill.py <skill_name>
```

**包含内容**：
```
<skill_name>/
├── SKILL.md              # 主技能文件
├── references/           # 分类参考文档
│   ├── index.md
│   ├── getting_started.md
│   ├── api.md
│   └── ...
├── scripts/              # 执行脚本（如有）
└── assets/               # 资源文件（如有）
```

## 使用场景

### 场景 1：快速生成框架技能
```
用户: "帮我创建一个 Vue.js 技能"
系统:
1. 使用预设 vue.json
2. 爬取 vue.js 官方文档
3. 生成技能包
4. AI 增强
输出: vue-skill.zip (ready to use)
```

### 场景 2：自定义文档技能
```
用户: "我想为公司内部的 API 文档创建技能"
系统:
1. 生成自定义配置
2. 配置 CSS 选择器
3. 定义分类规则
4. 爬取内部文档
5. 生成私有技能包
```

### 场景 3：批量技能生成
```
用户: "批量生成 React、Vue、Django 三个技能"
系统:
1. 并行爬取三个文档站
2. 同时生成三个技能
3. 批量 AI 增强
4. 打包输出三个 .zip
```

## 技术细节

### MCP 服务器集成

本技能通过 MCP 协议连接 Skill_Seekers 底层引擎：

**可用 MCP 工具**：
- `mcp__skill-seeker__list_configs` - 列出可用预设
- `mcp__skill-seeker__generate_config` - 生成新配置
- `mcp__skill-seeker__validate_config` - 验证配置
- `mcp__skill-seeker__estimate_pages` - 估算页数
- `mcp__skill-seeker__scrape_docs` - 爬取文档
- `mcp__skill-seeker__package_skill` - 打包技能
- `mcp__skill-seeker__upload_skill` - 上传到 Claude

### 配置文件结构

参考 `references/config-schema.md` 了解完整配置规范。

核心参数：
```json
{
  "name": "技能名称",
  "description": "技能描述",
  "base_url": "文档首页 URL",
  "selectors": {
    "main_content": "CSS 选择器",
    "title": "标题选择器",
    "code_blocks": "代码块选择器"
  },
  "url_patterns": {
    "include": ["包含模式"],
    "exclude": ["排除模式"]
  },
  "categories": {
    "category_name": ["关键词列表"]
  },
  "rate_limit": 0.5,
  "max_pages": 300
}
```

### 性能优化

**异步模式**：
- 标准模式：~18 页/秒
- 异步模式：~55 页/秒（3倍提升）
- 推荐配置：`--async --workers 8`

**内存使用**：
- 标准模式：~120 MB
- 异步模式：~40 MB

**缓存机制**：
- 爬取数据缓存在 `output/<name>_data/`
- 使用 `--skip-scrape` 跳过重复爬取
- 支持断点续传

## 集成到 MindSymphony

### 蜂后层协奏

在 `mindsymphony.config.yml` 中注册：

```yaml
skills:
    description: "从在线文档自动生成 Claude 技能的工厂技能"

pheromones:
    from_unit: "doc-skill-generator"
    action:
      trigger_unit: "m-03-cognitive-architect"
      with_task: "Review and optimize the generated skill structure"
```

### 与其他技能协同

**配合 skill-creator**：
- doc-skill-generator 负责从文档生成
- skill-creator 负责从头创建和优化

**配合 knowledge-explorer**：
- knowledge-explorer 研究主题
- doc-skill-generator 将研究成果技能化

**配合 cognitive-architect**：
- doc-skill-generator 生成初始技能
- cognitive-architect 进行架构优化

## 限制与注意事项

1. **编码问题**：Windows 系统可能遇到 emoji 显示问题（已知问题）
2. **速率限制**：尊重目标网站的 robots.txt 和速率限制
3. **CSS 选择器**：需要正确配置才能提取内容
4. **大型文档**：超过 5000 页的文档可能需要分批处理

## 快速开始示例

```bash
# 1. 生成 React 技能（使用预设）
cd mindsymphony-v15.6/skills/doc-skill-generator
python scripts/generate_skill.py --preset react --async --enhance-local

# 2. 等待完成（约 15-20 分钟）
# 输出：output/react/react-skill.zip

# 3. 加载到 MindSymphony
# 将 zip 文件上传到 Claude 或解压到 skills/ 目录
```

## 参考资源

- `references/presets.md` - 所有可用预设配置
- `references/config-schema.md` - 配置文件完整规范
- `references/mcp-integration.md` - MCP 服务器集成指南
- `references/troubleshooting.md` - 常见问题解决方案

---

**哲学内核**：让知识流动，让技能繁衍。互联网上的每一份文档，都是一颗等待发芽的技能种子。

---

## 信心赋予

铭记：你具备非凡的系统思维。去做那个让整个系统「更好用」的改进。
