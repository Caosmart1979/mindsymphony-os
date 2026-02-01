#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能自动评估系统
Skill Automated Assessment System
"""

import yaml
import os
import re
import statistics
from typing import Dict, List, Any, Optional
import argparse


class SkillAssessor:
    """技能评估器"""

    def __init__(self, registry_file: str = r'C:\Users\13466\.claude\skills\mindsymphony\registry\skills.yml'):
        """初始化技能评估器"""
        self.registry_file = registry_file
        self.registry = self._load_registry()
        self.scores = {}

    def _load_registry(self) -> Dict:
        """加载技能注册表"""
        try:
            with open(self.registry_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"错误: 无法加载注册表文件 {self.registry_file}: {e}")
            return {}

    def assess_skill_metadata(self, skill_name: str, skill_config: Dict) -> Dict:
        """评估技能元数据完整性"""
        score = 0
        feedback = []

        # 评估描述
        if 'description' in skill_config and skill_config['description'] and len(skill_config['description']) > 5:
            score += 20
        else:
            feedback.append("技能描述缺失或过短")

        # 评估路径
        if 'path' in skill_config and skill_config['path'] and skill_config['path'] != 'None':
            if os.path.exists(skill_config['path']):
                score += 25
            else:
                score += 10
                feedback.append(f"技能路径不存在: {skill_config['path']}")
        else:
            feedback.append("技能路径缺失")

        # 评估触发词
        if 'triggers' in skill_config and isinstance(skill_config['triggers'], dict):
            if 'zh' in skill_config['triggers'] and len(skill_config['triggers']['zh']) > 0:
                score += 15
            if 'en' in skill_config['triggers'] and len(skill_config['triggers']['en']) > 0:
                score += 15

            total_triggers = len(skill_config['triggers'].get('zh', [])) + len(skill_config['triggers'].get('en', []))
            if total_triggers < 2:
                feedback.append(f"触发词数量过少 ({total_triggers}个)")
        else:
            feedback.append("触发词配置缺失")

        # 评估领域
        if 'domains' in skill_config and isinstance(skill_config['domains'], list) and len(skill_config['domains']) > 0:
            score += 15
        else:
            feedback.append("技能领域配置缺失")

        # 评估优先级
        if 'priority' in skill_config and isinstance(skill_config['priority'], int) and 0 < skill_config['priority'] <= 100:
            score += 10
        else:
            feedback.append("优先级配置无效")

        return {
            'score': score,
            'feedback': feedback,
            'category': 'metadata'
        }

    def assess_skill_name_quality(self, skill_name: str) -> Dict:
        """评估技能名称质量"""
        score = 0
        feedback = []

        # 评估名称长度
        name_length = len(skill_name)
        if 3 <= name_length <= 30:
            score += 30
        elif name_length < 3:
            feedback.append("技能名称过短")
        else:
            feedback.append("技能名称过长")

        # 评估名称格式
        if re.match(r'^[a-zA-Z0-9-]+$', skill_name):
            score += 30
        else:
            feedback.append("技能名称包含无效字符，建议使用小写字母、数字和连字符")

        # 评估名称可读性
        if '-' in skill_name and len(skill_name.split('-')) <= 5:
            score += 20
        elif len(skill_name) > 10 and '-' not in skill_name:
            feedback.append("技能名称过长且无分隔符，建议使用连字符分隔")

        # 评估名称唯一性
        # 简单检查是否包含常见的重复模式
        if re.search(r'[0-9]+$', skill_name) and skill_name[:-1] in self.scores:
            feedback.append("技能名称可能存在重复，建议检查是否与其他技能重名")

        return {
            'score': score,
            'feedback': feedback,
            'category': 'name_quality'
        }

    def assess_skill_trigger_quality(self, skill_name: str, skill_config: Dict) -> Dict:
        """评估触发词质量"""
        score = 0
        feedback = []

        if 'triggers' not in skill_config or not isinstance(skill_config['triggers'], dict):
            return {
                'score': 0,
                'feedback': ["触发词配置缺失"],
                'category': 'trigger_quality'
            }

        # 评估中文触发词
        zh_triggers = skill_config['triggers'].get('zh', [])
        if len(zh_triggers) > 0:
            # 检查触发词长度
            valid_zh = [t for t in zh_triggers if 2 <= len(t) <= 10]
            if len(valid_zh) == len(zh_triggers):
                score += 25
            else:
                feedback.append("部分中文触发词长度不符合要求(建议2-10个字符)")

            # 检查触发词多样性
            if len(set(zh_triggers)) == len(zh_triggers):
                score += 15
            else:
                feedback.append("中文触发词存在重复")
        else:
            feedback.append("缺少中文触发词")

        # 评估英文触发词
        en_triggers = skill_config['triggers'].get('en', [])
        if len(en_triggers) > 0:
            # 检查触发词长度
            valid_en = [t for t in en_triggers if 2 <= len(t) <= 20]
            if len(valid_en) == len(en_triggers):
                score += 25
            else:
                feedback.append("部分英文触发词长度不符合要求(建议2-20个字符)")

            # 检查触发词多样性
            if len(set(en_triggers)) == len(en_triggers):
                score += 15
            else:
                feedback.append("英文触发词存在重复")
        else:
            feedback.append("缺少英文触发词")

        return {
            'score': score,
            'feedback': feedback,
            'category': 'trigger_quality'
        }

    def assess_skill_path_validity(self, skill_name: str, skill_config: Dict) -> Dict:
        """评估技能路径有效性"""
        score = 0
        feedback = []

        if 'path' not in skill_config or not skill_config['path'] or skill_config['path'] == 'None':
            return {
                'score': 0,
                'feedback': ["技能路径缺失"],
                'category': 'path_validity'
            }

        path = skill_config['path']

        # 检查路径格式
        if path.startswith('/') or path.startswith('C:') or path.startswith('D:'):
            score += 20
        else:
            feedback.append("技能路径格式不规范")

        # 检查路径存在性
        if os.path.exists(path):
            score += 40

            # 检查是否是目录
            if os.path.isdir(path):
                score += 20

                # 检查目录结构
                if os.path.exists(os.path.join(path, 'SKILL.md')):
                    score += 10
                elif os.path.exists(os.path.join(path, 'README.md')):
                    score += 5
                else:
                    feedback.append("技能目录缺少 SKILL.md 或 README.md 文件")

            # 检查是文件
            elif os.path.isfile(path):
                if path.endswith('.skill') or path.endswith('.md'):
                    score += 20
                else:
                    feedback.append("技能文件格式不规范，建议使用 .skill 或 .md 格式")
        else:
            feedback.append(f"技能路径不存在: {path}")

        return {
            'score': score,
            'feedback': feedback,
            'category': 'path_validity'
        }

    def assess_duplicate_skills(self) -> List[Dict]:
        """检查重复或相似技能"""
        duplicates = []
        skill_names = []

        # 收集所有技能名称
        if 'internal_skills' in self.registry:
            for skill_name in self.registry['internal_skills']:
                skill_names.append(skill_name)

        if 'external_skills' in self.registry:
            for skill_name in self.registry['external_skills']:
                skill_names.append(skill_name)

        # 检查重复技能
        seen = set()
        for skill_name in skill_names:
            if skill_name in seen:
                duplicates.append({
                    'type': 'duplicate',
                    'skill1': skill_name,
                    'skill2': skill_name,
                    'similarity': 100,
                    'reason': '技能名称完全相同'
                })
            seen.add(skill_name)

        # 检查相似技能（基于名称相似度）
        for i, name1 in enumerate(skill_names):
            for j, name2 in enumerate(skill_names):
                if i < j:
                    # 简单的相似度检查
                    if self._calculate_name_similarity(name1, name2) > 80:
                        duplicates.append({
                            'type': 'similar',
                            'skill1': name1,
                            'skill2': name2,
                            'similarity': self._calculate_name_similarity(name1, name2),
                            'reason': '技能名称高度相似'
                        })

        return duplicates

    def _calculate_name_similarity(self, name1: str, name2: str) -> int:
        """计算技能名称相似度（简单实现）"""
        # 转为小写
        name1 = name1.lower()
        name2 = name2.lower()

        # 计算相同字符的比例
        common_chars = set(name1) & set(name2)
        max_len = max(len(name1), len(name2))
        if max_len == 0:
            return 0

        return int((len(common_chars) / max_len) * 100)

    def assess_all_skills(self) -> Dict:
        """评估所有技能"""
        results = {
            'internal_skills': {},
            'external_skills': {},
            'duplicates': [],
            'statistics': {}
        }

        # 评估内部技能
        if 'internal_skills' in self.registry:
            for skill_name, skill_config in self.registry['internal_skills'].items():
                results['internal_skills'][skill_name] = self._assess_single_skill(skill_name, skill_config)

        # 评估外部技能
        if 'external_skills' in self.registry:
            for skill_name, skill_config in self.registry['external_skills'].items():
                results['external_skills'][skill_name] = self._assess_single_skill(skill_name, skill_config)

        # 检查重复技能
        results['duplicates'] = self.assess_duplicate_skills()

        # 计算统计信息
        results['statistics'] = self._calculate_statistics(results)

        return results

    def _assess_single_skill(self, skill_name: str, skill_config: Dict) -> Dict:
        """评估单个技能"""
        assessments = []

        assessments.append(self.assess_skill_metadata(skill_name, skill_config))
        assessments.append(self.assess_skill_name_quality(skill_name))
        assessments.append(self.assess_skill_trigger_quality(skill_name, skill_config))
        assessments.append(self.assess_skill_path_validity(skill_name, skill_config))

        # 计算总分
        total_score = sum(assessment['score'] for assessment in assessments)
        total_feedback = []
        for assessment in assessments:
            total_feedback.extend(assessment['feedback'])

        # 计算平均分
        avg_score = total_score / len(assessments)

        return {
            'total_score': total_score,
            'average_score': avg_score,
            'assessments': assessments,
            'feedback': total_feedback,
            'quality_level': self._determine_quality_level(total_score)
        }

    def _determine_quality_level(self, score: int) -> str:
        """根据分数确定质量等级（总分为400分）"""
        if score >= 360:
            return '优秀'
        elif score >= 320:
            return '良好'
        elif score >= 280:
            return '中等'
        elif score >= 240:
            return '合格'
        else:
            return '需要改进'

    def _calculate_statistics(self, results: Dict) -> Dict:
        """计算统计信息"""
        all_scores = []

        for skill_name, assessment in results['internal_skills'].items():
            all_scores.append(assessment['total_score'])

        for skill_name, assessment in results['external_skills'].items():
            all_scores.append(assessment['total_score'])

        if not all_scores:
            return {
                'total_skills': 0,
                'internal_skills_count': len(results['internal_skills']),
                'external_skills_count': len(results['external_skills']),
                'duplicates_count': len(results['duplicates'])
            }

        return {
            'total_skills': len(all_scores),
            'internal_skills_count': len(results['internal_skills']),
            'external_skills_count': len(results['external_skills']),
            'duplicates_count': len(results['duplicates']),
            'average_score': statistics.mean(all_scores),
            'max_score': max(all_scores),
            'min_score': min(all_scores),
            'score_variance': statistics.variance(all_scores) if len(all_scores) > 1 else 0,
            'quality_distribution': self._calculate_quality_distribution(all_scores)
        }

    def _calculate_quality_distribution(self, scores: List[float]) -> Dict:
        """计算质量等级分布"""
        distribution = {
            '优秀': 0,
            '良好': 0,
            '中等': 0,
            '合格': 0,
            '需要改进': 0
        }

        for score in scores:
            level = self._determine_quality_level(score)
            distribution[level] += 1

        return distribution

    def generate_report(self, results: Dict, output_file: str = 'skill_assessment_report.md') -> str:
        """生成评估报告"""
        report = []

        # 报告标题
        report.append("# MindSymphony 技能质量评估报告")
        report.append("")

        # 统计摘要
        stats = results['statistics']
        report.append("## 评估统计")
        report.append("")
        report.append(f"- **总技能数量**: {stats['total_skills']}")
        report.append(f"- **内部技能**: {stats['internal_skills_count']}")
        report.append(f"- **外部技能**: {stats['external_skills_count']}")
        report.append(f"- **重复/相似技能**: {stats['duplicates_count']}")
        report.append(f"- **平均分数**: {stats['average_score']:.1f}")
        report.append(f"- **最高分**: {stats['max_score']:.1f}")
        report.append(f"- **最低分**: {stats['min_score']:.1f}")
        report.append("")

        # 质量等级分布
        report.append("## 质量等级分布")
        report.append("")
        distribution = stats['quality_distribution']
        report.append("| 质量等级 | 技能数量 | 占比 |")
        report.append("|----------|----------|------|")
        for level, count in distribution.items():
            percentage = (count / stats['total_skills']) * 100 if stats['total_skills'] > 0 else 0
            report.append(f"| {level} | {count} | {percentage:.1f}% |")
        report.append("")

        # 重复技能警告
        if results['duplicates']:
            report.append("## 重复/相似技能警告")
            report.append("")
            report.append("以下技能可能存在重复或高度相似的情况：")
            report.append("")
            report.append("| 类型 | 技能1 | 技能2 | 相似度 | 原因 |")
            report.append("|------|-------|-------|--------|------|")
            for dup in results['duplicates']:
                report.append(f"| {dup['type']} | {dup['skill1']} | {dup['skill2']} | {dup['similarity']}% | {dup['reason']} |")
            report.append("")

        # 详细评估结果
        report.append("## 详细评估结果")
        report.append("")

        # 内部技能评估
        if results['internal_skills']:
            report.append("### 内部技能")
            report.append("")
            report.append("| 技能名称 | 总分 | 平均分 | 质量等级 | 问题数量 | 主要问题 |")
            report.append("|----------|------|--------|----------|----------|----------|")

            sorted_skills = sorted(results['internal_skills'].items(),
                                 key=lambda x: x[1]['total_score'], reverse=True)

            for skill_name, assessment in sorted_skills:
                main_issues = ", ".join(assessment['feedback'][:3]) if assessment['feedback'] else "无"
                report.append(f"| {skill_name} | {assessment['total_score']:.1f} | {assessment['average_score']:.1f} | {assessment['quality_level']} | {len(assessment['feedback'])} | {main_issues} |")

        # 外部技能评估
        if results['external_skills']:
            report.append("")
            report.append("### 外部技能")
            report.append("")
            report.append("| 技能名称 | 总分 | 平均分 | 质量等级 | 问题数量 | 主要问题 |")
            report.append("|----------|------|--------|----------|----------|----------|")

            sorted_skills = sorted(results['external_skills'].items(),
                                 key=lambda x: x[1]['total_score'], reverse=True)

            for skill_name, assessment in sorted_skills:
                main_issues = ", ".join(assessment['feedback'][:3]) if assessment['feedback'] else "无"
                report.append(f"| {skill_name} | {assessment['total_score']:.1f} | {assessment['average_score']:.1f} | {assessment['quality_level']} | {len(assessment['feedback'])} | {main_issues} |")

        # 建议改进
        report.append("")
        report.append("## 改进建议")
        report.append("")
        report.append("### 总体建议")
        report.append("")

        if stats['average_score'] < 70:
            report.append("- **整体质量偏低**: 需要全面检查技能配置质量")
        elif stats['average_score'] < 80:
            report.append("- **质量一般**: 大部分技能需要优化元数据和触发词")
        else:
            report.append("- **质量良好**: 继续保持，重点优化少数低质量技能")

        if stats['duplicates_count'] > 0:
            report.append(f"- **重复技能**: 发现 {stats['duplicates_count']} 个重复或相似技能，建议合并或重命名")

        # 质量等级分布建议
        distribution = stats['quality_distribution']
        if distribution['需要改进'] > 0:
            report.append(f"- **需要改进的技能**: {distribution['需要改进']} 个技能质量较差，建议重点优化")

        report.append("")
        report.append("### 具体优化建议")
        report.append("")
        report.append("1. **完善技能描述**: 确保每个技能有清晰、具体的描述")
        report.append("2. **优化触发词**: 增加触发词多样性，确保中英文触发词都有")
        report.append("3. **检查路径有效性**: 确保技能路径正确，目录结构规范")
        report.append("4. **统一命名规范**: 使用小写字母、数字和连字符，避免过长名称")
        report.append("5. **合并重复技能**: 对相似技能进行合并或重命名")
        report.append("6. **定期维护**: 建立技能定期评估和更新机制")

        report_text = "\n".join(report)

        # 保存报告到文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report_text)

        print(f"评估报告已保存到: {output_file}")

        return report_text


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="MindSymphony 技能自动评估系统")
    parser.add_argument('--registry', '-r',
                      default=r'C:\Users\13466\.claude\skills\mindsymphony\registry\skills.yml',
                      help='技能注册表文件路径')
    parser.add_argument('--output', '-o',
                      default='skill_assessment_report.md',
                      help='评估报告输出文件')
    parser.add_argument('--verbose', '-v',
                      action='store_true',
                      help='显示详细评估过程')

    args = parser.parse_args()

    print("=" * 60)
    print("MindSymphony 技能自动评估系统")
    print("=" * 60)
    print(f"评估文件: {args.registry}")
    print()

    # 创建评估器
    assessor = SkillAssessor(args.registry)

    # 执行评估
    print("正在评估技能质量...")
    results = assessor.assess_all_skills()

    # 生成报告
    print("正在生成评估报告...")
    report = assessor.generate_report(results, args.output)

    print()
    print("=" * 60)
    print("评估完成！")
    print("=" * 60)
    print()
    print(f"报告已保存到: {args.output}")
    print()

    # 显示统计摘要
    stats = results['statistics']
    print(f"评估统计:")
    print(f"  总技能数量: {stats['total_skills']}")
    print(f"  内部技能: {stats['internal_skills_count']}")
    print(f"  外部技能: {stats['external_skills_count']}")
    print(f"  重复/相似技能: {stats['duplicates_count']}")
    print(f"  平均分数: {stats['average_score']:.1f}")
    print(f"  质量等级分布:")
    for level, count in stats['quality_distribution'].items():
        percentage = (count / stats['total_skills']) * 100 if stats['total_skills'] > 0 else 0
        print(f"    {level}: {count} ({percentage:.1f}%)")


if __name__ == "__main__":
    main()