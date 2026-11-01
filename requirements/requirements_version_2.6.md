# 📑 BẢN ĐẶC TẢ YÊU CẦU KỸ THUẬT PHIÊN BẢN 2.6 (REQUIREMENTS VERSION 2.6)
### ⚖️ DỰ ÁN: LEGALTECH PLATFORM • TELEGRAM REMOTE CONTROL (/START & /END) & ANTIGRAVITY ENGINE
> 📌 **Ngày ban hành:** 01/11/2026 | **Kế thừa:** `preview_version_2.5.md` và `RULES.md`

---

## 🎯 MỤC TIÊU PHÁT TRIỂN (SPRINT GOALS)

1. **Telegram Command Listener & State Persistence:** Triển khai khả năng nhận diện và xử lý lệnh `/start`, `/end`, `/status` trực tiếp từ đoạn chat Telegram của người dùng.
2. **Watchdog Interruption Handling:** Tích hợp kiểm tra cờ trạng thái `data/autonomous_state.json` trong mỗi chu kỳ Watchdog.
3. **Antigravity Synergy Documentation:** Hướng dẫn kết hợp Antigravity Slash Commands (`/goal`, `/schedule`) với Telegram Remote Control.

---

## 📋 CHI TIẾT CÁC TÁC VỤ KỸ THUẬT (SPRINT BACKLOG)

### SPRINT 1: XÂY DỰNG MODULE REMOTE CONTROLLER (`src/security/telegram_remote_controller.py`)
- [x] **Task 1.1:** Viết class `TelegramRemoteController` quản lý trạng thái tại `data/autonomous_state.json`.
- [x] **Task 1.2:** Lắng nghe tin nhắn mới từ Telegram Bot API qua `getUpdates` và lọc theo `chat_id` của người dùng.
- [x] **Task 1.3:** Xử lý các lệnh:
  - `/end` hoặc `/stop`: Chuyển trạng thái `paused` và gửi tin xác nhận dừng lại.
  - `/start` hoặc `/resume`: Chuyển trạng thái `running` và gửi tin xác nhận kích hoạt.
  - `/status`: Báo cáo tình trạng hiện tại của hệ thống.

---

### SPRINT 2: TÍCH HỢP WATCHDOG & AUTOMATION LOOP (`scripts/hourly_agent_watchdog.py`)
- [x] **Task 2.1:** Thêm bước kiểm tra lệnh điều khiển từ xa ngay đầu hàm `run_watchdog()`.
- [x] **Task 2.2:** Tạm dừng các tác vụ tự hành nếu hệ thống đang ở trạng thái `paused`.

---

### SPRINT 3: KIỂM THỬ HỒI QUY, APPTEST & ĐỒNG BỘ GITHUB
- [x] **Task 3.1:** Chạy AppTest Streamlit đảm bảo tính ổn định.
- [x] **Task 3.2:** Cập nhật `README.md` và `tutorial/run_guide_version_2.6.md`.
- [x] **Task 3.3:** Commit chuẩn Conventional Commits và `git push origin main`.
- [x] **Task 3.4:** Gửi phản hồi xác nhận hướng dẫn điều khiển về Telegram của người dùng.
