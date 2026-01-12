"""
Integration Tests for Skill System
"""

import pytest
import sys
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "skills" / "skill_discovery"))
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import base test
try:
    from utils.base_test import IntegrationTestBase
except ImportError:
    class IntegrationTestBase:
        @staticmethod
        def assert_data_flow(input_data, output_data):
            assert input_data is not None
            assert output_data is not None


@pytest.mark.integration
class TestSkillDiscoveryIntegration(IntegrationTestBase):
    """Test skill discovery system integration."""

    @pytest.fixture(autouse=True)
    def setup(self, skills_root):
        try:
            from skill_metadata import load_all_skills
            from skill_index import SkillIndex
            from skill_router import SkillRouter

            self.skills_root = str(skills_root)
            self.load_all_skills = load_all_skills
            self.SkillIndex = SkillIndex
            self.SkillRouter = SkillRouter
        except ImportError as e:
            pytest.skip(f"Required module not available: {e}")

    def test_metadata_to_index_integration(self):
        """Test integration from metadata loading to indexing."""
        # Load skills
        skills = self.load_all_skills(self.skills_root)
        assert isinstance(skills, dict), "Should load skills as dict"
        assert len(skills) > 0, "Should have at least one skill"

        # Create index
        index = self.SkillIndex(self.skills_root)
        assert index is not None, "Should create index"

        # Get statistics
        stats = index.get_statistics()
        assert isinstance(stats, dict), "Should get statistics"

        self.assert_data_flow(skills, stats)

    def test_index_to_router_integration(self):
        """Test integration from indexing to routing."""
        # Create index
        index = self.SkillIndex(self.skills_root)

        # Create router
        router = self.SkillRouter(index)
        assert router is not None, "Should create router"

        # Route a query
        query = "创建一个前端组件"
        result = router.route(query)
        assert result is not None, "Should route query"

        self.assert_data_flow(index, result)

    def test_full_pipeline_integration(self):
        """Test full pipeline from metadata to routing."""
        # Load metadata
        skills = self.load_all_skills(self.skills_root)
        assert len(skills) > 0, "Should have skills"

        # Create index
        index = self.SkillIndex(self.skills_root)
        stats = index.get_statistics()
        assert stats.get("total_skills", 0) > 0, "Should index skills"

        # Create router
        router = self.SkillRouter(index)

        # Route multiple queries
        test_queries = ["创建前端", "生成代码", "运行测试"]
        results = []
        for query in test_queries:
            result = router.route(query)
            results.append(result)
            assert result is not None, f"Should route query: {query}"

        self.assert_data_flow(skills, results)
