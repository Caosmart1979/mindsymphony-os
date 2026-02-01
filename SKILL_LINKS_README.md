# 技能目录符号链接配置

## 目录结构

```
C:\Users\13466\.claude\skills           (Claude 全局技能)
C:\Users\13466\.gemini\skills           (Gemini 全局技能)
C:\Users\13466\.gemini\antigravity\skills (Gemini antigravity 技能)
D:\claudecode\skills                    (项目本地技能)

↓ 统一链接到 ↓

D:\claudecode\.claude\skills\           (统一访问点)
├── claude-global        -> C:\Users\13466\.claude\skills
├── gemini-global        -> C:\Users\13466\.gemini\skills
├── gemini-antigravity   -> C:\Users\13466\.gemini\antigravity\skills
└── local                -> D:\claudecode\skills
```

## 使用方法

### 初始设置（只需执行一次）

1. **双击运行** `setup_skill_links.bat`
   - 会自动请求管理员权限
   - 创建所有符号链接

2. 或 **以管理员身份运行 PowerShell**：
   ```powershell
   .\setup_skill_symlinks.ps1
   ```

### 验证链接状态

**双击运行** `verify_skill_links.bat` 查看所有链接状态。

## 文件说明

| 文件 | 说明 |
|------|------|
| `setup_skill_links.bat` | 一键启动器（推荐） |
| `setup_skill_symlinks.ps1` | PowerShell 设置脚本 |
| `verify_skill_links.bat` | 验证启动器 |
| `verify_skill_links.ps1` | PowerShell 验证脚本 |

## 使用示例

在 Claude Code 或其他工具中引用技能时，使用统一路径：

```
# 访问所有技能
D:\claudecode\.claude\skills\

# 访问特定来源的技能
D:\claudecode\.claude\skills\claude-global\    # Claude 全局技能
D:\claudecode\.claude\skills\gemini-global\    # Gemini 全局技能
D:\claudecode\.claude\skills\gemini-antigravity\  # Gemini antigravity 技能
D:\claudecode\.claude\skills\local\            # 项目本地技能
```

## 实时同步

使用符号链接后，对原始目录的任何修改都会**实时反映**在链接目录中，无需额外同步操作。

## 故障排除

### 链接显示"目标不存在"
- 检查原始源目录是否存在
- 重新运行 `setup_skill_links.bat`

### 权限错误
- 确保以管理员身份运行脚本
- Windows 需要管理员权限创建符号链接

### 删除链接
符号链接可以直接删除，不会影响原始目录：
```powershell
Remove-Item "D:\claudecode\.claude\skills\claude-global"
```
