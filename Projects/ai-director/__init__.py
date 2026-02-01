"""
AI Director Skill
AI导演助手 - ReAct智能体 + 人物一致性管理
"""

from .agent_core import (
    ReActAgent,
    Message,
    create_agent_instructions,
    format_tools_description,
    EXAMPLE_TOOLS
)

from .persona_consistency import (
    PersonaProfile,
    ConversationMemory,
    PersonaConsistencyManager,
    DIRECTOR_PERSONA,
    create_director_manager
)

__version__ = "1.0.0"

__all__ = [
    # Agent Core
    "ReActAgent",
    "Message",
    "create_agent_instructions",
    "format_tools_description",
    "EXAMPLE_TOOLS",
    # Persona Consistency
    "PersonaProfile",
    "ConversationMemory",
    "PersonaConsistencyManager",
    "DIRECTOR_PERSONA",
    "create_director_manager",
]
