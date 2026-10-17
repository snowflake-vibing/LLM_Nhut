# 📋 YÊU CẦU KỸ THUẬT PHIÊN BẢN 2.0 (REQUIREMENTS VERSION 2)
### ⚖️ ĐỀ TÀI: LEGALTECH SME ASSISTANT • NÂNG CẤP HỆ THỐNG DOANH NGHIỆP THỰC CHIẾN

> 📌 **Tài liệu tham chiếu:** Kế thừa từ đánh giá và phản biện tại [`requirements/preview_version_1.md`](./preview_version_1.md).

---

## 🎯 1. Mục tiêu Phiên bản 2.0
Phiên bản 2.0 tập trung giải quyết 4 bài toán trọng tâm do người dùng phản hồi, nâng tầm hệ thống từ một chatbot tư vấn thông thường trở thành **Bộ giải pháp Tự động hóa Pháp lý Khởi nghiệp Toàn diện cho Doanh nghiệp Vừa & Nhỏ (SMEs)**.

---

## 🛠️ 2. Danh mục Yêu cầu Kỹ thuật Cần Hiện thực hóa

### 🚀 Yêu cầu 1: Trích dẫn Căn cứ Pháp luật Chi tiết & Kèm Link Kiểm chứng
* **Mô tả:** Khi AI đưa ra câu trả lời, phần căn cứ pháp luật phải trích dẫn chính xác:
  * Tên văn bản luật (Luật Doanh nghiệp 2020, Nghị định 01/2021/NĐ-CP...).
  * Số Điều, Khoản cụ thể.
  * Nội dung điều luật trích dẫn nguyên văn (*verbatim text*).
  * **Đường link chính thức (Verify URL):** Dẫn tới văn bản tại Cổng Thông tin điện tử Chính phủ (`vanban.chinhphu.vn`) hoặc Thư Viện Pháp Luật (`thuvienphapluat.vn`) để người dùng tự bấm vào kiểm chứng.
* **Giao diện:** Render dạng **Citation Card** có nút bấm `[🔗 Kiểm chứng tại Cổng TT Chính phủ]`.

### 🚀 Yêu cầu 2: Bộ Tạo Hồ sơ Kê khai Pháp lý Tự động (Document & Dossier Generator)
* **Mô tả:** Xây dựng tính năng hỗ trợ tạo bộ hồ sơ thành lập doanh nghiệp hoàn chỉnh:
  1. *Form thông tin tương tác:* Cho phép người dùng nhập thông tin cơ bản (Tên công ty dự kiến, Địa chỉ trụ sở, Vốn điều lệ, Danh sách thành viên/cổ đông sáng lập).
  2. *AI Drafting Agent:* Tự động kiểm tra tính hợp lệ và điền dữ liệu vào các biểu mẫu quy chuẩn theo Nghị định 01/2021/NĐ-CP:
     * **Mẫu Giấy đề nghị đăng ký doanh nghiệp** (Phụ lục I-2 hoặc I-3).
     * **Dự thảo Điều lệ công ty**.
     * **Danh sách thành viên / cổ đông sáng lập**.
  3. *Xuất file:* Cho phép người dùng bấm nút **Tải về file Word (.docx) / PDF** chuẩn để in ra ký nộp.

### 🚀 Yêu cầu 3: Tra cứu Mở rộng theo Kiến trúc Lai (Hybrid Retrieval & Pagination)
* **Mô tả:**
  * Giữ nguyên CSDL SQLite nội bộ để đảm bảo tốc độ và đáp ứng Tiêu chí 4 của giảng viên.
  * Bổ sung **Web Search Tool** cho AI Agent: Khi người dùng tìm kiếm ngành nghề mới hoặc không có trong CSDL nội bộ, Agent tự động kích hoạt tìm kiếm mở rộng trên Internet.
  * Thêm bộ lọc phân trang (Pagination) trên giao diện Tab Tra cứu để hiển thị toàn bộ các kết quả liên quan thay vì chỉ hiển thị giới hạn.

### 🚀 Yêu cầu 4: Trực quan hóa Quy trình Bảo mật PII Masking
* **Mô tả:**
  * Thêm bảng trực quan hoặc sơ đồ minh họa cơ chế hoạt động của PII Masking trên giao diện Tab Bảo mật:
    `Dữ liệu người dùng (CCCD thật) -> [Hệ thống Local che dấu] -> [Google Gemini chỉ thấy mã giả] -> [Hệ thống Local khôi phục]`
  * Giúp người dùng hiểu rõ dữ liệu cá nhân của mình được bảo vệ tuyệt đối như thế nào khi dùng Cloud API.

---

## 📅 3. Lộ trình Triển khai Version 2.0
1. [ ] **Sprint 2.1:** Cập nhật Metadata Vector Store & Thẻ Citation có link kiểm chứng.
2. [ ] **Sprint 2.2:** Xây dựng Tab "Tạo Hồ sơ Doanh nghiệp" & Engine xuất file văn bản `.docx`.
3. [ ] **Sprint 2.3:** Tích hợp Web Search Tool vào Multi-Agent Workflow.
4. [ ] **Sprint 2.4:** Benchmark đánh giá lại với Ragas và viết báo cáo Version 2.
