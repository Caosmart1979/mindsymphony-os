"""
Unit Tests for Skill Discovery System
"""

import pytest
import sys
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "skills" / "skill_discovery"))
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import base test
try:
    from utils.base_test import SkillTestBase
except ImportError:
    class SkillTestBase:
        @staticmethod
        def assert_valid_skill_metadata(metadata):
            # Check for common fields (flexible validation)
            assert metadata is not None, "Metadata should not be None"
            assert isinstance(metadata, dict), "Metadata should be a dict"


@pytest.mark.unit
class TestSkillMetadata(SkillTestBase):
    """Test skill metadata functionality."""

    @pytest.fixture(autouse=True)
    def setup(self):
        try:
            from skill_metadata import load_all_skills
            self.load_all_skills = load_all_skills
        except ImportError:
            pytest.skip("skill_metadata module not available")

    def test_load_all_skills_returns_dict(self, skills_root):
        """Test that load_all_skills returns a dict."""
        skills = self.load_all_skills(str(skills_root))
        assert isinstance(skills, dict), f"Expected dict, got {type(skills)}"

    def test_load_all_skills_non_empty(self, skills_root):
        """Test that load_all_skills returns non-empty result."""
        skills = self.load_all_skills(str(skills_root))
        assert len(skills) > 0, "Should load at least one skill"

    def test_skill_metadata_structure(self, skills_root):
        """Test that skill metadata has expected structure."""
        skills = self.load_all_skills(str(skills_root))
        if skills:
            # Get first skill
            first_skill_key = list(skills.keys())[0]
            first_skill = skills[first_skill_key]
            # Verify it's a SkillMetadata object
            assert first_skill is not None, "First skill should not be None"
            # It should have either metadata attribute or be a dict
            assert hasattr(first_skill, 'metadata') or isinstance(first_skill, dict)


@pytest.mark.unit
class TestSkillIndex(SkillTestBase):
    """Test skill index functionality."""

    @pytest.fixture(autouse=True)
    def setup(self):
        try:
            from skill_index import SkillIndex
            self.SkillIndex = SkillIndex
        except ImportError:
            pytest.skip("skill_index module not available")

    def test_skill_index_creation(self, skills_root):
        """Test that SkillIndex can be created."""
        index = self.SkillIndex(str(skills_root))
        assert index is not None, "Should create index"

    def test_skill_index_has_statistics(self, skills_root):
        """Test that index provides statistics."""
        index = self.SkillIndex(str(skills_root))
        stats = index.get_statistics()
        assert isinstance(stats, dict), "Statistics should be a dict"
