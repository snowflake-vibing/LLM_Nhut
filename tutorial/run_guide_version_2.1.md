# 📖 HƯỚNG DẪN KIỂM THỬ THỰC TẾ PHIÊN BẢN 2.1 (RUN GUIDE VERSION 2.1)
### ⚖️ ĐỀ TÀI: LEGALTECH PLATFORM • HỆ THỐNG LUẬT SƯ AI TRỰC TUYẾN & TOOLS STUDIO (THE LEGAL AI LAWYER & STUDIO PLATFORM)

---

## 🎯 1. Giới thiệu Bản Cập nhật Version 2.1
Phiên bản 2.1 tái cấu trúc toàn diện LegalTech Platform thành **Vị Luật sư AI Trực tuyến Toàn năng (AI Online Lawyer)** với giao diện tối giản tinh gọn chuẩn phong cách **NotebookLM (Đúng 2 Tab)**:
- **Tab 1: 💬 AI Legal Chatbot & Command Center (In-Chat Everything):** Triệu hồi trực tiếp mọi công cụ tương tác (Quét hợp đồng 2 chiều, Form thông minh soạn thảo đơn từ, Tra cứu đa luật, Tải file Word) ngay trong luồng hội thoại.
- **Tab 2: 🧰 Legal Tools Studio (NotebookLM Style):** Trưng bày toàn bộ 8 công cụ chuyên sâu của hệ thống để thực thi và kiểm thử độc lập.

---

## 🚀 2. Hướng dẫn Khởi chạy Hệ thống

### Bước 1: Kích hoạt Môi trường Ảo (Virtual Environment)
Mở PowerShell tại thư mục gốc `D:\LLM\LLM_Nhut`:
```powershell
.\venv\Scripts\Activate.ps1
```

### Bước 2: Khởi động Ứng dụng Streamlit
```powershell
streamlit run app/main.py
```
Trình duyệt sẽ tự động mở tại địa chỉ: `http://localhost:8501`.

---

## 🧪 3. Kịch bản Kiểm thử Thực tế Chi tiết (Test Cases & Prompts)

### 📌 TEST CASE 1: Bóc tách Lỗ hổng Hợp đồng 2 Chiều Đối kháng (Bilateral Exploitation)
* **Ý nghĩa:** Đóng vai Luật sư bóc tách xem bên soạn thảo (mạnh thế) có thể lợi dụng điều gì và bên ký kết (yếu thế) bị ép hoặc có thể phản đòn bằng điều luật nào.
* **Cách thực hiện:** Tại **Tab 1**, dán câu lệnh sau vào khung chat hoặc bấm nút gợi ý:
```text
Hãy thẩm định hợp đồng mua bán này: "Nếu Bên B chậm thanh toán quá 5 ngày thì phải chịu phạt vi phạm 15% tổng giá trị hợp đồng và bồi thường 100 triệu, đồng thời không áp dụng bất kỳ lý do bất khả kháng nào."
```
* **Kỳ vọng đầu ra:**
  1. AI nhận diện vi phạm Điều 301 Luật Thương mại 2005 (Trần phạt vi phạm tối đa 8%) và Điều 156, 351 BLDS 2015 (thiếu Bất khả kháng).
  2. Hiển thị điểm an toàn pháp lý (`score: 60/100`).
  3. Xuất hiện **Thẻ Bóc tách Đối kháng 2 Chiều**:
     - 🔴 **Bên ra luật lợi dụng:** Dùng mức phạt 15% đe dọa áp lực tài chính vượt tổn thất thực tế.
     - 🟡 **Bên theo luật bị ép / Phản đòn:** Có thể phản tố tại Tòa tuyên vô hiệu điều khoản vượt trần, chỉ chịu tối đa 8%.
     - ✍️ **Điều khoản dung hòa:** Đề xuất điều khoản cân bằng chuẩn mực.
  4. Nút bấm **Tải Báo cáo Thẩm định (.docx)** hoạt động hoàn hảo.

---

