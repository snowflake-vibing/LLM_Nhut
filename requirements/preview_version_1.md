# 📋 ĐÁNH GIÁ PHIÊN BẢN 1 & ĐỊNH HƯỚNG NÂNG CẤP (PREVIEW VERSION 1)
### ⚖️ DỰ ÁN: LEGALTECH SME ASSISTANT • AI ENGINEER PROJECT

---

## 📌 I. TỔNG HỢP Ý KIẾN ĐÁNH GIÁ CỦA NGƯỜI DÙNG (USER FEEDBACK)

Sau khi trải nghiệm Phiên bản 1 (Version 1.0) của hệ thống, người dùng đưa ra 4 nhận xét cốt lõi:

1. **Về tra cứu mã ngành & giấy phép:**
   * *Hiện trạng:* Dữ liệu đang lưu tĩnh trong SQLite cục bộ, chỉ tìm được một số ngành có sẵn.
   * *Kỳ vọng:* Muốn mở rộng tra cứu trên Internet hoặc CSDL Cloud quy mô lớn; khi tìm kiếm phải hiển thị toàn bộ các kết quả liên quan một cách đầy đủ.
2. **Về trợ lý pháp lý & trích dẫn luật:**
   * *Hiện trạng:* Trả lời câu hỏi thông thường và phạm vi đang tập trung ở Luật Doanh nghiệp 2020.
   * *Kỳ vọng:* Căn cứ pháp luật trích dẫn phải ghi rõ vị trí Điều, Khoản, trích dẫn nội dung nguyên văn và **đính kèm đường link website chính thức (như vanban.chinhphu.vn, thuvienphapluat.vn)** để người dùng tự kiểm chứng tính xác thực.
3. **Về tính năng PII Masking (Bảo mật thông tin cá nhân):**
   * *Băn khoăn:* Chưa hiểu rõ bản chất PII Masking hoạt động ra sao (người dùng nhập thông tin riêng tư thì chatbot có ẩn đi không và ẩn nhằm mục đích gì).
4. **Về chức năng tạo hồ sơ kê khai (Tính năng còn thiếu):**
   * *Nỗi đau thực tế:* Doanh nghiệp/chủ quán không biết cần những loại giấy tờ nào, trong từng giấy tờ cần điền những gì.
   * *Kỳ vọng:* AI cần có chức năng hỗ trợ tạo form kê khai, tự động soạn thảo và xuất ra các file hồ sơ pháp lý hoàn chỉnh (Giấy đề nghị, Điều lệ công ty, Danh sách thành viên...).

---

## 🔬 II. ĐÁNH GIÁ NGHIÊM TÚC DƯỚI GÓC ĐỘ KỸ THUẬT AI (AI ENGINEERING CRITIQUE)

Dưới góc nhìn của một Kỹ sư AI và bám sát **7 tiêu chí chấm điểm của giảng viên**, tôi xin đưa ra phân tích chuyên sâu cho từng điểm:

---

### 1. Phân tích: Tra cứu CSDL nội bộ vs. Tìm kiếm Web / Cloud DB
* **Góc nhìn Tiêu chí chấm điểm (Tiêu chí 4: 1.5đ):**
  * Giảng viên yêu cầu rõ: *"Vector và RAG cơ bản, đọc từ CSDL"*.
  * Nếu chúng ta bỏ CSDL nội bộ mà chỉ dùng Google Search / Web API, dự án sẽ **mất trắng điểm phần CSDL quan hệ SQL**. Giảng viên cần thấy sinh viên biết thiết kế Schema, lập chỉ mục, và xây dựng SQL Tools để LLM gọi hàm (Function Calling).
* **Đánh giá giải pháp:**
  * ❌ *Chỉ dùng CSDL nội bộ:* Bị giới hạn dữ liệu, nếu người dùng hỏi ngành nghề quá mới (Gamefi, Tín chỉ Carbon, AI SaaS...) sẽ không tìm thấy.
  * ❌ *Chỉ dùng Web Search:* Phụ thuộc mạng, dễ dính thông tin rác, tốc độ chậm và mất điểm tiêu chí SQL.
  * 🌟 **Giải pháp tối ưu: KIẾN TRÚC LAI (HYBRID RETRIEVAL)**
    * **Tuyến 1 (Primary):** Tra cứu bảng VSIC 2018 trong CSDL SQLite nội bộ (tốc độ < 10ms, chuẩn xác 100%).
    * **Tuyến 2 (Fallback / Web Search Tool):** Tích hợp thêm **Web Search Tool** (Tavily Search API hoặc DuckDuckGo / Thư Viện Pháp Luật). Khi CSDL nội bộ không có kết quả, Agent tự động kích hoạt Web Search để cào thông tin mới nhất từ cổng thông tin quốc gia.
    * **Hiển thị đầy đủ kết quả:** Thêm bộ lọc phân trang (Pagination) trên giao diện Streamlit để hiển thị toàn bộ 20-50 kết quả liên quan thay vì chỉ hiển thị vài dòng.

