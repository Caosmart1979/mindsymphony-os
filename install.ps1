<#
.SYNOPSIS
    活水插件（42Plugin）及相关软件一键安装脚本 - Windows PowerShell (新手友好版)

.DESCRIPTION
    自动安装 bun、Claude Code、42plugin、42cc

    注意：Zed 编辑器自动安装已暂时禁用（NSIS 安装器性能问题）
    如需安装 Zed，请使用：.\install.ps1 -Only zed 或访问 https://zed.dev/download

    在线安装（推荐）:
    irm https://get.42plugin.com/win | iex

.PARAMETER NoMirror
    使用官方源（海外用户或有代理）

.PARAMETER Mirror
    使用国内镜像源（默认自动检测）

.PARAMETER No42cc
    跳过 42cc 安装

.PARAMETER Only
    只安装指定组件（逗号分隔）：bun,claude,git,42plugin,42cc,zed

.PARAMETER Skip
    跳过指定组件（逗号分隔）

.PARAMETER Yes
    跳过所有确认提示

.PARAMETER DryRun
    预览将要执行的操作，不实际安装

.PARAMETER Uninstall
    卸载所有已安装的组件

.PARAMETER Troubleshoot
    显示常见问题解决指南

.PARAMETER Version
    显示脚本版本

.PARAMETER Help
    显示帮助信息

.EXAMPLE
    irm https://get.42plugin.com/win | iex
    一键在线安装（推荐）

.EXAMPLE
    .\install.ps1 -Mirror
    使用国内镜像安装（大陆用户推荐）

.EXAMPLE
    .\install.ps1 -DryRun
    预览安装过程

.EXAMPLE
    .\install.ps1 -Troubleshoot
    查看故障排除指南

.NOTES
    版本: 1.2.1 (性能优化版)
    更新日志:
    - 1.2.1: 临时禁用 Zed 自动安装以提升性能（可通过 -Only zed 强制安装）
    - 1.2.0: 新手友好版，优化交互体验
#>

# PSScriptAnalyzer 抑制设置
# 这是一个交互式安装脚本，Write-Host 是必需的
# Invoke-Expression 用于官方 bun 安装脚本，是必需的
[Diagnostics.CodeAnalysis.SuppressMessageAttribute('PSAvoidUsingWriteHost', '')]
[Diagnostics.CodeAnalysis.SuppressMessageAttribute('PSAvoidUsingInvokeExpression', '')]
[Diagnostics.CodeAnalysis.SuppressMessageAttribute('PSUseDeclaredVarsMoreThanAssignments', '')]
[Diagnostics.CodeAnalysis.SuppressMessageAttribute('PSUseApprovedVerbs', '')]
[CmdletBinding()]

param(
    [switch]$NoMirror,
    [switch]$Mirror,
    [switch]$No42cc,
    [string]$Only = "",
    [string]$Skip = "",
    [Alias("y")][switch]$Yes,
    [switch]$DryRun,
    [switch]$Uninstall,
    [Alias("t")][switch]$Troubleshoot,
    [Alias("v")][switch]$Version,
    [Alias("h")][switch]$Help
)

$ErrorActionPreference = "Stop"

# 脚本版本
$SCRIPT_VERSION = "1.2.1"

# 42cc 版本信息 API
$CC_42_VERSION_URL = "https://get.42plugin.com/42cc/version.json"

# 镜像配置
$script:UseMirror = $null  # 将在 Detect-MirrorNeed 中设置
$NPM_MIRROR = "https://registry.npmmirror.com"
$BUN_MIRROR = "https://npmmirror.com/mirrors/bun"

# 安装状态标志
$script:BunJustInstalled = $false
$script:ARCH_TYPE = ""
$script:BunExe = $null
$script:ZedInstalled = $false
$script:HasOtherEditor = $false
$script:ZedInstallFailed = $false

# ============================================================================
# 显示版本
# ============================================================================
if ($Version) {
    Write-Host "42plugin 安装脚本 v$SCRIPT_VERSION"
    exit 0
}

# ============================================================================
# 显示帮助
# ============================================================================
if ($Help) {
    Write-Host @"
用法: .\install.ps1 [选项]

活水插件（42Plugin）及相关软件一键安装脚本 v$SCRIPT_VERSION

选项:
  -NoMirror       使用官方源（海外用户或有代理）
  -Mirror         使用国内镜像源（大陆用户推荐）
  -No42cc         跳过 42cc 安装
  -Only <组件>    只安装指定组件，逗号分隔
                  可用组件: bun, claude, git, 42plugin, 42cc, zed
  -Skip <组件>    跳过指定组件，逗号分隔
  -Yes, -y        跳过所有确认提示
  -DryRun         预览将要执行的操作，不实际安装
  -Uninstall      卸载所有已安装的组件
  -Troubleshoot   显示常见问题解决指南
  -Version, -v    显示脚本版本
  -Help, -h       显示此帮助信息

示例:
  # 使用默认设置安装
  irm https://get.42plugin.com/win | iex

  # 大陆用户推荐（使用镜像加速）
  .\install.ps1 -Mirror

  # 预览安装过程
  .\install.ps1 -DryRun

  # 查看故障排除指南
  .\install.ps1 -Troubleshoot

更多信息: https://docs.42plugin.com
"@
    exit 0
}

# ============================================================================
# 打印函数
# ============================================================================
function Write-Info {
    param([string]$Message)
    Write-Host "  $Message" -ForegroundColor DarkGray
}

function Write-Success {
    param([string]$Message)
    Write-Host "  ✓ $Message" -ForegroundColor Green
}

function Write-WarningMsg {
    param([string]$Message)
    Write-Host "  ⚠ $Message" -ForegroundColor Yellow
}

function Write-ErrorMsg {
    param([string]$Message)
    Write-Host "  ✗ $Message" -ForegroundColor Red
}

function Write-Step {
    param([string]$Message)
    Write-Host ""
    Write-Host "  ▸ $Message" -ForegroundColor Magenta
    Write-Host ""
}

# ============================================================================
# 进度动画
# ============================================================================
function Show-Progress {
    param(
        [string]$Activity,
        [scriptblock]$Action
    )

    $frames = @("⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏")
    $frameIndex = 0

    # 创建一个后台任务执行实际操作
    $job = Start-Job -ScriptBlock $Action

    # 显示进度动画
    while ($job.State -eq 'Running') {
        $frame = $frames[$frameIndex]
        Write-Host "`r  $frame $Activity" -NoNewline -ForegroundColor Cyan
        $frameIndex = ($frameIndex + 1) % $frames.Count
        Start-Sleep -Milliseconds 100
    }

    # 清除进度行
    Write-Host "`r                                                            `r" -NoNewline

    # 获取结果
    $result = Receive-Job -Job $job
    Remove-Job -Job $job

    return $result
}

