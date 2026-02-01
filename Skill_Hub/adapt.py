"""
Skill Hub - Adaptation Module
自动适配模块：将外部 Skill 转换为 MindSymphony 格式

实现 skill-curator Phase 4: 适配
- Frontmatter 标准化
- 文档结构统一
- 触发词本地化
- 风格调整
"""

import os
import re
import shutil
from pathlib import Path
from typing import Optional, Dict, List
from datetime import datetime

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

from models import SkillMetadata, SourceType


class MindSymphonyAdapter:
    """MindSymphony 格式适配器

    将外部 Skill 转换为符合 MindSymphony 标准的格式
    """

    # MindSymphony 模块分类
    MODULE_CATEGORIES = {
        'strategy': ['action', 'plan', 'roadmap', 'strategy'],
        'research': ['analyze', 'research', 'study', 'investigate'],
        'creative': ['design', 'create', 'generate', 'visual', 'art'],
        'writing': ['write', 'content', 'copy', 'edit'],
        'thinking': ['logic', 'think', 'reason', 'paradox'],
        'engineering': ['code', 'dev', 'build', 'test', 'deploy'],
        'meta': ['skill', 'config', 'manage', 'workflow'],
        'domains': ['data', 'doc', 'prompt', 'n8n', 'presentation'],
    }

    # MindSymphony 层级分类
    LAYER_MAPPING = {
        'dao': ['strategy', 'brand', 'value', 'purpose'],
        'fa': ['plan', 'architecture', 'design'],
        'shu': ['research', 'write', 'create'],
        'qi': ['code', 'tool', 'utility', 'implement'],
    }

    def __init__(self, target_path: str):
        """初始化适配器

        Args:
            target_path: MindSymphony skills 目录路径
        """
        self.target_path = Path(target_path)

    def adapt(
        self,
        source_path: str,
        metadata: SkillMetadata,
        user_requirement: str = ""
    ) -> Dict[str, str]:
        """适配 Skill 到 MindSymphony 格式

        Args:
            source_path: 源 skill 文件/目录路径
            metadata: Skill 元数据
            user_requirement: 用户需求描述

        Returns:
            适配结果字典:
            - status: 'success', 'partial', 'failed'
            - target_path: 适配后的文件路径
            - changes: 做出的修改列表
            - warnings: 警告信息列表
        """
        result = {
            'status': 'success',
            'target_path': '',
            'changes': [],
            'warnings': []
        }

        source_path = Path(source_path)

        # 1. 确定 skill 内容
        skill_content = self._read_skill_content(source_path)
        if not skill_content:
            result['status'] = 'failed'
            result['warnings'].append("无法读取 skill 内容")
            return result

        # 2. 生成适配后的 frontmatter
        adapted_frontmatter = self._create_adapted_frontmatter(metadata, user_requirement)
        result['changes'].append("Frontmatter 标准化")

        # 3. 适配文档结构
        adapted_content = self._adapt_content_structure(skill_content, metadata)
        result['changes'].append("文档结构统一")

        # 4. 确定目标路径
        target_path = self._determine_target_path(metadata)
        result['target_path'] = str(target_path)

        # 5. 写入适配后的文件
        try:
            self._write_adapted_skill(
                target_path,
                adapted_frontmatter,
                adapted_content,
                metadata
            )
            result['changes'].append(f"写入到 {target_path}")
        except Exception as e:
            result['status'] = 'failed'
            result['warnings'].append(f"写入失败: {e}")
            return result

        # 6. 检查是否完全通过
        if result['warnings']:
            result['status'] = 'partial'

        return result

    def _read_skill_content(self, source_path: Path) -> Optional[str]:
        """读取 skill 内容"""
        if source_path.is_file():
            try:
                with open(source_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except:
                return None
        elif source_path.is_dir():
            # 寻找主要文件
            for filename in ['SKILL.md', 'README.md', 'skill.md', 'readme.md']:
                file_path = source_path / filename
                if file_path.exists():
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            return f.read()
                    except:
                        continue
        return None

    def _create_adapted_frontmatter(
        self,
        metadata: SkillMetadata,
        user_requirement: str
    ) -> Dict:
        """创建适配后的 frontmatter"""
        frontmatter = {
            'name': self._normalize_name(metadata.name),
            'module': self._determine_module(metadata),
            'layer': self._determine_layer(metadata),
            'triggers': self._create_triggers(metadata),
            'type': self._determine_type(metadata),
            'version': '1.0',
        }

        # 添加原始来源
        if metadata.source != SourceType.LOCAL:
            frontmatter['source'] = metadata.source.value
            if metadata.url:
                frontmatter['original_url'] = metadata.url

        # 添加适配时间
        frontmatter['adapted_at'] = datetime.now().isoformat()

        return frontmatter

    def _normalize_name(self, name: str) -> str:
        """规范化 skill 名称（小写-连字符）"""
        # 转小写
        name = name.lower()
        # 替换空格和下划线为连字符
        name = re.sub(r'[\s_]+', '-', name)
        # 移除特殊字符
        name = re.sub(r'[^a-z0-9-]', '', name)
        # 移除开头的数字
        name = re.sub(r'^[0-9-]+', '', name)
        return name

    def _determine_module(self, metadata: SkillMetadata) -> str:
        """确定所属模块"""
        name_lower = metadata.name.lower()
        desc_lower = metadata.description.lower()

        for module, keywords in self.MODULE_CATEGORIES.items():
            for keyword in keywords:
                if keyword in name_lower or keyword in desc_lower:
                    return module

        return 'meta'  # 默认归入 meta

    def _determine_layer(self, metadata: SkillMetadata) -> str:
        """确定所属层级 (dao/fa/shu/qi)"""
        name_lower = metadata.name.lower()
        desc_lower = metadata.description.lower()

        for layer, keywords in self.LAYER_MAPPING.items():
            for keyword in keywords:
                if keyword in name_lower or keyword in desc_lower:
                    return layer

        return 'shu'  # 默认归入 shu (术)

    def _create_triggers(self, metadata: SkillMetadata) -> Dict[str, List[str]]:
        """创建触发词（中英双语）"""
        triggers = {}

        # 从元数据获取
        if metadata.triggers:
            if isinstance(metadata.triggers, dict):
                triggers = metadata.triggers
            elif isinstance(metadata.triggers, list):
                triggers['en'] = metadata.triggers

        # 确保有英文触发词
        if 'en' not in triggers:
            # 从名称生成
            triggers['en'] = [metadata.name]
            # 从描述关键词生成
            desc_words = re.findall(r'\b\w{3,}\b', metadata.description)
            triggers['en'].extend(desc_words[:3])

        # 生成中文触发词
        if 'zh' not in triggers:
            triggers['zh'] = self._generate_chinese_triggers(metadata)

        return triggers

    def _generate_chinese_triggers(self, metadata: SkillMetadata) -> List[str]:
        """生成中文触发词"""
        # 简化的中文触发词生成（可改进为更复杂的翻译）
        zh_triggers = []

        # 常见关键词映射
        keyword_map = {
            'write': '写作', 'create': '创建', 'design': '设计',
            'analyze': '分析', 'research': '研究', 'plan': '规划',
            'code': '代码', 'test': '测试', 'deploy': '部署',
            'visual': '视觉', 'art': '艺术', 'content': '内容',
        }

        name_lower = metadata.name.lower()
        for en, zh in keyword_map.items():
            if en in name_lower:
                zh_triggers.append(zh)

        # 如果没有生成任何触发词，添加通用触发词
        if not zh_triggers:
            zh_triggers.append(metadata.name)

        return zh_triggers

    def _determine_type(self, metadata: SkillMetadata) -> str:
        """确定 skill 类型"""
        desc_lower = metadata.description.lower()

        if any(word in desc_lower for word in ['create', 'generate', 'design', 'art']):
            return 'creative'
        elif any(word in desc_lower for word in ['analyze', 'research', 'study']):
            return 'analytical'
        elif any(word in desc_lower for word in ['code', 'build', 'implement']):
            return 'execution'
        else:
            return 'execution'  # 默认

    def _adapt_content_structure(self, content: str, metadata: SkillMetadata) -> str:
        """适配文档结构"""
        # 移除营销语言
        content = self._remove_marketing_language(content)

        # 统一术语
        content = self._standardize_terminology(content)

        # 添加 MindSymphony 特有元素
        content = self._add_mindsymphony_elements(content, metadata)

        return content

    def _remove_marketing_language(self, content: str) -> str:
        """移除营销语言"""
        marketing_patterns = [
            r'🚀\s*', r'✨\s*', r'⭐\s*',  # emoji
            r'amazing|awesome|incredible|unbelievable',  # 夸张形容词
            r'best|top|#1|first',  # 最高级
        ]

        for pattern in marketing_patterns:
            content = re.sub(pattern, '', content, flags=re.IGNORECASE)

        return content

    def _standardize_terminology(self, content: str) -> str:
        """统一术语表达"""
        # 统一 "skill" 的大小写
        content = re.sub(r'\b[Ss]kill\b', 'Skill', content)

        # 统一 "MindSymphony" 的大小写
        content = re.sub(r'\b[mindsymphony|MINDSYMPHONY]\b', 'MindSymphony', content)

        return content

    def _add_mindsymphony_elements(self, content: str, metadata: SkillMetadata) -> str:
        """添加 MindSymphony 特有元素"""
        # 检查是否已经有核心能力部分
        if '## 核心能力' not in content and '## Core Capabilities' not in content:
            # 在开头添加核心能力部分
            core_capabilities = f"""
## 核心能力

1. **主要功能**：{metadata.description[:100]}...
2. **适用场景**：根据需求确定
3. **独特价值**：{metadata.name}

"""
            # 在第一个标题后插入
            lines = content.split('\n')
            insert_pos = 0
            for i, line in enumerate(lines):
                if line.startswith('#'):
                    insert_pos = i + 1
                    break

            lines.insert(insert_pos, core_capabilities)
            content = '\n'.join(lines)

        # 添加使用示例（如果没有）
        if '## 使用示例' not in content and '## Usage' not in content:
            usage_example = """

## 使用示例

```
# 在 Claude Code 中直接调用
使用 {name} 来 [任务描述]

# 或通过触发词
{trigger}
```
""".format(
                name=metadata.name,
                trigger=list(metadata.triggers.values())[0][0] if metadata.triggers else metadata.name
            )
            content += usage_example

        return content

    def _determine_target_path(self, metadata: SkillMetadata) -> Path:
        """确定目标路径"""
        module = self._determine_module(metadata)
        normalized_name = self._normalize_name(metadata.name)

        # 目标路径: mindsymphony/extensions/{module}/{name}.md
        target_path = self.target_path / 'mindsymphony' / 'extensions' / module / f"{normalized_name}.md"

        return target_path

    def _write_adapted_skill(
        self,
        target_path: Path,
        frontmatter: Dict,
        content: str,
        metadata: SkillMetadata
    ) -> None:
        """写入适配后的 skill 文件"""
        # 确保目录存在
        target_path.parent.mkdir(parents=True, exist_ok=True)

        # 生成 YAML frontmatter
        if HAS_YAML:
            frontmatter_str = "---\n" + yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True) + "---\n\n"
        else:
            # 简化的 frontmatter 格式
            frontmatter_lines = ["---"]
            for key, value in frontmatter.items():
                if isinstance(value, list):
                    frontmatter_lines.append(f"{key}: [{', '.join(str(v) for v in value)}]")
                elif isinstance(value, dict):
                    frontmatter_lines.append(f"{key}: {{{value}}}")
                else:
                    frontmatter_lines.append(f"{key}: {value}")
            frontmatter_lines.append("---")
            frontmatter_str = '\n'.join(frontmatter_lines) + '\n\n'

        # 写入文件
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(frontmatter_str)
            f.write(content)


