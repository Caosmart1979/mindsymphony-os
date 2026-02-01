# 技能目录链接验证脚本
# 用于检查符号链接状态

$ErrorActionPreference = "Stop"

# 定义路径
$PROJECT_SKILLS_ROOT = "D:\claudecode\.claude\skills"
$SKILLS_CENTER = "D:\claudecode\.claude\skills-center"

Write-Host "=== 技能目录链接状态检查 ===" -ForegroundColor Cyan
Write-Host ""

# 检查函数
function Test-Symlink {
    param([string]$Path)

    if (-not (Test-Path $Path)) {
        return @{
            Exists = $false
            IsSymlink = $false
            Target = $null
            Status = "不存在"
        }
    }

    $item = Get-Item $Path -Force
    $isSymlink = $item.LinkType -eq "SymbolicLink"

    if ($isSymlink) {
        $target = $item.Target
        $targetExists = Test-Path $target
        $status = if ($targetExists) { "有效" } else { "目标不存在" }
    } else {
        $target = $null
        $status = "普通目录"
    }

    return @{
        Exists = $true
        IsSymlink = $isSymlink
        Target = $target
        Status = $status
    }
}

# 显示函数
function Show-SymlinkStatus {
    param([string]$Name, [string]$Path)

    $result = Test-Symlink $Path

    $icon = switch ($result.Status) {
        "有效" { "[✓]" }
        "目标不存在" { "[✗]" }
        "普通目录" { "[D]" }
        "不存在" { "[ ]" }
        default { "[?]" }
    }

    $color = switch ($result.Status) {
        "有效" { "Green" }
        "目标不存在" { "Red" }
        "普通目录" { "Yellow" }
        "不存在" { "Gray" }
        default { "White" }
    }

    Write-Host "  $icon $Name" -ForegroundColor $color -NoNewline
    Write-Host " -> " -NoNewline

    if ($result.IsSymlink) {
        Write-Host $result.Target -ForegroundColor Cyan
    } else {
        Write-Host $result.Status -ForegroundColor $color
    }
}

# 检查项目技能目录
Write-Host "项目技能目录 ($PROJECT_SKILLS_ROOT):" -ForegroundColor Yellow
if (Test-Path $PROJECT_SKILLS_ROOT) {
    Show-SymlinkStatus "claude-global" (Join-Path $PROJECT_SKILLS_ROOT "claude-global")
    Show-SymlinkStatus "gemini-global" (Join-Path $PROJECT_SKILLS_ROOT "gemini-global")
    Show-SymlinkStatus "gemini-antigravity" (Join-Path $PROJECT_SKILLS_ROOT "gemini-antigravity")
    Show-SymlinkStatus "local" (Join-Path $PROJECT_SKILLS_ROOT "local")
} else {
    Write-Host "  [ ] 目录不存在" -ForegroundColor Gray
    Write-Host "  请先运行 setup_skill_symlinks.ps1" -ForegroundColor Yellow
}

Write-Host ""

# 检查技能中心
Write-Host "技能中心目录 ($SKILLS_CENTER):" -ForegroundColor Yellow
if (Test-Path $SKILLS_CENTER) {
    $subdirs = @("claude-global", "gemini-global", "gemini-antigravity", "project-local")
    foreach ($subdir in $subdirs) {
        $path = Join-Path $SKILLS_CENTER $subdir
        $status = if (Test-Path $path) { "[✓]" } else { "[ ]" }
        $color = if (Test-Path $path) { "Green" } else { "Gray" }
        Write-Host "  $status $subdir" -ForegroundColor $color
    }
} else {
    Write-Host "  [ ] 目录不存在" -ForegroundColor Gray
}

Write-Host ""

# 检查原始目录
Write-Host "原始源目录:" -ForegroundColor Yellow
$sourceDirs = @{
    "Claude 全局" = "C:\Users\13466\.claude\skills"
    "Gemini 全局" = "C:\Users\13466\.gemini\skills"
    "Gemini antigravity" = "C:\Users\13466\.gemini\antigravity\skills"
    "项目本地" = "D:\claudecode\skills"
}

foreach ($kv in $sourceDirs.GetEnumerator()) {
    $status = if (Test-Path $kv.Value) { "[✓]" } else { "[ ]" }
    $color = if (Test-Path $kv.Value) { "Green" } else { "Red" }
    Write-Host "  $status $($kv.Key)" -ForegroundColor $color
    Write-Host "      $($kv.Value)" -ForegroundColor Gray
}

Write-Host ""
Write-Host "=== 检查完成 ===" -ForegroundColor Cyan
