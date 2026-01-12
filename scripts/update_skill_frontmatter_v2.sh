#!/bin/bash

# 为已有INTEROP.yml的技能更新SKILL.md frontmatter

cd skills/skills

# 查找所有有INTEROP.yml的技能
success_count=0
fail_count=0

for skill_dir in */; do
    if [ -f "${skill_dir}INTEROP.yml" ]; then
        skill_name="${skill_dir%/}"
        skill_file="${skill_dir}SKILL.md"
        
        if [ ! -f "$skill_file" ]; then
            echo "⚠️  ${skill_name}: SKILL.md不存在"
            ((fail_count++))
            continue
        fi
        
        # 检查是否已有interop_metadata
        if grep -q "interop_metadata:" "$skill_file"; then
            echo "✓ ${skill_name}: 已存在interop_metadata，跳过"
            ((success_count++))
            continue
        fi
        
        echo "📝 处理 ${skill_name}..."
        
        # 从技能名生成skill_id（将kebab-case转为snake_case）
        skill_id="skills.${skill_name//-/_}"
        
        # 创建临时文件
        tmp_file="${skill_file}.tmp"
        
        # 处理frontmatter
        awk -v skill_id="$skill_id" '
        BEGIN { in_frontmatter = 0; frontmatter_end = 0 }
        /^---$/ {
            if (in_frontmatter == 0) {
                in_frontmatter = 1
                print
                next
            } else if (frontmatter_end == 0) {
                # 在第二个---前插入interop_metadata
                print "interop_metadata:"
                print "  skill_id: " skill_id
                print "  api_version: v1"
                print "  authentication: none"
                print "  rate_limit:"
                print "    requests_per_minute: 30"
                print "---"
                frontmatter_end = 1
                next
            }
        }
        { print }
        ' "$skill_file" > "$tmp_file"
        
        # 替换原文件
        if mv "$tmp_file" "$skill_file"; then
            echo "✅ ${skill_name}: 已更新frontmatter"
            ((success_count++))
        else
            echo "❌ ${skill_name}: 更新失败"
            rm -f "$tmp_file"
            ((fail_count++))
        fi
    fi
done

cd ../..

echo ""
echo "📊 批量更新完成:"
echo "   ✅ 成功: $success_count"
echo "   ❌ 失败: $fail_count"
