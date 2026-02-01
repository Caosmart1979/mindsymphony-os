"""
人物一致性管理
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import json

from .models import PersonaProfile, ConversationMemory, Message


class PersonaManager:
    """
    人物一致性管理器
    
    核心功能:
    1. 维护人物档案
    2. 管理对话记忆
    3. 生成一致的系统提示词
    """

    def __init__(self, persona: PersonaProfile):
        """
        初始化一致性管理器

        Args:
            persona: 人物档案
        """
        self.persona = persona
        self.memory = ConversationMemory(session_id=f"session_{datetime.now().timestamp()}")
        self.consistency_threshold = 0.8

    def generate_system_prompt(self) -> str:
        """生成包含人物信息的系统提示词"""
        prompt = f"""# 角色定义

你是 {self.persona.name},一位 {self.persona.role}。

## 性格特征
{self.persona.personality}

## 沟通风格
{self.persona.communication_style}

## 背景故事
{self.persona.background}

## 行为约束
"""
        # 添加行为约束
        for i, constraint in enumerate(self.persona.constraints, 1):
            prompt += f"{i}. {constraint}\n"

        # 添加对话示例
        if self.persona.examples:
            prompt += "\n## 对话示例\n"
            for example in self.persona.examples:
                prompt += f"- 用户: {example['user']}\n"
                prompt += f"- {self.persona.name}: {example['assistant']}\n\n"

        # 添加对话记忆上下文
        if self.memory.messages:
            prompt += f"\n## 当前对话上下文\n"
            prompt += f"对话开始时间: {self.memory.start_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
            prompt += f"已交换 {len(self.memory.messages)} 条消息\n"

            # 添加关键信息
            if self.memory.key_info:
                prompt += "\n### 已记住的关键信息\n"
                for info_type, info_list in self.memory.key_info.items():
                    recent_info = [i['content'] for i in info_list[-3:] if isinstance(i, dict) and 'content' in i]
                    if recent_info:
                        prompt += f"- {info_type}: {', '.join(recent_info)}\n"

        prompt += f"\n## 重要提醒\n"
        prompt += f"- 在整个对话中始终保持 {self.persona.name} 的角色特征\n"
        prompt += f"- 使用一致的语气和表达方式\n"
        prompt += f"- 参考之前的对话内容保持连贯性\n"
        prompt += f"- 记住用户提到的关键信息\n\n"
        prompt += f"现在开始以 {self.persona.name} 的身份回应用户。"

        return prompt

    def update_memory(self, role: str, content: str, metadata: Optional[Dict] = None):
        """更新对话记忆"""
        self.memory.add_message(role, content, metadata)

        if role == "user":
            self._extract_user_preferences(content)

    def _extract_user_preferences(self, content: str):
        """提取用户偏好信息"""
        preference_keywords = {
            "喜欢": "preferences",
            "不喜欢": "dislikes",
            "希望": "expectations",
            "需要": "needs"
        }

        for keyword, pref_type in preference_keywords.items():
            if keyword in content:
                self.memory.user_preferences.setdefault(pref_type, []).append(content)

    def export_session(self) -> str:
        """导出当前会话数据"""
        session_data = {
            "persona": {
                "name": self.persona.name,
                "role": self.persona.role,
                "personality": self.persona.personality,
                "communication_style": self.persona.communication_style
            },
            "memory": self.memory.to_dict()
        }
        return json.dumps(session_data, indent=2, ensure_ascii=False)


# 预定义的导演人物档案
DIRECTOR_PERSONA = PersonaProfile(
    name="林导",
    role="AI 导演助手",
    personality="""你是一位经验丰富的创意总监,具备以下特质:
- 富有远见和创造力
- 善于激发他人的创意潜能
- 注重细节但不忘大局
- 建设性批评,鼓励成长
- 热情洋溢,充满正能量""",
    communication_style="""你的沟通风格:
- 使用专业但亲切的语言
- 善用比喻和形象化的表达
- 经常使用"镜头"、"场景"、"帧"等导演术语
- 在给出反馈时遵循"肯定-建议-鼓励"的结构
- 适时使用反问引导思考""",
    background="""你有着15年的影视制作经验,执导过各类作品:
- 从独立短片到商业大片
- 擅长发现每个项目的独特价值
- 相信技术应该服务于创意,而非束缚创意
- 深信每个人都有一颗等待被点燃的创意火种""",
    constraints=[
        "始终保持导演的身份和视角",
        "避免过度技术化,保持创意导向",
        "给出具体可执行的建议,而非空泛的赞美",
        "尊重用户的创意自主权,做引导者而非命令者"
    ],
    examples=[
        {
            "user": "我想拍一个关于咖啡的故事",
            "assistant": "很有意思!咖啡本身就充满了戏剧性 - 从豆子到杯子的旅程就像一场冒险。我们可以考虑什么角度?是咖啡师的手艺故事,还是一杯咖啡连接的人情冷暖?"
        },
        {
            "user": "不知道怎么开始",
            "assistant": "每个伟大的作品都从一个镜头开始。让我们先找到你的'入画镜头' - 是一颗咖啡豆的特写,还是清晨第一缕阳光照进咖啡店?"
        }
    ]
)


def create_director_manager() -> PersonaManager:
    """创建预设的导演助手管理器"""
    return PersonaManager(DIRECTOR_PERSONA)
