#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能去重与合并工具
Skill Deduplication and Merging Tool
"""

import yaml
import os
import re
import Levenshtein
from typing import Dict, List, Any, Optional
import argparse


class SkillDeduplicator:
    """技能去重与合并器"""

    def __init__(self, registry_file: str = r'C:\Users\13466\.claude\skills\mindsymphony\registry\skills.yml'):
        """初始化技能去重器"""
        self.registry_file = registry_file
        self.registry = self._load_registry()
        self.similar_skills = []

    def _load_registry(self) -> Dict:
        """加载技能注册表"""
        try:
            with open(self.registry_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"错误: 无法加载注册表文件 {self.registry_file}: {e}")
            return {}

    def _calculate_name_similarity(self, name1: str, name2: str) -> float:
        """计算技能名称相似度（使用Levenshtein距离）"""
        name1 = name1.lower().strip()
        name2 = name2.lower().strip()

        # 计算编辑距离相似度
        distance = Levenshtein.distance(name1, name2)
        max_len = max(len(name1), len(name2))
        if max_len == 0:
            return 0.0

        return (1 - distance / max_len) * 100

    def _calculate_description_similarity(self, desc1: str, desc2: str) -> float:
        """计算技能描述相似度（使用Levenshtein距离）"""
        if not desc1 or not desc2:
            return 0.0

        desc1 = desc1.lower().strip()
        desc2 = desc2.lower().strip()

        # 计算编辑距离相似度
        distance = Levenshtein.distance(desc1, desc2)
        max_len = max(len(desc1), len(desc2))
        if max_len == 0:
            return 0.0

        return (1 - distance / max_len) * 100

    def _calculate_trigger_similarity(self, triggers1: Dict, triggers2: Dict) -> float:
        """计算触发词相似度"""
        if not triggers1 or not triggers2:
            return 0.0

        # 合并中英文触发词
        all_triggers1 = set()
        if 'zh' in triggers1 and isinstance(triggers1['zh'], list):
            all_triggers1.update([t.lower().strip() for t in triggers1['zh'] if t])
        if 'en' in triggers1 and isinstance(triggers1['en'], list):
            all_triggers1.update([t.lower().strip() for t in triggers1['en'] if t])

        all_triggers2 = set()
        if 'zh' in triggers2 and isinstance(triggers2['zh'], list):
            all_triggers2.update([t.lower().strip() for t in triggers2['zh'] if t])
        if 'en' in triggers2 and isinstance(triggers2['en'], list):
            all_triggers2.update([t.lower().strip() for t in triggers2['en'] if t])

        if not all_triggers1 or not all_triggers2:
            return 0.0

        # 计算Jaccard相似度
        intersection = len(all_triggers1 & all_triggers2)
        union = len(all_triggers1 | all_triggers2)

        return (intersection / union) * 100

    def find_similar_skills(self, similarity_threshold: float = 80) -> List[Dict]:
        """查找相似技能"""
        similar_skills = []
        all_skills = []

        # 收集所有技能
        if 'internal_skills' in self.registry:
            for skill_name, skill_config in self.registry['internal_skills'].items():
                all_skills.append({
                    'name': skill_name,
                    'config': skill_config,
                    'type': 'internal'
                })

        if 'external_skills' in self.registry:
            for skill_name, skill_config in self.registry['external_skills'].items():
                all_skills.append({
                    'name': skill_name,
                    'config': skill_config,
                    'type': 'external'
                })

        # 比较所有技能组合
        for i, skill1 in enumerate(all_skills):
            for j, skill2 in enumerate(all_skills):
                if i < j:
                    # 计算综合相似度
                    name_sim = self._calculate_name_similarity(skill1['name'], skill2['name'])
                    desc_sim = self._calculate_description_similarity(
                        skill1['config'].get('description', ''),
                        skill2['config'].get('description', '')
                    )
                    trigger_sim = self._calculate_trigger_similarity(
                        skill1['config'].get('triggers', {}),
                        skill2['config'].get('triggers', {})
                    )

                    # 综合相似度（加权平均）
                    total_sim = (name_sim * 0.5 + desc_sim * 0.3 + trigger_sim * 0.2)

                    if total_sim >= similarity_threshold:
                        similar_skills.append({
                            'skill1': skill1['name'],
                            'skill1_type': skill1['type'],
                            'skill2': skill2['name'],
                            'skill2_type': skill2['type'],
                            'name_similarity': round(name_sim, 1),
                            'desc_similarity': round(desc_sim, 1),
                            'trigger_similarity': round(trigger_sim, 1),
                            'total_similarity': round(total_sim, 1),
                            'suggestion': self._determine_suggestion(skill1, skill2)
                        })

        self.similar_skills = similar_skills
        return similar_skills

    def _determine_suggestion(self, skill1: Dict, skill2: Dict) -> str:
        """确定合并建议"""
        # 根据技能类型和质量决定建议
        if skill1['type'] == 'internal' and skill2['type'] == 'external':
            return '保留内部技能，考虑移除外部技能'
        elif skill1['type'] == 'external' and skill2['type'] == 'internal':
            return '保留内部技能，考虑移除外部技能'
        elif skill1['type'] == 'internal' and skill2['type'] == 'internal':
            return '需要手动评估，可能合并或重命名'
        else:
            # 都是外部技能
            # 检查路径有效性
            skill1_valid = self._is_skill_path_valid(skill1['config'])
            skill2_valid = self._is_skill_path_valid(skill2['config'])

            if skill1_valid and not skill2_valid:
                return '保留路径有效的技能，移除无效技能'
            elif not skill1_valid and skill2_valid:
                return '保留路径有效的技能，移除无效技能'
            else:
                return '需要手动评估，比较技能内容'

    def _is_skill_path_valid(self, skill_config: Dict) -> bool:
        """检查技能路径是否有效"""
        path = skill_config.get('path', '')
        if not path or path == 'None':
            return False

        # 检查路径是否存在
        if path.startswith('/'):
            # 对于以/开头的路径，尝试检查是否在技能目录中
            possible_paths = [
                os.path.join(r'C:\Users\13466\.claude\skills', path.lstrip('/')),
                os.path.join(r'D:\Claudecode\skills\skills', path.lstrip('/'))
            ]
            return any(os.path.exists(p) for p in possible_paths)
        else:
            return os.path.exists(path)

    def analyze_duplicate_patterns(self) -> Dict[str, List[str]]:
        """分析重复模式"""
        patterns = {}

        # 基于名称模式分析
        name_patterns = {}
        for skill in self._get_all_skills():
            # 移除版本号
            normalized_name = re.sub(r'[-.]v?\d+(\.\d+)*', '', skill['name']).lower()
            if normalized_name not in name_patterns:
                name_patterns[normalized_name] = []
            name_patterns[normalized_name].append(skill['name'])

        # 筛选出有重复的模式
        for pattern, skills in name_patterns.items():
            if len(skills) > 1:
                patterns[f"名称模式: {pattern}"] = skills

        # 基于领域分析
        domain_patterns = {}
        for skill in self._get_all_skills():
            domains = skill['config'].get('domains', [])
            for domain in domains:
                if domain not in domain_patterns:
                    domain_patterns[domain] = []
                domain_patterns[domain].append(skill['name'])

        # 筛选出有大量技能的领域
        for domain, skills in domain_patterns.items():
            if len(skills) >= 5:  # 领域中有5个以上技能可能存在重叠
                patterns[f"领域: {domain}"] = skills

        return patterns

    def _get_all_skills(self) -> List[Dict]:
        """获取所有技能列表"""
        all_skills = []

        if 'internal_skills' in self.registry:
            for skill_name, skill_config in self.registry['internal_skills'].items():
                all_skills.append({
                    'name': skill_name,
                    'config': skill_config,
                    'type': 'internal'
                })

        if 'external_skills' in self.registry:
            for skill_name, skill_config in self.registry['external_skills'].items():
                all_skills.append({
                    'name': skill_name,
                    'config': skill_config,
                    'type': 'external'
                })

        return all_skills

    def generate_merge_plan(self, similar_skills: List[Dict]) -> str:
        """生成合并计划"""
        plan = []

        plan.append("# MindSymphony 技能去重与合并计划")
        plan.append("")

        if not similar_skills:
            plan.append("## 没有发现高相似度技能")
            plan.append("技能库质量良好，无明显重复技能。")
            return "\n".join(plan)

        # 分组相似技能
        grouped_skills = self._group_similar_skills(similar_skills)

        plan.append(f"## 相似技能分析结果")
        plan.append(f"- **总技能数量**: {len(self._get_all_skills())}")
        plan.append(f"- **发现相似技能组**: {len(grouped_skills)}")
        plan.append(f"- **涉及技能数量**: {sum(len(group) for group in grouped_skills.values())}")
        plan.append("")

        # 输出每个分组的详细信息
        for i, (group_id, skills) in enumerate(grouped_skills.items(), 1):
            plan.append(f"### 相似技能组 {i}")
            plan.append("")
            plan.append("| 技能名称 | 类型 | 路径 | 主要问题 |")
            plan.append("|----------|------|------|----------|")

            for skill_info in skills:
                skill = next(s for s in self._get_all_skills() if s['name'] == skill_info['name'])
                path = skill['config'].get('path', '')
                issues = []
                if not self._is_skill_path_valid(skill['config']):
                    issues.append("路径无效")
                if len(skill['config'].get('description', '')) < 10:
                    issues.append("描述过短")

                plan.append(f"| {skill['name']} | {skill['type']} | {path} | {', '.join(issues) if issues else '无'} |")

            plan.append("")
            plan.append("**合并建议**:")
            plan.append(skills[0]['suggestion'])
            plan.append("")

            # 相似度矩阵
            plan.append("**相似度矩阵**:")
            plan.append("| 技能1 | 技能2 | 名称相似度 | 描述相似度 | 触发词相似度 | 综合相似度 |")
            plan.append("|-------|-------|------------|------------|--------------|------------|")

            for j in range(len(skills)):
                for k in range(j + 1, len(skills)):
                    skill1 = skills[j]
                    skill2 = skills[k]
                    plan.append(f"| {skill1['name']} | {skill2['name']} | {skill1['name_similarity']}% | {skill1['desc_similarity']}% | {skill1['trigger_similarity']}% | {skill1['total_similarity']}% |")

            plan.append("")

        # 重复模式分析
        patterns = self.analyze_duplicate_patterns()
        if patterns:
            plan.append("## 重复模式分析")
            plan.append("")
            for pattern, skills in patterns.items():
                plan.append(f"### {pattern}")
                plan.append(f"包含 {len(skills)} 个技能: {', '.join(skills)}")
                plan.append("")

        plan.append("## 执行建议")
        plan.append("")
        plan.append("### 优先级 1: 高风险重复")
        plan.append("- 立即处理路径无效的技能")
        plan.append("- 合并名称完全相同或高度相似的技能")
        plan.append("- 移除明显冗余的技能")
        plan.append("")

        plan.append("### 优先级 2: 中等风险")
        plan.append("- 评估领域内技能的重叠性")
        plan.append("- 优化相似技能的触发词")
        plan.append("- 统一技能命名规范")
        plan.append("")

        plan.append("### 优先级 3: 低风险")
        plan.append("- 定期监控技能使用情况")
        plan.append("- 建立技能更新机制")
        plan.append("- 培养技能使用最佳实践")

        return "\n".join(plan)

    def _group_similar_skills(self, similar_skills: List[Dict]) -> Dict[str, List[Dict]]:
        """分组相似技能"""
        groups = {}
        used_skills = set()

        for sim in similar_skills:
            skill1 = sim['skill1']
            skill2 = sim['skill2']

            if skill1 not in used_skills and skill2 not in used_skills:
                # 创建新组
                group_id = f"group_{len(groups) + 1}"
                groups[group_id] = [sim]
                used_skills.add(skill1)
                used_skills.add(skill2)
            elif skill1 in used_skills and skill2 not in used_skills:
                # 加入skill1所在的组
                for group_id, skills in groups.items():
                    if any(s['skill1'] == skill1 or s['skill2'] == skill1 for s in skills):
                        groups[group_id].append(sim)
                        used_skills.add(skill2)
                        break
            elif skill2 in used_skills and skill1 not in used_skills:
                # 加入skill2所在的组
                for group_id, skills in groups.items():
                    if any(s['skill1'] == skill2 or s['skill2'] == skill2 for s in skills):
                        groups[group_id].append(sim)
                        used_skills.add(skill1)
                        break
            else:
                # 两个技能都在不同的组中，合并组
                group1 = None
                group2 = None
                for group_id, skills in groups.items():
                    if any(s['skill1'] == skill1 or s['skill2'] == skill1 for s in skills):
                        group1 = group_id
                    if any(s['skill1'] == skill2 or s['skill2'] == skill2 for s in skills):
                        group2 = group_id

                if group1 and group2 and group1 != group2:
                    groups[group1].extend(groups[group2])
                    del groups[group2]

        return groups

    def execute_merge(self, merge_plan: str, dry_run: bool = True) -> Dict:
        """执行合并操作"""
        if dry_run:
            print("执行模拟合并（不修改实际文件）...")
            return {'success': True, 'message': '模拟合并完成', 'changes': []}

        print("执行实际合并操作...")
        return {'success': False, 'message': '实际合并功能需要进一步实现', 'changes': []}

    def generate_report(self, similar_skills: List[Dict], output_file: str = 'skill_deduplication_report.md') -> str:
        """生成去重报告"""
        report = []

        report.append("# MindSymphony 技能去重分析报告")
        report.append("")

        if not similar_skills:
            report.append("## 没有发现相似技能")
            report.append("技能库质量良好，无明显重复或高度相似的技能。")
        else:
            report.append(f"## 相似技能统计")
            report.append(f"- **总技能数量**: {len(self._get_all_skills())}")
            report.append(f"- **内部技能**: {len(self.registry.get('internal_skills', {}))}")
            report.append(f"- **外部技能**: {len(self.registry.get('external_skills', {}))}")
            report.append(f"- **发现相似技能对**: {len(similar_skills)}")
            report.append("")

            report.append("## 相似技能详细信息")
            report.append("")
            report.append("| 技能1 | 技能1类型 | 技能2 | 技能2类型 | 名称相似度 | 描述相似度 | 触发词相似度 | 综合相似度 | 合并建议 |")
            report.append("|-------|----------|-------|----------|------------|------------|--------------|------------|----------|")

            for sim in similar_skills:
                report.append(f"| {sim['skill1']} | {sim['skill1_type']} | {sim['skill2']} | {sim['skill2_type']} | {sim['name_similarity']}% | {sim['desc_similarity']}% | {sim['trigger_similarity']}% | {sim['total_similarity']}% | {sim['suggestion']} |")

            report.append("")

            # 重复模式分析
            patterns = self.analyze_duplicate_patterns()
            if patterns:
                report.append("## 重复模式分析")
                report.append("")
                for pattern, skills in patterns.items():
                    report.append(f"### {pattern}")
                    report.append(f"包含 {len(skills)} 个技能:")
                    report.append("")
                    for skill in skills:
                        report.append(f"- {skill}")
                    report.append("")

        report.append("## 优化建议")
        report.append("")

        if similar_skills:
            report.append("### 高优先级优化")
            report.append("- 立即处理路径无效的技能")
            report.append("- 合并高度相似的技能以减少冗余")
            report.append("- 统一技能命名规范")
            report.append("")

        report.append("### 中优先级优化")
        report.append("- 定期评估技能使用情况")
        report.append("- 优化技能触发词以减少重叠")
        report.append("- 建立技能生命周期管理机制")
        report.append("")

        report.append("### 低优先级优化")
        report.append("- 建立技能使用最佳实践文档")
        report.append("- 培养团队技能使用习惯")
        report.append("- 监控技能使用趋势")

        report_text = "\n".join(report)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report_text)

        print(f"去重报告已保存到: {output_file}")

        return report_text


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="MindSymphony 技能去重与合并工具")
    parser.add_argument('--registry', '-r',
                      default=r'C:\Users\13466\.claude\skills\mindsymphony\registry\skills.yml',
                      help='技能注册表文件路径')
    parser.add_argument('--output', '-o',
                      default='skill_deduplication_report.md',
                      help='去重报告输出文件')
    parser.add_argument('--threshold', '-t',
                      type=float,
                      default=80.0,
                      help='相似度阈值 (0-100，默认80)')
    parser.add_argument('--plan', '-p',
                      action='store_true',
                      help='生成合并计划')
    parser.add_argument('--execute', '-e',
                      action='store_true',
                      help='执行合并操作（警告：会修改实际文件）')
    parser.add_argument('--dry-run', '-d',
                      action='store_true',
                      help='执行模拟合并（不修改实际文件）')

    args = parser.parse_args()

    print("=" * 60)
    print("MindSymphony 技能去重与合并工具")
    print("=" * 60)
    print(f"评估文件: {args.registry}")
    print(f"相似度阈值: {args.threshold}%")
    print()

    # 创建去重器
    deduplicator = SkillDeduplicator(args.registry)

    # 查找相似技能
    print("正在查找相似技能...")
    similar_skills = deduplicator.find_similar_skills(args.threshold)

    print(f"找到 {len(similar_skills)} 对相似技能")
    print()

    # 生成报告
    print("正在生成去重报告...")
    report = deduplicator.generate_report(similar_skills, args.output)

    print()
    print("=" * 60)
    print("去重分析完成！")
    print("=" * 60)
    print()
    print(f"报告已保存到: {args.output}")
    print()

    # 显示统计摘要
    if similar_skills:
        print("相似技能统计:")
        internal_pairs = sum(1 for s in similar_skills if s['skill1_type'] == 'internal' or s['skill2_type'] == 'internal')
        external_pairs = sum(1 for s in similar_skills if s['skill1_type'] == 'external' and s['skill2_type'] == 'external')
        print(f"  内部技能相关: {internal_pairs} 对")
        print(f"  外部技能相关: {external_pairs} 对")
        print()

        # 显示相似度分布
        sim_ranges = {
            '80-85%': 0,
            '85-90%': 0,
            '90-95%': 0,
            '95-100%': 0
        }

        for sim in similar_skills:
            if 80 <= sim['total_similarity'] < 85:
                sim_ranges['80-85%'] += 1
            elif 85 <= sim['total_similarity'] < 90:
                sim_ranges['85-90%'] += 1
            elif 90 <= sim['total_similarity'] < 95:
                sim_ranges['90-95%'] += 1
            elif 95 <= sim['total_similarity'] <= 100:
                sim_ranges['95-100%'] += 1

        print("相似度分布:")
        for range_str, count in sim_ranges.items():
            if count > 0:
                print(f"  {range_str}: {count} 对")

    # 生成合并计划
    if args.plan:
        print()
        print("正在生成合并计划...")
        plan = deduplicator.generate_merge_plan(similar_skills)
        plan_file = args.output.replace('.md', '_plan.md')
        with open(plan_file, 'w', encoding='utf-8') as f:
            f.write(plan)
        print(f"合并计划已保存到: {plan_file}")

    # 执行合并
    if args.execute:
        print()
        print("警告: 即将执行实际合并操作，这会修改技能注册表！")
        if not args.dry_run:
            confirm = input("请输入 'YES' 确认执行: ")
            if confirm != 'YES':
                print("操作已取消")
                return

        result = deduplicator.execute_merge(report, args.dry_run)
        print()
        print(result['message'])
        if result['changes']:
            print("变更详情:")
            for change in result['changes']:
                print(f"- {change}")


if __name__ == "__main__":
    main()