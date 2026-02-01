#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能推荐引擎
Skill Recommendation Engine
"""

import yaml
import os
import re
import math
from typing import Dict, List, Any, Optional
import argparse
import json
import datetime


class SkillRecommendationEngine:
    """技能推荐引擎"""

    def __init__(self, registry_file: str = r'C:\Users\13466\.claude\skills\mindsymphony\registry\skills.yml',
                 usage_data_file: str = 'skill_usage_data.json'):
        """初始化技能推荐引擎"""
        self.registry_file = registry_file
        self.usage_data_file = usage_data_file
        self.registry = self._load_registry()
        self.usage_data = self._load_usage_data()
        self.skill_keywords = self._extract_skill_keywords()

    def _load_registry(self) -> Dict:
        """加载技能注册表"""
        try:
            with open(self.registry_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"错误: 无法加载注册表文件 {self.registry_file}: {e}")
            return {'internal_skills': {}, 'external_skills': {}}

    def _load_usage_data(self) -> Dict:
        """加载技能使用数据"""
        if os.path.exists(self.usage_data_file):
            try:
                with open(self.usage_data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"警告: 无法加载使用数据文件 {self.usage_data_file}: {e}")
        return {'skills': {}, 'users': {}, 'sessions': []}

    def _save_usage_data(self):
        """保存技能使用数据"""
        try:
            with open(self.usage_data_file, 'w', encoding='utf-8') as f:
                json.dump(self.usage_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"警告: 无法保存使用数据文件 {self.usage_data_file}: {e}")

    def _extract_skill_keywords(self) -> Dict:
        """提取技能关键词"""
        keywords = {}

        for skill_type in ['internal_skills', 'external_skills']:
            if skill_type not in self.registry:
                continue

            for skill_name, skill_config in self.registry[skill_type].items():
                skill_keywords = set()

                # 技能名称作为关键词
                name_parts = re.split(r'[-_]', skill_name.lower())
                skill_keywords.update(name_parts)

                # 描述作为关键词
                if 'description' in skill_config:
                    desc_words = re.split(r'\W+', skill_config['description'].lower())
                    skill_keywords.update([word for word in desc_words if len(word) > 2])

                # 领域作为关键词
                if 'domains' in skill_config and isinstance(skill_config['domains'], list):
                    for domain in skill_config['domains']:
                        domain_parts = re.split(r'[-_]', domain.lower())
                        skill_keywords.update(domain_parts)

                # 触发词作为关键词
                if 'triggers' in skill_config and isinstance(skill_config['triggers'], dict):
                    for lang in ['zh', 'en']:
                        if lang in skill_config['triggers'] and isinstance(skill_config['triggers'][lang], list):
                            for trigger in skill_config['triggers'][lang]:
                                trigger_parts = re.split(r'\W+', trigger.lower())
                                skill_keywords.update([word for word in trigger_parts if len(word) > 1])

                keywords[skill_name] = list(skill_keywords)

        return keywords

    def _calculate_keyword_similarity(self, query_keywords: List[str], skill_keywords: List[str]) -> float:
        """计算关键词相似度"""
        if not query_keywords or not skill_keywords:
            return 0.0

        # 计算Jaccard相似度
        query_set = set(query_keywords)
        skill_set = set(skill_keywords)

        intersection = len(query_set & skill_set)
        union = len(query_set | skill_set)

        if union == 0:
            return 0.0

        return intersection / union

    def _calculate_usage_score(self, skill_name: str) -> float:
        """计算技能使用得分"""
        if skill_name not in self.usage_data['skills']:
            return 0.1  # 为未使用过的技能提供基础分数

        skill_usage = self.usage_data['skills'][skill_name]

        # 计算使用频率得分
        usage_count = skill_usage.get('count', 0)
        frequency_score = min(usage_count / 10, 1)  # 最多10次使用得满分

        # 计算最近使用得分
        last_used = skill_usage.get('last_used')
        if last_used:
            try:
                last_used_date = datetime.datetime.fromisoformat(last_used.replace('Z', '+00:00'))
                days_since_used = (datetime.datetime.now() - last_used_date).days
                recency_score = max(1 - days_since_used / 30, 0)  # 30天内使用过得满分
            except Exception:
                recency_score = 0.5
        else:
            recency_score = 0.5

        # 计算平均得分
        avg_score = skill_usage.get('avg_score', 5) / 5  # 归一化到0-1范围

        # 综合得分
        total_score = (frequency_score * 0.4) + (recency_score * 0.3) + (avg_score * 0.3)

        return total_score

    def _calculate_skill_quality_score(self, skill_config: Dict) -> float:
        """计算技能质量得分"""
        # 基于配置完整性计算质量得分
        score = 0

        if 'description' in skill_config and len(skill_config['description']) > 10:
            score += 20
        if 'path' in skill_config and skill_config['path'] and os.path.exists(skill_config['path']):
            score += 25
        if 'triggers' in skill_config and isinstance(skill_config['triggers'], dict):
            if 'zh' in skill_config['triggers'] and len(skill_config['triggers']['zh']) > 0:
                score += 15
            if 'en' in skill_config['triggers'] and len(skill_config['triggers']['en']) > 0:
                score += 15
        if 'domains' in skill_config and isinstance(skill_config['domains'], list) and len(skill_config['domains']) > 0:
            score += 15
        if 'priority' in skill_config and isinstance(skill_config['priority'], int) and 0 < skill_config['priority'] <= 100:
            score += 10

        return score / 100  # 归一化到0-1范围

    def _calculate_query_keywords(self, query: str) -> List[str]:
        """提取查询关键词"""
        # 去除标点符号，转为小写
        cleaned_query = re.sub(r'[^\w\s]', '', query.lower())
        # 分割成单词
        words = cleaned_query.split()
        # 过滤掉太短的词
        return [word for word in words if len(word) > 1]

    def recommend_skills(self, query: str, user_id: Optional[str] = None,
                       num_recommendations: int = 5, include_external: bool = True) -> List[Dict]:
        """推荐技能"""
        # 提取查询关键词
        query_keywords = self._calculate_query_keywords(query)

        # 收集所有技能
        all_skills = []

        if 'internal_skills' in self.registry:
            for skill_name, skill_config in self.registry['internal_skills'].items():
                all_skills.append({
                    'name': skill_name,
                    'config': skill_config,
                    'type': 'internal'
                })

        if include_external and 'external_skills' in self.registry:
            for skill_name, skill_config in self.registry['external_skills'].items():
                all_skills.append({
                    'name': skill_name,
                    'config': skill_config,
                    'type': 'external'
                })

        # 计算每个技能的推荐得分
        skill_scores = []

        for skill in all_skills:
            # 关键词匹配得分
            keyword_score = self._calculate_keyword_similarity(query_keywords, self.skill_keywords.get(skill['name'], []))

            # 使用得分
            usage_score = self._calculate_usage_score(skill['name'])

            # 质量得分
            quality_score = self._calculate_skill_quality_score(skill['config'])

            # 综合得分（加权平均）
            total_score = (keyword_score * 0.5) + (usage_score * 0.3) + (quality_score * 0.2)

            skill_scores.append({
                'name': skill['name'],
                'type': skill['type'],
                'config': skill['config'],
                'keyword_score': keyword_score,
                'usage_score': usage_score,
                'quality_score': quality_score,
                'total_score': total_score
            })

        # 按得分排序
        sorted_skills = sorted(skill_scores, key=lambda x: x['total_score'], reverse=True)

        # 筛选出前N个
        top_skills = sorted_skills[:num_recommendations]

        # 格式化推荐结果
        recommendations = []

        for skill in top_skills:
            recommendations.append({
                'name': skill['name'],
                'type': '内部技能' if skill['type'] == 'internal' else '外部技能',
                'description': skill['config'].get('description', '无描述'),
                'domains': skill['config'].get('domains', []),
                'score': round(skill['total_score'] * 100, 1),
                'keywords': self.skill_keywords.get(skill['name'], [])
            })

        return recommendations

    def log_skill_usage(self, skill_name: str, user_id: str, score: int = 5):
        """记录技能使用"""
        # 确保技能存在
        if skill_name not in self.skill_keywords:
            return

        # 更新技能使用数据
        if skill_name not in self.usage_data['skills']:
            self.usage_data['skills'][skill_name] = {
                'count': 0,
                'last_used': None,
                'avg_score': 0,
                'total_score': 0
            }

        skill_usage = self.usage_data['skills'][skill_name]
        skill_usage['count'] += 1
        skill_usage['last_used'] = datetime.datetime.now().isoformat()
        # 计算平均得分
        skill_usage['total_score'] += score
        skill_usage['avg_score'] = skill_usage['total_score'] / skill_usage['count']

        # 更新用户数据
        if user_id not in self.usage_data['users']:
            self.usage_data['users'][user_id] = {
                'name': f'用户{user_id}',
                'skills_used': [],
                'total_usage': 0
            }

        user = self.usage_data['users'][user_id]
        if skill_name not in user['skills_used']:
            user['skills_used'].append(skill_name)
        user['total_usage'] += 1

        # 记录会话
        self.usage_data['sessions'].append({
            'user_id': user_id,
            'skill_name': skill_name,
            'timestamp': datetime.datetime.now().isoformat(),
            'score': score
        })

        # 保存数据
        self._save_usage_data()

    def get_skill_usage_statistics(self) -> Dict:
        """获取技能使用统计"""
        stats = {
            'total_skills_used': len(self.usage_data['skills']),
            'total_usage_count': sum(skill['count'] for skill in self.usage_data['skills'].values()),
            'most_used_skills': [],
            'least_used_skills': [],
            'average_score': 0,
            'skills_by_domain': {}
        }

        # 计算平均得分
        if self.usage_data['skills']:
            total_score = sum(skill['total_score'] for skill in self.usage_data['skills'].values())
            total_count = sum(skill['count'] for skill in self.usage_data['skills'].values())
            stats['average_score'] = round(total_score / total_count, 2)

        # 按使用次数排序
        sorted_skills = sorted(self.usage_data['skills'].items(), key=lambda x: x[1]['count'], reverse=True)
        stats['most_used_skills'] = [{'name': name, 'count': data['count']} for name, data in sorted_skills[:10]]
        stats['least_used_skills'] = [{'name': name, 'count': data['count']} for name, data in sorted_skills[-10:]]

        # 按领域分组
        for skill_type in ['internal_skills', 'external_skills']:
            if skill_type not in self.registry:
                continue

            for skill_name, skill_config in self.registry[skill_type].items():
                domains = skill_config.get('domains', [])
                for domain in domains:
                    if domain not in stats['skills_by_domain']:
                        stats['skills_by_domain'][domain] = []
                    stats['skills_by_domain'][domain].append(skill_name)

        return stats

    def generate_recommendation_report(self, query: str, recommendations: List[Dict],
                                      user_id: Optional[str] = None) -> str:
        """生成推荐报告"""
        report = []

        report.append("# MindSymphony 技能推荐报告")
        report.append("")
        report.append(f"**查询内容**: {query}")
        if user_id:
            report.append(f"**用户ID**: {user_id}")
        report.append(f"**生成时间**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")

        report.append("## 推荐结果")
        report.append("")
        report.append("| 排名 | 技能名称 | 类型 | 描述 | 领域 | 得分 |")
        report.append("|------|----------|------|------|------|------|")

        for i, skill in enumerate(recommendations, 1):
            domains = ', '.join(skill['domains']) if skill['domains'] else '无'
            report.append(f"| {i} | {skill['name']} | {skill['type']} | {skill['description'][:50]}... | {domains} | {skill['score']} |")

        report.append("")

        report.append("## 关键词匹配分析")
        report.append("")

        all_keywords = set()
        for skill in recommendations:
            all_keywords.update(skill['keywords'])

        report.append("**匹配的关键词**: " + ", ".join(all_keywords))
        report.append("")

        report.append("## 技能使用建议")
        report.append("")
        report.append("### 如何有效使用推荐的技能:")
        report.append("")
        report.append("1. **查看技能详情**: 使用 `skill show <技能名称>` 命令查看完整配置")
        report.append("2. **测试技能功能**: 在实际场景中测试技能的效果")
        report.append("3. **提供反馈**: 使用后记录使用体验和建议，帮助优化技能")
        report.append("4. **探索相关技能**: 查看推荐技能的领域，寻找其他相关技能")
        report.append("")

        report.append("## 使用统计（最近30天）")
        report.append("")
        stats = self.get_skill_usage_statistics()
        report.append(f"- **总技能使用次数**: {stats['total_usage_count']}")
        report.append(f"- **使用技能数量**: {stats['total_skills_used']}")
        report.append(f"- **平均评分**: {stats['average_score']}")
        report.append("")

        if stats['most_used_skills']:
            report.append("### 最常用技能:")
            report.append("")
            for skill in stats['most_used_skills']:
                report.append(f"- {skill['name']} ({skill['count']} 次)")
            report.append("")

        return "\n".join(report)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="MindSymphony 技能推荐引擎")
    parser.add_argument('--query', '-q', required=True, help='查询关键词或描述')
    parser.add_argument('--user', '-u', help='用户ID（用于个性化推荐）')
    parser.add_argument('--num', '-n', type=int, default=5, help='推荐数量（默认5个）')
    parser.add_argument('--include-external', '-e', action='store_true',
                      help='是否包含外部技能（默认不包含）')
    parser.add_argument('--report', '-r', help='生成推荐报告的输出文件')
    parser.add_argument('--log-usage', '-l', action='store_true',
                      help='是否记录使用（用于测试）')

    args = parser.parse_args()

    print("=" * 60)
    print("MindSymphony 技能推荐引擎")
    print("=" * 60)
    print(f"查询内容: {args.query}")
    if args.user:
        print(f"用户ID: {args.user}")
    print(f"推荐数量: {args.num}")
    print(f"包含外部技能: {args.include_external}")
    print()

    engine = SkillRecommendationEngine()

    # 获取推荐
    recommendations = engine.recommend_skills(
        args.query,
        args.user,
        args.num,
        args.include_external
    )

    # 显示推荐结果
    print("推荐结果:")
    for i, skill in enumerate(recommendations, 1):
        print(f"{i}. {skill['name']} ({skill['type']})")
        print(f"   描述: {skill['description']}")
        print(f"   领域: {', '.join(skill['domains'])}")
        print(f"   得分: {skill['score']}")
        print()

    # 记录使用（如果需要）
    if args.log_usage and args.user:
        print("记录使用数据...")
        for skill in recommendations:
            engine.log_skill_usage(skill['name'], args.user)
        print("使用数据已保存")
        print()

    # 生成报告
    if args.report:
        print(f"正在生成推荐报告: {args.report}")
        report = engine.generate_recommendation_report(args.query, recommendations, args.user)

        with open(args.report, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"报告已保存到: {args.report}")

    print("=" * 60)
    print("技能推荐完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()