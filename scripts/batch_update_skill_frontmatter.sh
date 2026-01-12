#!/bin/bash

# 批量更新SKILL.md文件的frontmatter，添加interop_metadata

# Top 20技能列表及其interop配置
declare -A SKILLS=(
    ["cli-companion"]="corechan.cli_companion"
    ["context-builder"]="corechan.context_builder"
    ["conversation-coach"]="corechan.conversation_coach"
    ["creative-catalyst"]="corechan.creative_catalyst"
    ["debugger-detective"]="corechan.debugger_detective"
    ["emotion-engine"]="corechan.emotion_engine"
    ["environment-explorer"]="corechan.environment_explorer"
    ["file-fluent"]="corechan.file_fluent"
    ["git-genius"]="corechan.git_genius"
    ["hype-hunter"]="corechan.hype_hunter"
    ["insight-incubator"]="corechan.insight_incubator"
    ["integration-impresario"]="corechan.integration_impresario"
    ["log-logic"]="corechan.log_logic"
    ["memory-matrix"]="corechan.memory_matrix"
    ["meta-mediator"]="corechan.meta_mediator"
    ["pattern-pilot"]="corechan.pattern_pilot"
    ["project-pilot"]="corechan.project_pilot"
    ["research-ranger"]="corechan.research_ranger"
    ["sql-scout"]="corechan.sql_scout"
    ["style-symphonist"]="corechan.style_symphonist"
)

success_count=0
fail_count=0

for skill_name in "${!SKILLS[@]}"; do
    skill_id="${SKILLS[$skill_name]}"
    skill_file="skills/${skill_name}/SKILL.md"
    
    if [ ! -f "$skill_file" ]; then
        echo "❌ ${skill_name}: SKILL.md不存在"
        ((fail_count++))
        continue
    fi
    
    # 检查是否已有interop_metadata
    if grep -q "interop_metadata:" "$skill_file"; then
        echo "✓ ${skill_name}: 已存在interop_metadata，跳过"
        ((success_count++))
        continue
    fi
    
    # 使用sed在第二个---之前插入interop_metadata
    # 这个方法在frontmatter结束前插入内容
    if sed -i.bak '/^---$/{
        x
        /^$/!{
            x
            /^---$/!{
                x
                H
                b
            }
        }
        x
        /^---$/{
            a\
interop_metadata:\
  skill_id: '"$skill_id"'\
  api_version: v1\
  authentication: none\
  rate_limit:\
    requests_per_minute: 30
        }
    }' "$skill_file" 2>/dev/null; then
        echo "✅ ${skill_name}: 已更新frontmatter"
        ((success_count++))
        rm -f "${skill_file}.bak"
    else
        echo "⚠️  ${skill_name}: 更新失败，使用备用方法"
        # 备用方法：直接在第二个---前插入
        if awk 'BEGIN{found=0} /^---$/{if(found){print "interop_metadata:\n  skill_id: '"$skill_id"'\n  api_version: v1\n  authentication: none\n  rate_limit:\n    requests_per_minute: 30"}else{found=1}} {print}' "$skill_file" > "${skill_file}.tmp" && mv "${skill_file}.tmp" "$skill_file"; then
            echo "✅ ${skill_name}: 备用方法成功"
            ((success_count++))
        else
            echo "❌ ${skill_name}: 备用方法也失败"
            ((fail_count++))
        fi
        rm -f "${skill_file}.bak"
    fi
done

echo ""
echo "📊 批量更新完成:"
echo "   ✅ 成功: $success_count"
echo "   ❌ 失败: $fail_count"
echo "   📁 总计: ${#SKILLS[@]}"
