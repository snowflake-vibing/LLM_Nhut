Set-Location -Path $PSScriptRoot
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "🚀 ĐANG KHỞI CHẠY HỆ THỐNG 24/7 ĐỘC LẬP NGOÀI WINDOWS..." -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Cyan

$Pythonw = "$PSScriptRoot\venv\Scripts\pythonw.exe"
$TelegramScript = "$PSScriptRoot\scripts\telegram_bot_daemon.py"
$PipelineScript = "$PSScriptRoot\scripts\continuous_dev_pipeline.py"
$AppScript = "$PSScriptRoot\app\main.py"

# 1. Khởi chạy Telegram Bot Daemon ngầm
Start-Process -FilePath $Pythonw -ArgumentList $TelegramScript -WorkingDirectory $PSScriptRoot
Write-Host "🤖 [Telegram Daemon] Đã khởi chạy ngầm thành công! ✅" -ForegroundColor Green

# 2. Khởi chạy Continuous Pipeline ngầm
Start-Process -FilePath $Pythonw -ArgumentList $PipelineScript -WorkingDirectory $PSScriptRoot
Write-Host "🌟 [Continuous Pipeline] Đã khởi chạy ngầm thành công! ✅" -ForegroundColor Green

# 3. Khởi chạy Streamlit Web App ngầm tại port 8501
Start-Process -FilePath $Pythonw -ArgumentList "-m streamlit run $AppScript --server.port 8501 --server.headless true" -WorkingDirectory $PSScriptRoot
Write-Host "🌐 [Streamlit Web App] Đã khởi chạy ngầm tại http://localhost:8501 ✅" -ForegroundColor Green

Write-Host ""
Write-Host "🎉 CẢ 3 DỊCH VỤ ĐÃ CHẠY ĐỘC LẬP TRÊN WINDOWS!" -ForegroundColor Yellow
Write-Host "💡 Bạn có thể TẮT Antigravity và Docker Desktop; hệ thống vẫn chạy 24/7!" -ForegroundColor Yellow
Write-Host ""
Start-Sleep -Seconds 3