class AutoAdaptOrchestrator:
    """自动适配编排器

    协调完整的适配流程
    """

    def __init__(self, config):
        self.config = config
        self.adapter = MindSymphonyAdapter(config.integration.skills_path)

    def auto_adapt(
        self,
        source_path: str,
        metadata: SkillMetadata,
        user_requirement: str = ""
    ) -> Dict:
        """自动适配 Skill

        Args:
            source_path: 源 skill 路径
            metadata: Skill 元数据
            user_requirement: 用户需求

        Returns:
            适配结果
        """
        if not self.config.evaluation.auto_adapt:
            return {
                'status': 'skipped',
                'message': '自动适配未启用'
            }

        # 执行适配
        result = self.adapter.adapt(source_path, metadata, user_requirement)

        # 如果成功，尝试注册到 Intent Router
        if result['status'] in ['success', 'partial'] and self.config.integration.auto_register:
            self._register_to_intent_router(result['target_path'], metadata)

        return result

    def _register_to_intent_router(self, skill_path: str, metadata: SkillMetadata):
        """注册到 Intent Router"""
        router_path = Path(self.config.integration.skills_path) / 'mindsymphony' / 'router' / 'intent-router.md'

        if not router_path.exists():
            return

        try:
            with open(router_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 检查是否已经注册
            if metadata.name in content:
                return

            # 添加到路由表
            new_entry = f"| **{metadata.name}** | {self.adapter._determine_module(metadata)} | 100% |"

            # 在路由表中插入
            lines = content.split('\n')
            insert_pos = len(lines)
            for i, line in enumerate(lines):
                if '| 关键词 | 路由到 |' in line:
                    # 找到表格，在最后一个表格行后插入
                    for j in range(i + 1, len(lines)):
                        if not lines[j].strip().startswith('|'):
                            insert_pos = j
                            break
                    break

            lines.insert(insert_pos, new_entry)

            with open(router_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))

        except Exception as e:
            print(f"[WARNING] 注册到 Intent Router 失败: {e}")


def adapt_skill_from_metadata(
    metadata: SkillMetadata,
    source_content: str,
    target_path: str,
    user_requirement: str = ""
) -> Dict:
    """便捷函数：从元数据适配 Skill

    Args:
        metadata: Skill 元数据
        source_content: 源内容
        target_path: 目标路径
        user_requirement: 用户需求

    Returns:
        适配结果
    """
    adapter = MindSymphonyAdapter(target_path)

    # 写入临时文件
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
        f.write(source_content)
        temp_path = f.name

    try:
        result = adapter.adapt(temp_path, metadata, user_requirement)
        return result
    finally:
        # 清理临时文件
        os.unlink(temp_path)
