# 📑 BẢN ĐẶC TẢ YÊU CẦU KỸ THUẬT PHIÊN BẢN 2.8 (REQUIREMENTS VERSION 2.8)
### ⚖️ DỰ ÁN: LEGALTECH PLATFORM • HUMAN-CENTRIC ACCESSIBILITY, EMOTIONAL DE-NOISER & ZERO-TRUST PRIVACY
> 📌 **Ngày ban hành:** 01/11/2026 | **Kế thừa:** `preview_version_2.7.md` và `RULES.md`

---

## 🎯 MỤC TIÊU PHÁT TRIỂN (SPRINT GOALS)

Tái định nghĩa sản phẩm theo triết lý **"Pháp luật vì Con người" (Human-First LegalTech)**:
1. **Elderly & Low-Tech Mode:** Hỗ trợ người cao tuổi và người không rành công nghệ với giao diện chữ lớn (Large Font), độ tương phản cao và nút bấm siêu to.
2. **Emotional Disjointed Rant De-noiser & Socratic Guide:** Bộ lọc bóc tách lời kể dài dòng, cảm xúc lộn xộn ("nói không đâu vào đâu") thành 3 điểm cốt lõi, tự động hướng dẫn bằng các câu hỏi trắc nghiệm `[Có]` / `[Không]`.
3. **Panic Clear & Incognito Privacy Vault:** Nút bấm khẩn cấp xóa sạch 100% dữ liệu phiên làm việc trong 0.1 giây để bảo vệ người dùng trước nguy cơ bị xem trộm điện thoại/máy tính.
4. **Performance Acceleration:** Tối ưu hóa render Streamlit và bộ nhớ đệm giúp tốc độ phản hồi đạt mức tối đa.

---

## 📋 CHI TIẾT CÁC TÁC VỤ KỸ THUẬT (SPRINT BACKLOG)

### SPRINT 1: XÂY DỰNG BỘ LỌC CẢM XÚC & DẪN DẮT SOCRATIC (`src/tools/emotional_rant_parser.py`)
- [x] **Task 1.1:** Viết class `EmotionalRantParser`:
  - Phân tích văn bản dài dòng, rối bời, uất ức.
  - Trấn an tâm lý người dùng bằng lời khuyên chân thành và đồng cảm sâu sắc.
  - Trích xuất tự động 3 trường thông tin: (1) Ai là người vi phạm/gây tổn hại? (2) Thiệt hại thực tế là gì? (3) Mốc thời gian ước lượng.
  - Tạo bộ câu hỏi dẫn dắt từng bước dạng `[Có]` / `[Không]` (Socratic Questionnaire).

---

### SPRINT 2: XÂY DỰNG CƠ CHẾ BẢO MẬT KHẨN CẤP (`src/security/ephemeral_privacy.py`)
- [x] **Task 2.1:** Triển khai `EphemeralPrivacyManager`:
  - Chế độ Incognito Ephemeral: Không bao giờ lưu trữ vĩnh viễn nội dung nhạy cảm của người dùng xuống ổ đĩa nếu không được yêu cầu.
  - Tính năng `panic_wipe_session()`: Xóa sạch `st.session_state` (messages, memory, forms) và reset phiên tức thì.

---

### SPRINT 3: TÍCH HỢP GIAO DIỆN CHỮ LỚN & NÚT KHẨN CẤP TRÊN WEB (`app/main.py`)
- [x] **Task 3.1:** Thêm nút gạt chế độ **"👓 Chế độ Chữ Lớn Dành Cho Người Cao Tuổi"** trên Sidebar: Tự động điều chỉnh CSS font 19px, khoảng cách dòng rộng rãi, giao diện tương phản cao dễ đọc.
- [x] **Task 3.2:** Thêm nút đỏ khẩn cấp **"🚨 XÓA DẤU VẾT KHẨN CẤP (Panic Wipe)"** trên thanh điều hướng để người dùng bấm một phát là sạch bóng toàn bộ lịch sử tư vấn.
- [x] **Task 3.3:** Tích hợp bộ giải mã câu hỏi lộn xộn vào khung chat: Khi người dùng tâm sự dài dòng, AI tự động hiển thị bản tóm tắt mạch lạc kèm các nút bấm Có/Không để dẫn dắt tiếp.

---

### SPRINT 4: KIỂM THỬ HỒI QUY, APPTEST & GITHUB SYNC
- [x] **Task 4.1:** Chạy AppTest Streamlit xác nhận không phát sinh lỗi.
- [x] **Task 4.2:** Cập nhật `README.md` và `tutorial/run_guide_version_2.8.md`.
- [x] **Task 4.3:** Commit chuẩn mực và `git push origin main`.
- [x] **Task 4.4:** Báo cáo chi tiết qua Telegram cho người dùng.
