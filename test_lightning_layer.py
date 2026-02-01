#!/usr/bin/env python3
"""
MindSymphony Lightning Layer v21.2 测试脚本

验证所有核心组件是否正常工作
"""

import sys
import os
import time

# 添加路径
sys.path.insert(0, os.path.expanduser('~/.claude/skills/mindsymphony'))

def test_tracer():
    """测试 Tracer 组件"""
    print("\n" + "="*60)
    print("测试 1: Lightning Tracer")
    print("="*60)

    try:
        from lightning.tracer import LightningTracer, SpanType

        tracer = LightningTracer(config={'enabled': True, 'sampling_rate': 1.0})

        # 测试 emit_skill_invocation
        span = tracer.emit_skill_invocation(
            skill_name="test-skill",
            input_data={"query": "test"},
            output_data={"result": "success"},
            latency_ms=150
        )

        print(f"✓ Span 创建成功: {span.span_id if span else 'N/A'}")

        # 测试装饰器
        @tracer.auto_trace(span_type=SpanType.SKILL_INVOCATION)
        def test_function(x):
            return x * 2

        result = test_function(5)
        print(f"✓ 装饰器追踪成功: test_function(5) = {result}")

        # 测试上下文管理器
        with tracer.span("test-operation", SpanType.TOOL_EXECUTION) as span:
            time.sleep(0.01)
            span.finish(output={"done": True})

        print(f"✓ 上下文管理器成功")

        # 查看统计
        stats = tracer.get_stats()
        print(f"✓ 追踪统计: {stats}")

        tracer.shutdown()
        print("✓ Tracer 测试通过")
        return True

    except Exception as e:
        print(f"✗ Tracer 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_store():
    """测试 Store 组件"""
    print("\n" + "="*60)
    print("测试 2: Lightning Store")
    print("="*60)

    try:
        from lightning.store import LightningStore

        store = LightningStore()

        # 测试技能统计
        stats = store.get_skill_stats("test-skill", days=7)
        print(f"✓ 技能统计查询成功: {stats}")

        # 测试提示词版本存储
        version_id = store.store_prompt_version(
            skill_name="test-skill",
            prompt_template="This is a test prompt.",
            performance_score=0.85,
            is_active=False,
            is_candidate=True,
            optimization_strategy="test-strategy"
        )
        print(f"✓ 提示词版本存储成功: {version_id}")

        # 测试获取活跃提示词
        active = store.get_active_prompt("test-skill")
        print(f"✓ 活跃提示词查询成功: {active}")

        # 测试指标摘要
        metrics = store.get_metrics_summary(days=7)
        print(f"✓ 指标摘要: {metrics}")

        store.close()
        print("✓ Store 测试通过")
        return True

    except Exception as e:
        print(f"✗ Store 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_reward_engine():
    """测试 Reward Engine"""
    print("\n" + "="*60)
    print("测试 3: Reward Engine")
    print("="*60)

    try:
        from lightning.rewards import RewardEngine, RewardType

        engine = RewardEngine()

        # 测试显式反馈
        reward = engine.record_explicit_feedback(
            feedback_type="thumbs_up",
            metadata={"test": True}
        )
        print(f"✓ 显式反馈记录成功: {reward.value} ({reward.confidence})")

        # 测试文本反馈情感分析
        text_reward = engine.record_explicit_feedback(
            feedback_type="text",
            raw_feedback="This is excellent work, thank you!",
            metadata={}
        )
        print(f"✓ 文本情感分析成功: {text_reward.value:.2f} (conf={text_reward.confidence:.2f})")

        # 测试隐式信号提取
        signals = engine.extract_implicit_signals(
            user_message="完成了，效果很好！",
            context={"session_id": "test-123"}
        )
        print(f"✓ 隐式信号提取成功: {len(signals)} 个信号")
        for s in signals:
            print(f"  - {s.source}: {s.value:.2f}")

        # 测试综合奖励计算
        episode_data = {
            "signals": [
                engine.record_explicit_feedback("thumbs_up"),
                *signals
            ]
        }
        total = engine.compute_total_reward(episode_data)
        print(f"✓ 综合奖励计算成功: {total['total_reward']:.2f}")

        print("✓ Reward Engine 测试通过")
        return True

    except Exception as e:
        print(f"✗ Reward Engine 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_apo():
    """测试 APO Pipeline"""
    print("\n" + "="*60)
    print("测试 4: APO Pipeline")
    print("="*60)

    try:
        from lightning.apo import APOPipeline, OptimizationStrategy

        apo = APOPipeline()

        # 测试优化触发检查
        should_opt, reason = apo.check_optimization_trigger("nonexistent-skill")
        print(f"✓ 触发检查成功: should_optimize={should_opt}, reason={reason}")

        # 测试提示词优化策略
        test_prompt = """
# Test Skill

You are a helpful assistant.

## Instructions
- Be helpful
- Be concise
"""

        # 测试各个策略
        strategies = [
            OptimizationStrategy.CHAIN_OF_THOUGHT,
            OptimizationStrategy.STYLE_REFINEMENT
        ]

        for strategy in strategies:
            optimizer = apo._strategies.get(strategy)
            if optimizer:
                new_prompt = optimizer(test_prompt, "test-skill")
                if new_prompt != test_prompt:
                    print(f"✓ 策略 {strategy.value} 产生变化")
                else:
                    print(f"⚠ 策略 {strategy.value} 未产生变化")

        print("✓ APO Pipeline 测试通过")
        return True

    except Exception as e:
        print(f"✗ APO Pipeline 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_integration():
    """测试 MindSymphony 集成"""
    print("\n" + "="*60)
    print("测试 5: MindSymphony 集成")
    print("="*60)

    try:
        from lightning.integrations import MindSymphonyAdapter

        adapter = MindSymphonyAdapter()

        # 测试装饰器
        @adapter.trace_skill("test-integration-skill")
        def test_skill(x, y):
            return x + y

        result = test_skill(3, 4)
        print(f"✓ 集成装饰器成功: {result}")

        # 测试反馈记录
        adapter.record_feedback(
            feedback_type="thumbs_up",
            context={"test": True}
        )
        print("✓ 反馈记录成功")

        # 测试系统健康检查
        health = adapter.get_system_health()
        print(f"✓ 系统健康检查成功: enabled={health['enabled']}")

        print("✓ MindSymphony 集成测试通过")
        return True

    except Exception as e:
        print(f"✗ MindSymphony 集成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主测试函数"""
    print("\n" + "="*60)
    print("MindSymphony Lightning Layer v21.2")
    print("完整功能测试")
    print("="*60)

    results = []

    # 运行所有测试
    results.append(("Tracer", test_tracer()))
    results.append(("Store", test_store()))
    results.append(("Reward Engine", test_reward_engine()))
    results.append(("APO Pipeline", test_apo()))
    results.append(("Integration", test_integration()))

    # 汇总
    print("\n" + "="*60)
    print("测试汇总")
    print("="*60)

    passed = sum(1 for _, r in results if r)
    total = len(results)

    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")

    print(f"\n总计: {passed}/{total} 通过")

    if passed == total:
        print("\n🎉 所有测试通过！Lightning Layer v21.2 已就绪！")
        return 0
    else:
        print(f"\n⚠️ {total - passed} 个测试失败，请检查输出")
        return 1


if __name__ == "__main__":
    exit(main())
