"""
Skill Hub - Evaluation Engine
评估引擎：重复度检测、功能匹配、质量评分、安全扫描、决策引擎
融合 skill-curator 的评估标准
"""

import os
import re
import math
from typing import List, Optional, Tuple, Dict
from datetime import datetime, timedelta
from collections import Counter


def _score_by_thresholds(
    value: float,
    thresholds: List[Tuple[float, float]],
    max_score: float
) -> float:
    """根据阈值计算分数的辅助函数

    Args:
        value: 要评估的值
        thresholds: [(阈值, 分数), ...] 列表，按降序排列
        max_score: 最大分数限制

    Returns:
        计算出的分数

    Examples:
        >>> _score_by_thresholds(50, [(100, 10), (50, 8), (10, 5)], 10)
        8.0
        >>> _score_by_thresholds(5, [(100, 10), (50, 8), (10, 5)], 10)
        0.0
    """
    for threshold, score in thresholds:
        if value >= threshold:
            return min(score, max_score)
    return 0.0

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

from models import (
    SkillMetadata, PreEvaluationReport, SearchResult,
    OverlapDetails, QualityBreakdown, QualityReport,
    SecurityReport, RiskLevel, Recommendation,
    FunctionalMatchBreakdown, QualityAnchorReport
)


class SimilarityDetector:
    """相似度检测器"""

    def __init__(self):
        if HAS_SKLEARN:
            self.vectorizer = TfidfVectorizer(
                ngram_range=(1, 2),
                min_df=1,
                analyzer='word'
            )
        else:
            self.vectorizer = None

    def calculate_overlap(
        self, remote: SkillMetadata, local_skills: List[SkillMetadata]
    ) -> Tuple[float, Optional[SkillMetadata], OverlapDetails]:
        """计算与本地 skills 的重叠度

        返回: (最高重叠度, 最相似的skill, 详细信息)
        """
        if not local_skills:
            return 0.0, None, OverlapDetails()

        max_overlap = 0.0
        most_similar = None
        best_details = OverlapDetails()

        for local in local_skills:
            overlap, details = self._calculate_single(remote, local)
            if overlap > max_overlap:
                max_overlap = overlap
                most_similar = local
                best_details = details

        return max_overlap, most_similar, best_details

    def _calculate_single(
        self, remote: SkillMetadata, local: SkillMetadata
    ) -> Tuple[float, OverlapDetails]:
        """计算单个 skill 的相似度"""

        # 名称相似度 (15%)
        name_sim = self._name_similarity(remote.name, local.name)

        # 描述语义相似度 (35%)
        desc_sim = self._semantic_similarity(remote.description, local.description)

        # 触发词重叠度 (25%)
        trigger_sim = self._trigger_overlap(remote.triggers, local.triggers)

        # 文件结构相似度 (15%)
        struct_sim = self._structure_similarity(remote.file_list, local.file_list)

        # 标签重叠度 (10%)
        tag_sim = self._tag_overlap(remote.tags, local.tags)

        # 加权总分
        total = (
            name_sim * 0.15 +
            desc_sim * 0.35 +
            trigger_sim * 0.25 +
            struct_sim * 0.15 +
            tag_sim * 0.10
        )

        details = OverlapDetails(
            name=name_sim,
            description=desc_sim,
            triggers=trigger_sim,
            structure=struct_sim,
            tags=tag_sim,
        )

        return total, details

    def _name_similarity(self, name1: str, name2: str) -> float:
        """名称相似度（简单字符串匹配）"""
        if not name1 or not name2:
            return 0.0

        n1, n2 = name1.lower().strip(), name2.lower().strip()

        if n1 == n2:
            return 1.0

        # 检查包含关系
        if n1 in n2 or n2 in n1:
            return 0.7

        # 检查前缀/后缀
        if n1.split('-')[0] == n2.split('-')[0]:
            return 0.5

        return 0.0

    def _semantic_similarity(self, text1: str, text2: str) -> float:
        """语义相似度"""
        if not text1 or not text2:
            return 0.0

        if HAS_SKLEARN and self.vectorizer:
            try:
                vectors = self.vectorizer.fit_transform([text1, text2])
                return float(cosine_similarity(vectors[0:1], vectors[1:2])[0][0])
            except:
                pass

        # 简化版：词汇重叠
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())

        if not words1 or not words2:
            return 0.0

        intersection = len(words1 & words2)
        union = len(words1 | words2)

        return intersection / union if union > 0 else 0.0

    def _trigger_overlap(
        self, triggers1: Dict[str, List[str]], triggers2: Dict[str, List[str]]
    ) -> float:
        """触发词 Jaccard 相似度"""
        # 展平所有触发词
        flat1 = self._flatten_triggers(triggers1)
        flat2 = self._flatten_triggers(triggers2)

        if not flat1 or not flat2:
            return 0.0

        set1, set2 = set(flat1), set(flat2)
        intersection = len(set1 & set2)
        union = len(set1 | set2)

        return intersection / union if union > 0 else 0.0

    def _flatten_triggers(self, triggers: Dict[str, List[str]]) -> List[str]:
        """展平触发词字典"""
        result = []
        for lang, words in triggers.items():
            if isinstance(words, list):
                result.extend([w.lower().strip() for w in words])
            elif isinstance(words, str):
                result.append(words.lower().strip())
        return result

    def _structure_similarity(self, files1: List[str], files2: List[str]) -> float:
        """文件结构相似度"""
        if not files1 or not files2:
            return 0.0

        set1, set2 = set(files1), set(files2)
        intersection = len(set1 & set2)
        union = len(set1 | set2)

        return intersection / union if union > 0 else 0.0

    def _tag_overlap(self, tags1: List[str], tags2: List[str]) -> float:
        """标签重叠度"""
        if not tags1 or not tags2:
            return 0.0

        set1, set2 = set(t.lower() for t in tags1), set(t.lower() for t in tags2)
        intersection = len(set1 & set2)
        union = len(set1 | set2)

        return intersection / union if union > 0 else 0.0


