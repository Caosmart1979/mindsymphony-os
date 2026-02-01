#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# MindSymphony v21.0 版本一致性检查脚本
# ═══════════════════════════════════════════════════════════════════════════════
# 版本: 21.0.0-evolution
# 更新: 2025-01-23
# 用途: 验证所有版本声明是否统一到 v21.0
# ═══════════════════════════════════════════════════════════════════════════════

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# 统计变量
total_checks=0
passed_checks=0
failed_checks=0

# 辅助函数
print_header() {
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}$1${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════════${NC}"
}

print_check() {
    echo -e "${BLUE}检查${NC} $1"
    ((total_checks++))
}

print_pass() {
    echo -e "${GREEN}  ✓ 通过${NC} - $1"
    ((passed_checks++))
}

print_fail() {
    echo -e "${RED}  ✗ 失败${NC} - $1"
    ((failed_checks++))
}

print_info() {
    echo -e "${YELLOW}  ℹ${NC} $1"
}

# ═══════════════════════════════════════════════════════════════════════════════
# 检查函数
# ═══════════════════════════════════════════════════════════════════════════════

check_skill_md() {
    print_check "SKILL.md 版本声明"

    local skill_file="D:/claudecode/skills/skills/mindsymphony/SKILL.md"

    if [ ! -f "$skill_file" ]; then
        print_fail "文件不存在: $skill_file"
        return 1
    fi

    local version=$(grep "^version:" "$skill_file" | head -1 | grep -o '21\.0\.0')

    if [[ "$version" == "21.0.0" ]]; then
        print_pass "SKILL.md 版本正确 (21.0.0)"
        return 0
    else
        print_fail "SKILL.md 版本不正确，期望 21.0.0"
        return 1
    fi
}

check_version_yml() {
    print_check "VERSION.yml 版本声明"

    local yml_file="D:/claudecode/skills/skills/mindsymphony/VERSION.yml"

    if [ ! -f "$yml_file" ]; then
        print_fail "文件不存在: $yml_file"
        return 1
    fi

    local version=$(grep "system_version:" "$yml_file" | head -1 | grep -o '21\.0\.0')

    if [[ "$version" == "21.0.0" ]]; then
        print_pass "VERSION.yml 版本正确 (21.0.0)"
        return 0
    else
        print_fail "VERSION.yml 版本不正确，期望 21.0.0"
        return 1
    fi
}

check_config_yml() {
    print_check "mindsymphony.config.yml 版本声明"

    local config_file="C:/Users/13466/.claude/mindsymphony-v21/mindsymphony-v15.6/mindsymphony.config.yml"

    if [ ! -f "$config_file" ]; then
        # 尝试备用路径
        config_file="C:/Users/13466/.claude/mindsymphony-v21/mindsymphony.config.yml"
    fi

    if [ ! -f "$config_file" ]; then
        print_fail "配置文件不存在"
        return 1
    fi

    local version=$(grep "version:" "$config_file" | head -1 | grep -o '21\.0\.0-evolution')

    if [[ "$version" == "21.0.0-evolution" ]]; then
        print_pass "配置文件版本正确 (21.0.0-evolution)"
        return 0
    else
        print_fail "配置文件版本不正确，期望 21.0.0-evolution"
        return 1
    fi
}

check_directory_name() {
    print_check "目录名称"

    if [ -d "C:/Users/13466/.claude/mindsymphony-v21" ]; then
        print_pass "目录名正确 (mindsymphony-v21)"
        return 0
    else
        print_fail "目录名不正确，期望 mindsymphony-v21"
        return 1
    fi
}

check_interop_yml() {
    print_check "INTEROP.yml 版本声明"

    local interop_file="D:/claudecode/skills/skills/mindsymphony/INTEROP.yml"

    if [ ! -f "$interop_file" ]; then
        print_fail "文件不存在: $interop_file"
        return 1
    fi

    local version=$(grep "version:" "$interop_file" | head -1 | grep -o '21\.0\.0')

    if [[ "$version" == "21.0.0" ]]; then
        print_pass "INTEROP.yml 版本正确 (21.0.0)"
        return 0
    else
        print_fail "INTEROP.yml 版本不正确，期望 21.0.0"
        return 1
    fi
}

check_claude_md() {
    print_check "CLAUDE.md 路径引用"

    local claude_md="C:/Users/13466/.claude/CLAUDE.md"

    if [ ! -f "$claude_md" ]; then
        print_fail "文件不存在: $claude_md"
        return 1
    fi

    if grep -q "mindsymphony-v21" "$claude_md"; then
        if grep -q "mindsymphony-v15.6" "$claude_md"; then
            print_fail "CLAUDE.md 包含旧路径引用 (v15.6)"
            return 1
        else
            print_pass "CLAUDE.md 路径正确 (v21)"
            return 0
        fi
    else
        print_fail "CLAUDE.md 没有找到 v21 路径引用"
        return 1
    fi
}

