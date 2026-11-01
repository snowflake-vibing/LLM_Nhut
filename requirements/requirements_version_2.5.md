# 📑 BẢN ĐẶC TẢ YÊU CẦU KỸ THUẬT PHIÊN BẢN 2.5 (REQUIREMENTS VERSION 2.5)
### ⚖️ DỰ ÁN: LEGALTECH PLATFORM • PLAIN-LANGUAGE DUAL-PERSONA SWITCHER & COMPASSIONATE MENTOR
> 📌 **Ngày ban hành:** 01/11/2026 | **Kế thừa:** `preview_version_2.4.md` và `RULES.md`

---

## 🎯 MỤC TIÊU PHÁT TRIỂN (SPRINT GOALS)

Tạo đột phá về khả năng tiếp cận pháp luật (*Legal Accessibility Heuristics*):
1. **Plain-Language Engine:** Xây dựng engine chuyển đổi ngôn ngữ hàn lâm sang phong cách đàm thoại đời thường, mộc mạc, gần gũi nhưng giữ trọn 100% bản chất pháp lý.
2. **Dual-Persona In-Chat Experience:** Tích hợp tính năng 1-click chuyển đổi văn phong song ngữ ngay bên dưới từng câu trả lời của AI.
3. **Báo cáo Chu kỳ Tự hành #2 về Telegram:** Gửi tóm tắt các tính năng mới và tình trạng mã nguồn về Telegram của người dùng.

---

## 📋 CHI TIẾT CÁC TÁC VỤ KỸ THUẬT (SPRINT BACKLOG)

### SPRINT 1: XÂY DỰNG PLAIN-LANGUAGE ENGINE (`src/tools/plain_language_engine.py`)
- [x] **Task 1.1:** Định nghĩa từ điển giải thích thuật ngữ tư pháp thông dụng bằng ngôn ngữ đời thường (`LEGAL_GLOSSARY_PLAIN_EXPLANATIONS`).
- [x] **Task 1.2:** Triển khai phương thức `translate_to_plain_language()` ứng dụng Persona "Người Bạn Luật Sư Tận Tâm" theo cấu trúc 3 phần (Tóm gọn bản chất, 3 việc nên làm ngay, Cạm bẫy cần tránh).

---

### SPRINT 2: TÍCH HỢP GIAO DIỆN CHATBOT (`app/main.py`)
- [x] **Task 2.1:** Khởi tạo `PlainLanguageEngine` trong session state của Streamlit.
- [x] **Task 2.2:** Thêm component Expander "☕ Xem Diễn giải sang Ngôn ngữ Bình dân" ngay dưới từng tin nhắn tư vấn của trợ lý ảo trong Tab 1.

---

### SPRINT 3: KIỂM THỬ HỒI QUY, APPTEST & ĐỒNG BỘ GITHUB
- [x] **Task 3.1:** Chạy AppTest đảm bảo không phát sinh lỗi widget Streamlit.
- [x] **Task 3.2:** Cập nhật `README.md` và `tutorial/run_guide_version_2.5.md`.
- [x] **Task 3.3:** Commit chuẩn Conventional Commits và `git push origin main`.
- [x] **Task 3.4:** Gửi tin nhắn Telegram thông báo Chu kỳ 2 hoàn tất về điện thoại người dùng.