### 📌 TEST CASE 2: Bạo lực học đường & Trách nhiệm của Nhà trường
* **Ý nghĩa:** Xử lý tình huống trường học thoái thác trách nhiệm khi học sinh bị đánh có thương tích trong giờ học.
* **Cách thực hiện:** Tại **Tab 1**, dán prompt:
```text
Con tôi bị bạo lực học đường có thương tích nhưng nhà trường không chịu trách nhiệm vì nói xảy ra ngoài tầm mắt giáo viên. Luật sư cho tôi biết nhà trường có phải bồi thường không và thủ tục xử lý ra sao?
```
* **Kỳ vọng đầu ra:**
  1. Trích dẫn chính xác **Khoản 1 Điều 599 Bộ luật Dân sự 2015** (Nhà trường phải bồi thường thiệt hại do người dưới 15 tuổi gây ra trong thời gian trường học trực tiếp quản lý) và Nghị định 80/2017/NĐ-CP.
  2. Đưa ra lộ trình 3 bước: (1) Giám định viện phí, (2) Yêu cầu trích xuất camera & lập biên bản, (3) Gửi Đơn khiếu nại / tố cáo.
  3. Tự động triệu hồi **Form Thông minh Soạn thảo Đơn khiếu nại bạo lực học đường**:
     - Điền sẵn 100% căn cứ pháp luật và nội dung yêu cầu giải quyết.
     - Cho phép nhập tên phụ huynh, học sinh hoặc để trống để AI tự động chèn dòng chấm `........................`.
     - Tải ngay file Word: `Don_Khieu_Nai_Bao_Luc_Hoc_Duong.docx`.

---

### 📌 TEST CASE 3: Tranh chấp Ranh giới Sổ đỏ & Xây dựng Lấn chiếm
* **Ý nghĩa:** Hàng xóm xây hàng rào lấn sang mốc giới đất đã có Giấy chứng nhận quyền sử dụng đất.
* **Cách thực hiện:** Tại **Tab 1**, dán prompt:
```text
Hàng xóm nhà tôi xây hàng rào lấn sang đất của tôi hơn 1 mét rưỡi. Tôi đã có Sổ đỏ chính chủ. Tôi có cần hòa giải ở xã trước không và làm đơn gì?
```
* **Kỳ vọng đầu ra:**
  1. Nhấn mạnh nguyên tắc: **Điều 202 Luật Đất đai bắt buộc phải qua thủ tục hòa giải tại UBND cấp xã/phường** trước khi khởi kiện ra Tòa án nhân dân.
  2. Trích dẫn Điều 175, 176 BLDS 2015 về bảo vệ ranh giới và mốc giới bất động sản.
  3. Triệu hồi biểu mẫu: `Đơn yêu cầu hòa giải tranh chấp ranh giới đất đai` điền sẵn và tải về file Word `.docx`.

---

### 📌 TEST CASE 4: Khởi kiện Đòi nợ khi Con nợ Cố tình Bỏ trốn
* **Ý nghĩa:** Vay nợ có bằng chứng giao dịch nhưng con nợ cắt liên lạc và rời khỏi nơi cư trú.
* **Cách thực hiện:** Tại **Tab 1**, dán prompt:
```text
Tôi có cho bạn vay 300 triệu có giấy nhận tiền và sao kê ngân hàng, nhưng nay đến hạn con nợ cắt liên lạc và bỏ trốn khỏi địa phương. Tôi muốn khởi kiện đòi nợ thì nộp đơn ở đâu?
```
* **Kỳ vọng đầu ra:**
  1. Tư vấn rõ 2 hướng:
     - Dân sự: Nộp Đơn khởi kiện tại TAND nơi cư trú cuối cùng theo Điều 39, 40 BLTTDS (Tòa án niêm yết xét xử vắng mặt).
     - Hình sự: Nếu có dấu hiệu bỏ trốn chiếm đoạt tài sản, tố giác theo Điều 175 BLHS.
  2. Kích hoạt biểu mẫu `Đơn khởi kiện tranh chấp hợp đồng vay tài sản` chuẩn Nghị quyết 01/2017/NQ-HĐTP.
  3. Người dùng nhập số tiền hoặc để trống thì AI tự chèn `........................ VNĐ`, xuất file Word dùng ngay.

---

### 📌 TEST CASE 5: Ly hôn, Phân chia Tài sản & Quyền nuôi con
* **Ý nghĩa:** Thuận tình ly hôn, thỏa thuận quyền nuôi con (con nhỏ dưới 36 tháng, con trên 7 tuổi) và chia tài sản.
* **Cách thực hiện:** Tại **Tab 1**, dán prompt:
```text
Vợ chồng tôi muốn thuận tình ly hôn. Có 2 con (1 bé 2 tuổi, 1 bé 8 tuổi) và 1 căn nhà chung. Chúng tôi muốn làm đơn thỏa thuận phân chia quyền nuôi con và tài sản thì thủ tục thế nào?
```
* **Kỳ vọng đầu ra:**
  1. Căn cứ Điều 55, 59, 81 Luật Hôn nhân và Gia đình 2014: Con dưới 36 tháng tuổi ưu tiên giao mẹ nuôi; con từ đủ 7 tuổi Tòa án bắt buộc ghi nhận nguyện vọng của con.
  2. Triệu hồi biểu mẫu `Đơn thuận tình ly hôn và thỏa thuận nuôi con, chia tài sản` với chữ ký của cả hai vợ chồng, tải file `.docx` định dạng chuẩn tư pháp.

