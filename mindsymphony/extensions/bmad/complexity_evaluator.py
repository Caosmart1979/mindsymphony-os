"""
复杂度评估引擎
基于 BMAD 方法论，自动评估任务的复杂度并推荐合适的工作流路径
"""

import re
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Tuple
import json
import os


class DomainComplexity(Enum):
    SIMPLE = 1    # bugfix, docs, refactor
    MEDIUM = 3    # feature, api
    COMPLEX = 5   # architecture, service
    EXPERT = 8    # distributed, ai-model


class ScaleComplexity(Enum):
    TINY = 1      # <50 lines
    SMALL = 2     # 50-200 lines
    MEDIUM = 4    # 200-1000 lines
    LARGE = 7     # 1000+ lines


class ImpactScope(Enum):
    ISOLATED = 1   # 单一模块
    MODULE = 3     # 多个模块
    CROSS_TEAM = 5 # 跨团队
    BREAKING = 7   # 破坏性变更


@dataclass
class ComplexityScore:
    """复杂度评分结果"""
    total_score: int           # 总分 (1-10+)
    domain_score: int
    scale_score: int
    impact_score: int
    domain_type: str
    scale_type: str
    impact_type: str
    recommended_path: str      # "quick" | "full" | "party"
    confidence: float          # 0.0 - 1.0
    reasoning: List[str]       # 评分理由

    def to_dict(self) -> Dict:
        return {
            "total_score": self.total_score,
            "domain_score": self.domain_score,
            "scale_score": self.scale_score,
            "impact_score": self.impact_score,
            "domain_type": self.domain_type,
            "scale_type": self.scale_type,
            "impact_type": self.impact_type,
            "recommended_path": self.recommended_path,
            "confidence": self.confidence,
            "reasoning": self.reasoning
        }


