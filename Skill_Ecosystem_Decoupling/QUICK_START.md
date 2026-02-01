# 快速入门指南

## 5分钟上手

### 步骤 1: 了解系统

技能生态系统解耦系统允许你:
- ✅ 让技能自动发现和协作
- ✅ 用智能路由自动选择最佳技能组合
- ✅ 通过标准元数据描述技能能力

### 步骤 2: 查看现有技能

```bash
# 查看技能索引
cat skills/skill_index.json

# 列出所有技能
ls skills/
```

### 步骤 3: 运行测试

```bash
# 运行协作测试
python test_collaboration.py

# 查看测试结果
```

### 步骤 4: 使用智能路由

```python
# 示例: 自动路由到合适的技能
from skill_discovery.discovery import SkillDiscoverySystem

system = SkillDiscoverySystem()

# 自动发现并执行
result = system.route_and_execute(
    task="创建登录页面并验证品牌规范",
    context={'company': 'Acme Corp'}
)
```

## 常见使用场景

### 场景 1: 单个技能

```python
# 直接使用特定技能
skill = system.load_skill('frontend-design')
result = skill.execute("创建响应式页面")
```

### 场景 2: 顺序协作

```python
# 按顺序执行多个技能
chain = ['frontend-design', 'brand-guidelines', 'doc-coauthoring']
result = system.execute_chain(chain, task)
```

### 场景 3: 并行执行

```python
# 同时运行多个技能
skills = ['code-reviewer', 'test-runner', 'security-scanner']
results = system.execute_parallel(skills, task)
```

## 下一步

- 📖 阅读完整文档: [README.md](README.md)
- 🔧 学习创建技能: [SKILL_INTEROP_TEMPLATE.md](SKILL_INTEROP_TEMPLATE.md)
- 🧪 查看更多示例: [examples/](examples/)
