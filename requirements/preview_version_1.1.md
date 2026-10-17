# 📋 ĐÁNH GIÁ PHIÊN BẢN 1.1 & ĐỊNH HƯỚNG NÂNG CẤP (PREVIEW VERSION 1.1)
### ⚖️ DỰ ÁN: LEGALTECH SME ASSISTANT • AI ENGINEER PROJECT (UIT)

> 📌 **Tài liệu tham chiếu:** Kế thừa từ kết quả bàn giao của Version 1.1 và các yêu cầu mở rộng mới của người dùng ngày 17/10/2026.

---

## 📌 I. TỔNG HỢP Ý KIẾN ĐÁNH GIÁ CỦA NGƯỜI DÙNG (USER FEEDBACK)

Sau khi nghiệm thu Version 1.1 (với 5 Tab, trích dẫn link Cổng TT Chính phủ, bộ tạo hồ sơ Word và Hybrid Web Search), người dùng tiếp tục đề xuất bước nhảy vọt mới với 4 trọng tâm:

1. **Bộ Công cụ Pháp lý Chuyên sâu (Legal Tools Suite):**
   * *Mong muốn:* Xây dựng các tool độc lập, mạnh mẽ:
     * Tool tìm kiếm pháp luật nâng cao (Search Tool).
     * Tool soạn thảo văn bản pháp lý (Drafting Tool).
     * **Tool đánh giá, thẩm định & chấm điểm văn bản pháp lý bằng cách phát hiện các lỗ hổng / rủi ro tiềm ẩn (Contract Vulnerability & Red-flag Scanning Tool).**
2. **Khung Chat Tương tác Toàn diện (In-Chat Interactive Canvas / Generative UI):**
   * *Hiện trạng v1.1:* Người dùng phải chuyển đổi giữa các tab riêng biệt ở thanh Sidebar (ví dụ: muốn tạo hồ sơ phải bấm sang Tab 2).
   * *Kỳ vọng:* Khung Chat đóng vai trò là một **Interactive Tổng (Command Center)**: Khi người dùng trò chuyện và muốn tạo hồ sơ hoặc thẩm định hợp đồng, AI sẽ triệu hồi và hiển thị **công cụ tương tác (form, widget, upload, live editor) ngay bên trong luồng chat**, không bắt người dùng phải rời khỏi ngữ cảnh hội thoại.
3. **Mở rộng Phạm vi Pháp lý Toàn diện (Scope Expansion):**
   * *Hiện trạng:* Phạm vi RAG chủ yếu tập trung vào Luật Doanh nghiệp 2020 và đăng ký kinh doanh.
   * *Kỳ vọng:* Mở rộng phạm vi bao quát **tất cả các văn bản pháp luật liên quan đến cả cá nhân và tổ chức doanh nghiệp** (Bộ luật Dân sự, Bộ luật Lao động, Luật Thương mại, Luật Sở hữu trí tuệ, Luật Quản lý Thuế...).
4. **Vấn đề Học liên tục của Tool (Tool Training & Continual Learning):**
   * *Băn khoăn:* "Các tool có cần được train liên tục để đưa ra kết quả tốt nhất không?"

---

## 🔬 II. PHẢN BIỆN CHUYÊN SÂU DƯỚI GÓC ĐỘ KỸ THUẬT AI (AI ENGINEERING CRITIQUE)

Dưới góc nhìn của một Kỹ sư AI phát triển hệ thống Agentic AI trong ngành Tư pháp số (LegalTech) và bám sát **7 tiêu chí học thuật của đề cương UIT**, tôi xin đưa ra phân tích chi tiết:

---

### 1. Phân tích: Tool Đánh giá, Chấm điểm Lỗ hổng Hợp đồng & Soạn thảo Pháp lý
* **Ý nghĩa thực tiễn & Học thuật:**
  * Đây là tính năng giá trị nhất của LegalTech hiện đại (tương tự các sản phẩm kỳ lân như *Robin AI, Ironclad, Casetext CoCounsel*). 
  * Thay vì chỉ hỏi - đáp chung chung, hệ thống có khả năng "đọc" một bản hợp đồng thật (file Word/PDF hoặc văn bản dán vào), bóc tách từng điều khoản và **phát hiện cạm bẫy pháp lý (Legal Vulnerability / Risk Detection)**.
