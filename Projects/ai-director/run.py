"""
AI Director 统一入口
整合 ReAct 智能体和人物一致性管理
"""

import os
from typing import Optional, Dict, Any
from anthropic import Anthropic

from .agent_core import ReActAgent, create_agent_instructions, format_tools_description
from .persona_consistency import PersonaConsistencyManager, create_director_manager


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
        persona_manager: Optional[PersonaConsistencyManager] = None
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

        # 初始化 ReAct 智能体
        self._initialize_agent()

    def _initialize_agent(self):
        """初始化 ReAct 智能体"""
        # 生成系统提示词
        instructions = self._create_system_prompt()

        # 定义可用工具
        tools = self._get_tools()

        self.agent = ReActAgent(
            instructions=instructions,
            tools=tools,
            model=self.model
        )

    def _create_system_prompt(self) -> str:
        """创建包含人物信息的系统提示词"""
        return self.persona_manager.generate_system_prompt()

    def _get_tools(self) -> list:
        """定义可用工具列表"""
        return [
            {
                "name": "creative_brainstorm",
                "description": "进行创意头脑风暴,生成多个创意方向",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "topic": {
                            "type": "string",
                            "description": "创意主题"
                        },
                        "count": {
                            "type": "integer",
                            "description": "生成创意方向的数量",
                            "default": 3
                        }
                    },
                    "required": ["topic"]
                }
            },
            {
                "name": "story_structure",
                "description": "构建故事结构,包括起承转合",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "concept": {
                            "type": "string",
                            "description": "核心概念"
                        },
                        "style": {
                            "type": "string",
                            "description": "故事风格",
                            "default": "经典三幕式"
                        }
                    },
                    "required": ["concept"]
                }
            },
            {
                "name": "visual_planning",
                "description": "进行视觉化规划,包括分镜头设计",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "scene": {
                            "type": "string",
                            "description": "场景描述"
                        },
                        "shots_count": {
                            "type": "integer",
                            "description": "镜头数量",
                            "default": 5
                        }
                    },
                    "required": ["scene"]
                }
            }
        ]

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

        # 调用智能体生成响应
        response = self._generate_response(user_input)

        # 更新记忆
        self.persona_manager.update_memory("assistant", response)

        return response

    def _generate_response(self, user_input: str) -> str:
        """
        生成响应 (实际调用 API)

        Args:
            user_input: 用户输入

        Returns:
            模型响应
        """
        # 获取对话历史
        messages = self._build_messages(user_input)

        try:
            # 调用 Anthropic API
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                system=self._create_system_prompt(),
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
                "role": msg["role"],
                "content": msg["content"]
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
        self._initialize_agent()

    def export_session(self) -> str:
        """导出会话数据"""
        return self.persona_manager.export_session()

    def get_session_stats(self) -> Dict[str, Any]:
        """获取会话统计信息"""
        return {
            "message_count": len(self.persona_manager.memory.messages),
            "session_duration": str(
                self.persona_manager.memory.start_time
            ),
            "key_info_count": sum(
                len(info) for info in self.persona_manager.memory.key_info.values()
            ),
            "user_preferences": self.persona_manager.memory.user_preferences
        }


def main():
    """命令行入口"""
    import sys

    print("🎬 AI Director - 创意导演助手")
    print("=" * 50)
    print("输入 'quit' 或 'exit' 退出\n")

    try:
        director = AIDirector()

        while True:
            user_input = input("你的创意: ").strip()

            if user_input.lower() in ['quit', 'exit', '退出']:
                print("\n感谢使用 AI Director! 再见!")
                break

            if not user_input:
                continue

            print("\n林导: ", end="", flush=True)
            response = director.chat(user_input)
            print(response)
            print()

            # 显示会话统计
            if user_input.lower() == 'stats':
                stats = director.get_session_stats()
                print("\n会话统计:")
                for key, value in stats.items():
                    print(f"  {key}: {value}")
                print()

    except KeyboardInterrupt:
        print("\n\n感谢使用 AI Director! 再见!")
    except Exception as e:
        print(f"\n错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
