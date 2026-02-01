"""
基础使用示例
演示如何使用技能生态系统进行单技能和多技能协作
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skill_discovery.discovery import SkillDiscoverySystem


def example_single_skill():
    """示例 1: 使用单个技能"""
    print("\n=== 示例 1: 单技能使用 ===")
    
    system = SkillDiscoverySystem()
    
    # 加载前端设计技能
    skill = system.discover_skill("frontend-design")
    
    if skill:
        print(f"✓ 找到技能: {skill['name']}")
        print(f"  描述: {skill['description']}")
        print(f"  能力: {', '.join([c['capability'] for c in skill['interoperability']['provides']])}")
    else:
        print("✗ 未找到技能")


def example_skill_chain():
    """示例 2: 技能协作链"""
    print("\n=== 示例 2: 技能协作链 ===")
    
    system = SkillDiscoverySystem()
    
    # 定义任务
    task = "创建一个登录页面"
    
    # 发现相关技能
    related = system.find_relevant_skills(task)
    
    print(f"任务: {task}")
    print(f"找到 {len(related)} 个相关技能:")
    for skill in related[:3]:
        print(f"  - {skill['name']}: {skill['description'][:50]}...")
    
    # 构建协作链
    chain = system.build_collaboration_chain(task)
    
    if chain:
        print(f"\n推荐的协作链:")
        for i, step in enumerate(chain, 1):
            print(f"  {i}. {step['skill']}")
            if step.get('reason'):
                print(f"     原因: {step['reason']}")


def example_parallel_execution():
    """示例 3: 并行执行"""
    print("\n=== 示例 3: 并行执行模拟 ===")
    
    system = SkillDiscoverySystem()
    
    # 发现可以并行执行的技能
    task = "审查代码并运行测试"
    related = system.find_relevant_skills(task)
    
    print(f"任务: {task}")
    print(f"可并行的技能组合:")
    print(f"  1. {related[0]['name'] if len(related) > 0 else 'code-reviewer'} - 代码审查")
    print(f"  2. {related[1]['name'] if len(related) > 1 else 'test-runner'} - 测试运行")
    print("\n  → 这两个技能可以并行执行以提高效率")


def example_smart_routing():
    """示例 4: 智能路由"""
    print("\n=== 示例 4: 智能路由决策 ===")
    
    system = SkillDiscoverySystem()
    
    # 复杂任务
    task = "创建符合品牌规范的登录页面并生成文档"
    
    # 智能路由
    plan = system.plan_collaboration(task)
    
    print(f"复杂任务: {task}")
    print(f"\n系统推荐的执行计划:")
    print(f"步骤数: {len(plan)}")
    
    for i, step in enumerate(plan, 1):
        print(f"\n步骤 {i}:")
        print(f"  技能: {step['skill']}")
        print(f"  优先级: {step.get('priority', 'normal')}")
        if step.get('dependencies'):
            print(f"  依赖: {', '.join(step['dependencies'])}")


if __name__ == "__main__":
    print("=" * 60)
    print("技能生态系统 - 基础使用示例")
    print("=" * 60)
    
    try:
        example_single_skill()
        example_skill_chain()
        example_parallel_execution()
        example_smart_routing()
        
        print("\n" + "=" * 60)
        print("✓ 所有示例运行完成!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ 错误: {e}")
        import traceback
        traceback.print_exc()
