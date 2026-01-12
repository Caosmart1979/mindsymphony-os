#!/bin/bash
# Skill Collaboration System Test Script

echo "=== Skill Collaboration System Test Suite ==="
echo ""

cd skills/skill_discovery

# Test 1: Import modules
echo "Test 1: Importing modules..."
python -c "from skill_metadata import load_all_skills, SkillMetadata; from skill_index import SkillIndex; from skill_router import SkillRouter; from cache_manager import CacheManager" 2>&1
if [ $? -eq 0 ]; then
    echo "[PASS] Successfully imported all modules"
else
    echo "[FAIL] Failed to import modules"
    exit 1
fi

# Test 2: Load skills
echo ""
echo "Test 2: Loading skill metadata..."
python -c "
from skill_metadata import load_all_skills
skills = load_all_skills('../skills')
print(f'[PASS] Loaded {len(skills)} skill metadata files')
" 2>&1

# Test 3: Create index
echo ""
echo "Test 3: Creating skill index..."
python -c "
from skill_index import SkillIndex
index = SkillIndex('../skills')
stats = index.get_statistics()
print(f'[PASS] Created index with {stats.get(\"total_skills\", 0)} skills')
" 2>&1

# Test 4: Test routing
echo ""
echo "Test 4: Testing intelligent routing..."
python -c "
from skill_router import SkillRouter
from skill_index import SkillIndex
index = SkillIndex('../skills')
router = SkillRouter(index)
result = router.route('create a branded frontend component')
print(f'[PASS] Routed to {result.primary} (confidence: {result.confidence}%)')
" 2>&1

# Test 5: Test collaboration chains
echo ""
echo "Test 5: Testing collaboration chains..."
python -c "
from skill_router import SkillRouter
from skill_index import SkillIndex
index = SkillIndex('../skills')
router = SkillRouter(index)
collabs = router._infer_collaboration_chain('frontend-design')
print(f'[PASS] Found {len(collabs)} collaborators for frontend-design')
print(f'       Collaborators: {collabs}')
" 2>&1

# Test 6: Test skill combination suggestions
echo ""
echo "Test 6: Testing skill combination suggestions..."
python -c "
from skill_router import SkillRouter
from skill_index import SkillIndex
index = SkillIndex('../skills')
router = SkillRouter(index)
combo = router.suggest_combination('design_component')
print(f'[PASS] Suggested combination:')
print(f'       Primary: {combo.get(\"primary\", \"N/A\")}')
print(f'       Collaborators: {combo.get(\"collaborators\", [])}')
" 2>&1

cd ../..

echo ""
echo "=== Test Suite Complete ==="
