# 简化的管理员链接脚本
# 右键 - 以管理员身份运行 PowerShell

$ErrorActionPreference = "Stop"

$baseDir = "D:\claudecode\.claude\skills"

Write-Host "=== 创建符号链接 ===" -ForegroundColor Cyan
Write-Host ""

# 创建 gemini-global 链接
Write-Host "[1/2] 创建 gemini-global 链接..." -ForegroundColor Yellow
$linkPath = "$baseDir\gemini-global"
$targetPath = "C:\Users\13466\.gemini\skills"
if (Test-Path $linkPath) { Remove-Item $linkPath -Force -Recurse }
New-Item -ItemType SymbolicLink -Path $linkPath -Target $targetPath -Force | Out-Null
Write-Host "  OK: $linkPath -> $targetPath" -ForegroundColor Green

# 创建 local 链接
Write-Host "[2/2] 创建 local 链接..." -ForegroundColor Yellow
$linkPath = "$baseDir\local"
$targetPath = "D:\claudecode\skills"
if (Test-Path $linkPath) { Remove-Item $linkPath -Force -Recurse }
New-Item -ItemType SymbolicLink -Path $linkPath -Target $targetPath -Force | Out-Null
Write-Host "  OK: $linkPath -> $targetPath" -ForegroundColor Green

Write-Host ""
Write-Host "=== 完成！===" -ForegroundColor Green
Write-Host ""
Get-ChildItem $baseDir -Force | Format-Table Name, LinkType, Target -AutoSize
