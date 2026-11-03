Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "ℹ️ KIỂM TRA TRẠNG THÁI DỊCH VỤ ĐỘC LẬP 24/7..." -ForegroundColor Yellow
Write-Host "==================================================" -ForegroundColor Cyan

$procs = Get-Process -Name "pythonw" -ErrorAction SilentlyContinue
if ($procs) {
    Write-Host "🟢 Có $($procs.Count) tiến trình pythonw đang chạy ngầm 24/7:" -ForegroundColor Green
    foreach ($p in $procs) {
        Write-Host "• PID: $($p.Id) | Memory: $([math]::Round($p.WorkingSet64 / 1MB, 1)) MB" -ForegroundColor White
    }
    Write-Host ""
    Write-Host "✅ Hệ thống đang hoạt động bình thường kể cả khi tắt Antigravity và Docker Desktop!" -ForegroundColor Green
} else {
    Write-Host "🔴 Không có tiến trình pythonw nào đang chạy." -ForegroundColor Red
    Write-Host "👉 Hãy nhấp đúp vào start_standalone_247.bat để khởi động!" -ForegroundColor Yellow
}
Write-Host ""
pause
