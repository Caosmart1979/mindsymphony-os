#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# MindSymphony v21.0 测试脚本
# ═══════════════════════════════════════════════════════════════════════════════

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

print_header() {
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}$1${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════════${NC}"
}

print_test() {
    echo -e "${BLUE}测试 $1: $2${NC}"
}

print_pass() {
    echo -e "${GREEN}✓ 通过${NC} - $1"
}

print_fail() {
    echo -e "${RED}✗ 失败${NC} - $1"
}

print_info() {
    echo -e "${YELLOW}ℹ${NC} $1"
}

# ═══════════════════════════════════════════════════════════════════════════════
# 测试函数
# ═══════════════════════════════════════════════════════════════════════════════

test_config_version() {
    print_test "1" "配置版本检查"

    local version=$(grep "version:" "C:/Users/13466/.claude/mindsymphony-v21/mindsymphony.config.yml" | head -1 | grep -o '21\.0\.0-evolution')

    if [ -n "$version" ]; then
        print_pass "配置版本正确 (v21.0.0-evolution)"
        return 0
    else
        print_fail "配置版本不正确"
        return 1
    fi
}

test_unified_triggers() {
    print_test "2" "统一触发层检查"

    if grep -q "unified_triggers:" "C:/Users/13466/.claude/mindsymphony-v21/mindsymphony.config.yml"; then
        print_pass "统一触发层已启用"
        return 0
    else
        print_fail "统一触发层未找到"
        return 1
    fi
}

test_evolution_protocol() {
    print_test "3" "进化协议检查"

    if grep -q "evolution_protocol:" "C:/Users/13466/.claude/mindsymphony-v21/mindsymphony.config.yml"; then
        print_pass "进化协议已启用"

        # 检查进化目录
        if [ -d "C:/Users/13466/.claude/mindsymphony-v21/evolution" ]; then
            print_pass "进化目录存在"
        else
            print_fail "进化目录不存在"
        fi

        return 0
    else
        print_fail "进化协议未找到"
        return 1
    fi
}

test_collaboration() {
    print_test "4" "Skills-n8n 协作层检查"

    if grep -q "skills_n8n_collaboration:" "C:/Users/13466/.claude/mindsymphony-v21/mindsymphony.config.yml"; then
        print_pass "Skills-n8n 协作层已启用"
        return 0
    else
        print_fail "Skills-n8n 协作层未找到"
        return 1
    fi
}

test_backup() {
    print_test "5" "备份文件检查"

    local backup_file="C:/Users/13466/.claude/mindsymphony-v21/mindsymphony.config.yml.backup.before-v21-activation"

    if [ -f "$backup_file" ]; then
        print_pass "备份文件存在"
        return 0
    else
        print_fail "备份文件不存在"
        return 1
    fi
}

test_templates() {
    print_test "6" "模板文件检查"

    local templates_dir="C:/Users/13466/.claude/mindsymphony-v21/templates"

    if [ -f "$templates_dir/collaboration-templates.yml" ]; then
        print_pass "协作模板存在"
    else
        print_fail "协作模板不存在"
    fi

    if [ -f "$templates_dir/trigger-examples.yml" ]; then
        print_pass "触发器示例存在"
    else
        print_fail "触发器示例不存在"
    fi
}

test_skill_triggers() {
    print_test "7" "技能触发器检查"

    local config="C:/Users/13466/.claude/mindsymphony-v21/mindsymphony.config.yml"

    # 检查是否有技能触发器配置
    if grep -q "skill_triggers:" "$config"; then
        print_pass "技能触发器配置存在"

        # 统计触发器数量
        local count=$(grep -c "triggers:" "$config" || echo "0")
        print_info "找到 $count 个触发器配置"
    else
        print_fail "技能触发器配置不存在"
    fi
}

print_test_examples() {
    print_header "测试示例命令"

    echo -e "${GREEN}命令触发测试:${NC}"
    echo "  /paper"
    echo "  /cite"
    echo "  /analyze"

    echo ""
    echo -e "${GREEN}语义触发测试:${NC}"
    echo "  帮我写一篇研究论文"
    echo "  分析这个代码库的结构"
    echo "  设计一个自动化工作流"

    echo ""
    echo -e "${GREEN}模式触发测试:${NC}"
    echo "  这个研究的学术价值"
    echo "  论文写作指南"
    echo "  机器学习模型训练"
}

print_next_steps() {
    print_header "下一步操作"

    echo -e "${CYAN}1. 立即测试${NC}"
    echo "   尝试上面列出的测试命令"

    echo ""
    echo -e "${CYAN}2. 观察进化数据${NC}"
    echo "   使用一段时间后查看数据库"
    echo "   sqlite3 C:/Users/13466/.claude/mindsymphony-v21/evolution/learning.db"

    echo ""
    echo -e "${CYAN}3. 配置 n8n 协作（可选）${NC}"
    echo "   如果使用 n8n，配置 MCP 桥接"

    echo ""
    echo -e "${CYAN}4. 自定义触发器${NC}"
    echo "   参考 templates/trigger-examples.yml"
}

# ═══════════════════════════════════════════════════════════════════════════════
# 主测试流程
# ═══════════════════════════════════════════════════════════════════════════════

main() {
    clear

    print_header "MindSymphony v21.0 测试套件"
    echo ""
    print_info "版本: 21.0.0-evolution"
    print_info "日期: $(date +%Y-%m-%d)"
    echo ""

    # 运行测试
    local passed=0
    local failed=0

    test_config_version && ((passed++)) || ((failed++))
    test_unified_triggers && ((passed++)) || ((failed++))
    test_evolution_protocol && ((passed++)) || ((failed++))
    test_collaboration && ((passed++)) || ((failed++))
    test_backup && ((passed++)) || ((failed++))
    test_templates && ((passed++)) || ((failed++))
    test_skill_triggers && ((passed++)) || ((failed++))

    # 测试结果
    echo ""
    print_header "测试结果"
    echo -e "${GREEN}通过: $passed${NC}"
    echo -e "${RED}失败: $failed${NC}"
    echo ""

    if [ $failed -eq 0 ]; then
        echo -e "${GREEN}🎉 所有测试通过！v21.0 已成功激活！${NC}"
    else
        echo -e "${YELLOW}⚠ 部分测试失败，请检查配置${NC}"
    fi

    echo ""
    print_test_examples
    echo ""
    print_next_steps
    echo ""
}

# 运行测试
main "$@"
