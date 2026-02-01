#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# MindSymphony v21.0 迁移脚本
# ═══════════════════════════════════════════════════════════════════════════════
# 版本: 21.0.0-evolution
# 更新: 2025-01-11
# 用途: 从 v20.x 升级到 v21.0
# ═══════════════════════════════════════════════════════════════════════════════

set -e  # 遇到错误立即退出

# ═══════════════════════════════════════════════════════════════════════════════
# 配置变量
# ═══════════════════════════════════════════════════════════════════════════════

MINDSYMPHONY_DIR="C:/Users/13466/.claude/mindsymphony-v21"
V21_CONFIG_SOURCE="D:/claudecode/mindsymphony-v21.0.config.yml"
BACKUP_SUFFIX="v20-pre-migration"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ═══════════════════════════════════════════════════════════════════════════════
# 辅助函数
# ═══════════════════════════════════════════════════════════════════════════════

print_header() {
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════════${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# ═══════════════════════════════════════════════════════════════════════════════
# 迁移步骤
# ═══════════════════════════════════════════════════════════════════════════════

# 步骤 1: 验证环境
step1_validate_environment() {
    print_header "步骤 1: 验证环境"

    # 检查 MindSymphony 目录
    if [ ! -d "$MINDSYMPHONY_DIR" ]; then
        print_error "MindSymphony 目录不存在: $MINDSYMPHONY_DIR"
        exit 1
    fi
    print_success "找到 MindSymphony 目录"

    # 检查 v21.0 配置文件
    if [ ! -f "$V21_CONFIG_SOURCE" ]; then
        print_error "v21.0 配置文件不存在: $V21_CONFIG_SOURCE"
        exit 1
    fi
    print_success "找到 v21.0 配置文件"

    # 检查当前配置文件
    if [ ! -f "$MINDSYMPHONY_DIR/mindsymphony.config.yml" ]; then
        print_error "当前配置文件不存在"
        exit 1
    fi
    print_success "找到当前配置文件"

    echo ""
}

# 步骤 2: 创建备份
step2_create_backup() {
    print_header "步骤 2: 创建备份"

    local backup_dir="$MINDSYMPHONY_DIR/backups/$BACKUP_SUFFIX"
    mkdir -p "$backup_dir"

    # 备份配置文件
    cp "$MINDSYMPHONY_DIR/mindsymphony.config.yml" "$backup_dir/mindsymphony.config.yml"
    print_success "配置文件已备份"

    # 备份记忆数据库（如果存在）
    if [ -d "$MINDSYMPHONY_DIR/memory" ]; then
        cp -r "$MINDSYMPHONY_DIR/memory" "$backup_dir/"
        print_success "记忆数据库已备份"
    fi

    echo ""
    print_info "备份位置: $backup_dir"
    echo ""
}

# 步骤 3: 创建 v21.0 目录结构
step3_create_directory_structure() {
    print_header "步骤 3: 创建 v21.0 目录结构"

    local v21_dir="$MINDSYMPHONY_DIR/../mindsymphony-v21"

    # 创建主目录
    mkdir -p "$v21_dir"
    print_success "创建 v21.0 主目录"

    # 创建子目录
    mkdir -p "$v21_dir/evolution"
    mkdir -p "$v21_dir/memory"
    mkdir -p "$v21_dir/logs"
    mkdir -p "$v21_dir/templates"

    print_success "创建子目录结构"

    echo ""
    print_info "v21.0 目录: $v21_dir"
    echo ""
}

# 步骤 4: 复制配置文件
step4_copy_configuration() {
    print_header "步骤 4: 复制配置文件"

    # 复制 v21.0 配置到原位置
    cp "$V21_CONFIG_SOURCE" "$MINDSYMPHONY_DIR/mindsymphony-v21.0.config.yml"
    print_success "v21.0 配置文件已复制"

    # 创建符号链接（可选）
    cd "$MINDSYMPHONY_DIR"
    if [ -f "mindsymphony.config.yml" ]; then
        mv mindsymphony.config.yml mindsymphony.config.yml.old
    fi
    cp mindsymphony-v21.0.config.yml mindsymphony.config.yml
    print_success "激活 v21.0 配置"

    echo ""
}

# 步骤 5: 初始化进化数据库
step5_init_evolution_db() {
    print_header "步骤 5: 初始化进化数据库"

    local v21_dir="$MINDSYMPHONY_DIR/../mindsymphony-v21"
    local db_path="$v21_dir/evolution/learning.db"

    # 创建 SQLite 数据库
    sqlite3 "$db_path" <<EOF
-- 技能使用统计表
CREATE TABLE IF NOT EXISTS skill_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    skill_name TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    trigger_type TEXT,
    success BOOLEAN,
    execution_time_ms INTEGER,
    user_satisfaction INTEGER
);

-- 触发模式统计表
CREATE TABLE IF NOT EXISTS trigger_patterns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    skill_name TEXT NOT NULL,
    pattern TEXT NOT NULL,
    match_count INTEGER DEFAULT 0,
    success_count INTEGER DEFAULT 0,
    last_used DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 用户偏好表
CREATE TABLE IF NOT EXISTS user_preferences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    preference_key TEXT NOT NULL UNIQUE,
    preference_value TEXT,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 进化指标表
CREATE TABLE IF NOT EXISTS evolution_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    metric_name TEXT NOT NULL,
    metric_value REAL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 协作统计表
CREATE TABLE IF NOT EXISTS collaboration_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_type TEXT NOT NULL,
    used_skills BOOLEAN,
    used_n8n BOOLEAN,
    hybrid BOOLEAN,
    success BOOLEAN,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_skill_usage_name ON skill_usage(skill_name);
CREATE INDEX IF NOT EXISTS idx_trigger_patterns_skill ON trigger_patterns(skill_name);
CREATE INDEX IF NOT EXISTS idx_evolution_metrics_name ON evolution_metrics(metric_name);
EOF

    print_success "进化数据库已初始化"
    echo ""
    print_info "数据库位置: $db_path"
    echo ""
}

# 步骤 6: 创建迁移模板
step6_create_templates() {
    print_header "步骤 6: 创建协作模板"

    local v21_dir="$MINDSYMPHONY_DIR/../mindsymphony-v21"
    local templates_dir="$v21_dir/templates"

    # 创建 Skills-n8n 协作模板
    cat > "$templates_dir/collaboration-templates.yml" <<'EOF'
# MindSymphony v21.0 协作模板

# 模板 1: 智能生成 + 自动分发
template_1_content_distribution:
  name: "内容生成与自动分发"
  description: "Skills 生成内容，n8n 自动分发"

  skills_phase:
    - skill: "scientific-writing"
      task: "生成内容草稿"
    - skill: "citation-management"
      task: "整理引用"

  n8n_phase:
    - node: "schedule"
      config: "设定定时时间"
    - node: "email"
      config: "发送给接收者"
    - node: "storage"
      config: "备份到云存储"

# 模板 2: 智能监控 + 告警
template_2_intelligent_monitoring:
  name: "智能监控与告警"
  description: "n8n 监控，Skills 智能分析"

  n8n_phase:
    - node: "http_request"
      config: "定时检查 API"
    - node: "condition"
      config: "判断异常条件"

  skills_phase:
    - skill: "knowledge-explorer"
      task: "分析问题原因"
    - skill: "codebase-ecologist"
      task: "提供解决方案"

# 模板 3: 数据处理管道
template_3_data_pipeline:
  name: "数据处理管道"
  description: "n8n 收集，Skills 处理，n8n 存储"

  n8n_phase:
    - node: "webhook"
      config: "接收数据"
    - node: "queue"
      config: "缓冲队列"

  skills_phase:
    - skill: "exploratory-data-analysis"
      task: "探索性分析"
    - skill: "matplotlib"
      task: "生成可视化"

  n8n_phase:
    - node: "database"
      config: "存储结果"
    - node: "notification"
      config: "发送通知"
EOF

    print_success "协作模板已创建"

    # 创建触发器示例
    cat > "$templates_dir/trigger-examples.yml" <<'EOF'
# MindSymphony v21.0 触发器配置示例

# 示例 1: 自定义技能触发器
example_1_custom_skill:
  skill: "my-custom-skill"
  priority: "medium"

  triggers:
    - type: "command"
      patterns: ["/my", "/custom"]
      weight: 10.0

    - type: "semantic"
      intent: "custom_task"
      examples:
        - "帮我执行自定义任务"
        - "运行我的脚本"
      weight: 8.0

    - type: "pattern"
      regex: "自定义|my.*task"
      weight: 5.0

  learning:
    track_usage: true
    optimize_patterns: true

# 示例 2: n8n 工作流触发器
example_2_n8n_workflow:
  skill: "h-01-n8n-workflow-architect"
  category: "workflow"

  triggers:
    - type: "semantic"
      intent: "workflow_automation"
      keywords: ["自动化", "定时", "工作流", "cron"]
      examples:
        - "设计一个自动化流程"
        - "每天定时执行任务"
      weight: 7.0

    - type: "pattern"
      regex: "n8n|工作流|自动化.*流程"
      weight: 6.0

  workflow_capabilities:
    - "scheduled_execution"
    - "external_integration"
    - "persistent_state"
EOF

    print_success "触发器示例已创建"
    echo ""
}

# 步骤 7: 验证配置
step7_validate_configuration() {
    print_header "步骤 7: 验证配置"

    local config_file="$MINDSYMPHONY_DIR/mindsymphony.config.yml"

    # 检查配置文件存在
    if [ ! -f "$config_file" ]; then
        print_error "配置文件不存在"
        return 1
    fi
    print_success "配置文件存在"

    # 检查版本号
    if grep -q "21.0.0-evolution" "$config_file"; then
        print_success "配置版本正确 (v21.0.0-evolution)"
    else
        print_warning "配置版本可能不正确"
    fi

    # 检查关键配置节
    local required_sections=(
        "unified_triggers"
        "evolution_protocol"
        "skills_n8n_collaboration"
    )

    for section in "${required_sections[@]}"; do
        if grep -q "$section:" "$config_file"; then
            print_success "找到配置节: $section"
        else
            print_warning "缺失配置节: $section"
        fi
    done

    echo ""
}

# 步骤 8: 创建摘要报告
step8_create_summary() {
    print_header "步骤 8: 创建迁移摘要"

    local v21_dir="$MINDSYMPHONY_DIR/../mindsymphony-v21"
    local summary_file="$v21_dir/migration-summary.md"

    cat > "$summary_file" <<EOF
# MindSymphony v21.0 迁移摘要

**迁移日期**: $(date +%Y-%m-%d)
**版本**: 21.0.0-evolution

---

## ✅ 迁移完成

### 已完成的步骤

1. **环境验证** ✓
   - MindSymphony 目录: $MINDSYMPHONY_DIR
   - 备份位置: $MINDSYMPHONY_DIR/backups/$BACKUP_SUFFIX

2. **备份创建** ✓
   - 配置文件已备份
   - 记忆数据库已备份

3. **目录结构** ✓
   - v21.0 目录: $v21_dir
   - 子目录: evolution, memory, logs, templates

4. **配置迁移** ✓
   - v21.0 配置已激活
   - 旧配置已保存为 .old

5. **数据库初始化** ✓
   - 进化数据库已创建
   - 表结构已建立

6. **模板创建** ✓
   - 协作模板已创建
   - 触发器示例已创建

---

## 🎯 新功能概览

### 1. 统一触发层
- 4种触发模式：命令、语义、模式、上下文
- 自动学习优化
- 权重动态调整

### 2. 进化协议
- 自我学习：使用追踪、模式优化
- 环境适应：项目检测、规范学习
- 协作进化：协同分析、集体智能

### 3. Skills-n8n 协作
- 智能路由：自动选择工具
- MCP 桥接：双向通信
- 协作模板：混合模式

---

## 📋 下一步操作

### 1. 测试基本功能
\`\`\`bash
# 测试命令触发
/paper

# 测试语义触发
"帮我写论文"

# 测试模式触发
"分析这个研究的学术价值"
\`\`\`

### 2. 监控进化数据
\`\`\`bash
sqlite3 $v21_dir/evolution/learning.db

# 查询使用统计
SELECT skill_name, COUNT(*) as count
FROM skill_usage
GROUP BY skill_name
ORDER BY count DESC
LIMIT 10;
\`\`\`

### 3. 配置 n8n 协作（可选）
\`\`\`yaml
skills_n8n_collaboration:
  enabled: true
  mcp_bridge:
    n8n_mcp_server:
      endpoint: "http://localhost:5678/mcp"
\`\`\`

---

## 🔄 回滚方法

如果需要回滚到 v20.1：

\`\`\`bash
cd $MINDSYMPHONY_DIR

# 恢复配置
cp backups/$BACKUP_SUFFIX/mindsymphony.config.yml mindsymphony.config.yml

# 恢复记忆（如果需要）
cp -r backups/$BACKUP_SUFFIX/memory ./
\`\`\`

---

## 📚 参考文档

- 配置文件: $MINDSYMPHONY_DIR/mindsymphony-v21.0.config.yml
- 迁移指南: D:/claudecode/MINDSYMPHONY_V21_MIGRATION_GUIDE.md
- 协作模板: $templates_dir/collaboration-templates.yml
- 触发器示例: $templates_dir/trigger-examples.yml

---

**祝你使用愉快！🎉**
EOF

    print_success "迁移摘要已创建"
    echo ""
    print_info "摘要位置: $summary_file"
    echo ""
}

# ═══════════════════════════════════════════════════════════════════════════════
# 主流程
# ═══════════════════════════════════════════════════════════════════════════════

main() {
    clear

    print_header "MindSymphony v21.0 迁移向导"
    echo ""
    print_info "版本: 21.0.0-evolution"
    print_info "日期: $(date +%Y-%m-%d)"
    echo ""

    # 询问确认
    print_warning "此操作将升级 MindSymphony 到 v21.0"
    echo ""
    read -p "是否继续？(y/N) " -n 1 -r
    echo ""

    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "迁移已取消"
        exit 0
    fi

    echo ""

    # 执行迁移步骤
    step1_validate_environment
    step2_create_backup
    step3_create_directory_structure
    step4_copy_configuration
    step5_init_evolution_db
    step6_create_templates
    step7_validate_configuration
    step8_create_summary

    # 完成
    print_header "迁移完成！"
    echo ""
    print_success "MindSymphony 已成功升级到 v21.0"
    echo ""
    print_info "新功能："
    echo "  • 统一触发层 - 更智能的技能调用"
    echo "  • 进化协议 - 自我学习和适应"
    echo "  • Skills-n8n 协作 - 智能工作流编排"
    echo ""
    print_info "查看迁移摘要: $MINDSYMPHONY_DIR/../mindsymphony-v21/migration-summary.md"
    echo ""
}

# 运行主流程
main "$@"
