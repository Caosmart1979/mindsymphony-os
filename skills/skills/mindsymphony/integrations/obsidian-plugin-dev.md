---
name: obsidian-plugin-dev
type: integration
external_path: /skills/skills/obsidian-plugin-dev
priority: high
triggers:
  zh: [Obsidian插件, obsidian插件, 插件开发, manifest.json, Obsidian API]
  en: [Obsidian plugin, obsidian plugin, plugin development, manifest.json, Obsidian API]
commands:
  - /obsidian [任务描述]
  - /plugin [任务描述]
---

# Obsidian Plugin Development - 插件开发集成

> 开发高质量 Obsidian 插件的完整指南，包含 27 条关键规则

---

## 核心能力

### 27 条关键规则

完整覆盖 Obsidian 插件开发的各个方面：

| 类别 | 规则数 | 覆盖内容 |
|------|--------|----------|
| **提交与命名** | 5 | Plugin ID/名称/描述 Bot 验证规则 |
| **内存与生命周期** | 2 | 内存泄漏预防、registerEvent() 使用 |
| **类型安全** | 1 | instanceof 替代类型转换 |
| **UI/UX** | 5 | 句子大小写、命令命名、设置界面 |
| **API 最佳实践** | 6 | Editor/Vault API、路径处理、网络请求 |
| **样式** | 2 | CSS 变量、样式作用域 |
| **可访问性** | 3 | 键盘导航、ARIA 标签、焦点指示器 |
| **安全与兼容性** | 2 | XSS 防护、iOS 兼容性 |
| **代码质量** | 1 | 移除示例代码 |

---

## 触发词

### 中文
- Obsidian插件、obsidian插件
- 插件开发
- manifest.json
- Obsidian API

### English
- Obsidian plugin, obsidian plugin
- plugin development
- manifest.json
- Obsidian API

---

## 命令前缀

```
/obsidian [你的任务描述]
/plugin [你的任务描述]
```

---

## 使用示例

### 示例1：创建新插件

```
用户：帮我创建一个 Obsidian 插件来管理任务

激活：obsidian-plugin-dev
响应：
1. 使用交互式脚手架生成器
2. 验证插件元数据（实时 Bot 规则检查）
3. 生成完整的 TypeScript 项目结构
4. 配置 esbuild、TypeScript、ESLint
5. 遵循所有最佳实践
```

### 示例2：验证插件

```
用户：检查我的插件是否符合提交要求

激活：obsidian-plugin-dev
响应：
1. 运行 27 条规则验证
2. 检查 manifest.json 元数据
3. 分析代码质量和内存泄漏
4. 验证可访问性要求
5. 生成详细报告和修复建议
```

---

## 与其他 Skill 协作

### 与 skill-creator-meta 配合

```yaml
场景：创建 Obsidian 插件项目
obsidian-plugin-dev:
  - 插件特定的 27 条规则
  - Obsidian API 最佳实践
skill-creator-meta:
  - 通用项目结构
  - Skill 开发模式
结果：插件项目 + Skill 文档
```

### 与 code-refactoring-expert 配合

```yaml
场景：重构插件代码
obsidian-plugin-dev:
  - Obsidian 特定的重构规则
  - API 使用模式检查
code-refactoring-expert:
  - 通用重构策略
  - 代码质量改进
结果：符合 Obsidian 标准的重构
```

---

## 核心规则速览

### 提交验证（必须通过 Bot 检查）

| 规则 | 正确 | 错误 |
|------|------|------|
| Plugin ID | `my-awesome-plugin` | `obsidian-plugin`, `myPlugin` |
| Plugin Name | `Todo Manager` | `Obsidian Todo`, `Todo Plugin` |
| Description | `Manage tasks efficiently.` | `This plugin manages tasks.` |

### 内存管理

```typescript
// ✅ 正确 - 自动清理
this.registerView(VIEW_TYPE, (leaf) => new CustomView(leaf));

// ❌ 错误 - 内存泄漏
this.view = new CustomView(leaf);  // 存储引用
```

### API 最佳实践

```typescript
// 编辑操作：Editor API
const editor = activeView.editor;
editor.replaceRange('text', from, to);

// 后台文件修改：Vault.process()
await this.app.vault.process(file, (data) => data.replace('old', 'new'));

// 路径处理：normalizePath()
const safePath = this.app.vault.normalizePath(userPath);

// 网络请求：requestUrl()
const response = await this.app.vault.requestUrl({ url: '...' });
```

---

## ESLint 集成

```bash
npm install --save-dev eslint eslint-plugin-obsidianmd
```

```javascript
import obsidianmd from "eslint-plugin-obsidianmd";

export default [
  ...obsidianmd.configs.recommended,
  {
    rules: {
      "obsidianmd/ui/sentence-case": ["warn", {
        brands: ["Obsidian", "GitHub"],
        acronyms: ["API", "URL", "HTML"],
      }],
    },
  },
];
```

---

## 提交检查清单

### 提交验证（Bot 检查）
- [ ] Plugin ID：无 "obsidian"，不以 "plugin" 结尾
- [ ] Plugin name：无 "Obsidian"，不以 "Plugin" 结尾
- [ ] Description：无 "Obsidian"/"This plugin"
- [ ] Description 以标点结尾
- [ ] manifest.json 与提交匹配

### 代码质量
- [ ] 无内存泄漏
- [ ] 类型安全（instanceof）
- [ ] UI 文本句子大小写
- [ ] 使用首选 API
- [ ] 无 iOS 不兼容功能
- [ ] 移除示例代码
- [ ] 无安全问题

### 可访问性（MANDATORY）
- [ ] 所有交互元素键盘可访问
- [ ] 图标按钮有 ARIA 标签
- [ ] 清晰的焦点指示器
- [ ] 触摸目标至少 44×44px
- [ ] 工具提示正确位置

---

## 参考文档

完整参考文档位于 `/skills/skills/obsidian-plugin-dev/references/`：

| 文件 | 描述 |
|------|------|
| `memory-management.md` | 生命周期与清理模式 |
| `type-safety.md` | 类型缩小与安全 |
| `ui-ux.md` | UI 标准与命令 |
| `file-operations.md` | Vault 与文件 API |
| `css-styling.md` | 主题与样式 |
| `accessibility.md` | 可访问性要求 |
| `code-quality.md` | 最佳实践与安全 |
| `submission.md` | 发布指南 |

---

## 资源

- **Obsidian API 文档**: https://docs.obsidian.md
- **ESLint 插件**: https://github.com/obsidianmd/eslint-plugin
- **插件指南**: https://docs.obsidian.md/Plugins/Releasing/Plugin+guidelines
- **提交仓库**: https://github.com/obsidianmd/obsidian-releases

---

## 详细文档

完整文档位置：`/skills/skills/obsidian-plugin-dev/SKILL.md`
