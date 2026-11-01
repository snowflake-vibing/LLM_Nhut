# 📑 BẢN ĐẶC TẢ YÊU CẦU KỸ THUẬT PHIÊN BẢN 2.4 (REQUIREMENTS VERSION 2.4)
### ⚖️ DỰ ÁN: LEGALTECH PLATFORM • INTERACTIVE LEGAL ROADMAP & SMART EVIDENCE VAULT
> 📌 **Ngày ban hành:** 01/11/2026 | **Kế thừa:** `preview_version_2.3.md` và `RULES.md`

---

## 🎯 MỤC TIÊU PHÁT TRIỂN (SPRINT GOALS)

Nâng cấp trải nghiệm người dùng từ "Đọc văn bản tư vấn" sang **"Tương tác Tiến trình Pháp lý & Thẩm định Bằng chứng"**:
1. **Interactive Legal Roadmap Component:** Tạo sơ đồ bước nhảy trực quan (Stepper) hiển thị lộ trình xử lý vụ việc từ nộp đơn, hòa giải, xét xử đến thi hành án kèm thời hạn luật định.
2. **Smart Evidence Vault & Evidentiary Weight Meter:** Đánh giá tính pháp lý của chứng cứ theo Bộ luật Tố tụng Dân sự 2015, đưa ra cảnh báo rủi ro chứng cứ và điểm trọng lượng pháp lý (0 - 100).
3. **Báo cáo Tự hành về Telegram:** Tự động gửi tin nhắn báo cáo danh sách sửa đổi chi tiết về Telegram của người dùng ngay khi hoàn tất chu kỳ.

---

## 📋 CHI TIẾT CÁC TÁC VỤ KỸ THUẬT (SPRINT BACKLOG)

### SPRINT 1: XÂY DỰNG ENGINE TIẾN TRÌNH & BẰNG CHỨNG (`src/tools/evidence_vault_engine.py`)
- [x] **Task 1.1:** Định nghĩa dữ liệu lộ trình tố tụng (Roadmap Steps & Statutory Deadlines) cho 4 tình huống đời sống:
  - Bạo lực học đường (Giám định thương tật $\rightarrow$ Yêu cầu trường giải quyết $\rightarrow$ Tố cáo cơ quan công an / Phòng GD&ĐT).
  - Tranh chấp ranh giới đất đai (Trích lục hồ sơ $\rightarrow$ Hòa giải UBND cấp xã 45 ngày $\rightarrow$ Khởi kiện TAND $\rightarrow$ Thi hành án).
  - Đòi nợ khi con nợ trốn (Thu thập vi bằng $\rightarrow$ Xác minh cư trú cuối cùng $\rightarrow$ Khởi kiện niêm yết vắng mặt / Tố giác tội phạm 175 BLHS).
  - Ly hôn, nuôi con & tài sản (Hòa giải gia đình $\rightarrow$ Nộp đơn TAND $\rightarrow$ Phiên họp giao nộp chứng cứ $\rightarrow$ Phiên tòa sơ thẩm).
- [x] **Task 1.2:** Xây dựng cơ chế đánh giá giá trị pháp lý chứng cứ (*Evidentiary Weight Calculator*):
  - Nhận diện loại tài liệu (Văn bản công chứng, Vi bằng thừa phát lại, Dữ liệu điện tử Zalo/SMS, Giấy viết tay, Lời khai nhân chứng).
  - Chấm điểm trọng lượng chứng cứ (0 - 100%) và gợi ý củng cố pháp lý.

---

### SPRINT 2: TÍCH HỢP GIAO DIỆN ROADMAP & EVIDENCE VAULT (`app/main.py`)
- [x] **Task 2.1:** Tại Tab 2 (🧰 Legal Tools Studio), nâng cấp mục Social Cases & Legal Center bổ sung giao diện **Visual Roadmap Stepper** và **Smart Evidence Vault**.
- [x] **Task 2.2:** Tại Tab 1 (💬 AI Legal Chatbot), bổ sung nút mở rộng xem nhanh Tiến trình vụ việc & Thước đo chứng cứ.

---

### SPRINT 3: KIỂM THỬ HỒI QUY, APPTEST & ĐỒNG BỘ GITHUB
- [x] **Task 3.1:** Chạy AppTest đảm bảo không phát sinh lỗi widget Streamlit.
- [x] **Task 3.2:** Cập nhật `README.md` và `tutorial/run_guide_version_2.4.md`.
- [x] **Task 3.3:** Commit chuẩn Conventional Commits và `git push origin main`.
- [x] **Task 3.4:** Gửi tin nhắn Telegram tổng kết các nội dung đã sửa đổi về điện thoại người dùng.
