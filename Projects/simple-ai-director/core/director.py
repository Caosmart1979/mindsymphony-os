"""
AI Director 主类 - 统一接口
"""

import os
from typing import Optional, Dict, Any
from anthropic import Anthropic

from .agent import ReActAgent
from .persona import PersonaManager, create_director_manager


class AIDirector:
    """
    AI 导演助手 - 统一接口
    
    整合 ReAct 智能体推理能力和人物一致性管理,
    提供创意导演辅助服务。
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "claude-sonnet-4",
        persona_manager: Optional[PersonaManager] = None
    ):
        """
        初始化 AI 导演助手

        Args:
            api_key: Anthropic API key (如不提供则从环境变量读取)
            model: 使用的模型名称
            persona_manager: 人物一致性管理器 (如不提供则使用默认导演设定)
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("需要提供 ANTHROPIC_API_KEY")

        self.client = Anthropic(api_key=self.api_key)
        self.model = model
        self.persona_manager = persona_manager or create_director_manager()

    def chat(self, user_input: str) -> str:
        """
        与导演助手对话

        Args:
            user_input: 用户输入

        Returns:
            助手响应
        """
        # 更新记忆
        self.persona_manager.update_memory("user", user_input)

        # 调用 API 生成响应
        response = self._generate_response(user_input)

        # 更新记忆
        self.persona_manager.update_memory("assistant", response)

        return response

    def _generate_response(self, user_input: str) -> str:
        """生成响应 (实际调用 API)"""
        # 获取对话历史
        messages = self._build_messages(user_input)

        try:
            # 调用 Anthropic API
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                system=self.persona_manager.generate_system_prompt(),
                messages=messages
            )

            # 提取响应文本
            return response.content[0].text

        except Exception as e:
            return f"抱歉,生成响应时出错: {str(e)}"

    def _build_messages(self, user_input: str) -> list:
        """构建消息列表"""
        messages = []

        # 添加历史对话 (最近10轮)
        recent_messages = self.persona_manager.memory.messages[-20:]
        for msg in recent_messages:
            messages.append({
                "role": msg.role,
                "content": msg.content
            })

        # 添加当前用户输入
        messages.append({
            "role": "user",
            "content": user_input
        })

        return messages

    def reset_session(self):
        """重置当前会话"""
        self.persona_manager = create_director_manager()

    def export_session(self) -> str:
        """导出会话数据"""
        return self.persona_manager.export_session()

    def get_session_stats(self) -> Dict[str, Any]:
        """获取会话统计信息"""
        return {
            "message_count": len(self.persona_manager.memory.messages),
            "session_duration": str(self.persona_manager.memory.start_time),
            "key_info_count": sum(
                len(info) for info in self.persona_manager.memory.key_info.values()
            ),
            "user_preferences": self.persona_manager.memory.user_preferences
        }
