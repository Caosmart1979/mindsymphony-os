"""
简单测试脚本 - 验证核心功能
"""

def test_imports():
    """测试导入"""
    print("测试 1: 导入模块...")
    try:
        from agent_core import ReActAgent, Message
        from persona_consistency import PersonaProfile, create_director_manager
        print("✓ 所有模块导入成功")
        return True
    except Exception as e:
        print(f"✗ 导入失败: {e}")
        return False


def test_agent_creation():
    """测试智能体创建"""
    print("\n测试 2: 创建 ReAct 智能体...")
    try:
        from agent_core import ReActAgent, create_agent_instructions
        
        instructions = create_agent_instructions()
        agent = ReActAgent(
            instructions=instructions,
            tools=[]
        )
        print("✓ ReAct 智能体创建成功")
        return True
    except Exception as e:
        print(f"✗ 创建失败: {e}")
        return False


def test_persona_manager():
    """测试人物管理器"""
    print("\n测试 3: 创建人物一致性管理器...")
    try:
        from persona_consistency import create_director_manager
        
        manager = create_director_manager()
        prompt = manager.generate_system_prompt()
        
        if len(prompt) > 100:
            print("✓ 人物管理器创建成功")
            print(f"  生成的提示词长度: {len(prompt)} 字符")
            return True
        else:
            print("✗ 提示词生成异常")
            return False
    except Exception as e:
        print(f"✗ 创建失败: {e}")
        return False


def test_conversation_memory():
    """测试对话记忆"""
    print("\n测试 4: 测试对话记忆功能...")
    try:
        from persona_consistency import create_director_manager
        
        manager = create_director_manager()
        manager.update_memory("user", "测试消息")
        manager.update_memory("assistant", "测试响应")
        
        if len(manager.memory.messages) == 2:
            print("✓ 对话记忆功能正常")
            return True
        else:
            print("✗ 记忆存储异常")
            return False
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        return False


def main():
    """运行所有测试"""
    print("=" * 50)
    print("AI Director Skill 功能测试")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_agent_creation,
        test_persona_manager,
        test_conversation_memory
    ]
    
    results = []
    for test in tests:
        result = test()
        results.append(result)
    
    print("\n" + "=" * 50)
    print(f"测试结果: {sum(results)}/{len(results)} 通过")
    print("=" * 50)
    
    if all(results):
        print("\n🎉 所有测试通过! Skill 已准备就绪。")
    else:
        print("\n⚠️  部分测试失败,请检查代码。")


if __name__ == "__main__":
    main()
