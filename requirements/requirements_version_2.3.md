# 📑 BẢN ĐẶC TẢ YÊU CẦU KỸ THUẬT PHIÊN BẢN 2.3 (REQUIREMENTS VERSION 2.3)
### ⚖️ DỰ ÁN: LEGALTECH PLATFORM • CLOUD AUTONOMOUS WATCHDOG & 24/7 TELEGRAM ALERT PLATFORM
> 📌 **Ngày ban hành:** 01/11/2026 | **Kế thừa:** `preview_version_2.2.md` và `RULES.md`

---

## 🎯 MỤC TIÊU PHÁT TRIỂN (SPRINT GOALS)

1. **Cloud 24/7 Autonomous Execution:** Thiết lập GitHub Actions Workflow tự động kích hoạt kiểm thử toàn diện trên Cloud mỗi 1 giờ, hoạt động hoàn toàn độc lập với máy tính cá nhân.
2. **Real-time Telegram Notification:** Tích hợp module Telegram Notifier tự động gửi báo cáo tóm tắt tình trạng hệ thống về điện thoại người dùng sau mỗi chu kỳ kiểm tra.
3. **Bảo mật Bí mật Tuyệt đối (Secrets Management):** Quản lý `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` và `GOOGLE_API_KEY` qua `.env` và GitHub Repository Secrets theo Điều 3 của `RULES.md`.

---

## 📋 CHI TIẾT CÁC TÁC VỤ KỸ THUẬT (SPRINT BACKLOG)

### SPRINT 1: XÂY DỰNG MODULE TELEGRAM NOTIFIER (`src/security/telegram_notifier.py`)
- [x] **Task 1.1:** Viết class `TelegramNotifier` sử dụng Telegram Bot REST API (`https://api.telegram.org/bot<token>/sendMessage`).
- [x] **Task 1.2:** Thiết kế định dạng tin nhắn báo cáo thân thiện, trực quan với emoji, thời gian chuẩn ISO, và trạng thái của từng thành phần (Cloud LLM, Local LLM, Vector DB, LangGraph Workflow).
- [x] **Task 1.3:** Xử lý ngoại lệ an toàn (*graceful fallback*): Nếu chưa cấu hình token hoặc mạng chập chờn, ghi log hướng dẫn lấy token mà không làm gián đoạn chương trình chính.

---

### SPRINT 2: NÂNG CẤP WATCHDOG SCRIPT (`scripts/hourly_agent_watchdog.py`)
- [x] **Task 2.1:** Tích hợp `TelegramNotifier` vào chu kỳ kết thúc của `run_watchdog()`.
- [x] **Task 2.2:** Cung cấp cờ CLI `--notify` hoặc tự động gửi khi phát hiện biến môi trường `TELEGRAM_BOT_TOKEN`.

---

### SPRINT 3: THIẾT LẬP GITHUB ACTIONS WORKFLOW 24/7 (`.github/workflows/hourly_watchdog.yml`)
- [x] **Task 3.1:** Viết file cấu hình workflow với lịch kích hoạt `schedule: - cron: '0 * * * *'` (mỗi 1 giờ) và `workflow_dispatch` (kích hoạt thủ công bất kỳ lúc nào qua nút bấm trên GitHub).
- [x] **Task 3.2:** Cấu hình môi trường `ubuntu-latest`, Python 3.11, cài đặt `requirements.txt`.
- [x] **Task 3.3:** Liên kết các biến bí mật từ GitHub Secrets: `GOOGLE_API_KEY`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`.

---

### SPRINT 4: ĐỒNG BỘ CẤU HÌNH, HƯỚNG DẪN & GIT SYNC
- [x] **Task 4.1:** Cập nhật `.env.example` với hướng dẫn lấy Token từ `@BotFather` và Chat ID từ `@userinfobot`.
- [x] **Task 4.2:** Viết tài liệu hướng dẫn kiểm thử `tutorial/run_guide_version_2.3.md`.
- [x] **Task 4.3:** Cập nhật `README.md` thể hiện các tính năng Version 2.3 và hướng dẫn cài đặt Telegram Bot.
- [x] **Task 4.4:** Chạy kiểm thử toàn diện và đẩy code (`git push origin main`) lên GitHub repository `https://github.com/snowflake-vibing/LLM_Nhut`.
