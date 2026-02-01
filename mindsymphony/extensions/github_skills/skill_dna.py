"""
Skill DNA System
个人技能DNA - 追踪用户专长、偏好和演化

功能:
- 用户画像建模
- GitHub行为分析
- 技能使用模式识别
- 个性化推荐
"""

import json
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path
from collections import defaultdict


@dataclass
class UserProfile:
    """用户画像"""
    user_id: str
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    # 专长领域 (domain -> proficiency 0-1)
    expertise_domains: Dict[str, float] = field(default_factory=dict)

    # 偏好模式
    preferred_patterns: List[str] = field(default_factory=list)

    # 技能偏好
    skill_preferences: Dict[str, Any] = field(default_factory=lambda: {
        'complexity': 'balanced',  # simple/detailed/balanced
        'style': 'pragmatic',      # academic/pragmatic/creative
        'depth': 'moderate'        # quick/moderate/thorough
    })

    # GitHub数据源
    github_sources: Dict[str, List[str]] = field(default_factory=lambda: {
        'starred_repos': [],
        'contributed_repos': [],
        'frequent_refs': [],
        'code_snippets': []
    })

    # 学习历史
    learning_history: List[Dict] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> 'UserProfile':
        return cls(**data)


@dataclass
class SkillUsagePattern:
    """技能使用模式"""
    skill_id: str
    skill_name: str
    first_used: str
    last_used: str
    use_count: int = 0
    success_count: int = 0
    avg_success_rate: float = 0.0
    context_tags: List[str] = field(default_factory=list)


