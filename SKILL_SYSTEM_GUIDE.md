# MindSymphony 技能系统使用手册

## 概述

MindSymphony 技能系统是一个用于管理、评估、优化和使用 Claude 技能的完整解决方案。它提供了一系列工具，帮助用户有效地管理技能库，提高技能的质量和使用效率。

## 系统架构

MindSymphony 技能系统包括以下核心组件：

1. **技能自动评估系统**：评估技能质量和完整性
2. **技能去重与合并工具**：检测和合并重复或相似的技能
3. **新技能引入管理工具**：规范从网上下载的新技能
4. **技能推荐引擎**：根据用户需求推荐合适的技能
5. **技能使用指南生成工具**：为每个技能生成详细的使用指南
6. **技能持续优化机制**：定期评估技能质量，提供优化建议

## 安装和配置

### 系统要求

- Python 3.7 或更高版本
- 必要的 Python 库：`PyYAML`, `Levenshtein`, `schedule`

### 安装依赖库

```bash
pip install PyYAML python-Levenshtein schedule
```

### 配置技能系统

1. 确保技能注册表文件 `skills.yml` 位于正确的位置
2. 检查技能路径配置是否正确
3. 配置技能使用数据存储位置

## 使用方法

### 技能自动评估系统

**功能**：评估技能质量和完整性，检查技能配置是否符合要求。

**使用命令**：
```bash
# 运行技能自动评估系统
python skill_assessor.py

# 自定义输出文件
python skill_assessor.py --output my_assessment_report.md

# 使用自定义技能注册表
python skill_assessor.py --registry /path/to/skills.yml
```

**输出**：生成技能质量评估报告，包含技能得分、质量等级分布等信息。

### 技能去重与合并工具

**功能**：检测和合并重复或相似的技能，减少技能库的冗余。

**使用命令**：
```bash
# 运行技能去重与合并工具
python skill_deduplicator.py

# 生成合并计划
python skill_deduplicator.py --plan

# 自定义相似度阈值（默认80%）
python skill_deduplicator.py --threshold 70

# 执行模拟合并
python skill_deduplicator.py --plan --execute --dry-run
```

**输出**：生成技能去重分析报告和合并计划。

### 新技能引入管理工具

**功能**：规范从网上下载的新技能，确保技能配置符合系统要求。

**使用命令**：
```bash
# 验证现有技能配置
python skill_introducer.py --validate

# 从文件导入技能
python skill_introducer.py --import-file /path/to/skill_file.yml --type internal

# 从URL导入技能（需要网络连接）
python skill_introducer.py --import-url "https://example.com/skill.yml" --type external

# 生成技能引入报告
python skill_introducer.py --validate --report introduction_report.md
```

**输出**：验证结果和技能引入报告。

### 技能推荐引擎

**功能**：根据用户需求推荐合适的技能，支持个性化推荐。

**使用命令**：
```bash
# 基于查询关键词推荐技能
python skill_recommender.py --query "数据分析" --num 5

# 个性化推荐（需要用户ID）
python skill_recommender.py --query "项目管理" --user "user123" --num 3

# 包含外部技能的推荐
python skill_recommender.py --query "机器学习" --include-external --num 10

# 生成推荐报告
python skill_recommender.py --query "深度学习" --report recommendation_report.md
```

**输出**：技能推荐列表和推荐报告。

### 技能使用指南生成工具

**功能**：为每个技能生成详细的使用指南，包括技能描述、触发词、使用示例等。

**使用命令**：
```bash
# 生成所有技能的使用指南
python skill_guide_generator.py --output skill_guides

# 只生成索引文件
python skill_guide_generator.py --index-only --output skill_guides

# 生成领域分类索引
python skill_guide_generator.py --index-only --domain-index --output skill_guides

# 生成快速参考卡片
python skill_guide_generator.py --quick-ref --output skill_guides

# 只生成单个技能的指南
python skill_guide_generator.py --single "data-analyst" --output single_guide
```

**输出**：技能使用指南目录，包含索引文件和各个技能的详细指南。

### 技能持续优化机制

**功能**：定期评估技能质量，提供优化建议，支持定时任务。

**使用命令**：
```bash
# 立即运行优化任务
python skill_optimizer.py --run --report optimization_report.md

# 启动定时优化任务（每天02:00运行）
python skill_optimizer.py --schedule

# 使用自定义配置文件
python skill_optimizer.py --config my_optimization_config.json --run
```

**配置文件示例**：
```json
{
    "quality_threshold": 70,
    "usage_threshold": 3,
    "inactive_days_threshold": 30,
    "optimization_categories": [
        "description_optimization",
        "trigger_optimization",
        "path_validation",
        "duplicate_detection",
        "usage_analysis"
    ],
    "automatic_optimization": false,
    "report_generation": true,
    "notification": false
}
```

## 整合测试

**功能**：运行所有工具的整合测试，确保系统健康运行。

**使用命令**：
```bash
python skill_system_tester.py
```

**输出**：测试结果摘要和详细的测试报告。

## 最佳实践

### 1. 定期维护技能库

```bash
# 每周运行一次技能评估和优化
python skill_assessor.py --output weekly_assessment.md
python skill_optimizer.py --run --report weekly_optimization.md
python skill_deduplicator.py --plan --threshold 75
```

### 2. 技能引入流程

```bash
# 新技能引入前的检查流程
python skill_introducer.py --import-file new_skill.yml --validate-only
python skill_deduplicator.py --check-similarity --similar-to new_skill
python skill_assessor.py --evaluate-single new_skill.yml
```

### 3. 技能优化流程

```bash
# 分析技能使用情况，优化低质量技能
python skill_optimizer.py --run --report optimization_report.md
python skill_guide_generator.py --update guides/
python skill_recommender.py --reindex
```

### 4. 技能版本管理

```bash
# 备份技能注册表
cp -r /path/to/skills.yml /path/to/skills_$(date +%Y%m%d).yml

# 恢复技能注册表
cp /path/to/skills_20231231.yml /path/to/skills.yml
```

## 故障排除

### 常见问题及解决方案

1. **技能路径无效**
   - 检查技能配置中的路径是否正确
   - 确保技能文件存在于指定位置
   - 修复路径后重新运行评估

2. **技能触发词不符合要求**
   - 检查触发词长度是否在2-10个字符之间
   - 确保触发词不含特殊字符
   - 补充中英文触发词

3. **技能重复或相似**
   - 运行技能去重工具
   - 调整相似度阈值
   - 手动评估相似技能，决定保留或合并

4. **技能未使用**
   - 检查技能描述和触发词是否准确
   - 提供更多使用示例
   - 考虑是否需要删除该技能

5. **工具运行失败**
   - 检查Python版本是否符合要求
   - 确保所有依赖库已正确安装
   - 查看错误信息，定位问题并修复

## 技术支持

如果遇到无法解决的问题，可以：

1. 查看测试报告中的详细错误信息
2. 检查技能配置文件是否正确
3. 查看日志文件，定位问题
4. 联系技术支持团队获取帮助

## 版本历史

### v1.0 (2026-01-18)

- 初始版本
- 包含技能自动评估系统
- 包含技能去重与合并工具
- 包含新技能引入管理工具
- 包含技能推荐引擎
- 包含技能使用指南生成工具
- 包含技能持续优化机制
- 包含整合测试脚本
- 提供完整的使用手册