#!/bin/bash

echo "============================================================"
echo "🚀 技能发现与A/B测试系统"
echo "============================================================"

echo ""
echo "📊 1. 技能统计"
echo "----------------------------------------"

# 统计技能
total_skills=$(find skills/skills -name "SKILL.md" | wc -l)
with_interop=$(find skills/skills -name "INTEROP.yml" | wc -l)
with_frontmatter=$(grep -l "interop_metadata:" skills/skills/*/SKILL.md 2>/dev/null | wc -l)

echo "总技能数: $total_skills"
echo "有INTEROP.yml: $with_interop"
echo "有interop_metadata: $with_frontmatter"

echo ""
echo "📂 2. 技能列表"
echo "----------------------------------------"

find skills/skills -name "SKILL.md" -exec dirname {} \; | xargs -I {} basename {} | head -10

echo ""
echo "🧪 3. A/B测试配置"
echo "----------------------------------------"

# 选择前2个技能进行A/B测试
skill_a=$(find skills/skills -name "SKILL.md" -exec dirname {} \; | xargs -I {} basename {} | head -1)
skill_b=$(find skills/skills -name "SKILL.md" -exec dirname {} \; | xargs -I {} basename {} | head -2 | tail -1)

echo "A/B测试配置:"
echo "  测试名称: skill_comparison"
echo "  变体A: $skill_a"
echo "  变体B: $skill_b"
echo "  流量分配: 50% / 50%"

echo ""
echo "📝 4. 模拟路由"
echo "----------------------------------------"

for i in {1..10}; do
  if [ $((i % 2)) -eq 0 ]; then
    echo "  user$i -> $skill_a"
  else
    echo "  user$i -> $skill_b"
  fi
done

echo ""
echo "📊 5. 测试报告"
echo "----------------------------------------"
echo "  $skill_a: 5 次选择 (50%)"
echo "  $skill_b: 5 次选择 (50%)"

echo ""
echo "✅ 测试完成！"
echo "============================================================"
