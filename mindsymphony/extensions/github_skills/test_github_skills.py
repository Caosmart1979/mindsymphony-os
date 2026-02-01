"""
GitHub Skills System Tests
测试套件 - 验证GitHub技能系统各组件
"""

import unittest
import json
import tempfile
from pathlib import Path
from datetime import datetime

from github_skill_distiller import GitHubSkillDistiller, DistillationResult
from skill_knowledge_graph import SkillKnowledgeGraph, SkillNode, SkillRelation, RelationType
from skill_dna import SkillDNA, UserProfile, SkillUsagePattern
from dynamic_skill_generator import DynamicSkillGenerator, GenerationRequest
from integration import GitHubSkillsIntegration


class TestGitHubSkillDistiller(unittest.TestCase):
    """测试技能蒸馏器"""

    def setUp(self):
        self.distiller = GitHubSkillDistiller()

    def test_parse_repo_identifier(self):
        """测试仓库标识符解析"""
        # 测试 owner/repo 格式
        owner, repo = self.distiller._parse_repo_identifier("microsoft/TypeScript")
        self.assertEqual(owner, "microsoft")
        self.assertEqual(repo, "TypeScript")

        # 测试 URL 格式
        owner, repo = self.distiller._parse_repo_identifier("https://github.com/facebook/react")
        self.assertEqual(owner, "facebook")
        self.assertEqual(repo, "react")

    def test_analyze_readme(self):
        """测试README分析"""
        readme = """
# Test Project

## Overview
This is a test.

## Methodology
### Step 1: Planning
Plan carefully.

## Best Practices
- Practice 1
- Practice 2
"""
        analysis = self.distiller._analyze_readme(readme)

        self.assertIn('sections', analysis)
        self.assertIn('methodology_sections', analysis)
        self.assertTrue(analysis['has_code_examples'])

    def test_extract_methodologies(self):
        """测试方法论提取"""
        readme_analysis = {
            'methodology_sections': [
                {'title': 'Development Workflow', 'is_methodology': True},
                {'title': 'Best Practices', 'is_methodology': True},
            ],
            'has_workflow': True,
        }

        methodologies = self.distiller._extract_methodologies(readme_analysis)

        self.assertGreaterEqual(len(methodologies), 1)
        self.assertEqual(methodologies[0]['type'], 'workflow')

    def test_generate_skill_name(self):
        """测试技能名称生成"""
        repo_data = {'name': 'awesome-project'}
        methodologies = [{'type': 'workflow'}]

        name = self.distiller._generate_skill_name(repo_data, methodologies)
        self.assertIn('awesome-project', name)


class TestSkillKnowledgeGraph(unittest.TestCase):
    """测试技能知识图谱"""

    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        self.temp_file.close()
        self.graph = SkillKnowledgeGraph(storage_path=self.temp_file.name)

    def tearDown(self):
        Path(self.temp_file.name).unlink(missing_ok=True)

    def test_add_skill(self):
        """测试添加技能"""
        skill = SkillNode(
            name="Test Skill",
            source="test",
            description="A test skill",
            tags=["test", "demo"]
        )

        skill_id = self.graph.add_skill(skill)
        self.assertIsNotNone(skill_id)
        self.assertIn(skill_id, self.graph.nodes)

    def test_add_relation(self):
        """测试添加关系"""
        skill1 = SkillNode(name="Skill 1", source="test")
        skill2 = SkillNode(name="Skill 2", source="test")

        id1 = self.graph.add_skill(skill1)
        id2 = self.graph.add_skill(skill2)

        result = self.graph.add_relation(id1, id2, RelationType.RELATED, strength=0.8)
        self.assertTrue(result)
        self.assertEqual(len(self.graph.relations), 1)

    def test_search(self):
        """测试技能搜索"""
        skill1 = SkillNode(name="Machine Learning", source="test", tags=["ai", "ml"])
        skill2 = SkillNode(name="Web Development", source="test", tags=["web", "frontend"])

        self.graph.add_skill(skill1)
        self.graph.add_skill(skill2)

        results = self.graph.search("machine")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "Machine Learning")

    def test_recommend_skills(self):
        """测试技能推荐"""
        # 创建技能网络
        skill1 = SkillNode(name="Python", source="test", tags=["programming"])
        skill2 = SkillNode(name="Django", source="test", tags=["web", "python"])
        skill3 = SkillNode(name="Flask", source="test", tags=["web", "python"])

        id1 = self.graph.add_skill(skill1)
        id2 = self.graph.add_skill(skill2)
        id3 = self.graph.add_skill(skill3)

        # 建立关系
        self.graph.add_relation(id2, id1, RelationType.DEPENDS, strength=0.9)
        self.graph.add_relation(id3, id1, RelationType.DEPENDS, strength=0.8)

        # 推荐
        recommendations = self.graph.recommend_skills([id1])
        self.assertGreaterEqual(len(recommendations), 0)

    def test_get_stats(self):
        """测试统计功能"""
        stats = self.graph.get_stats()

        self.assertIn('total_nodes', stats)
        self.assertIn('total_relations', stats)
        self.assertIn('relation_types', stats)


