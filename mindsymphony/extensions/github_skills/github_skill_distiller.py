"""
GitHub Skill Distiller
分析GitHub仓库并提取结构化技能

功能:
- README解析和方法论提取
- 代码结构分析
- 最佳实践识别
- 生成标准SKILL.md格式
"""

import re
import json
import hashlib
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from urllib.parse import urlparse
import os


@dataclass
class DistillationResult:
    """蒸馏结果"""
    skill_name: str
    skill_content: str  # Markdown格式的SKILL.md
    metadata: Dict[str, Any]
    patterns: List[Dict]
    confidence: float
    source_repo: str
    distillation_time: datetime


@dataclass
class ExtractedPattern:
    """提取的模式"""
    name: str
    type: str  # 'workflow', 'architecture', 'practice', 'pattern'
    description: str
    implementation: str
    confidence: float


class GitHubSkillDistiller:
    """
    GitHub技能蒸馏器

    将GitHub仓库的方法论、最佳实践提取为可复用的技能
    """

    def __init__(self, config: Optional[Dict] = None):
        """
        初始化蒸馏器

        Args:
            config: 配置选项
                - github_token: GitHub API token
                - cache_dir: 缓存目录
                - min_confidence: 最小置信度阈值
        """
        self.config = config or {}
        self.github_token = self.config.get('github_token') or os.getenv('GITHUB_TOKEN')
        self.cache_dir = self.config.get('cache_dir', '~/.mindsymphony/github_skills_cache')
        self.min_confidence = self.config.get('min_confidence', 0.6)

        # 编译正则表达式模式
        self._compile_patterns()

    def _compile_patterns(self):
        """编译用于提取的正则表达式"""
        # README章节标题
        self.section_pattern = re.compile(
            r'^(#{1,6})\s+(.+?)$',
            re.MULTILINE
        )

        # 方法论关键词
        self.methodology_patterns = [
            re.compile(r'\b(method|methodology|approach|framework|process|workflow)\b', re.I),
            re.compile(r'\b(best practice|guideline|principle|pattern)\b', re.I),
            re.compile(r'\b(how to|step by step|guide|tutorial)\b', re.I),
        ]

        # 代码模式
        self.code_patterns = {
            'architecture': re.compile(r'\b(architecture|structure|design|pattern)\b', re.I),
            'workflow': re.compile(r'\b(flow|pipeline|process|stage|step)\b', re.I),
            'testing': re.compile(r'\b(test|spec|validate|verify|assert)\b', re.I),
        }

    def distill(
        self,
        repo_identifier: str,
        extract_patterns: bool = True,
        include_code_examples: bool = True,
        personalize: bool = False
    ) -> DistillationResult:
        """
        蒸馏GitHub仓库为技能

        Args:
            repo_identifier: 仓库标识 (如 "bmad-code-org/BMAD-METHOD")
            extract_patterns: 是否提取代码模式
            include_code_examples: 是否包含代码示例
            personalize: 是否根据个人DNA个性化

        Returns:
            DistillationResult: 蒸馏结果
        """
        print(f"🔬 正在蒸馏仓库: {repo_identifier}")

        # 1. 解析仓库信息
        owner, repo = self._parse_repo_identifier(repo_identifier)

        # 2. 获取仓库数据 (模拟API调用)
        repo_data = self._fetch_repo_data(owner, repo)

        # 3. 解析README
        readme_analysis = self._analyze_readme(repo_data.get('readme', ''))

        # 4. 提取方法论
        methodologies = self._extract_methodologies(readme_analysis)

        # 5. 分析代码结构
        code_patterns = []
        if extract_patterns:
            code_patterns = self._analyze_code_structure(repo_data)

        # 6. 生成技能名称
        skill_name = self._generate_skill_name(repo_data, methodologies)

        # 7. 生成SKILL.md内容
        skill_content = self._generate_skill_md(
            skill_name=skill_name,
            repo_data=repo_data,
            methodologies=methodologies,
            code_patterns=code_patterns,
            include_code_examples=include_code_examples
        )

        # 8. 构建元数据
        metadata = {
            'source': {
                'repo': repo_identifier,
                'url': f"https://github.com/{repo_identifier}",
                'stars': repo_data.get('stars', 0),
                'language': repo_data.get('language', 'Unknown'),
                'license': repo_data.get('license', 'Unknown'),
            },
            'extraction': {
                'methodologies_count': len(methodologies),
                'patterns_count': len(code_patterns),
                'readme_sections': len(readme_analysis.get('sections', [])),
            },
            'version': '1.0.0',
            'created_at': datetime.now().isoformat(),
        }

        # 9. 计算置信度
        confidence = self._calculate_confidence(
            readme_analysis, methodologies, code_patterns
        )

        print(f"✅ 蒸馏完成: {skill_name} (置信度: {confidence:.1%})")

        return DistillationResult(
            skill_name=skill_name,
            skill_content=skill_content,
            metadata=metadata,
            patterns=[p.__dict__ for p in code_patterns],
            confidence=confidence,
            source_repo=repo_identifier,
            distillation_time=datetime.now()
        )

    def _parse_repo_identifier(self, identifier: str) -> Tuple[str, str]:
        """解析仓库标识符"""
        # 支持多种格式:
        # - "owner/repo"
        # - "https://github.com/owner/repo"
        # - "github.com/owner/repo"

        identifier = identifier.strip().rstrip('/')

        # 如果是URL，解析路径
        if 'github.com' in identifier:
            parsed = urlparse(identifier)
            path_parts = parsed.path.strip('/').split('/')
            if len(path_parts) >= 2:
                return path_parts[0], path_parts[1]

        # 否则假设是 "owner/repo" 格式
        parts = identifier.split('/')
        if len(parts) == 2:
            return parts[0], parts[1]

        raise ValueError(f"无效的仓库标识符: {identifier}")

    def _fetch_repo_data(self, owner: str, repo: str) -> Dict[str, Any]:
        """
        获取仓库数据

        实际实现中会调用GitHub API
        这里使用模拟数据演示
        """
        # 模拟仓库数据
        # 实际实现中应该使用 requests 调用 GitHub API
        return {
            'name': repo,
            'owner': owner,
            'description': f'Methodology from {owner}/{repo}',
            'stars': 1000,
            'language': 'Python',
            'license': 'MIT',
            'readme': self._get_mock_readme(repo),
            'topics': ['methodology', 'workflow', 'best-practices'],
        }

    def _get_mock_readme(self, repo: str) -> str:
        """获取模拟README (实际实现中会调用API)"""
        # 这里返回一个示例README结构
        return f"""
# {repo}

A comprehensive methodology for software development.

## Overview

This repository contains best practices and workflows.

## Methodology

### Step 1: Planning
Start with clear objectives.

### Step 2: Execution
Follow the structured approach.

### Step 3: Validation
Verify all requirements.

## Best Practices

- Practice A: Do this first
- Practice B: Then do this
- Practice C: Finally verify

## Architecture

The system follows a layered architecture.

## Workflow

1. Analyze requirements
2. Design solution
3. Implement code
4. Test thoroughly
5. Deploy carefully

## Examples

```python
def example():
    pass
```
"""

    def _analyze_readme(self, readme_content: str) -> Dict[str, Any]:
        """分析README结构"""
        sections = []
        current_section = None

        for match in self.section_pattern.finditer(readme_content):
            level = len(match.group(1))
            title = match.group(2).strip()

            section = {
                'level': level,
                'title': title,
                'is_methodology': any(
                    p.search(title) for p in self.methodology_patterns
                ),
                'position': match.start()
            }
            sections.append(section)

            # 识别特殊章节
            if level <= 2:
                current_section = section

        # 提取方法论章节
        methodology_sections = [
            s for s in sections
            if s['is_methodology'] or self._is_methodology_section(s['title'])
        ]

        return {
            'sections': sections,
            'methodology_sections': methodology_sections,
            'total_length': len(readme_content),
            'has_code_examples': '```' in readme_content,
            'has_workflow': 'workflow' in readme_content.lower(),
        }

    def _is_methodology_section(self, title: str) -> bool:
        """判断是否为方法论章节"""
        methodology_keywords = [
            'method', 'methodology', 'approach', 'framework',
            'workflow', 'process', 'guide', 'best practice',
            'principle', 'pattern', 'how to', 'tutorial'
        ]
        return any(kw in title.lower() for kw in methodology_keywords)

    def _extract_methodologies(self, readme_analysis: Dict) -> List[Dict]:
        """提取方法论"""
        methodologies = []

        for section in readme_analysis.get('methodology_sections', []):
            methodology = {
                'name': section['title'],
                'type': self._classify_methodology_type(section['title']),
                'confidence': 0.8 if section['is_methodology'] else 0.6,
            }
            methodologies.append(methodology)

        # 如果README有明确的流程描述，提取为工作流
        if readme_analysis.get('has_workflow'):
            methodologies.append({
                'name': 'Primary Workflow',
                'type': 'workflow',
                'confidence': 0.75,
            })

        return methodologies

    def _classify_methodology_type(self, title: str) -> str:
        """分类方法论类型"""
        title_lower = title.lower()

        if any(w in title_lower for w in ['workflow', 'process', 'flow']):
            return 'workflow'
        elif any(w in title_lower for w in ['architecture', 'design', 'structure']):
            return 'architecture'
        elif any(w in title_lower for w in ['pattern', 'anti-pattern']):
            return 'pattern'
        elif any(w in title_lower for w in ['guide', 'how to', 'tutorial']):
            return 'guide'
        elif any(w in title_lower for w in ['practice', 'principle']):
            return 'practice'
        else:
            return 'methodology'

    def _analyze_code_structure(self, repo_data: Dict) -> List[ExtractedPattern]:
        """分析代码结构，提取模式"""
        patterns = []

        # 基于仓库元数据推断模式
        topics = repo_data.get('topics', [])
        description = repo_data.get('description', '')

        # 工作流模式
        if 'workflow' in topics or 'workflow' in description.lower():
            patterns.append(ExtractedPattern(
                name='Structured Workflow',
                type='workflow',
                description='Follows a structured multi-step workflow',
                implementation='Define clear stages and transitions',
                confidence=0.8
            ))

        # 架构模式
        if 'architecture' in topics or 'architecture' in description.lower():
            patterns.append(ExtractedPattern(
                name='Layered Architecture',
                type='architecture',
                description='Uses layered architectural pattern',
                implementation='Separate concerns into distinct layers',
                confidence=0.75
            ))

        # 最佳实践
        patterns.append(ExtractedPattern(
            name='Documentation First',
            type='practice',
            description='Emphasizes comprehensive documentation',
            implementation='Document before implementation',
            confidence=0.7
        ))

        return patterns

    def _generate_skill_name(self, repo_data: Dict, methodologies: List[Dict]) -> str:
        """生成技能名称"""
        repo_name = repo_data.get('name', 'unknown')

        # 清理名称
        name = repo_name.lower()
        name = re.sub(r'[-_]', '-', name)

        # 添加类型前缀
        if methodologies:
            main_type = methodologies[0]['type']
            if main_type == 'workflow':
                return f"{name}-workflow"
            elif main_type == 'architecture':
                return f"{name}-architecture"

        return name

    def _generate_skill_md(
        self,
        skill_name: str,
        repo_data: Dict,
        methodologies: List[Dict],
        code_patterns: List[ExtractedPattern],
        include_code_examples: bool
    ) -> str:
        """生成SKILL.md内容"""

        content = f"""# {skill_name.replace('-', ' ').title()}

从 [{repo_data['owner']}/{repo_data['name']}](https://github.com/{repo_data['owner']}/{repo_data['name']}) 蒸馏的技能

## 概述

{repo_data.get('description', 'Distilled methodology and best practices.')}

**来源**: GitHub ({repo_data.get('stars', 0)} ⭐)
**语言**: {repo_data.get('language', 'Unknown')}
**许可证**: {repo_data.get('license', 'Unknown')}
**蒸馏时间**: {datetime.now().strftime('%Y-%m-%d')}

---

## 核心方法论

"""

        # 添加方法论
        for i, method in enumerate(methodologies[:5], 1):
            content += f"""### {i}. {method['name']}

**类型**: {method['type']}
**置信度**: {method['confidence']:.0%}

{self._get_methodology_description(method)}

"""

        # 添加模式
        if code_patterns:
            content += """---

## 识别模式

"""
            for pattern in code_patterns[:5]:
                content += f"""### {pattern.name}

**类型**: {pattern.type}
**置信度**: {pattern.confidence:.0%}

{pattern.description}

**实现要点**:
{pattern.implementation}

"""

        # 添加使用指南
        content += f"""---

## 使用指南

### 适用场景

- 需要{skill_name.replace('-', ' ')}的项目
- 追求最佳实践的团队
- 标准化工作流程

### 集成到MindSymphony

```python
from mindsymphony.extensions.github_skills import distill_github_repo

# 使用此技能
result = distill_github_repo("{repo_data['owner']}/{repo_data['name']}")
skill = result.skill_content
```

### 通过快捷指令

```
/ms-github {repo_data['owner']}/{repo_data['name']}
```

---

## 演进历史

- **v1.0.0** ({datetime.now().strftime('%Y-%m-%d')}): 从GitHub自动蒸馏

---

*此技能由MindSymphony GitHub Skills Distiller自动生成*
"""

        return content

    def _get_methodology_description(self, method: Dict) -> str:
        """获取方法论描述"""
        descriptions = {
            'workflow': '遵循结构化的工作流程，确保每个阶段都有明确的目标和产出。',
            'architecture': '采用分层的架构设计，分离关注点，提高系统的可维护性。',
            'pattern': '应用经过验证的设计模式，解决常见问题。',
            'practice': '遵循行业最佳实践，提高代码质量和团队协作效率。',
            'guide': '按照指南逐步执行，确保不遗漏关键步骤。',
        }
        return descriptions.get(
            method['type'],
            '应用系统化的方法论，提高效率和效果。'
        )

    def _calculate_confidence(
        self,
        readme_analysis: Dict,
        methodologies: List[Dict],
        code_patterns: List[ExtractedPattern]
    ) -> float:
        """计算蒸馏结果的置信度"""
        scores = []

        # README质量
        if readme_analysis.get('has_code_examples'):
            scores.append(0.2)
        if readme_analysis.get('has_workflow'):
            scores.append(0.15)
        if len(readme_analysis.get('sections', [])) > 3:
            scores.append(0.1)

        # 方法论数量
        if len(methodologies) >= 3:
            scores.append(0.25)
        elif len(methodologies) >= 1:
            scores.append(0.15)

        # 模式识别
        if len(code_patterns) >= 2:
            scores.append(0.2)
        elif len(code_patterns) >= 1:
            scores.append(0.1)

        # 基础置信度
        scores.append(0.2)

        return min(sum(scores), 1.0)

    def batch_distill(
        self,
        repo_list: List[str],
        **kwargs
    ) -> List[DistillationResult]:
        """
        批量蒸馏多个仓库

        Args:
            repo_list: 仓库标识符列表
            **kwargs: 传递给distill的参数

        Returns:
            DistillationResult列表
        """
        results = []
        for repo in repo_list:
            try:
                result = self.distill(repo, **kwargs)
                results.append(result)
            except Exception as e:
                print(f"❌ 蒸馏失败 {repo}: {e}")
        return results
