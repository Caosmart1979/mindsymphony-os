# A/B测试框架实现指南

## 概述

在MindSymphony中实现技能级别的A/B测试,用于优化技能选择和执行策略。

## 测试维度

### 1. 技能选择策略
- **Variant A**: 关键词匹配(基于INTEROP.yml patterns)
- **Variant B**: 语义相似度匹配(使用embeddings)
- **Metrics**: 准确率、响应时间、用户满意度

### 2. 执行策略
- **Variant A**: 直接执行(快速)
- **Variant B**: 预览确认(安全)
- **Metrics**: 成功率、重试率、任务完成质量

## 实现架构

```python
class ABTestFramework:
    def __init__(self):
        self.variants = []
        self.metrics = {}
        self.results = {}

    def load_variants_from_interop(self, skill_path):
        """从INTEROP.yml加载测试变体"""
        interop = load_yaml(f"{skill_path}/INTEROP.yml")
        if interop.get('ab_testing', {}).get('enabled'):
            self.variants = interop['ab_testing']['variants']
            self.metrics = interop['ab_testing']['metrics']

    def select_variant(self):
        """根据weight随机选择variant"""
        import random
        weights = [v['weight'] for v in self.variants]
        return random.choices(self.variants, weights=weights)[0]

    def record_metrics(self, variant_name, execution_data):
        """记录执行指标"""
        if variant_name not in self.results:
            self.results[variant_name] = {
                'invocations': 0,
                'successes': 0,
                'total_time': 0,
                'satisfaction_scores': []
            }

        result = self.results[variant_name]
        result['invocations'] += 1
        result['total_time'] += execution_data.get('execution_time', 0)

        if execution_data.get('success'):
            result['successes'] += 1

        if 'satisfaction' in execution_data:
            result['satisfaction_scores'].append(
                execution_data['satisfaction']
            )

    def analyze_results(self):
        """分析A/B测试结果"""
        report = {}
        for variant, data in self.results.items():
            if data['invocations'] > 0:
                report[variant] = {
                    'success_rate': data['successes'] / data['invocations'],
                    'avg_time': data['total_time'] / data['invocations'],
                    'avg_satisfaction': (
                        sum(data['satisfaction_scores']) / len(data['satisfaction_scores'])
                        if data['satisfaction_scores'] else 0
                    ),
                    'invocations': data['invocations']
                }
        return report
```

## 使用示例

### 1. 初始化测试

```yaml
# 在技能的INTEROP.yml中配置
ab_testing:
  enabled: true
  variants:
    - name: keyword-matching
      weight: 0.7  # 70%流量
      config:
        method: "keyword"
        threshold: 0.7
    - name: semantic-matching
      weight: 0.3  # 30%流量
      config:
        method: "semantic"
        model: "text-embedding-3-small"
  metrics: ["success_rate", "execution_time", "user_satisfaction"]
```

### 2. 执行测试

```python
# 在MindSymphony的路由逻辑中
framework = ABTestFramework()
framework.load_variants_from_interop("./skills/skills/frontend-design")

# 选择variant
variant = framework.select_variant()  # e.g., keyword-matching

# 执行技能
start_time = time.time()
result = execute_skill_with_variant(
    "frontend-design",
    variant['config']
)
execution_time = time.time() - start_time

# 记录指标
framework.record_metrics(variant['name'], {
    'success': result.get('success', False),
    'execution_time': execution_time,
    'satisfaction': result.get('user_rating')
})
```

### 3. 分析结果

```python
# 定期分析(例如每100次调用后)
report = framework.analyze_results()

for variant, metrics in report.items():
    print(f"{variant}:")
    print(f"  Success Rate: {metrics['success_rate']:.2%}")
    print(f"  Avg Time: {metrics['avg_time']:.2f}s")
    print(f"  Satisfaction: {metrics['avg_satisfaction']:.2f}/5.0")
    print(f"  Invocations: {metrics['invocations']}")
```

## 优化策略

### 1. 自适应权重

基于测试结果自动调整variant权重:

```python
def adaptive_weights(self, min_samples=100):
    """根据性能调整权重"""
    for skill in skills:
        report = self.analyze_results(skill)
        
        # 确保有足够样本
        if all(v['invocations'] > min_samples for v in report.values()):
            # 计算新权重(基于success_rate)
            total_rate = sum(v['success_rate'] for v in report.values())
            
            new_weights = {}
            for variant, metrics in report.items():
                performance_ratio = metrics['success_rate'] / total_rate
                # 给优胜者更多流量
                new_weights[variant] = min(0.9, performance_ratio * 1.5)
            
            # 归一化
            total = sum(new_weights.values())
            for variant in new_weights:
                new_weights[variant] /= total
            
            # 更新INTEROP.yml
            update_skill_weights(skill, new_weights)
```

### 2. 统计显著性

使用t检验确认variant差异是否显著:

```python
from scipy import stats

def is_significant(self, variant_a, variant_b, metric='success_rate'):
    """检验两个variant是否显著差异"""
    data_a = self.results[variant_a][metric]
    data_b = self.results[variant_b][metric]
    
    t_stat, p_value = stats.ttest_ind(data_a, data_b)
    
    return {
        'significant': p_value < 0.05,
        'p_value': p_value,
        't_statistic': t_stat
    }
```

### 3. 早期停止

当某个variant明显胜出时提前结束测试:

```python
def should_stop_test(self, confidence=0.95, min_samples=200):
    """判断是否应该停止测试"""
    report = self.analyze_results()
    
    if len(report) < 2:
        return False
    
    variants = list(report.values())
    
    # 检查样本量
    if any(v['invocations'] < min_samples for v in variants):
        return False
    
    # 检查性能差异
    rates = [v['success_rate'] for v in variants]
    max_diff = max(rates) - min(rates)
    
    # 如果差异>20%,停止测试
    if max_diff > 0.2:
        winner = max(report.items(), key=lambda x: x[1]['success_rate'])
        return {
            'stop': True,
            'winner': winner[0],
            'reason': f"Large performance gap: {max_diff:.2%}"
        }
    
    return False
```

## 集成到MindSymphony

### 1. 路由层集成

在`mindsymphony/SKILL.md`的意图路由部分添加:

```markdown
## 意图路由(增强版 - A/B测试)

```
用户输入 → A/B测试分流 → 技能发现 → 执行 → 指标记录
              ↓
         [keyword: 70%]
         [semantic: 30%]
```

### 2. 性能监控面板

创建简单的性能追踪:

```yaml
# skills/skills/mindsymphony/AB_TESTING_RESULTS.yml
last_updated: 2025-01-08

frontend-design:
  variants:
    keyword-matching:
      success_rate: 0.87
      avg_time: 2.3s
      invocations: 245
    semantic-matching:
      success_rate: 0.91
      avg_time: 3.1s
      invocations: 108
  winner: "semantic-matching"
  recommendation: "Increase semantic weight to 50%"
```

## 最佳实践

1. **从简单开始**: 先测试高流量技能(如frontend-design, doc-coauthoring)
2. **明确假设**: 每个测试都应该有明确的假设
3. **足够的样本**: 至少100次调用后再做决策
4. **一个变量**: 每次只测试一个变量
5. **长期监控**: 即使锁定winner,也要持续监控性能

## 下一步

- [ ] 实现ABTestFramework类
- [ ] 为Top 5技能启用A/B测试
- [ ] 创建性能监控面板
- [ ] 建立自动化报告机制
- [ ] 优化并推广到所有技能