class SkillDNA:
    """
    个人技能DNA系统

    追踪用户的技能专长、使用模式和学习偏好
    """

    def __init__(self, user_id: str, storage_dir: Optional[str] = None):
        """
        初始化技能DNA

        Args:
            user_id: 用户ID
            storage_dir: 存储目录
        """
        self.user_id = user_id
        self.storage_dir = Path(storage_dir or f'~/.mindsymphony/skill_dna/{user_id}')
        self.storage_dir = Path(self.storage_dir).expanduser()
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        # 加载或创建用户画像
        self.profile = self._load_profile()

        # 技能使用模式
        self.usage_patterns: Dict[str, SkillUsagePattern] = {}
        self._load_usage_patterns()

    def analyze_github_profile(self, github_username: str) -> Dict:
        """
        分析GitHub用户档案

        提取starred repos、贡献历史等

        Args:
            github_username: GitHub用户名

        Returns:
            分析结果
        """
        print(f"🔍 分析GitHub档案: {github_username}")

        # 模拟GitHub分析 (实际实现会调用GitHub API)
        analysis = {
            'starred_repos': [
                'microsoft/TypeScript',
                'facebook/react',
                'bmad-code-org/BMAD-METHOD'
            ],
            'top_languages': ['Python', 'TypeScript', 'JavaScript'],
            'interests': ['architecture', 'methodology', 'AI'],
            'contributions': 150
        }

        # 更新用户画像
        self._update_from_github_analysis(analysis)

        return analysis

    def record_skill_usage(
        self,
        skill_id: str,
        skill_name: str,
        success: bool,
        context: Optional[Dict] = None
    ):
        """
        记录技能使用情况

        Args:
            skill_id: 技能ID
            skill_name: 技能名称
            success: 是否成功
            context: 上下文信息
        """
        context = context or {}
        now = datetime.now().isoformat()

        if skill_id not in self.usage_patterns:
            self.usage_patterns[skill_id] = SkillUsagePattern(
                skill_id=skill_id,
                skill_name=skill_name,
                first_used=now,
                last_used=now,
                use_count=0,
                success_count=0,
                context_tags=context.get('tags', [])
            )

        pattern = self.usage_patterns[skill_id]
        pattern.last_used = now
        pattern.use_count += 1

        if success:
            pattern.success_count += 1

        # 更新成功率
        pattern.avg_success_rate = pattern.success_count / pattern.use_count

        # 添加上下文标签
        for tag in context.get('tags', []):
            if tag not in pattern.context_tags:
                pattern.context_tags.append(tag)

        self._save_usage_patterns()

        # 更新专长领域
        self._update_expertise_from_usage(skill_id, success)

    def get_expertise_report(self) -> Dict:
        """
        生成专长报告

        Returns:
            专长领域分析报告
        """
        report = {
            'user_id': self.user_id,
            'generated_at': datetime.now().isoformat(),
            'expertise_domains': self.profile.expertise_domains,
            'top_skills': self._get_top_skills(10),
            'learning_velocity': self._calculate_learning_velocity(),
            'skill_diversity': len(self.usage_patterns),
            'success_rate': self._calculate_overall_success_rate()
        }

        return report

    def recommend_learning_path(
        self,
        target_domain: str,
        current_skills: Optional[List[str]] = None
    ) -> List[Dict]:
        """
        推荐学习路径

        Args:
            target_domain: 目标领域
            current_skills: 当前技能列表

        Returns:
            推荐的学习路径
        """
        current_skills = current_skills or []

        # 基于目标领域和当前专长推荐
        recommendations = []

        # 1. 基础技能 (如果专长分数低)
        if self.profile.expertise_domains.get(target_domain, 0) < 0.3:
            recommendations.append({
                'type': 'foundation',
                'name': f'{target_domain}-fundamentals',
                'priority': 'high',
                'reason': '需要先掌握基础知识'
            })

        # 2. 进阶技能
        if 0.3 <= self.profile.expertise_domains.get(target_domain, 0) < 0.7:
            recommendations.append({
                'type': 'advanced',
                'name': f'{target_domain}-patterns',
                'priority': 'medium',
                'reason': '可以学习高级模式'
            })

        # 3. 相关领域
        related_domains = self._find_related_domains(target_domain)
        for domain in related_domains[:2]:
            recommendations.append({
                'type': 'related',
                'name': f'{domain}-integration',
                'priority': 'low',
                'reason': f'扩展相关领域: {domain}'
            })

        return recommendations

    def detect_skill_gaps(self, required_skills: List[str]) -> List[str]:
        """
        检测技能缺口

        Args:
            required_skills: 需要的技能列表

        Returns:
            缺失的技能列表
        """
        gaps = []

        for skill in required_skills:
            # 检查是否已有此技能
            found = False
            for pattern in self.usage_patterns.values():
                if pattern.skill_name.lower() == skill.lower():
                    # 检查熟练度
                    if pattern.avg_success_rate < 0.5:
                        gaps.append(f'{skill} (需要提高熟练度)')
                    found = True
                    break

            if not found:
                gaps.append(skill)

        return gaps

    def personalize_skill_content(
        self,
        skill_content: str,
        skill_type: str
    ) -> str:
        """
        个性化技能内容

        根据用户DNA调整技能内容

        Args:
            skill_content: 原始技能内容
            skill_type: 技能类型

        Returns:
            个性化后的内容
        """
        preferences = self.profile.skill_preferences

        # 根据偏好调整
        if preferences['complexity'] == 'simple':
            # 简化内容，提取关键要点
            skill_content = self._simplify_content(skill_content)
        elif preferences['complexity'] == 'detailed':
            # 添加更多细节
            skill_content = self._enrich_content(skill_content)

        if preferences['style'] == 'academic':
            # 添加理论背景
            skill_content = self._add_theory_background(skill_content)

        return skill_content

    def export_dna_profile(self) -> Dict:
        """
        导出DNA档案

        Returns:
            完整的DNA档案
        """
        return {
            'profile': self.profile.to_dict(),
            'usage_patterns': {
                sid: asdict(pattern)
                for sid, pattern in self.usage_patterns.items()
            },
            'statistics': {
                'total_skills_used': len(self.usage_patterns),
                'avg_success_rate': self._calculate_overall_success_rate(),
                'expertise_areas': list(self.profile.expertise_domains.keys())
            }
        }

    def _load_profile(self) -> UserProfile:
        """加载用户画像"""
        profile_path = self.storage_dir / 'profile.json'

        if profile_path.exists():
            try:
                with open(profile_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return UserProfile.from_dict(data)
            except Exception as e:
                print(f"[SkillDNA] 加载画像失败: {e}")

        # 创建新画像
        return UserProfile(user_id=self.user_id)

    def _save_profile(self):
        """保存用户画像"""
        profile_path = self.storage_dir / 'profile.json'
        self.profile.updated_at = datetime.now().isoformat()

        with open(profile_path, 'w', encoding='utf-8') as f:
            json.dump(self.profile.to_dict(), f, ensure_ascii=False, indent=2)

    def _load_usage_patterns(self):
        """加载使用模式"""
        patterns_path = self.storage_dir / 'usage_patterns.json'

        if patterns_path.exists():
            try:
                with open(patterns_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                for sid, pattern_data in data.items():
                    self.usage_patterns[sid] = SkillUsagePattern(**pattern_data)
            except Exception as e:
                print(f"[SkillDNA] 加载使用模式失败: {e}")

    def _save_usage_patterns(self):
        """保存使用模式"""
        patterns_path = self.storage_dir / 'usage_patterns.json'

        data = {
            sid: asdict(pattern)
            for sid, pattern in self.usage_patterns.items()
        }

        with open(patterns_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _update_from_github_analysis(self, analysis: Dict):
        """从GitHub分析更新画像"""
        # 更新GitHub源
        self.profile.github_sources['starred_repos'] = analysis.get('starred_repos', [])

        # 推断专长领域
        for lang in analysis.get('top_languages', []):
            domain = self._language_to_domain(lang)
            current = self.profile.expertise_domains.get(domain, 0)
            self.profile.expertise_domains[domain] = min(current + 0.2, 1.0)

        # 更新兴趣领域
        for interest in analysis.get('interests', []):
            if interest not in self.profile.expertise_domains:
                self.profile.expertise_domains[interest] = 0.3

        self._save_profile()

    def _language_to_domain(self, language: str) -> str:
        """编程语言映射到领域"""
        mapping = {
            'Python': 'data_science',
            'JavaScript': 'web_development',
            'TypeScript': 'web_development',
            'Java': 'enterprise',
            'Go': 'systems',
            'Rust': 'systems',
        }
        return mapping.get(language, 'general_programming')

    def _update_expertise_from_usage(self, skill_id: str, success: bool):
        """从使用更新专长"""
        # 这里简化处理，实际应该根据技能类型更新相应领域
        pass

    def _get_top_skills(self, limit: int) -> List[Dict]:
        """获取最常用的技能"""
        sorted_patterns = sorted(
            self.usage_patterns.values(),
            key=lambda p: p.use_count,
            reverse=True
        )

        return [
            {
                'skill_id': p.skill_id,
                'skill_name': p.skill_name,
                'use_count': p.use_count,
                'success_rate': p.avg_success_rate
            }
            for p in sorted_patterns[:limit]
        ]

    def _calculate_learning_velocity(self) -> float:
        """计算学习速度"""
        if len(self.usage_patterns) < 2:
            return 0.0

        # 基于技能增长曲线计算
        return len(self.usage_patterns) / 10.0  # 简化计算

    def _calculate_overall_success_rate(self) -> float:
        """计算总体成功率"""
        if not self.usage_patterns:
            return 0.0

        total_success = sum(p.success_count for p in self.usage_patterns.values())
        total_usage = sum(p.use_count for p in self.usage_patterns.values())

        return total_success / total_usage if total_usage > 0 else 0.0

    def _find_related_domains(self, domain: str) -> List[str]:
        """查找相关领域"""
        # 领域关系映射
        relations = {
            'web_development': ['frontend', 'backend', 'devops'],
            'data_science': ['machine_learning', 'statistics', 'visualization'],
            'systems': ['networking', 'security', 'performance'],
        }

        return relations.get(domain, [])

    def _simplify_content(self, content: str) -> str:
        """简化内容"""
        # 提取关键部分
        lines = content.split('\n')
        key_lines = []

        for line in lines:
            if line.startswith('#') or line.startswith('- ') or line.startswith('1.'):
                key_lines.append(line)

        return '\n'.join(key_lines[:20]) if key_lines else content

    def _enrich_content(self, content: str) -> str:
        """丰富内容"""
        # 添加更多解释和示例
        return content + "\n\n## 深入阅读\n\n- 详细文档链接\n- 相关论文\n- 案例研究"

    def _add_theory_background(self, content: str) -> str:
        """添加理论背景"""
        theory_section = """
## 理论基础

此方法基于以下理论：
- 认知负荷理论
- 专家实践研究
- 软件工程原理

### 研究背景

[理论解释...]
"""
        return theory_section + "\n\n" + content
