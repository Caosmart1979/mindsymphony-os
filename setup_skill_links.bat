@echo off
REM 技能目录符号链接设置启动器
REM 会自动请求管理员权限

setlocal

cd /d "%~dp0"

echo === 检查管理员权限...
net session >nul 2>&1
if %errorLevel% == 0 (
    echo [OK] 已具有管理员权限
    echo.
    echo 执行设置脚本...
    echo.
    PowerShell.exe -ExecutionPolicy Bypass -File "%~dp0setup_skill_symlinks.ps1"
) else (
    echo [!] 需要管理员权限
    echo.
    echo 正在请求管理员权限...
    echo.
    PowerShell.exe -Command "Start-Process PowerShell.exe -ArgumentList '-ExecutionPolicy Bypass -File ""%~dp0setup_skill_symlinks.ps1""' -Verb RunAs"
)

endlocal
pause