class FunctionalMatcher:
    """功能匹配评估器 (skill-curator 30%权重)

    评估 Skill 是否满足用户的功能需求，包括：
    - 核心功能覆盖 (0-10分)
    - 边缘场景支持 (0-10分)
    - 扩展潜力 (0-10分)
    """

    def match(self, metadata: SkillMetadata, user_requirement: str) -> FunctionalMatchBreakdown:
        """评估功能匹配度"""
        breakdown = FunctionalMatchBreakdown()

        # 核心功能覆盖 (10分)
        breakdown.core_coverage = self._score_core_coverage(metadata, user_requirement)

        # 边缘场景支持 (10分)
        breakdown.edge_support = self._score_edge_support(metadata, user_requirement)

        # 扩展潜力 (10分)
        breakdown.extension_potential = self._score_extension_potential(metadata)

        return breakdown

    def _score_core_coverage(self, metadata: SkillMetadata, requirement: str) -> float:
        """核心功能覆盖评分 (0-10)"""
        score = 0.0

        # 提取需求关键词
        requirement_lower = requirement.lower()
        keywords = self._extract_keywords(requirement_lower)

        # 名称匹配 (4分)
        if any(kw in metadata.name.lower() for kw in keywords):
            score += 4
        elif any(kw in metadata.description.lower() for kw in keywords):
            score += 2

        # 描述深度 (3分)
        desc = metadata.description.lower()
        if len(desc) > 200 and any(kw in desc for kw in keywords):
            score += 3
        elif len(desc) > 100 and any(kw in desc for kw in keywords):
            score += 2

        # 触发词相关性 (3分)
        trigger_relevance = 0
        for lang, triggers in metadata.triggers.items():
            if isinstance(triggers, list):
                for trigger in triggers:
                    if any(kw in trigger.lower() for kw in keywords):
                        trigger_relevance += 1
        if trigger_relevance >= 3:
            score += 3
        elif trigger_relevance >= 1:
            score += 1.5

        return min(score, 10.0)

    def _score_edge_support(self, metadata: SkillMetadata, requirement: str) -> float:
        """边缘场景支持评分 (0-10)"""
        score = 0.0

        # 文件结构复杂度 (3分) - 更多的文件通常意味着更完善的功能
        if len(metadata.file_list) > 10:
            score += 3
        elif len(metadata.file_list) > 5:
            score += 2

        # 有示例文件 (2分)
        has_examples = any('example' in f.lower() for f in metadata.file_list)
        if has_examples:
            score += 2

        # 有参考文件 (1分)
        has_references = any('reference' in f.lower() for f in metadata.file_list)
        if has_references:
            score += 1

        # 有测试文件 (2分)
        has_tests = any('test' in f.lower() for f in metadata.file_list)
        if has_tests:
            score += 2

        # README 中提到边缘场景 (2分)
        readme_lower = metadata.readme_content.lower()
        edge_keywords = ['edge case', 'boundary', 'exception', 'error handling', 'fallback']
        if any(kw in readme_lower for kw in edge_keywords):
            score += 2

        return min(score, 10.0)

    def _score_extension_potential(self, metadata: SkillMetadata) -> float:
        """扩展潜力评分 (0-10)"""
        score = 0.0

        # 模块化设计 (3分)
        has_multiple_files = len(metadata.file_list) > 3
        if has_multiple_files:
            score += 3

        # 有配置文件 (2分)
        has_config = any('config' in f.lower() or 'setting' in f.lower() for f in metadata.file_list)
        if has_config:
            score += 2

        # 文档提到扩展性 (2分)
        readme_lower = metadata.readme_content.lower()
        ext_keywords = ['extensible', 'customizable', 'plugin', 'modular', 'extend']
        if any(kw in readme_lower for kw in ext_keywords):
            score += 2

        # 依赖合理 (不过度也不过少) (1分)
        dep_count = len(metadata.dependencies)
        if 0 < dep_count <= 5:
            score += 1

        # 有版本信息/更新历史 (2分)
        if metadata.github_stats and metadata.github_stats.last_commit:
            score += 2

        return min(score, 10.0)

    def _extract_keywords(self, text: str) -> List[str]:
        """从文本中提取关键词"""
        # 简单的关键词提取（可改进为更复杂的NLP）
        words = re.findall(r'\b\w+\b', text)

        # 过滤常见停用词
        stopwords = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
            'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'could', 'should', 'may', 'might', 'must', 'shall', 'can',
            'need', 'want', 'use', 'get', 'make', 'take', 'give', 'help', 'show'
        }

        keywords = [w for w in words if w.lower() not in stopwords and len(w) > 2]
        return keywords[:10]  # 返回前10个关键词


