@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo Đang khởi chạy hệ thống LegalTech 24/7 độc lập ngoài Windows...
.\venv\Scripts\python.exe scripts\manage_standalone.py start
pause
