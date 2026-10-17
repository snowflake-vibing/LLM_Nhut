# 📋 ĐÁNH GIÁ PHIÊN BẢN 2.0 & ĐỊNH HƯỚNG NÂNG CẤP (PREVIEW VERSION 2.0)
### ⚖️ DỰ ÁN: LEGALTECH PLATFORM • BƯỚC CHUYỂN MÌNH THÀNH "LUẬT SƯ TRỰC TUYẾN TOÀN NĂNG"

> 📌 **Tài liệu tham chiếu:** Kế thừa từ kết quả nghiệm thu Version 2.0 và các yêu cầu kiến trúc mang tính đột phá của người dùng ngày 17/10/2026.

---

## 📌 I. TỔNG HỢP Ý KIẾN ĐÁNH GIÁ & TẦM NHÌN CỦA NGƯỜI DÙNG (USER FEEDBACK)

Sau khi kiểm thử Version 2.0 với 6 tab, người dùng đưa ra các nhận xét chiến lược và yêu cầu tái cấu trúc toàn diện sản phẩm:

1. **Vị thế "Vị Luật sư Online Thực thụ" (Two-Sided Adversarial Legal Analysis):**
   * *Nỗi đau thực tế:* Khi đọc một bản hợp đồng lao động, hợp đồng dịch vụ hay thỏa thuận dân sự, người dùng không chỉ muốn biết đúng/sai quy định, mà cần **góc nhìn đa chiều của cả hai bên**:
     * Chỗ nào bên "ra luật / soạn thảo" (Bên mạnh thế - ví dụ: Chủ doanh nghiệp, Bên thuê dịch vụ, Bên cho thuê nhà) có thể **lợi dụng để ép quyền lợi**?
     * Chỗ nào bên "theo luật / ký kết" (Bên yếu thế - ví dụ: Người lao động, Freelancer, Người thuê nhà) có thể **lợi dụng kẽ hở hoặc bảo vệ chính mình**?
     * $\rightarrow$ Cung cấp một **Bản Phân tích Lợi thế & Bất lợi Đối kháng (Bilateral Risk & Exploitation Analysis)** giúp người dùng có góc nhìn tổng quát trước khi đặt bút ký.

2. **Mở rộng các Case Tình huống Xã hội Thực tế (Civil & Social Real-world Cases):**
   * Người dùng muốn mở rộng hệ thống để giải quyết các bài toán pháp lý "nóng" của đời sống người dân:
     * 🏫 **Bạo lực học đường:** Học sinh bị bạo lực có thương tích nhưng nhà trường tìm cách chối bỏ trách nhiệm $\rightarrow$ AI xác định trách nhiệm liên đới của nhà trường (Điều 599 BLDS 2015), quyền yêu cầu giám định thương tật, trình tự nộp đơn tố cáo cơ quan công an / sở GD&ĐT.
     * 🏡 **Tranh chấp Sổ đỏ & Đất đai:** Tranh chấp ranh giới quyền sử dụng đất, hàng xóm xây dựng lấn chiếm sang đất nhà mình $\rightarrow$ Quy trình hòa giải tại UBND cấp xã (Điều 202 Luật Đất đai), khởi kiện Tòa án nhân dân và thủ tục đo đạc hiện trạng.
     * 💰 **Đòi nợ & Tìm con nợ trốn tránh:** Chủ nợ có đầy đủ giấy tờ vay mượn nhưng con nợ bỏ trốn, không tìm được nơi cư trú $\rightarrow$ Thủ tục khởi kiện tại Tòa án nơi con nợ cư trú cuối cùng, thông báo tìm kiếm người vắng mặt, chuyển hồ sơ dấu hiệu "Lạm dụng tín nhiệm chiếm đoạt tài sản" (Điều 175 Bộ luật Hình sự).
     * 💔 **Ly hôn, Phân chia Tài sản & Quyền Nuôi con:** Tranh chấp quyền nuôi con dưới 36 tháng tuổi (ưu tiên mẹ theo Luật Hôn nhân & Gia đình), phân chia tài sản chung/riêng, nghĩa vụ cấp dưỡng.

3. **Soạn thảo Văn bản Pháp lý Đa dạng theo Yêu cầu Tùy biến (On-Demand Legal Drafting):**
   * Không gò bó trong một vài form cố định (như Giấy đề nghị ĐKDN hay Điều lệ công ty), mà cho phép người dùng **yêu cầu soạn bất kỳ loại văn bản pháp lý nào** (Đơn khởi kiện, Đơn tố giác tội phạm, Đơn yêu cầu hòa giải đất đai, Thỏa thuận phân chia tài sản sau ly hôn, Di chúc, Hợp đồng vay tiền cá nhân...).

