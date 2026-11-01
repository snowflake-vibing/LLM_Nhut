# 📋 ĐẶC TẢ YÊU CẦU KỸ THUẬT PHIÊN BẢN 3.0 (REQUIREMENTS VERSION 3.0 - MAJOR RELEASE)
### The Citizen-Centric Conversational Legal Workstation & Multimodal Judicial Suite

> **Tài liệu tham chiếu:** [`RULES.md`](../RULES.md) | File đánh giá tiền đề: [`preview_version_2.9.md`](./preview_version_2.9.md)  
> **Trạng thái:** [x] ĐÃ HOÀN THÀNH 100% & TOÀN DIỆN HÓA

---

## 🎯 1. TỔNG QUAN PHIÊN BẢN 3.0

Phiên bản 3.0 đánh dấu **bước ngoặt chuyển mình chiến lược** của LegalTech Platform:
- Chuyển 100% trọng tâm phục vụ **Cá nhân & Người dân** (Người cao tuổi, người mắt kém/khiếm thị, người ít am hiểu công nghệ và người hoang mang khi vướng tranh chấp dân sự).
- Đưa toàn bộ module doanh nghiệp phức tạp vào chế độ chờ (standby) ở Tab 2 Studio.
- Thay thế hoàn toàn thói quen *"xả tràng dài điều luật khô khan"* bằng **"Thăm khám Pháp lý Từng bước (Socratic Legal Intake)"** kèm hệ thống công cụ dân sinh tương tác 1-chạm toàn diện.

---

## 🛠️ 2. CHI TIẾT CÁC NĂNG LỰC CỐT LÕI CỦA VERSION 3.0

### 2.1. Tác Nhân Thăm Khám Socratic & Gợi Ý Kép 1-Chạm (`src/agents/citizen_intake_agent.py`)
- Lắng nghe, lọc bỏ cảm xúc tiêu cực/hoang mang (`EmotionalRantParser`).
- Hỏi từng bước 1-2 câu then chốt để xác minh chứng cứ và mốc thời gian trước khi kết luận.
- **Hệ thống Gợi ý Kép 1-chạm:**
  - `quick_options`: Các nút chọn nhanh câu trả lời (A/B/C, Có/Không, Giấy viết tay/Zalo...) để người già không phải gõ chữ.
  - `suggested_followups`: Các nút gợi ý câu hỏi tiếp theo người dân nên hỏi Luật sư.

### 2.2. Trợ Lý Giọng Nói Tiếng Việt Song Phương (Two-Way Voice Assistant)
- **Voice Input:** Cổng thu âm giọng nói trực tiếp (`st.audio_input`) giúp người dân chỉ việc nói mà không cần gõ bàn phím.
- **Voice Output (TTS) (`src/tools/voice_narrator.py`):** Nút **`🔊 Đọc to lời giải thích bằng giọng nói`** dưới mỗi phản hồi của AI. Tự động làm sạch định dạng Markdown, cất giọng đọc tiếng Việt ấm áp, rõ ràng cho người cao tuổi và người khiếm thị lắng nghe.

### 2.3. Hộp Công Cụ Dân Sinh 1-Chạm (In-Chat Toolbar 6 Tabs)
Tích hợp trực tiếp tại Tab 1 Chatbot:
1. **💰 1. Tính Án Phí Tòa Án (NQ 326/2016):** Tính chính xác án phí dân sự sơ thẩm và mức tạm ứng 50% phải nộp cho cơ quan thi hành án.
2. **📝 2. Xuất Đơn Khởi Kiện Chuẩn (.docx) (`InstantPetitionGenerator`):** Soạn thảo tức thì Đơn khởi kiện chuẩn Mẫu số 23-DS của Hội đồng Thẩm phán TANDTC.
3. **⏳ 3. Kiểm Tra Thời Hiệu Khởi Kiện (Điều 429 BLDS):** Xác định vụ việc còn hay hết thời hiệu 3 năm để tránh bị Tòa đình chỉ.
4. **🏛️ 4. Xác Định Thẩm Quyền Tòa Án:** Hướng dẫn nộp đơn đúng TAND cấp Huyện nơi bị đơn cư trú hoặc nơi có bất động sản.
5. **⚖️ 5. Giả Lập Bàn Cờ Tố Tụng 2 Chiều (`LegalLitigationSimulator`):**
   - Dự báo tỷ lệ thắng kiện khách quan (0 - 100%) theo loại chứng cứ.
   - Bóc tách 3 mũi tấn công của Nguyên đơn vs 3 chiêu bài phản đòn của Bị đơn (chối chữ ký, nại hùn vốn làm ăn, câu giờ).
   - Trang bị 3 kế sách hóa giải: Nộp đơn yêu cầu áp dụng **Biện pháp khẩn cấp tạm thời** (phong tỏa tài khoản, kê biên tài sản) và lập Vi bằng chứng cứ điện tử.
6. **📦 6. Xuất Trọn Gói Bộ Hồ Sơ Tố Tụng (.docx) (`LitigationDossierGenerator`):**
   - Đóng gói toàn bộ Đơn Mẫu 23-DS + Bảng án phí NQ 326 + Báo cáo bàn cờ tố tụng + Danh mục chứng cứ kèm chữ ký thành 1 file Word duy nhất sẵn sàng nộp TAND.

### 2.4. Giám Định Chứng Cứ Đa Phương Tiện (`src/tools/multimodal_evidence_parser.py`)
- Tiếp nhận PDF, Word, Ảnh chụp giấy nợ viết tay, Sổ đỏ, Tin nhắn Zalo.
- Đánh giá Thước đo Giá trị Chứng cứ (Evidentiary Weight Meter 0-100%).

### 2.5. Trợ Năng Người Cao Tuổi & Bảo Mật Zero-Trust
- Phóng to font chữ 19px, line-height 1.85, chống mỏi mắt.
- Nút **Panic Wipe (Xóa Sạch Dấu Vết)** giải phóng RAM tức thì, bảo vệ an toàn cho nạn nhân bạo lực gia đình hoặc người bị theo dõi.

---

## 🧪 3. KIỂM THỬ VÀ NGHIỆM THU HỆ THỐNG

- Kiểm thử tự động `streamlit.testing.v1.AppTest`: **`PASS 100% (No Exceptions)`**.
- Telegram Daemon Agent phản hồi tức thì với độ trễ dưới 1 giây.