* **Cơ chế Triển khai Kỹ thuật:**
  * **Module Thẩm định & Quét Rủi ro (Contract Risk Scanner):**
    * *Rủi ro loại 1 - Vi phạm điều cấm của luật:* Ví dụ thỏa thuận mức phạt vi phạm hợp đồng thương mại lên đến 20% (Vi phạm Điều 301 Luật Thương mại 2005 - mức trần tối đa là 8%).
    * *Rủi ro loại 2 - Điều khoản bất bình đẳng / mơ hồ:* Điều khoản đơn phương chấm dứt hợp đồng không báo trước, miễn trừ trách nhiệm vô căn cứ, điều khoản giải quyết tranh chấp không rõ cơ quan tài phán.
    * *Rủi ro loại 3 - Thiếu điều khoản bảo vệ cốt lõi:* Thiếu điều khoản Bất khả kháng (Force Majeure - Điều 156 Bộ luật Dân sự 2015), thiếu thỏa thuận bảo mật (NDA).
  * **Hệ thống Chấm điểm An toàn (Legal Risk Scoring Engine):**
    * Điểm số từ `0 đến 100` (100 = Tuyệt đối an toàn; < 60 = Nguy cơ tranh chấp cao).
    * Phân loại trực quan: 🔴 *Nghiêm trọng (Critical)*, 🟡 *Cảnh báo (Warning)*, 🟢 *Khuyến nghị tối ưu (Best Practice)*.
  * **Tính năng Redlining & Đề xuất Điều khoản Thay thế:**
    * Cung cấp nút bấm `Đề xuất điều khoản chuẩn (Clause Redlining)` để thay thế ngay điều khoản nguy hiểm bằng văn phong chuẩn mực của luật sư.

---

### 2. Phân tích: In-Chat Interactive Canvas (Generative UI trong Khung Chat)
* **Đánh giá trải nghiệm người dùng (UX):**
  * Chia tab ở Sidebar như v1.1 là giải pháp tổ chức tốt cho bài toán demo giảng viên, nhưng trong môi trường làm việc thực tế, người dùng thích **Chat-first Interface**: Muốn làm gì chỉ cần ra lệnh tự nhiên trong chat.
* **Thách thức kỹ thuật:**
  * Streamlit bản chất chạy theo mô hình re-run toàn bộ script khi state thay đổi.
  * Nếu nhúng một form phức tạp vào trong message Streamlit mà không xử lý Session State khéo léo, form sẽ bị reset mỗi lần người dùng gửi thêm tin nhắn mới.
* **Giải pháp Kiến trúc (Agent-triggered Generative UI):**
  * Xây dựng cơ chế **Interactive Intent Detection**: Khi `Router Agent` nhận diện người dùng muốn *"soạn thảo hợp đồng"*, *"tạo hồ sơ"* hoặc *"kiểm tra rủi ro văn bản"*, Agent trả về một cấu trúc dữ liệu đặc biệt (Interactive Action Payload).
  * Giao diện Chatbot sẽ render một **Interactive Action Card** ngay tại tin nhắn đó:
    * Chứa các input fields thu gọn hoặc file uploader.
    * Người dùng thao tác và bấm `Thực thi` ngay trong bubble chat.
    * Kết quả (file Word, bảng chấm điểm rủi ro, link kiểm chứng) hiển thị tiếp nối ngay trong luồng hội thoại.
  * Thanh Sidebar vẫn giữ vai trò Quick Navigation để người dùng truy cập trực tiếp các tool khi cần thao tác toàn màn hình.

---

### 3. Phân tích: Mở rộng Scope sang Toàn bộ Văn bản Cá nhân & Doanh nghiệp
* **Thách thức về độ chính xác RAG (The Retrieval Dilution Problem):**
  * Khi mở rộng từ 1 bộ luật (Luật Doanh nghiệp 2020) sang hàng chục bộ luật lớn (Dân sự, Lao động, Thương mại, Sở hữu trí tuệ, Thuế...), dung lượng tri thức sẽ tăng từ hàng trăm chunks lên hàng nghìn chunks.
  * Nếu dùng 1 Vector Index duy nhất, độ chính xác tìm kiếm (Context Precision) sẽ bị loãng: Người hỏi về hợp đồng lao động có thể bị kéo nhầm điều khoản của hợp đồng thương mại.
* **Giải pháp Kiến trúc: HIERARCHICAL LEGAL VECTOR ROUTER (Định tuyến Tri thức Đa tầng):**
  * Phân chia tri thức thành các **Collection chuyên ngành**:
    1. `corporate_law`: Luật Doanh nghiệp 2020, Nghị định 01/2021/NĐ-CP (Thành lập, vốn, quản trị công ty).
    2. `civil_law`: Bộ luật Dân sự 2015 (Giao dịch dân sự, hợp đồng vay, thuê mượn, bồi thường).
    3. `labor_law`: Bộ luật Lao động 2019 (Hợp đồng lao động, thử việc, chấm dứt, kỷ luật, BHXH).
    4. `commercial_law`: Luật Thương mại 2005 (Mua bán hàng hóa, chế tài phạt vi phạm, giải quyết tranh chấp).
    5. `ip_law`: Luật Sở hữu Trí tuệ (Bản quyền, nhãn hiệu thương hiệu).
  * `Router Agent` sẽ phân tích câu hỏi/văn bản thuộc lĩnh vực nào để định tuyến truy vấn đến đúng Vector Collection tương ứng $\rightarrow$ **Bảo toàn độ chính xác Ragas Precision > 85%**.

---

### 4. Phản biện Trọng tâm: "Các Tool có cần được Train liên tục để đưa ra kết quả tốt nhất không?"

Đây là câu hỏi xuất sắc chạm đến bản chất của **Kỹ thuật Học máy (Machine Learning) vs. Hệ thống Tác nhân Trí tuệ (Agentic Systems)**. Tôi xin phân tích đa chiều:

