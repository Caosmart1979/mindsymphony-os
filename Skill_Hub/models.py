"""
Skill Hub - Core Data Models
定义所有数据结构
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Literal
from datetime import datetime
from enum import Enum


class SourceType(Enum):
    """数据源类型"""
    SKILLSLM = "skillslm"
    FORTY_TWO_PLUGIN = "42plugin"
    GITHUB = "github"
    LOCAL = "local"


class RiskLevel(Enum):
    """安全风险等级"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class Recommendation(Enum):
    """推荐操作"""
    ADOPT = "ADOPT"       # 直接使用
    ADAPT = "ADAPT"       # 改造适配
    ABSORB = "ABSORB"     # 增强吸收
    SKIP = "SKIP"         # 跳过
    REJECT = "REJECT"     # 拒绝
    INSPECT = "INSPECT"   # 人工审查


@dataclass
class GitHubStats:
    """GitHub 统计信息"""
    stars: int = 0
    forks: int = 0
    watchers: int = 0
    last_commit: Optional[datetime] = None
    commit_frequency: float = 0.0  # 每月提交数
    open_issues: int = 0
    license: Optional[str] = None


@dataclass
class QualityBreakdown:
    """质量评分细分"""
    documentation: float = 0.0   # 文档完整性 (0-25)
    community: float = 0.0       # 社区验证 (0-25)
    maintenance: float = 0.0     # 维护活跃度 (0-20)
    code_health: float = 0.0     # 代码健康度 (0-15)
    compatibility: float = 0.0   # 兼容性 (0-15)

    @property
    def total(self) -> float:
        return (
            self.documentation * 0.25 +
            self.community * 0.25 +
            self.maintenance * 0.20 +
            self.code_health * 0.15 +
            self.compatibility * 0.15
        )


@dataclass
class FunctionalMatchBreakdown:
    """功能匹配度细分 (skill-curator 30%权重)"""
    core_coverage: float = 0.0   # 核心功能覆盖 (0-10)
    edge_support: float = 0.0     # 边缘场景支持 (0-10)
    extension_potential: float = 0.0  # 扩展潜力 (0-10)

    @property
    def total(self) -> float:
        return self.core_coverage + self.edge_support + self.extension_potential


@dataclass
class QualityAnchorReport:
    """质量锚点检查报告 (MindSymphony 质量标准)"""
    passed: bool = False
    checks: Dict[str, bool] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    critical_issues: List[str] = field(default_factory=list)

    def add_check(self, name: str, passed: bool):
        self.checks[name] = passed

    def add_warning(self, warning: str):
        self.warnings.append(warning)

    def add_critical(self, issue: str):
        self.critical_issues.append(issue)


@dataclass
class OverlapDetails:
    """重叠度细分"""
    name: float = 0.0
    description: float = 0.0
    triggers: float = 0.0
    structure: float = 0.0
    tags: float = 0.0


@dataclass
class SkillMetadata:
    """Skill 元数据（远程获取，不下载本体）"""
    # 基础信息
    name: str
    source: SourceType
    description: str = ""
    author: str = ""
    url: str = ""
    repo_url: str = ""

    # 内容指纹（用于重复度检测）
    triggers: Dict[str, List[str]] = field(default_factory=dict)  # {zh: [...], en: [...]}
    tags: List[str] = field(default_factory=list)
    file_list: List[str] = field(default_factory=list)

    # Frontmatter
    frontmatter: Dict = field(default_factory=dict)

    # GitHub 统计
    github_stats: Optional[GitHubStats] = None

    # 用户评分 (42plugin)
    user_rating: Optional[float] = None  # 0-5
    download_count: int = 0

    # 依赖
    dependencies: List[str] = field(default_factory=list)

    # README 内容预览
    readme_content: str = ""

    # 缓存时间
    cached_at: Optional[datetime] = None


@dataclass
class SecurityReport:
    """安全扫描报告"""
    risk_level: RiskLevel = RiskLevel.LOW
    warnings: List[str] = field(default_factory=list)

    def add_warning(self, warning: str, level: RiskLevel = RiskLevel.MEDIUM):
        """添加警告"""
        self.warnings.append(warning)
        # 更新风险等级（取最高）
        if level.value == "HIGH" or self.risk_level.value == "LOW":
            self.risk_level = level


@dataclass
class QualityReport:
    """质量评分报告"""
    score: float = 0.0
    breakdown: QualityBreakdown = field(default_factory=QualityBreakdown)
    notes: List[str] = field(default_factory=list)


@dataclass
class OverlapReport:
    """重叠度报告"""
    score: float = 0.0
    most_similar: Optional[str] = None
    details: OverlapDetails = field(default_factory=OverlapDetails)


