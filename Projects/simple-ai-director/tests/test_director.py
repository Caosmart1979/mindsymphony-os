"""
Simple AI Director 测试
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.models import PersonaProfile, Message, ConversationMemory
from core.persona import PersonaManager, create_director_manager


def test_persona_profile():
    """测试人物档案创建"""
    persona = PersonaProfile(
        name="测试助手",
        role="测试角色",
        personality="友好",
        communication_style="简洁",
        background="测试背景"
    )
    assert persona.name == "测试助手"
    print("✓ PersonaProfile 创建测试通过")


def test_conversation_memory():
    """测试对话记忆"""
    memory = ConversationMemory(session_id="test_session")
    memory.add_message("user", "你好")
    memory.add_message("assistant", "你好啊!")
    
    assert len(memory.messages) == 2
    assert memory.messages[0].role == "user"
    print("✓ ConversationMemory 测试通过")


def test_persona_manager():
    """测试人物管理器"""
    manager = create_director_manager()
    
    # 测试系统提示词生成
    prompt = manager.generate_system_prompt()
    assert "林导" in prompt
    assert "AI 导演助手" in prompt
    
    # 测试记忆更新
    manager.update_memory("user", "测试消息")
    assert len(manager.memory.messages) == 1
    
    print("✓ PersonaManager 测试通过")


def test_session_export():
    """测试会话导出"""
    manager = create_director_manager()
    manager.update_memory("user", "我想拍电影")
    manager.update_memory("assistant", "很好的想法!")
    
    session_data = manager.export_session()
    assert "林导" in session_data
    assert "我想拍电影" in session_data
    
    print("✓ Session export 测试通过")


def run_all_tests():
    """运行所有测试"""
    print("🧪 开始测试 Simple AI Director\n")
    
    try:
        test_persona_profile()
        test_conversation_memory()
        test_persona_manager()
        test_session_export()
        
        print("\n✅ 所有测试通过!")
        return True
    except AssertionError as e:
        print(f"\n❌ 测试失败: {e}")
        return False
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