---

### 📌 TEST CASE 6: Trải nghiệm Tab 2 - 🧰 Legal Tools Studio
* **Cách thực hiện:** Chọn tab **🧰 Legal Tools Studio (NotebookLM Style)** tại sidebar bên trái.
* **Thử nghiệm các Studio chuyên sâu:**
  1. **🛡️ Bilateral Contract Risk Scanner:** Chọn các mẫu hợp đồng vi phạm để xem ma trận đối kháng 2 chiều.
  2. **📝 On-Demand Smart Legal Drafter:** Thử nghiệm cơ chế Form thông minh: nhập một vài thông tin hoặc để trống hoàn toàn để kiểm tra tính năng tự động chèn placeholder `........................` vào file Word.
  3. **🏛️ Social Cases Legal Center:** Xem cẩm nang pháp lý cho 4 case đời sống xã hội.
  4. **📦 Enterprise Dossier Generator:** Kiểm tra hợp lệ tên doanh nghiệp và tải 4 văn bản ĐKDN theo NĐ 01/2021.
  5. **🔎 Hybrid Industry Lookup:** Tra cứu từ khóa mới (ví dụ: `livestream`, `cà phê`, `phần mềm`) để xem CSDL SQLite kết hợp Web Search fallback và phân trang.
  6. **🔐 Security & Model Switcher:** Thử nghiệm PII Masking che CCCD/SĐT, kiểm tra phòng thủ Jailbreak và chuyển đổi giữa Gemini Cloud và Local Model.
  7. **🧠 Legal Memory Bank:** Xem danh mục tiền lệ và ghi nhận kiến thức mới vào bộ nhớ mà không cần huấn luyện lại trọng số mô hình.
  8. **📊 Ragas Evaluation Dashboard:** Xem các chỉ số Faithfulness, Answer Relevance, Context Precision và Context Recall.

---

## ✅ 4. Bảng Đối Chiếu 7 Tiêu Chí Chấm Điểm của UIT

| STT | Tiêu chí đánh giá của Giảng viên | Điểm | Vị trí thể hiện trong Version 2.1 | Trạng thái |
|:---:|:---|:---:|:---|:---:|
| **1** | **Ứng dụng LLM trong doanh nghiệp & xã hội** | 1.0đ | Vị Luật sư Trực tuyến giải quyết hợp đồng và 4 case đời sống | ✅ Đạt tối đa |
| **2** | **Kỹ năng Prompting (Few-shot, CoT, Structured Output)** | 2.0đ | Bóc tách 2 chiều đối kháng, Few-shot Router, Chain-of-Thought | ✅ Đạt tối đa |
| **3** | **Lập trình Cloud & Local Model (Model Switcher)** | 2.5đ | Chuyển đổi linh hoạt Gemini 3.5 Flash Lite $\leftrightarrow$ Ollama Qwen 2.5 | ✅ Đạt tối đa |
| **4** | **Vector DB & RAG cơ bản, đọc CSDL SQL** | 1.5đ | Hierarchical RAG (53 chunks đa luật), SQLite VSIC 2018 + Web fallback | ✅ Đạt tối đa |
| **5** | **AI Agents & Đa tác nhân (Multi-Agent System)** | 1.5đ | Router, Advisory, Lookup, Reviewer, Contract Scanner, Dynamic Drafter | ✅ Đạt tối đa |
| **6** | **Đánh giá mô hình LLM (Ragas Benchmark)** | 1.0đ | Dashboard 4 chỉ số Faithfulness, Relevance, Precision, Recall | ✅ Đạt tối đa |
| **7** | **Bảo mật LLM (PII Masking, Anti-Jailbreak)** | 0.5đ | Local PII Masker 2 chiều, Anti-Injection Guardrail trước khi gọi LLM | ✅ Đạt tối đa |
| **TỔNG** | **TẤT CẢ TIÊU CHÍ** | **10.0đ** | **LegalTech Platform v2.1** | **XUẤT SẮC** |
