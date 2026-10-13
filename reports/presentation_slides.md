# 🎤 SLIDE THUYẾT TRÌNH ĐỒ ÁN AI ENGINEER

## LEGALTECH SME ASSISTANT
**Trợ lý AI Hỗ trợ Tư vấn & Tự động Hóa Thủ tục Pháp lý cho Doanh nghiệp Vừa và Nhỏ**

---

### Slide 1: Trang tiêu đề
* **Tên đề tài:** LegalTech SME Assistant
* **Sinh viên:** snowflake-vibing (MSSV: 24520496)
* **Trường:** Đại học Công nghệ Thông tin - ĐHQG-HCM (UIT)
* **Giảng viên hướng dẫn:** Giảng viên phụ trách môn AI Engineer

---

### Slide 2: Đặt vấn đề & Nỗi đau Doanh nghiệp (Business Case - 1.0đ)
* Hơn 5 triệu hộ kinh doanh & SMEs đối mặt với "rừng luật" phức tạp khi khởi nghiệp.
* Chi phí tư vấn luật sư ban đầu vượt quá ngân sách.
* Rủi ro bị phạt hoặc đình chỉ do thiếu giấy phép con (ATVSTP, PCCC, giấy phép rượu...).
* **Mục tiêu:** Xây dựng Trợ lý AI định hướng loại hình doanh nghiệp, tra cứu mã ngành VSIC và hướng dẫn thủ tục tự động 24/7.

---

### Slide 3: Kiến trúc Tổng thể Hệ thống
* **Frontend:** Streamlit đa chức năng (Chatbot, DB Explorer, Guardrails Monitor, Eval Dashboard).
* **Security Layer:** PII Masking + Prompt Injection Defense.
* **Multi-Agent Orchestrator:** LangGraph điều phối 4 Agents chuyên trách.
* **Knowledge & Data:** ChromaDB (Văn bản luật) + SQLite (Mã ngành VSIC 2018).
* **LLM Engine:** Hybrid Switcher (Cloud Gemini 1.5 Flash & Local Ollama Llama 3).

---

### Slide 4: Kỹ năng Prompt Engineering Nâng cao (2.0đ)
* **System Prompting:** Phân tách rõ ràng Role, Task, Context, Constraints và Output format.
* **Few-shot Prompting:** Mẫu trích xuất ý định và thông tin kinh doanh chuẩn xác.
* **Chain-of-Thought (CoT):** Ép mô hình tư duy 5 bước lập luận trước khi đưa ra kết luận.
* **Structured Output:** Chuẩn hóa đầu ra dạng JSON Schema với Pydantic.

---

### Slide 5: Triển khai Cloud Server & Local Model (2.5đ)
* **Cloud API:** Tích hợp Google Gemini API qua REST và LangChain (Free Tier, tốc độ cao ~0.8s).
* **Local Model:** Chạy Ollama on-premise với Qwen 2.5 / Llama 3 (Offline 100%, bảo mật tuyệt đối).
* **Model Factory Switcher:** Chuyển đổi linh hoạt runtime + cơ chế Auto-fallback tự động.

---

### Slide 6: Vector Database & RAG Pipeline (1.5đ - P1)
* **Dữ liệu nguồn:** Luật Doanh nghiệp 2020, Nghị định 01/2021/NĐ-CP, Nghị định 39/2018/NĐ-CP.
* **Article-level Chunking:** Tách đoạn theo từng Điều / Khoản để giữ nguyên vẹn ngữ cảnh.
* **Semantic Search:** Tính toán Cosine Similarity kết hợp keyword bonus.
* **Citation:** Tự động trích dẫn chính xác: `[Luật Doanh nghiệp 2020 - Điều 74]`.

---

### Slide 7: Cơ sở Dữ liệu Quan hệ SQLite & SQL Tools (1.5đ - P2)
* **CSDL `sme_legal.db`:**
  * Bảng `industry_codes`: Danh mục mã ngành VSIC 2018 và điều kiện kinh doanh.
  * Bảng `license_requirements`: Điều kiện cấp giấy phép con, lệ phí và thời gian xử lý.
  * Bảng `registration_checklist`: Các bước nộp hồ sơ theo từng loại hình.
* **SQL Tool Calling:** Cho phép Agent tự động truy vấn dữ liệu chuẩn xác 100%.

---

### Slide 8: Hệ thống Đa Tác Nhân (Multi-Agent Workflow - 1.5đ)
* **Legal Router Agent:** Phân loại ý định người dùng.
* **Entity Advisory Agent:** So sánh và tư vấn loại hình công ty phù hợp (kết hợp RAG).
* **Industry Lookup Agent:** Tra cứu mã ngành và giấy phép con (kết hợp SQL).
* **Document Reviewer Agent:** Xây dựng checklist hành động từng bước.

---

### Slide 9: Đánh giá Mô hình & Ragas Benchmark (1.0đ)
* **Tập dữ liệu kiểm thử:** 10 Benchmark test cases thực tế.
* **Kết quả đo lường Ragas:**
  * **Faithfulness (Độ trung thực, không bịa luật):** `95.0%`
  * **Context Precision (Độ chính xác tài liệu):** `74.9%`
  * **Context Recall (Độ bao phủ tri thức):** `70.8%`
  * **Answer Relevance:** `53.6%`
  * **Overall Score:** `73.6%`

---

### Slide 10: An toàn Bảo mật LLM (Security & Guardrails - 0.5đ)
* **PII Masking:** Tự động che giấu CCCD (12 số), SĐT, Email trước khi gửi ra Cloud.
* **Anti-Injection:** Ngăn chặn bẻ khóa system prompt và lệnh jailbreak.
* **Từ chối Vi phạm:** Tuân thủ Điều 16 Luật Doanh nghiệp, chặn các câu hỏi trốn thuế, rửa tiền.
* **Legal Disclaimer:** Tự động đính kèm khuyến cáo pháp lý chuẩn mực.

---

### Slide 11: Demo Sản phẩm Giao diện Streamlit
* Tab 1: Chatbot tư vấn tương tác trực tiếp, trích dẫn nguồn luật.
* Tab 2: Tra cứu CSDL mã ngành kinh tế VSIC trực quan.
* Tab 3: Bảng điều khiển thử nghiệm PII Masking và phòng thủ Jailbreak.
* Tab 4: Dashboard trực quan hóa biểu đồ điểm số Ragas Benchmark.

---

### Slide 12: Tổng kết & Điểm nổi bật Đồ án
* Hoàn thành trọn vẹn cả 7 tiêu chí chấm điểm của giảng viên.
* Chi phí triển khai 0 VNĐ (sử dụng Gemini Free Tier và Ollama Open-source).
* Mã nguồn module hóa sạch sẽ, có unit test và đẩy đầy đủ lên GitHub.
* **Q&A:** Cảm ơn thầy cô và các bạn đã lắng nghe!
