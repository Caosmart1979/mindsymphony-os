"""
Simple AI Director 使用示例
"""

import os
from core import AIDirector, PersonaManager, PersonaProfile


def example_basic_usage():
    """基本使用示例"""
    print("=" * 60)
    print("示例 1: 基本使用")
    print("=" * 60)
    
    # 注意: 需要设置 ANTHROPIC_API_KEY 环境变量
    # director = AIDirector()
    # response = director.chat("我想拍一个关于咖啡的故事")
    # print(f"林导: {response}")
    
    print("需要设置 ANTHROPIC_API_KEY 才能运行此示例\n")


def example_custom_persona():
    """自定义人物示例"""
    print("=" * 60)
    print("示例 2: 自定义人物")
    print("=" * 60)
    
    # 创建自定义人物档案
    custom_persona = PersonaProfile(
        name="创意教练",
        role="创意启发专家",
        personality="热情、鼓励、富有洞察力",
        communication_style="使用积极的语言,善于提问引导",
        background="拥有20年创意咨询经验,帮助过无数创作者突破瓶颈",
        constraints=[
            "始终保持鼓励和支持的态度",
            "避免否定或批评",
            "用提问引导而非直接给出答案"
        ],
        examples=[
            {
                "user": "我没有灵感",
                "assistant": "灵感往往来自意想不到的地方。让我们从你最感兴趣的事物开始,有什么特别让你兴奋的话题吗?"
            }
        ]
    )
    
    # 创建自定义管理器
    persona_manager = PersonaManager(custom_persona)
    
    # 查看生成的系统提示词
    system_prompt = persona_manager.generate_system_prompt()
    print(f"系统提示词预览:\n{system_prompt[:200]}...\n")


def example_session_management():
    """会话管理示例"""
    print("=" * 60)
    print("示例 3: 会话管理")
    print("=" * 60)
    
    # director = AIDirector()
    
    # 进行多轮对话
    # director.chat("我想拍一个短片")
    # director.chat("主题是关于时间旅行")
    # director.chat("但预算有限")
    
    # 查看会话统计
    # stats = director.get_session_stats()
    # print(f"会话统计: {stats}")
    
    # 导出会话数据
    # session_data = director.export_session()
    # print(f"会话数据: {session_data}")
    
    print("需要设置 ANTHROPIC_API_KEY 才能运行此示例\n")


def example_persona_components():
    """人物组件独立使用示例"""
    print("=" * 60)
    print("示例 4: 独立使用人物管理器")
    print("=" * 60)
    
    from core.persona import create_director_manager
    
    # 创建人物管理器
    manager = create_director_manager()
    
    # 更新记忆
    manager.update_memory("user", "我想拍一个关于咖啡的故事")
    manager.update_memory("assistant", "很有意思!咖啡本身就充满了戏剧性...")
    manager.update_memory("user", "我想要一个温暖的故事")
    
    # 查看记忆
    print(f"对话轮数: {len(manager.memory.messages)}")
    print(f"用户消息: {[m.content for m in manager.memory.messages if m.role == 'user']}")
    
    # 检查系统提示词是否包含记忆上下文
    prompt = manager.generate_system_prompt()
    has_context = "我想拍一个关于咖啡的故事" in prompt
    print(f"系统提示词包含对话上下文: {has_context}\n")


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("Simple AI Director 使用示例")
    print("=" * 60 + "\n")
    
    example_basic_usage()
    example_custom_persona()
    example_session_management()
    example_persona_components()
    
    print("=" * 60)
    print("所有示例演示完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
