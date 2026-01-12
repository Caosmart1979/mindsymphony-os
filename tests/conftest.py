"""
Pytest Configuration and Fixtures
"""

import pytest
import sys
import json
import os
from pathlib import Path
from typing import Dict, Any, List
import tempfile
import shutil

# Add skill discovery to path
project_root = Path(__file__).parent.parent
skill_discovery_path = project_root / "skills" / "skill_discovery"
if str(skill_discovery_path) not in sys.path:
    sys.path.insert(0, str(skill_discovery_path))


@pytest.fixture(scope="session")
def project_root():
    """Project root directory."""
    return Path(__file__).parent.parent


@pytest.fixture(scope="session")
def skills_root(project_root):
    """Skills directory path."""
    return project_root / "skills" / "skills"


@pytest.fixture(scope="session")
def skill_discovery_path(project_root):
    """Skill discovery module path."""
    return project_root / "skills" / "skill_discovery"


@pytest.fixture(scope="function")
def temp_directory():
    """Create a temporary directory for testing."""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)


@pytest.fixture(scope="function")
def temp_skill_directory(temp_directory):
    """Create a temporary skill directory structure."""
    skills_dir = temp_directory / "skills"
    skills_dir.mkdir()
    yield skills_dir


@pytest.fixture(scope="session")
def test_config():
    """Load test configuration."""
    config_path = project_root / "tests" / "config" / "test_config.json"
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


@pytest.fixture(scope="function")
def mock_skill_data():
    """Provide mock skill data for testing."""
    return [
        {
            "name": "test_skill_1",
            "description": "First test skill",
            "version": "1.0.0",
            "category": "testing",
            "tags": ["test", "unit"],
            "author": "Test Suite",
            "capabilities": ["run_tests", "assert_results"]
        },
        {
            "name": "design_skill",
            "description": "Design component skill",
            "version": "1.0.0",
            "category": "design",
            "tags": ["frontend", "ui", "ux"],
            "author": "Test Suite",
            "capabilities": ["create_component", "apply_styles"]
        },
        {
            "name": "code_skill",
            "description": "Code generation skill",
            "version": "1.0.0",
            "category": "code",
            "tags": ["backend", "api"],
            "author": "Test Suite",
            "capabilities": ["generate_code", "refactor"]
        }
    ]


@pytest.fixture(scope="function")
def create_mock_skill_files(temp_skill_directory, mock_skill_data):
    """Create mock skill metadata files in temp directory."""
    created_files = []

    for skill in mock_skill_data:
        file_path = temp_skill_directory / f"{skill['name']}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(skill, f, indent=2, ensure_ascii=False)
        created_files.append(file_path)

    return {
        "directory": temp_skill_directory,
        "files": created_files,
        "skills": mock_skill_data
    }


@pytest.fixture(scope="session")
def skill_index(skills_root):
    """Load or create skill index."""
    try:
        from skill_index import SkillIndex
        index = SkillIndex(str(skills_root))
        return index
    except Exception as e:
        pytest.skip(f"Could not load skill index: {e}")


@pytest.fixture(scope="session")
def skill_router(skill_index):
    """Load skill router."""
    try:
        from skill_router import SkillRouter
        router = SkillRouter(skill_index)
        return router
    except Exception as e:
        pytest.skip(f"Could not load skill router: {e}")


@pytest.fixture(scope="function")
def test_queries():
    """Provide test queries for routing."""
    return [
        "创建一个前端组件",
        "分析这段代码",
        "设计一个数据库",
        "运行单元测试",
        "生成API文档",
        "优化性能",
        "创建一个有品牌风格的设计",
        "编写测试用例",
        "refactor this function",
        "create a REST API"
    ]


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "unit: mark test as a unit test")
    config.addinivalue_line("markers", "integration: mark test as an integration test")
    config.addinivalue_line("markers", "e2e: mark test as an end-to-end test")
    config.addinivalue_line("markers", "performance: mark test as a performance test")
    config.addinivalue_line("markers", "slow: mark test as slow running")
