# 📋 CHECKLIST CÁC OUTPUT BẮT BUỘC CHO DỰ ÁN (PROJECT DELIVERABLES)

Checklist này tổng hợp toàn bộ các **Sản phẩm bàn giao (Deliverables / Outputs)** cụ thể cần có để nghiệm thu dự án **LegalTech SME Assistant**, đảm bảo đạt điểm tối đa (10/10) theo 7 tiêu chí của giảng viên.

---

## 🧩 PHẦN 1: OUTPUT MÃ NGUỒN (SOURCE CODE & MODULES)

### 1.1. Module Mô hình Đám mây & Nội bộ (Cloud & Local LLM Provider - 2.5đ)
- [x] **`llm_provider/cloud_provider.py`**: Tích hợp Google Gemini API (hoặc OpenAI API) qua SDK/LangChain.
- [x] **`llm_provider/local_provider.py`**: Kết nối Ollama cục bộ (Llama 3.1 / Qwen 2.5) qua API `http://localhost:11434`.
- [x] **`llm_provider/model_factory.py`**: Cơ chế Factory/Switcher cho phép chuyển đổi tức thì giữa Cloud và Local bằng cấu hình hoặc nút gạt trên UI.

### 1.2. Kỹ năng Prompting (Prompt Engineering - 2.0đ)
- [x] **`src/prompts/system_prompts.py`**: Bộ System Prompts hoàn chỉnh (đầy đủ Role, Context, Constraint, Tone of Voice).
- [x] **`src/prompts/few_shot_templates.py`**: Prompt mẫu trích xuất ý định và thông tin pháp lý từ câu hỏi của người dùng (Few-shot learning).
- [x] **`src/prompts/cot_reasoning.py`**: Prompt suy luận từng bước (Chain-of-Thought) phân tích loại hình doanh nghiệp phù hợp.
- [x] **`src/prompts/schemas.py`**: Pydantic Schema định nghĩa chuẩn đầu ra dạng JSON (Structured Output) cho hồ sơ thành lập doanh nghiệp.

### 1.3. Module Vector DB & RAG (1.5đ - Phần 1)
- [x] **`src/rag/ingestion.py`**: Script đọc file văn bản pháp luật PDF/TXT, chia đoạn (*chunking*) tối ưu theo Điều/Khoản.
- [x] **`src/rag/embeddings.py`**: Module tạo vector nhúng (Embedding model hỗ trợ tiếng Việt tốt: Gemini text-embedding-004 & fallback).
- [x] **`src/rag/vector_store.py`**: Tích hợp ChromaDB / Persistent Vector Store lưu trữ vector và thực hiện truy vấn tìm kiếm tương đồng ngữ nghĩa (*Semantic Search*).
- [x] **`src/rag/retriever.py`**: Bộ trích xuất ngữ cảnh RAG kèm cơ chế trích dẫn nguồn luật chính xác (tên Luật, số Điều, Khoản).

### 1.4. Module Đọc & Truy vấn CSDL (Database Integration - 1.5đ - Phần 2)
- [x] **`data/database/sme_legal.db`**: Cơ sở dữ liệu SQLite chứa:
  - Bảng `industry_codes` (Hệ thống ngành kinh tế Việt Nam - VSIC 2018: Mã ngành, Tên ngành, Ngành nghề có điều kiện).
  - Bảng `license_requirements` (Danh mục giấy phép con: ATVSTP, PCCC, giấy phép môi trường...).
  - Bảng `registration_checklist` (Tiến độ và các bước làm hồ sơ).
- [x] **`src/database/db_manager.py`**: Kết nối và quản lý truy vấn CSDL an toàn.
- [x] **`src/database/sql_tools.py`**: Cung cấp công cụ Tool Calling cho Agent tự động sinh câu lệnh SQL tra cứu mã ngành.

### 1.5. Module AI Agents & Đa Tác Nhân (Multi-Agent - 1.5đ)
- [x] **`src/agents/router_agent.py`**: Agent phân loại câu hỏi (Tư vấn mô hình DN, Tra cứu mã ngành, Hỏi thủ tục, hay Kiểm tra hồ sơ).
- [x] **`src/agents/advisory_agent.py`**: Agent phân tích ưu/nhược điểm các mô hình (TNHH 1TV, TNHH 2TV+, Cổ phần, Hộ cá thể).
- [x] **`src/agents/lookup_agent.py`**: Agent gọi Tool CSDL và RAG tra cứu mã ngành và giấy phép con tương ứng.
- [x] **`src/agents/reviewer_agent.py`**: Agent kiểm duyệt và tổng hợp checklist hồ sơ pháp lý hoàn chỉnh cho người dùng.
- [x] **`src/agents/graph.py`**: Điều phối luồng làm việc giữa các agent (StateGraph Multi-Agent Workflow).

### 1.6. Module Bảo mật LLM (Security & Guardrails - 0.5đ)
- [x] **`src/security/pii_masking.py`**: Lọc và che dấu dữ liệu nhạy cảm (CCCD/CMND, Số điện thoại, Địa chỉ nhà, Email) trước khi gửi qua API.
- [x] **`src/security/prompt_injection_guard.py`**: Nhận diện và chặn đứng các prompt cố tình jailbreak, bẻ khóa hoặc hỏi cách trốn thuế, lách luật.
- [x] **`src/security/output_moderation.py`**: Kiểm duyệt đầu ra, từ chối đưa ra lời khuyên pháp lý sai trái hoặc mang tính phỉ báng.