check_codename() {
    print_check "版本代号"

    local yml_file="D:/claudecode/skills/skills/mindsymphony/VERSION.yml"

    if [ ! -f "$yml_file" ]; then
        print_fail "VERSION.yml 文件不存在"
        return 1
    fi

    local codename=$(grep "codename:" "$yml_file" | head -1 | grep -i "evolutionary")

    if [[ -n "$codename" ]]; then
        print_pass "版本代号正确 (Evolutionary Intelligence)"
        return 0
    else
        print_fail "版本代号不正确，期望 Evolutionary Intelligence"
        return 1
    fi
}

check_ab_testing() {
    print_check "AB 测试配置"

    local interop_file="D:/claudecode/skills/skills/mindsymphony/INTEROP.yml"

    if [ ! -f "$interop_file" ]; then
        print_fail "INTEROP.yml 文件不存在"
        return 1
    fi

    # 检查 v21.0 权重是否为 100
    local v21_weight=$(grep -A 2 "name: v21.0" "$interop_file" | grep "weight:" | awk '{print $2}')

    if [[ "$v21_weight" == "100" ]]; then
        print_pass "AB 测试配置正确 (v21.0 权重 100)"
        return 0
    else
        print_fail "AB 测试配置不正确，v21.0 权重应为 100"
        return 1
    fi
}

check_changelog() {
    print_check "变更日志"

    local yml_file="D:/claudecode/skills/skills/mindsymphony/VERSION.yml"

    if [ ! -f "$yml_file" ]; then
        print_fail "VERSION.yml 文件不存在"
        return 1
    fi

    if grep -q '"21.0.0":' "$yml_file"; then
        print_pass "变更日志包含 v21.0.0 条目"
        return 0
    else
        print_fail "变更日志缺少 v21.0.0 条目"
        return 1
    fi
}

check_release_date() {
    print_check "发布日期"

    local yml_file="D:/claudecode/skills/skills/mindsymphony/VERSION.yml"

    if [ ! -f "$yml_file" ]; then
        print_fail "VERSION.yml 文件不存在"
        return 1
    fi

    local release_date=$(grep "release_date:" "$yml_file" | head -1 | grep -o '2025-01-11')

    if [[ "$release_date" == "2025-01-11" ]]; then
        print_pass "发布日期正确 (2025-01-11)"
        return 0
    else
        print_fail "发布日期不正确，期望 2025-01-11"
        return 1
    fi
}

check_backup_exists() {
    print_check "备份存在性"

    local backup_dir="C:/Users/13466/.claude/mindsymphony-v15.6.backup.20260123"

    if [ -d "$backup_dir" ]; then
        print_pass "备份目录存在"
        return 0
    else
        print_fail "备份目录不存在"
        return 1
    fi
}

check_features() {
    print_check "新功能开关"

    local config_file="C:/Users/13466/.claude/mindsymphony-v21/mindsymphony-v15.6/mindsymphony.config.yml"

    if [ ! -f "$config_file" ]; then
        config_file="C:/Users/13466/.claude/mindsymphony-v21/mindsymphony.config.yml"
    fi

    if [ ! -f "$config_file" ]; then
        print_fail "配置文件不存在"
        return 1
    fi

    local has_unified=$(grep -q "unified_triggers:" "$config_file" && echo "yes")
    local has_evolution=$(grep -q "evolution_protocol:" "$config_file" && echo "yes")
    local has_collaboration=$(grep -q "skills_n8n_collaboration:" "$config_file" && echo "yes")

    if [[ "$has_unified" == "yes" && "$has_evolution" == "yes" && "$has_collaboration" == "yes" ]]; then
        print_pass "所有新功能开关已启用"
        return 0
    else
        print_fail "部分新功能开关缺失"
        return 1
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
# 主检查流程
# ═══════════════════════════════════════════════════════════════════════════════

main() {
    clear

    print_header "MindSymphony v21.0 版本一致性检查"
    echo ""
    print_info "开始时间: $(date +%Y-%m-%d\ %H:%M:%S)"
    echo ""

    # 执行所有检查
    check_skill_md
    check_version_yml
    check_config_yml
    check_directory_name
    check_interop_yml
    check_claude_md
    check_codename
    check_ab_testing
    check_changelog
    check_release_date
    check_backup_exists
    check_features

    # 显示结果
    echo ""
    print_header "检查结果"
    echo ""
    echo -e "${CYAN}总检查项:${NC} $total_checks"
    echo -e "${GREEN}通过:${NC} $passed_checks"
    echo -e "${RED}失败:${NC} $failed_checks"
    echo ""

    local success_rate=0
    if [ $total_checks -gt 0 ]; then
        success_rate=$((passed_checks * 100 / total_checks))
    fi
    echo -e "${CYAN}成功率:${NC} $success_rate%"
    echo ""

    if [ $failed_checks -eq 0 ]; then
        echo -e "${GREEN}🎉 所有版本声明已统一到 v21.0！${NC}"
        echo ""
        print_info "系统版本: MindSymphony v21.0.0 (Evolutionary Intelligence)"
        print_info "代号: 进化智能体系统"
        print_info "发布日期: 2025-01-11"
        echo ""
        return 0
    else
        echo -e "${YELLOW}⚠ 部分检查失败，请检查上述错误${NC}"
        echo ""
        return 1
    fi
}

# 运行主流程
main "$@"
