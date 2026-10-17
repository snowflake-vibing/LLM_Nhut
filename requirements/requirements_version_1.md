# 🎯 BỘ YÊU CẦU DỰ ÁN AI ENGINEER PHIÊN BẢN 1 (REQUIREMENTS VERSION 1)
### ⚖️ ĐỀ TÀI: LEGALTECH SME ASSISTANT (HỖ TRỢ PHÁP LÝ DOANH NGHIỆP VỪA & NHỎ)

## 📌 Tổng quan dự án
Tài liệu này tổng hợp toàn bộ các tiêu chí đánh giá, yêu cầu kỹ thuật và lộ trình xây dựng dự án môn học **AI Engineer**. Dự án hướng đến việc phát triển một ứng dụng tích hợp Trí tuệ nhân tạo tạo sinh (Generative AI / LLM) giải quyết bài toán thực tế trong doanh nghiệp, đáp ứng đầy đủ 7 tiêu chí chấm điểm từ giảng viên.

---

## 🎯 Bảng tiêu chí đánh giá & Yêu cầu chi tiết

| STT | Tiêu chí đánh giá | Trọng số | Mô tả chi tiết & Yêu cầu kỹ thuật |
| :--- | :--- | :---: | :--- |
| **1** | **Ứng dụng LLM trong doanh nghiệp** | **1.0 đ** | - Xác định rõ ràng bài toán kinh doanh (*Business Use-case*).<br>- Phân tích bài toán thực tế: Thực trạng & nỗi đau của doanh nghiệp (*Pain points*), giải pháp LLM mang lại giá trị gì so với cách làm truyền thống.<br>- Đối tượng người dùng mục tiêu và tính khả thi khi triển khai vào quy trình thực tế. |
| **2** | **Kỹ năng Prompting (Prompt Engineering)** | **2.0 đ** | - Thiết kế System Prompts chuyên sâu: Role, Task, Context, Constraints, Response Guidelines.<br>- Áp dụng các kỹ thuật prompting nâng cao:<br>  + **Few-shot Prompting**: Cung cấp các ví dụ mẫu chuẩn xác cho mô hình.<br>  + **Chain-of-Thought (CoT)**: Hướng dẫn mô hình tư duy, lập luận từng bước trước khi ra kết quả.<br>  + **Structured Output**: Ràng buộc định dạng đầu ra chuẩn JSON Schema để backend dễ dàng xử lý. |
| **3** | **Lập trình ứng dụng Cloud Server & Local Model** | **2.5 đ** | - Xây dựng ứng dụng hoàn chỉnh có giao diện người dùng (Frontend: Streamlit / Chainlit / Web App) và Backend (FastAPI / Python).<br>- **Cloud Server**: Kết nối và gọi các mô hình thương mại qua API (OpenAI GPT-4o, Google Gemini API, Anthropic Claude...).<br>- **Local Model**: Chạy mô hình mã nguồn mở trên máy nội bộ / server riêng (Ollama, vLLM, HuggingFace với Llama 3, Qwen 2.5, Mistral...).<br>- Cho phép chuyển đổi linh hoạt (*Model Switcher/Toggle*) giữa Cloud và Local tùy theo nhu cầu bảo mật và tài nguyên. |
| **4** | **Vector và RAG cơ bản, đọc từ CSDL** | **1.5 đ** | - **Retrieval-Augmented Generation (RAG)** pipeline hoàn chỉnh:<br>  + Document Loading & Chunking (cắt đoạn văn bản hợp lý).<br>  + Embedding Model (OpenAI text-embedding-3, BGE, Nomic...).<br>  + Vector Database: Lưu trữ và Semantic Search (ChromaDB, FAISS, Qdrant).<br>- **Tích hợp CSDL truyền thống (SQL/NoSQL)**: Đọc, truy vấn dữ liệu có cấu trúc (ví dụ: bảng sản phẩm, thông tin khách hàng, hóa đơn từ SQLite / PostgreSQL). |
| **5** | **AI Agents và Đa Tác Nhân (Multi-Agent)** | **1.5 đ** | - Xây dựng hệ thống Agent có khả năng suy luận và sử dụng công cụ (*Tool Calling / Function Calling*):<br>  + Tool tra cứu Vector DB (RAG).<br>  + Tool truy vấn CSDL (SQL Query Tool).<br>  + Tool tính toán hoặc gọi API ngoài.<br>- Triển khai mô hình **Đa tác nhân (Multi-Agent)** phối hợp với nhau (dùng LangGraph, CrewAI hoặc AutoGen):<br>  + *Router Agent*: Phân loại ý định người dùng.<br>  + *Specialized Agents*: Xử lý từng tác vụ chuyên biệt.<br>  + *Supervisor / Reviewer Agent*: Tổng hợp, rà soát kết quả. |
| **6** | **Đánh giá mô hình LLM (Evaluation)** | **1.0 đ** | - Xây dựng bộ dữ liệu kiểm thử (Evaluation Dataset / Benchmark: 20-50 test cases gồm Query, Context, Ground Truth).<br>- Sử dụng framework đánh giá tự động (Ragas, DeepEval, hoặc TruLens) với các chỉ số cốt lõi:<br>  + **Faithfulness**: Độ trung thực, không bị ảo giác so với context.<br>  + **Answer Relevance**: Câu trả lời sát đúng trọng tâm câu hỏi.<br>  + **Context Precision & Recall**: Mức độ chính xác của tài liệu RAG lấy ra.<br>- Báo cáo so sánh thực nghiệm hiệu năng giữa Cloud Model vs. Local Model (Latency, Token Cost, Accuracy). |
| **7** | **Bảo mật LLM (LLM Security & Guardrails)** | **0.5 đ** | - Phòng chống các lỗ hổng OWASP Top 10 for LLM:<br>  + **Prompt Injection & Jailbreak Defense**: Lọc đầu vào, ngăn chặn câu lệnh cố tình bẻ khóa system prompt.<br>  + **PII Redaction / Data Masking**: Che giấu/ẩn thông tin nhạy cảm của người dùng (email, số điện thoại, CCCD/CMND) trước khi gửi qua API bên ngoài.<br>  + **Output Moderation**: Kiểm duyệt đầu ra để tránh phản hồi thông tin độc hại hoặc rò rỉ dữ liệu mật. |