@dataclass
class PreEvaluationReport:
    """完整预评估报告"""
    skill_name: str
    source: SourceType

    # 相似性分析
    overlap: OverlapReport = field(default_factory=OverlapReport)

    # 功能匹配度 (skill-curator 30%权重)
    functional_match: Optional[FunctionalMatchBreakdown] = None

    # 质量评分
    quality: QualityReport = field(default_factory=QualityReport)

    # 安全评估
    security: SecurityReport = field(default_factory=SecurityReport)

    # 质量锚点检查 (MindSymphony 标准)
    quality_anchors: Optional[QualityAnchorReport] = None

    # 最终建议
    recommendation: Recommendation = Recommendation.INSPECT
    confidence: float = 0.5
    reason: str = ""

    # 元数据引用
    metadata: Optional[SkillMetadata] = None

    # 用户需求描述（用于功能匹配）
    user_requirement: str = ""

    def display(self) -> str:
        """终端友好的报告输出"""
        risk_icons = {"LOW": "✅", "MEDIUM": "⚠️", "HIGH": "🚨"}
        rec_icons = {
            "ADOPT": "✅",
            "ADAPT": "🔧",
            "ABSORB": "🔄",
            "SKIP": "⏭️",
            "REJECT": "🚫",
            "INSPECT": "👀"
        }

        lines = [
            "=" * 60,
            f"📊 预评估报告: {self.skill_name}",
            "=" * 60,
            "",
            f"📍 来源: {self.source.value}",
            "",
        ]

        # 重叠度分析
        lines.extend([
            "🔍 重复度分析:",
            f"   最相似的本地 skill: {self.overlap.most_similar or '无'}",
            f"   重叠度: {self.overlap.score * 100:.0f}%",
        ])
        if self.overlap.details:
            d = self.overlap.details
            lines.extend([
                f"   ├─ 名称相似: {d.name * 100:.0f}%",
                f"   ├─ 描述相似: {d.description * 100:.0f}%",
                f"   ├─ 触发词重叠: {d.triggers * 100:.0f}%",
                f"   └─ 结构相似: {d.structure * 100:.0f}%",
            ])
        lines.append("")

        # 功能匹配度 (skill-curator 30%权重)
        if self.functional_match:
            fm = self.functional_match
            lines.extend([
                "🎯 功能匹配度 (skill-curator):",
                f"   总分: {fm.total:.1f}/30",
                f"   ├─ 核心功能覆盖: {fm.core_coverage:.1f}/10",
                f"   ├─ 边缘场景支持: {fm.edge_support:.1f}/10",
                f"   └─ 扩展潜力: {fm.extension_potential:.1f}/10",
                ""
            ])

        # 质量评分
        b = self.quality.breakdown
        lines.extend([
            f"⭐ 质量评分: {self.quality.score:.1f}/100",
            f"   ├─ 文档完整性: {b.documentation:.1f}/25",
            f"   ├─ 社区验证: {b.community:.1f}/25",
            f"   ├─ 维护活跃度: {b.maintenance:.1f}/20",
            f"   ├─ 代码健康度: {b.code_health:.1f}/15",
            f"   └─ 兼容性: {b.compatibility:.1f}/15",
            ""
        ])

        # 安全评估
        risk_icon = risk_icons.get(self.security.risk_level.value, "❓")
        lines.extend([
            f"🛡️ 安全评估: {risk_icon} {self.security.risk_level.value}"
        ])
        if self.security.warnings:
            for w in self.security.warnings:
                lines.append(f"   ⚠️  {w}")
        else:
            lines.append("   无安全风险")
        lines.append("")

        # 质量锚点检查 (MindSymphony 标准)
        if self.quality_anchors:
            anchor_icon = "✅" if self.quality_anchors.passed else "⚠️"
            lines.extend([
                f"📐 质量锚点: {anchor_icon} {'通过' if self.quality_anchors.passed else '未完全通过'}",
            ])
            if self.quality_anchors.critical_issues:
                lines.append("   🚨 关键问题:")
                for issue in self.quality_anchors.critical_issues:
                    lines.append(f"      - {issue}")
            if self.quality_anchors.warnings:
                lines.append("   ⚠️  警告:")
                for warning in self.quality_anchors.warnings:
                    lines.append(f"      - {warning}")
            lines.append("")

        # 最终建议
        rec_icon = rec_icons.get(self.recommendation.value, "❓")
        lines.extend([
            "=" * 60,
            f"💡 建议: {rec_icon} {self.recommendation.value}",
            f"📝 理由: {self.reason}",
            f"📊 置信度: {self.confidence * 100:.0f}%",
            "=" * 60,
        ])

        return "\n".join(lines)


@dataclass
class SearchResult:
    """搜索结果项"""
    name: str
    source: SourceType
    description: str
    url: str
    metadata: Optional[SkillMetadata] = None

    # 预评估结果（如果已评估）
    evaluation: Optional[PreEvaluationReport] = None
