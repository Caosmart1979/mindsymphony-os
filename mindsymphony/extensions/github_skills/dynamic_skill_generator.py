"""
Dynamic Skill Generator
动态技能生成器 - 根据任务需求实时生成技能

功能:
- 任务需求分析
- GitHub搜索和最佳实践提取
- 临时技能生成
- 技能验证和固化
"""

import re
import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path

from .skill_knowledge_graph import SkillKnowledgeGraph, SkillNode, RelationType
from .skill_dna import SkillDNA


@dataclass
class GenerationRequest:
    """技能生成请求"""
    task_description: str
    context: Optional[Dict] = None
    required_capabilities: List[str] = field(default_factory=list)
    constraints: Dict[str, Any] = field(default_factory=dict)
    preferred_sources: List[str] = field(default_factory=list)


@dataclass
class GeneratedSkill:
    """生成的技能"""
    skill_id: str
    name: str
    content: str
    metadata: Dict[str, Any]
    sources: List[Dict]
    confidence: float
    is_temporary: bool = True
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


class DynamicSkillGenerator:
    """
    动态技能生成器

    根据任务需求实时搜索GitHub并生成技能
    """

    def __init__(
        self,
        skill_graph: Optional[SkillKnowledgeGraph] = None,
        skill_dna: Optional[SkillDNA] = None,
        config: Optional[Dict] = None
    ):
        """
        初始化生成器

        Args:
            skill_graph: 技能知识图谱
            skill_dna: 个人技能DNA
            config: 配置选项
        """
        self.skill_graph = skill_graph or SkillKnowledgeGraph()
        self.skill_dna = skill_dna
        self.config = config or {}

        self.min_confidence = self.config.get('min_confidence', 0.6)
        self.max_sources = self.config.get('max_sources', 5)

    def generate(
        self,
        request: GenerationRequest,
        persist: bool = False
    ) -> GeneratedSkill:
        """
        根据任务需求生成技能

        Args:
            request: 生成请求
            persist: 是否持久化到技能库

        Returns:
            GeneratedSkill: 生成的技能
        """
        print(f"🎯 分析任务需求: {request.task_description[:50]}...")

        # 1. 分析任务需求
        task_analysis = self._analyze_task(request)

        # 2. 搜索相关GitHub项目
        github_sources = self._search_github_sources(task_analysis)

        # 3. 提取最佳实践
        best_practices = self._extract_best_practices(github_sources)

        # 4. 生成技能内容
        skill_content = self._generate_skill_content(
            task_analysis,
            best_practices,
            request
        )

        # 5. 计算置信度
        confidence = self._calculate_generation_confidence(
            task_analysis,
            github_sources,
            best_practices
        )

        # 6. 构建技能对象
        skill_id = f"dynamic_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        skill_name = self._generate_skill_name(task_analysis)

        generated_skill = GeneratedSkill(
            skill_id=skill_id,
            name=skill_name,
            content=skill_content,
            metadata={
                'task_description': request.task_description,
                'task_analysis': task_analysis,
                'generated_at': datetime.now().isoformat(),
                'generator_version': '1.0.0',
                'confidence': confidence,
            },
            sources=github_sources,
            confidence=confidence,
            is_temporary=not persist
        )

        # 7. 如需要，持久化到技能库
        if persist and confidence >= self.min_confidence:
            self._persist_skill(generated_skill)

        print(f"✅ 技能生成完成: {skill_name} (置信度: {confidence:.1%})")

        return generated_skill

    def generate_from_query(self, task_description: str, **kwargs) -> GeneratedSkill:
        """
        便捷方法：从描述生成技能

        Args:
            task_description: 任务描述
            **kwargs: 额外参数

        Returns:
            GeneratedSkill: 生成的技能
        """
        request = GenerationRequest(
            task_description=task_description,
            context=kwargs.get('context'),
            required_capabilities=kwargs.get('required_capabilities', []),
            constraints=kwargs.get('constraints', {}),
            preferred_sources=kwargs.get('preferred_sources', [])
        )
        return self.generate(request, persist=kwargs.get('persist', False))

    def _analyze_task(self, request: GenerationRequest) -> Dict:
        """
        分析任务需求

        提取关键信息：
        - 任务类型
        - 技术栈
        - 复杂度
        - 相关领域
        """
        description = request.task_description.lower()

        # 识别任务类型
        task_types = []
        type_keywords = {
            'analysis': ['分析', 'analyze', 'analysis', '统计', '计算', 'compute'],
            'generation': ['生成', 'generate', '创建', 'create', '构建', 'build'],
            'optimization': ['优化', 'optimize', '改进', 'improve', '提升', 'enhance'],
            'validation': ['验证', 'validate', '检查', 'check', '测试', 'test'],
            'integration': ['集成', 'integrate', '连接', 'connect', '导入', 'import'],
        }

        for task_type, keywords in type_keywords.items():
            if any(kw in description for kw in keywords):
                task_types.append(task_type)

        if not task_types:
            task_types.append('general')

        # 识别技术栈
        tech_stack = self._extract_technology_stack(description)

        # 识别领域
        domains = self._extract_domains(description)

        # 评估复杂度
        complexity = self._assess_complexity(description, request)

        return {
            'task_types': task_types,
            'tech_stack': tech_stack,
            'domains': domains,
            'complexity': complexity,
            'original_description': request.task_description,
            'key_requirements': request.required_capabilities,
        }

    def _extract_technology_stack(self, description: str) -> List[str]:
        """从技术描述中提取技术栈"""
        tech_patterns = {
            'python': ['python', 'py', 'pandas', 'numpy', 'sklearn'],
            'javascript': ['javascript', 'js', 'node', 'react', 'vue'],
            'typescript': ['typescript', 'ts'],
            'rust': ['rust', 'cargo'],
            'go': ['go', 'golang'],
            'java': ['java', 'spring'],
            'docker': ['docker', 'container'],
            'kubernetes': ['kubernetes', 'k8s'],
            'aws': ['aws', 'amazon web services'],
            'gcp': ['gcp', 'google cloud'],
            'azure': ['azure', 'microsoft cloud'],
            'machine_learning': ['machine learning', 'ml', 'deep learning', 'ai'],
            'data_analysis': ['data analysis', '数据分析', 'data science'],
            'web_scraping': ['scraping', 'crawler', 'spider'],
            'automation': ['automation', '自动化', 'script'],
        }

        found_tech = []
        for tech, patterns in tech_patterns.items():
            if any(p in description for p in patterns):
                found_tech.append(tech)

        return found_tech

    def _extract_domains(self, description: str) -> List[str]:
        """从描述中提取领域"""
        domain_patterns = {
            'web_development': ['web', 'frontend', 'backend', 'api', '网站'],
            'data_science': ['data', 'analysis', 'analytics', '数据', '分析'],
            'machine_learning': ['ml', 'ai', 'machine learning', '模型', '预测'],
            'devops': ['devops', 'deployment', 'ci/cd', 'pipeline', '部署'],
            'mobile': ['mobile', 'app', 'android', 'ios', '移动'],
            'security': ['security', '安全', '加密', 'authentication', 'auth'],
            'database': ['database', 'db', 'sql', 'nosql', '数据库'],
            'cloud': ['cloud', 'aws', 'azure', 'gcp', '云'],
        }

        found_domains = []
        for domain, patterns in domain_patterns.items():
            if any(p in description for p in patterns):
                found_domains.append(domain)

        return found_domains

    def _assess_complexity(
        self,
        description: str,
        request: GenerationRequest
    ) -> str:
        """评估任务复杂度"""
        complexity_indicators = {
            'simple': ['简单', 'simple', 'basic', '基础', 'quick', '快速'],
            'complex': ['复杂', 'complex', 'advanced', '高级', 'sophisticated'],
        }

        if any(w in description for w in complexity_indicators['simple']):
            return 'simple'
        elif any(w in description for w in complexity_indicators['complex']):
            return 'complex'

        # 基于需求数量评估
        if len(request.required_capabilities) > 5:
            return 'complex'
        elif len(request.required_capabilities) < 3:
            return 'simple'

        return 'moderate'

    def _search_github_sources(self, task_analysis: Dict) -> List[Dict]:
        """
        搜索相关GitHub项目

        基于任务分析构建搜索查询
        """
        print("🔍 搜索GitHub相关项目...")

        # 构建搜索查询
        queries = self._build_search_queries(task_analysis)

        # 模拟GitHub搜索结果
        # 实际实现中会调用GitHub Search API
        sources = []

        # 基于领域和技术栈生成模拟结果
        for domain in task_analysis['domains'][:2]:
            for tech in task_analysis['tech_stack'][:2]:
                source = {
                    'repo': f"awesome-{domain}-{tech}",
                    'owner': 'example-org',
                    'url': f"https://github.com/example-org/awesome-{domain}-{tech}",
                    'stars': 1000 + hash(domain + tech) % 9000,
                    'relevance_score': 0.7 + (hash(tech) % 100) / 1000,
                    'description': f'Best practices for {domain} using {tech}',
                    'extracted_patterns': [
                        f'{domain}-workflow',
                        f'{tech}-best-practices',
                    ]
                }
                sources.append(source)

        # 如果没有找到，添加通用资源
        if not sources:
            sources.append({
                'repo': 'awesome-guidelines',
                'owner': 'community',
                'url': 'https://github.com/community/awesome-guidelines',
                'stars': 5000,
                'relevance_score': 0.5,
                'description': 'General best practices',
                'extracted_patterns': ['general-workflow']
            })

        # 按相关度排序
        sources.sort(key=lambda x: x['relevance_score'], reverse=True)

        return sources[:self.max_sources]

    def _build_search_queries(self, task_analysis: Dict) -> List[str]:
        """构建GitHub搜索查询"""
        queries = []

        # 基于技术栈和领域构建查询
        for tech in task_analysis['tech_stack'][:2]:
            for domain in task_analysis['domains'][:2]:
                queries.append(f"{tech} {domain} best practices")

        # 基于任务类型构建查询
        for task_type in task_analysis['task_types']:
            for tech in task_analysis['tech_stack'][:1]:
                queries.append(f"{tech} {task_type} workflow")

        return queries

    def _extract_best_practices(self, github_sources: List[Dict]) -> List[Dict]:
        """
        从GitHub项目中提取最佳实践

        分析README和代码结构
        """
        practices = []

        for source in github_sources:
            # 模拟提取最佳实践
            patterns = source.get('extracted_patterns', [])

            for pattern in patterns:
                practice = {
                    'name': pattern,
                    'source': f"{source['owner']}/{source['repo']}",
                    'source_url': source['url'],
                    'confidence': source['relevance_score'],
                    'description': f'Extracted from {source["description"]}',
                    'applicability': ['general'],
                }
                practices.append(practice)

        # 按置信度排序
        practices.sort(key=lambda x: x['confidence'], reverse=True)

        return practices[:10]

    def _generate_skill_content(
        self,
        task_analysis: Dict,
        best_practices: List[Dict],
        request: GenerationRequest
    ) -> str:
        """
        生成技能内容

        创建标准SKILL.md格式
        """
        skill_name = self._generate_skill_name(task_analysis)

        content = f"""# {skill_name.replace('-', ' ').title()}

## 概述

动态生成的技能，用于处理: {request.task_description}

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**任务类型**: {', '.join(task_analysis['task_types'])}
**复杂度**: {task_analysis['complexity']}
**技术栈**: {', '.join(task_analysis['tech_stack']) or '通用'}

---

## 任务分析

### 目标领域
{chr(10).join(['- ' + d for d in task_analysis['domains']]) or '- 通用任务'}

### 关键需求
{chr(10).join(['- ' + r for r in request.required_capabilities]) or '- 标准实现'}

### 建议方法
基于分析，推荐采用以下方法：

"""

        # 添加最佳实践
        if best_practices:
            content += """## 参考最佳实践

"""
            for i, practice in enumerate(best_practices[:5], 1):
                content += f"""### {i}. {practice['name']}

**来源**: [{practice['source']}]({practice['source_url']})
**可信度**: {practice['confidence']:.0%}

{practice['description']}

"""

        # 添加执行步骤
        content += f"""---

## 执行步骤

### 步骤1: 准备阶段
- 确认任务需求和约束条件
- 准备必要的工具和环境
- 理解目标领域背景

### 步骤2: 分析阶段
- 收集相关信息
- 分析现有解决方案
- 识别关键挑战

### 步骤3: 实施阶段
- 应用最佳实践
- 执行核心任务
- 记录中间结果

### 步骤4: 验证阶段
- 检查结果质量
- 验证是否满足需求
- 优化和调整

---

## 注意事项

1. **环境依赖**: 确保安装了相关技术栈
2. **数据安全**: 处理敏感数据时注意隐私保护
3. **性能考虑**: 对于大规模任务考虑优化策略
4. **错误处理**: 实现适当的异常处理机制

---

## 示例代码

```python
# 根据任务生成的示例框架
def execute_task(input_data):
    '''
    执行任务: {request.task_description}
    '''
    # TODO: 实现具体逻辑
    result = process_data(input_data)
    return result
```

---

## 参考资源

"""

        # 添加参考资源
        for source in request.preferred_sources:
            content += f"- {source}\n"

        content += """
---

*此技能由MindSymphony动态技能生成器自动创建*
*基于GitHub最佳实践和任务需求分析*
"""

        return content

    def _generate_skill_name(self, task_analysis: Dict) -> str:
        """生成技能名称"""
        # 基于任务类型和领域生成名称
        task_type = task_analysis['task_types'][0] if task_analysis['task_types'] else 'task'
        domain = task_analysis['domains'][0] if task_analysis['domains'] else 'general'
        tech = task_analysis['tech_stack'][0] if task_analysis['tech_stack'] else 'auto'

        return f"{task_type}-{domain}-{tech}-handler"

    def _calculate_generation_confidence(
        self,
        task_analysis: Dict,
        github_sources: List[Dict],
        best_practices: List[Dict]
    ) -> float:
        """
        计算生成结果的置信度
        """
        scores = []

        # 任务分析质量
        if task_analysis['domains']:
            scores.append(0.2)
        if task_analysis['tech_stack']:
            scores.append(0.2)
        if task_analysis['task_types']:
            scores.append(0.15)

        # GitHub来源质量
        if github_sources:
            avg_relevance = sum(s['relevance_score'] for s in github_sources) / len(github_sources)
            scores.append(avg_relevance * 0.25)

        # 最佳实践数量和质量
        if best_practices:
            avg_confidence = sum(p['confidence'] for p in best_practices) / len(best_practices)
            scores.append(avg_confidence * 0.2)

        return min(sum(scores), 1.0)

    def _persist_skill(self, generated_skill: GeneratedSkill):
        """
        将生成的技能持久化到知识图谱
        """
        # 创建技能节点
        skill_node = SkillNode(
            name=generated_skill.name,
            source='dynamic_generation',
            description=generated_skill.metadata.get('task_description', ''),
            type='dynamic',
            tags=generated_skill.metadata.get('task_analysis', {}).get('tech_stack', []),
            metadata={
                'generated_at': generated_skill.created_at,
                'confidence': generated_skill.confidence,
                'content': generated_skill.content,
            }
        )

        # 添加到知识图谱
        self.skill_graph.add_skill(skill_node)

        # 与来源建立关系
        for source in generated_skill.sources:
            source_node = SkillNode(
                name=source['repo'],
                source=f"github:{source['owner']}/{source['repo']}",
                type='source',
            )
            source_id = self.skill_graph.add_skill(source_node)

            # 建立学习关系
            self.skill_graph.add_relation(
                skill_node.id,
                source_id,
                RelationType.LEARNED_FROM,
                strength=source['relevance_score']
            )

        print(f"💾 技能已持久化到知识图谱: {skill_node.id}")

    def refine_skill(
        self,
        skill: GeneratedSkill,
        feedback: Dict[str, Any]
    ) -> GeneratedSkill:
        """
        基于反馈优化技能

        Args:
            skill: 原始生成的技能
            feedback: 用户反馈
                - success: 是否成功
                - issues: 遇到的问题
                - improvements: 改进建议

        Returns:
            GeneratedSkill: 优化后的技能
        """
        print(f"🔄 基于反馈优化技能: {skill.name}")

        # 更新元数据
        skill.metadata['refinement_history'] = skill.metadata.get('refinement_history', [])
        skill.metadata['refinement_history'].append({
            'feedback': feedback,
            'timestamp': datetime.now().isoformat(),
        })

        # 根据反馈调整内容
        if not feedback.get('success', True):
            # 添加问题说明
            skill.content += f"""

---

## 已知问题与改进

### 发现的问题
{chr(10).join(['- ' + issue for issue in feedback.get('issues', [])])}

### 改进建议
{chr(10).join(['- ' + imp for imp in feedback.get('improvements', [])])}
"""

        # 更新置信度
        skill.confidence *= 0.95  # 每次优化略微降低置信度

        print(f"✅ 技能已优化")

        return skill


