# 📋 ĐẶC TẢ YÊU CẦU KỸ THUẬT PHIÊN BẢN 3.0 (REQUIREMENTS VERSION 3.0)
### The Citizen-Centric Conversational Intake & Multi-Turn Socratic Diagnostic Platform

> **Tài liệu tham chiếu:** [`RULES.md`](../RULES.md) | File đánh giá tiền đề: [`preview_version_2.9.md`](./preview_version_2.9.md)  
> **Trạng thái:** [x] ĐÃ HOÀN THÀNH 100% & VERIFIED

---

## 🎯 1. MỤC TIÊU PHIÊN BẢN 3.0 (MAJOR RELEASE)

Chuyển đổi toàn diện trải nghiệm tương tác của LegalTech Platform từ cơ chế *"trả lời dồn dập toàn bộ điều luật (One-shot legal dump)"* sang **"Thăm khám Pháp lý Từng bước Đa lượt (Multi-Turn Socratic Legal Intake)"**, đặt 100% trọng tâm vào **Cá nhân & Người dân**; tạm đưa phạm vi Doanh nghiệp / Công ty vào chế độ chờ.

---

## 🛠️ 2. CHI TIẾT TÍNH NĂNG VÀ KIẾN TRÚC MỚI

### 2.1. Tác Nhân Thăm Khám Pháp Lý Dân Sinh (`src/agents/citizen_intake_agent.py`)
- [x] Tạo lớp `CitizenIntakeAgent` với các nguyên tắc vàng:
  - **Không trả lời dồn dập:** Không trút tràng điều luật khô khan vào tin nhắn chính.
  - **Hỏi để chắc chắn:** Chỉ hỏi tối đa 1 đến 2 câu hỏi trọng tâm nhất nhằm xác thực chứng cứ, thời gian, và mong muốn của người dân.
  - **Gợi ý lựa chọn nhanh (Quick-reply options):** Tự động sinh ra 3-4 nút bấm gợi ý (A/B/C, Có/Không, Giấy viết tay / Tin nhắn Zalo...) để người già hoặc người ít thạo công nghệ chỉ cần bấm chọn.
  - **Giọng điệu đồng hành:** Xưng hô "mình - bạn", mộc mạc như người bạn hiểu luật ngồi lắng nghe bên chén trà.

### 2.2. Đại Tu Trải Nghiệm Chatbot Tab 1 (`app/main.py`)
- [x] Đính kèm Banner thông báo phạm vi: `🎯 Định Hướng Trọng Tâm: 👨‍👩‍👧 Dành Cho Cá Nhân & Người Dân`.
- [x] Tích hợp bộ thăm khám `CitizenIntakeAgent` làm luồng phản hồi chính trong bong bóng chat.
- [x] Hiển thị các nút bấm trả lời nhanh (Quick Options) trực quan ngay dưới câu hỏi của AI.
- [x] Đưa toàn bộ điều luật chuyên sâu, kết quả quét hợp đồng và biểu mẫu dự thảo vào Expander thu gọn (`⚖️ Xem Thêm Căn Cứ Điều Luật & Hồ Sơ Đính Kèm`), giúp người dân không bị ngợp.

### 2.3. Nâng Cấp Luồng Trò Chuyện Trực Tiếp Trên Telegram Daemon (`scripts/telegram_bot_daemon.py`)
- [x] Tích hợp `CitizenIntakeAgent` vào bot Telegram `@SnowflakeVibingBot`.
- [x] Phản hồi ngắn gọn, hỏi 1 câu xác minh then chốt kèm danh sách gợi ý gõ nhanh dạng bullet points.
- [x] Giữ nguyên khả năng phản hồi sub-second (<1s) và các lệnh quản trị `/status`, `/audit`, `/end`, `/start`.

---

## 🧪 3. KỊCH BẢN KIỂM THỬ THỰC ĐỊA

1. **Tình huống Đòi nợ cá nhân:**
   - *Người dân nhắn:* "Tôi cho đứa bạn mượn 50 triệu tiêu xài, hẹn tháng trước trả mà giờ nó im luôn, gọi điện không bắt máy."
   - *AI phản hồi:* Trấn an ngắn gọn $\rightarrow$ Hỏi đúng 1 câu: *"Khi cho vay, hai bên có lập giấy viết tay không, hay chỉ nhắn tin qua Zalo / chuyển khoản ngân hàng?"* $\rightarrow$ Đưa ra 4 nút chọn nhanh.
2. **Tình huống Tranh chấp đất đai:**
   - *Người dân nhắn:* "Hàng xóm mới mua đất kế bên đập tường cũ xây tường mới lấn sang sân nhà tôi."
   - *AI phản hồi:* Trấn an $\rightarrow$ Hỏi: *"Thửa đất nhà bạn hiện đã có Sổ đỏ chính chủ đo đạc ranh giới tọa độ rõ ràng chưa?"* $\rightarrow$ Đưa ra các lựa chọn Có / Chưa có sổ đỏ.