---

### 2. Phân tích: Trích dẫn Điều khoản luật & Link kiểm chứng
* **Đánh giá kỹ thuật:** Đây là góp ý **XUẤT SẮC NHẤT**, chạm đúng vào điểm cốt lõi của bài toán RAG trong lĩnh vực Pháp lý (LegalTech).
* **Ý nghĩa học thuật:**
  * Trong luật pháp, ảo giác (hallucination) là cấm kỵ. Nếu AI trích dẫn sai số Điều hoặc bịa đặt văn bản luật, hệ thống hoàn toàn vô dụng.
  * Việc hiển thị: `[Tên Văn bản] -> [Điều ...] -> [Khoản ...] -> [Đoạn trích nguyên văn] -> [🔗 Link xem trực tiếp trên Cổng TT Chính phủ]` sẽ giúp đồ án đạt điểm **tuyệt đối ở Tiêu chí 4 (RAG) và Tiêu chí 6 (Ragas Faithfulness 100%)**.
* **Giải pháp hiện thực hóa:**
  * Nâng cấp metadata của từng Chunk trong Vector Store:
    ```json
    {
      "source_law": "Luật Doanh nghiệp 2020 (Số 59/2020/QH14)",
      "article": "Điều 74",
      "clause": "Khoản 1",
      "verbatim_text": "Công ty trách nhiệm hữu hạn một thành viên là doanh nghiệp do một tổ chức hoặc một cá nhân làm chủ sở hữu...",
      "verify_url": "https://vanban.chinhphu.vn/?pageid=27160&docid=200676"
    }
    ```
  * Trên UI Streamlit, thiết kế mỗi trích dẫn thành một **Thẻ Căn cứ Pháp lý (Citation Card)** có nút bấm nhảy thẳng đến trang văn bản của Chính phủ để kiểm chứng.

---

### 3. Phân tích & Giải thích: Bản chất của PII Masking
* **Người dùng băn khoăn:** *"Có phải ai đó nhập thông tin riêng tư thì chatbot ẩn đi không?"*
* **Bản chất kỹ thuật (Tiêu chí 7: Bảo mật LLM):**
  * Khi bạn chat với chatbot dùng Cloud (như Gemini của Google hay GPT-4o của OpenAI), toàn bộ câu chữ bạn gõ sẽ được truyền qua đường truyền Internet đến máy chủ của Google đặt tại Mỹ.
  * Nếu người dùng gõ:  
    `"Tôi là Nguyễn Văn Nhựt, CCCD 079201004567, SĐT 0901234567, vốn 5 tỷ muốn lập công ty."`
  * $\rightarrow$ **Nguy cơ:** Dữ liệu cá nhân nhạy cảm này có thể bị rò rỉ, bị hacker bắt gói tin hoặc bị phía bên thứ ba lưu log đào tạo AI trái phép, vi phạm Nghị định 13/2023/NĐ-CP về Bảo vệ dữ liệu cá nhân của Việt Nam.
* **Cơ chế PII Masking bảo vệ như thế nào?**
  1. **Bước 1 (Che mắt Google):** Ngay trên máy tính của bạn (Local), trước khi gửi đi, hàm Regex tự động che dấu:  
     `"Tôi là Nguyễn Văn Nhựt, CCCD [MASKED_CCCD_1], SĐT [MASKED_PHONE_1], vốn 5 tỷ..."`
  2. **Bước 2 (AI xử lý):** Google nhận được bản đã che dấu. Google vẫn hiểu `[MASKED_CCCD_1]` là mã căn cước để soạn hợp đồng, nhưng Google **hoàn toàn không biết số thật là gì**.
  3. **Bước 3 (Khôi phục cho người dùng):** Khi Google trả lời xong và gửi kết quả về máy bạn, hệ thống cục bộ tự động thay ngược lại số thật:  
     `"Hồ sơ thành lập cho ông Nguyễn Văn Nhựt (CCCD 079201004567)..."`
  * 👉 **Tóm lại:** Bạn (người dùng cuối) vẫn đọc được đầy đủ thông tin của mình trên màn hình, nhưng **các công ty AI máy chủ bên ngoài thì bị bịt mắt hoàn toàn, không thể thu thập lén dữ liệu của bạn!**

