# 📋 YÊU CẦU KỸ THUẬT PHIÊN BẢN 2.0 (REQUIREMENTS VERSION 2.0)
### ⚖️ ĐỀ TÀI: LEGALTECH SME ASSISTANT • ĐẠI TU KIẾN TRÚC & NỀN TẢNG TRÍ TUỆ PHÁP LÝ TOÀN DIỆN (MAJOR RELEASE)
#### 🚀 THE FULL-STACK LEGAL INTELLIGENCE & CONTRACT VULNERABILITY PLATFORM

> 📌 **Tài liệu tham chiếu:** Kế thừa từ đánh giá và phản biện kỹ thuật tại [`requirements/preview_version_1.1.md`](./preview_version_1.1.md).

---

## 🎯 1. Mục tiêu Đột phá của Phiên bản 2.0 (Major Release)
Phiên bản 2.0 đánh dấu bước chuyển đổi bước ngoặt từ một trợ lý hỏi-đáp RAG cơ bản sang một **Nền tảng Trí tuệ Pháp lý Toàn diện (Full-stack Legal Intelligence Platform)**:
1. **Thẩm định & Quét Lỗ hổng Hợp đồng:** Quét cạm bẫy pháp lý, cảnh báo điều khoản vi phạm điều cấm hoặc bất bình đẳng, chấm điểm an toàn (Legal Risk Score 0 - 100) và đề xuất điều khoản thay thế (Clause Redlining).
2. **In-Chat Generative UI (Interactive Command Center):** Khung chat trở thành trung tâm tương tác tổng, tự động triệu hồi các widget/form tạo hồ sơ và quét hợp đồng trực tiếp trong luồng hội thoại.
3. **Mở rộng Phạm vi Toàn diện (Hierarchical Multi-Domain RAG):** Bao quát toàn bộ hệ thống pháp luật chi phối cá nhân và tổ chức doanh nghiệp (*Bộ luật Dân sự 2015, Bộ luật Lao động 2019, Luật Thương mại 2005, Luật Sở hữu trí tuệ, Luật Quản lý Thuế...*).
4. **Học liên tục Chuẩn Công nghiệp (Continual Learning without Weight Training):** Cơ chế Dynamic In-Context Learning + Continuous Vector Ingestion + Deterministic Rule Engine đảm bảo 100% không bị ảo giác hay quên lãng.

---

## 🛠️ 2. Danh mục Yêu cầu Kỹ thuật Cụ thể

### 🚀 Yêu cầu 1: Tool Thẩm định, Quét Lỗ hổng & Chấm điểm Hợp đồng (Contract Vulnerability & Risk Scanner)
* **Mô tả:** Xây dựng công cụ phân tích hợp đồng chuyên sâu (`src/tools/contract_scanner.py`):
  * **Input:** Người dùng dán văn bản hợp đồng hoặc tải file hợp đồng (Hợp đồng thuê mặt bằng, Hợp đồng lao động, Hợp đồng mua bán hàng hóa, Hợp đồng hợp tác kinh doanh...).
  * **Cơ chế quét 4 nhóm rủi ro:**
    1. *Vi phạm điều cấm của pháp luật:* Điều khoản phạt vi phạm vượt quá mức trần 8% giá trị nghĩa vụ hợp đồng (Điều 301 Luật Thương mại 2005), điều khoản hạn chế quyền kết hôn/sinh con của người lao động (Điều 8 Bộ luật Lao động 2019)...
    2. *Điều khoản bất bình đẳng / một chiều:* Trao quyền đơn phương hủy bỏ hợp đồng cho một bên mà không cần lý do hoặc không chịu bồi thường.
    3. *Điều khoản mơ hồ, khó thi hành:* Trách nhiệm thanh toán không gắn hạn chót, cơ quan tài phán không xác định (ghi chung chung là "Tòa án có thẩm quyền").
    4. *Thiếu điều khoản bảo vệ trọng yếu:* Thiếu thỏa thuận Bất khả kháng (Force Majeure - Điều 156 BLDS 2015), thiếu điều khoản bảo mật thông tin (NDA), thiếu quy định xử lý tài sản sau thanh lý.
  * **Chấm điểm An toàn Pháp lý (Legal Risk Score 0 - 100):**
    * `85 - 100:` An toàn, cân bằng quyền lợi các bên.
    * `65 - 84:` Rủi ro trung bình, cần bổ sung điều khoản bảo vệ.
    * `< 65:` Rủi ro cao, tiềm ẩn tranh chấp nghiêm trọng hoặc vô hiệu từng phần.
  * **Đề xuất Điều khoản Chuẩn (Clause Redlining / Diff):**
    * AI đưa ra đoạn văn bản pháp lý thay thế chuẩn xác của luật sư để người dùng copy đàm phán lại.

