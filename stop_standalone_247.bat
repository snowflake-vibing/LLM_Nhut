@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo Đang dừng toàn bộ dịch vụ ngầm...
.\venv\Scripts\python.exe scripts\manage_standalone.py stop
pause
