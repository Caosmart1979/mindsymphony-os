#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能持续优化机制
Skill Continuous Optimization Mechanism
"""

import yaml
import os
import re
import datetime
import time
import schedule
from typing import Dict, List, Any, Optional
import argparse
import json


class SkillOptimizer:
    """技能持续优化器"""

    def __init__(self, registry_file: str = r'C:\Users\13466\.claude\skills\mindsymphony\registry\skills.yml',
                 usage_data_file: str = 'skill_usage_data.json',
                 optimization_config: str = 'skill_optimization_config.json'):
        """初始化技能优化器"""
        self.registry_file = registry_file
        self.usage_data_file = usage_data_file
        self.optimization_config = optimization_config

        self.registry = self._load_registry()
        self.usage_data = self._load_usage_data()
        self.optimization_rules = self._load_optimization_config()

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

    def _load_optimization_config(self) -> Dict:
        """加载优化配置"""
        default_config = {
            'quality_threshold': 70,
            'usage_threshold': 3,
            'inactive_days_threshold': 30,
            'optimization_categories': [
                'description_optimization',
                'trigger_optimization',
                'path_validation',
                'duplicate_detection',
                'usage_analysis'
            ],
            'automatic_optimization': False,
            'report_generation': True,
            'notification': False
        }

        if os.path.exists(self.optimization_config):
            try:
                with open(self.optimization_config, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                return {**default_config, **config}
            except Exception as e:
                print(f"警告: 无法加载优化配置文件 {self.optimization_config}: {e}")

        return default_config

    def _save_optimization_config(self):
        """保存优化配置"""
        try:
            with open(self.optimization_config, 'w', encoding='utf-8') as f:
                json.dump(self.optimization_rules, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"警告: 无法保存优化配置文件 {self.optimization_config}: {e}")

    def _calculate_skill_quality_score(self, skill_config: Dict) -> float:
        """计算技能质量得分"""
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

        return score

    def _analyze_low_quality_skills(self) -> List[Dict]:
        """分析低质量技能"""
        low_quality_skills = []

        for skill_type in ['internal_skills', 'external_skills']:
            if skill_type not in self.registry:
                continue

            for skill_name, skill_config in self.registry[skill_type].items():
                quality_score = self._calculate_skill_quality_score(skill_config)

                if quality_score < self.optimization_rules['quality_threshold']:
                    low_quality_skills.append({
                        'name': skill_name,
                        'type': '内部' if skill_type == 'internal_skills' else '外部',
                        'quality_score': quality_score,
                        'config': skill_config
                    })

        return low_quality_skills

    def _analyze_unused_skills(self) -> List[Dict]:
        """分析未使用的技能"""
        unused_skills = []

        for skill_type in ['internal_skills', 'external_skills']:
            if skill_type not in self.registry:
                continue

            for skill_name, skill_config in self.registry[skill_type].items():
                if skill_name not in self.usage_data.get('skills', {}):
                    unused_skills.append({
                        'name': skill_name,
                        'type': '内部' if skill_type == 'internal_skills' else '外部',
                        'config': skill_config
                    })

        return unused_skills

    def _analyze_inactive_skills(self) -> List[Dict]:
        """分析长期未使用的技能"""
        inactive_skills = []

        for skill_name, skill_usage in self.usage_data.get('skills', {}).items():
            if 'last_used' in skill_usage:
                try:
                    last_used_date = datetime.datetime.fromisoformat(skill_usage['last_used'].replace('Z', '+00:00'))
                    days_since_used = (datetime.datetime.now() - last_used_date).days

                    if days_since_used > self.optimization_rules['inactive_days_threshold']:
                        # 查找技能配置
                        skill_config = None
                        if skill_name in self.registry.get('internal_skills', {}):
                            skill_config = self.registry['internal_skills'][skill_name]
                            skill_type = '内部'
                        elif skill_name in self.registry.get('external_skills', {}):
                            skill_config = self.registry['external_skills'][skill_name]
                            skill_type = '外部'

                        if skill_config:
                            inactive_skills.append({
                                'name': skill_name,
                                'type': skill_type,
                                'days_inactive': days_since_used,
                                'usage_count': skill_usage.get('count', 0),
                                'config': skill_config
                            })

                except Exception as e:
                    print(f"警告: 无法解析技能 {skill_name} 的最后使用时间: {e}")

        return inactive_skills

    def _analyze_underused_skills(self) -> List[Dict]:
        """分析使用次数过少的技能"""
        underused_skills = []

        for skill_name, skill_usage in self.usage_data.get('skills', {}).items():
            if skill_usage.get('count', 0) < self.optimization_rules['usage_threshold']:
                # 查找技能配置
                skill_config = None
                if skill_name in self.registry.get('internal_skills', {}):
                    skill_config = self.registry['internal_skills'][skill_name]
                    skill_type = '内部'
                elif skill_name in self.registry.get('external_skills', {}):
                    skill_config = self.registry['external_skills'][skill_name]
                    skill_type = '外部'

                if skill_config:
                    underused_skills.append({
                        'name': skill_name,
                        'type': skill_type,
                        'usage_count': skill_usage.get('count', 0),
                        'config': skill_config
                    })

        return underused_skills

    def _generate_optimization_suggestions(self, low_quality: List[Dict],
                                        unused: List[Dict],
                                        inactive: List[Dict],
                                        underused: List[Dict]) -> List[Dict]:
        """生成优化建议"""
        suggestions = []

        # 低质量技能建议
        for skill in low_quality:
            suggestion = {
                'skill_name': skill['name'],
                'type': skill['type'],
                'issue': '低质量技能',
                'severity': '高',
                'suggestions': [],
                'quality_score': skill['quality_score']
            }

            if len(skill['config'].get('description', '')) < 10:
                suggestion['suggestions'].append("完善技能描述，确保长度至少10个字符")

            if not os.path.exists(skill['config'].get('path', '')):
                suggestion['suggestions'].append("检查并修复技能路径")

            if not skill['config'].get('triggers', {}).get('zh') and not skill['config'].get('triggers', {}).get('en'):
                suggestion['suggestions'].append("添加中文或英文触发词")

            if not skill['config'].get('domains', []):
                suggestion['suggestions'].append("添加技能适用领域")

            suggestions.append(suggestion)

        # 未使用技能建议
        for skill in unused:
            suggestion = {
                'skill_name': skill['name'],
                'type': skill['type'],
                'issue': '未使用技能',
                'severity': '中',
                'suggestions': [
                    "检查技能是否符合当前需求",
                    "考虑是否需要保留或删除",
                    "更新技能描述或触发词以提高可见性"
                ],
                'usage_count': 0
            }

            suggestions.append(suggestion)

        # 长期未使用技能建议
        for skill in inactive:
            suggestion = {
                'skill_name': skill['name'],
                'type': skill['type'],
                'issue': '长期未使用技能',
                'severity': '中',
                'suggestions': [
                    f"该技能已 {skill['days_inactive']} 天未使用",
                    "检查是否还符合需求",
                    "考虑是否需要更新或删除",
                    "可以尝试重新宣传该技能"
                ],
                'days_inactive': skill['days_inactive'],
                'usage_count': skill['usage_count']
            }

            suggestions.append(suggestion)

        # 使用过少技能建议
        for skill in underused:
            suggestion = {
                'skill_name': skill['name'],
                'type': skill['type'],
                'issue': '使用次数过少',
                'severity': '低',
                'suggestions': [
                    f"该技能仅使用了 {skill['usage_count']} 次",
                    "检查技能的描述和触发词是否准确",
                    "考虑是否需要优化技能功能",
                    "可以提供更多使用示例"
                ],
                'usage_count': skill['usage_count']
            }

            suggestions.append(suggestion)

        return suggestions

    def run_optimization(self, run_all: bool = True) -> Dict:
        """运行技能优化"""
        results = {
            'timestamp': datetime.datetime.now().isoformat(),
            'low_quality_skills': [],
            'unused_skills': [],
            'inactive_skills': [],
            'underused_skills': [],
            'suggestions': []
        }

        if run_all or 'description_optimization' in self.optimization_rules['optimization_categories'] or \
           'trigger_optimization' in self.optimization_rules['optimization_categories'] or \
           'path_validation' in self.optimization_rules['optimization_categories']:
            print("正在分析低质量技能...")
            results['low_quality_skills'] = self._analyze_low_quality_skills()

        if run_all or 'usage_analysis' in self.optimization_rules['optimization_categories']:
            print("正在分析未使用的技能...")
            results['unused_skills'] = self._analyze_unused_skills()

            print("正在分析长期未使用的技能...")
            results['inactive_skills'] = self._analyze_inactive_skills()

            print("正在分析使用次数过少的技能...")
            results['underused_skills'] = self._analyze_underused_skills()

        # 生成优化建议
        results['suggestions'] = self._generate_optimization_suggestions(
            results['low_quality_skills'],
            results['unused_skills'],
            results['inactive_skills'],
            results['underused_skills']
        )

        return results

    def generate_optimization_report(self, results: Dict, output_file: str = 'skill_optimization_report.md') -> str:
        """生成优化报告"""
        report = []

        report.append("# MindSymphony 技能持续优化报告")
        report.append("")
        report.append(f"**生成时间**: {datetime.datetime.fromisoformat(results['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"**技能总数**: {len(self.registry.get('internal_skills', {})) + len(self.registry.get('external_skills', {}))}")
        report.append(f"**评估技能**: {len(self.registry.get('internal_skills', {})) + len(self.registry.get('external_skills', {}))}")
        report.append("")

        # 低质量技能
        if results['low_quality_skills']:
            report.append("## 低质量技能")
            report.append("")
            report.append("| 技能名称 | 类型 | 质量得分 | 主要问题 |")
            report.append("|----------|------|----------|----------|")

            for skill in results['low_quality_skills']:
                issues = []
                if len(skill['config'].get('description', '')) < 10:
                    issues.append("描述过短")
                if not os.path.exists(skill['config'].get('path', '')):
                    issues.append("路径无效")
                if not skill['config'].get('triggers', {}).get('zh') and not skill['config'].get('triggers', {}).get('en'):
                    issues.append("缺少触发词")
                if not skill['config'].get('domains', []):
                    issues.append("缺少领域")

                report.append(f"| {skill['name']} | {skill['type']} | {skill['quality_score']} | {', '.join(issues)} |")

            report.append("")

        # 未使用技能
        if results['unused_skills']:
            report.append("## 未使用技能")
            report.append("")
            report.append(f"发现 {len(results['unused_skills'])} 个技能从未使用")
            report.append("")
            report.append("| 技能名称 | 类型 | 领域 |")
            report.append("|----------|------|------|")

            for skill in results['unused_skills']:
                domains = ', '.join(skill['config'].get('domains', []))
                report.append(f"| {skill['name']} | {skill['type']} | {domains} |")

            report.append("")

        # 长期未使用技能
        if results['inactive_skills']:
            report.append("## 长期未使用技能")
            report.append("")
            report.append(f"发现 {len(results['inactive_skills'])} 个技能超过 {self.optimization_rules['inactive_days_threshold']} 天未使用")
            report.append("")
            report.append("| 技能名称 | 类型 | 未使用天数 | 使用次数 |")
            report.append("|----------|------|------------|----------|")

            for skill in results['inactive_skills']:
                report.append(f"| {skill['name']} | {skill['type']} | {skill['days_inactive']} | {skill['usage_count']} |")

            report.append("")

        # 使用过少技能
        if results['underused_skills']:
            report.append("## 使用次数过少技能")
            report.append("")
            report.append(f"发现 {len(results['underused_skills'])} 个技能使用次数少于 {self.optimization_rules['usage_threshold']} 次")
            report.append("")
            report.append("| 技能名称 | 类型 | 使用次数 |")
            report.append("|----------|------|----------|")

            for skill in results['underused_skills']:
                report.append(f"| {skill['name']} | {skill['type']} | {skill['usage_count']} |")

            report.append("")

        # 优化建议
        if results['suggestions']:
            report.append("## 优化建议")
            report.append("")

            # 按严重程度分组
            high_severity = [s for s in results['suggestions'] if s['severity'] == '高']
            medium_severity = [s for s in results['suggestions'] if s['severity'] == '中']
            low_severity = [s for s in results['suggestions'] if s['severity'] == '低']

            if high_severity:
                report.append("### 高优先级")
                report.append("")
                for suggestion in high_severity:
                    report.append(f"#### {suggestion['skill_name']} ({suggestion['type']})")
                    report.append("- **问题**: " + suggestion['issue'])
                    for s in suggestion['suggestions']:
                        report.append("- **建议**: " + s)
                    report.append("")

            if medium_severity:
                report.append("### 中优先级")
                report.append("")
                for suggestion in medium_severity:
                    report.append(f"#### {suggestion['skill_name']} ({suggestion['type']})")
                    report.append("- **问题**: " + suggestion['issue'])
                    for s in suggestion['suggestions']:
                        report.append("- **建议**: " + s)
                    report.append("")

            if low_severity:
                report.append("### 低优先级")
                report.append("")
                for suggestion in low_severity:
                    report.append(f"#### {suggestion['skill_name']} ({suggestion['type']})")
                    report.append("- **问题**: " + suggestion['issue'])
                    for s in suggestion['suggestions']:
                        report.append("- **建议**: " + s)
                    report.append("")

        # 优化总结
        report.append("## 优化总结")
        report.append("")

        total_issues = len(results['suggestions'])
        report.append(f"- **总问题数量**: {total_issues}")
        report.append(f"- **低质量技能**: {len(results['low_quality_skills'])}")
        report.append(f"- **未使用技能**: {len(results['unused_skills'])}")
        report.append(f"- **长期未使用技能**: {len(results['inactive_skills'])}")
        report.append(f"- **使用次数过少技能**: {len(results['underused_skills'])}")
        report.append("")

        report.append("### 建议的优化步骤")
        report.append("")
        report.append("1. **立即处理高优先级问题**: 重点修复低质量技能的问题")
        report.append("2. **评估未使用技能**: 检查未使用技能的必要性，决定保留或删除")
        report.append("3. **分析使用模式**: 了解技能使用情况，优化触发词和描述")
        report.append("4. **定期维护**: 建立技能定期评估和优化机制")
        report.append("")

        # 保存报告
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(report))

        print(f"优化报告已保存到: {output_file}")
        return output_file

    def start_scheduled_optimization(self):
        """启动定时优化任务"""
        # 每天运行一次优化
        schedule.every().day.at("02:00").do(self._run_scheduled_optimization)

        print("定时优化任务已启动，将在每天 02:00 运行")
        print("按 Ctrl+C 停止任务")

        while True:
            schedule.run_pending()
            time.sleep(60)

    def _run_scheduled_optimization(self):
        """运行定时优化任务"""
        print(f"开始定时优化任务: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        results = self.run_optimization()
        report_file = f"skill_optimization_report_{datetime.datetime.now().strftime('%Y%m%d')}.md"
        self.generate_optimization_report(results, report_file)

        print(f"定时优化任务完成: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="MindSymphony 技能持续优化工具")
    parser.add_argument('--run', '-r', action='store_true', help='立即运行优化')
    parser.add_argument('--schedule', '-s', action='store_true', help='启动定时优化任务')
    parser.add_argument('--report', '-o', help='输出优化报告文件')
    parser.add_argument('--config', '-c', help='优化配置文件')

    args = parser.parse_args()

    print("=" * 60)
    print("MindSymphony 技能持续优化工具")
    print("=" * 60)

    optimizer = SkillOptimizer()

    if args.config:
        optimizer.optimization_rules = optimizer._load_optimization_config()

    if args.schedule:
        optimizer.start_scheduled_optimization()
    elif args.run:
        print("正在运行技能优化...")
        results = optimizer.run_optimization()
        print("优化完成！")
        print()

        if args.report:
            optimizer.generate_optimization_report(results, args.report)
        else:
            optimizer.generate_optimization_report(results)
    else:
        parser.print_help()

    print("=" * 60)


if __name__ == "__main__":
    main()