# AI Director Skill

> 你的私人创意导演助手,基于 ReAct 智能体框架

## 🎬 简介

AI Director 是一个强大的创意导演助手 skill,它结合了:
- **ReAct 智能体**: 思维-行动-观察循环,提供深度推理
- **人物一致性**: 确保"林导"角色在多轮对话中保持稳定风格
- **创意方法论**: 运用专业导演框架进行创意指导

## ✨ 功能特性

- 🧠 **智能推理**: 在给出建议前进行深度思考
- 🎭 **角色一致**: 稳定的"林导"人物设定
- 💡 **创意激发**: 通过提问和引导激发创意
- 📝 **内容规划**: 协助制定拍摄脚本、分镜方案
- 🔄 **对话记忆**: 记住项目背景和用户偏好

## 📦 安装

```bash
# 克隆或下载 skill
cd ai-director

# 安装依赖
pip install -r requirements.txt
```

## 🚀 使用方法

### 1. 命令行模式

```bash
# 设置 API key
export ANTHROPIC_API_KEY="your-api-key"

# 运行
python run.py
```

### 2. Python 代码调用

```python
from ai_director import AIDirector

# 创建助手
director = AIDirector()

# 开始对话
response = director.chat("我想拍一个关于咖啡的短片")
print(response)
```

### 3. 作为 Claude Code Skill 使用

在 Claude Code 中:

```
我有一个创意想法,想用 ai-director 来帮我梳理
```

## 📁 项目结构

```
ai-director/
├── __init__.py           # 包初始化
├── agent_core.py         # ReAct 智能体核心
├── persona_consistency.py # 人物一致性管理
├── run.py               # 统一入口
├── SKILL.md             # Skill 定义
├── requirements.txt     # 依赖
└── README.md           # 本文件
```

## 🎯 使用场景

- 创意项目初期构思
- 脚本和分镜设计
- 内容创作指导
- 项目复盘与优化
- 创意问题解决

## 🔧 配置选项

### 自定义人物设定

编辑 `persona_consistency.py` 中的 `DIRECTOR_PERSONA`:

```python
DIRECTOR_PERSONA = PersonaProfile(
    name="你的角色名",
    role="角色定位",
    personality="性格特征",
    communication_style="沟通风格",
    ...
)
```

### 添加新工具

在 `run.py` 的 `_get_tools()` 方法中添加:

```python
{
    "name": "your_tool",
    "description": "工具描述",
    "input_schema": {...}
}
```

## 📝 示例对话

```
你的创意: 我想拍一个关于城市变迁的纪录片

林导: 很有深度的主题!城市变迁就像一部正在进行的大电影...
```

## ⚠️ 注意事项

1. 需要有效的 Anthropic API key
2. 建议使用 Claude Sonnet 4 模型
3. 对话历史保存在内存中,重启会丢失

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request!
