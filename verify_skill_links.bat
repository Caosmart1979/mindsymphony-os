@echo off
REM 技能目录链接验证启动器

cd /d "%~dp0"

PowerShell.exe -ExecutionPolicy Bypass -File "%~dp0verify_skill_links.ps1"

pause