4. **Tái cấu trúc Giao diện Tối giản (The 2-Tab NotebookLM Experience):**
   * *Gom gọn toàn bộ trang web chỉ còn đúng 2 Tab duy nhất:*
     * **Tab 1: 💬 AI Legal Chatbot (All-in-One Command Center):** Tích hợp tất cả các công cụ (RAG, Web Search, Quét hợp đồng, Soạn thảo văn bản). **Mỗi khi người dùng yêu cầu, công cụ tương tác (Interactive Tool Card, Form, Download) sẽ hiển thị ngay bên trong khung chat** theo lệnh text tự nhiên.
     * **Tab 2: 🧰 Legal Tools Studio:** Một trung tâm hiển thị toàn bộ các tool đang có trong hệ sinh thái (tương tự NotebookLM studio), cho phép xem danh mục tool, chạy thử tool độc lập hoặc xem tài liệu hướng dẫn.

---

## 🔬 II. PHẢN BIỆN CHUYÊN SÂU DƯỚI GÓC ĐỘ KỸ THUẬT AI (AI ENGINEERING CRITIQUE)

Dưới góc nhìn của một Kỹ sư AI phát triển hệ thống Agentic AI và bảo toàn **7 tiêu chí học thuật của đề cương UIT**, tôi xin phân tích chi tiết:

---

### 1. Phân tích: Tính năng "Góc nhìn Đối kháng Song phương" (Bilateral Exploitation Analysis)
* **Ý nghĩa học thuật:**
  * Đây là một bước tiến vượt bậc so với các chatbot pháp lý thông thường. Thông thường AI chỉ kiểm tra xem hợp đồng có phạm luật không.
  * Phân tích song phương yêu cầu áp dụng **Multi-Perspective Prompting / Role-playing CoT**:
    * *Persona 1 (Luật sư Bên A):* Tìm mọi điểm hở để tối đa hóa quyền kiểm soát và giảm thiểu trách nhiệm bồi thường.
    * *Persona 2 (Luật sư Bên B):* Bóc tách các bẫy câu chữ ("quyền quyết định cuối cùng thuộc về...", "thời hạn thanh toán phụ thuộc bên thứ ba..."), tìm kiếm các điều luật bắt buộc (mandatory statutory rules) để phản tố.
  * **Đầu ra:** Bảng ma trận đối sánh 3 cột trực quan:
    `[Điều khoản hợp đồng]` $\longleftrightarrow$ `[Bên A có thể lợi dụng điều gì?]` $\longleftrightarrow$ `[Bên B có thể lợi dụng hoặc bị ép ra sao?]` $\longleftrightarrow$ `[Giải pháp dung hòa an toàn]`

---

### 2. Phân tích: Mở rộng các Case Tình huống Đời sống Xã hội & Pháp lý Phức tạp
* **Thách thức:**
  * Bạo lực học đường, tranh chấp đất đai, trốn nợ, ly hôn... thuộc về các ngành luật hoàn toàn khác nhau:
    * *Luật Trẻ em 2016 & Nghị định 80/2017/NĐ-CP (Bạo lực học đường).*
    * *Luật Đất đai 2024 / 2013 & Bộ luật Tố tụng Dân sự 2015 (Tranh chấp ranh giới, lấn chiếm).*
    * *Bộ luật Dân sự 2015 & Bộ luật Hình sự 2015 (Vay nợ, trốn nợ, lừa đảo/lạm dụng tín nhiệm).*
    * *Luật Hôn nhân và Gia đình 2014 (Ly hôn, tài sản chung, quyền nuôi con).*
* **Giải pháp Kiến trúc: MULTI-DOMAIN SPECIALIZED LEGAL RETRIEVERS:**
  * Mở rộng thêm 4 tập văn bản nguồn tương ứng vào `data/raw_documents/`.
  * Xây dựng bộ **Tình huống Pháp lý Mẫu (Legal Benchmark Scenarios)** trong hệ thống để người dùng có thể bấm thử nghiệm ngay các case này với 1 click.

---