class QualityAnchorChecker:
    """质量锚点检查器 (MindSymphony 质量标准)

    检查 Skill 是否符合 MindSymphony 的核心质量原则：
    - 意图对齐
    - 调性一致
    - 边界清晰
    - 差异化价值
    """

    MINDSYMPHONY_ANTI_PATTERNS = {
        # 创意设计反模式
        '泛滥的AI审美': ['inter', 'roboto', '紫色渐变', '圆角卡片'],
        # 学术写作反模式
        '学术陈词滥调': ['众所周知', '具有重要意义', '有待进一步研究'],
        # 技术文档反模式
        '过度抽象': ['具体实现略', '显而易见', '留给读者'],
        # 品牌策略反模式
        '流行词汇堆砌': ['颠覆性', '范式转移', '革命性', 'game-changing'],
    }

    def check(self, metadata: SkillMetadata) -> QualityAnchorReport:
        """执行质量锚点检查"""
        report = QualityAnchorReport()

        # 必要检查（硬性条件）
        self._check_hard_requirements(metadata, report)

        # 质量原则检查
        self._check_quality_principles(metadata, report)

        # 反模式检测
        self._detect_anti_patterns(metadata, report)

        # 计算是否通过
        report.passed = (
            not report.critical_issues and
            sum(report.checks.values()) >= len(report.checks) * 0.7
        )

        return report

    def _check_hard_requirements(self, metadata: SkillMetadata, report: QualityAnchorReport):
        """检查硬性条件"""
        # 1. 有 SKILL.md 或 README
        has_skill_md = any('skill.md' in f.lower() for f in metadata.file_list)
        has_readme = any('readme' in f.lower() for f in metadata.file_list)
        report.add_check("有说明文档", has_skill_md or has_readme)
        if not (has_skill_md or has_readme):
            report.add_critical("缺少说明文档 (SKILL.md 或 README)")

        # 2. 有描述
        report.add_check("有功能描述", len(metadata.description) > 20)
        if len(metadata.description) <= 20:
            report.add_critical("功能描述过短或缺失")

        # 3. 有触发词
        has_triggers = bool(metadata.triggers)
        report.add_check("有触发词", has_triggers)
        if not has_triggers:
            report.add_warning("缺少触发词定义")

        # 4. 许可证允许使用
        has_license = metadata.github_stats and metadata.github_stats.license
        report.add_check("有许可证", has_license is not None)
        if has_license and has_license.lower() in ['proprietary', 'commercial']:
            report.add_warning(f"许可证可能限制使用: {has_license}")

    def _check_quality_principles(self, metadata: SkillMetadata, report: QualityAnchorReport):
        """检查质量原则"""
        readme = metadata.readme_content.lower()

        # 意图对齐：是否有明确的目的说明
        has_purpose = any(word in readme for word in ['purpose', 'goal', 'objective', '目的', '目标', '用途'])
        report.add_check("目的明确", has_purpose)

        # 调性一致：是否有统一的风格
        has_examples = 'example' in readme or '示例' in readme
        report.add_check("有使用示例", has_examples)

        # 边界清晰：是否说明了适用范围
        has_boundaries = any(word in readme for word in ['limit', 'scope', 'boundary', '限制', '范围', '边界'])
        report.add_check("边界清晰", has_boundaries)

        # 差异化价值：是否说明了独特价值
        has_differentiation = any(word in readme for word in ['unique', 'different', 'special', '独特', '特色', '优势'])
        report.add_check("差异化价值", has_differentiation)

    def _detect_anti_patterns(self, metadata: SkillMetadata, report: QualityAnchorReport):
        """检测 MindSymphony 反模式"""
        readme = metadata.readme_content.lower()
        description = metadata.description.lower()

        for pattern_name, keywords in self.MINDSYMPHONY_ANTI_PATTERNS.items():
            for keyword in keywords:
                if keyword.lower() in readme or keyword.lower() in description:
                    report.add_warning(f"可能包含 {pattern_name} 反模式: '{keyword}'")


