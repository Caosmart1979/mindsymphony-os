"""
ReAct 智能体核心实现
"""

from typing import List, Dict, Any, Optional
import json

from .models import Message, ConversationMemory


class ReActAgent:
    """
    ReAct 智能体 - 实现思维-行动-观察循环

    核心特性:
    1. 推理与行动结合
    2. 工具使用能力
    3. 观察与迭代优化
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
        self.memory = ConversationMemory(session_id=f"react_{int(datetime.now().timestamp())}")
        self.max_iterations = 10

    def _execute_tool_call(self, tool_call: Dict[str, Any]) -> str:
        """执行工具调用"""
        tool_name = tool_call["function"]["name"]
        tool_args = json.loads(tool_call["function"]["arguments"])
        return f"Tool {tool_name} executed with args: {tool_args}"

    def run(self, user_input: str) -> str:
        """运行 ReAct 循环处理用户输入"""
        self.memory.add_message("user", user_input)

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
            self.memory.messages.append(assistant_msg)

            # 如果没有工具调用,返回最终响应
            if not assistant_msg.tool_calls:
                return assistant_msg.content

            # 执行工具调用
            for tool_call in assistant_msg.tool_calls:
                result = self._execute_tool_call(tool_call)
                tool_msg = Message(
                    role="tool",
                    content=str(result),
                    tool_call_id=tool_call["id"]
                )
                self.memory.messages.append(tool_msg)

        return "达到最大迭代次数,未能完成请求"

    def _call_model(self) -> Dict[str, Any]:
        """调用语言模型 (需要子类实现)"""
        return {
            "content": "这是模拟的模型响应",
            "tool_calls": None
        }

    def reset(self):
        """重置对话历史"""
        self.memory = ConversationMemory(session_id=f"react_{int(datetime.now().timestamp())}")


# 修复 datetime 导入
from datetime import datetime
