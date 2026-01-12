# Obsidian Plugin - 内存管理与生命周期

> 预防内存泄漏和正确管理资源的关键模式

---

## 核心原则

**让 Obsidian 处理清理** - 使用注册方法，Obsidian 会在卸载时自动清理。

---

## 注册方法

### registerEvent()

```typescript
// ✅ 正确 - 自动清理
this.registerEvent(
  this.app.workspace.on('file-open', (file) => {
    // 处理文件打开
  })
);

// ✅ 多个事件
this.registerEvent(this.app.metadataCache.on('changed', ...));
this.registerEvent(this.app.vault.on('create', ...));
```

### registerView()

```typescript
// ✅ 正确 - 每次创建新实例
this.registerView(VIEW_TYPE, (leaf) => {
  return new CustomView(leaf);  // 创建并返回
});
```

### addCommand()

```typescript
// ✅ 正确 - Obsidian 自动清理命令
this.addCommand({
  id: 'my-command',
  name: 'My command',
  checkCallback: (checking) => {
    // 命令逻辑
  }
});
```

### registerDomEvent()

```typescript
// ✅ 正确 - DOM 事件自动清理
this.registerDomEvent(documentElement, 'click', (e) => {
  // 处理点击
});
```

### registerInterval()

```typescript
// ✅ 正确 - 定时器自动清理
this.registerInterval(window.setInterval(() => {
  // 定期执行
}, 1000));
```

---

## 常见反模式

### ❌ 存储视图引用

```typescript
// 错误 - 内存泄漏
class MyPlugin extends Plugin {
  view: CustomView;

  async onload() {
    this.registerView(VIEW_TYPE, (leaf) => {
      this.view = new CustomView(leaf);  // 不要存储
      return this.view;
    });
  }
}
```

### ❌ 手动清理

```typescript
// 错误 - 不必要
class MyPlugin extends Plugin {
  eventRef: any;

  async onload() {
    this.eventRef = this.app.workspace.on('file-open', ...);
  }

  onunload() {
    this.app.workspace.offref(this.eventRef);  // 不需要
  }
}
```

---

## 正确模式

```typescript
class MyPlugin extends Plugin {
  async onload() {
    // 所有注册方法自动清理
    this.registerEvent(...);
    this.registerView(...);
    this.addCommand(...);
    this.registerDomEvent(...);
    this.registerInterval(...);
  }

  onunload() {
    // Obsidian 自动处理所有清理
    // 只需处理非标准资源
  }
}
```

---

## 特殊情况

### 非标准资源

```typescript
// 需要手动清理的资源
class MyPlugin extends Plugin {
  private interval: number;
  private externalConnection: any;

  async onload() {
    // 非标准定时器
    this.interval = window.setInterval(...);

    // 外部连接
    this.externalConnection = createConnection();
  }

  onunload() {
    // 清理非标准资源
    clearInterval(this.interval);
    this.externalConnection?.close();
  }
}
```

---

## 检查清单

- [ ] 使用 `registerEvent()` 而非直接 `on()`
- [ ] 使用 `registerView()` 返回新实例
- [ ] 不在插件类中存储视图引用
- [ ] 不使用插件类作为组件
- [ ] 让 Obsidian 处理标准清理
- [ ] 只清理非标准资源
