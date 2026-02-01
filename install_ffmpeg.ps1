# FFmpeg Windows 安装脚本
# 以管理员身份运行 PowerShell

Write-Host "=== FFmpeg 安装脚本 ===" -ForegroundColor Cyan

# 1. 创建安装目录
$ffmpegPath = "C:\ffmpeg"
Write-Host "创建目录: $ffmpegPath" -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path $ffmpegPath | Out-Null

# 2. 下载 FFmpeg 静态构建版本
Write-Host "下载 FFmpeg..." -ForegroundColor Yellow
$zipUrl = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
$zipFile = "$env:TEMP\ffmpeg.zip"

Invoke-WebRequest -Uri $zipUrl -OutFile $zipFile -UseBasicParsing

# 3. 解压文件
Write-Host "解压文件..." -ForegroundColor Yellow
Expand-Archive -Path $zipFile -DestinationPath $ffmpegPath -Force

# 4. 移动文件到根目录
Write-Host "整理文件..." -ForegroundColor Yellow
$extractedPath = Get-ChildItem -Path $ffmpegPath -Directory | Select-Object -First 1
Move-Item -Path "$extractedPath\*" -Destination $ffmpegPath -Force
Remove-Item -Path $extractedPath.FullName -Force

# 5. 添加到系统 PATH
Write-Host "添加到 PATH..." -ForegroundColor Yellow
$binPath = "$ffmpegPath\bin"
$regPath = "HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
$currentPath = [Environment]::GetEnvironmentVariable("Path", "Machine")

if ($currentPath -notlike "*$binPath*") {
    [Environment]::SetEnvironmentVariable("Path", "$currentPath;$binPath", "Machine")
    Write-Host "✅ FFmpeg 已添加到系统 PATH" -ForegroundColor Green
} else {
    Write-Host "ℹ️  FFmpeg 已在 PATH 中" -ForegroundColor Cyan
}

# 6. 清理临时文件
Remove-Item -Path $zipFile -Force

Write-Host ""
Write-Host "=== 安装完成 ===" -ForegroundColor Green
Write-Host "请重新启动终端或运行以下命令刷新 PATH：" -ForegroundColor Yellow
Write-Host '  $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine")' -ForegroundColor White
Write-Host ""
Write-Host "验证安装：ffmpeg -version" -ForegroundColor Cyan