### 3. Phân tích: Engine Soạn thảo Văn bản Pháp lý Đa dạng theo Form Thông minh (Smart Pre-filled Form with Placeholders)
* **Ý nghĩa & Trải nghiệm thực tế:**
  * Đây là một cải tiến UX cực kỳ tinh tế và thấu hiểu tâm lý người dùng. Người dân hoặc chủ doanh nghiệp bình thường thường **không biết một lá đơn hay văn bản pháp lý cần có những điều khoản hay căn cứ luật nào**.
  * **Giải pháp kỹ thuật (Pre-filled by AI & Flexible Placeholders):**
    * Khi người dùng chọn một loại văn bản (Đơn khởi kiện đòi nợ, Đơn giải quyết tranh chấp đất đai, Đơn tố giác bạo lực học đường, Hợp đồng hợp tác kinh doanh...), AI sẽ **soạn thảo và điền sẵn 100% các căn cứ pháp luật, nội dung sự việc mẫu và các yêu cầu chuẩn mực**.
    * Về phần thông tin cá nhân: Cung cấp form trực quan với các trường (Họ tên, CCCD, địa chỉ, số tiền/diện tích...).
    * **Cơ chế Fallback thông minh:** Người dùng có thông tin gì thì điền vào đó. **Nếu người dùng chưa biết, chưa có giấy tờ trong tay hoặc để trống**, AI sẽ tự động thay thế bằng **các dòng chấm chuẩn hóa hoặc placeholder** (*`CCCD số: ........................................`* hoặc *`[SỐ TIỀN YÊU CẦU ĐÒI NỢ]`*).
    * Người dùng vẫn có thể bấm nút xuất và tải ngay tệp Word (.docx) chuẩn thể thức để điền tay hoặc bổ sung sau bất cứ lúc nào!

---

### 4. Phân tích: Tái cấu trúc Giao diện còn 2 Tab (The NotebookLM Experience)
* **Đánh giá UX:**
  * Đây là bước đi cực kỳ táo bạo và thông minh. Thay vì làm người dùng "hoa mắt" với 6 tab bên sidebar, giao diện 2 tab mang lại trải nghiệm hiện đại, tập trung cao độ:
    * **Tab 1: 💬 AI Legal Chatbot & Command Center:** 90% thời gian người dùng tương tác tại đây. Chatbot hiểu mọi lệnh, tự render tool (upload hợp đồng, quét lỗ hổng 2 chiều, điền form, tải file Word) ngay trong tin nhắn.
    * **Tab 2: 🧰 Legal Tools Studio:** Đóng vai trò là "Phòng trưng bày / Trạm công cụ" show toàn bộ 6 tools cốt lõi của hệ thống để giảng viên và người dùng có thể kiểm tra từng công cụ độc lập.
* **Bảo toàn 7 Tiêu chí UIT:**
  * Model Switcher, Guardrails PII, SQLite DB, Vector RAG và Benchmark Ragas vẫn được tích hợp đầy đủ và khéo léo trong cả 2 tab (Sidebar giữ nút Switcher và Health Check).

---

## 🎯 III. KẾT LUẬN & ĐỀ XUẤT LỘ TRÌNH CHO PHIÊN BẢN 2.1

Dựa trên toàn bộ phân tích kỹ thuật và định hướng sản phẩm mới, phiên bản tiếp theo được định danh chính thức là:  
**Phiên bản 2.1 (Version 2.1 - The Legal AI Lawyer & Studio Platform)** gồm 4 Sprint trọng tâm:

1. **Sprint 2.1.1: Bilateral Adversarial Analysis Engine:** Xây dựng module phân tích hợp đồng 2 chiều (bên ra luật vs bên theo luật có thể lợi dụng điều gì).
2. **Sprint 2.1.2: Multi-Domain Social Legal Knowledge Base:** Bổ sung cơ sở dữ liệu và kịch bản giải quyết 4 case đời sống (Bạo lực học đường, Tranh chấp đất đai, Trốn nợ, Ly hôn).
3. **Sprint 2.1.3: Dynamic On-Demand Document Drafting:** Engine tự động sinh và xuất file Word (.docx) cho bất kỳ loại đơn từ / hợp đồng pháp lý nào theo yêu cầu người dùng.
4. **Sprint 2.1.4: The 2-Tab NotebookLM Experience:** Tái cấu trúc giao diện Streamlit thành 2 Tab duy nhất (AI Chatbot Command Center & Legal Tools Studio).

*Chi tiết thông số kỹ thuật được đặc tả đầy đủ tại file kế tiếp: [`requirements/requirements_version_2.1.md`](./requirements_version_2.1.md).*
