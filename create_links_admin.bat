@echo off
REM 以管理员权限创建剩余的符号链接

PowerShell.exe -Command "Start-Process PowerShell -ArgumentList '-NoExit', '-ExecutionPolicy Bypass', '-File', '%~dp0admin_links.ps1' -Verb RunAs"