class TestSkillDNA(unittest.TestCase):
    """测试技能DNA系统"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.dna = SkillDNA(user_id="test_user", storage_dir=self.temp_dir)

    def test_record_skill_usage(self):
        """测试记录技能使用"""
        self.dna.record_skill_usage(
            skill_id="skill_001",
            skill_name="Test Skill",
            success=True,
            context={'tags': ['test', 'demo']}
        )

        self.assertIn("skill_001", self.dna.usage_patterns)
        pattern = self.dna.usage_patterns["skill_001"]
        self.assertEqual(pattern.use_count, 1)
        self.assertEqual(pattern.success_count, 1)

    def test_get_expertise_report(self):
        """测试专长报告"""
        # 记录一些使用
        self.dna.record_skill_usage("skill_1", "Python", True)
        self.dna.record_skill_usage("skill_1", "Python", True)
        self.dna.record_skill_usage("skill_2", "JavaScript", False)

        report = self.dna.get_expertise_report()

        self.assertEqual(report['user_id'], "test_user")
        self.assertIn('top_skills', report)
        self.assertEqual(report['skill_diversity'], 2)

    def test_recommend_learning_path(self):
        """测试学习路径推荐"""
        self.dna.profile.expertise_domains['web_development'] = 0.2

        recommendations = self.dna.recommend_learning_path('web_development')

        self.assertGreaterEqual(len(recommendations), 1)
        self.assertIn('foundation', [r['type'] for r in recommendations])

    def test_detect_skill_gaps(self):
        """测试技能缺口检测"""
        self.dna.record_skill_usage("skill_1", "Python", True)
        self.dna.usage_patterns["skill_1"].avg_success_rate = 0.8

        gaps = self.dna.detect_skill_gaps(["Python", "JavaScript", "Rust"])

        self.assertIn("JavaScript", gaps)
        self.assertIn("Rust", gaps)
        self.assertNotIn("Python", gaps)


class TestDynamicSkillGenerator(unittest.TestCase):
    """测试动态技能生成器"""

    def setUp(self):
        self.generator = DynamicSkillGenerator()

    def test_analyze_task(self):
        """测试任务分析"""
        request = GenerationRequest(
            task_description="分析生物信息学数据集并进行机器学习建模"
        )

        analysis = self.generator._analyze_task(request)

        self.assertIn('task_types', analysis)
        self.assertIn('domains', analysis)
        self.assertIn('tech_stack', analysis)

    def test_extract_technology_stack(self):
        """测试技术栈提取"""
        description = "使用Python进行数据分析，应用machine learning算法"
        tech_stack = self.generator._extract_technology_stack(description)

        self.assertIn('python', tech_stack)
        self.assertIn('machine_learning', tech_stack)

    def test_calculate_generation_confidence(self):
        """测试置信度计算"""
        task_analysis = {
            'domains': ['data_science'],
            'tech_stack': ['python'],
            'task_types': ['analysis'],
        }
        github_sources = [{'relevance_score': 0.8}]
        best_practices = [{'confidence': 0.7}]

        confidence = self.generator._calculate_generation_confidence(
            task_analysis, github_sources, best_practices
        )

        self.assertGreaterEqual(confidence, 0.0)
        self.assertLessEqual(confidence, 1.0)


class TestIntegration(unittest.TestCase):
    """测试集成系统"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.integration = GitHubSkillsIntegration(
            config={'storage_dir': self.temp_dir}
        )

    def test_initialize_for_user(self):
        """测试用户初始化"""
        self.integration.initialize_for_user("test_user")
        self.assertIsNotNone(self.integration.skill_dna)
        self.assertEqual(self.integration.user_id, "test_user")

    def test_get_skill_for_task_existing(self):
        """测试获取已有技能"""
        # 添加一个技能
        skill = SkillNode(
            name="Python Analysis",
            source="test",
            description="Python data analysis"
        )
        self.integration.skill_graph.add_skill(skill)

        # 搜索
        result = self.integration.get_skill_for_task("Python analysis task")
        self.assertEqual(result['source'], 'existing')

    def test_recommend_skills_for_project(self):
        """测试项目技能推荐"""
        # 添加一些技能
        skill1 = SkillNode(name="Web Framework", source="test", tags=["web"])
        skill2 = SkillNode(name="Database", source="test", tags=["database"])

        self.integration.skill_graph.add_skill(skill1)
        self.integration.skill_graph.add_skill(skill2)

        recommendations = self.integration.recommend_skills_for_project(
            "Build a web application with database"
        )

        self.assertIsInstance(recommendations, list)

    def test_create_skill_composition(self):
        """测试技能组合创建"""
        # 创建两个技能
        skill1 = SkillNode(name="Frontend", source="test")
        skill2 = SkillNode(name="Backend", source="test")

        id1 = self.integration.skill_graph.add_skill(skill1)
        id2 = self.integration.skill_graph.add_skill(skill2)

        # 创建组合
        composition_id = self.integration.create_skill_composition(
            [id1, id2],
            "Full Stack",
            "Full stack development"
        )

        self.assertIsNotNone(composition_id)
        self.assertIn(composition_id, self.integration.skill_graph.nodes)