---

### 🚀 Yêu cầu 2: In-Chat Interactive Canvas (Generative UI trong Khung Chat)
* **Mô tả:** Nâng cấp khung chat thành trung tâm điều khiển tương tác (Interactive Command Center):
  * Người dùng trò chuyện tự nhiên: *"soạn cho tôi một thỏa thuận bảo mật NDA giữa công ty và nhân viên mới"* hoặc *"hãy kiểm tra rủi ro hợp đồng này giúp tôi"*.
  * Router Agent tự động phát hiện ý định và **triệu hồi Interactive Action Card ngay bên trong tin nhắn chat**:
    * Cho phép điền nhanh các thông tin then chốt hoặc dán nội dung điều khoản trực tiếp.
    * Bấm nút `🔍 Phân tích Lỗ hổng` hoặc `📥 Tải file Word (.docx)` ngay tại tin nhắn mà không cần phải rời tab chat.
  * Giữ nguyên thanh menu Sidebar để người dùng có thể thao tác ở chế độ toàn màn hình (Full-page Workspace) khi cần.

---

### 🚀 Yêu cầu 3: Mở rộng Phạm vi Tri thức Pháp luật Đa tầng (Hierarchical Multi-Domain Legal RAG)
* **Mô tả:** Mở rộng cơ sở tri thức pháp luật từ 1 bộ luật sang hệ thống văn bản chi phối toàn diện cá nhân và doanh nghiệp:
  1. **Bộ luật Dân sự 2015 (Số 91/2015/QH13):** Quy chuẩn giao dịch, hợp đồng dân sự, đặt cọc, ủy quyền, bồi thường thiệt hại ngoài hợp đồng.
  2. **Bộ luật Lao động 2019 (Số 45/2019/QH14):** Giao kết HĐLĐ, thử việc, chấm dứt, sa thải, bảo hiểm xã hội, bảo vệ quyền lợi cá nhân người lao động và doanh nghiệp.
  3. **Luật Thương mại 2005 (Số 36/2005/QH11):** Hợp đồng mua bán hàng hóa, cung ứng dịch vụ, đại lý, mức trần phạt vi phạm, giải quyết tranh chấp thương mại.
  4. **Luật Sở hữu Trí tuệ (Số 50/2005/QH11 sửa đổi 2022):** Bản quyền tác giả phần mềm, nhãn hiệu thương mại, bảo vệ bí mật kinh doanh.
* **Cơ chế:** Phân tầng theo **Domain Collections** kết hợp với **Router Agent** định tuyến truy vấn, bảo đảm độ chính xác Ragas Context Precision $\ge 85\%$.

---

### 🚀 Yêu cầu 4: Cơ chế Tối ưu Chất lượng Liên tục Không Gây Ảo giác (Continual Optimization)
* **Mô tả:** Hiện thực hóa phản biện kỹ thuật về việc "học liên tục không đổi trọng số":
  1. *Dynamic In-Context Learning & Few-shot Bank (`src/agents/memory_store.py`):* Lưu trữ các case phân tích hợp đồng và mẫu điều khoản tối ưu vào kho dữ liệu động. Agent tự động truy xuất ví dụ tương đồng tốt nhất nạp vào prompt theo thời gian thực.
  2. *Deterministic Rule Engine:* Tích hợp bộ quy tắc cứng (Code-based verification) cho các chỉ số pháp lý bất biến (mức phạt trần 8%, thời hạn góp vốn 90 ngày, thời hạn báo trước chấm dứt HĐLĐ...) để loại trừ 100% khả năng hallucination.

---

## 📅 3. Lộ trình Triển khai Version 2.0 (Major Release) - [ĐÃ HOÀN THÀNH 100%]
1. [x] **Sprint 2.0.1:** Thu thập, chunking và xây dựng Hierarchical Vector Collections cho Bộ luật Dân sự 2015, Bộ luật Lao động 2019 và Luật Thương mại 2005 (kèm link kiểm chứng vanban.chinhphu.vn).
2. [x] **Sprint 2.0.2:** Xây dựng Engine Thẩm định Lỗ hổng Hợp đồng (`src/tools/contract_scanner.py`) với hệ thống chấm điểm rủi ro (0-100), gợi ý điều khoản thay thế (Redlining) và xuất báo cáo Word (.docx).
3. [x] **Sprint 2.0.3:** Tích hợp In-Chat Interactive Canvas (Generative UI) cho phép tương tác tool trực tiếp trong luồng hội thoại Streamlit (`app/main.py`).
4. [x] **Sprint 2.0.4:** Tích hợp Dynamic Few-shot Memory Store (`src/agents/memory_store.py`), cập nhật kịch bản kiểm thử benchmark và hoàn thiện tài liệu bàn giao.
