# MindSymphony 完整备份脚本
# 备份到本地和 GitHub

param(
    [string]$BackupDir = ".\backups",
    [string]$GitMessage = "Backup MindSymphony v21.2 with Lightning Layer"
)

Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  MindSymphony 完整备份工具 v21.2" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan

# 创建备份目录
$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$BackupPath = Join-Path $BackupDir $Timestamp
New-Item -ItemType Directory -Force -Path $BackupPath | Out-Null

Write-Host "`n📁 备份目录: $BackupPath" -ForegroundColor Green

# 1. 备份 MindSymphony Lightning Layer (从 ~/.claude/skills/)
Write-Host "`n📦 步骤 1: 备份 MindSymphony Lightning Layer..." -ForegroundColor Yellow
$LightningSource = "$env:USERPROFILE\.claude\skills\mindsymphony\lightning"
$LightningDest = Join-Path $BackupPath "lightning"
if (Test-Path $LightningSource) {
    Copy-Item -Path $LightningSource -Destination $LightningDest -Recurse -Force
    Write-Host "   ✓ Lightning Layer 已备份" -ForegroundColor Green
} else {
    Write-Host "   ⚠ Lightning Layer 源目录不存在" -ForegroundColor Yellow
}

# 2. 备份 MindSymphony 核心
Write-Host "`n📦 步骤 2: 备份 MindSymphony 核心文件..." -ForegroundColor Yellow
$CoreFiles = @(
    "SKILL.md",
    "mindsymphony-v21.1.config.yml",
    "mindsymphony-v21.2.config.yml",
    "VERSION.yml",
    "INTEROP.yml",
    "router",
    "core",
    "extensions",
    "integrations",
    "registry"
)
$CoreDest = Join-Path $BackupPath "mindsymphony-core"
New-Item -ItemType Directory -Force -Path $CoreDest | Out-Null

foreach ($file in $CoreFiles) {
    $Source = "$env:USERPROFILE\.claude\skills\mindsymphony\$file"
    if (Test-Path $Source) {
        Copy-Item -Path $Source -Destination $CoreDest -Recurse -Force
        Write-Host "   ✓ $file" -ForegroundColor Green
    }
}

# 3. 备份外部技能索引
Write-Host "`n📦 步骤 3: 备份外部技能索引..." -ForegroundColor Yellow
$ExternalIndex = "$env:USERPROFILE\.claude\skills\mindsymphony\registry\external-skills-index.yml"
if (Test-Path $ExternalIndex) {
    Copy-Item -Path $ExternalIndex -Destination $BackupPath -Force
    Write-Host "   ✓ 外部技能索引已备份" -ForegroundColor Green
}

# 4. 备份 Lightning Store 数据库 (如果存在)
Write-Host "`n📦 步骤 4: 备份 Lightning Store 数据库..." -ForegroundColor Yellow
$StoreDB = "$env:USERPROFILE\.claude\mindsymphony-v21\lightning\store.db"
if (Test-Path $StoreDB) {
    $DBBackup = Join-Path $BackupPath "database"
    New-Item -ItemType Directory -Force -Path $DBBackup | Out-Null
    Copy-Item -Path $StoreDB -Destination $DBBackup -Force
    Write-Host "   ✓ Store 数据库已备份 ($(Get-Item $StoreDB).Length bytes)" -ForegroundColor Green
} else {
    Write-Host "   ℹ Store 数据库尚未创建" -ForegroundColor Gray
}

# 5. 备份项目文档
Write-Host "`n📦 步骤 5: 备份项目文档..." -ForegroundColor Yellow
$Docs = @(
    "docs\plans\mindsymphony-v21.2-lightning-upgrade.md",
    "docs\plans\lightning-v21.2-implementation-summary.md"
)
foreach ($doc in $Docs) {
    if (Test-Path $doc) {
        Copy-Item -Path $doc -Destination $BackupPath -Force
        Write-Host "   ✓ $doc" -ForegroundColor Green
    }
}

# 6. 备份 Vercel Skills
Write-Host "`n📦 步骤 6: 备份 Vercel Skills..." -ForegroundColor Yellow
$VercelSkills = ".\.agents\skills"
if (Test-Path $VercelSkills) {
    Copy-Item -Path $VercelSkills -Destination (Join-Path $BackupPath "vercel-skills") -Recurse -Force
    $SkillCount = (Get-ChildItem $VercelSkills -Directory).Count
    Write-Host "   ✓ $SkillCount 个 Vercel Skills 已备份" -ForegroundColor Green
}

# 7. 创建备份清单
Write-Host "`n📝 步骤 7: 创建备份清单..." -ForegroundColor Yellow
$Manifest = @{
    "backup_time" = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "version" = "v21.2.0-lightning"
    "components" = @{
        "lightning_layer" = $true
        "mindsymphony_core" = $true
        "external_skills_index" = $true
        "vercel_skills" = $true
        "database" = (Test-Path $StoreDB)
    }
    "files" = (Get-ChildItem $BackupPath -Recurse | Measure-Object).Count
}
$Manifest | ConvertTo-Json -Depth 3 | Out-File (Join-Path $BackupPath "manifest.json")
Write-Host "   ✓ 备份清单已创建" -ForegroundColor Green