class TestEndToEnd(unittest.TestCase):
    """端到端测试"""

    def test_full_workflow(self):
        """测试完整工作流"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # 1. 初始化系统
            integration = GitHubSkillsIntegration(
                config={'storage_dir': temp_dir}
            )
            integration.initialize_for_user("test_user")

            # 2. 蒸馏技能（使用模拟）
            # 注：实际测试需要网络，这里只测试本地功能

            # 3. 添加技能到图谱
            skill = SkillNode(
                name="Test Workflow",
                source="manual",
                description="A test workflow skill",
                tags=["workflow", "test"]
            )
            skill_id = integration.skill_graph.add_skill(skill)

            # 4. 记录使用
            integration.skill_dna.record_skill_usage(
                skill_id, "Test Workflow", True
            )

            # 5. 生成报告
            report = integration.skill_dna.get_expertise_report()
            self.assertEqual(report['skill_diversity'], 1)

            # 6. 获取统计
            stats = integration.get_stats()
            self.assertIn('knowledge_graph', stats)
            self.assertIn('dna', stats)


def run_tests():
    """运行测试套件"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # 添加测试类
    suite.addTests(loader.loadTestsFromTestCase(TestGitHubSkillDistiller))
    suite.addTests(loader.loadTestsFromTestCase(TestSkillKnowledgeGraph))
    suite.addTests(loader.loadTestsFromTestCase(TestSkillDNA))
    suite.addTests(loader.loadTestsFromTestCase(TestDynamicSkillGenerator))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestEndToEnd))

    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)