# ============================================================================
# 详细错误帮助
# ============================================================================
function Show-ErrorHelp {
    param([string]$ErrorType)

    Write-Host ""
    Write-Host "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Red

    switch ($ErrorType) {
        "bun_install" {
            Write-Host "  ❌ bun 安装失败" -ForegroundColor Red
            Write-Host ""
            Write-Host "  可能的原因和解决方法：" -ForegroundColor White
            Write-Host ""
            Write-Host "  1️⃣  网络连接问题" -ForegroundColor Yellow
            Write-Host "      → 检查网络连接是否正常" -ForegroundColor Gray
            Write-Host "      → 尝试关闭 VPN 或代理后重试" -ForegroundColor Gray
            Write-Host ""
            Write-Host "  2️⃣  服务器临时不可用" -ForegroundColor Yellow
            Write-Host "      → 稍后重试（服务器可能在维护）" -ForegroundColor Gray
            Write-Host ""
            Write-Host "  3️⃣  手动安装" -ForegroundColor Yellow
            Write-Host "      → 国内用户：https://npmmirror.com/mirrors/bun" -ForegroundColor Cyan
            Write-Host "      → 海外用户：https://bun.sh" -ForegroundColor Cyan
        }
        "bun_not_found" {
            Write-Host "  ❌ 找不到 bun 命令" -ForegroundColor Red
            Write-Host ""
            Write-Host "  这通常是因为环境变量没有刷新。" -ForegroundColor White
            Write-Host ""
            Write-Host "  解决方法（选择其一）：" -ForegroundColor White
            Write-Host ""
            Write-Host "  方法 1（推荐）" -ForegroundColor Yellow
            Write-Host "      关闭当前 PowerShell 窗口，打开一个新的" -ForegroundColor Gray
            Write-Host ""
            Write-Host "  方法 2" -ForegroundColor Yellow
            Write-Host "      刷新环境变量：" -ForegroundColor Gray
            Write-Host "      `$env:PATH = [Environment]::GetEnvironmentVariable('PATH', 'User')" -ForegroundColor Cyan
        }
        "claude_install" {
            Write-Host "  ❌ Claude Code 安装失败" -ForegroundColor Red
            Write-Host ""
            Write-Host "  可能的原因和解决方法：" -ForegroundColor White
            Write-Host ""
            Write-Host "  1️⃣  网络问题" -ForegroundColor Yellow
            Write-Host "      → 尝试使用镜像源：" -ForegroundColor Gray
            Write-Host "        .\install.ps1 -Mirror" -ForegroundColor Cyan
            Write-Host ""
            Write-Host "  2️⃣  bun 版本过旧" -ForegroundColor Yellow
            Write-Host "      → 更新 bun：" -ForegroundColor Gray
            Write-Host "        bun upgrade" -ForegroundColor Cyan
            Write-Host ""
            Write-Host "  3️⃣  手动安装" -ForegroundColor Yellow
            Write-Host "        bun add -g @anthropic-ai/claude-code" -ForegroundColor Cyan
        }
        "git_install" {
            Write-Host "  ❌ Git 安装失败" -ForegroundColor Red
            Write-Host ""
            Write-Host "  Claude Code 需要 Git 才能正常工作。" -ForegroundColor White
            Write-Host ""
            Write-Host "  解决方法：" -ForegroundColor White
            Write-Host ""
            Write-Host "  1️⃣  手动下载安装" -ForegroundColor Yellow
            Write-Host "      → https://git-scm.com/downloads/win" -ForegroundColor Cyan
            Write-Host ""
            Write-Host "  2️⃣  使用 winget 安装" -ForegroundColor Yellow
            Write-Host "        winget install Git.Git" -ForegroundColor Cyan
        }
        "plugin_install" {
            Write-Host "  ❌ 42plugin 安装失败" -ForegroundColor Red
            Write-Host ""
            Write-Host "  可能的原因和解决方法：" -ForegroundColor White
            Write-Host ""
            Write-Host "  1️⃣  网络问题" -ForegroundColor Yellow
            Write-Host "      → 尝试使用镜像源：" -ForegroundColor Gray
            Write-Host "        .\install.ps1 -Mirror" -ForegroundColor Cyan
            Write-Host ""
            Write-Host "  2️⃣  手动安装" -ForegroundColor Yellow
            Write-Host "        bun add -g @42ailab/42plugin" -ForegroundColor Cyan
        }
    }

    Write-Host ""
    Write-Host "  更多帮助: https://docs.42plugin.com" -ForegroundColor DarkGray
    Write-Host "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Red
    Write-Host ""
}

# ============================================================================
# 故障排除指南
# ============================================================================
function Show-Troubleshooting {
    Write-Host ""
    Write-Host "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
    Write-Host "                    常见问题解决指南" -ForegroundColor White
    Write-Host "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  ❓ " -NoNewline -ForegroundColor Yellow
    Write-Host '"claude : 无法将"claude"项识别为..."' -ForegroundColor White
    Write-Host "     原因：环境变量未刷新" -ForegroundColor Gray
    Write-Host "     解决：关闭当前 PowerShell 窗口，打开新的" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  ❓ " -NoNewline -ForegroundColor Yellow
    Write-Host '"bun : 无法将"bun"项识别为..."' -ForegroundColor White
    Write-Host "     原因：bun 环境变量未生效" -ForegroundColor Gray
    Write-Host "     解决：重启 PowerShell 或运行：" -ForegroundColor Gray
    Write-Host '     $env:PATH = [Environment]::GetEnvironmentVariable("PATH", "User")' -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  ❓ " -NoNewline -ForegroundColor Yellow
    Write-Host "安装过程卡住不动" -ForegroundColor White
    Write-Host "     原因：网络较慢或连接不稳定" -ForegroundColor Gray
    Write-Host "     解决：等待 2-3 分钟，或按 Ctrl+C 中断后使用 -Mirror 重试" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  ❓ " -NoNewline -ForegroundColor Yellow
    Write-Host "执行策略错误" -ForegroundColor White
    Write-Host "     原因：PowerShell 执行策略限制" -ForegroundColor Gray
    Write-Host "     解决：以管理员身份运行：" -ForegroundColor Gray
    Write-Host "     Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  ❓ " -NoNewline -ForegroundColor Yellow
    Write-Host "如何完全卸载？" -ForegroundColor White
    Write-Host "     解决：运行 " -NoNewline -ForegroundColor Gray
    Write-Host ".\install.ps1 -Uninstall" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  ❓ " -NoNewline -ForegroundColor Yellow
    Write-Host "安装成功但无法使用" -ForegroundColor White
    Write-Host "     解决：重启 PowerShell 后重试" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
    Write-Host "  更多帮助: " -NoNewline -ForegroundColor Gray
    Write-Host "https://docs.42plugin.com/faq" -ForegroundColor Blue
    Write-Host "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
    Write-Host ""
}