class QualityScorer:
    """质量评分器"""

    def score(self, metadata: SkillMetadata) -> QualityReport:
        """对 skill 进行质量评分 (0-100)"""
        breakdown = QualityBreakdown()

        # 文档完整性 (25分)
        breakdown.documentation = self._score_documentation(metadata)

        # 社区验证 (25分)
        breakdown.community = self._score_community_validation(metadata)

        # 维护活跃度 (20分)
        breakdown.maintenance = self._score_maintenance(metadata)

        # 代码健康度 (15分)
        breakdown.code_health = self._score_code_health(metadata)

        # 兼容性 (15分)
        breakdown.compatibility = self._score_compatibility(metadata)

        return QualityReport(
            score=breakdown.total,
            breakdown=breakdown,
        )

    def _score_documentation(self, metadata: SkillMetadata) -> float:
        """文档完整性评分 (0-25)"""
        score = 0.0

        # 必需文件 (10分)
        has_skill_md = any('skill.md' in f.lower() for f in metadata.file_list)
        has_readme = any('readme' in f.lower() for f in metadata.file_list)
        score += (has_skill_md * 5) + (has_readme * 5)

        # Frontmatter 完整性 (8分)
        if metadata.frontmatter:
            required_fields = ['name', 'description', 'triggers']
            present = sum(1 for f in required_fields if f in metadata.frontmatter)
            score += (present / len(required_fields)) * 8

        # 描述质量 (7分)
        desc_len = len(metadata.description)
        if desc_len > 500:
            score += 7
        elif desc_len > 200:
            score += 5
        elif desc_len > 50:
            score += 3

        return min(score, 25.0)

    def _score_community_validation(self, metadata: SkillMetadata) -> float:
        """社区验证评分 (0-25)"""
        score = 0.0

        # Stars/Forks (15分) - 使用辅助函数简化
        if metadata.github_stats:
            stars = metadata.github_stats.stars
            score += _score_by_thresholds(
                stars,
                [(100, 15), (50, 12), (10, 8), (0, 4)],
                15
            )

        # 用户评分 (10分)
        if metadata.user_rating:
            score += (metadata.user_rating / 5) * 10

        return min(score, 25.0)

    def _score_maintenance(self, metadata: SkillMetadata) -> float:
        """维护活跃度评分 (0-20)"""
        if not metadata.github_stats or not metadata.github_stats.last_commit:
            return 0.0

        # 最近更新时间 (12分) - 越新分数越高
        days_since = (datetime.now() - metadata.github_stats.last_commit).days
        freshness_thresholds = [
            (7, 12),   # 7天内
            (30, 10),  # 30天内
            (90, 7),   # 90天内
            (180, 4),  # 180天内
            (365, 2),  # 1年内
        ]
        freshness_score = 0
        for threshold, score in freshness_thresholds:
            if days_since <= threshold:
                freshness_score = score
                break

        # 提交频率/活跃度 (8分)
        activity_score = 4 if metadata.github_stats.stars > 0 else 0

        return min(freshness_score + activity_score, 20.0)

    def _score_code_health(self, metadata: SkillMetadata) -> float:
        """代码健康度评分 (0-15)"""
        # 依赖数量 (5分) - 使用辅助函数（反向：越少越好）
        dep_count = len(metadata.dependencies)
        dep_score = _score_by_thresholds(
            10 - dep_count,  # 反转：依赖越少分数越高
            [(10, 5), (7, 4), (5, 3), (0, 1)],
            5
        )

        # 文件结构 (5分)
        file_score = 0
        if metadata.file_list:
            has_references = any('reference' in f.lower() for f in metadata.file_list)
            has_examples = any('example' in f.lower() for f in metadata.file_list)
            has_tests = any('test' in f.lower() for f in metadata.file_list)
            file_score = sum([has_references, has_examples, has_tests]) * (5/3)

        # License (5分)
        license_score = 5 if metadata.github_stats and metadata.github_stats.license else 0

        return min(dep_score + file_score + license_score, 15.0)

    def _score_compatibility(self, metadata: SkillMetadata) -> float:
        """兼容性评分 (0-15)"""
        score = 0.0

        # Frontmatter 格式 (8分)
        if metadata.frontmatter:
            ms_fields = ['name', 'description', 'type', 'triggers']
            present = sum(1 for f in ms_fields if f in metadata.frontmatter)
            score += (present / len(ms_fields)) * 8

        # 触发词格式 (4分)
        if metadata.triggers:
            if isinstance(metadata.triggers, dict):
                if 'zh' in metadata.triggers or 'en' in metadata.triggers:
                    score += 4
                else:
                    score += 2
            elif isinstance(metadata.triggers, list):
                score += 2

        # 命名规范 (3分)
        if metadata.name and re.match(r'^[a-z][a-z0-9-]*$', metadata.name):
            score += 3

        return min(score, 15.0)