#### ❌ Tại sao trong ngành Luật (LegalTech), "Train lại mô hình liên tục" (Continual Model Fine-Tuning) là một Sai lầm Nguy hiểm (Anti-Pattern)?
1. **Hiện tượng Quên Lãng Thảm Khốc (Catastrophic Forgetting):**
   * Khi bạn fine-tune trọng số (weights) của một LLM lớn bằng tập dữ liệu luật mới, mô hình có xu hướng "quên" hoặc suy giảm năng lực suy luận logic, toán học và kỹ năng sinh code/định dạng JSON đã được huấn luyện trước đó.
2. **Nguy cơ Ảo giác Đóng băng (Frozen Hallucinations):**
   * Luật pháp Việt Nam thay đổi liên tục qua các kỳ họp Quốc hội, Nghị định và Thông tư.
   * Nếu nạp luật vào "trọng số mạng nơ-ron", kiến thức đó bị đóng băng tĩnh. Khi một điều luật bị sửa đổi/bãi bỏ, mô hình vẫn ghi nhớ điều luật cũ trong weights và tự tin đưa ra tư vấn sai pháp luật mà không có cách nào thu hồi kịp thời.
3. **Chi phí và Thời gian Không Khả thi:**
   * Việc huấn luyện lại mô hình (kể cả LoRA/QLoRA) đòi hỏi GPU đắt đỏ, kiểm thử hồi quy (regression testing) phức tạp và mất hàng giờ/ngày, không thể đáp ứng tính cập nhật tức thời của pháp luật.

#### ✅ Chuẩn mực Toàn cầu của AI Engineer: "LEARNING WITHOUT WEIGHT TRAINING" (Học liên tục không cần đổi trọng số)
Các hệ thống hàng đầu thế giới (*Harvey AI, Casetext CoCounsel, LexisNexis AI*) đều áp dụng kiến trúc **3 Tầng Tối ưu Liên tục** sau:

1. **Continual Knowledge Ingestion (Tự động hóa Cập nhật Tri thức RAG):**
   * Thay vì train model, hệ thống liên tục nạp văn bản mới vào **Vector Database & SQL Database**. Khi Quốc hội ban hành luật mới, chỉ cần 1 lệnh Ingestion là toàn bộ hệ thống cập nhật kiến thức mới ngay trong 5 giây mà không tốn chi phí train.
2. **DSPy & Dynamic Few-shot In-Context Learning (Tự học qua Mẫu ví dụ):**
   * Xây dựng một **Few-shot Bank (Ngân hàng Tình huống Chuẩn)**. Khi các luật sư hoặc người dùng đánh giá câu trả lời của AI là xuất sắc, trường hợp đó được tự động lưu vào Memory Store.
   * Lần sau khi gặp tình huống tương tự, Agent tự động bốc ví dụ đó vào Prompt (In-Context Learning) để mô hình làm theo. Mô hình ngày càng thông minh hơn mà không cần đổi một trọng số nào!
3. **Deterministic Logic Rules (Quy tắc Pháp lý Bất biến):**
   * Các quy định mang tính tuyệt đối (Ví dụ: mức phạt hợp đồng thương mại $\le 8\%$, thời hạn góp vốn $= 90$ ngày, độ tuổi đại diện pháp luật $\ge 18$) **BẮT BUỘC phải được cài đặt bằng Rule-based Deterministic Code (Python/Regex)**.
   * Tuyệt đối không giao việc này cho mô hình tự suy đoán theo xác suất, vì kể cả mô hình mạnh nhất thế giới (GPT-4o, Gemini 1.5 Pro) vẫn có xác suất hallucination nhỏ.

---

## 🎯 III. KẾT LUẬN & ĐỀ XUẤT LỘ TRÌNH CHO PHIÊN BẢN 1.2

Dựa trên các phân tích kỹ thuật nghiêm ngặt trên, bản nâng cấp tiếp theo sẽ được định danh là **Phiên bản 1.2 (Version 1.2 - The Legal Intelligence & Vulnerability Suite)** với 4 trụ cột kỹ thuật:

1. **Tool 1: Contract Vulnerability Scanner & Scorer:** Quét lỗ hổng hợp đồng, chấm điểm rủi ro (0-100) và gợi ý điều khoản thay thế chuẩn.
2. **Tool 2: In-Chat Generative UI:** Cho phép kích hoạt form tương tác và tải file ngay trong tin nhắn chat.
3. **Tool 3: Hierarchical Multi-Domain Legal RAG:** Mở rộng tri thức sang Bộ luật Dân sự 2015, Bộ luật Lao động 2019, Luật Thương mại 2005.
4. **Tool 4: Dynamic In-Context Learning & Memory Feedback:** Lưu vết các case thẩm định hợp đồng thành công để tự động tối ưu chất lượng tư vấn theo thời gian mà không gây ảo giác.

*Chi tiết thông số kỹ thuật được đặc tả đầy đủ tại file kế tiếp: [`requirements/requirements_version_1.2.md`](./requirements_version_1.2.md).*
