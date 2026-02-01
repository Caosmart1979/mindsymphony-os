#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新技能引入管理工具
New Skill Introduction Management Tool
"""

import yaml
import os
import re
import shutil
import hashlib
from typing import Dict, List, Any, Optional
import argparse
import datetime


class SkillIntroducer:
    """新技能引入管理器"""

    def __init__(self, registry_file: str = r'C:\Users\13466\.claude\skills\mindsymphony\registry\skills.yml',
                 skills_dir: str = r'C:\Users\13466\.claude\skills'):
        """初始化技能引入管理器"""
        self.registry_file = registry_file
        self.skills_dir = skills_dir
        self.registry = self._load_registry()
        self.temp_dir = os.path.join(os.path.dirname(__file__), 'temp_skills')
        os.makedirs(self.temp_dir, exist_ok=True)

    def _load_registry(self) -> Dict:
        """加载技能注册表"""
        try:
            with open(self.registry_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"错误: 无法加载注册表文件 {self.registry_file}: {e}")
            return {'internal_skills': {}, 'external_skills': {}}

    def _save_registry(self):
        """保存技能注册表"""
        try:
            with open(self.registry_file, 'w', encoding='utf-8') as f:
                yaml.dump(self.registry, f, allow_unicode=True, default_flow_style=False)
            print(f"注册表已保存到: {self.registry_file}")
        except Exception as e:
            print(f"错误: 无法保存注册表文件 {self.registry_file}: {e}")

    def _validate_skill_name(self, skill_name: str) -> List[str]:
        """验证技能名称格式"""
        errors = []

        # 检查长度
        if len(skill_name) < 3:
            errors.append("技能名称过短（至少3个字符）")
        if len(skill_name) > 30:
            errors.append("技能名称过长（最多30个字符）")

        # 检查字符规范
        if not re.match(r'^[a-zA-Z0-9-]+$', skill_name):
            errors.append("技能名称包含无效字符，建议使用小写字母、数字和连字符")

        # 检查是否已存在
        if skill_name in self.registry.get('internal_skills', {}) or skill_name in self.registry.get('external_skills', {}):
            errors.append("技能名称已存在")

        return errors

    def _normalize_skill_name(self, raw_name: str) -> str:
        """规范化技能名称"""
        # 转为小写
        normalized = raw_name.lower()
        # 替换无效字符为连字符
        normalized = re.sub(r'[^a-zA-Z0-9-]', '-', normalized)
        # 移除重复的连字符
        normalized = re.sub(r'-+', '-', normalized)
        # 移除首尾的连字符
        normalized = normalized.strip('-')
        # 截断到30个字符
        return normalized[:30]

    def _validate_skill_config(self, skill_config: Dict) -> List[str]:
        """验证技能配置"""
        errors = []

        # 检查描述
        if 'description' not in skill_config or not skill_config['description'] or len(skill_config['description']) < 10:
            errors.append("技能描述缺失或过短（至少10个字符）")

        # 检查路径
        if 'path' not in skill_config or not skill_config['path'] or skill_config['path'] == 'None':
            errors.append("技能路径缺失")
        else:
            if not os.path.exists(skill_config['path']):
                errors.append(f"技能路径不存在: {skill_config['path']}")

        # 检查触发词
        if 'triggers' not in skill_config or not isinstance(skill_config['triggers'], dict):
            errors.append("触发词配置缺失或格式错误")
        else:
            zh_triggers = skill_config['triggers'].get('zh', [])
            en_triggers = skill_config['triggers'].get('en', [])

            if not zh_triggers and not en_triggers:
                errors.append("至少需要一种语言的触发词")

            # 检查中文触发词
            for trigger in zh_triggers:
                if len(trigger) < 2 or len(trigger) > 10:
                    errors.append(f"中文触发词长度不符合要求: {trigger}")

            # 检查英文触发词
            for trigger in en_triggers:
                if len(trigger) < 2 or len(trigger) > 20:
                    errors.append(f"英文触发词长度不符合要求: {trigger}")

        # 检查领域
        if 'domains' not in skill_config or not isinstance(skill_config['domains'], list) or len(skill_config['domains']) == 0:
            errors.append("技能领域配置缺失")

        # 检查优先级
        if 'priority' not in skill_config or not isinstance(skill_config['priority'], int) or not (0 < skill_config['priority'] <= 100):
            errors.append("优先级配置无效（应为1-100的整数）")

        return errors

    def _generate_skill_config(self, skill_path: str) -> Dict:
        """从技能文件生成配置"""
        config = {
            'description': '',
            'path': skill_path,
            'triggers': {'zh': [], 'en': []},
            'domains': [],
            'priority': 50
        }

        # 尝试从SKILL.md或README.md中读取信息
        for filename in ['SKILL.md', 'README.md']:
            readme_path = os.path.join(skill_path, filename)
            if os.path.exists(readme_path):
                try:
                    with open(readme_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # 尝试提取描述（前几行）
                        lines = content.split('\n')
                        for line in lines:
                            line = line.strip()
                            if line and not line.startswith('#'):
                                config['description'] = line[:100]
                                break
                except Exception as e:
                    print(f"警告: 无法读取 {readme_path}: {e}")

        return config

    def _calculate_skill_hash(self, skill_path: str) -> str:
        """计算技能内容的哈希值"""
        hash_obj = hashlib.md5()

        for root, dirs, files in os.walk(skill_path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'rb') as f:
                        for chunk in iter(lambda: f.read(4096), b""):
                            hash_obj.update(chunk)
                except Exception as e:
                    print(f"警告: 无法读取文件 {file_path}: {e}")

        return hash_obj.hexdigest()

    def import_skill_from_file(self, skill_file: str, skill_type: str = 'external') -> Dict:
        """从文件导入技能"""
        if not os.path.exists(skill_file):
            return {'success': False, 'message': f"文件不存在: {skill_file}"}

        try:
            # 解析技能文件
            with open(skill_file, 'r', encoding='utf-8') as f:
                skill_data = yaml.safe_load(f)
        except Exception as e:
            return {'success': False, 'message': f"无法解析技能文件: {e}"}

        # 验证技能数据
        if 'name' not in skill_data:
            return {'success': False, 'message': "技能文件缺少'name'字段"}

        # 规范化技能名称
        original_name = skill_data['name']
        normalized_name = self._normalize_skill_name(original_name)

        # 验证技能名称
        name_errors = self._validate_skill_name(normalized_name)
        if name_errors:
            return {'success': False, 'message': f"技能名称验证失败: {', '.join(name_errors)}"}

        # 验证技能配置
        config_errors = self._validate_skill_config(skill_data.get('config', {}))
        if config_errors:
            return {'success': False, 'message': f"技能配置验证失败: {', '.join(config_errors)}"}

        # 确定技能存储位置
        if skill_type == 'internal':
            target_dir = os.path.join(self.skills_dir, 'mindsymphony', 'core')
            config_key = 'internal_skills'
        else:
            target_dir = os.path.join(self.skills_dir, skill_data.get('category', 'external'))
            config_key = 'external_skills'

        # 确保目标目录存在
        os.makedirs(target_dir, exist_ok=True)

        # 复制技能文件到目标位置
        skill_dest = os.path.join(target_dir, normalized_name)
        if os.path.exists(skill_dest):
            return {'success': False, 'message': f"技能已存在于目标位置: {skill_dest}"}

        # 如果是目录，复制整个目录
        if os.path.isdir(skill_file):
            shutil.copytree(skill_file, skill_dest)
        else:
            # 如果是文件，创建对应的目录结构
            os.makedirs(skill_dest, exist_ok=True)
            shutil.copy2(skill_file, os.path.join(skill_dest, os.path.basename(skill_file)))

        # 更新技能配置路径
        skill_data['config']['path'] = skill_dest

        # 添加到注册表
        if config_key not in self.registry:
            self.registry[config_key] = {}

        self.registry[config_key][normalized_name] = skill_data['config']
        self._save_registry()

        return {'success': True, 'message': f"技能导入成功: {normalized_name}", 'skill_name': normalized_name}

    def import_skill_from_url(self, url: str, skill_type: str = 'external') -> Dict:
        """从URL导入技能（模拟实现）"""
        # 实际实现需要下载技能文件
        return {'success': False, 'message': "从URL导入功能尚未实现"}

    def validate_existing_skills(self) -> List[Dict]:
        """验证现有技能的配置"""
        invalid_skills = []

        for skill_type in ['internal_skills', 'external_skills']:
            if skill_type not in self.registry:
                continue

            for skill_name, skill_config in self.registry[skill_type].items():
                errors = self._validate_skill_config(skill_config)
                if errors:
                    invalid_skills.append({
                        'name': skill_name,
                        'type': '内部' if skill_type == 'internal_skills' else '外部',
                        'errors': errors
                    })

        return invalid_skills

    def generate_introduction_report(self, imported_skills: List[Dict], invalid_skills: List[Dict]) -> str:
        """生成技能引入报告"""
        report = []

        report.append("# MindSymphony 新技能引入报告")
        report.append("")
        report.append(f"**生成时间**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"**总技能数量**: {len(self.registry.get('internal_skills', {})) + len(self.registry.get('external_skills', {}))}")
        report.append(f"**内部技能**: {len(self.registry.get('internal_skills', {}))}")
        report.append(f"**外部技能**: {len(self.registry.get('external_skills', {}))}")
        report.append("")

        if imported_skills:
            report.append("## 新增技能")
            report.append("")
            report.append("| 技能名称 | 类型 | 状态 | 描述 |")
            report.append("|----------|------|------|------|")

            for skill in imported_skills:
                status = "成功" if skill['success'] else "失败"
                config = self.registry.get('internal_skills', {}).get(skill.get('skill_name', '')) or \
                         self.registry.get('external_skills', {}).get(skill.get('skill_name', ''))
                desc = config.get('description', '') if config else ''
                report.append(f"| {skill.get('skill_name', 'N/A')} | {skill.get('type', 'N/A')} | {status} | {desc[:50]}... |")

            report.append("")

        if invalid_skills:
            report.append("## 配置无效的技能")
            report.append("")
            report.append("| 技能名称 | 类型 | 错误信息 |")
            report.append("|----------|------|----------|")

            for skill in invalid_skills:
                report.append(f"| {skill['name']} | {skill['type']} | {', '.join(skill['errors'])} |")

            report.append("")

        report.append("## 改进建议")
        report.append("")

        if invalid_skills:
            report.append("### 配置修复建议")
            report.append("")
            report.append("- 检查技能路径是否存在")
            report.append("- 完善技能描述，确保长度足够")
            report.append("- 优化触发词，确保中英文触发词符合长度要求")
            report.append("- 检查技能领域配置是否完整")
            report.append("- 确保优先级配置在1-100范围内")
            report.append("")

        report.append("### 技能管理建议")
        report.append("")
        report.append("- 定期运行技能验证，确保配置有效性")
        report.append("- 建立技能引入审核机制")
        report.append("- 维护技能使用文档和最佳实践")
        report.append("- 定期评估技能使用效果，优化技能库")

        return "\n".join(report)

    def clean_temp_files(self):
        """清理临时文件"""
        if os.path.exists(self.temp_dir):
            try:
                shutil.rmtree(self.temp_dir)
            except Exception as e:
                print(f"警告: 无法清理临时文件: {e}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="MindSymphony 新技能引入管理工具")
    parser.add_argument('--import-file', '-f', help='要导入的技能文件或目录路径')
    parser.add_argument('--import-url', '-u', help='要导入的技能URL')
    parser.add_argument('--type', '-t', choices=['internal', 'external'],
                      default='external', help='技能类型（内部/外部，默认外部）')
    parser.add_argument('--validate', '-v', action='store_true',
                      help='验证现有技能配置')
    parser.add_argument('--report', '-r', help='生成技能引入报告的输出文件')

    args = parser.parse_args()

    print("=" * 60)
    print("MindSymphony 新技能引入管理工具")
    print("=" * 60)

    introducer = SkillIntroducer()

    imported_skills = []
    invalid_skills = []

    try:
        if args.import_file:
            print(f"正在从文件导入技能: {args.import_file}")
            result = introducer.import_skill_from_file(args.import_file, args.type)
            imported_skills.append({**result, 'type': args.type})
            print(result['message'])
            print()

        if args.import_url:
            print(f"正在从URL导入技能: {args.import_url}")
            result = introducer.import_skill_from_url(args.import_url, args.type)
            imported_skills.append({**result, 'type': args.type})
            print(result['message'])
            print()

        if args.validate:
            print("正在验证现有技能配置...")
            invalid_skills = introducer.validate_existing_skills()
            print(f"发现 {len(invalid_skills)} 个配置无效的技能")
            print()

        if args.report or imported_skills or invalid_skills:
            report_file = args.report if args.report else 'skill_introduction_report.md'
            print(f"正在生成技能引入报告: {report_file}")
            report = introducer.generate_introduction_report(imported_skills, invalid_skills)

            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)

            print(f"报告已保存到: {report_file}")
            print()

        # 显示统计信息
        total_skills = len(introducer.registry.get('internal_skills', {})) + len(introducer.registry.get('external_skills', {}))
        internal_skills = len(introducer.registry.get('internal_skills', {}))
        external_skills = len(introducer.registry.get('external_skills', {}))

        print("技能库统计:")
        print(f"  总技能数量: {total_skills}")
        print(f"  内部技能: {internal_skills}")
        print(f"  外部技能: {external_skills}")
        print()

        if invalid_skills:
            print("配置无效的技能:")
            for skill in invalid_skills:
                print(f"  - {skill['name']} ({skill['type']}): {', '.join(skill['errors'])}")

    finally:
        introducer.clean_temp_files()

    print()
    print("=" * 60)
    print("技能引入管理完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()