### 1.7. Module Đánh giá Mô hình (LLM Evaluation - 1.0đ)
- [x] **`data/evaluation/benchmark_dataset.json`**: Tập dữ liệu kiểm thử chuẩn gồm các test cases thực tế (Question, Ground Truth, Expected Context).
- [x] **`src/evaluation/ragas_evaluator.py`**: Script tự động chạy benchmark đo 4 chỉ số:
  - *Faithfulness* (Độ trung thực, không bịa luật).
  - *Answer Relevance* (Mức độ liên quan của câu trả lời).
  - *Context Precision* (Độ chính xác của văn bản luật trích xuất).
  - *Context Recall* (Độ bao phủ của tài liệu trích xuất).
- [x] **`src/evaluation/model_comparison.py`**: Script so sánh thực nghiệm giữa Local Model (Ollama) và Cloud Model (Gemini): Thời gian phản hồi (Latency), Tokens/s, Điểm số chính xác.

### 1.8. Giao diện Người dùng (User Interface)
- [x] **`app/main.py`**: Ứng dụng Streamlit hoàn chỉnh gồm:
  - Tab 1: **Trò chuyện Trợ lý Pháp lý (Chatbot AI)** - Hỗ trợ chat, trích dẫn nguồn luật.
  - Tab 2: **Tra cứu Mã ngành & Giấy phép con (Database Explorer)** - Tìm kiếm trực tiếp trên CSDL VSIC.
  - Tab 3: **Trình chuyển đổi Model (Model Switcher & Security Monitor)** - Chọn Cloud/Local và xem nhật ký lọc PII.
  - Tab 4: **Bảng điều khiển Đánh giá (Evaluation Dashboard)** - Biểu đồ trực quan hóa kết quả Ragas Benchmark.

---

## 📚 PHẦN 2: OUTPUT DỮ LIỆU & TÀI NGUYÊN (DATA ARTIFACTS)

- [x] **Thư mục `data/raw_documents/`**: Chứa các file văn bản pháp luật chính thức:
  - `Luat_Doanh_Nghiep_2020.txt`
  - `Nghi_Dinh_01_2021_ND_CP.txt`
  - `Nghi_Dinh_39_2018_ND_CP.txt`
- [x] **Thư mục `data/chromadb/`**: CSDL Vector đã được nhúng sẵn vector từ các file văn bản luật.
- [x] **File `data/database/schema.sql` & `sme_legal.db`**: Dữ liệu danh mục mã ngành kinh tế Việt Nam VSIC 2018 hoàn chỉnh.

---

## 📊 PHẦN 3: OUTPUT BÁO CÁO & KẾT QUẢ ĐO LƯỜNG (REPORTS & EVALUATION)

- [x] **Bảng kết quả Ragas Benchmark**: Xuất file `reports/evaluation_results.csv` ghi rõ điểm số từng chỉ số.
- [x] **Báo cáo so sánh Local vs Cloud**: File `reports/model_comparison_report.md` so sánh Latency, Độ chính xác và Chi phí.
- [x] **Báo cáo Đồ án hoàn chỉnh**: File `reports/PROJECT_REPORT.md` (8 chương chi tiết bao quát toàn bộ 7 tiêu chí).
- [x] **Slide thuyết trình**: File `reports/presentation_slides.md` (12 slide tóm tắt toàn bộ dự án để báo cáo trước giảng viên).

---

## 🛠️ PHẦN 4: OUTPUT MÔI TRƯỜNG & HẠ TẦNG (DEPLOYMENT & CONFIG)

- [x] **`requirements.txt`**: Danh sách đầy đủ các thư viện phụ thuộc (`streamlit`, `fastapi`, `langchain`, `pydantic`...).
- [x] **`.env.example`**: File mẫu chứa toàn bộ cấu hình mẫu.
- [x] **`README.md`**: Đầy đủ hướng dẫn cài đặt và khởi chạy từ A đến Z.
- [x] **Lịch sử Git Commit**: Lịch sử commit rõ ràng, có quy tắc.

---

## 📈 TIẾN ĐỘ THỰC HIỆN TỔNG THỂ

```
[x] Giai đoạn 1: Chuẩn bị Dữ liệu (Văn bản Luật + CSDL Mã ngành VSIC)
[x] Giai đoạn 2: Xây dựng RAG Pipeline & CSDL Tools
[x] Giai đoạn 3: Tích hợp Model Providers (Gemini API & Local Ollama)
[x] Giai đoạn 4: Xây dựng Multi-Agent Workflow (LangGraph / StateGraph)
[x] Giai đoạn 5: Thêm lớp Bảo mật Guardrails (PII Masking & Anti-Jailbreak)
[x] Giai đoạn 6: Đánh giá mô hình bằng Ragas & Xuất báo cáo CSV/Markdown
[x] Giai đoạn 7: Hoàn thiện Giao diện Streamlit & Viết Báo cáo tổng kết + Slide
```
