# 技能目录符号链接设置脚本
# 需要以管理员权限运行 PowerShell

$ErrorActionPreference = "Stop"

# 定义所有技能目录
$GLOBAL_CLAUDE_SKILLS = "C:\Users\13466\.claude\skills"
$GLOBAL_GEMINI_SKILLS = "C:\Users\13466\.gemini\skills"
$GEMINI_ANTIGRAVITY_SKILLS = "C:\Users\13466\.gemini\antigravity\skills"
$PROJECT_SKILLS_ROOT = "D:\claudecode\.claude\skills"

# 创建统一的技能中心目录
$SKILLS_CENTER = "D:\claudecode\.claude\skills-center"

Write-Host "=== 技能目录符号链接设置 ===" -ForegroundColor Cyan
Write-Host ""

# 检查管理员权限
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "错误: 此脚本需要管理员权限运行！" -ForegroundColor Red
    Write-Host "请右键点击 PowerShell，选择 '以管理员身份运行'" -ForegroundColor Yellow
    exit 1
}

# 创建目录结构
Write-Host "[1/5] 创建目录结构..." -ForegroundColor Yellow

# 确保项目技能目录存在
if (-not (Test-Path $PROJECT_SKILLS_ROOT)) {
    New-Item -ItemType Directory -Path $PROJECT_SKILLS_ROOT -Force | Out-Null
    Write-Host "  ✓ 创建: $PROJECT_SKILLS_ROOT" -ForegroundColor Green
}

# 创建技能中心目录
if (-not (Test-Path $SKILLS_CENTER)) {
    New-Item -ItemType Directory -Path $SKILLS_CENTER -Force | Out-Null
    Write-Host "  ✓ 创建: $SKILLS_CENTER" -ForegroundColor Green
}

# 创建中心目录的子目录
$subdirs = @("claude-global", "gemini-global", "gemini-antigravity", "project-local")
foreach ($subdir in $subdirs) {
    $path = Join-Path $SKILLS_CENTER $subdir
    if (-not (Test-Path $path)) {
        New-Item -ItemType Directory -Path $path -Force | Out-Null
        Write-Host "  ✓ 创建: $path" -ForegroundColor Green
    }
}

Write-Host ""

# 设置符号链接
Write-Host "[2/5] 设置 Claude 全局技能链接..." -ForegroundColor Yellow
$claudeLinkSource = Join-Path $PROJECT_SKILLS_ROOT "claude-global"
if (Test-Path $claudeLinkSource) {
    Remove-Item -Path $claudeLinkSource -Force -Recurse
}
New-Item -ItemType SymbolicLink -Path $claudeLinkSource -Target $GLOBAL_CLAUDE_SKILLS | Out-Null
Write-Host "  ✓ 链接: $claudeLinkSource -> $GLOBAL_CLAUDE_SKILLS" -ForegroundColor Green

Write-Host "[3/5] 设置 Gemini 全局技能链接..." -ForegroundColor Yellow
$geminiLinkSource = Join-Path $PROJECT_SKILLS_ROOT "gemini-global"
if (Test-Path $geminiLinkSource) {
    Remove-Item -Path $geminiLinkSource -Force -Recurse
}
New-Item -ItemType SymbolicLink -Path $geminiLinkSource -Target $GLOBAL_GEMINI_SKILLS | Out-Null
Write-Host "  ✓ 链接: $geminiLinkSource -> $GLOBAL_GEMINI_SKILLS" -ForegroundColor Green

Write-Host "[4/5] 设置 Gemini antigravity 技能链接..." -ForegroundColor Yellow
$antigravityLinkSource = Join-Path $PROJECT_SKILLS_ROOT "gemini-antigravity"
if (Test-Path $antigravityLinkSource) {
    Remove-Item -Path $antigravityLinkSource -Force -Recurse
}
New-Item -ItemType SymbolicLink -Path $antigravityLinkSource -Target $GEMINI_ANTIGRAVITY_SKILLS | Out-Null
Write-Host "  ✓ 链接: $antigravityLinkSource -> $GEMINI_ANTIGRAVITY_SKILLS" -ForegroundColor Green

Write-Host "[5/5] 链接现有项目技能..." -ForegroundColor Yellow
$existingProjectSkills = "D:\claudecode\skills"
if (Test-Path $existingProjectSkills) {
    $projectLinkSource = Join-Path $PROJECT_SKILLS_ROOT "local"
    if (Test-Path $projectLinkSource) {
        Remove-Item -Path $projectLinkSource -Force -Recurse
    }
    New-Item -ItemType SymbolicLink -Path $projectLinkSource -Target $existingProjectSkills | Out-Null
    Write-Host "  ✓ 链接: $projectLinkSource -> $existingProjectSkills" -ForegroundColor Green
}

Write-Host ""
Write-Host "=== 设置完成！===" -ForegroundColor Cyan
Write-Host ""
Write-Host "目录结构：" -ForegroundColor White
Write-Host "  $PROJECT_SKILLS_ROOT\" -ForegroundColor Cyan
Write-Host "    ├── claude-global      -> $GLOBAL_CLAUDE_SKILLS" -ForegroundColor Gray
Write-Host "    ├── gemini-global      -> $GLOBAL_GEMINI_SKILLS" -ForegroundColor Gray
Write-Host "    ├── gemini-antigravity -> $GEMINI_ANTIGRAVITY_SKILLS" -ForegroundColor Gray
Write-Host "    └── local              -> $existingProjectSkills" -ForegroundColor Gray
Write-Host ""
Write-Host "技能中心：" -ForegroundColor White
Write-Host "  $SKILLS_CENTER" -ForegroundColor Cyan
Write-Host ""
Write-Host "现在可以通过 $PROJECT_SKILLS_ROOT 访问所有技能！" -ForegroundColor Green