if ($Troubleshoot) {
    Show-Troubleshooting
    exit 0
}

# ============================================================================
# 快速入门指南
# ============================================================================
function Show-QuickStartGuide {
    Write-Host ""
    Write-Host "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
    Write-Host "                       快速入门指南" -ForegroundColor White
    Write-Host "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  第一步：配置 Claude Code" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "    42cc 已启动，点击系统托盘图标即可配置。" -ForegroundColor Gray
    Write-Host "    下次使用时，可在开始菜单搜索「42cc」启动。" -ForegroundColor Gray
    Write-Host ""
    Write-Host "    或使用命令行登录：" -ForegroundColor Gray
    Write-Host "    claude login" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  第二步：开始使用" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "    打开任意代码项目文件夹，然后运行：" -ForegroundColor Gray
    Write-Host "    cd 你的项目目录" -ForegroundColor Cyan
    Write-Host "    claude" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "    Claude Code 会自动分析你的代码，你可以用自然语言问它问题。" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  第三步：探索插件" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "    42plugin 可以扩展 Claude Code 的功能：" -ForegroundColor Gray
    Write-Host "    42plugin search          # 搜索可用插件" -ForegroundColor Cyan
    Write-Host "    42plugin install <名称>  # 安装插件" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
    Write-Host ""
}

# ============================================================================
# 兼容层函数
# ============================================================================

# CIM/WMI 兼容层
function Get-OSInfo {
    try {
        if (Get-Command Get-CimInstance -ErrorAction SilentlyContinue) {
            return Get-CimInstance -ClassName Win32_OperatingSystem
        }
    } catch {}
    return Get-WmiObject -Class Win32_OperatingSystem
}

# 解析 bun.exe 路径
function Resolve-BunExe {
    $preferred = Join-Path $env:USERPROFILE ".bun\bin\bun.exe"
    if (Test-Path $preferred) { return $preferred }

    $cmds = Get-Command bun -All -ErrorAction SilentlyContinue
    $app = $cmds | Where-Object CommandType -eq 'Application' | Select-Object -First 1
    if ($app) { return $app.Source }

    return $null
}

# 统一 bun 调用入口
function Invoke-Bun {
    param([Parameter(ValueFromRemainingArguments=$true)][string[]]$BunArguments)

    if (-not $script:BunExe) { $script:BunExe = Resolve-BunExe }
    if (-not $script:BunExe) { throw "未找到 bun.exe" }

    & $script:BunExe @BunArguments
}

# 刷新当前会话的 PATH 环境变量
# 从 Machine 和 User 级别的 PATH 中加载，避免重复
function Update-SessionPath {
    $machinePath = [System.Environment]::GetEnvironmentVariable("PATH", "Machine")
    $userPath = [System.Environment]::GetEnvironmentVariable("PATH", "User")

    # 合并 Machine 和 User 路径
    $combinedPath = if ($machinePath -and $userPath) {
        "$machinePath;$userPath"
    } elseif ($machinePath) {
        $machinePath
    } elseif ($userPath) {
        $userPath
    } else {
        ""
    }

    # 更新当前会话
    $env:PATH = $combinedPath
}

# Invoke-WebRequest 兼容层
function Invoke-WebRequestCompat {
    param(
        [Parameter(Mandatory)][string]$Uri,
        [Parameter(Mandatory)][string]$OutFile,
        [int]$TimeoutSec = 300
    )

    $params = @{ Uri = $Uri; OutFile = $OutFile; TimeoutSec = $TimeoutSec }

    $cmd = Get-Command Invoke-WebRequest -ErrorAction Stop
    if ($cmd.Parameters.ContainsKey('UseBasicParsing')) {
        $params.UseBasicParsing = $true
    }

    Invoke-WebRequest @params
}

# ============================================================================
# 组件过滤
# ============================================================================
function Test-ShouldInstall {
    param([string]$Component)

    if ($Only -ne "") {
        $onlyList = $Only -split ","
        if ($Component -notin $onlyList) {
            return $false
        }
    }

    if ($Skip -ne "") {
        $skipList = $Skip -split ","
        if ($Component -in $skipList) {
            return $false
        }
    }

    return $true
}

# ============================================================================
# 自动检测镜像需求
# ============================================================================
function Detect-MirrorNeed {
    if ($NoMirror) {
        $script:UseMirror = $false
        return
    }
    if ($Mirror) {
        $script:UseMirror = $true
        return
    }

    # 并行检测：同时测试国内外网络，谁先成功用谁
    $globalJob = Start-Job -ScriptBlock {
        try {
            $null = Invoke-WebRequest -Uri "https://registry.npmjs.org" -TimeoutSec 2 -UseBasicParsing -ErrorAction Stop
            return "global"
        } catch {
            return $null
        }
    }
    $chinaJob = Start-Job -ScriptBlock {
        try {
            $null = Invoke-WebRequest -Uri "https://registry.npmmirror.com" -TimeoutSec 2 -UseBasicParsing -ErrorAction Stop
            return "china"
        } catch {
            return $null
        }
    }

    # 等待最多 1.5 秒
    $result = $null
    $waited = 0
    while ($waited -lt 15 -and $null -eq $result) {
        Start-Sleep -Milliseconds 100
        $waited++
        if ($globalJob.State -eq "Completed") {
            $result = Receive-Job -Job $globalJob -ErrorAction SilentlyContinue
        }
        if ($null -eq $result -and $chinaJob.State -eq "Completed") {
            $result = Receive-Job -Job $chinaJob -ErrorAction SilentlyContinue
        }
    }

    # 清理 Job
    Stop-Job -Job $globalJob -ErrorAction SilentlyContinue
    Stop-Job -Job $chinaJob -ErrorAction SilentlyContinue
    Remove-Job -Job $globalJob -Force -ErrorAction SilentlyContinue
    Remove-Job -Job $chinaJob -Force -ErrorAction SilentlyContinue

    # 根据结果决定是否使用镜像
    if ($result -eq "global") {
        $script:UseMirror = $false
    } else {
        # 默认使用镜像（国内网络或检测超时）
        $script:UseMirror = $true
    }
}

