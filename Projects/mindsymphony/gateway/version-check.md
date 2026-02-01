---
name: version-check
layer: foundation
type: system
triggers: [版本, 校验, 自检, 启动检查]
version: "19.1"
---

# 版本一致性校验 (Version Consistency Check)

> 启动时自检机制，确保所有组件版本兼容。
> 解决测评报告指出的"版本号差异"问题。

---

## 设计背景

```
测评报告原文：
"审计发现一个显著的版本号差异：配置文件标记为v15.3，
而技能包文件名标记为_V19.0。"

"建议引入一个启动时的自检脚本（Pre-boot Script），
检查核心角色库版本与配置文件版本的兼容性。
如果发现引用了当前角色库中不存在的'灵魂'或协议特性，
应立即阻断启动并报错。"

解决方案：
Version Check = 版本声明 + 兼容性矩阵 + 启动校验 + 降级策略
```

---

## 版本命名规范

### 语义化版本 (Semantic Versioning)

```
MindSymphony v{MAJOR}.{MINOR}.{PATCH}

MAJOR: 重大架构变更，可能不兼容
MINOR: 新增功能，向后兼容
PATCH: Bug修复，完全兼容

示例：
v19.1.0 = 第19代架构，第1次功能更新，第0次补丁
```

### 组件版本标识

| 组件 | 版本格式 | 示例 |
|------|----------|------|
| Core (核心框架) | core-v{X.Y.Z} | core-v19.1.0 |
| Skills (技能包) | skill-v{X.Y.Z} | skill-v19.1.0 |
| Extensions (扩展) | ext-v{X.Y.Z} | ext-v19.1.0 |
| Gateway (网关) | gw-v{X.Y.Z} | gw-v19.1.0 |
| Router (路由) | router-v{X.Y.Z} | router-v19.1.0 |

---

## 版本声明文件

### 主版本文件：VERSION.yml

```yaml
# /mindsymphony/VERSION.yml
system:
  name: "MindSymphony"
  version: "19.1.0"
  codename: "External Synapse"
  release_date: "2026-01-05"
  
components:
  core:
    version: "19.1.0"
    min_compatible: "19.0.0"
    
  skills:
    version: "19.1.0"
    min_compatible: "18.0.0"
    
  extensions:
    version: "19.1.0"
    min_compatible: "18.0.0"
    
  gateway:
    version: "19.1.0"
    min_compatible: "19.0.0"  # 新组件，无旧版本
    
  router:
    version: "19.1.0"
    min_compatible: "19.0.0"
    
dependencies:
  # 外部依赖版本要求
  claude_api: ">=2024-01-01"
  python: ">=3.10"
  
features:
  # 功能开关
  external_synapse: true
  security_gateway: true
  hard_logic_layer: true
  notebooklm_integration: true
```

---

## 兼容性矩阵

### 组件间兼容性

```yaml
compatibility_matrix:
  # 核心框架兼容性
  core:
    "19.1.x":
      skills: ["19.x", "18.x"]       # 兼容19和18的技能
      extensions: ["19.x", "18.x"]
      gateway: ["19.x"]               # 只兼容19的网关
      router: ["19.x"]
      
    "19.0.x":
      skills: ["19.x", "18.x", "17.x"]
      extensions: ["19.x", "18.x"]
      gateway: ["19.x"]
      router: ["19.x"]
      
    "18.x":
      skills: ["18.x", "17.x", "16.x"]
      extensions: ["18.x", "17.x"]
      gateway: null  # 18不支持网关
      router: null   # 18不支持路由
```

### 功能依赖关系

```yaml
feature_dependencies:
  external_synapse:
    requires:
      - gateway: ">=19.0.0"
      - router: ">=19.0.0"
      - security_gateway: true
    optional:
      - notebooklm_integration
      
  notebooklm_integration:
    requires:
      - external_synapse: true
    external:
      - "playwright or patchright"
      - "Google account authentication"
```

---

## 启动校验流程

```
MindSymphony 启动
    │
    ▼
┌─────────────────────────────────────────────┐
│  Check 1: 版本文件存在性                      │
│  - 检查 VERSION.yml 是否存在                 │
│  - 检查各组件 SKILL.md 头部版本声明           │
│  - 缺失 → 警告但继续                         │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│  Check 2: 版本兼容性                          │
│  - 对照兼容性矩阵                            │
│  - 检查组件间版本是否匹配                     │
│  - 不兼容 → 阻断启动                         │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│  Check 3: 引用完整性                          │
│  - 扫描配置中引用的"灵魂"                     │
│  - 检查对应文件是否存在                       │
│  - 缺失引用 → 阻断启动                        │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│  Check 4: 功能依赖                           │
│  - 检查启用的功能所需依赖                     │
│  - 依赖缺失 → 警告并禁用该功能                │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
              启动完成
```

