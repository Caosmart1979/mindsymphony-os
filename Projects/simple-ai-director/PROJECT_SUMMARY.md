# Simple AI Director 项目总结

## 项目概述

Simple AI Director 是一个从原 ai-director 项目精简提取的独立运行框架，专注于提供 AI 创意导演辅助功能。

## 核心特性

### 1. ReAct 智能体框架
- **思维-行动-观察循环**: 推理与行动结合的智能体模式
- **工具使用能力**: 可扩展的工具调用系统
- **迭代优化**: 基于观察结果的持续改进

### 2. 人物一致性管理
- **人物档案**: 定义 AI 角色的性格、风格、背景
- **对话记忆**: 维护多轮对话的上下文
- **一致性保证**: 确保角色特征在整个对话中保持一致

### 3. 创意导演场景
- **预置导演人设**: "林导" - 经验丰富的创意总监
- **创意启发**: 专业的创意引导和反馈
- **场景优化**: 专为影视创作场景设计

## 项目结构

```
simple-ai-director/
├── core/                      # 核心模块
│   ├── __init__.py           # 模块导出
│   ├── models.py             # 数据模型 (Message, PersonaProfile, ConversationMemory)
│   ├── agent.py              # ReAct 智能体实现
│   ├── persona.py            # 人物一致性管理
│   └── director.py           # 主类 - 统一接口
├── tests/                     # 测试模块
│   ├── __init__.py
│   └── test_director.py      # 单元测试
├── examples.py               # 使用示例
├── main.py                   # 命令行入口
├── requirements.txt          # 项目依赖
├── .env.example              # 环境变量模板
├── README.md                 # 项目说明
└── PROJECT_SUMMARY.md        # 本文档
```

## 核心组件说明

### 1. 数据模型 (core/models.py)

- **Message**: 消息数据结构
  - role, content, timestamp
  - 支持 tool_calls 和 tool_call_id
  
- **PersonaProfile**: 人物档案
  - name, role, personality
  - communication_style, background
  - constraints, examples
  
- **ConversationMemory**: 对话记忆
  - messages: 消息列表
  - key_info: 关键信息提取
  - user_preferences: 用户偏好

### 2. ReAct 智能体 (core/agent.py)

- **ReActAgent**: 智能体核心类
  - 推理-行动循环实现
  - 工具调用执行
  - 对话历史管理

### 3. 人物管理 (core/persona.py)

- **PersonaManager**: 一致性管理器
  - 生成包含人物信息的系统提示词
  - 维护对话记忆和上下文
  - 提取用户偏好信息
  
- **DIRECTOR_PERSONA**: 预置导演人设
  - "林导" - 15年经验的创意总监
  - 专业的沟通风格和反馈方式

### 4. 主控制器 (core/director.py)

- **AIDirector**: 统一接口类
  - 整合智能体和人物管理
  - Anthropic API 集成
  - 会话管理和导出

## 使用方法

### 1. 基本使用

```python
from core import AIDirector

# 初始化 (需要设置 ANTHROPIC_API_KEY 环境变量)
director = AIDirector()

# 对话
response = director.chat("我想拍一个关于咖啡的故事")
print(response)
```

### 2. 自定义人物

```python
from core import PersonaProfile, PersonaManager

# 创建自定义人物
persona = PersonaProfile(
    name="创意教练",
    role="创意启发专家",
    personality="热情、鼓励、富有洞察力",
    communication_style="使用积极的语言",
    background="20年创意咨询经验"
)

manager = PersonaManager(persona)
```

### 3. 命令行使用

```bash
# 安装依赖
pip install -r requirements.txt

# 配置 API Key
cp .env.example .env
# 编辑 .env 填入 ANTHROPIC_API_KEY

# 运行
python main.py
```

## 测试

```bash
# 运行测试
python tests/test_director.py

# 运行示例
python examples.py
```

## 与原项目的差异

### 简化内容
- 移除了复杂的多文件依赖
- 精简了示例和文档
- 优化了代码结构

### 保留核心
- ✅ ReAct 智能体框架
- ✅ 人物一致性管理
- ✅ 创意导演场景
- ✅ Anthropic API 集成

### 新增内容
- ✅ 独立运行能力
- ✅ 完整的单元测试
- ✅ 使用示例代码
- ✅ 清晰的项目结构

## 技术栈

- **Python 3.8+**
- **anthropic**: Anthropic API SDK
- **python-dotenv**: 环境变量管理
- **dataclasses**: 数据模型定义

## 扩展方向

1. **更多工具集成**: 添加创意辅助工具
2. **多人物支持**: 支持快速切换不同人设
3. **持久化存储**: 会话数据保存和加载
4. **Web 界面**: 开发 Web 交互界面
5. **多模型支持**: 支持 Claude 以外的模型

## License

MIT

## 贡献

欢迎提交 Issue 和 Pull Request!