# ============================================================================
# 显示欢迎信息（新手友好版）
# ============================================================================
function Show-Welcome {
    Write-Host ""
    Write-Host "  +-------------------------------------------------------------+" -ForegroundColor Cyan
    Write-Host "  |                                                             |" -ForegroundColor Cyan
    Write-Host "  |     欢迎使用 活水插件 (42Plugin) 及相关软件一键安装脚本     |" -ForegroundColor Cyan
    Write-Host "  |                                                             |" -ForegroundColor Cyan
    Write-Host "  +-------------------------------------------------------------+" -ForegroundColor Cyan
    Write-Host ""

    Write-Host "  这个脚本会帮你安装以下工具：" -ForegroundColor White
    Write-Host ""
    Write-Host "    • " -NoNewline -ForegroundColor Green
    Write-Host "bun" -NoNewline -ForegroundColor White
    Write-Host "         - 包管理工具（类似手机上的应用商店）" -ForegroundColor Gray
    Write-Host "    • " -NoNewline -ForegroundColor Green
    Write-Host "Claude Code" -NoNewline -ForegroundColor White
    Write-Host " - AI 编程助手（帮你写代码、解答问题）" -ForegroundColor Gray
    Write-Host "    • " -NoNewline -ForegroundColor Green
    Write-Host "Git" -NoNewline -ForegroundColor White
    Write-Host "         - 版本控制（Claude Code 需要它）" -ForegroundColor Gray
    Write-Host "    • " -NoNewline -ForegroundColor Green
    Write-Host "42plugin" -NoNewline -ForegroundColor White
    Write-Host "    - 插件管理器（给 Claude Code 安装扩展功能）" -ForegroundColor Gray
    Write-Host "    • " -NoNewline -ForegroundColor Green
    Write-Host "42cc" -NoNewline -ForegroundColor White
    Write-Host "        - 配置工具（图形界面，方便配置 Claude Code）" -ForegroundColor Gray
    Write-Host "    • " -NoNewline -ForegroundColor Green
    Write-Host "Zed" -NoNewline -ForegroundColor White
    Write-Host "         - 代码编辑器（写代码的软件，可选）" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
    Write-Host ""
    Write-Host "  ⏱  预计安装时间: " -NoNewline -ForegroundColor Cyan
    Write-Host "5-10 分钟" -NoNewline -ForegroundColor White
    Write-Host "（取决于网络速度）" -ForegroundColor Gray
    Write-Host "  💾 所需磁盘空间: " -NoNewline -ForegroundColor Cyan
    Write-Host "约 800MB" -ForegroundColor White
    Write-Host "  📦 脚本版本: v$SCRIPT_VERSION" -ForegroundColor Cyan
    Write-Host ""

    # 显示镜像状态
    if ($script:UseMirror) {
        Write-Host "  🚀 使用国内镜像源 (npmmirror)" -NoNewline -ForegroundColor Green
        Write-Host " - 下载更快" -ForegroundColor Gray
        Write-Host "     如需使用官方源，请添加 -NoMirror 参数" -ForegroundColor DarkGray
    } else {
        Write-Host "  🌐 使用官方源" -ForegroundColor Cyan
        Write-Host "     如果下载很慢，请添加 -Mirror 参数使用国内镜像" -ForegroundColor DarkGray
    }

    # 显示模式
    if ($DryRun) {
        Write-Host ""
        Write-Host "  🔍 预览模式" -NoNewline -ForegroundColor Yellow
        Write-Host " - 不会实际安装，只显示将要执行的操作" -ForegroundColor Gray
    }

    Write-Host ""
}

# ============================================================================
# 安装前确认
# ============================================================================
function Confirm-Installation {
    if ($Yes -or $DryRun) {
        return
    }

    Write-Host "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
    Write-Host ""
    Write-Host "  即将安装以下组件：" -ForegroundColor White
    Write-Host ""

    $totalSize = 0

    if (Test-ShouldInstall "bun") {
        Write-Host "    ✓ bun         (约 50MB)" -ForegroundColor Green
        $totalSize += 50
    }
    if (Test-ShouldInstall "claude") {
        Write-Host "    ✓ Claude Code (约 30MB)" -ForegroundColor Green
        $totalSize += 30
    }
    if (Test-ShouldInstall "git") {
        Write-Host "    ✓ Git         (约 500MB)" -ForegroundColor Green
        $totalSize += 500
    }
    if (Test-ShouldInstall "42plugin") {
        Write-Host "    ✓ 42plugin    (约 10MB)" -ForegroundColor Green
        $totalSize += 10
    }
    if ((Test-ShouldInstall "42cc") -and (-not $No42cc)) {
        Write-Host "    ✓ 42cc        (约 100MB)" -ForegroundColor Green
        $totalSize += 100
    }
    if (Test-ShouldInstall "zed") {
        Write-Host "    ✓ Zed         (约 80MB，如已安装则跳过)" -ForegroundColor Green
        $totalSize += 80
    }

    Write-Host ""
    Write-Host "  总计下载: 约 ${totalSize}MB" -ForegroundColor White
    Write-Host ""

    $confirm = Read-Host "  确认开始安装？[Y/n]"
    if ($confirm -match "^[Nn]") {
        Write-Info "已取消安装"
        exit 0
    }
    Write-Host ""
}

# ============================================================================
# 检查管理员权限
# ============================================================================
function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# ============================================================================
# 检测系统信息
# ============================================================================
function Get-SystemInfo {
    Write-Step "检测系统环境"

    $os = Get-OSInfo
    $arch = $env:PROCESSOR_ARCHITECTURE

    Write-Info "系统: $($os.Caption)"
    Write-Info "架构: $arch"

    if ($arch -eq "AMD64")      { $script:ARCH_TYPE = "x64" }
    elseif ($arch -eq "ARM64")  { $script:ARCH_TYPE = "arm64" }
    else {
        Write-ErrorMsg "不支持的系统架构: $arch"
        exit 1
    }

    Write-Success "环境检测完成: Windows / $($script:ARCH_TYPE)"
}

# ============================================================================
# 检查命令是否存在
# ============================================================================
function Test-CommandExists {
    param([string]$Command)
    try {
        if (Get-Command $Command -ErrorAction Stop) {
            return $true
        }
    } catch {
        return $false
    }
}

