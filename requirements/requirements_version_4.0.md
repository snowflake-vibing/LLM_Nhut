# 📋 ĐẶC TẢ YÊU CẦU KỸ THUẬT PHIÊN BẢN 4.0 (REQUIREMENTS VERSION 4.0 - MAJOR RELEASE)
### The In-Chat Multi-Tool Autonomous Legal Workstation & Multimodal Evidence Diagnostic Engine

> **Tài liệu tham chiếu:** [`RULES.md`](../RULES.md) | File đánh giá tiền đề: [`preview_version_3.1.md`](./preview_version_3.1.md)  
> **Trạng thái:** [x] ĐÃ HOÀN THÀNH 100% & VERIFIED

---

## 🎯 1. MỤC TIÊU PHIÊN BẢN 4.0 (MAJOR RELEASE)

Tạo bước nhảy vọt toàn diện biến LegalTech Platform thành **Trạm Làm Việc Pháp Lý Đa Năng Trực Tiếp Trong Khung Chat (In-Chat Legal Workstation)**:
1. **Nạp & Giám định Tài liệu / Ảnh Chứng Cứ Đa Phương Tiện (Multimodal File Upload & OCR).**
2. **Bộ Công Cụ Pháp Lý Dân Sinh 1-Chạm (In-Chat Citizen Legal Tools):** Tính án phí NQ 326, Kiểm tra thời hiệu BLDS, Tra cứu thẩm quyền cơ quan.
3. **Gợi Ý Kép Thông Minh (Dual-Action Suggestions):** Gợi ý câu trả lời nhanh A/B/C + Gợi ý câu hỏi đào sâu 1-chạm cho người dùng.

---

## 🛠️ 2. CHI TIẾT CÁC TÍNH NĂNG VÀ MÃ NGUỒN MỚI

### 2.1. Bộ Công Cụ Pháp Lý Dân Sinh 1-Chạm (`src/tools/citizen_legal_tools.py`)
- [x] `CitizenLegalTools.calculate_court_fee(dispute_amount_vnd)`:
  - Tính chính xác Án phí Dân sự Sơ thẩm theo Biểu mức Nghị quyết 326/2016/UBTVQH14.
  - Tự động tính Tiền tạm ứng án phí phải nộp trước (50%) và chỉ rõ căn cứ pháp luật.
- [x] `CitizenLegalTools.check_statute_of_limitations(incident_date_str, domain)`:
  - Tính toán số ngày/tháng còn lại dựa trên ngày phát sinh sự việc theo Điều 429, 588, 623 BLDS 2015.
  - Cảnh báo trạng thái: `🟢 CÒN THỜI HIỆU` hoặc `⚠️ ĐÃ HẾT THỜI HIỆU KHỞI KIỆN`.
- [x] `CitizenLegalTools.locate_competent_authority(dispute_type, defendant_district, defendant_province)`:
  - Định vị rõ ràng quy trình 2 bước: Bước 1 (Tiếp nhận ban đầu: UBND xã đối với đất đai, Công an đối với lừa đảo, TAND đối với nợ nần); Bước 2 (Cơ quan xét xử/kiểm sát tiếp theo).

### 2.2. Trình Bóc Tách & Giám Định Chứng Cứ Đa Phương Tiện (`src/tools/multimodal_evidence_parser.py`)
- [x] Hỗ trợ nạp trực tiếp trong Chat: File tài liệu (`.pdf`, `.docx`, `.txt`) và Hình ảnh chứng cứ (`.png`, `.jpg`, `.jpeg`).
- [x] Bóc tách văn bản, trích xuất dữ liệu tài sản, ngày tháng, chữ ký, con dấu.
- [x] Chấm điểm Thước đo Giá trị Chứng cứ (0 - 100 điểm) theo BLTTDS 2015 và đưa ra lời khuyên lập Vi bằng Thừa phát lại kịp thời.
- [x] 1-click đưa toàn bộ nội dung bóc tách vào cuộc trò chuyện với Luật sư AI.

### 2.3. Hệ Thống Gợi Ý Kép Thông Minh (Dual-Action Dynamic Chips)
- [x] Nâng cấp `CitizenIntakeAgent`:
  - Trả về `quick_options` (Các phương án A/B/C hoặc Có/Không để người dân bấm trả lời câu hỏi của luật sư).
  - Trả về `suggested_followups` (Các câu hỏi đào sâu then chốt để người dân hỏi luật sư chỉ bằng 1 chạm).
- [x] Đồng bộ hiển thị mượt mà trên cả Giao diện Web Streamlit lẫn Bot Telegram Daemon.

---

## 🧪 3. KẾT QUẢ KIỂM THỬ

- Streamlit AppTest: **`PASS 100% with no exceptions!`**
- Kiểm thử công cụ tính án phí: Vụ tranh chấp 100.000.000 VNĐ $\rightarrow$ Án phí 5.000.000 VNĐ, Tạm ứng 2.500.000 VNĐ (Chính xác theo NQ 326/2016).
- Kiểm thử thời hiệu: Ngày 15/05/2023 $\rightarrow$ Còn thời hiệu khởi kiện đến 15/05/2026.
