# 🧪 HƯỚNG DẪN KIỂM THỬ PHIÊN BẢN 2.7 (TEST & RUN GUIDE VERSION 2.7)
### ⚖️ DỰ ÁN: LEGALTECH PLATFORM • MẠNG LƯỚI ĐA TÁC NHÂN, DUAL-PERSONA TESTER & REAL-TIME TELEGRAM DAEMON
> 📌 **Phiên bản:** Version 2.7 | **Môi trường:** Python 3.10+ • LangGraph Multi-Agent • Telegram Daemon

---

## 🎯 I. TỔNG QUAN NÂNG CẤP TẠI VERSION 2.7

1. **Phân rã Hệ thống thành 4 AI Agent Chuyên trách (Specialized Multi-Agent Swarm):**
   - 🛠️ **Builder & Orchestrator Agent (`src/agents/graph.py`):** Xây dựng tính năng, phân tích hợp đồng và bóc tách dữ liệu.
   - 🕵️‍♂️ **Adversarial Dual-Persona Tester Agent (`src/agents/adversarial_tester_agent.py`):** Thẩm định 2 vai độc lập (Senior QA & First-time Customer).
   - 📱 **Real-time Telegram Interactive Daemon Agent (`scripts/telegram_bot_daemon.py`):** Tiến trình nền 24/7 phản hồi tin nhắn tức thì (< 1 giây).
   - ⏱️ **Autonomous Watchdog Agent (`scripts/hourly_agent_watchdog.py`):** Giám sát CI/CD và hồi quy hệ thống.
2. **Khắc phục Triệt để Độ trễ Telegram:** Bot hiện tại luôn trực chiến 24/7. Bạn nhắn bất cứ lúc nào, bot cũng trả lời ngay lập tức!
3. **Tư vấn Pháp luật Trực tiếp ngay trên Telegram:** Bạn có thể chat hỏi bất kỳ điều luật nào trực tiếp trong khung chat Telegram và nhận câu trả lời đầy đủ kèm trích dẫn!

---

## 📱 II. KỊCH BẢN KIỂM THỬ TRỰC TIẾP TRÊN TELEGRAM

### Thử nghiệm 1: Kiểm tra phản hồi tức thì của các lệnh điều khiển
1. Mở bot **`@SnowflakeVibingBot`** trên Telegram.
2. Nhắn `/status` $\rightarrow$ Bot trả lời ngay lập tức thông tin trạng thái và kiến trúc Version 2.7.
3. Nhắn `/end` $\rightarrow$ Bot phản hồi tức thì xác nhận tạm dừng.
4. Nhắn `/start` $\rightarrow$ Bot phản hồi tức thì xác nhận tiếp tục.

### Thử nghiệm 2: Chat hỏi tư vấn pháp lý trực tiếp trong Telegram
1. Nhắn vào bot:
   > *"Cho tôi hỏi con dưới 36 tháng tuổi khi ly hôn thì ai có quyền nuôi?"*
2. **Kỳ vọng:**
   - Bot lập tức phản hồi thông báo đang tra cứu qua LangGraph.
   - Sau vài giây, gửi câu trả lời hoàn chỉnh viện dẫn Khoản 3 Điều 81 Luật Hôn nhân & Gia đình 2014!
