---
name: skill-creator-meta
type: integration
external_path: /mnt/skills/user/skill-creator-meta
priority: medium
triggers:
  zh: [创建skill, 技能开发, skill设计, 元技能, 铸造技能, 技能模板]
  en: [create skill, skill development, skill design, meta skill, forge skill]
---

# 技能创建元系统 (Skill Creator Meta) 快捷入口

> Skill创建方法论，从0到1构建高质量Claude Skills。

---

## 核心能力

1. **架构设计** - 目录结构、模块划分、依赖管理
2. **文档规范** - SKILL.md模板、frontmatter标准
3. **验证测试** - 结构验证、触发词测试
4. **迭代优化** - 真实场景测试、持续改进

---

## 触发词

### 中文
- 创建skill、技能开发、技能设计
- 铸造技能、技能模板
- 元技能、skill架构

### English
- create skill, skill development
- skill design, meta skill
- forge skill, skill template

---

## 命令前缀

```
/create-skill [技能名称或领域]
```

---

## 创建流程

```
1. 需求明确
   ├─ 这个skill要解决什么问题？
   ├─ 目标用户是谁？
   └─ 成功标准是什么？

2. 架构设计
   ├─ 单文件 vs 多文件结构
   ├─ 是否需要子模块
   └─ 依赖哪些外部资源

3. 内容编写
   ├─ SKILL.md主文件
   ├─ references/参考资料
   └─ examples/使用示例

4. 验证测试
   ├─ 结构验证：validate_skill.py
   ├─ 触发词测试
   └─ 端到端测试

5. 迭代优化
   ├─ 收集真实使用反馈
   ├─ 持续更新改进
   └─ 版本管理
```

---

## 使用示例

### 示例1：从0创建skill

```
用户：我想创建一个专门处理法律合同的skill

激活：skill-creator-meta
响应：
- 分析法律合同处理的核心能力
- 设计skill架构
- 生成SKILL.md模板
- 提供验证和测试指南
```

### 示例2：优化现有skill

```
用户：我的skill触发词不够准确，怎么优化？

激活：skill-creator-meta
响应：
- 分析当前触发词覆盖度
- 建议增加/删除的触发词
- 提供测试方法
```

### 示例3：skill架构咨询

```
用户：我的skill内容很多，应该拆分成多个文件吗？

激活：skill-creator-meta
响应：
- 评估内容量和复杂度
- 建议目录结构
- 提供模块化拆分方案
```

---

## 验证工具

```bash
# 验证skill结构
python3 /mnt/skills/user/skill-creator-meta/scripts/validate_skill.py /path/to/skill

# 输出示例
# ✅ Skill is valid!
# 或
# ⚠️ WARNINGS: ...
```

---

## 详细文档

完整文档位置：`/mnt/skills/user/skill-creator-meta/SKILL.md`

包含：
- 完整创建流程
- 架构模式库
- 验证脚本
- 最佳实践
