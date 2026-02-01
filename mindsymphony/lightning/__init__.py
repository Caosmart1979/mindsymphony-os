"""
MindSymphony Lightning Layer v21.2
受 Microsoft Agent Lightning 启发的进化训练基础设施

核心组件:
- Tracer: 非侵入式事件追踪
- Store: 中心化数据存储
- RewardEngine: 奖励信号工程
- APO: 自动提示词优化

使用方法:
    from mindsymphony.lightning import get_tracer, get_reward_engine

    tracer = get_tracer()
    tracer.emit_skill_invocation("my_skill", input_data, output_data)
"""

__version__ = "21.2.0"
__codename__ = "Lightning"

# 导出核心类（延迟加载避免循环导入）
def get_tracer(config=None):
    """获取全局 Tracer 实例"""
    from .tracer.core import LightningTracer
    return LightningTracer(config)

def get_store():
    """获取全局 Store 实例"""
    from .store.core import LightningStore
    return LightningStore()

def get_reward_engine(config=None):
    """获取全局 RewardEngine 实例"""
    from .rewards.engine import get_reward_engine as _get_re
    return _get_re(config)

def get_apo(config=None):
    """获取全局 APO 实例"""
    from .apo.pipeline import APOPipeline
    return APOPipeline(config)

# 导出核心类型
from .tracer.core import Span, SpanType
from .rewards.engine import RewardSignal, RewardType
from .apo.pipeline import PromptCandidate, OptimizationStrategy

__all__ = [
    "get_tracer", "get_store", "get_reward_engine", "get_apo",
    "Span", "SpanType",
    "RewardSignal", "RewardType",
    "PromptCandidate", "OptimizationStrategy"
]
