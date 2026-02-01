#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能使用指南生成工具
Skill Usage Guide Generation Tool
"""

import yaml
import os
import re
import datetime
from typing import Dict, List, Any, Optional
import argparse


class SkillUsageGuideGenerator:
    """技能使用指南生成器"""

    def __init__(self, registry_file: str = r'C:\Users\13466\.claude\skills\mindsymphony\registry\skills.yml'):
        """初始化技能使用指南生成器"""
        self.registry_file = registry_file
        self.registry = self._load_registry()

    def _load_registry(self) -> Dict:
        """加载技能注册表"""
        try:
            with open(self.registry_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"错误: 无法加载注册表文件 {self.registry_file}: {e}")
            return {'internal_skills': {}, 'external_skills': {}}

    def _extract_skill_info(self, skill_name: str, skill_config: Dict, skill_type: str) -> Dict:
        """提取技能信息"""
        info = {
            'name': skill_name,
            'type': '内部技能' if skill_type == 'internal' else '外部技能',
            'description': skill_config.get('description', '无描述'),
            'path': skill_config.get('path', '无路径'),
            'priority': skill_config.get('priority', 50),
            'domains': skill_config.get('domains', []),
            'triggers': skill_config.get('triggers', {'zh': [], 'en': []}),
            'examples': self._extract_examples(skill_config)
        }

        return info

    def _extract_examples(self, skill_config: Dict) -> List[str]:
        """从技能配置中提取使用示例"""
        examples = []

        # 尝试从描述中提取示例
        description = skill_config.get('description', '')
        match = re.search(r'示例[:：]?\s*(.*?)(?:\.|$)', description, re.DOTALL)
        if match:
            examples.extend([e.strip() for e in match.group(1).split(';') if e.strip()])

        # 尝试从专门的示例字段中提取
        if 'examples' in skill_config:
            if isinstance(skill_config['examples'], list):
                examples.extend([e.strip() for e in skill_config['examples'] if e.strip()])
            elif isinstance(skill_config['examples'], str):
                examples.extend([e.strip() for e in skill_config['examples'].split(';') if e.strip()])

        # 尝试从技能文件中提取示例（如果有路径）
        path = skill_config.get('path', '')
        if path and os.path.exists(path):
            examples.extend(self._extract_examples_from_file(path))

        return examples

    def _extract_examples_from_file(self, skill_path: str) -> List[str]:
        """从技能文件中提取使用示例"""
        examples = []

        # 检查是否是目录
        if os.path.isdir(skill_path):
            # 查找SKILL.md或README.md文件
            for filename in ['SKILL.md', 'README.md']:
                readme_path = os.path.join(skill_path, filename)
                if os.path.exists(readme_path):
                    examples.extend(self._parse_markdown_examples(readme_path))
        else:
            # 直接解析文件
            if skill_path.endswith('.md'):
                examples.extend(self._parse_markdown_examples(skill_path))

        return examples

    def _parse_markdown_examples(self, file_path: str) -> List[str]:
        """解析Markdown文件中的示例"""
        examples = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 查找示例部分
            example_patterns = [
                r'## 示例.*?(?=##|$)',
                r'### 示例.*?(?=###|$)',
                r'#### 示例.*?(?=####|$)',
                r'## 使用示例.*?(?=##|$)',
                r'### 使用示例.*?(?=###|$)',
                r'#### 使用示例.*?(?=####|$)'
            ]

            for pattern in example_patterns:
                matches = re.findall(pattern, content, re.DOTALL)
                for match in matches:
                    # 提取代码块或列表项
                    code_blocks = re.findall(r'```.*?```', match, re.DOTALL)
                    examples.extend([block.strip() for block in code_blocks])

                    list_items = re.findall(r'^\s*[-*+]\s*(.*)$', match, re.MULTILINE)
                    examples.extend([item.strip() for item in list_items])

        except Exception as e:
            print(f"警告: 无法解析文件 {file_path}: {e}")

        return examples

    def _generate_skill_guide(self, skill_info: Dict) -> str:
        """生成单个技能的使用指南"""
        guide = []

        # 技能基本信息
        guide.append(f"# {skill_info['name']}")
        guide.append("")
        guide.append(f"**类型**: {skill_info['type']}")
        guide.append(f"**优先级**: {skill_info['priority']}")
        guide.append("")

        # 技能描述
        guide.append("## 技能描述")
        guide.append("")
        guide.append(skill_info['description'])
        guide.append("")

        # 适用领域
        if skill_info['domains']:
            guide.append("## 适用领域")
            guide.append("")
            for domain in skill_info['domains']:
                guide.append(f"- {domain}")
            guide.append("")

        # 触发词
        guide.append("## 触发词")
        guide.append("")
        if skill_info['triggers']['zh']:
            guide.append("### 中文触发词")
            guide.append("")
            for trigger in skill_info['triggers']['zh']:
                guide.append(f"- {trigger}")
            guide.append("")

        if skill_info['triggers']['en']:
            guide.append("### 英文触发词")
            guide.append("")
            for trigger in skill_info['triggers']['en']:
                guide.append(f"- {trigger}")
            guide.append("")

        # 使用示例
        if skill_info['examples']:
            guide.append("## 使用示例")
            guide.append("")
            for i, example in enumerate(skill_info['examples'], 1):
                guide.append(f"### 示例 {i}")
                guide.append("")
                guide.append(example)
                guide.append("")

        # 使用建议
        guide.append("## 使用建议")
        guide.append("")

        if skill_info['type'] == '内部技能':
            guide.append("- 内部技能是系统核心能力，建议在复杂任务中使用")
            guide.append("- 可以与其他内部技能组合使用，发挥协同效应")
            guide.append("- 如有问题，建议查看源代码进行调试")
        else:
            guide.append("- 外部技能是扩展能力，提供专业领域的功能")
            guide.append("- 建议在明确的使用场景下使用，避免滥用")
            guide.append("- 使用前建议先测试效果")

        guide.append("")
        guide.append("- 每次使用后可以记录反馈，帮助优化技能")
        guide.append("- 定期清理不常用的技能，保持技能库的健康")
        guide.append("")

        # 技能路径信息
        guide.append("## 技术信息")
        guide.append("")
        guide.append(f"**技能路径**: {skill_info['path']}")
        guide.append(f"**文件状态**: {'存在' if os.path.exists(skill_info['path']) else '不存在'}")
        guide.append("")

        return "\n".join(guide)

    def generate_all_guides(self, output_dir: str = 'skill_guides'):
        """生成所有技能的使用指南"""
        os.makedirs(output_dir, exist_ok=True)

        guides = []

        # 生成内部技能指南
        if 'internal_skills' in self.registry:
            internal_dir = os.path.join(output_dir, 'internal')
            os.makedirs(internal_dir, exist_ok=True)

            for skill_name, skill_config in self.registry['internal_skills'].items():
                skill_info = self._extract_skill_info(skill_name, skill_config, 'internal')
                guide = self._generate_skill_guide(skill_info)
                output_file = os.path.join(internal_dir, f"{skill_name}.md")

                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(guide)

                guides.append({
                    'name': skill_name,
                    'type': 'internal',
                    'path': output_file,
                    'status': '成功'
                })
                print(f"已生成内部技能指南: {skill_name}")

        # 生成外部技能指南
        if 'external_skills' in self.registry:
            external_dir = os.path.join(output_dir, 'external')
            os.makedirs(external_dir, exist_ok=True)

            for skill_name, skill_config in self.registry['external_skills'].items():
                skill_info = self._extract_skill_info(skill_name, skill_config, 'external')
                guide = self._generate_skill_guide(skill_info)
                output_file = os.path.join(external_dir, f"{skill_name}.md")

                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(guide)

                guides.append({
                    'name': skill_name,
                    'type': 'external',
                    'path': output_file,
                    'status': '成功'
                })
                print(f"已生成外部技能指南: {skill_name}")

        return guides

    def generate_index(self, output_dir: str = 'skill_guides'):
        """生成技能指南索引"""
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)

        index = []

        index.append("# MindSymphony 技能使用指南索引")
        index.append("")
        index.append(f"**生成时间**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        index.append(f"**技能总数**: {len(self.registry.get('internal_skills', {})) + len(self.registry.get('external_skills', {}))}")
        index.append("")

        # 内部技能索引
        if 'internal_skills' in self.registry:
            index.append("## 内部技能")
            index.append("")
            index.append("| 技能名称 | 优先级 | 适用领域 | 描述 |")
            index.append("|----------|--------|----------|------|")

            for skill_name, skill_config in sorted(self.registry['internal_skills'].items()):
                domains = ', '.join(skill_config.get('domains', []))
                desc = skill_config.get('description', '')[:50] + '...'
                index.append(f"| [{skill_name}](./internal/{skill_name}.md) | {skill_config.get('priority', 50)} | {domains} | {desc} |")

            index.append("")

        # 外部技能索引
        if 'external_skills' in self.registry:
            index.append("## 外部技能")
            index.append("")
            index.append("| 技能名称 | 优先级 | 适用领域 | 描述 |")
            index.append("|----------|--------|----------|------|")

            for skill_name, skill_config in sorted(self.registry['external_skills'].items()):
                domains = ', '.join(skill_config.get('domains', []))
                desc = skill_config.get('description', '')[:50] + '...'
                index.append(f"| [{skill_name}](./external/{skill_name}.md) | {skill_config.get('priority', 50)} | {domains} | {desc} |")

            index.append("")

        # 使用说明
        index.append("## 使用说明")
        index.append("")
        index.append("1. **如何找到技能**: 使用浏览器打开 `index.md` 文件")
        index.append("2. **查看技能详情**: 点击技能名称链接查看详细指南")
        index.append("3. **搜索功能**: 使用浏览器的搜索功能查找关键词")
        index.append("4. **定期更新**: 建议定期重新生成指南以保持同步")
        index.append("")

        # 生成索引文件
        output_file = os.path.join(output_dir, 'index.md')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(index))

        print(f"已生成技能指南索引: {output_file}")
        return output_file

    def generate_domain_index(self, output_dir: str = 'skill_guides'):
        """生成按领域分类的技能索引"""
        domain_index = {}

        # 收集按领域分类的技能
        for skill_type in ['internal_skills', 'external_skills']:
            if skill_type not in self.registry:
                continue

            for skill_name, skill_config in self.registry[skill_type].items():
                domains = skill_config.get('domains', [])
                for domain in domains:
                    if domain not in domain_index:
                        domain_index[domain] = []

                    domain_index[domain].append({
                        'name': skill_name,
                        'type': '内部' if skill_type == 'internal_skills' else '外部',
                        'priority': skill_config.get('priority', 50),
                        'description': skill_config.get('description', '')
                    })

        # 生成领域索引文件
        domain_index_file = os.path.join(output_dir, 'domain_index.md')
        domain_content = []

        domain_content.append("# 按领域分类的技能索引")
        domain_content.append("")
        domain_content.append(f"**生成时间**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        domain_content.append(f"**领域数量**: {len(domain_index)}")
        domain_content.append("")

        for domain in sorted(domain_index.keys()):
            domain_content.append(f"## {domain}")
            domain_content.append("")
            domain_content.append("| 技能名称 | 类型 | 优先级 | 描述 |")
            domain_content.append("|----------|------|--------|------|")

            for skill in sorted(domain_index[domain], key=lambda x: x['priority'], reverse=True):
                skill_file = f"{skill['name']}.md"
                skill_path = os.path.join('internal' if skill['type'] == '内部' else 'external', skill_file)
                desc = skill['description'][:50] + '...'
                domain_content.append(f"| [{skill['name']}]({skill_path}) | {skill['type']} | {skill['priority']} | {desc} |")

            domain_content.append("")

        with open(domain_index_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(domain_content))

        print(f"已生成领域分类索引: {domain_index_file}")
        return domain_index_file

    def generate_quick_reference(self, output_dir: str = 'skill_guides'):
        """生成技能快速参考卡片"""
        quick_ref_file = os.path.join(output_dir, 'quick_reference.md')
        quick_ref = []

        quick_ref.append("# 技能快速参考")
        quick_ref.append("")
        quick_ref.append(f"**生成时间**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        quick_ref.append("")

        quick_ref.append("## 内部技能")
        quick_ref.append("")
        quick_ref.append("| 技能名称 | 触发词 | 描述 |")
        quick_ref.append("|----------|--------|------|")

        if 'internal_skills' in self.registry:
            for skill_name, skill_config in sorted(self.registry['internal_skills'].items()):
                triggers = ', '.join(skill_config.get('triggers', {}).get('zh', []))
                desc = skill_config.get('description', '')[:30] + '...'
                quick_ref.append(f"| [{skill_name}](./internal/{skill_name}.md) | {triggers} | {desc} |")

        quick_ref.append("")

        quick_ref.append("## 外部技能")
        quick_ref.append("")
        quick_ref.append("| 技能名称 | 触发词 | 描述 |")
        quick_ref.append("|----------|--------|------|")

        if 'external_skills' in self.registry:
            for skill_name, skill_config in sorted(self.registry['external_skills'].items()):
                triggers = ', '.join(skill_config.get('triggers', {}).get('zh', []))
                desc = skill_config.get('description', '')[:30] + '...'
                quick_ref.append(f"| [{skill_name}](./external/{skill_name}.md) | {triggers} | {desc} |")

        with open(quick_ref_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(quick_ref))

        print(f"已生成快速参考卡片: {quick_ref_file}")
        return quick_ref_file


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="MindSymphony 技能使用指南生成工具")
    parser.add_argument('--output', '-o', default='skill_guides', help='输出目录（默认: skill_guides）')
    parser.add_argument('--single', '-s', help='只生成单个技能的指南')
    parser.add_argument('--index-only', '-i', action='store_true', help='只生成索引文件')
    parser.add_argument('--domain-index', '-d', action='store_true', help='生成领域分类索引')
    parser.add_argument('--quick-ref', '-q', action='store_true', help='生成快速参考卡片')

    args = parser.parse_args()

    print("=" * 60)
    print("MindSymphony 技能使用指南生成工具")
    print("=" * 60)
    print(f"输出目录: {args.output}")
    print()

    generator = SkillUsageGuideGenerator()

    if args.single:
        # 查找技能
        found = False
        skill_info = None

        if 'internal_skills' in generator.registry and args.single in generator.registry['internal_skills']:
            skill_info = generator._extract_skill_info(args.single, generator.registry['internal_skills'][args.single], 'internal')
            found = True
        elif 'external_skills' in generator.registry and args.single in generator.registry['external_skills']:
            skill_info = generator._extract_skill_info(args.single, generator.registry['external_skills'][args.single], 'external')
            found = True

        if found:
            guide = generator._generate_skill_guide(skill_info)
            output_file = os.path.join(args.output, f"{args.single}.md")

            os.makedirs(args.output, exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(guide)

            print(f"已生成技能指南: {args.single}")
            print(f"文件路径: {output_file}")
        else:
            print(f"错误: 未找到技能 '{args.single}'")

    elif args.index_only:
        # 只生成索引
        generator.generate_index(args.output)

    else:
        # 生成所有指南
        print("正在生成技能使用指南...")
        guides = generator.generate_all_guides(args.output)
        print(f"已生成 {len(guides)} 个技能指南")
        print()

        # 生成索引
        generator.generate_index(args.output)

        # 生成领域分类索引
        if args.domain_index:
            generator.generate_domain_index(args.output)

        # 生成快速参考卡片
        if args.quick_ref:
            generator.generate_quick_reference(args.output)

        print()
        print("技能使用指南生成完成！")

    print()
    print("=" * 60)


if __name__ == "__main__":
    main()