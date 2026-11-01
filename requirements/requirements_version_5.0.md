# 📋 ĐẶC TẢ YÊU CẦU KỸ THUẬT PHIÊN BẢN 5.0 (REQUIREMENTS VERSION 5.0 - MAJOR RELEASE)
### The 2-Way Adversarial Courtroom Simulator & Strategic Litigation Forecaster

> **Tài liệu tham chiếu:** [`RULES.md`](../RULES.md) | File đánh giá tiền đề: [`preview_version_4.1.md`](./preview_version_4.1.md)  
> **Trạng thái:** [x] ĐÃ HOÀN THÀNH 100% & VERIFIED

---

## 🎯 1. MỤC TIÊU PHIÊN BẢN 5.0 (MAJOR RELEASE)

Tạo nên **bước nhảy vọt mang tính cách mạng** từ một chatbot tư vấn thông thường thành **Tổng Tham Mưu Trưởng Chiến Lược Tố Tụng Dân Sự**:
1. **Mô Phỏng Giả Lập Phiên Tòa Đối Kháng 2 Chiều (`LegalLitigationSimulator`).**
2. **Dự Báo Tỷ Lệ Thắng Kiện Khách Quan (0 - 100%)** dựa trên loại chứng cứ có sẵn.
3. **Bóc Tách Chiêu Bài Phản Đòn Của Bị Đơn & Trang Bị Đòn Phản Công Hóa Giải.**
4. **Tích Hợp Trực Tiếp Tab 5 Vào In-Chat Toolbar Của Chatbot Tab 1.**

---

## 🛠️ 2. CHI TIẾT TÍNH NĂNG VÀ MÃ NGUỒN MỚI

### 2.1. Động Cơ Mô Phỏng Bàn Cờ Tố Tụng 2 Chiều (`src/tools/litigation_simulator.py`)
- [x] Tạo lớp `LegalLitigationSimulator`:
  - `simulate_case(case_type, facts, evidence_type)`:
    - **Dự báo tỷ lệ thắng kiện (Win Rate %):** Công chứng/Vi bằng (90%), Giấy viết tay (75%), Tin nhắn Zalo (60%), Lời nói miệng (45%).
    - **Mũi tấn công của Nguyên đơn:** Căn cứ Điều 463, 468 BLDS (Đòi nợ), Điều 166, 202, 203 Luật Đất đai (Tranh chấp đất), Điều 56, 81 Luật HNGĐ (Ly hôn).
    - **Chiêu bài phản đòn của Bị đơn:** Yêu cầu giám định chữ ký để câu giờ, khai đã trả tiền mặt không giấy biên nhận, viện dẫn hết thời hiệu 3 năm, nại tranh chấp ranh giới cũ do địa chính đo sai, tẩu tán tài sản trước khi nộp đơn.
    - **Kế sách hóa giải tối ưu:** Yêu cầu áp dụng biện pháp khẩn cấp tạm thời (kê biên, phong tỏa tài khoản), yêu cầu đình chỉ thi công công trình lấn chiếm, lập Vi bằng tin nhắn Zalo.
    - **Dự báo phán quyết của Hội đồng Xét xử:** Đưa ra nhận định khách quan về kết quả vụ án.

### 2.2. Tích Hợp Tab 5 Trong In-Chat Toolbar (`app/main.py`)
- [x] Thêm Tab `"⚖️ 5. Giả Lập Bàn Cờ Tố Tụng 2 Chiều"` trong `Hộp Công Cụ Dân Sinh 1-Chạm`.
- [x] Giao diện trực quan 2 cột: Cột Xanh (Mũi tấn công của Bạn) vs Cột Đỏ (Chiêu phản đòn của Đối phương), kèm Thẻ điểm Tỷ lệ thắng và Kế sách hành động.

---

## 🧪 3. KẾT QUẢ KIỂM THỬ

- Streamlit AppTest: **`PASS 100% with no exceptions!`**
- Test Case Đòi nợ có Giấy viết tay $\rightarrow$ Tỷ lệ thắng 75%, cảnh báo đối phương chối chữ ký $\rightarrow$ Khuyến nghị nộp bản chính trưng cầu giám định và phong tỏa tài khoản.
