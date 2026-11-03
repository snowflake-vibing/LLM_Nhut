Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "🛑 ĐANG DỪNG TOÀN BỘ DỊCH VỤ NGẦM LEGALTECH..." -ForegroundColor Red
Write-Host "==================================================" -ForegroundColor Cyan

Stop-Process -Name "pythonw" -Force -ErrorAction SilentlyContinue
Write-Host "✅ Đã dừng toàn bộ dịch vụ ngầm (Telegram Daemon, Pipeline, Streamlit) thành công!" -ForegroundColor Green
Start-Sleep -Seconds 2
