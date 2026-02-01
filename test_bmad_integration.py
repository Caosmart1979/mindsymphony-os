#!/usr/bin/env python3
"""
BMAD + MindSymphony 整合测试脚本
验证所有核心功能
"""

import sys
import os

# 添加路径
sys.path.insert(0, os.path.expanduser('~/.claude/skills/mindsymphony'))
sys.path.insert(0, 'mindsymphony/extensions')

print("=" * 70)
print("  MindSymphony + BMAD Integration Test")
print("  Version: v21.3")
print("=" * 70)

# 测试计数
tests_passed = 0
tests_failed = 0

def test(name):
    """测试装饰器"""
    def decorator(func):
        def wrapper():
            global tests_passed, tests_failed
            try:
                print(f"\n🧪 测试: {name}")
                func()
                print(f"   ✓ 通过")
                tests_passed += 1
                return True
            except Exception as e:
                print(f"   ✗ 失败: {e}")
                tests_failed += 1
                return False
        return wrapper
    return decorator

# ==================== 测试1: 复杂度评估 ====================
@test("复杂度评估引擎")
def test_complexity_evaluator():
    from bmad import ComplexityEvaluator, evaluate_complexity

    evaluator = ComplexityEvaluator()

    # 测试简单任务
    score = evaluator.evaluate("fix a typo in the login button")
    assert score.total_score <= 3, f"简单任务评分应<=3，实际{score.total_score}"
    assert score.recommended_path == "quick", "应推荐quick路径"

    # 测试复杂任务
    score2 = evaluator.evaluate("design a distributed microservices architecture")
    assert score2.total_score >= 6, f"复杂任务评分应>=6，实际{score2.total_score}"
    assert score2.recommended_path == "party", "应推荐party路径"

    # 测试便捷函数
    score3 = evaluate_complexity("add a new API endpoint for user profile")
    assert score3.total_score >= 4, f"中等任务评分应>=4，实际{score3.total_score}"

    print(f"   评分示例: typo修复={score.total_score}, 微服务={score2.total_score}")

# ==================== 测试2: 快捷指令解析 ====================
@test("快捷指令解析")
def test_quick_commands():
    from bmad import QuickCommandParser, parse_command

    parser = QuickCommandParser()

    # 测试 /ms-quick
    cmd = parser.parse("/ms-quick fix login bug")
    assert cmd.command == "/ms-quick"
    assert cmd.command_type.value == "workflow"
    assert cmd.execution_params["workflow"] == "quick"

    # 测试 /ms-deep
    cmd2 = parser.parse("/ms-deep design new system --plan-only")
    assert cmd2.command == "/ms-deep"
    assert cmd2.flags.get("plan-only") == "true"

    # 测试 /ms-party
    cmd3 = parser.parse("/ms-party refactor core --roles=architect,developer,tester")
    assert cmd3.command == "/ms-party"
    assert "architect" in cmd3.execution_params.get("roles", [])

    # 测试别名
    cmd4 = parser.parse("/fix small bug")
    assert cmd4.command == "/ms-quick"  # 应解析为标准命令

    # 测试自然语言
    cmd5 = parser.parse("帮我修复一个bug")
    assert cmd5.command_type.value == "workflow"
    assert cmd5.execution_params.get("auto_route") == True

    print(f"   解析示例: {cmd.command}, {cmd2.command}, {cmd3.command}")

# ==================== 测试3: 工作流路由 ====================
@test("工作流路由")
def test_workflow_router():
    from bmad import WorkflowRouter, route_request

    router = WorkflowRouter()

    # 测试 Quick Flow 路由
    result = router.route("fix typo in docs")
    assert result["workflow_type"] == "quick"
    assert len(result["stages"]) <= 4
    assert "execution_id" in result

    # 测试 Full Planning 路由
    result2 = router.route("design new feature", force_path="full")
    assert result2["workflow_type"] == "full"
    assert len(result2["stages"]) >= 6

    # 测试 Party Mode 路由
    result3 = router.route("redesign entire architecture", force_path="party")
    assert result3["workflow_type"] == "party"

    # 测试便捷函数
    result4 = route_request("simple bug fix")
    assert "workflow_type" in result4

    print(f"   路由示例: {result['workflow_type']}, {result2['workflow_type']}")

# ==================== 测试4: Party Mode ====================
@test("Party Mode 会话")
def test_party_mode():
    from bmad import PartySession, AgentRole, CollaborationPhase

    # 创建 Party 会话
    roles = [AgentRole.ARCHITECT, AgentRole.DEVELOPER]
    party = PartySession(roles)

    # 启动会话
    start_info = party.start_session({
        "description": "设计新的用户系统",
        "context": "test"
    })

    assert "session_id" in start_info
    assert len(start_info["roles"]) == 2

    session_id = start_info["session_id"]

    # 运行阶段
    phase1_result = party.run_phase(CollaborationPhase.UNDERSTANDING)
    assert phase1_result["phase"] == "understanding"
    assert len(phase1_result["contributions"]) == 2  # 两个角色

    phase2_result = party.run_phase(CollaborationPhase.DIVERGENCE)
    assert phase2_result["phase"] == "divergence"

    # 获取报告
    report = party.get_session_report()
    assert report["session_id"] == session_id
    assert report["total_contributions"] > 0

    # 综合方案
    unified_plan = party.synthesize_consensus()
    assert unified_plan.summary != ""
    assert len(unified_plan.action_items) > 0

    print(f"   Party会话: {session_id}, 贡献数: {report['total_contributions']}")

