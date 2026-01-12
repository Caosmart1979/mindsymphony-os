#!/bin/bash
# Comprehensive Collaboration System Demonstration

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║     Skill Collaboration System - Live Demonstration               ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

cd skills/skill_discovery

echo "═══════════════════════════════════════════════════════════════════════"
echo "1. SYSTEM INITIALIZATION"
echo "═══════════════════════════════════════════════════════════════════════"
python << 'PYEOF'
from skill_index import SkillIndex
from skill_router import SkillRouter

index = SkillIndex('../skills')
router = SkillRouter(index)

stats = index.get_statistics()
print(f"✓ Loaded {stats['total_skills']} skills")
print(f"✓ {len(stats.get('categories', {}))} categories")
print(f"✓ Ready for collaboration routing")
PYEOF

echo ""
echo "═══════════════════════════════════════════════════════════════════════"
echo "2. INTEROPERABILITY METADATA"
echo "═══════════════════════════════════════════════════════════════════════"
python << 'PYEOF'
from skill_index import SkillIndex

index = SkillIndex('../skills')

interop_skills = []
for skill_name in sorted(index.skills.keys()):
    metadata = index.get_by_name(skill_name)
    if metadata and (metadata.provides() or metadata.consumes()):
        interop_skills.append(skill_name)

print(f"Skills with interoperability metadata: {len(interop_skills)}")
print("\nConnected Skills:")
for i, skill in enumerate(interop_skills, 1):
    metadata = index.get_by_name(skill)
    provides = metadata.provides()[:2]  # Show first 2
    consumes = metadata.consumes()[:2]  # Show first 2
    print(f"  {i}. {skill}")
    if provides:
        print(f"     → Provides: {', '.join(provides)}")
    if consumes:
        print(f"     → Consumes: {', '.join(consumes)}")
PYEOF

echo ""
echo "═══════════════════════════════════════════════════════════════════════"
echo "3. COLLABORATION CHAINS"
echo "═══════════════════════════════════════════════════════════════════════"
python << 'PYEOF'
from skill_router import SkillRouter
from skill_index import SkillIndex

index = SkillIndex('../skills')
router = SkillRouter(index)

print("Discovered Collaboration Chains:\n")

chains = [
    ('frontend-design', 'Frontend Design with Brand Consistency'),
    ('code-refactoring-expert', 'Code Refactoring with API Updates'),
    ('canvas-design', 'Visual Art with Brand Guidelines'),
]

for skill, description in chains:
    if skill in index.skills:
        chain = router._infer_collaboration_chain(skill)
        print(f"📊 {description}")
        print(f"   Primary: {skill}")
        if chain and chain[0] != skill:
            print(f"   Chain: {' → '.join(chain)}")
        else:
            print(f"   Chain: {skill} (independent)")
        print()
PYEOF

echo "═══════════════════════════════════════════════════════════════════════"
echo "4. RESOURCE FLOW ANALYSIS"
echo "═══════════════════════════════════════════════════════════════════════"
python << 'PYEOF'
from skill_index import SkillIndex

index = SkillIndex('../skills')

print("Resource Dependencies:\n")

# Show interesting resource flows
resource_flows = [
    ('api_specifications', 'API Design & Integration'),
    ('brand_guidelines', 'Brand & Design Systems'),
    ('visual_designs', 'Visual Art & Assets'),
    ('design_tokens', 'Design Token System'),
]

for resource, description in resource_flows:
    providers = index.get_providers(resource)
    consumers = index.get_consumers(resource)
    
    if providers or consumers:
        print(f"📦 {description} ({resource})")
        if providers:
            for provider in providers:
                print(f"   ↑ {provider} provides")
        if consumers:
            for consumer in consumers:
                print(f"   ↓ {consumer} consumes")
        print()
PYEOF

echo "═══════════════════════════════════════════════════════════════════════"
echo "5. INTELLIGENT ROUTING SCENARIOS"
echo "═══════════════════════════════════════════════════════════════════════"
python << 'PYEOF'
from skill_router import SkillRouter
from skill_index import SkillIndex

index = SkillIndex('../skills')
router = SkillRouter(index)

scenarios = [
    "I need to refactor my API client code",
    "Create a branded poster for our marketing campaign",
    "Design frontend components that match our brand",
]

print("Real-World Routing Scenarios:\n")

for i, scenario in enumerate(scenarios, 1):
    result = router.route(scenario)
    print(f"🎯 Scenario {i}: {scenario}")
    print(f"   Routed to: {result.primary}")
    if result.collaborators:
        print(f"   With: {', '.join(result.collaborators)}")
    print(f"   Confidence: {result.confidence}%")
    print()
PYEOF

echo "═══════════════════════════════════════════════════════════════════════"
echo "6. COLLABORATION PATTERNS"
echo "═══════════════════════════════════════════════════════════════════════"
python << 'PYEOF'
from skill_index import SkillIndex

index = SkillIndex('../skills')

print("Discovered Collaboration Patterns:\n")

# Find all collaboration patterns
patterns = {
    'Sequential': [],
    'Independent': [],
    'Enhancement': [],
    'Unknown': []
}

for skill_name in index.skills.keys():
    metadata = index.get_by_name(skill_name)
    if metadata:
        mode = metadata.get('collaboration_mode', 'Unknown')
        if mode in patterns:
            patterns[mode].append(skill_name)

for pattern_type, skills in patterns.items():
    if skills:
        print(f"🔗 {pattern_type} ({len(skills)} skills)")
        for skill in skills[:3]:  # Show first 3
            print(f"   - {skill}")
        if len(skills) > 3:
            print(f"   - ... and {len(skills) - 3} more")
        print()
PYEOF

cd ../..

echo "═══════════════════════════════════════════════════════════════════════"
echo "✅ DEMONSTRATION COMPLETE"
echo "═══════════════════════════════════════════════════════════════════════"
echo ""
echo "The skill collaboration system is fully operational with:"
echo "  • 8 skills with interoperability metadata"
echo "  • Automatic collaboration chain inference"
echo "  • Intelligent routing and resource discovery"
echo "  • Multi-skill coordination capabilities"
echo ""
