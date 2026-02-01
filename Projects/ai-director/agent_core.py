"""
ReAct 智能体核心代码
基于思维-行动-观察循环的对话式智能体
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import json


@dataclass
class Message:
    """消息数据结构"""
    role: str  # 'system', 'user', 'assistant', 'tool'
    content: str
    tool_calls: Optional[List[Dict[str, Any]]] = None
    tool_call_id: Optional[str] = None


class ReActAgent:
    """
    ReAct 智能体 - 实现思维-行动-观察循环

    核心特性:
    1. 推理与行动结合: 在生成响应前先进行思维链推理
    2. 工具使用: 可以调用外部工具获取信息
    3. 观察: 根据工具返回结果调整后续行动
    """

    def __init__(
        self,
        instructions: str,
        tools: List[Dict[str, Any]],
        model: str = "claude-sonnet-4"
    ):
        """
        初始化 ReAct 智能体

        Args:
            instructions: 系统提示词
            tools: 可用工具列表
            model: 使用的模型
        """
        self.instructions = instructions
        self.tools = tools
        self.model = model
        self.conversation_history: List[Message] = []
        self.max_iterations = 10  # 最大迭代次数

        # 初始化时添加系统消息
        self._add_system_message()

    def _add_system_message(self):
        """添加系统消息到对话历史"""
        system_msg = Message(
            role="system",
            content=self.instructions
        )
        self.conversation_history.append(system_msg)

    def _format_messages_for_api(self) -> List[Dict[str, Any]]:
        """将消息历史格式化为 API 请求格式"""
        messages = []
        for msg in self.conversation_history:
            message_dict = {
                "role": msg.role,
                "content": msg.content
            }
            if msg.tool_calls:
                message_dict["tool_calls"] = msg.tool_calls
            if msg.tool_call_id:
                message_dict["tool_call_id"] = msg.tool_call_id
            messages.append(message_dict)
        return messages

    def _execute_tool_call(self, tool_call: Dict[str, Any]) -> str:
        """
        执行工具调用

        Args:
            tool_call: 工具调用信息

        Returns:
            工具执行结果
        """
        tool_name = tool_call["function"]["name"]
        tool_args = json.loads(tool_call["function"]["arguments"])

        # 这里需要根据实际工具映射来执行
        # 这是一个示例框架
        print(f"[执行工具] {tool_name} with args: {tool_args}")

        # 实际实现中,这里会调用真实的工具函数
        # result = tool_mapping[tool_name](**tool_args)

        return f"Tool {tool_name} executed with args: {tool_args}"

    def run(self, user_input: str) -> str:
        """
        运行 ReAct 循环处理用户输入

        Args:
            user_input: 用户输入

        Returns:
            最终响应
        """
        # 添加用户消息
        user_msg = Message(role="user", content=user_input)
        self.conversation_history.append(user_msg)

        iteration = 0
        while iteration < self.max_iterations:
            iteration += 1

            # 调用模型生成响应
            response = self._call_model()
            assistant_msg = Message(
                role="assistant",
                content=response.get("content", ""),
                tool_calls=response.get("tool_calls")
            )
            self.conversation_history.append(assistant_msg)

            # 如果没有工具调用,返回最终响应
            if not assistant_msg.tool_calls:
                return assistant_msg.content

            # 执行工具调用
            for tool_call in assistant_msg.tool_calls:
                result = self._execute_tool_call(tool_call)

                # 添加工具结果到对话历史
                tool_msg = Message(
                    role="tool",
                    content=str(result),
                    tool_call_id=tool_call["id"]
                )
                self.conversation_history.append(tool_msg)

        return "达到最大迭代次数,未能完成请求"

    def _call_model(self) -> Dict[str, Any]:
        """
        调用语言模型

        Returns:
            模型响应
        """
        messages = self._format_messages_for_api()

        # 这里是示例代码,实际需要调用真实 API
        print(f"[模型调用] 准备发送 {len(messages)} 条消息")

        # 模拟响应
        return {
            "content": "这是模拟的模型响应",
            "tool_calls": None
        }

    def reset(self):
        """重置对话历史"""
        self.conversation_history = []
        self._add_system_message()

    def export_conversation(self) -> str:
        """导出对话历史"""
        messages = self._format_messages_for_api()
        return json.dumps(messages, indent=2, ensure_ascii=False)


def create_agent_instructions() -> str:
    """创建 ReAct 智能体的系统提示词"""
    return """你是一个基于 ReAct (Reasoning + Acting) 范式的智能助手。

## 核心原则
1. **思维-行动-观察循环**: 在采取行动前先进行推理,根据观察结果调整策略
2. **明确推理过程**: 使用 <thinking> 标签展示你的思考过程
3. **工具使用**: 当需要外部信息时,主动调用可用工具
4. **迭代优化**: 根据工具返回结果持续优化你的回答

## 推理格式
<thinking>
- 分析用户需求
- 确定需要的信息
- 规划行动步骤
- 预期结果
</thinking>

## 可用工具
{tools_description}

## 响应要求
- 复杂问题先思考再行动
- 工具调用要基于明确的推理
- 根据工具结果调整后续行动
- 最终回答要完整且有帮助

记住: 好的推理带来好的行动!"""


def format_tools_description(tools: List[Dict[str, Any]]) -> str:
    """格式化工具描述"""
    descriptions = []
    for tool in tools:
        name = tool.get("name", "unknown")
        description = tool.get("description", "无描述")
        descriptions.append(f"- **{name}**: {description}")
    return "\n".join(descriptions)


# 示例工具定义
EXAMPLE_TOOLS = [
    {
        "name": "search",
        "description": "搜索信息以回答用户问题",
        "parameters": {
            "query": {"type": "string", "description": "搜索查询"}
        }
    },
    {
        "name": "calculate",
        "description": "执行数学计算",
        "parameters": {
            "expression": {"type": "string", "description": "数学表达式"}
        }
    }
]


if __name__ == "__main__":
    # 示例使用
    instructions = create_agent_instructions()
    agent = ReActAgent(
        instructions=instructions,
        tools=EXAMPLE_TOOLS
    )

    response = agent.run("帮我搜索最新的 AI 发展趋势")
    print(response)
