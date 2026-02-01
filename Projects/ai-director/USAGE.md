# AI Director Skill - 使用说明

## 📋 安装步骤

### 1. 安装依赖

```bash
# 进入 skill 目录
cd ai-director

# 安装 Python 依赖
pip install -r requirements.txt
```

### 2. 配置 API Key

```bash
# 设置环境变量 (Linux/Mac)
export ANTHROPIC_API_KEY="your-api-key-here"

# 或在 Windows PowerShell 中
$env:ANTHROPIC_API_KEY="your-api-key-here"
```

## 🎯 使用方法

### 方法 1: 命令行交互

```bash
# 运行导演助手
python run.py
```

然后输入你的创意想法,与"林导"进行对话。

### 方法 2: Python 代码调用

```python
# example.py
from ai_director import AIDirector

# 创建助手实例
director = AIDirector()

# 对话
response = director.chat("我想拍一个关于城市变迁的纪录片")
print(response)

# 查看会话统计
stats = director.get_session_stats()
print(stats)

# 导出会话
session_data = director.export_session()
print(session_data)
```

### 方法 3: 作为 Claude Code Skill

在 Claude Code 中直接使用:

```
请调用 ai-director skill 帮我构思一个短视频创意
```

## 🔍 功能验证

### 手动测试步骤

1. **测试导入**:
```python
python3 -c "from ai_director import AIDirector; print('✓ 导入成功')"
```

2. **测试人物管理**:
```python
python3 << PYEOF
from ai_director.persona_consistency import create_director_manager
manager = create_director_manager()
prompt = manager.generate_system_prompt()
print(f"✓ 提示词生成成功,长度: {len(prompt)} 字符")
PYEOF
```

3. **测试智能体创建**:
```python
python3 << PYEOF
from ai_director.agent_core import ReActAgent, create_agent_instructions
agent = ReActAgent(
    instructions=create_agent_instructions(),
    tools=[]
)
print("✓ ReAct 智能体创建成功")
PYEOF
```

4. **运行完整测试**:
```bash
python test_skill.py
```

## 📝 示例对话场景

### 场景 1: 创意构思

```
你的创意: 我想拍一个关于咖啡的短片

林导: 很有意思!咖啡本身就充满了戏剧性 - 从豆子到杯子的旅程就像一场冒险。我们可以考虑什么角度?
```

### 场景 2: 故事结构

```
你的创意: 帮我构建一个关于追梦的故事结构

林导: 追梦故事是最经典的叙事...让我们用"英雄之旅"的框架来构建...
```

### 场景 3: 视觉规划

```
你的创意: 我需要一个雨夜的分手场景

林导: 雨夜分手,很有画面感!我们可以这样设计镜头...
```

## ⚙️ 自定义配置

### 修改人物设定

编辑 `persona_consistency.py`:

```python
# 修改人物特征
DIRECTOR_PERSONA = PersonaProfile(
    name="你的名字",
    role="你的定位",
    personality="你的性格...",
    ...
)
```

### 添加自定义工具

编辑 `run.py` 中的 `_get_tools()` 方法:

```python
def _get_tools(self):
    return [
        # 现有工具...
        {
            "name": "your_custom_tool",
            "description": "你的工具描述",
            "input_schema": {
                "type": "object",
                "properties": {
                    "param": {"type": "string"}
                }
            }
        }
    ]
```

## 🐛 故障排除

### 问题 1: API Key 错误

```
错误: ValueError: 需要提供 ANTHROPIC_API_KEY
解决: 确保已正确设置环境变量或传入 api_key 参数
```

### 问题 2: 导入失败

```
错误: ModuleNotFoundError: No module named 'anthropic'
解决: 运行 pip install -r requirements.txt
```

### 问题 3: 响应为空

```
错误: 模型没有返回响应
解决: 检查 API key 是否有效,网络连接是否正常
```

## 📊 性能优化建议

1. **调整 token 限制**: 在 `run.py` 中修改 `max_tokens` 参数
2. **缓存会话**: 定期调用 `export_session()` 保存对话
3. **模型选择**: 根据需求选择不同的 Claude 模型

## 🔗 相关资源

- [Anthropic API 文档](https://docs.anthropic.com/)
- [ReAct 论文](https://arxiv.org/abs/2210.03629)
- [Claude Code 文档](https://docs.claude.com/)

## 💡 最佳实践

1. 明确你的创意需求,提供足够的上下文
2. 充分利用对话记忆,逐步深入讨论
3. 定期导出会话数据,保存重要讨论
4. 根据反馈调整人物设定和工具配置

---

有问题? 查看 README.md 或提交 Issue!