class ComplexityEvaluator:
    """
    复杂度评估引擎

    评估维度:
    1. 领域复杂度 (Domain) - 技术领域难度
    2. 规模复杂度 (Scale) - 代码量/文件数
    3. 影响范围 (Impact) - 变更影响面

    总分 = domain + scale + impact
    - 1-3: Quick Flow
    - 4-5: Full Planning
    - 6+: 建议 Party Mode
    """

    # 领域关键词映射
    DOMAIN_KEYWORDS = {
        DomainComplexity.SIMPLE: [
            "fix", "bug", "typo", "doc", "comment", "rename", "format",
            "lint", "style", "cleanup", "refactor", "extract", "move",
            "update", "patch", "correct", "improve"
        ],
        DomainComplexity.MEDIUM: [
            "add", "feature", "endpoint", "component", "page", "route",
            "api", "function", "method", "class", "module", "service",
            "implement", "create", "build"
        ],
        DomainComplexity.COMPLEX: [
            "system", "platform", "architecture", "redesign", "migration",
            "refactor", "restructure", "redesign", "framework", "engine",
            "orchestration", "workflow", "pipeline"
        ],
        DomainComplexity.EXPERT: [
            "distributed", "consensus", "crypto", "blockchain", "ml-model",
            "ai-training", "kernel", "compiler", "database-engine",
            "real-time", "high-performance", "concurrent", "parallel"
        ]
    }

    # 规模关键词
    SCALE_KEYWORDS = {
        "files": {
            ScaleComplexity.TINY: ["one file", "single file", "小文件"],
            ScaleComplexity.SMALL: ["few files", "couple files", "几个文件"],
            ScaleComplexity.MEDIUM: ["multiple files", "several files", "多个文件"],
            ScaleComplexity.LARGE: ["many files", "across project", "整个项目"]
        },
        "lines": {
            ScaleComplexity.TINY: ["few lines", "trivial", "简单几行"],
            ScaleComplexity.SMALL: ["small change", "几十行"],
            ScaleComplexity.MEDIUM: ["hundreds of lines", "几百行"],
            ScaleComplexity.LARGE: ["thousands of lines", "大规模", "上千行"]
        }
    }

    # 影响范围关键词
    IMPACT_KEYWORDS = {
        ImpactScope.ISOLATED: [
            "isolated", "single", "one place", "local", "internal",
            "private", "helper", "utility"
        ],
        ImpactScope.MODULE: [
            "module", "package", "component", "several places",
            "multiple locations", "related"
        ],
        ImpactScope.CROSS_TEAM: [
            "cross-team", "shared", "common", "public api",
            "interface", "contract", "dependency"
        ],
        ImpactScope.BREAKING: [
            "breaking", "deprecated", "major version", "incompatible",
            "fundamental", "core", "critical path"
        ]
    }

    # 阈值配置
    THRESHOLDS = {
        "quick_flow_max": 3,
        "full_flow_min": 4,
        "party_mode_min": 6
    }

    def __init__(self, config_path: Optional[str] = None):
        """
        初始化复杂度评估器

        Args:
            config_path: 可选的配置文件路径
        """
        self.config = self._load_config(config_path)
        self._compile_patterns()

    def _load_config(self, config_path: Optional[str]) -> Dict:
        """加载配置"""
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _compile_patterns(self):
        """编译正则表达式模式"""
        self.domain_patterns = {}
        for domain, keywords in self.DOMAIN_KEYWORDS.items():
            pattern = r'\b(?:' + '|'.join(re.escape(kw) for kw in keywords) + r')\b'
            self.domain_patterns[domain] = re.compile(pattern, re.IGNORECASE)

    def evaluate(
        self,
        user_input: str,
        context: Optional[Dict] = None
    ) -> ComplexityScore:
        """
        评估用户输入的复杂度

        Args:
            user_input: 用户描述的任务
            context: 可选的上下文信息
                - codebase_stats: 代码库统计
                - recent_changes: 最近的变更
                - user_history: 用户历史偏好

        Returns:
            ComplexityScore: 复杂度评分结果
        """
        context = context or {}
        reasoning = []

        # 1. 评估领域复杂度
        domain_score, domain_type = self._evaluate_domain(user_input)
        reasoning.append(f"领域评估: {domain_type} (分数: {domain_score})")

        # 2. 评估规模复杂度
        scale_score, scale_type = self._evaluate_scale(user_input, context)
        reasoning.append(f"规模评估: {scale_type} (分数: {scale_score})")

        # 3. 评估影响范围
        impact_score, impact_type = self._evaluate_impact(user_input, context)
        reasoning.append(f"影响评估: {impact_type} (分数: {impact_score})")

        # 计算总分
        total_score = domain_score + scale_score + impact_score

        # 4. 调整因素
        adjustments = self._apply_adjustments(user_input, context, total_score)
        if adjustments:
            total_score += adjustments["delta"]
            reasoning.extend(adjustments["reasons"])

        # 确定推荐路径
        recommended_path = self._determine_path(total_score, context)

        # 计算置信度
        confidence = self._calculate_confidence(
            user_input, domain_score, scale_score, impact_score
        )

        return ComplexityScore(
            total_score=total_score,
            domain_score=domain_score,
            scale_score=scale_score,
            impact_score=impact_score,
            domain_type=domain_type,
            scale_type=scale_type,
            impact_type=impact_type,
            recommended_path=recommended_path,
            confidence=confidence,
            reasoning=reasoning
        )

    def _evaluate_domain(self, user_input: str) -> Tuple[int, str]:
        """评估领域复杂度"""
        scores = {domain: 0 for domain in DomainComplexity}
        user_lower = user_input.lower()

        for domain, pattern in self.domain_patterns.items():
            matches = len(pattern.findall(user_input))
            scores[domain] = matches

        # 检查是否是明显简单的任务
        simple_indicators = ['typo', 'spell', '错别字', '拼写', '格式', 'format', '空格', 'space']
        if any(ind in user_lower for ind in simple_indicators):
            return DomainComplexity.SIMPLE.value, "simple"

        # 找出最高分的领域
        max_domain = max(scores, key=scores.get)
        max_score = scores[max_domain]

        if max_score == 0:
            # 没有匹配到关键词，检查输入长度
            if len(user_input.split()) <= 5:
                return DomainComplexity.SIMPLE.value, "simple"
            return DomainComplexity.MEDIUM.value, "medium"

        return max_domain.value, max_domain.name.lower()

    def _evaluate_scale(self, user_input: str, context: Dict) -> Tuple[int, str]:
        """评估规模复杂度"""
        user_lower = user_input.lower()

        # 检查是否是极小规模任务
        tiny_indicators = ['typo', 'spell', 'format', 'rename', '空格', '拼写']
        if any(ind in user_lower for ind in tiny_indicators):
            return ScaleComplexity.TINY.value, "tiny"

        # 检查显式的规模描述
        for scale_type, keywords in self.SCALE_KEYWORDS["lines"].items():
            for keyword in keywords:
                if keyword.lower() in user_lower:
                    return scale_type.value, scale_type.name.lower()

        # 基于代码库统计推断
        codebase_stats = context.get("codebase_stats", {})
        estimated_lines = codebase_stats.get("estimated_lines_changed", 0)

        if estimated_lines > 0:
            if estimated_lines < 50:
                return ScaleComplexity.TINY.value, "tiny"
            elif estimated_lines < 200:
                return ScaleComplexity.SMALL.value, "small"
            elif estimated_lines < 1000:
                return ScaleComplexity.MEDIUM.value, "medium"
            else:
                return ScaleComplexity.LARGE.value, "large"

        # 默认最小规模 (typo等小修改)
        words = len(user_input.split())
        if words <= 5:
            return ScaleComplexity.TINY.value, "tiny"

        return ScaleComplexity.SMALL.value, "small"

    def _evaluate_impact(self, user_input: str, context: Dict) -> Tuple[int, str]:
        """评估影响范围"""
        user_lower = user_input.lower()
        scores = {impact: 0 for impact in ImpactScope}

        # 明显的小修改，直接返回最小影响
        trivial_indicators = ['typo', 'spell', 'format', 'comment', 'doc']
        if any(ind in user_lower for ind in trivial_indicators):
            return ImpactScope.ISOLATED.value, "isolated"

        for impact, keywords in self.IMPACT_KEYWORDS.items():
            for keyword in keywords:
                if keyword.lower() in user_lower:
                    scores[impact] += 1

        max_impact = max(scores, key=scores.get)
        max_score = scores[max_impact]

        if max_score == 0:
            # 检查是否有破坏性变更关键词
            breaking_keywords = ["remove", "delete", "replace", "upgrade"]
            for kw in breaking_keywords:
                if kw in user_lower:
                    return ImpactScope.MODULE.value, "module"

            # 默认最小影响
            return ImpactScope.ISOLATED.value, "isolated"

        return max_impact.value, max_impact.name.lower()

    def _apply_adjustments(
        self,
        user_input: str,
        context: Dict,
        current_score: int
    ) -> Optional[Dict]:
        """应用调整因素"""
        adjustments = {"delta": 0, "reasons": []}

        # 1. 用户明确指定复杂度
        if any(kw in user_input.lower() for kw in ["简单", "quick", "fast", "easy"]):
            adjustments["delta"] -= 1
            adjustments["reasons"].append("用户明确表示简单任务 (-1)")

        if any(kw in user_input.lower() for kw in ["复杂", "difficult", "challenging", "大规模"]):
            adjustments["delta"] += 2
            adjustments["reasons"].append("用户明确表示复杂任务 (+2)")

        # 2. 跨领域指示
        domain_indicators = sum(1 for d in DomainComplexity if self._has_domain_keyword(user_input, d))
        if domain_indicators > 1:
            adjustments["delta"] += 1
            adjustments["reasons"].append("涉及多个技术领域 (+1)")

        # 3. 历史成功率调整 (如果 Lightning 数据可用)
        user_history = context.get("user_history", {})
        similar_tasks = user_history.get("similar_tasks", [])
        if similar_tasks:
            avg_success = sum(t["success"] for t in similar_tasks) / len(similar_tasks)
            if avg_success < 0.5:
                adjustments["delta"] += 1
                adjustments["reasons"].append(f"类似任务历史成功率低 ({avg_success:.1%}) (+1)")

        return adjustments if adjustments["delta"] != 0 else None

    def _has_domain_keyword(self, user_input: str, domain: DomainComplexity) -> bool:
        """检查是否包含某领域的关键词"""
        pattern = self.domain_patterns.get(domain)
        if pattern:
            return bool(pattern.search(user_input))
        return False

    def _determine_path(self, total_score: int, context: Dict) -> str:
        """根据总分确定推荐路径"""
        # 检查用户是否强制指定路径
        user_override = context.get("force_path")
        if user_override:
            return user_override

        # 根据分数推荐
        if total_score <= self.THRESHOLDS["quick_flow_max"]:
            return "quick"
        elif total_score >= self.THRESHOLDS["party_mode_min"]:
            return "party"
        else:
            return "full"

    def _calculate_confidence(
        self,
        user_input: str,
        domain_score: int,
        scale_score: int,
        impact_score: int
    ) -> float:
        """计算评估置信度"""
        # 基于输入长度和信息量
        confidence = 0.5

        # 输入越长，置信度越高 (最多 +0.2)
        words = len(user_input.split())
        confidence += min(words / 50, 0.2)

        # 匹配到关键词越多，置信度越高
        total_matches = domain_score + scale_score + impact_score
        confidence += min(total_matches / 10, 0.2)

        # 如果涉及多个维度，置信度更高
        dimensions_with_signal = sum([
            1 if domain_score > 0 else 0,
            1 if scale_score > 0 else 0,
            1 if impact_score > 0 else 0
        ])
        confidence += (dimensions_with_signal - 1) * 0.05

        return min(confidence, 1.0)

    def explain_decision(self, score: ComplexityScore) -> str:
        """生成决策解释文本"""
        explanation = f"""
## 复杂度评估报告

**总评分**: {score.total_score}/10

### 维度分析
| 维度 | 级别 | 分数 |
|------|------|------|
| 领域复杂度 | {score.domain_type} | {score.domain_score} |
| 规模复杂度 | {score.scale_type} | {score.scale_score} |
| 影响范围 | {score.impact_type} | {score.impact_score} |

### 评估理由
"""
        for reason in score.reasoning:
            explanation += f"- {reason}\n"

        explanation += f"""
### 推荐工作流
**{self._get_path_name(score.recommended_path)}**

置信度: {score.confidence:.0%}
"""
        return explanation

    def _get_path_name(self, path: str) -> str:
        """获取路径名称"""
        names = {
            "quick": "⚡ Quick Flow (快速流程)",
            "full": "🔍 Full Planning (完整规划)",
            "party": "🎉 Party Mode (多Agent协作)"
        }
        return names.get(path, "Unknown")


# 便捷函数
def evaluate_complexity(user_input: str, context: Optional[Dict] = None) -> ComplexityScore:
    """便捷函数：评估复杂度"""
    evaluator = ComplexityEvaluator()
    return evaluator.evaluate(user_input, context)