class SecurityPreScanner:
    """安全预扫描器"""

    SUSPICIOUS_FILES = [
        'eval', 'exec', 'system', 'shell',
        'hack', 'crack', 'bypass', 'inject'
    ]

    RISK_PATTERNS = [
        'ignore instructions',
        'override prompt',
        'bypass security',
        'execute arbitrary',
        'reverse shell',
    ]

    def scan(self, metadata: SkillMetadata) -> SecurityReport:
        """安全预扫描"""
        report = SecurityReport()

        # 来源检查
        if metadata.source.value == "unknown":
            report.add_warning("来自未知来源", RiskLevel.MEDIUM)

        # 文件名检查
        for fname in metadata.file_list:
            if any(s in fname.lower() for s in self.SUSPICIOUS_FILES):
                report.add_warning(f"可疑文件: {fname}", RiskLevel.HIGH)

        # README 风险模式检查
        if metadata.readme_content:
            readme_lower = metadata.readme_content.lower()
            for pattern in self.RISK_PATTERNS:
                if pattern in readme_lower:
                    report.add_warning(f"README 包含风险模式: {pattern}", RiskLevel.HIGH)

        # 依赖检查
        if metadata.dependencies:
            risky_deps = ['request', 'urllib']  # 示例
            for dep in metadata.dependencies:
                if any(r in dep.lower() for r in risky_deps):
                    report.add_warning(f"依赖可能存在风险: {dep}", RiskLevel.MEDIUM)

        return report


