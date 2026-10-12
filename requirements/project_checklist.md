# 📋 CHECKLIST CÁC OUTPUT BẮT BUỘC CHO DỰ ÁN (PROJECT DELIVERABLES)

Checklist này tổng hợp toàn bộ các **Sản phẩm bàn giao (Deliverables / Outputs)** cụ thể cần có để nghiệm thu dự án **LegalTech SME Assistant**, đảm bảo đạt điểm tối đa (10/10) theo 7 tiêu chí của giảng viên.

---

## 🧩 PHẦN 1: OUTPUT MÃ NGUỒN (SOURCE CODE & MODULES)

### 1.1. Module Mô hình Đám mây & Nội bộ (Cloud & Local LLM Provider - 2.5đ)
- [ ] **`src/llm_providers/cloud_provider.py`**: Tích hợp Google Gemini API (hoặc OpenAI API) qua SDK/LangChain.
- [ ] **`src/llm_providers/local_provider.py`**: Kết nối Ollama cục bộ (Llama 3.1 / Qwen 2.5) qua API `http://localhost:11434`.
- [ ] **`src/llm_providers/model_factory.py`**: Cơ chế Factory/Switcher cho phép chuyển đổi tức thì giữa Cloud và Local bằng cấu hình hoặc nút gạt trên UI.

### 1.2. Kỹ năng Prompting (Prompt Engineering - 2.0đ)
- [ ] **`src/prompts/system_prompts.py`**: Bộ System Prompts hoàn chỉnh (đầy đủ Role, Context, Constraint, Tone of Voice).
- [ ] **`src/prompts/few_shot_templates.py`**: Prompt mẫu trích xuất ý định và thông tin pháp lý từ câu hỏi của người dùng (Few-shot learning).
- [ ] **`src/prompts/cot_reasoning.py`**: Prompt suy luận từng bước (Chain-of-Thought) phân tích loại hình doanh nghiệp phù hợp.
- [ ] **`src/prompts/schemas.py`**: Pydantic Schema định nghĩa chuẩn đầu ra dạng JSON (Structured Output) cho hồ sơ thành lập doanh nghiệp.

### 1.3. Module Vector DB & RAG (1.5đ - Phần 1)
- [ ] **`src/rag/ingestion.py`**: Script đọc file văn bản pháp luật PDF, chia đoạn (*chunking*) tối ưu theo Điều/Khoản.
- [ ] **`src/rag/embeddings.py`**: Module tạo vector nhúng (Embedding model hỗ trợ tiếng Việt tốt: BAAI/bge, Nomic, text-embedding-3).
- [ ] **`src/rag/vector_store.py`**: Tích hợp ChromaDB lưu trữ vector và thực hiện truy vấn tìm kiếm tương đồng ngữ nghĩa (*Semantic Search*).
- [ ] **`src/rag/retriever.py`**: Bộ trích xuất ngữ cảnh RAG kèm cơ chế trích dẫn nguồn luật chính xác (tên Luật, số Điều, Khoản).

### 1.4. Module Đọc & Truy vấn CSDL (Database Integration - 1.5đ - Phần 2)
- [ ] **`data/database/sme_legal.db`**: Cơ sở dữ liệu SQLite chứa:
  - Bảng `industry_codes` (Hệ thống ngành kinh tế Việt Nam - VSIC 2018: Mã ngành, Tên ngành, Ngành nghề có điều kiện).
  - Bảng `license_requirements` (Danh mục giấy phép con: ATVSTP, PCCC, giấy phép môi trường...).
  - Bảng `registration_checklist` (Tiến độ và các bước làm hồ sơ).
- [ ] **`src/database/db_manager.py`**: Kết nối và quản lý truy vấn CSDL.
- [ ] **`src/database/sql_tools.py`**: Cung cấp công cụ Tool Calling cho Agent tự động sinh câu lệnh SQL tra cứu mã ngành.

