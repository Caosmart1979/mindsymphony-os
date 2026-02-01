---
name: academic-forge
type: integration
external_path: /mnt/skills/user/academic-forge
priority: high
triggers:
  zh: [学术, 论文, 研究设计, 统计方法, 文献, 投稿, NHANES, CHARLS, 队列研究, 方法学]
  en: [academic, paper, research design, statistics, literature, manuscript, cohort]
---

# 学术研究锻造 (Academic Forge) 快捷入口

> 端到端学术研究系统，从研究设计到投稿的全流程支持。

---

## 核心能力

1. **研究设计** - STROBE/CONSORT/TRIPOD报告规范
2. **统计方法** - 方法选择、样本量计算、敏感性分析
3. **手稿撰写** - Methods/Results/Discussion结构化写作
4. **投稿准备** - 期刊选择、Cover Letter、审稿回复

---

## 触发词

### 中文
- 学术、论文、研究设计、统计方法
- 文献综述、投稿、审稿回复
- NHANES、CHARLS、队列研究
- 预测模型、TRIPOD、方法学守护

### English
- academic, paper, research design
- statistics, literature review, manuscript
- cohort study, prediction model

---

## 命令前缀

```
/academic [你的研究问题]
```

---

## 模块导航

| 需求 | 去这里 |
|------|--------|
| 研究设计 | references/01-design/ |
| 统计方法 | references/02-methods/ |
| 特定数据集 | references/03-datasets/ |
| 预测建模 | references/04-prediction/ |
| 手稿写作 | references/05-writing/ |
| 投稿流程 | references/06-submission/ |

---

## 使用示例

### 示例1：研究设计咨询

```
用户：我想用NHANES数据研究BRI和死亡率的关系，应该用什么研究设计？

激活：academic-forge
响应：
- 推荐观察性队列设计
- 应用STROBE报告规范
- 建议亚组分析策略
- 提醒选择偏倚和混杂控制
```

### 示例2：统计方法选择

```
用户：我的因变量是生存时间，应该用什么统计方法？

激活：academic-forge
响应：
- Cox比例风险模型
- K-M生存曲线
- 比例风险假设检验
- 限制性立方样条处理非线性
```

### 示例3：审稿回复

```
用户：审稿人说我的样本量不足，怎么回复？

激活：academic-forge
响应：
- 补充事后功效分析
- 引用类似研究的样本量
- 承认局限性但强调发现的意义
- 提供敏感性分析结果
```

---

## 详细文档

完整文档位置：`/mnt/skills/user/academic-forge/SKILL.md`

包含：
- 6大模块详细参考
- 方法学守护协议
- 预审模拟系统
- R代码调试指南