---

### 4. Phân tích: Tính năng Tạo Form & Xuất File Kê khai Pháp lý
* **Đánh giá chuyên môn:** Đây chính là **Tính năng Sát thủ (Killer Feature)**. Nếu làm được phần này, dự án của bạn sẽ vượt trội hoàn toàn so với các đồ án AI thông thường (thường chỉ dừng lại ở Chatbot hỏi đáp).
* **Khả năng khớp với 7 Tiêu chí:**
  * **Tiêu chí 1 (Doanh nghiệp):** Mang lại giá trị chuyển đổi số trực tiếp. Thay vì trả 2 - 3 triệu tiền dịch vụ thành lập công ty, chủ doanh nghiệp chỉ cần bấm nút là có ngay bộ hồ sơ hoàn chỉnh.
  * **Tiêu chí 2 (Prompting):** Áp dụng kỹ thuật **Structured Output (JSON Schema)** để trích xuất toàn bộ thông tin người dùng điền vào biểu mẫu chuẩn.
  * **Tiêu chí 5 (AI Agents):** Bổ sung thêm **Form Generator Agent (Tác nhân Soạn thảo)**.
* **Quy trình triển khai:**
  1. **Interactive Form (Giao diện nhập liệu):** Người dùng nhập: Tên dự kiến, Địa chỉ, Vốn điều lệ, Thông tin người đại diện.
  2. **AI Drafting Engine:** AI tự động kiểm tra tính hợp lệ (Tên có bị cấm không? Vốn có phù hợp ngành nghề không?) và điền vào các mẫu biểu theo Nghị định 01/2021/NĐ-CP:
     * *Phụ lục I-2:* Giấy đề nghị đăng ký công ty TNHH một thành viên.
     * *Phụ lục I-3:* Giấy đề nghị đăng ký công ty TNHH hai thành viên trở lên.
     * *Điều lệ mẫu công ty.*
  3. **File Export:** Cho phép người dùng bấm nút **Tải về file Word (.docx) hoặc PDF** chuẩn mẫu hành chính nhà nước.

---

## 🚀 III. KẾ HOẠCH NÂNG CẤP PHIÊN BẢN 1.1 (ROADMAP VERSION 1.1)

| STT | Hạng mục nâng cấp | Mô tả kỹ thuật | Tiêu chí củng cố |
| :---: | :--- | :--- | :---: |
| **1** | **Citation kèm Link Kiểm chứng** | Thêm URL chính thức (`vanban.chinhphu.vn`, `thuvienphapluat.vn`) vào metadata của Vector DB. Render thẻ trích dẫn nguyên văn Điều/Khoản kèm link kiểm chứng. | **Tiêu chí 4 & 6** *(RAG & Eval)* |
| **2** | **Bộ Sinh Hồ sơ Doanh nghiệp (Document Generator)** | Xây dựng thêm Tab 5: Điền form thông tin $\rightarrow$ AI soạn thảo Điều lệ & Giấy đề nghị đăng ký $\rightarrow$ Xuất file `.docx` / `.pdf` tải về. | **Tiêu chí 1, 2 & 5** *(Business & Agents)* |
| **3** | **Tra cứu Hybrid (CSDL + Web Search)** | Kết hợp tìm kiếm CSDL SQLite sẵn có và Tool tìm kiếm mở rộng trên Web đối với các ngành nghề mới, hỗ trợ xem toàn bộ kết quả phân trang. | **Tiêu chí 4 & 5** *(Database & Tools)* |
| **4** | **Trực quan hóa luồng PII Masking** | Bổ sung visual badge giải thích rõ cho người dùng cách dữ liệu cá nhân được mã hóa trước khi bay ra nước ngoài. | **Tiêu chí 7** *(Bảo mật LLM)* |

---

## 🎯 IV. KẾT LUẬN
Bản đánh giá của bạn rất sát với nhu cầu thực tế của người dùng khởi nghiệp. Bằng cách kết hợp giữa việc **bảo tồn trọn vẹn 7 tiêu chí học thuật của giảng viên** và **bổ sung thêm 2 tính năng thực chiến (Link kiểm chứng & Tự động xuất hồ sơ văn bản)**, dự án sẽ đạt mức độ hoàn thiện xuất sắc ở cấp độ đồ án Tốt nghiệp / Sản phẩm ứng dụng doanh nghiệp thực tế.
