#!/usr/bin/env python3
"""
MindSymphony 外部技能扫描器
扫描 .agents/skills/ 目录，更新 external-skills-index.yml
"""

import os
import re
import yaml
from pathlib import Path
from datetime import datetime

# 配置
SOURCE_DIR = Path(".agents/skills")
INDEX_FILE = Path("C:/Users/13466/.claude/skills/mindsymphony/registry/external-skills-index.yml")

# 层级分类规则
TIER_MAPPING = {
    "engineering": ["vercel-composition-patterns", "vercel-react-best-practices",
                    "vercel-react-native-skills", "find-skills"],
    "creative": ["web-design-guidelines"],
    "custom": ["my-local-skill"]
}

def get_tier(skill_name: str) -> str:
    """根据技能名确定道法术器层级"""
    for tier, skills in [
        ("术", TIER_MAPPING["engineering"] + TIER_MAPPING["creative"]),
        ("器", ["find-skills"] + TIER_MAPPING["custom"]),
    ]:
        if skill_name in skills:
            return tier
    return "器"  # 默认

def get_category(skill_name: str) -> str:
    """根据技能名确定分类"""
    for cat, skills in TIER_MAPPING.items():
        if skill_name in skills:
            return cat
    return "general"

def parse_skill_md(skill_path: Path) -> dict:
    """解析 SKILL.md 文件，提取元数据"""
    try:
        content = skill_path.read_text(encoding='utf-8')

        # 提取 frontmatter
        frontmatter_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        if not frontmatter_match:
            return None

        try:
            metadata = yaml.safe_load(frontmatter_match.group(1))
        except yaml.YAMLError:
            return None

        if not metadata:
            return None

        name = metadata.get('name', skill_path.parent.name)
        return {
            'name': name,
            'description': metadata.get('description', ''),
            'version': metadata.get('metadata', {}).get('version', 'unknown'),
            'author': metadata.get('metadata', {}).get('author', 'unknown'),
            'license': metadata.get('license', 'unknown'),
            'path': str(skill_path.parent).replace('\\', '/'),
            'tier': get_tier(name),
            'category': get_category(name),
            'status': 'active'
        }
    except Exception as e:
        print(f"解析失败 {skill_path}: {e}")
        return None

def scan_skills():
    """扫描目录并生成索引"""
    skills = []

    if not SOURCE_DIR.exists():
        print(f"源目录不存在: {SOURCE_DIR}")
        return []

    for skill_dir in SOURCE_DIR.iterdir():
        if not skill_dir.is_dir():
            continue

        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue

        skill_info = parse_skill_md(skill_md)
        if skill_info:
            skills.append(skill_info)
            print(f"✓ 发现技能: {skill_info['name']} ({skill_info['tier']})")

    return skills

def generate_index(skills: list):
    """生成索引文件"""
    stats = {
        'total': len(skills),
        'by_tier': {'道': 0, '法': 0, '术': 0, '器': 0},
        'by_category': {}
    }

    for skill in skills:
        stats['by_tier'][skill['tier']] = stats['by_tier'].get(skill['tier'], 0) + 1
        cat = skill['category']
        stats['by_category'][cat] = stats['by_category'].get(cat, 0) + 1

    index_data = {
        'version': '1.0.0',
        'last_scan': datetime.now().strftime('%Y-%m-%d'),
        'source_directory': str(SOURCE_DIR).replace('\\', '/'),
        'external_skills': skills,
        'stats': stats,
        'scan_config': {
            'auto_scan': True,
            'scan_on_startup': False,
            'watch_directory': str(SOURCE_DIR).replace('\\', '/')
        }
    }

    INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write("# MindSymphony 外部技能索引\n")
        f.write("# 自动生成，请勿手动修改\n")
        f.write(f"# 生成时间: {datetime.now()}\n\n")
        yaml.dump(index_data, f, allow_unicode=True, sort_keys=False)

    print(f"\n✅ 索引已更新: {INDEX_FILE}")
    print(f"   共 {stats['total']} 个技能")
    print(f"   道: {stats['by_tier']['道']}, 法: {stats['by_tier']['法']}, "
          f"术: {stats['by_tier']['术']}, 器: {stats['by_tier']['器']}")

def main():
    print("🔍 扫描外部技能...")
    print(f"   源目录: {SOURCE_DIR.absolute()}")
    print()

    skills = scan_skills()
    if skills:
        generate_index(skills)
    else:
        print("\n⚠️ 未找到任何技能")

if __name__ == "__main__":
    main()
