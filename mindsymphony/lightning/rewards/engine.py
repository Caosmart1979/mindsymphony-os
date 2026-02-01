"""
Reward Engine - 奖励信号工程

核心职责:
1. 显式奖励收集 - 用户直接反馈
2. 隐式信号提取 - 从交互模式推断
3. 计算奖励生成 - 跨任务聚合
4. 奖励归一化和验证

受 Agent Lightning 启发，自动将交互转化为奖励信号
"""

import re
import json
import time
from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class RewardType(Enum):
    """奖励类型"""
    EXPLICIT = "explicit"      # 用户直接反馈
    IMPLICIT = "implicit"      # 从交互模式推断
    COMPUTED = "computed"      # 跨任务计算


@dataclass
class RewardSignal:
    """奖励信号数据结构"""
    reward_type: RewardType
    value: float  # -1.0 to 1.0
    confidence: float  # 0.0 to 1.0
    source: str  # 来源说明
    context: Dict[str, Any]  # 上下文
    timestamp: float


class RewardEngine:
    """奖励信号引擎

    从多维度提取奖励信号，用于驱动进化学习

    维度:
    1. 显式反馈: 用户评分、👍/👎、文字反馈
    2. 任务完成: 完成度、成功/失败
    3. 参与度: 交互深度、追问、延续
    4. 效率: Token效率、时间效率
    5. 协同: 多技能协作流畅度

    示例:
        engine = RewardEngine()

        # 记录显式反馈
        engine.record_explicit_feedback("thumbs_up", confidence=1.0)

        # 从用户消息提取隐式信号
        signals = engine.extract_implicit_signals(user_message, interaction_context)

        # 计算综合奖励
        total_reward = engine.compute_total_reward(episode_data)
    """

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}

        # 权重配置
        self.weights = {
            RewardType.EXPLICIT: self.config.get('explicit_weight', 1.0),
            RewardType.IMPLICIT: self.config.get('implicit_weight', 0.6),
            RewardType.COMPUTED: self.config.get('computed_weight', 0.4)
        }

        # 隐式信号提取器
        self._implicit_extractors: List[Callable] = [
            self._extract_task_completion_signals,
            self._extract_engagement_signals,
            self._extract_sentiment_signals,
            self._extract_efficiency_signals
        ]

        # 历史记录（用于计算奖励）
        self._interaction_history: List[Dict] = []
        self._max_history = 1000

    def record_explicit_feedback(
        self,
        feedback_type: str,  # 'thumbs_up', 'thumbs_down', 'rating', 'text'
        value: Optional[float] = None,
        raw_feedback: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> RewardSignal:
        """记录显式用户反馈

        Args:
            feedback_type: 反馈类型
            value: 数值（如评分 1-5）
            raw_feedback: 原始反馈文本
            metadata: 额外上下文
        """
        context = metadata or {}
        context['feedback_type'] = feedback_type
        context['raw_feedback'] = raw_feedback

        # 转换为 -1.0 ~ 1.0 范围
        normalized_value, confidence = self._normalize_explicit_feedback(
            feedback_type, value, raw_feedback
        )

        reward = RewardSignal(
            reward_type=RewardType.EXPLICIT,
            value=normalized_value,
            confidence=confidence,
            source=f"explicit:{feedback_type}",
            context=context,
            timestamp=time.time()
        )

        return reward

    def _normalize_explicit_feedback(
        self,
        feedback_type: str,
        value: Optional[float],
        raw_feedback: Optional[str]
    ) -> tuple[float, float]:
        """将显式反馈归一化到 [-1, 1]"""

        if feedback_type == 'thumbs_up':
            return 1.0, 1.0

        elif feedback_type == 'thumbs_down':
            return -1.0, 1.0

        elif feedback_type == 'rating':
            # 假设 1-5 评分
            if value is None:
                return 0.0, 0.0
            # 1->-1, 3->0, 5->1
            normalized = (value - 3) / 2
            return max(-1.0, min(1.0, normalized)), 1.0

        elif feedback_type == 'text':
            # 从文本提取情感
            return self._analyze_text_sentiment(raw_feedback or "")

        return 0.0, 0.0

    def _analyze_text_sentiment(self, text: str) -> tuple[float, float]:
        """简单的文本情感分析"""
        text = text.lower()

        # 积极词汇
        positive_words = ['好', '棒', '优秀', '完美', '感谢', 'good', 'great', 'excellent', 'perfect', 'thanks', 'love', 'awesome']
        # 消极词汇
        negative_words = ['差', '糟', '错误', '问题', 'bad', 'poor', 'wrong', 'error', 'terrible', 'awful', 'hate', 'sucks']

        pos_count = sum(1 for w in positive_words if w in text)
        neg_count = sum(1 for w in negative_words if w in text)

        if pos_count == 0 and neg_count == 0:
            return 0.0, 0.3  # 中性，低置信度

        # 计算情感值
        total = pos_count + neg_count
        sentiment = (pos_count - neg_count) / max(total, 1)

        # 置信度基于匹配数量
        confidence = min(0.9, 0.3 + total * 0.2)

        return sentiment, confidence

    def extract_implicit_signals(
        self,
        user_message: str,
        context: Dict[str, Any]
    ) -> List[RewardSignal]:
        """从用户交互中提取隐式奖励信号

        这类似于 Agent Lightning 的隐式信号提取
        """
        signals = []

        for extractor in self._implicit_extractors:
            try:
                signal = extractor(user_message, context)
                if signal:
                    signals.append(signal)
            except Exception as e:
                print(f"[RewardEngine] Extractor error: {e}")

        # 保存到历史
        self._interaction_history.append({
            'message': user_message,
            'context': context,
            'signals': [s.source for s in signals],
            'timestamp': time.time()
        })

        # 限制历史大小
        if len(self._interaction_history) > self._max_history:
            self._interaction_history = self._interaction_history[-self._max_history:]

        return signals

    def _extract_task_completion_signals(
        self,
        message: str,
        context: Dict
    ) -> Optional[RewardSignal]:
        """提取任务完成信号"""
        message = message.lower()

        # 完成信号
        completion_patterns = [
            r'完成', r'好了', r'搞定', r'ok', r'okay', r'done', r'finished',
            r'完美', r'正是', r'exactly', r'perfect', r'thank', r'感谢'
        ]

        # 中断/放弃信号
        interruption_patterns = [
            r'算了', r'停止', r'放弃', r'stop', r'quit', r'give up',
            r'不对', r'错了', r'wrong', r'incorrect'
        ]

        for pattern in completion_patterns:
            if re.search(pattern, message):
                return RewardSignal(
                    reward_type=RewardType.IMPLICIT,
                    value=0.5,
                    confidence=0.7,
                    source="implicit:task_completion",
                    context={"matched_pattern": pattern, "message_preview": message[:50]},
                    timestamp=time.time()
                )

        for pattern in interruption_patterns:
            if re.search(pattern, message):
                return RewardSignal(
                    reward_type=RewardType.IMPLICIT,
                    value=-0.5,
                    confidence=0.7,
                    source="implicit:interruption",
                    context={"matched_pattern": pattern, "message_preview": message[:50]},
                    timestamp=time.time()
                )

        return None

    def _extract_engagement_signals(
        self,
        message: str,
        context: Dict
    ) -> Optional[RewardSignal]:
        """提取参与度信号"""
        # 获取会话历史
        session_id = context.get('session_id')
        if not session_id:
            return None

        # 统计当前会话的交互轮数
        session_messages = [
            h for h in self._interaction_history
            if h['context'].get('session_id') == session_id
        ]

        turn_count = len(session_messages)

        # 多轮交互 = 高参与度
        if turn_count >= 5:
            return RewardSignal(
                reward_type=RewardType.IMPLICIT,
                value=0.3,
                confidence=0.6,
                source="implicit:high_engagement",
                context={"turn_count": turn_count},
                timestamp=time.time()
            )

        # 追问/深入信号
        followup_patterns = [
            r'为什么', r'怎么', r'能否', r'还有', r'详细',
            r'why', r'how', r'can you', r'what about', r'more', r'details'
        ]

        for pattern in followup_patterns:
            if re.search(pattern, message.lower()):
                return RewardSignal(
                    reward_type=RewardType.IMPLICIT,
                    value=0.2,
                    confidence=0.5,
                    source="implicit:followup",
                    context={"matched_pattern": pattern},
                    timestamp=time.time()
                )

        return None

    def _extract_sentiment_signals(
        self,
        message: str,
        context: Dict
    ) -> Optional[RewardSignal]:
        """提取情感信号"""
        sentiment, confidence = self._analyze_text_sentiment(message)

        # 只提取明确的情感
        if abs(sentiment) > 0.3 and confidence > 0.5:
            return RewardSignal(
                reward_type=RewardType.IMPLICIT,
                value=sentiment * 0.5,  # 隐式情感权重较低
                confidence=confidence * 0.8,
                source="implicit:sentiment",
                context={"raw_sentiment": sentiment},
                timestamp=time.time()
            )

        return None

    def _extract_efficiency_signals(
        self,
        message: str,
        context: Dict
    ) -> Optional[RewardSignal]:
        """提取效率信号"""
        # 从上下文获取性能指标
        token_count = context.get('token_count', 0)
        latency_ms = context.get('latency_ms', 0)
        expected_latency = context.get('expected_latency_ms', 5000)

        if latency_ms == 0 or expected_latency == 0:
            return None

        # 效率 = 1 - (实际延迟 / 预期延迟)
        efficiency = 1.0 - (latency_ms / expected_latency)

        # 只有显著的效率差异才产生奖励
        if efficiency > 0.3:  # 比预期快30%
            return RewardSignal(
                reward_type=RewardType.IMPLICIT,
                value=0.2,
                confidence=0.5,
                source="implicit:high_efficiency",
                context={"efficiency": efficiency, "latency_ms": latency_ms},
                timestamp=time.time()
            )
        elif efficiency < -0.5:  # 比预期慢50%
            return RewardSignal(
                reward_type=RewardType.IMPLICIT,
                value=-0.2,
                confidence=0.5,
                source="implicit:low_efficiency",
                context={"efficiency": efficiency, "latency_ms": latency_ms},
                timestamp=time.time()
            )

        return None

    def compute_total_reward(
        self,
        episode_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """计算综合奖励

        聚合显式、隐式、计算三类奖励
        """
        signals = episode_data.get('signals', [])

        # 按类型分组
        by_type = {
            RewardType.EXPLICIT: [],
            RewardType.IMPLICIT: [],
            RewardType.COMPUTED: []
        }

        for signal in signals:
            if isinstance(signal, dict):
                signal = RewardSignal(**signal)
            by_type[signal.reward_type].append(signal)

        # 计算各类型加权奖励
        weighted_rewards = {}
        total_confidence = 0

        for rtype, rlist in by_type.items():
            if not rlist:
                weighted_rewards[rtype] = 0.0
                continue

            # 按置信度加权平均
            total_weight = sum(s.confidence for s in rlist)
            if total_weight == 0:
                weighted_rewards[rtype] = 0.0
                continue

            avg_reward = sum(s.value * s.confidence for s in rlist) / total_weight
            weighted_rewards[rtype] = avg_reward * self.weights[rtype]
            total_confidence += total_weight

        # 总奖励
        total_reward = sum(weighted_rewards.values())

        # 归一化到 [-1, 1]
        total_weight_sum = sum(self.weights.values())
        if total_weight_sum > 0:
            total_reward = total_reward / total_weight_sum

        return {
            "total_reward": max(-1.0, min(1.0, total_reward)),
            "by_type": {
                k.value: v for k, v in weighted_rewards.items()
            },
            "signal_counts": {
                k.value: len(v) for k, v in by_type.items()
            },
            "confidence": min(1.0, total_confidence / max(len(signals), 1)),
            "timestamp": time.time()
        }

    def compute_synergy_reward(
        self,
        skill_sequence: List[str],
        handoff_scores: List[float]
    ) -> RewardSignal:
        """计算多技能协同奖励"""
        if not handoff_scores:
            return RewardSignal(
                reward_type=RewardType.COMPUTED,
                value=0.0,
                confidence=0.0,
                source="computed:synergy",
                context={"reason": "no_handoffs"},
                timestamp=time.time()
            )

        # 协同质量 = 交接流畅度
        avg_handoff = sum(handoff_scores) / len(handoff_scores)

        # 多样性奖励（使用多个不同技能）
        unique_skills = len(set(skill_sequence))
        diversity_bonus = min(0.2, (unique_skills - 1) * 0.05)

        value = avg_handoff * 0.8 + diversity_bonus

        return RewardSignal(
            reward_type=RewardType.COMPUTED,
            value=value,
            confidence=0.6,
            source="computed:synergy",
            context={
                "skill_count": len(skill_sequence),
                "unique_skills": unique_skills,
                "avg_handoff": avg_handoff
            },
            timestamp=time.time()
        )

    def compute_novelty_reward(
        self,
        current_pattern: Dict,
        historical_patterns: List[Dict]
    ) -> RewardSignal:
        """计算新颖性奖励 - 鼓励探索新模式"""
        if not historical_patterns:
            # 第一个模式，给予中等奖励
            return RewardSignal(
                reward_type=RewardType.COMPUTED,
                value=0.3,
                confidence=0.5,
                source="computed:novelty",
                context={"reason": "first_pattern"},
                timestamp=time.time()
            )

        # 计算与历史模式的相似度
        similarities = []
        for pattern in historical_patterns[-100:]:  # 最近100个
            sim = self._pattern_similarity(current_pattern, pattern)
            similarities.append(sim)

        max_similarity = max(similarities) if similarities else 0

        # 新颖度 = 1 - 最大相似度
        novelty = 1.0 - max_similarity

        # 只有显著新颖的模式才奖励
        if novelty > 0.7:
            return RewardSignal(
                reward_type=RewardType.COMPUTED,
                value=0.3,
                confidence=novelty * 0.8,
                source="computed:novelty",
                context={"novelty_score": novelty, "max_similarity": max_similarity},
                timestamp=time.time()
            )

        return RewardSignal(
            reward_type=RewardType.COMPUTED,
            value=0.0,
            confidence=0.3,
            source="computed:novelty",
            context={"novelty_score": novelty, "reason": "not_novel"},
            timestamp=time.time()
        )

    def _pattern_similarity(self, p1: Dict, p2: Dict) -> float:
        """计算两个模式的相似度"""
        # 简化的相似度计算
        s1 = set(p1.get('skills', []))
        s2 = set(p2.get('skills', []))

        if not s1 and not s2:
            return 1.0
        if not s1 or not s2:
            return 0.0

        intersection = len(s1 & s2)
        union = len(s1 | s2)

        return intersection / union if union > 0 else 0.0

    def get_reward_summary(self, hours: int = 24) -> Dict:
        """获取奖励信号摘要"""
        since = time.time() - hours * 3600

        recent = [
            h for h in self._interaction_history
            if h['timestamp'] > since
        ]

        return {
            "period_hours": hours,
            "total_interactions": len(recent),
            "signals_extracted": sum(len(h.get('signals', [])) for h in recent),
            "avg_signals_per_interaction": (
                sum(len(h.get('signals', [])) for h in recent) / len(recent)
                if recent else 0
            )
        }


# 全局 RewardEngine 实例
_default_reward_engine: Optional[RewardEngine] = None


def get_reward_engine(config: Optional[Dict] = None) -> RewardEngine:
    """获取全局 RewardEngine 实例"""
    global _default_reward_engine
    if _default_reward_engine is None:
        _default_reward_engine = RewardEngine(config)
    return _default_reward_engine
