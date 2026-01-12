#!/usr/bin/env python3
"""
Skill Collaboration System Test Suite
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Change to skill discovery directory for imports
os.chdir('skills/skill_discovery')

try:
    from skill_metadata import load_all_skills, SkillMetadata
    from skill_index import SkillIndex
    from skill_router import SkillRouter, RouteResult
    from cache_manager import CacheManager
    
    print("[PASS] Successfully imported collaboration modules")
    
    # Test skill metadata loading
    skills_root = "../skills"
    skills = load_all_skills(skills_root)
    print(f"[PASS] Loaded {len(skills)} skill metadata files")
    
    # Test skill index
    index = SkillIndex(skills_root)
    stats = index.get_statistics()
    print(f"[PASS] Created skill index with {stats.get('total_skills', 0)} skills")
    
    # Test skill router
    router = SkillRouter(index)
    print("[PASS] Skill router initialized")
    
    # Test route planning
    test_input = "创建一个有品牌风格的前端组件"
    result = router.route(test_input)
    print(f"[PASS] Routed query to {result.primary} (confidence: {result.confidence}%)")
    
    # Test collaboration chain inference
    collaborators = router._infer_collaboration_chain("frontend-design")
    print(f"[PASS] Found {len(collaborators)} collaborators for frontend-design")
    
    # Test combination suggestion
    combo = router.suggest_combination("design_component")
    print(f"[PASS] Suggested skill combination: {combo.get('primary', 'N/A')}")
    
    print("\n[SUCCESS] All basic tests passed!")
    
except Exception as e:
    print(f"[FAIL] Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