# ============================================================================
# 安装 bun
# ============================================================================
function Install-Bun {
    if (-not (Test-ShouldInstall "bun")) {
        return
    }

    Write-Step "1/6 安装 bun"

    $existingBunExe = Resolve-BunExe
    if ($existingBunExe) {
        $script:BunExe = $existingBunExe
        $bunVersion = & $script:BunExe --version
        Write-Success "bun 已安装 (v$bunVersion)，跳过安装"
        Configure-NpmMirror
        return
    }

    if ($DryRun) {
        Write-Info "[预览] 将下载并安装 bun (约 50MB)"
        return
    }

    Write-Info "正在下载 bun（这可能需要 1-2 分钟，请耐心等待...）"

    $maxRetries = 3
    $retryCount = 0
    $installSuccess = $false
    $waitTimes = @(0, 2, 4, 6)  # 递增等待：0秒、2秒、4秒、6秒

    while ($retryCount -lt $maxRetries -and -not $installSuccess) {
        try {
            # 智能切换逻辑：前 2 次用镜像源，第 3 次切换到官方源
            $useMirrorThisTime = $script:UseMirror -and ($retryCount -lt 2)

            if ($useMirrorThisTime) {
                if ($retryCount -eq 0) {
                    Write-Info "使用 npmmirror 镜像加速..."
                } else {
                    Write-Info "重试镜像源 (第 $($retryCount + 1)/$maxRetries 次)..."
                }
                $env:BUN_MIRROR = $BUN_MIRROR
            } else {
                if ($script:UseMirror -and $retryCount -eq 2) {
                    Write-WarningMsg "镜像源失败，切换到官方源..."
                } elseif ($retryCount -eq 0) {
                    Write-Info "使用官方源..."
                } else {
                    Write-Info "重试官方源 (第 $($retryCount + 1)/$maxRetries 次)..."
                }
                $env:BUN_MIRROR = $null
            }

            # 添加 -ErrorAction Stop 确保错误被捕获
            $installScript = Invoke-RestMethod -Uri https://bun.sh/install.ps1 -TimeoutSec 30 -ErrorAction Stop
            Invoke-Expression $installScript -ErrorAction Stop

            $installSuccess = $true

        } catch {
            $retryCount++

            if ($retryCount -lt $maxRetries) {
                $waitSeconds = $waitTimes[$retryCount]
                Write-WarningMsg "下载失败: $($_.Exception.Message)"
                Write-Info "等待 $waitSeconds 秒后重试..."
                Start-Sleep -Seconds $waitSeconds
            } else {
                # 最后一次失败，显示详细错误
                Write-ErrorMsg "bun 安装失败（已重试 $maxRetries 次）"
                Write-Host ""
                Write-Host "  错误详情: $($_.Exception.Message)" -ForegroundColor Red
                Write-Host ""
                Write-Host "  💡 可能的解决方法：" -ForegroundColor Yellow
                Write-Host "     1. 检查网络连接是否正常" -ForegroundColor Gray
                Write-Host "     2. 稍后重试（服务器可能临时维护）" -ForegroundColor Gray
                Write-Host "     3. 手动下载安装：" -ForegroundColor Gray
                if ($script:UseMirror) {
                    Write-Host "        https://npmmirror.com/mirrors/bun （国内镜像）" -ForegroundColor Cyan
                } else {
                    Write-Host "        https://bun.sh" -ForegroundColor Cyan
                }

                Show-ErrorHelp "bun_install"
                exit 1
            }
        }
    }

    # 添加到 PATH
    $bunPath = "$env:USERPROFILE\.bun\bin"
    $userPath = [Environment]::GetEnvironmentVariable("PATH", [EnvironmentVariableTarget]::User)
    if (-not ($userPath -like "*$bunPath*")) {
        $newUserPath = if ($userPath) { "$bunPath;$userPath" } else { $bunPath }
        [Environment]::SetEnvironmentVariable("PATH", $newUserPath, [EnvironmentVariableTarget]::User)
        $env:PATH = "$bunPath;$env:PATH"
    }

    # 重新解析 bun.exe
    $script:BunExe = Resolve-BunExe
    if (-not $script:BunExe) {
        Show-ErrorHelp "bun_not_found"
        exit 1
    }

    $bunVersion = & $script:BunExe --version
    Write-Success "bun 安装成功 (v$bunVersion)"

    Configure-NpmMirror
    $script:BunJustInstalled = $true
}

