"""
高级协作模式示例
演示复杂的技能协作场景和模式
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skill_discovery.discovery import SkillDiscoverySystem


def example_waterfall_pattern():
    """瀑布流模式: 顺序执行,每个阶段的输出是下一个的输入"""
    print("\n=== 高级模式 1: 瀑布流 ===")
    
    system = SkillDiscoverySystem()
    
    task = "完整的Web应用开发流程"
    
    # 瀑布流: 需求 → 设计 → 开发 → 测试 → 部署
    workflow = [
        ("frontend-design", "创建界面设计"),
        ("brand-guidelines", "验证品牌一致性"),
        ("doc-coauthoring", "生成技术文档"),
    ]
    
    print(f"工作流: {task}")
    print("\n执行步骤:")
    
    for i, (skill_name, subtask) in enumerate(workflow, 1):
        skill = system.discover_skill(skill_name)
        if skill:
            print(f"\n阶段 {i}: {skill['name']}")
            print(f"  子任务: {subtask}")
            print(f"  输出准备传递给下一阶段...")


def example_parallel_map_reduce():
    """Map-Reduce 模式: 并行处理多个任务,然后聚合结果"""
    print("\n=== 高级模式 2: Map-Reduce ===")
    
    system = SkillDiscoverySystem()
    
    # Map: 并行执行多个分析
    map_tasks = [
        ("code-reviewer", "代码质量审查"),
        ("optimization-advisor", "性能优化分析"),
        ("test-runner", "测试覆盖率检查"),
    ]
    
    print("Map 阶段 - 并行分析:")
    for skill_name, task in map_tasks:
        skill = system.discover_skill(skill_name)
        if skill:
            print(f"  ✓ {skill['name']}: {task}")
    
    print("\nReduce 阶段 - 聚合结果:")
    print("  • 整合所有分析报告")
    print("  • 生成综合优化建议")
    print("  • 优先级排序")


def example_feedback_loop():
    """反馈循环模式: 迭代改进"""
    print("\n=== 高级模式 3: 反馈循环 ===")
    
    system = SkillDiscoverySystem()
    
    task = "持续优化的界面设计"
    
    print(f"任务: {task}")
    print("\n迭代过程:")
    
    max_iterations = 3
    for i in range(1, max_iterations + 1):
        print(f"\n迭代 {i}:")
        print(f"  1. frontend-design - 生成设计")
        print(f"  2. optimization-advisor - 分析改进点")
        print(f"  3. 反馈 → 优化设计")
        
        if i < max_iterations:
            print(f"  → 继续下一轮迭代")
        else:
            print(f"  → 达到优化目标")


def example_conditional_routing():
    """条件路由: 根据结果动态选择下一步"""
    print("\n=== 高级模式 4: 条件路由 ===")
    
    system = SkillDiscoverySystem()
    
    task = "代码审查流程"
    
    print(f"任务: {task}")
    print("\n决策流程:")
    
    # 模拟决策树
    print("1. code-reviewer 执行审查")
    print("   ↓")
    print("2. 检查严重问题")
    print("   ├─ 发现严重问题 → 停止,要求修复")
    print("   ├─ 发现小问题 → optimization-advisor 提供优化建议")
    print("   └─ 无问题 → test-runner 运行测试")


def example_event_driven():
    """事件驱动模式: 基于事件触发技能"""
    print("\n=== 高级模式 5: 事件驱动 ===")
    
    system = SkillDiscoverySystem()
    
    print("事件驱动的自动化流程:")
    print("\n事件 → 技能触发:")
    
    events = [
        ("代码提交", ["code-reviewer", "test-runner"]),
        ("设计更新", ["brand-guidelines", "doc-coauthoring"]),
        ("性能报告", ["optimization-advisor"]),
    ]
    
    for event, skills in events:
        print(f"\n事件: {event}")
        for skill_name in skills:
            skill = system.discover_skill(skill_name)
            if skill:
                print(f"  → 触发 {skill['name']}")


def example_composite_workflow():
    """复合工作流: 组合多种模式"""
    print("\n=== 高级模式 6: 复合工作流 ===")
    
    system = SkillDiscoverySystem()
    
    print("复合工作流: 完整的项目交付流程")
    print("\n阶段 1: 并行准备")
    print("  ├─ frontend-design: 设计界面")
    print("  └─ brand-guidelines: 准备品牌规范")
    
    print("\n阶段 2: 顺序执行")
    print("  ├─ 应用品牌规范到设计")
    print("  └─ doc-coauthoring: 生成文档")
    
    print("\n阶段 3: 反馈循环")
    print("  └─ 迭代优化直到满足标准")
    
    print("\n阶段 4: 最终验证")
    print("  └─ 全面质量检查")


def example_error_recovery():
    """错误恢复模式"""
    print("\n=== 高级模式 7: 错误恢复 ===")
    
    system = SkillDiscoverySystem()
    
    print("容错的执行流程:")
    print("\n主流程:")
    print("  frontend-design → brand-guidelines → doc-coauthoring")
    
    print("\n错误处理策略:")
    print("  ✓ 如果 brand-guidelines 失败:")
    print("    → 记录警告,继续执行")
    print("    → 在最终结果中标注")
    
    print("  ✓ 如果 doc-coauthoring 失败:")
    print("    → 重试 1 次")
    print("    → 仍失败则使用备用文档模板")


if __name__ == "__main__":
    print("=" * 70)
    print("技能生态系统 - 高级协作模式示例")
    print("=" * 70)
    
    try:
        example_waterfall_pattern()
        example_parallel_map_reduce()
        example_feedback_loop()
        example_conditional_routing()
        example_event_driven()
        example_composite_workflow()
        example_error_recovery()
        
        print("\n" + "=" * 70)
        print("✓ 所有高级模式示例运行完成!")
        print("=" * 70)
        print("\n💡 提示: 这些模式可以组合使用以构建复杂的工作流")
        
    except Exception as e:
        print(f"\n✗ 错误: {e}")
        import traceback
        traceback.print_exc()
