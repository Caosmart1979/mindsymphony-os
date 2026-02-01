# Quick Start - 快速开始

## 5 分钟上手 Simple AI Director

### 步骤 1: 安装依赖

```bash
pip install -r requirements.txt
```

### 步骤 2: 配置 API Key

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填入你的 Anthropic API Key
# ANTHROPIC_API_KEY=sk-ant-xxxxx
```

### 步骤 3: 运行测试

```bash
python tests/test_director.py
```

预期输出:
```
✓ PersonaProfile 创建测试通过
✓ ConversationMemory 测试通过
✓ PersonaManager 测试通过
✓ Session export 测试通过

✅ 所有测试通过!
```

### 步骤 4: 运行示例

```bash
python examples.py
```

### 步骤 5: 开始使用

**命令行模式:**
```bash
python main.py
```

**代码模式:**
```python
from core import AIDirector

director = AIDirector()
response = director.chat("我想拍一个关于咖啡的故事")
print(response)
```

## 常用命令

| 命令 | 说明 |
|------|------|
| `python main.py` | 启动命令行交互 |
| `python tests/test_director.py` | 运行单元测试 |
| `python examples.py` | 运行使用示例 |

## 交互命令

在命令行模式中:
- 输入任何文字与林导对话
- 输入 `stats` 查看会话统计
- 输入 `quit` 或 `exit` 退出

## 下一步

- 阅读 [README.md](README.md) 了解详细功能
- 查看 [examples.py](examples.py) 学习更多用法
- 查看 [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) 了解项目架构

## 遇到问题?

1. **API Key 错误**: 确保 `.env` 文件中的 ANTHROPIC_API_KEY 正确
2. **模块导入错误**: 确保在项目根目录运行命令
3. **编码问题 (Windows)**: 使用 `python -X utf8` 运行

## 技术支持

- 查看原项目: [ai-director](../ai-director/)
- 提交 Issue: [GitHub Issues](https://github.com/your-repo/issues)