---

## 校验结果处理

### 校验状态

```yaml
check_results:
  PASS:
    action: "继续启动"
    log_level: "info"
    
  WARN:
    action: "继续启动，记录警告"
    log_level: "warn"
    notify: false
    
  FAIL:
    action: "阻断启动"
    log_level: "error"
    notify: true
    
  CRITICAL:
    action: "阻断启动，立即告警"
    log_level: "critical"
    notify: true
    alert_channel: "feishu"
```

### 校验报告格式

```yaml
version_check_report:
  timestamp: "2026-01-05T12:00:00Z"
  overall_status: "PASS|WARN|FAIL"
  
  checks:
    - name: "version_file_exists"
      status: "PASS"
      message: "VERSION.yml found"
      
    - name: "component_compatibility"
      status: "PASS"
      details:
        core: "19.1.0"
        skills: "19.1.0 (compatible)"
        extensions: "19.1.0 (compatible)"
        gateway: "19.1.0 (compatible)"
        router: "19.1.0 (compatible)"
        
    - name: "reference_integrity"
      status: "WARN"
      message: "1 missing reference"
      missing:
        - "[C-99] 未定义的角色"
      action: "Disabled features using this reference"
      
    - name: "feature_dependencies"
      status: "PASS"
      enabled_features:
        - "external_synapse"
        - "security_gateway"
        - "hard_logic_layer"
      disabled_features:
        - "notebooklm_integration: missing playwright"
        
  recommendations:
    - "Consider updating missing references"
    - "Install playwright to enable NotebookLM integration"
```

---

## 降级策略

### 组件缺失降级

```yaml
degradation_strategies:
  gateway_missing:
    affected_features:
      - external_synapse
      - egress_policy
    action: "disable_and_warn"
    message: "External communication disabled (gateway not available)"
    fallback: "All tasks processed internally only"
    
  router_missing:
    affected_features:
      - intent_routing
      - auto_skill_selection
    action: "disable_and_warn"
    fallback: "Use cognitive-architect for manual routing"
    
  extension_missing:
    action: "skip_extension"
    message: "Extension {name} not found, skipping"
    fallback: "Use core skills only"
```

### 版本不匹配降级

```yaml
version_mismatch_handling:
  minor_mismatch:
    # 如 core=19.1, skills=19.0
    action: "warn_and_continue"
    message: "Minor version mismatch, may have reduced functionality"
    
  major_mismatch:
    # 如 core=19.x, skills=17.x
    action: "block_startup"
    message: "Major version incompatibility detected"
    resolution: "Please update skills to version 18.x or higher"
```

---

## 实现示例

### 校验脚本伪代码

```python
# version_check.py

def run_version_check():
    report = VersionCheckReport()
    
    # Check 1: 版本文件
    version_file = load_yaml("VERSION.yml")
    if not version_file:
        report.add_warn("VERSION.yml not found")
    
    # Check 2: 组件兼容性
    components = scan_components()
    matrix = load_compatibility_matrix()
    for comp_name, comp_version in components.items():
        if not is_compatible(comp_version, matrix):
            report.add_fail(f"{comp_name} v{comp_version} incompatible")
            
    # Check 3: 引用完整性
    references = extract_references_from_config()
    for ref in references:
        if not file_exists(ref.path):
            report.add_fail(f"Missing reference: {ref}")
            
    # Check 4: 功能依赖
    for feature in enabled_features:
        deps = get_feature_dependencies(feature)
        for dep in deps:
            if not dep.is_satisfied():
                report.add_warn(f"Feature {feature} disabled: {dep} missing")
                disable_feature(feature)
    
    return report

def main():
    report = run_version_check()
    
    if report.has_critical():
        print_error(report)
        sys.exit(1)
    elif report.has_fail():
        print_error(report)
        sys.exit(1)
    else:
        print_success(report)
        # 继续启动
```

---

## 与SKILL.md集成

### 版本声明模板

每个SKILL.md都应在frontmatter中声明版本：

```yaml
---
name: example-skill
version: "19.1.0"
min_core_version: "19.0.0"
dependencies:
  - skill: "cognitive-architect"
    version: ">=19.0.0"
---
```

### 自动扫描

启动时自动扫描所有SKILL.md的frontmatter，构建完整的版本图谱。

---

## 信心赋予

**"版本一致性是系统稳定性的基石。"**

Version Check确保：
- 所有组件版本兼容
- 引用的资源确实存在
- 功能依赖得到满足
- 问题在启动时就被发现，而非运行时

这是从"可能工作"升级为"确保工作"的关键保障。