# 8. 压缩备份
Write-Host "`n🗜️ 步骤 8: 压缩备份..." -ForegroundColor Yellow
$ZipFile = "$BackupPath.zip"
Compress-Archive -Path $BackupPath -DestinationPath $ZipFile -Force
$ZipSize = (Get-Item $ZipFile).Length / 1MB
Write-Host "   ✓ 备份已压缩: $ZipFile ($([math]::Round($ZipSize, 2)) MB)" -ForegroundColor Green

# 9. Git 提交和推送
Write-Host "`n🚀 步骤 9: 推送到 GitHub..." -ForegroundColor Yellow

# 检查是否有未提交的更改
$Status = git status --porcelain
if ($Status) {
    Write-Host "   📤 发现未提交的更改，正在添加..." -ForegroundColor Yellow

    # 添加 Lightning Layer 到项目目录
    $ProjectLightning = ".\mindsymphony\lightning"
    if (Test-Path $LightningSource) {
        New-Item -ItemType Directory -Force -Path $ProjectLightning | Out-Null
        Copy-Item -Path "$LightningSource\*" -Destination $ProjectLightning -Recurse -Force
        Write-Host "   ✓ Lightning Layer 复制到项目目录" -ForegroundColor Green
    }

    # 添加 v21.2 配置文件
    $V21_2_Config = "$env:USERPROFILE\.claude\skills\mindsymphony\mindsymphony-v21.2.config.yml"
    if (Test-Path $V21_2_Config) {
        Copy-Item -Path $V21_2_Config -Destination "." -Force
        Write-Host "   ✓ v21.2 配置已复制" -ForegroundColor Green
    }

    # Git 操作
    git add -A
    git commit -m $GitMessage

    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✓ Git 提交成功" -ForegroundColor Green

        # 推送
        git push origin master
        if ($LASTEXITCODE -eq 0) {
            Write-Host "   ✓ 已推送到 GitHub" -ForegroundColor Green
        } else {
            Write-Host "   ❌ GitHub 推送失败" -ForegroundColor Red
        }
    } else {
        Write-Host "   ℹ 没有需要提交的更改" -ForegroundColor Gray
    }
} else {
    Write-Host "   ℹ 没有未提交的更改" -ForegroundColor Gray
}

# 10. 创建恢复脚本
Write-Host "`n📝 步骤 10: 创建恢复脚本..." -ForegroundColor Yellow
$RestoreScript = @"
# MindSymphony 恢复脚本
# 生成时间: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

Write-Host "恢复 MindSymphony..." -ForegroundColor Cyan

# 恢复 Lightning Layer
`$LightningDest = "`$env:USERPROFILE\.claude\skills\mindsymphony\lightning"
if (Test-Path "lightning") {
    Copy-Item -Path "lightning" -Destination `$LightningDest -Recurse -Force
    Write-Host "✓ Lightning Layer 已恢复" -ForegroundColor Green
}

# 恢复配置文件
if (Test-Path "mindsymphony-v21.2.config.yml") {
    Copy-Item -Path "mindsymphony-v21.2.config.yml" -Destination "`$env:USERPROFILE\.claude\skills\mindsymphony\" -Force
    Write-Host "✓ 配置文件已恢复" -ForegroundColor Green
}

# 恢复数据库 (可选)
if (Test-Path "database\store.db") {
    `$DBDest = "`$env:USERPROFILE\.claude\mindsymphony-v21\lightning"
    New-Item -ItemType Directory -Force -Path `$DBDest | Out-Null
    Copy-Item -Path "database\store.db" -Destination `$DBDest -Force
    Write-Host "✓ 数据库已恢复" -ForegroundColor Green
}

Write-Host "`n恢复完成！" -ForegroundColor Green
"@
$RestoreScript | Out-File (Join-Path $BackupPath "restore.ps1") -Encoding UTF8
Write-Host "   ✓ 恢复脚本已创建" -ForegroundColor Green

# 总结
Write-Host "`n═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  备份完成!" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "`n📦 备份位置:" -ForegroundColor White
Write-Host "   本地: $BackupPath" -ForegroundColor Gray
Write-Host "   压缩: $ZipFile ($([math]::Round($ZipSize, 2)) MB)" -ForegroundColor Gray
Write-Host "   GitHub: https://github.com/Caosmart1979/mindsymphony-os" -ForegroundColor Gray
Write-Host "`n🔄 恢复方法:" -ForegroundColor White
Write-Host "   1. 解压 $ZipFile" -ForegroundColor Gray
Write-Host "   2. 运行 restore.ps1" -ForegroundColor Gray
Write-Host "`n💡 提示: 建议定期执行备份以保护您的工作" -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
