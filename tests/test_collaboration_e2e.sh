#!/bin/bash
# End-to-End Collaboration Test

echo "=== End-to-End Collaboration Chain Test ==="
echo ""

cd skills/skill_discovery

echo "Scenario 1: Frontend Design with Brand Guidelines"
echo "---------------------------------------------------"
python << 'PYEOF'
from skill_index import SkillIndex
from skill_router import SkillRouter

# Initialize system
index = SkillIndex('../skills')
router = SkillRouter(index)

# User wants to design a component with brand consistency
user_input = "I want to design a frontend component that follows our brand guidelines"

# Route the request
result = router.route(user_input)
print(f"User Request: {user_input}")
print(f"Primary Skill: {result.primary}")
print(f"Collaborators: {result.collaborators}")
print(f"Confidence: {result.confidence}%")
print(f"Reasoning: {result.reasoning}")

# Show the collaboration chain
print("\nCollaboration Chain:")
chain = router._infer_collaboration_chain(result.primary)
for i, skill in enumerate(chain, 1):
    print(f"  {i}. {skill}")
PYEOF

echo ""
echo "Scenario 2: Technical Documentation Co-authoring"
echo "-------------------------------------------------"
python << 'PYEOF'
from skill_index import SkillIndex
from skill_router import SkillRouter

# Initialize system
index = SkillIndex('../skills')
router = SkillRouter(index)

# User wants to co-author technical docs
user_input = "Help me write technical documentation for our API"

# Route the request
result = router.route(user_input)
print(f"User Request: {user_input}")
print(f"Primary Skill: {result.primary}")
print(f"Collaborators: {result.collaborators}")
print(f"Confidence: {result.confidence}%")
print(f"Reasoning: {result.reasoning}")

# Show the collaboration chain
print("\nCollaboration Chain:")
chain = router._infer_collaboration_chain(result.primary)
for i, skill in enumerate(chain, 1):
    print(f"  {i}. {skill}")
PYEOF

echo ""
echo "Scenario 3: Complex Multi-stage Design Task"
echo "--------------------------------------------"
python << 'PYEOF'
from skill_index import SkillIndex
from skill_router import SkillRouter

# Initialize system
index = SkillIndex('../skills')
router = SkillRouter(index)

# User has a complex design task
user_input = "Create a complete landing page design with brand consistency and responsive layouts"

# Route the request
result = router.route(user_input)
print(f"User Request: {user_input}")
print(f"Primary Skill: {result.primary}")
print(f"Collaborators: {result.collaborators}")
print(f"Confidence: {result.confidence}%")
print(f"Reasoning: {result.reasoning}")

# Get skill combination suggestion
print("\nOptimal Skill Combination:")
combo = router.suggest_combination("landing_page_design")
print(f"  Primary: {combo.get('primary', 'N/A')}")
print(f"  Collaborators: {combo.get('collaborators', [])}")
print(f"  Reasoning: {combo.get('reasoning', 'N/A')}")
PYEOF

echo ""
echo "Scenario 4: Resource Flow Analysis"
echo "-----------------------------------"
python << 'PYEOF'
from skill_index import SkillIndex

# Initialize system
index = SkillIndex('../skills')

# Analyze resource dependencies
print("Resource Dependency Analysis:")

# Find providers of design-tokens
providers = index.get_providers("design-tokens")
print(f"\nProviders of 'design-tokens': {providers}")

# Find consumers of design-tokens
consumers = index.get_consumers("design-tokens")
print(f"Consumers of 'design-tokens': {consumers}")

# Find providers of brand-guidelines
providers = index.get_providers("brand-guidelines")
print(f"\nProviders of 'brand-guidelines': {providers}")

# Find consumers of brand-guidelines  
consumers = index.get_consumers("brand-guidelines")
print(f"Consumers of 'brand-guidelines': {consumers}")

# Show resource flow
print("\nResource Flow:")
print("  brand-guidelines → frontend-design")
print("  design-tokens → frontend-design")
print("  component-specs → frontend-implementation")
PYEOF

cd ../..

echo ""
echo "=== End-to-End Test Complete ==="
