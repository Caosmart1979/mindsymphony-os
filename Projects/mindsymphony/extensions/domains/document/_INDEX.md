---
name: document-extension
description: "文档处理扩展包。4个技能覆盖docx、pdf、pptx、xlsx等常见文档格式的创建和编辑。"
skills: 4
domain: document
---

# 文档处理扩展包 (Document Extension)

> 专业文档的创建、编辑和格式化。

## 技能列表

| 技能 | 定位 | 格式 |
|------|------|------|
| **docx** | Word文档处理 | .docx |
| **pdf** | PDF文档处理 | .pdf |
| **pptx** | 演示文稿处理 | .pptx |
| **xlsx** | 电子表格处理 | .xlsx |

## 使用场景

| 场景 | 推荐技能 |
|------|----------|
| "创建一个Word文档" | docx |
| "生成PDF报告" | pdf |
| "制作PPT演示" | pptx |
| "创建Excel表格" | xlsx |

## 加载方式

```yaml
extensions:
  enabled:
    - domains/document
```