class DecisionEngine:
    """决策引擎（融合 skill-curator 标准）"""

    def decide(
        self,
        overlap_score: float,
        quality_score: float,
        security_risk: RiskLevel,
        functional_score: float = 0.0,  # 新增：功能匹配度
        quality_anchors_passed: bool = True,  # 新增：质量锚点是否通过
        config_overlap_threshold: float = 0.8,
        config_quality_threshold: float = 60.0
    ) -> Recommendation:
        """做出决策

        融合 skill-curator 的评估维度：
        - 功能匹配度 (30%权重) - 新增
        - 质量锚点检查 - 新增
        """

        # 安全一票否决
        if security_risk == RiskLevel.HIGH:
            return Recommendation.REJECT

        # 质量锚点不通过，需要人工审查
        if not quality_anchors_passed:
            if functional_score >= 20 and quality_score >= config_quality_threshold:
                return Recommendation.ADAPT  # 质量好但需适配 MindSymphony 格式
            else:
                return Recommendation.INSPECT

        # 功能匹配度太低，跳过
        if functional_score > 0 and functional_score < 10:
            return Recommendation.SKIP

        # 高重复度
        if overlap_score >= config_overlap_threshold:
            if quality_score > config_quality_threshold * 1.2:  # 质量明显更好
                return Recommendation.ABSORB
            else:
                return Recommendation.SKIP

        # 中等重复度
        elif overlap_score >= config_overlap_threshold * 0.6:
            return Recommendation.ENHANCE

        # 低重复度
        else:
            # 融合 skill-curator：功能匹配度是关键决策因素
            if functional_score >= 20:  # 功能匹配度高
                if quality_score >= config_quality_threshold:
                    return Recommendation.ADOPT
                else:
                    return Recommendation.ADAPT  # 需要适配
            elif functional_score >= 10:  # 功能匹配度中等
                if quality_score >= config_quality_threshold * 0.8:
                    return Recommendation.ADOPT
                else:
                    return Recommendation.INSPECT
            else:  # 功能匹配度低或未评估
                if quality_score >= config_quality_threshold:
                    return Recommendation.ADOPT
                else:
                    return Recommendation.INSPECT


