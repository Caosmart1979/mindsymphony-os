# 技能发现系统 - 快速开始指南

## 🚀 5分钟快速上手

### 步骤1: 查看已配置的技能

```bash
# 列出所有已配置INTEROP.yml的技能
ls -1 ./skills/skills/*/INTEROP.yml | wc -l
# 输出: 20

# 查看某个技能的配置
cat ./skills/skills/frontend-design/INTEROP.yml
```

### 步骤2: 运行测试

```bash
# 运行完整测试套件
python test_discovery_system.py

# 预期输出:
# ✅ Passed: 3
# ⚠️  Warnings: 2
# ✗ Failed: 0
# 🎉 All tests passed!
```

### 步骤3: 测试技能发现

```python
# 在Python中使用
from test_discovery_system import SkillDiscoveryTest

# 创建测试实例
tester = SkillDiscoveryTest()
tester.load_all_interop_configs()

# 测试查询
query = "Create a React component"
matches = tester.discover_skills(query)

# 查看结果
for skill, score in matches:
    print(f"{skill}: {score:.3f}")
# 输出:
# frontend-design: 0.720
```

## 📖 核心概念

### INTEROP.yml结构

```yaml
skill:
  name: skill-name          # 技能名称
  version: 1.0.0            # 版本号
  category: design          # 类别
  priority: high            # 优先级: critical|high|medium|low
  status: active            # 状态

discovery:
  auto_route: true          # 是否自动路由
  confidence_threshold: 0.7 # 置信度阈值
  routing_patterns:         # 路由模式
    - pattern: "react|vue|frontend"
      confidence: 0.9       # 匹配时的置信度
  related_skills: []        # 相关技能

ab_testing:
  enabled: true             # 是否启用A/B测试
  variants:                 # 测试变体
    - name: variant-a
      weight: 0.5           # 流量分配权重
  metrics:                  # 测试指标
    - success_rate
    - execution_time
```

### 发现算法

```python
# 1. 匹配routing_patterns
pattern_matches = [
    ("frontend-design", 0.9),  # pattern匹配的置信度
    ("doc-coauthoring", 0.7),
]

# 2. 应用优先级权重
priority_weights = {
    "critical": 1.0,
    "high": 0.8,
    "medium": 0.6,
    "low": 0.4,
}

# 3. 计算最终分数
final_score = pattern_confidence * priority_weight

# 4. 过滤低分结果
if final_score >= confidence_threshold:
    return skill
```

## 🎯 实际应用示例

### 示例1: 自动技能选择

**场景:** 用户说"帮我写一个API文档"

**发现流程:**
```python
query = "帮我写一个API文档"
matches = discover_skills(query)

# 结果:
# 1. doc-coauthoring: 0.720 (高优先级 + 匹配"docs")
# 2. api-integration-designer: 0.540 (中等优先级 + 匹配"api")
```

**决策:** 选择doc-coauthoring

### 示例2: 多技能协作

**场景:** 用户说"设计一个完整的Web应用,包括前端和后端"

**发现流程:**
```python
query = "设计一个完整的Web应用,包括前端和后端"
matches = discover_skills(query)

# 结果:
# 1. frontend-design: 0.720
# 2. api-integration-designer: 0.540
# 3. mindsymphony: 0.720
```

**决策:** 触发mindsymphony进行任务分解和协调

### 示例3: A/B测试

**场景:** 测试两种技能选择策略

```python
# 配置A/B测试
ab_testing:
  enabled: true
  variants:
    - name: keyword-matching
      weight: 0.7  # 70%流量使用关键词匹配
    - name: semantic-matching
      weight: 0.3  # 30%流量使用语义匹配

# 执行测试
variant = select_variant()  # 随机选择
result = execute_skill(variant)

# 记录指标
record_metrics(variant, {
    'success': True,
    'execution_time': 2.3,
    'user_satisfaction': 4.5
})
```

## 🔧 配置优化

### 优化1: 调整置信度阈值

**问题:** 召回率低,很多查询未匹配

**解决:**
```yaml
# 从
discovery:
  confidence_threshold: 0.7

# 改为
discovery  confidence_threshold: 0.5  # 更宽松
```

### 优化2: 添加更多patterns

**问题:** 某些查询无法匹配

**解决:**
```yaml
discovery:
  routing_patterns:
    - pattern: "poster|art|design"
      confidence: 0.9
    # 添加新的pattern
    - pattern: "graphic|visual|creative"
      confidence: 0.85
```

### 优化3: 调整优先级

**问题:** 重要技能没有被优先选择

**解决:**
```yaml
# 从
skill:
  priority: medium

# 改为
skill:
  priority: high  # 提高优先级
```

## 📊 监控指标

### 关键指标

1. **准确率:** 正确技能在Top-3的比例
   - 目标: >90%
   
2. **召回率:** 成功匹配至少一个技能的比例
   - 目标: >85%
   
3. **平均响应时间:** 从查询到返回结果的时间
   - 目标: <100ms

### 查看性能数据

```yaml
# 在INTEROP.yml中
performance:
  avg_execution_time: 2345ms    # 平均执行时间
  avg_success_rate: 0.87       # 成功率
  total_invocations: 152       # 总调用次数
  last_invocation: 2025-01-08  # 最后调用时间
```

## 🚨 常见问题

### Q1: 为什么我的查询没有匹配到任何技能?

**A:** 可能的原因:
1. 置信度阈值过高 → 降低threshold
2. routing_patterns不够全面 → 添加更多patterns
3. 查询表述模糊 → 使用更明确的关键词

### Q2: 如何为新技能添加INTEROP.yml?

**A:** 复制模板并修改:
```bash
# 复制现有配置
cp ./skills/skills/frontend-design/INTEROP.yml \
   ./skills/skills/my-new-skill/INTEROP.yml

# 编辑配置
vim ./skills/skills/my-new-skill/INTEROP.yml
```

### Q3: A/B测试需要多少样本?

**A:** 建议:
- 最小样本: 100次调用/variant
- 推荐样本: 500-1000次调用/variant
- 统计显著性: p-value < 0.05

### Q4: 如何调试技能发现?

**A:** 使用测试脚本:
```python
tester = SkillDiscoveryTest()
tester.load_all_interop_configs()

# 查看所有patterns
for skill, config in tester.skills.items():
    patterns = config['discovery']['routing_patterns']
    print(f"{skill}: {patterns}")

# 测试特定查询
query = "your query here"
matches = tester.discover_skills(query, top_n=10)
for skill, score in matches:
    print(f"{skill}: {score}")
```

## 📚 下一步

1. ✅ 完成: 为Top 20技能创建INTEROP.yml
2. ⏳ 待办: 优化routing_patterns
3. ⏳ 待办: 实现Discovery Engine
4. ⏳ 待办: 集成到MindSymphony
5. ⏳ 待办: 启用A/B测试

## 💡 最佳实践

1. **从高价值技能开始:** 优先配置常用技能
2. **数据驱动:** 基于实际使用数据优化patterns
3. **持续监控:** 定期查看性能指标
4. **A/B测试:** 对重要决策进行A/B测试
5. **版本控制:** INTEROP.yml的变更也要版本管理

---

**需要帮助?** 查看:
- `PROJECT_SUMMARY.md` - 完整项目总结
- `mindsymphony/DISCOVERY_ROUTING.md` - 系统设计文档
- `mindsymphony/AB_TESTING.md` - A/B测试指南