### 1.5. Module AI Agents & Đa Tác Nhân (Multi-Agent - 1.5đ)
- [ ] **`src/agents/router_agent.py`**: Agent phân loại câu hỏi (Tư vấn mô hình DN, Tra cứu mã ngành, Hỏi thủ tục, hay Kiểm tra hồ sơ).
- [ ] **`src/agents/advisory_agent.py`**: Agent phân tích ưu/nhược điểm các mô hình (TNHH 1TV, TNHH 2TV+, Cổ phần, Hộ cá thể).
- [ ] **`src/agents/lookup_agent.py`**: Agent gọi Tool CSDL và RAG tra cứu mã ngành và giấy phép con tương ứng.
- [ ] **`src/agents/reviewer_agent.py`**: Agent kiểm duyệt và tổng hợp checklist hồ sơ pháp lý hoàn chỉnh cho người dùng.
- [ ] **`src/agents/graph.py`**: Điều phối luồng làm việc giữa các agent bằng **LangGraph** (StateGraph, Conditional Edges).

### 1.6. Module Bảo mật LLM (Security & Guardrails - 0.5đ)
- [ ] **`src/security/pii_masking.py`**: Lọc và che dấu dữ liệu nhạy cảm (CCCD/CMND, Số điện thoại, Địa chỉ nhà, Email) trước khi gửi qua API.
- [ ] **`src/security/prompt_injection_guard.py`**: Nhận diện và chặn đứng các prompt cố tình jailbreak, bẻ khóa hoặc hỏi cách trốn thuế, lách luật.
- [ ] **`src/security/output_moderation.py`**: Kiểm duyệt đầu ra, từ chối đưa ra lời khuyên pháp lý sai trái hoặc mang tính phỉ báng.

### 1.7. Module Đánh giá Mô hình (LLM Evaluation - 1.0đ)
- [ ] **`data/evaluation/benchmark_dataset.json`**: Tập dữ liệu kiểm thử chuẩn gồm 25-30 câu hỏi thực tế (Question, Ground Truth, Expected Context).
- [ ] **`src/evaluation/ragas_evaluator.py`**: Script tự động chạy benchmark bằng framework **Ragas** đo 4 chỉ số:
  - *Faithfulness* (Độ trung thực, không bịa luật).
  - *Answer Relevance* (Mức độ liên quan của câu trả lời).
  - *Context Precision* (Độ chính xác của văn bản luật trích xuất).
  - *Context Recall* (Độ bao phủ của tài liệu trích xuất).
- [ ] **`src/evaluation/model_comparison.py`**: Script so sánh thực nghiệm giữa Local Model (Ollama) và Cloud Model (Gemini): Thời gian phản hồi (Latency), Tokens/s, Điểm số chính xác.

### 1.8. Giao diện Người dùng (User Interface)
- [ ] **`app/main.py`**: Ứng dụng Streamlit hoàn chỉnh gồm:
  - Tab 1: **Trò chuyện Trợ lý Pháp lý (Chatbot AI)** - Hỗ trợ streaming text, trích dẫn nguồn luật.
  - Tab 2: **Tra cứu Mã ngành & Giấy phép con (Database Explorer)** - Tìm kiếm trực tiếp trên CSDL VSIC.
  - Tab 3: **Trình chuyển đổi Model (Model Switcher & Security Monitor)** - Chọn Cloud/Local và xem nhật ký lọc PII.
  - Tab 4: **Bảng điều khiển Đánh giá (Evaluation Dashboard)** - Biểu đồ trực quan hóa kết quả Ragas Benchmark.

---

## 📚 PHẦN 2: OUTPUT DỮ LIỆU & TÀI NGUYÊN (DATA ARTIFACTS)

- [ ] **Thư mục `data/raw_documents/`**: Chứa tối thiểu 2-3 file văn bản pháp luật chính thức dạng PDF:
  - `Luat_Doanh_Nghiep_2020.pdf`
  - `Nghi_Dinh_01_2021_ND_CP_Dang_ky_doanh_nghiep.pdf`
  - `Nghi_Dinh_39_2018_Huong_dan_Luat_Ho_tro_SME.pdf`
