# Simple AI Director

一个精简的 AI 导演助手框架,基于 ReAct 智能体和人物一致性管理。

## 特性

- **ReAct 智能体**: 思维-行动-观察循环
- **人物一致性**: 多轮对话中保持角色特征
- **创意辅助**: 专为创意导演场景设计

## 安装

```bash
pip install -r requirements.txt
```

## 配置

1. 复制 `.env.example` 为 `.env`
2. 填入你的 Anthropic API Key

```bash
cp .env.example .env
```

## 运行

```bash
python main.py
```

## 项目结构

```
simple-ai-director/
├── core/
│   ├── __init__.py
│   ├── models.py       # 数据模型
│   ├── agent.py        # ReAct 智能体
│   ├── persona.py      # 人物一致性管理
│   └── director.py     # 主类
├── main.py             # 命令行入口
├── requirements.txt    # 依赖
└── README.md           # 说明文档
```

## 使用示例

```python
from core import AIDirector

# 初始化
director = AIDirector()

# 对话
response = director.chat("我想拍一个关于咖啡的故事")
print(response)

# 导出会话
session_data = director.export_session()
```

## 命令

- 输入文字与林导对话
- 输入 `stats` 查看会话统计
- 输入 `quit` 或 `exit` 退出

## License

MIT
