---
name: inner-loop-automation
module: meta
layer: qi
triggers: ['自动化', '重复任务', '快捷命令', '内循环']
type: execution
source: boris-cherny-13-tips
---

# 内循环自动化 (Inner Loop Automation)

> 基于Boris Cherny的经验："对于每天都要重复多次的'内循环'工作流，我都会使用斜杠命令。这省去了重复输入Prompt的麻烦。"

---

## 核心原则

```
高频操作 → 自动化 → 效率飞跃

手动方式：每次输入完整prompt → 等待理解 → 执行 → 重复
自动化方式：/command → 立即执行 → 节省80%时间
```

---

## 内循环识别

内循环 = 每天重复3次以上的操作模式

### 常见内循环

| 场景 | 内循环操作 | 自动化价值 |
|------|-----------|-----------|
| 开发 | commit + push + PR | ⭐⭐⭐ |
| 开发 | lint + test | ⭐⭐⭐ |
| 写作 | 格式化 + 校对 | ⭐⭐ |
| 研究 | 搜索 + 总结 | ⭐⭐ |

---

## 自动化层级

1. **Prompt模板** - 保存常用prompt
2. **Slash Commands** - 定义快捷命令
3. **Subagents** - 独立子代理处理特定任务

---

## 信心赋予

**"我和Claude每天会用几十次/commit-push-pr命令"** —— Boris

识别你的内循环，然后自动化它。