class EvaluationEngine:
    """综合评估引擎（融合 skill-curator 标准）"""

    def __init__(self, config=None):
        self.similarity_detector = SimilarityDetector()
        self.functional_matcher = FunctionalMatcher()  # 新增：功能匹配评估器
        self.quality_scorer = QualityScorer()
        self.security_scanner = SecurityPreScanner()
        self.quality_anchor_checker = QualityAnchorChecker()  # 新增：质量锚点检查器
        self.decision_engine = DecisionEngine()
        self.config = config

    async def evaluate(
        self,
        remote: SkillMetadata,
        local_skills: List[SkillMetadata],
        user_requirement: str = ""
    ) -> PreEvaluationReport:
        """综合评估一个 skill

        Args:
            remote: 远程 skill 元数据
            local_skills: 本地 skills 列表（用于重复度检测）
            user_requirement: 用户需求描述（用于功能匹配评估）
        """

        report = PreEvaluationReport(
            skill_name=remote.name,
            source=remote.source,
            metadata=remote,
            user_requirement=user_requirement
        )

        # 1. 重复度检测
        overlap_score, most_similar, overlap_details = self.similarity_detector.calculate_overlap(
            remote, local_skills
        )
        report.overlap.score = overlap_score
        report.overlap.most_similar = most_similar.name if most_similar else None
        report.overlap.details = overlap_details

        # 2. 功能匹配度评估 (skill-curator 30%权重)
        if user_requirement:
            report.functional_match = self.functional_matcher.match(remote, user_requirement)

        # 3. 质量评分
        report.quality = self.quality_scorer.score(remote)

        # 4. 安全扫描
        report.security = self.security_scanner.scan(remote)

        # 5. 质量锚点检查 (MindSymphony 标准)
        report.quality_anchors = self.quality_anchor_checker.check(remote)

        # 6. 决策（考虑功能匹配度）
        overlap_threshold = self.config.evaluation.overlap_threshold if self.config else 0.8
        quality_threshold = self.config.evaluation.quality_threshold * 100 if self.config else 60.0

        # 计算综合评分（考虑功能匹配）
        functional_score = report.functional_match.total if report.functional_match else 0
        adjusted_quality_score = self._adjust_quality_for_functional_match(
            report.quality.score, functional_score
        )

        report.recommendation = self.decision_engine.decide(
            overlap_score=overlap_score,
            quality_score=adjusted_quality_score,
            functional_score=functional_score,  # 新增参数
            security_risk=report.security.risk_level,
            quality_anchors_passed=report.quality_anchors.passed,  # 新增参数
            config_overlap_threshold=overlap_threshold,
            config_quality_threshold=quality_threshold
        )

        # 计算置信度
        report.confidence = self._calculate_confidence(report)

        # 生成理由
        report.reason = self._generate_reason(report)

        return report

    def _adjust_quality_for_functional_match(self, quality_score: float, functional_score: float) -> float:
        """根据功能匹配度调整质量分数"""
        # 功能匹配度是 skill-curator 的核心维度 (30%权重)
        # 如果功能匹配度低，即使质量分数高也应该降低综合评分
        if functional_score < 10:  # 功能匹配度不足 1/3
            return quality_score * 0.7
        elif functional_score < 20:  # 功能匹配度不足 2/3
            return quality_score * 0.85
        else:
            return quality_score

    def _calculate_confidence(self, report: PreEvaluationReport) -> float:
        """计算决策置信度"""
        confidence = 0.5  # 基础置信度

        # 质量分数越高，置信度越高
        confidence += (report.quality.score / 100) * 0.3

        # 重复度越清晰，置信度越高
        if report.overlap.score > 0.8 or report.overlap.score < 0.3:
            confidence += 0.1

        # 安全风险越低，置信度越高
        if report.security.risk_level == RiskLevel.LOW:
            confidence += 0.1

        return min(confidence, 1.0)

    def _generate_reason(self, report: PreEvaluationReport) -> str:
        """生成决策理由"""
        reasons = {
            Recommendation.ADOPT: "质量合格，与本地 skills 无明显重复",
            Recommendation.ADAPT: "质量良好，需要适配 MindSymphony 格式",
            Recommendation.ABSORB: f"与现有 skill 重复 {report.overlap.score*100:.0f}%，但质量更高",
            Recommendation.SKIP: f"与现有 skill 重复 {report.overlap.score*100:.0f}%，且质量不如本地",
            Recommendation.REJECT: "安全风险过高",
            Recommendation.ENHANCE: f"与现有 skill 有 {report.overlap.score*100:.0f}% 重叠，可作为补充增强",
            Recommendation.INSPECT: "质量较低，建议人工审查",
        }
        return reasons.get(report.recommendation, "")