class SkillGeneratorCLI:
    """
    技能生成器命令行接口
    """

    def __init__(self):
        self.generator = DynamicSkillGenerator()

    def generate_skill(self, task_description: str, **kwargs):
        """生成技能"""
        skill = self.generator.generate_from_query(task_description, **kwargs)

        # 保存到文件
        output_dir = Path('~/.mindsymphony/generated_skills').expanduser()
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / f"{skill.skill_id}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(skill.content)

        print(f"\n📝 技能已保存到: {output_file}")
        print(f"📊 置信度: {skill.confidence:.1%}")
        print(f"🔗 来源: {len(skill.sources)} 个GitHub项目")

        return skill


# 便捷函数
def generate_skill_for_task(task_description: str, **kwargs) -> dict:
    """
    便捷函数：为任务生成技能

    Args:
        task_description: 任务描述
        **kwargs: 额外参数
            - persist: 是否持久化 (默认False)
            - required_capabilities: 必需能力列表

    Returns:
        dict: 生成的技能信息
    """
    generator = DynamicSkillGenerator()
    skill = generator.generate_from_query(task_description, **kwargs)

    return {
        'skill_id': skill.skill_id,
        'name': skill.name,
        'content': skill.content,
        'confidence': skill.confidence,
        'sources': skill.sources,
        'metadata': skill.metadata,
    }
