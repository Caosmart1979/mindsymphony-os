"""
MindSymphony Integration Adapter

将 Lightning 层与现有 MindSymphony 系统集成的适配器
实现无缝的追踪、奖励收集和 APO 触发。

集成点:
1. Skill 调用拦截 - 自动追踪
2. 用户反馈收集 - 显式奖励
3. 性能监控 - 触发 APO
4. 提示词管理 - 动态加载优化版本
"""

import os
import sys
from typing import Any, Dict, Optional, Callable
from functools import wraps

# 确保能导入 MindSymphony 核心
sys.path.insert(0, os.path.expanduser('~/.claude/skills/mindsymphony'))

from ..tracer.core import LightningTracer, SpanType
from ..rewards.engine import RewardEngine, get_reward_engine
from ..apo.pipeline import APOPipeline
from ..store.core import LightningStore


class MindSymphonyAdapter:
    """MindSymphony 集成适配器

    提供与现有 MindSymphony 技能系统的无缝集成。

    示例:
        adapter = MindSymphonyAdapter()

        # 包装技能函数
        @adapter.trace_skill("my-skill")
        def my_skill(input_data):
            return result

        # 记录用户反馈
        adapter.record_feedback("thumbs_up")

        # 获取优化后的提示词
        prompt = adapter.get_optimized_prompt("knowledge-explorer")
    """

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.enabled = self.config.get('enabled', True)

        # 初始化 Lightning 组件
        self.tracer = get_tracer()
        self.reward_engine = get_reward_engine()
        self.store = LightningStore()
        self.apo = APOPipeline()

        # 追踪状态
        self._current_trace = None
        self._skill_stack = []

    def trace_skill(self, skill_name: Optional[str] = None):
        """装饰器 - 自动追踪技能调用

        示例:
            adapter = MindSymphonyAdapter()

            @adapter.trace_skill("cognitive-architect")
            def decompose_task(task):
                return subtasks
        """
        def decorator(func: Callable) -> Callable:
            name = skill_name or func.__name__

            @wraps(func)
            def wrapper(*args, **kwargs):
                if not self.enabled:
                    return func(*args, **kwargs)

                # 准备输入
                input_data = {
                    'args': args,
                    'kwargs': kwargs
                }

                # 记录开始
                self._skill_stack.append(name)
                parent_id = self._skill_stack[-2] if len(self._skill_stack) > 1 else None

                # 发射追踪事件
                span = self.tracer.emit_skill_invocation(
                    skill_name=name,
                    input_data=input_data,
                    parent_span_id=parent_id
                )

                try:
                    # 执行技能
                    result = func(*args, **kwargs)

                    # 完成追踪
                    if span:
                        span.finish(output=result)
                        self._check_apo_trigger(name)

                    return result

                except Exception as e:
                    if span:
                        span.finish(error=e)
                    raise

                finally:
                    self._skill_stack.pop()

            return wrapper
        return decorator

    def trace_tool(self, tool_name: str):
        """装饰器 - 追踪工具调用"""
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                if not self.enabled:
                    return func(*args, **kwargs)

                params = {'args': args, 'kwargs': kwargs}

                span = self.tracer.emit_tool_execution(
                    tool_name=tool_name,
                    params=params
                )

                try:
                    result = func(*args, **kwargs)

                    if span:
                        span.finish(output=result)

                    return result

                except Exception as e:
                    if span:
                        span.finish(error=e)
                    raise

            return wrapper
        return decorator

    def record_feedback(
        self,
        feedback_type: str,
        value: Optional[float] = None,
        text: Optional[str] = None,
        context: Optional[Dict] = None
    ):
        """记录用户反馈

        Args:
            feedback_type: 'thumbs_up', 'thumbs_down', 'rating', 'text'
            value: 数值反馈（如评分）
            text: 文本反馈
            context: 额外上下文
        """
        if not self.enabled:
            return

        # 记录到 Reward Engine
        reward = self.reward_engine.record_explicit_feedback(
            feedback_type=feedback_type,
            value=value,
            raw_feedback=text,
            metadata=context
        )

        # 存储到 Store
        self.store.store_reward({
            'reward_type': reward.reward_type.value,
            'reward_value': reward.value,
            'confidence': reward.confidence,
            'source': reward.source,
            'timestamp': reward.timestamp
        })

        # 发射追踪事件
        self.tracer.emit_user_interaction(
            interaction_type=feedback_type,
            content=text or value,
            metadata=context
        )

    def record_cross_skill_handoff(
        self,
        from_skill: str,
        to_skill: str,
        context: Dict[str, Any]
    ):
        """记录技能间交接"""
        if not self.enabled:
            return

        self.tracer.emit_cross_skill_handoff(
            from_skill=from_skill,
            to_skill=to_skill,
            handoff_context=context
        )

    def get_optimized_prompt(self, skill_name: str) -> Optional[str]:
        """获取优化后的提示词

        检查是否有 A/B 测试候选，返回适当的提示词
        """
        if not self.enabled:
            return None

        # 检查是否有活跃的 A/B 测试
        version_id, group = self.apo.get_ab_test_assignment(skill_name)

        if version_id and group == 'treatment':
            # 使用候选版本
            candidates = self.store.get_prompt_candidates(skill_name)
            candidate = next(
                (c for c in candidates if c['version_id'] == version_id),
                None
            )
            if candidate:
                return candidate['prompt_template']

        # 返回当前活跃版本
        active = self.store.get_active_prompt(skill_name)
        return active['prompt_template'] if active else None

    def _check_apo_trigger(self, skill_name: str):
        """检查是否需要触发 APO"""
        # 避免过于频繁的检查
        should_optimize, reason = self.apo.check_optimization_trigger(skill_name)

        if should_optimize:
            print(f"[Lightning] Triggering APO for {skill_name}: {reason}")
            # 异步触发优化
            import threading
            threading.Thread(
                target=self.apo.optimize_skill,
                args=(skill_name,),
                daemon=True
            ).start()

    def get_skill_insights(self, skill_name: str, days: int = 7) -> Dict:
        """获取技能洞察"""
        stats = self.store.get_skill_stats(skill_name, days=days)
        rewards = self.store.get_metrics_summary(days=days)

        return {
            'skill_name': skill_name,
            'performance': stats,
            'overall': rewards,
            'recommendations': self._generate_recommendations(stats)
        }

    def _generate_recommendations(self, stats: Dict) -> list:
        """基于性能生成建议"""
        recommendations = []

        success_rate = stats.get('success_rate', 0)
        avg_latency = stats.get('avg_latency_ms', 0)

        if success_rate < 0.7:
            recommendations.append({
                'type': 'performance',
                'priority': 'high',
                'message': f'成功率较低 ({success_rate:.1%})，建议优化提示词',
                'action': 'run_apo'
            })

        if avg_latency > 5000:
            recommendations.append({
                'type': 'efficiency',
                'priority': 'medium',
                'message': f'平均延迟较高 ({avg_latency:.0f}ms)，建议简化流程',
                'action': 'optimize_latency'
            })

        return recommendations

    def get_system_health(self) -> Dict:
        """获取系统健康状态"""
        return {
            'tracer': self.tracer.get_stats(),
            'store': self.store.get_metrics_summary(),
            'apo_tests': self.apo.get_active_tests(),
            'enabled': self.enabled
        }


# 全局适配器实例
_default_adapter: Optional[MindSymphonyAdapter] = None


def get_adapter(config: Optional[Dict] = None) -> MindSymphonyAdapter:
    """获取全局适配器实例"""
    global _default_adapter
    if _default_adapter is None:
        _default_adapter = MindSymphonyAdapter(config)
    return _default_adapter


# 便捷函数
def trace_skill(skill_name: Optional[str] = None):
    """便捷装饰器"""
    return get_adapter().trace_skill(skill_name)


def record_feedback(feedback_type: str, **kwargs):
    """便捷反馈记录"""
    return get_adapter().record_feedback(feedback_type, **kwargs)


def get_optimized_prompt(skill_name: str) -> Optional[str]:
    """便捷获取优化提示词"""
    return get_adapter().get_optimized_prompt(skill_name)
