---
name: obsidian-plugin-dev
version: 1.0.0
category: development
integration: mindsymphony
type: specialist
description: Obsidian 插件开发专家 - 遵循最佳实践的插件开发指南
triggers:
  zh: [Obsidian插件, obsidian插件, 插件开发, manifest.json, Obsidian API]
  en: [Obsidian plugin, obsidian plugin, plugin development, manifest.json, Obsidian API]
commands:
  - /obsidian [任务描述]
  - /plugin [任务描述]
---

# Obsidian Plugin Development - 插件开发专家

> 开发高质量 Obsidian 插件的完整指南，遵循官方最佳实践和提交要求。

---

## 核心能力

### 27 条关键规则

这个 skill 提供了 Obsidian 插件开发的全部 27 条关键规则，覆盖：

| 类别 | 规则数 | 描述 |
|------|--------|------|
| **提交与命名** | 5 | Plugin ID/名称/描述验证规则 |
| **内存与生命周期** | 2 | 内存泄漏预防、资源清理 |
| **类型安全** | 1 | instanceof 替代类型转换 |
| **UI/UX** | 5 | 句子大小写、命令命名、设置界面 |
| **API 最佳实践** | 6 | Editor API、Vault API、路径处理 |
| **样式** | 2 | CSS 变量、样式作用域 |
| **可访问性** | 3 | 键盘导航、ARIA 标签、焦点指示器 |
| **安全与兼容性** | 2 | XSS 防护、iOS 兼容性 |
| **代码质量** | 1 | 移除示例代码 |

---

## 快速开始

### 创建新插件

```bash
# 使用交互式脚手架生成器
node /path/to/obsidian-plugin-dev/tools/create-plugin.js
```

**生成的结构：**
```
your-plugin/
├── src/
│   ├── main.ts           # Plugin 类
│   └── settings.ts       # 设置界面
├── manifest.json         # 插件元数据
├── styles.css           # CSS 样式
├── tsconfig.json        # TypeScript 配置
├── package.json         # 依赖
├── esbuild.config.mjs   # 构建配置
└── versions.json        # 版本追踪
```

---

## 核心规则速览

### 1. 提交验证（必须通过 Bot 检查）

```yaml
Plugin ID:
  规则: 不能包含 "obsidian"，不能以 "plugin" 结尾，仅小写
  正确: my-awesome-plugin
  错误: obsidian-plugin, myPlugin

Plugin Name:
  规则: 不能包含 "Obsidian"，不能以 "Plugin" 结尾
  正确: Todo Manager
  错误: Obsidian Todo, Todo Plugin

Description:
  规则: 不能包含 "Obsidian"/"This plugin"，必须以标点结尾
  正确: Manage your tasks efficiently.
  错误: This plugin manages tasks., An Obsidian task manager
```

### 2. 内存管理

```typescript
// ❌ 错误 - 内存泄漏
class MyPlugin extends Plugin {
  view: CustomView;  // 存储视图引用

  async onload() {
    this.registerView(VIEW_TYPE, (leaf) => {
      this.view = new CustomView(leaf);  // 泄漏！
      return this.view;
    });
  }
}

// ✅ 正确 - 自动清理
class MyPlugin extends Plugin {
  async onload() {
    this.registerView(VIEW_TYPE, (leaf) => {
      return new CustomView(leaf);  // 直接返回
    });
  }

  onunload() {
    // Obsidian 自动处理清理
  }
}
```

### 3. API 最佳实践

```typescript
// 编辑操作：使用 Editor API
const activeView = this.app.workspace.getActiveViewOfType(MarkdownView);
if (activeView) {
  const editor = activeView.editor;
  editor.replaceRange('text', from, to);
}

// 后台文件修改：使用 Vault.process()
await this.app.vault.process(file, (data) => {
  return data.replace('old', 'new');
});

// 路径处理：使用 normalizePath()
const safePath = this.app.vault.normalizePath(userPath);

// 网络请求：使用 requestUrl()
const response = await this.app.vault.requestUrl({
  url: 'https://api.example.com',
});
```

### 4. 可访问性（MANDATORY）

```typescript
// 所有交互元素必须键盘可访问
button.setAttrs({
  'aria-label': 'Save settings',  // 图标按钮需要 ARIA
  'data-tooltip-position': 'top'  // 工具提示位置
});

// CSS 焦点指示器
.my-plugin-button:focus-visible {
  outline: 2px solid var(--interactive-accent);
  outline-offset: 2px;
}
```

---

## 完整规则列表

### 提交与命名（5 条）

1. ✅ Plugin ID：无 "obsidian"，不以 "plugin" 结尾，小写
2. ✅ Plugin name：无 "Obsidian"，不以 "Plugin" 结尾
3. ✅ Plugin name：不以 "Obsi" 开头或 "dian" 结尾
4. ✅ Description：无 "Obsidian"/"This plugin"
5. ✅ Description：必须以 `.?!)` 标点结尾

### 内存与生命周期（2 条）

6. ✅ 使用 `registerEvent()` 自动清理
7. ✅ 不在插件中存储视图引用

### 类型安全（1 条）

