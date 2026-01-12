"""
技能元数据加载模块
负责从 SKILL.md 和 INTEROP.yml 加载技能元数据
"""

import os
import re
import yaml
from typing import Dict, List, Optional, Any
from pathlib import Path


class SkillMetadata:
    """技能元数据类"""

    def __init__(self, skill_dir: str):
        self.skill_dir = skill_dir
        self.skill_name = os.path.basename(skill_dir)
        self.metadata = {}
        self._mtime = 0
        self._load()

    def _load(self):
        """加载技能元数据"""
        skill_md = os.path.join(self.skill_dir, 'SKILL.md')
        interop_yml = os.path.join(self.skill_dir, 'INTEROP.yml')

        # 获取修改时间
        if os.path.exists(skill_md):
            self._mtime = os.path.getmtime(skill_md)

        # 加载 SKILL.md frontmatter
        if os.path.exists(skill_md):
            frontmatter = self._parse_frontmatter(skill_md)
            self.metadata.update(frontmatter)

        # 加载 INTEROP.yml（如果存在）
        if os.path.exists(interop_yml):
            with open(interop_yml, 'r', encoding='utf-8') as f:
                interop_data = yaml.safe_load(f)
                self.metadata.update(interop_data)

        # 添加基础信息
        self.metadata['name'] = self.metadata.get('name', self.skill_name)
        self.metadata['_mtime'] = self._mtime
        self.metadata['_path'] = self.skill_dir

    def _parse_frontmatter(self, skill_md: str) -> Dict[str, Any]:
        """解析 SKILL.md 的 YAML frontmatter"""
        with open(skill_md, 'r', encoding='utf-8') as f:
            content = f.read()

        # 匹配 --- 包围的 YAML
        match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if match:
            try:
                return yaml.safe_load(match.group(1)) or {}
            except yaml.YAMLError:
                return {}

        return {}

    def get(self, key: str, default: Any = None) -> Any:
        """获取元数据字段"""
        return self.metadata.get(key, default)

    def provides(self) -> List[str]:
        """获取提供的能力列表"""
        provides = self.metadata.get('provides', [])
        if isinstance(provides, str):
            return [provides]

        # 如果是字典列表，提取 id 字段
        result = []
        for item in provides:
            if isinstance(item, dict):
                result.append(item.get('id', str(item)))
            else:
                result.append(item)
        return result

    def consumes(self) -> List[str]:
        """获取消耗的能力列表"""
        consumes = self.metadata.get('consumes', [])
        if isinstance(consumes, str):
            return [consumes]

        # 如果是字典列表，提取 id 字段
        result = []
        for item in consumes:
            if isinstance(item, dict):
                result.append(item.get('id', str(item)))
            else:
                result.append(item)
        return result

    def triggers(self) -> List[Dict[str, Any]]:
        """获取触发条件列表"""
        triggers = self.metadata.get('triggers', [])
        if isinstance(triggers, dict):
            return [triggers]
        return triggers

    def is_stale(self) -> bool:
        """检查技能元数据是否过期"""
        skill_md = os.path.join(self.skill_dir, 'SKILL.md')
        if not os.path.exists(skill_md):
            return True
        return os.path.getmtime(skill_md) > self._mtime

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return self.metadata.copy()


def load_skill_metadata(skill_dir: str) -> Optional[SkillMetadata]:
    """
    加载单个技能的元数据

    Args:
        skill_dir: 技能目录路径

    Returns:
        SkillMetadata 对象，如果加载失败返回 None
    """
    try:
        return SkillMetadata(skill_dir)
    except Exception as e:
        print(f"⚠️  加载技能元数据失败 {skill_dir}: {e}")
        return None


def load_all_skills(skills_root: str) -> Dict[str, SkillMetadata]:
    """
    加载所有技能的元数据

    Args:
        skills_root: 技能根目录

    Returns:
        技能名称到 SkillMetadata 的映射
    """
    skills = {}

    if not os.path.exists(skills_root):
        return skills

    for item in os.listdir(skills_root):
        skill_dir = os.path.join(skills_root, item)

        # 跳过非目录
        if not os.path.isdir(skill_dir):
            continue

        # 检查是否有 SKILL.md
        skill_md = os.path.join(skill_dir, 'SKILL.md')
        if not os.path.exists(skill_md):
            continue

        # 加载元数据
        metadata = load_skill_metadata(skill_dir)
        if metadata:
            skills[metadata.get('name', item)] = metadata

    return skills


if __name__ == '__main__':
    # 测试代码
    skills_root = os.path.join(os.path.dirname(__file__), '..', 'skills')
    skills = load_all_skills(skills_root)

    print(f"✅ 加载了 {len(skills)} 个技能:")
    for name, metadata in skills.items():
        print(f"  - {name}")
        print(f"    分类: {metadata.get('category')}")
        print(f"    标签: {metadata.get('tags', [])}")
        print(f"    提供: {metadata.provides()}")
        print(f"    消耗: {metadata.consumes()}")
        print()
