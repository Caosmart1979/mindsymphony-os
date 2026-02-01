#!/usr/bin/env python3
"""
Quick Test Runner - Runs a subset of tests for fast validation
"""

import sys
import os
from pathlib import Path

# Set UTF-8 encoding for Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Add paths
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "skills" / "skill_discovery"))

def run_quick_tests():
    """Run a quick subset of tests."""
    print("="*60)
    print("AI Agent Framework - Quick Test Suite")
    print("="*60)
    print()

    tests_passed = 0
    tests_failed = 0

    # Test 1: Import modules
    print("Test 1: Importing modules...")
    try:
        from skill_metadata import load_all_skills
        from skill_index import SkillIndex
        from skill_router import SkillRouter
        print("[PASS] All modules imported successfully\n")
        tests_passed += 1
    except Exception as e:
        print(f"[FAIL] Could not import modules: {e}\n")
        tests_failed += 1
        return tests_passed, tests_failed

    # Test 2: Load skills
    print("Test 2: Loading skills...")
    try:
        skills_root = Path(__file__).parent / "skills" / "skills"
        skills = load_all_skills(str(skills_root))
        print(f"[PASS] Loaded {len(skills)} skills\n")
        tests_passed += 1
    except Exception as e:
        print(f"[FAIL] Could not load skills: {e}\n")
        tests_failed += 1

    # Test 3: Create index
    print("Test 3: Creating skill index...")
    try:
        index = SkillIndex(str(skills_root))
        stats = index.get_statistics()
        print(f"[PASS] Index created with {stats.get('total_skills', 0)} skills\n")
        tests_passed += 1
    except Exception as e:
        print(f"[FAIL] Could not create index: {e}\n")
        tests_failed += 1

    # Test 4: Create router
    print("Test 4: Creating skill router...")
    try:
        router = SkillRouter(index)
        print("[PASS] Router created successfully\n")
        tests_passed += 1
    except Exception as e:
        print(f"[FAIL] Could not create router: {e}\n")
        tests_failed += 1

    # Test 5: Route query
    print("Test 5: Routing test query...")
    try:
        test_query = "创建一个前端组件"
        result = router.route(test_query)
        print(f"[PASS] Routed '{test_query}' to {result.primary} (confidence: {result.confidence}%)\n")
        tests_passed += 1
    except Exception as e:
        print(f"[FAIL] Could not route query: {e}\n")
        tests_failed += 1

    # Summary
    print("="*60)
    print("Quick Test Summary")
    print("="*60)
    print(f"[PASS] Passed: {tests_passed}")
    print(f"[FAIL] Failed: {tests_failed}")
    print(f"[TOTAL] Total:  {tests_passed + tests_failed}")
    print("="*60)

    return tests_passed, tests_failed


if __name__ == "__main__":
    passed, failed = run_quick_tests()

    if failed == 0:
        print("\n[SUCCESS] All quick tests passed!")
        sys.exit(0)
    else:
        print(f"\n[WARNING] {failed} test(s) failed")
        sys.exit(1)