8. ✅ 使用 `instanceof` 替代类型转换

### UI/UX（5 条）

9. ✅ 所有 UI 文本使用句子大小写
10. ✅ 命令名称/ID 中无 "command"
11. ✅ 命令 ID 中无 plugin ID
12. ✅ 无默认热键
13. ✅ 设置使用 `.setHeading()`

### API 最佳实践（6 条）

14. ✅ 活跃文件编辑使用 Editor API
15. ✅ 后台文件修改使用 Vault.process()
16. ✅ 用户路径使用 normalizePath()
17. ✅ OS 检测使用 Platform API
18. ✅ 网络请求使用 requestUrl() 而非 fetch()
19. ✅ 生产环境无 console.log

### 样式（2 条）

20. ✅ 使用 Obsidian CSS 变量
21. ✅ CSS 作用域限制到插件容器

### 可访问性（3 条）- MANDATORY

22. ✅ 所有交互元素键盘可访问
23. ✅ 图标按钮提供 ARIA 标签
24. ✅ 定义清晰的焦点指示器

### 安全与兼容性（2 条）

25. ✅ 不使用 innerHTML/outerHTML
26. ✅ 避免 regex lookbehind（iOS 不兼容）

### 代码质量（1 条）

27. ✅ 移除所有示例/模板代码

---

## 参考文档

详细参考文档位于 `references/` 目录：

| 文件 | 描述 |
|------|------|
| `memory-management.md` | 生命周期与清理模式 |
| `type-safety.md` | 类型缩小与安全 |
| `ui-ux.md` | UI 标准与命令 |
| `file-operations.md` | Vault 与文件 API |
| `css-styling.md` | 主题与样式 |
| `accessibility.md` | 可访问性要求（必须） |
| `code-quality.md` | 最佳实践与安全 |
| `submission.md` | 发布指南 |

---

## ESLint 集成

安装官方 ESLint 插件：

```bash
npm install --save-dev eslint eslint-plugin-obsidianmd
```

创建 `eslint.config.js`：

```javascript
import obsidianmd from "eslint-plugin-obsidianmd";

export default [
  ...obsidianmd.configs.recommended,
  {
    rules: {
      "obsidianmd/ui/sentence-case": ["warn", {
        brands: ["Obsidian", "GitHub"],
        acronyms: ["API", "URL", "HTML"],
        enforceCamelCaseLower: true,
      }],
    },
  },
];
```

自动修复：
```bash
eslint . --fix
```

---

## 提交检查清单

使用此清单在提交前检查：

### 提交验证（Bot 检查）
- [ ] Plugin ID：无 "obsidian"，不以 "plugin" 结尾，小写
- [ ] Plugin name：无 "Obsidian"，不以 "Plugin" 结尾
- [ ] Plugin name：不以 "Obsi" 开头或 "dian" 结尾
- [ ] Description：无 "Obsidian"/"This plugin"
- [ ] Description 以标点结尾（. ? ! 或 )）
- [ ] Description < 250 字符
- [ ] manifest.json 与提交条目匹配

### 代码质量
- [ ] 无内存泄漏（视图/组件正确管理）
- [ ] 类型安全（使用 instanceof）
- [ ] 所有 UI 文本句子大小写
- [ ] 命令名称中无冗余词
- [ ] 使用首选 API（Editor API、Vault.process 等）
- [ ] 无 iOS 不兼容功能（regex lookbehind）
- [ ] 所有示例代码已移除
- [ ] 无安全问题（innerHTML、XSS）

### 可访问性（MANDATORY）
- [ ] 所有交互元素键盘可访问（Tab、Enter、Space）
- [ ] 所有图标按钮有 ARIA 标签
- [ ] 清晰的焦点指示器（:focus-visible CSS）
- [ ] 触摸目标至少 44×44px（移动端）
- [ ] 工具提示使用 data-tooltip-position

### 发布要求
- [ ] manifest.json 有效且版本正确
- [ ] 包含 LICENSE 文件
- [ ] 已测试移动端（如非仅桌面）
- [ ] 仓库启用了 issues

---

## 资源

- **Obsidian API 文档**: https://docs.obsidian.md
- **ESLint 插件**: https://github.com/obsidianmd/eslint-plugin
- **示例插件**: https://github.com/obsidianmd/obsidian-sample-plugin
- **插件指南**: https://docs.obsidian.md/Plugins/Releasing/Plugin+guidelines
- **提交仓库**: https://github.com/obsidianmd/obsidian-releases

---

## 设计哲学

本 skill 遵循 **Anthropic 的 agent skills 最佳实践**：

- **渐进式披露**: 主 SKILL.md 提供概述；参考文件包含详细信息
- **上下文窗口效率**: "上下文窗口是公共资源" - 优化 token 使用
- **一级引用**: 所有参考文件直接在 reference/ 下（无嵌套）
- **基于主题的组织**: 每个参考文件专注于特定领域
- **一致的术语**: 全文使用相同术语以保持清晰

---

**版本:** 1.0.0
**许可:** MIT
**作者**: MindSymphony 团队（基于 gapmiss/obsidian-plugin-skill）
