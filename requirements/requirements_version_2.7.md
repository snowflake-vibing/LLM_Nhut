# 📑 BẢN ĐẶC TẢ YÊU CẦU KỸ THUẬT PHIÊN BẢN 2.7 (REQUIREMENTS VERSION 2.7)
### ⚖️ DỰ ÁN: LEGALTECH PLATFORM • SPECIALIZED MULTI-AGENT SWARM, DUAL-PERSONA TESTER & REAL-TIME TELEGRAM DAEMON
> 📌 **Ngày ban hành:** 01/11/2026 | **Kế thừa:** `preview_version_2.6.md` và `RULES.md`

---

## 🎯 MỤC TIÊU PHÁT TRIỂN (SPRINT GOALS)

1. **Phân rã Hệ thống Đa Tác nhân Độc lập:** Chia tách rõ ràng trách nhiệm giữa Builder Agent, Adversarial Tester Agent, Telegram Daemon Bot Agent và Watchdog Agent (Đạt điểm tuyệt đối Tiêu chí 5 UIT: 1.5/1.5đ).
2. **Dual-Persona Adversarial Critic Engine:** Triển khai module tự động đóng 2 vai phản biện:
   - Senior QA Tester (Stress-test lỗi, kiểm tra điều luật, thử prompt injection).
   - First-time Customer (Đánh giá mức độ dễ dùng, ngôn ngữ bình dân, cảm xúc hoang mang/an tâm).
3. **Real-time Telegram Daemon Bot:** Xây dựng daemon chạy nền độc lập phản hồi tin nhắn Telegram tức thì (< 1 giây) cả cho lệnh điều khiển (`/start`, `/end`, `/status`) và câu hỏi tư vấn pháp luật trực tiếp.

---

## 📋 CHI TIẾT CÁC TÁC VỤ KỸ THUẬT (SPRINT BACKLOG)

### SPRINT 1: XÂY DỰNG ADVERSARIAL DUAL-PERSONA TESTER AGENT (`src/agents/adversarial_tester_agent.py`)
- [x] **Task 1.1:** Định nghĩa Persona 1 - Senior QA Tester:
  - Kiểm tra tính xác thực các trích dẫn pháp luật (BLDS 2015, Luật Đất đai, Luật HNGĐ, NĐ 01/2021).
  - Tấn công thử nghiệm Prompt Injection / Jailbreak để kiểm tra lớp phòng thủ Guardrails.
  - Chấm điểm Kỹ thuật & Độ chính xác (0 - 10đ).
- [x] **Task 1.2:** Định nghĩa Persona 2 - First-time Customer:
  - Đóng vai người dùng mới tinh đang lo lắng (ví dụ: bị quỵt tiền, tranh chấp đất, ly hôn).
  - Đánh giá độ rõ ràng của Roadmap, độ dễ hiểu của Két bằng chứng và bản dịch Plain-Language.
  - Chấm điểm Trải nghiệm & Độ an tâm (0 - 10đ).
- [x] **Task 1.3:** Xuất bản Báo cáo Thẩm định Độc lập (Dual-Persona Quality Audit Report).

---

### SPRINT 2: XÂY DỰNG REAL-TIME TELEGRAM DAEMON BOT AGENT (`scripts/telegram_bot_daemon.py`)
- [x] **Task 2.1:** Viết script daemon chạy vòng lặp thường trực với cơ chế Long-polling (`timeout=20`), xử lý tin nhắn ngay tức khắc.
- [x] **Task 2.2:** Tích hợp bộ định tuyến lệnh:
  - Nếu là lệnh `/start`, `/end`, `/status`: Gọi `TelegramRemoteController` phản hồi và lưu trạng thái.
  - Nếu là câu hỏi pháp lý tự nhiên: Kích hoạt `LegalMultiAgentWorkflow` tư vấn trực tiếp và gửi kết quả về Telegram.

---

### SPRINT 3: KIỂM THỬ HỒI QUY, APPTEST, CHẠY DUAL-PERSONA REVIEW & GITHUB SYNC
- [x] **Task 3.1:** Chạy AppTest Streamlit đảm bảo tính ổn định.
- [x] **Task 3.2:** Khởi chạy Dual-Persona Tester đánh giá Version 2.7.
- [x] **Task 3.3:** Khởi động Telegram Daemon Agent chạy nền.
- [x] **Task 3.4:** Cập nhật `README.md` và `tutorial/run_guide_version_2.7.md`.
- [x] **Task 3.5:** Commit chuẩn Conventional Commits và `git push origin main`.
- [x] **Task 3.6:** Bắn bản tin đánh giá 2 vai về Telegram của người dùng.
