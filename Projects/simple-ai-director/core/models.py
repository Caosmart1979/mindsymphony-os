"""
数据模型定义
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime


@dataclass
class Message:
    """消息数据结构"""
    role: str  # 'system', 'user', 'assistant', 'tool'
    content: str
    tool_calls: Optional[List[Dict[str, Any]]] = None
    tool_call_id: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PersonaProfile:
    """人物档案 - 定义 AI 角色的基本特征"""
    name: str  # 角色名称
    role: str  # 角色定位
    personality: str  # 性格特征
    communication_style: str  # 沟通风格
    background: str  # 背景故事
    constraints: List[str] = field(default_factory=list)  # 行为约束
    examples: List[Dict[str, str]] = field(default_factory=list)  # 对话示例


@dataclass
class ConversationMemory:
    """对话记忆 - 存储对话历史和重要信息"""
    session_id: str
    start_time: datetime = field(default_factory=datetime.now)
    messages: List[Message] = field(default_factory=list)
    key_info: Dict[str, Any] = field(default_factory=dict)
    user_preferences: Dict[str, Any] = field(default_factory=dict)

    def add_message(self, role: str, content: str, metadata: Optional[Dict] = None):
        """添加消息到记忆中"""
        message = Message(
            role=role,
            content=content,
            metadata=metadata or {}
        )
        self.messages.append(message)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "session_id": self.session_id,
            "start_time": self.start_time.isoformat(),
            "messages": [
                {
                    "role": msg.role,
                    "content": msg.content,
                    "timestamp": msg.timestamp
                }
                for msg in self.messages
            ],
            "key_info": self.key_info,
            "user_preferences": self.user_preferences
        }