- [ ] **Thư mục `data/chromadb/`**: CSDL Vector đã được nhúng sẵn vector từ các file PDF luật.
- [ ] **File `data/database/vsic_2018.sql` hoặc `.csv`**: Dữ liệu danh mục mã ngành kinh tế Việt Nam hoàn chỉnh.

---

## 📊 PHẦN 3: OUTPUT BÁO CÁO & KẾT QUẢ ĐO LƯỜNG (REPORTS & EVALUATION)

- [ ] **Bảng kết quả Ragas Benchmark**: Xuất file `reports/evaluation_results.csv` hoặc bảng Markdown ghi rõ điểm số từng chỉ số.
- [ ] **Báo cáo so sánh Local vs Cloud**: Biểu đồ so sánh Latency, Độ chính xác và Chi phí (Token Cost).
- [ ] **Báo cáo Đồ án hoàn chỉnh (Project Report PDF / Docx)**:
  - Mục 1: Đặt vấn đề và bài toán doanh nghiệp (Business Case).
  - Mục 2: Thiết kế Prompt Engineering & Few-shot / CoT.
  - Mục 3: Kiến trúc Cloud & Local Server (Docker/Ollama).
  - Mục 4: Thiết kế hệ thống RAG và CSDL quan hệ.
  - Mục 5: Thiết kế Multi-Agent Workflow (Sơ đồ LangGraph).
  - Mục 6: Thực nghiệm & Kết quả đánh giá mô hình.
  - Mục 7: Phân tích an toàn bảo mật & Giải pháp phòng chống lỗ hổng.
- [ ] **Slide thuyết trình (Presentation Slides - PPTX / PDF)**: 15-20 slide tóm tắt toàn bộ dự án để báo cáo trước giảng viên.

---

## 🛠️ PHẦN 4: OUTPUT MÔI TRƯỜNG & HẠ TẦNG (DEPLOYMENT & CONFIG)

- [ ] **`requirements.txt`**: Danh sách đầy đủ các thư viện phụ thuộc (`langchain`, `langgraph`, `chromadb`, `ragas`, `streamlit`, `fastapi`, `ollama`, `google-genai`...).
- [ ] **`.env.example`**: File mẫu chứa toàn bộ cấu hình mẫu:
  ```env
  GOOGLE_API_KEY=your_api_key_here
  OLLAMA_BASE_URL=http://localhost:11434
  LOCAL_MODEL_NAME=llama3.1:latest
  CLOUD_MODEL_NAME=gemini-1.5-pro
  EMBEDDING_MODEL=text-embedding-3-small
  DEFAULT_MODE=cloud
  ```
- [ ] **`README.md`**: Đầy đủ hướng dẫn cài đặt và khởi chạy từ A đến Z.
- [ ] **Lịch sử Git Commit**: Lịch sử commit rõ ràng, có quy tắc (Conventional Commits: `feat:`, `fix:`, `docs:`...).

---

## 📈 TIẾN ĐỘ THỰC HIỆN TỔNG THỂ

```
[ ] Giai đoạn 1: Chuẩn bị Dữ liệu (PDF Luật + CSDL Mã ngành VSIC)
[ ] Giai đoạn 2: Xây dựng RAG Pipeline & CSDL Tools
[ ] Giai đoạn 3: Tích hợp Model Providers (Gemini API & Local Ollama)
[ ] Giai đoạn 4: Xây dựng Multi-Agent Workflow (LangGraph)
[ ] Giai đoạn 5: Thêm lớp Bảo mật Guardrails (PII Masking & Anti-Jailbreak)
[ ] Giai đoạn 6: Đánh giá mô hình bằng Ragas & Xuất báo cáo
[ ] Giai đoạn 7: Hoàn thiện Giao diện Streamlit & Viết Báo cáo tổng kết
```