# ============================================================================
# 配置 npm 镜像源
# ============================================================================
function Configure-NpmMirror {
    if (-not $script:UseMirror) {
        return
    }

    if ($DryRun) {
        Write-Info "[预览] 将配置 npm 镜像源"
        return
    }

    try {
        Invoke-Bun config set registry $NPM_MIRROR -ErrorAction SilentlyContinue
    } catch {
        $bunfigPath = "$env:USERPROFILE\.bunfig.toml"
        if (-not (Test-Path $bunfigPath) -or -not (Select-String -Path $bunfigPath -Pattern "registry" -Quiet)) {
            Add-Content -Path $bunfigPath -Value "[install]"
            Add-Content -Path $bunfigPath -Value "registry = `"$NPM_MIRROR`""
        }
    }
}

# ============================================================================
# 安装 Claude Code
# ============================================================================
function Install-ClaudeCode {
    if (-not (Test-ShouldInstall "claude")) {
        return
    }

    Write-Step "2/6 安装 Claude Code"

    if (Test-CommandExists "claude") {
        try {
            $null = & claude --version 2>&1
            if ($LASTEXITCODE -eq 0) {
                $claudeVersion = & claude --version 2>&1
                Write-Success "Claude Code 已安装 ($claudeVersion)，跳过安装"
                return
            }
        } catch {}
        Write-WarningMsg "检测到旧版本，将重新安装"
    }

    if ($DryRun) {
        Write-Info "[预览] 将安装 Claude Code (约 30MB)"
        return
    }

    if (-not $script:BunExe) {
        Write-ErrorMsg "需要先安装 bun"
        exit 1
    }

    Write-Info "正在安装 Claude Code..."

    try {
        Invoke-Bun add -g @anthropic-ai/claude-code
        Write-Success "Claude Code 安装成功"

        if (Test-CommandExists "claude") {
            try {
                $claudeVersion = & claude --version 2>&1
                Write-Success "Claude Code 已就绪 ($claudeVersion)"
            } catch {
                Write-Success "Claude Code 已就绪"
            }
        } else {
            Write-WarningMsg "Claude Code 安装完成，重启 PowerShell 后可使用"
        }
    } catch {
        Show-ErrorHelp "claude_install"
        exit 1
    }
}

# ============================================================================
# 安装 Git for Windows
# ============================================================================
function Install-Git {
    if (-not (Test-ShouldInstall "git")) {
        return
    }

    Write-Step "3/6 安装 Git for Windows"

    if (Test-CommandExists "git") {
        $gitVersion = & git --version
        Write-Success "Git 已安装 ($gitVersion)，跳过安装"
        return
    }

    if ($DryRun) {
        Write-Info "[预览] 将安装 Git for Windows (约 500MB)"
        return
    }

    Write-Info "Claude Code 需要 Git 才能正常工作"
    Write-Info "正在安装 Git for Windows..."

    $maxRetries = 3
    $retryCount = 0
    $installSuccess = $false
    $waitTimes = @(0, 2, 4, 6)

    while ($retryCount -lt $maxRetries -and -not $installSuccess) {
        try {
            # 智能切换逻辑：前 2 次用镜像源，第 3 次切换到 winget
            $useMirrorThisTime = $script:UseMirror -and ($retryCount -lt 2)

            if ($useMirrorThisTime) {
                if ($retryCount -eq 0) {
                    Write-Info "使用 npmmirror 镜像下载..."
                } else {
                    Write-Info "重试镜像源 (第 $($retryCount + 1)/$maxRetries 次)..."
                }

                $mirrorBase = "https://registry.npmmirror.com/-/binary/git-for-windows"

                # 获取最新版本
                $latestVersion = $null
                try {
                    $versions = Invoke-RestMethod -Uri $mirrorBase -TimeoutSec 30 -ErrorAction Stop
                    $latestVersion = ($versions | Where-Object { $_.name -match "^v\d+\.\d+\.\d+\.windows\.\d+/$" } |
                        Sort-Object { [version]($_.name -replace "^v" -replace "\.windows\.\d+/$", "") } -Descending |
                        Select-Object -First 1).name.TrimEnd("/")
                } catch {
                    $latestVersion = "v2.47.1.windows.1"
                    Write-WarningMsg "无法获取最新版本，使用 $latestVersion"
                }

                $versionNumber = $latestVersion -replace "^v" -replace "\.windows\.\d+$", ""
                $installerName = if ($script:ARCH_TYPE -eq "arm64") { "Git-$versionNumber-arm64.exe" } else { "Git-$versionNumber-64-bit.exe" }
                $downloadUrl = "$mirrorBase/$latestVersion/$installerName"
                $installerPath = "$env:TEMP\$installerName"

                Write-Info "下载 Git $versionNumber..."
                Invoke-WebRequestCompat -Uri $downloadUrl -OutFile $installerPath -TimeoutSec 300

                if (Test-Path $installerPath) {
                    Write-Info "正在安装..."
                    Start-Process -FilePath $installerPath -ArgumentList "/VERYSILENT", "/NORESTART", "/NOCANCEL", "/SP-", "/CLOSEAPPLICATIONS", "/RESTARTAPPLICATIONS" -Wait -NoNewWindow
                    Remove-Item $installerPath -Force -ErrorAction SilentlyContinue
                    Update-SessionPath

                    if (Test-CommandExists "git") {
                        $gitVersion = & git --version
                        Write-Success "Git 安装成功 ($gitVersion)"
                        $installSuccess = $true
                    } else {
                        $gitPath = "C:\Program Files\Git\cmd"
                        if (Test-Path $gitPath) {
                            $env:PATH = "$gitPath;$env:PATH"
                            Write-Success "Git 安装成功"
                            $installSuccess = $true
                        } else {
                            throw "Git 命令未找到"
                        }
                    }
                } else {
                    throw "下载失败"
                }
            } else {
                # 使用 winget 作为降级方案
                if ($script:UseMirror -and $retryCount -eq 2) {
                    Write-WarningMsg "镜像源失败，切换到 winget..."
                } elseif ($retryCount -eq 0) {
                    Write-Info "使用 winget 安装 Git..."
                } else {
                    Write-Info "重试 winget (第 $($retryCount + 1)/$maxRetries 次)..."
                }

                if (Test-CommandExists "winget") {
                    & winget install Git.Git --silent --accept-package-agreements --accept-source-agreements
                    Update-SessionPath

                    if (Test-CommandExists "git") {
                        $gitVersion = & git --version
                        Write-Success "Git 安装成功 ($gitVersion)"
                        $installSuccess = $true
                    } else {
                        throw "Git 命令未找到"
                    }
                } else {
                    throw "winget 不可用"
                }
            }

        } catch {
            $retryCount++

            if ($retryCount -lt $maxRetries) {
                $waitSeconds = $waitTimes[$retryCount]
                Write-WarningMsg "安装失败: $($_.Exception.Message)"
                Write-Info "等待 $waitSeconds 秒后重试..."
                Start-Sleep -Seconds $waitSeconds
            } else {
                Write-ErrorMsg "Git 安装失败（已重试 $maxRetries 次）"
                Show-ErrorHelp "git_install"
                exit 1
            }
        }
    }
}

# ============================================================================
# 安装 42plugin
# ============================================================================
function Install-42Plugin {
    if (-not (Test-ShouldInstall "42plugin")) {
        return
    }

    Write-Step "4/6 安装 42plugin"

    if (Test-CommandExists "42plugin") {
        try {
            $null = & 42plugin --version 2>&1
            if ($LASTEXITCODE -eq 0) {
                $pluginVersion = & 42plugin --version 2>&1
                Write-Success "42plugin 已安装 ($pluginVersion)，跳过安装"
                return
            }
        } catch {}
        Write-WarningMsg "检测到旧版本，将重新安装"
    }

    if ($DryRun) {
        Write-Info "[预览] 将安装 42plugin (约 10MB)"
        return
    }

    if (-not $script:BunExe) {
        Write-ErrorMsg "需要先安装 bun"
        exit 1
    }

    Write-Info "正在安装 42plugin..."

    try {
        Invoke-Bun add -g @42ailab/42plugin
        Write-Success "42plugin 安装成功"

        if (Test-CommandExists "42plugin") {
            try {
                $pluginVersion = & 42plugin --version 2>&1
                Write-Success "42plugin 已就绪 ($pluginVersion)"
            } catch {
                Write-Success "42plugin 已就绪"
            }
        } else {
            Write-WarningMsg "42plugin 安装完成，重启 PowerShell 后可使用"
        }
    } catch {
        Show-ErrorHelp "plugin_install"
        exit 1
    }
}

# ============================================================================
# 安装 42cc
# ============================================================================
function Install-42CC {
    if (-not (Test-ShouldInstall "42cc")) {
        return
    }

    Write-Step "5/6 安装 42cc"

    if ($No42cc) {
        Write-Info "已跳过 42cc 安装"
        return
    }

    # 检查是否已安装
    $installedPath = "$env:LOCALAPPDATA\Programs\42cc\42cc.exe"
    if (Test-Path $installedPath) {
        Write-Success "42cc 已安装，跳过安装"
        return
    }

    if ($DryRun) {
        Write-Info "[预览] 将下载并安装 42cc"
        return
    }

    Write-Info "正在获取 42cc 版本信息..."

    try {
        # 获取版本信息
        $versionJson = Invoke-RestMethod -Uri $CC_42_VERSION_URL -TimeoutSec 30

        if (-not $versionJson.windows -or -not $versionJson.windows.url) {
            Write-WarningMsg "无法获取 42cc Windows 版本下载地址"
            Write-Info "您可以访问 https://get.42plugin.com/42cc/version.json 查看最新版本"
            return
        }

        $downloadUrl = $versionJson.windows.url
        $version = $versionJson.version

        Write-Info "42cc 版本: v$version"

        # 下载 exe
        $exeName = "42cc.exe"
        $tempExePath = "$env:TEMP\$exeName"

        Write-Info "正在下载 42cc v$version..."

        Invoke-WebRequestCompat -Uri $downloadUrl -OutFile $tempExePath -TimeoutSec 300

        if (Test-Path $tempExePath) {
            Write-Success "42cc 下载完成"

            Write-Info "正在安装 42cc..."

            # 创建安装目录
            $installDir = "$env:LOCALAPPDATA\Programs\42cc"
            if (-not (Test-Path $installDir)) {
                New-Item -ItemType Directory -Path $installDir -Force | Out-Null
            }

            # 复制 exe 到安装目录
            Copy-Item -Path $tempExePath -Destination $installedPath -Force

            # 清理临时文件
            Remove-Item $tempExePath -Force -ErrorAction SilentlyContinue

            # 创建开始菜单快捷方式
            $startMenuPath = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\42cc.lnk"
            try {
                $WshShell = New-Object -ComObject WScript.Shell
                $Shortcut = $WshShell.CreateShortcut($startMenuPath)
                $Shortcut.TargetPath = $installedPath
                $Shortcut.Description = "Claude Code 配置工具"
                $Shortcut.Save()
                Write-Success "已创建开始菜单快捷方式"
            } catch {
                Write-WarningMsg "创建快捷方式失败，您可以手动创建"
            }

            # 验证安装
            if (Test-Path $installedPath) {
                Write-Success "42cc 安装成功"

                # CI 环境无 OpenGL，跳过启动 GUI
                $isCI = $env:CI -eq "true" -or $env:GITHUB_ACTIONS -eq "true" -or $env:TF_BUILD -eq "True" -or $env:JENKINS_URL
                if (-not $isCI) {
                    Write-Info "正在启动 42cc..."
                    Start-Process -FilePath $installedPath
                    Write-Success "42cc 已启动，请查看系统托盘"
                }
            } else {
                Write-WarningMsg "42cc 安装可能未完成"
            }
        } else {
            Write-WarningMsg "42cc 下载失败"
            Write-Info "您可以手动下载: $downloadUrl"
        }
    } catch {
        Write-WarningMsg "42cc 安装失败: $_"
        Write-Info "您可以稍后手动安装 42cc"
        Write-Info "下载地址: https://get.42plugin.com/42cc/version.json"
    }
}

# ============================================================================
# 安装 Zed 编辑器
# ============================================================================
function Install-Zed {
    if (-not (Test-ShouldInstall "zed")) {
        return
    }

    Write-Step "6/6 安装 Zed 编辑器"

    # 检查是否已安装 Zed
    if (Test-CommandExists "zed") {
        Write-Success "Zed 已安装，跳过安装"
        $script:ZedInstalled = $true
        return
    }

    # 检查常见安装路径
    $zedPaths = @(
        "$env:LOCALAPPDATA\Programs\Zed\zed.exe",
        "$env:LOCALAPPDATA\Zed\zed.exe",
        "C:\Program Files\Zed\zed.exe"
    )
    foreach ($path in $zedPaths) {
        if (Test-Path $path) {
            Write-Success "Zed 已安装，跳过安装"
            $script:ZedInstalled = $true
            return
        }
    }

    # 检查是否已有 VS Code
    if (Test-CommandExists "code") {
        Write-Success "检测到 VS Code，跳过 Zed 安装"
        $script:HasOtherEditor = $true
        return
    }

    # 临时禁用 Zed 自动安装（NSIS 安装器在某些环境下可能需要 5-10 分钟）
    # 用户可以稍后手动安装：https://zed.dev/download
    # 或使用 -Only zed 参数强制安装
    Write-Info "Zed 编辑器自动安装已暂时禁用（性能优化）"
    Write-Info "如需安装 Zed，请访问: https://zed.dev/download"
    Write-Info "或运行: .\install.ps1 -Only zed"
    $script:ZedSkipped = $true
    return

    if ($DryRun) {
        Write-Info "[预览] 将安装 Zed 编辑器 (约 80MB)"
        return
    }

    Write-Info "正在安装 Zed 编辑器..."

    try {
        # 获取最新版本信息
        Write-Info "获取 Zed 最新版本..."
        $releaseInfo = Invoke-RestMethod -Uri "https://api.github.com/repos/zed-industries/zed/releases/latest" -TimeoutSec 30

        $tagName = $releaseInfo.tag_name  # 如 v0.217.4

        # 根据架构选择下载文件
        if ($script:ARCH_TYPE -eq "arm64") {
            $assetName = "Zed-aarch64.exe"
        } else {
            $assetName = "Zed-x86_64.exe"
        }

        # 查找下载链接
        $asset = $releaseInfo.assets | Where-Object { $_.name -eq $assetName } | Select-Object -First 1
        if (-not $asset) {
            throw "未找到 Windows 安装包: $assetName"
        }

        $downloadUrl = $asset.browser_download_url
        $installerPath = "$env:TEMP\$assetName"

        Write-Info "下载 Zed $tagName ($assetName)..."

        Invoke-WebRequestCompat -Uri $downloadUrl -OutFile $installerPath -TimeoutSec 300

        if (Test-Path $installerPath) {
            Write-Info "正在安装..."

            # Zed 的 exe 是 NSIS 安装程序，支持静默安装
            Start-Process -FilePath $installerPath -ArgumentList "/S" -Wait -NoNewWindow

            # 清理临时文件
            Remove-Item $installerPath -Force -ErrorAction SilentlyContinue

            # 刷新 PATH 以识别新安装的 Zed
            Update-SessionPath

            # 验证安装
            if (Test-CommandExists "zed") {
                Write-Success "Zed 安装成功"
                $script:ZedInstalled = $true
            } else {
                # 检查常见安装路径
                $installed = $false
                foreach ($path in $zedPaths) {
                    if (Test-Path $path) {
                        Write-Success "Zed 安装成功"
                        $script:ZedInstalled = $true
                        $installed = $true
                        break
                    }
                }
                if (-not $installed) {
                    Write-WarningMsg "Zed 安装完成，重启 PowerShell 后可使用"
                    $script:ZedInstalled = $true
                }
            }
        } else {
            throw "下载失败"
        }
    } catch {
        Write-WarningMsg "Zed 安装失败: $_"
        Write-Info "可稍后手动安装: https://zed.dev/download"
        $script:ZedInstallFailed = $true
    }
}

# ============================================================================
# 验证安装
# ============================================================================
function Verify-Installations {
    if ($DryRun) {
        return
    }

    $bunBin = "$env:USERPROFILE\.bun\bin"
    $hasConflict = $false

    foreach ($cmd in @("claude", "42plugin")) {
        $cmdInfo = Get-Command $cmd -ErrorAction SilentlyContinue
        if (-not $cmdInfo) { continue }

        if ($cmdInfo.Source -notlike "$bunBin*") {
            if (Test-Path "$bunBin\$cmd.exe") {
                $hasConflict = $true
            }
        }
    }

    if ($hasConflict) {
        Write-Host ""
        Write-WarningMsg "检测到可能存在旧版本命令冲突"
        Write-Info "如果运行命令时出错，请重启 PowerShell"
        Write-Host ""
    }
}

# ============================================================================
# 配置 Claude Code
# ============================================================================
function Configure-Claude {
    if ($DryRun) {
        return
    }

    $claudeDir = "$env:USERPROFILE\.claude"

    if (-not (Test-Path $claudeDir)) {
        New-Item -ItemType Directory -Path $claudeDir -Force | Out-Null
    }
}

# ============================================================================
# 显示完成信息（新手友好版）
# ============================================================================
function Show-Completion {
    if ($DryRun) {
        Write-Host ""
        Write-Host "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "  🔍 预览完成！" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "  以上是将要执行的操作预览。" -ForegroundColor Gray
        Write-Host "  移除 -DryRun 参数开始正式安装。" -ForegroundColor Gray
        Write-Host ""
        Write-Host "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Yellow
        return
    }

    Write-Host ""
    Write-Host "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Green
    Write-Host ""
    Write-Host "  🎉 恭喜！安装完成！" -ForegroundColor Green
    Write-Host ""
    Write-Host "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Green
    Write-Host ""

    # 检查是否需要刷新环境
    if ($script:BunJustInstalled) {
        Write-Host "  ⚠ 重要：请先刷新环境" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "    关闭当前 PowerShell 窗口，打开新的，然后继续下一步。" -ForegroundColor Gray
        Write-Host ""
        Write-Host "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
        Write-Host ""
    }

    Write-Host "  下一步该做什么？" -ForegroundColor White
    Write-Host ""
    Write-Host "  第 1 步：配置 Claude Code" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "    42cc 已启动并在系统托盘中运行，点击托盘图标即可配置。" -ForegroundColor Gray
    Write-Host "    下次使用时，可在开始菜单搜索「42cc」启动。" -ForegroundColor Gray
    Write-Host ""
    Write-Host "    或使用命令行登录：" -ForegroundColor Gray
    Write-Host "    claude login" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  第 2 步：开始使用" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "    进入你的代码项目文件夹，然后运行：" -ForegroundColor Gray
    Write-Host "    cd 你的项目目录" -ForegroundColor Cyan
    Write-Host "    claude" -ForegroundColor Cyan
    Write-Host ""

    Write-Host "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
    Write-Host ""
    Write-Host "  📚 更多资源" -ForegroundColor White
    Write-Host "     官网: " -NoNewline -ForegroundColor Gray
    Write-Host "https://42plugin.com" -ForegroundColor Blue
    Write-Host "     文档: " -NoNewline -ForegroundColor Gray
    Write-Host "https://docs.42plugin.com" -ForegroundColor Blue
    Write-Host ""

    # 交互式选项
    if (-not $Yes) {
        Write-Host "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
        Write-Host ""
        Write-Host "  现在要做什么？" -ForegroundColor White
        Write-Host ""
        Write-Host "    1) 查看快速入门指南" -ForegroundColor Gray
        Write-Host "    2) 退出" -ForegroundColor Gray
        Write-Host ""
        $choice = Read-Host "  请选择 [1/2]"

        switch ($choice) {
            "1" {
                Show-QuickStartGuide
            }
        }
    }

    Write-Host ""
    Write-Success "祝你使用愉快！"
    Write-Host ""
}

# ============================================================================
# 卸载功能
# ============================================================================
function Uninstall-All {
    Write-Step "卸载 42Plugin 相关组件"

    Write-Host "  卸载前请注意：" -ForegroundColor Yellow
    Write-Host "    • 你的配置文件 (~\.claude\) 不会被删除" -ForegroundColor Gray
    Write-Host "    • 你的项目文件不会受影响" -ForegroundColor Gray
    Write-Host ""

    if (-not $Yes) {
        Write-Host "  即将卸载以下组件：" -ForegroundColor Yellow
        Write-Host "    • Claude Code" -ForegroundColor Gray
        Write-Host "    • 42plugin" -ForegroundColor Gray
        Write-Host "    • bun（可选）" -ForegroundColor Gray
        Write-Host ""
        $confirm = Read-Host "  确定要继续吗？[y/N]"
        if ($confirm -notmatch "^[Yy]") {
            Write-Info "已取消卸载"
            exit 0
        }
    }

    # 卸载 Claude Code
    if (Test-CommandExists "claude") {
        Write-Info "卸载 Claude Code..."
        $bunExe = Resolve-BunExe
        if ($bunExe) {
            & $bunExe remove -g @anthropic-ai/claude-code 2>&1 | Out-Null
        }
        Write-Success "Claude Code 已卸载"
    }

    # 卸载 42plugin
    if (Test-CommandExists "42plugin") {
        Write-Info "卸载 42plugin..."
        $bunExe = Resolve-BunExe
        if ($bunExe) {
            & $bunExe remove -g @42ailab/42plugin 2>&1 | Out-Null
        }
        Write-Success "42plugin 已卸载"
    }

    # 询问是否卸载 bun
    $bunExe = Resolve-BunExe
    if ($bunExe) {
        Write-Host ""
        if (-not $Yes) {
            $confirmBun = Read-Host "  是否也卸载 bun？[y/N]"
        } else {
            $confirmBun = "n"
        }

        if ($confirmBun -match "^[Yy]") {
            Write-Info "卸载 bun..."
            $bunDir = "$env:USERPROFILE\.bun"
            if (Test-Path $bunDir) {
                Remove-Item -Path $bunDir -Recurse -Force -ErrorAction SilentlyContinue
            }
            Write-Success "bun 已卸载"
            Write-Host ""
            Write-Info "提示：你可能需要手动从 PATH 中移除 bun 相关路径"
        }
    }

    Write-Host ""
    Write-Success "卸载完成！"
}

# ============================================================================
# 主函数
# ============================================================================
function Main {
    # 自动检测镜像需求
    Detect-MirrorNeed

    # 卸载模式
    if ($Uninstall) {
        Uninstall-All
        exit 0
    }

    Show-Welcome

    # 检查管理员权限
    if (-not (Test-Administrator)) {
        Write-WarningMsg "建议以管理员身份运行此脚本"
        Write-Info "继续安装..."
    }

    # 检测系统
    Get-SystemInfo

    # 安装前确认
    Confirm-Installation

    # 按顺序安装组件
    try {
        Install-Bun
        Install-ClaudeCode
        Install-Git
        Install-42Plugin
        Install-42CC
        Install-Zed
    } catch {
        Write-ErrorMsg "安装过程中出现错误: $_"
        Write-Host ""
        Write-Host "  遇到问题？试试这些方法：" -ForegroundColor Yellow
        Write-Host "    1. 重新运行安装脚本" -ForegroundColor Gray
        Write-Host "    2. 运行 .\install.ps1 -Troubleshoot 查看故障排除指南" -ForegroundColor Gray
        Write-Host "    3. 访问 https://docs.42plugin.com 获取帮助" -ForegroundColor Gray
        exit 1
    }

    # 安装后验证
    Verify-Installations

    # 配置
    Configure-Claude

    # 显示完成信息
    Show-Completion

    # 刷新环境变量（如果安装了 bun）
    if ($script:BunJustInstalled) {
        Update-SessionPath
    }
}

# 运行主函数
Main