---

## 🛠️ Đề xuất Công nghệ & Kiến trúc (Tech Stack)

* **Ngôn ngữ:** Python 3.10+
* **Framework giao diện:** Streamlit / Chainlit / Next.js
* **Backend & API:** FastAPI / Pydantic
* **LLM Orchestration:** LangChain / LangGraph / CrewAI
* **Vector DB & Database:** ChromaDB / FAISS + SQLite / PostgreSQL
* **Local LLM Engine:** Ollama (Llama 3.1 / Qwen 2.5)
* **Cloud LLM Engine:** Google Gemini API / OpenAI API
* **Đánh giá (Eval):** Ragas / DeepEval
* **Bảo mật (Security):** NeMo Guardrails / PII Masking regex / Llama Guard

---

## 📅 Lộ trình thực hiện gợi ý

1. **Giai đoạn 1:** Khởi tạo kiến trúc dự án, thiết kế cơ sở dữ liệu và thu thập tài liệu nghiệp vụ.
2. **Giai đoạn 2:** Xây dựng module kết nối Cloud Model & Local Model (Ollama), cấu hình Prompt Template chuẩn.
3. **Giai đoạn 3:** Xây dựng pipeline RAG (Vector DB) kết hợp đọc dữ liệu CSDL.
4. **Giai đoạn 4:** Phát triển Multi-Agent Workflow (Router, Task Executor, Tool Calling).
5. **Giai đoạn 5:** Tích hợp lớp bảo mật Guardrails (chống Prompt Injection, ẩn thông tin PII).
6. **Giai đoạn 6:** Viết script benchmark tự động (Ragas) xuất biểu đồ đánh giá và hoàn thiện giao diện demo.