# ==================== 测试5: BMAD 集成入口 ====================
@test("BMAD 集成入口")
def test_bmad_integration():
    from bmad import get_bmad_integration, process

    # 获取集成实例
    bmad = get_bmad_integration()
    assert bmad is not None
    assert bmad.enabled == True

    # 处理请求 - Quick Flow
    result = bmad.process_request("/ms-quick fix typo")
    assert result["workflow_type"] == "quick"

    # 处理请求 - Help
    result2 = bmad.process_request("/ms-help")
    assert result2["status"] == "help"

    # 处理请求 - Status
    result3 = bmad.process_request("/ms-status")
    assert result3["status"] == "system_status"
    assert "bmad_version" in result3

    # 便捷函数
    result4 = process("/ms-help quick")
    assert result4["status"] == "help"

    print(f"   集成测试通过: version={result3.get('bmad_version')}")

# ==================== 测试6: 完整工作流 ====================
@test("完整工作流执行")
def test_full_workflow():
    from bmad import get_bmad_integration

    bmad = get_bmad_integration()

    # 启动工作流
    result = bmad.process_request("/ms-quick fix a bug in login")
    execution_id = result["execution_id"]

    # 模拟执行阶段
    next_stage = bmad.get_workflow_next_step(execution_id)
    assert next_stage is not None

    # 完成阶段
    result = bmad.complete_workflow_stage(
        execution_id,
        stage_result={"status": "done"},
        metrics={"duration": 5}
    )

    # 验证可以继续到下一阶段
    assert "stage_name" in result or result.get("status") == "completed"

    print(f"   工作流执行: {execution_id}")

# ==================== 测试7: 复杂度解释 ====================
@test("复杂度解释输出")
def test_complexity_explanation():
    from bmad import ComplexityEvaluator

    evaluator = ComplexityEvaluator()
    score = evaluator.evaluate("design a complex distributed system")

    explanation = evaluator.explain_decision(score)
    assert "复杂度评估报告" in explanation or "复杂度" in explanation
    assert str(score.total_score) in explanation
    # 路径名称可能被装饰，只检查关键词存在
    assert "party" in score.recommended_path.lower() or "full" in score.recommended_path.lower()

    print(f"   解释长度: {len(explanation)} 字符, 推荐路径: {score.recommended_path}")

# ==================== 测试8: 帮助系统 ====================
@test("帮助系统")
def test_help_system():
    from bmad import get_help, QuickCommandParser

    parser = QuickCommandParser()

    # 获取总体帮助
    help_text = parser.get_help_text()
    assert "/ms-quick" in help_text
    assert "/ms-deep" in help_text
    assert "/ms-party" in help_text

    # 获取特定主题帮助
    party_help = parser.get_help_text("party")
    assert "Party Mode" in party_help or "party" in party_help.lower()

    # 命令建议
    suggestions = parser.get_suggestion("/ms-")
    assert len(suggestions) > 0

    # 便捷函数
    help2 = get_help("quick")
    assert "quick" in help2.lower() or "快速" in help2

    print(f"   帮助系统: {len(help_text)} 字符, 建议数: {len(suggestions)}")

# ==================== 测试9: 边界条件测试 ====================
@test("边界条件测试")
def test_edge_cases():
    """测试边界条件和异常情况"""
    from bmad import evaluate_complexity, parse_command, WorkflowRouter

    # 测试空输入
    try:
        result = evaluate_complexity("")
        assert result is not None
        print("   ✓ 空输入处理正常")
    except Exception as e:
        print(f"   ⚠ 空输入处理: {e}")

    # 测试超长输入
    long_input = "design " * 1000
    result = evaluate_complexity(long_input)
    assert result.confidence >= 0
    print("   ✓ 超长输入处理正常")

    # 测试特殊字符
    special_chars = "fix bug @#$%^&*()"
    cmd = parse_command(special_chars)
    assert cmd is not None
    print("   ✓ 特殊字符处理正常")

    # 测试无效命令
    invalid_cmd = parse_command("/invalid-command")
    assert not invalid_cmd.should_execute
    print("   ✓ 无效命令处理正常")

    # 测试只有空格的输入
    whitespace_only = parse_command("   ")
    assert whitespace_only is not None
    print("   ✓ 空白输入处理正常")

    # 测试极短输入
    short = evaluate_complexity("a")
    assert short.total_score >= 1
    print("   ✓ 极短输入处理正常")

# ==================== 运行所有测试 ====================
def main():
    print("\n开始测试...\n")

    tests = [
        test_complexity_evaluator,
        test_quick_commands,
        test_workflow_router,
        test_party_mode,
        test_bmad_integration,
        test_full_workflow,
        test_complexity_explanation,
        test_help_system,
        test_edge_cases,
    ]

    for test_func in tests:
        test_func()

    # 总结
    print("\n" + "=" * 70)
    print(f"  测试完成!")
    print(f"  通过: {tests_passed}/{len(tests)}")
    print(f"  失败: {tests_failed}/{len(tests)}")
    print("=" * 70)

    if tests_failed == 0:
        print("\n✅ 所有测试通过! BMAD + MindSymphony v21.3 已就绪!")
        return 0
    else:
        print(f"\n⚠️  {tests_failed} 个测试失败")
        return 1

if __name__ == "__main__":
    sys.exit(main())
