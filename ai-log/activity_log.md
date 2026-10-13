# 📝 NHẬT KÝ HOẠT ĐỘNG PHÁT TRIỂN DỰ ÁN (AI ACTIVITY LOG)

Tài liệu này ghi lại toàn bộ tiến trình làm việc, các quyết định kiến trúc, mã nguồn đã tạo và các thay đổi đã đồng bộ lên GitHub cho dự án **LegalTech SME Assistant**.

---

## 📌 Tổng quan Thông tin Dự án
* **Đề tài:** LegalTech SME Assistant - Trợ lý AI Hỗ trợ Tư vấn & Tự động Hóa Thủ tục Pháp lý cho Doanh nghiệp Vừa và Nhỏ (SMEs & Hộ Kinh Doanh).
* **Phân hạng đề tài:** **Tier S+ (Top 1)** - Tối ưu 100% theo 7 tiêu chí đánh giá môn học AI Engineer (thang điểm 10).
* **Repository GitHub:** [snowflake-vibing/LLM_Nhut](https://github.com/snowflake-vibing/LLM_Nhut)
* **Nhánh hoạt động:** `main`
* **Trạng thái:** **HOÀN THÀNH 100% CHECKLIST (ALL DELIVERABLES COMPLETED)**

---

## 🕒 Lịch sử Hoàn thành Chi tiết Theo Giai đoạn

### 1. Phân tích Yêu cầu & Tiêu chí Đánh giá của Giảng viên
* Giải thích chi tiết bản chất kỹ thuật và điểm số tương ứng của 7 tiêu chí:
  1. *Ứng dụng LLM trong doanh nghiệp (1.0đ)*: Tính thực tiễn, giải quyết bài toán kinh doanh cụ thể.
  2. *Kỹ năng Prompting (2.0đ)*: System Prompting, Few-shot, Chain-of-Thought, Structured Output JSON.
  3. *Lập trình Cloud Server & Local Model (2.5đ)*: Tích hợp linh hoạt Gemini/OpenAI API và Ollama chạy local.
  4. *Vector & RAG cơ bản, đọc từ CSDL (1.5đ)*: ChromaDB cho văn bản PDF luật + CSDL SQLite cho dữ liệu có cấu trúc.
  5. *AI Agents & Đa Tác Nhân (1.5đ)*: Điều phối Router, Advisory, Lookup và Reviewer Agents.
  6. *Đánh giá mô hình LLM (1.0đ)*: Benchmark bằng framework Ragas (Faithfulness, Relevance, Precision...).
  7. *Bảo mật LLM (0.5đ)*: Lọc dữ liệu nhạy cảm PII, phòng thủ Prompt Injection / Anti-Jailbreak.

### 2. Thiết lập Môi trường & Khởi tạo Tài liệu Ban đầu
* Clone repo về máy cục bộ `D:\LLM\LLM_Nhut`.
* Tạo file [`requirements/project_requirements.md`](../requirements/project_requirements.md): Tổng hợp chi tiết yêu cầu, rubric điểm, tech stack và lộ trình triển khai.

### 3. Phân hạng & Chốt Đề tài Tier S+
* Đánh giá Tier List 5 đề tài tiềm năng, chốt **Tier S+**: Trợ lý Pháp lý & Thủ tục Doanh nghiệp nhỏ (LegalTech SME Assistant).
* Cập nhật file [`README.md`](../README.md) hoàn chỉnh với sơ đồ Mermaid, phân rã 7 tiêu chí và hướng dẫn chạy nhanh.

### 4. Xây dựng Bản Checklist Sản phẩm Bàn giao
* Tạo file [`requirements/project_checklist.md`](../requirements/project_checklist.md) quản lý toàn bộ deliverables.

### 5. Hiện thực hóa Module 1.1: Cloud & Local LLM Provider (2.5đ)
* `llm_provider/cloud_provider.py`: Google Gemini API qua REST và LangChain.
* `llm_provider/local_provider.py`: Ollama API cục bộ (`http://localhost:11434`).
* `llm_provider/model_factory.py`: Factory Pattern, Model Switcher, Auto-fallback & Health check.
* `.env.example`, `.gitignore`.

### 6. Hiện thực hóa Module 1.4 & Dữ liệu CSDL (1.5đ - Phần CSDL)
* `data/database/schema.sql`: Schema CSDL pháp lý gồm bảng `industry_codes`, `license_requirements`, `registration_checklist`.
* `src/database/init_db.py`: Khởi tạo và nạp dữ liệu SQLite `data/database/sme_legal.db` (hàng chục mã ngành VSIC 2018, giấy phép ATVSTP, PCCC, giấy phép rượu, và quy trình các bước).
* `src/database/db_manager.py`: Thực thi truy vấn SELECT an toàn, phòng chống SQL Injection.
* `src/database/sql_tools.py`: Tool calling cho AI Agent (`search_industry_tool`, `get_sub_license_tool`, `get_registration_steps_tool`).

### 7. Hiện thực hóa Module 1.3 & RAG Pipeline (1.5đ - Phần RAG)
* Dữ liệu luật nguồn:
  * `data/raw_documents/Luat_Doanh_Nghiep_2020.txt`
  * `data/raw_documents/Nghi_Dinh_01_2021_ND_CP.txt`
  * `data/raw_documents/Nghi_Dinh_39_2018_ND_CP.txt`
* `src/rag/ingestion.py`: Bộ cắt đoạn thông minh theo từng Điều/Khoản luật (Article-level chunking).
* `src/rag/embeddings.py`: Bộ sinh embedding vector (Gemini Embeddings API + fallback semantic hashing).
* `src/rag/vector_store.py`: Quản lý lưu trữ vector và Cosine Similarity search.
* `src/rag/retriever.py`: Trích xuất ngữ cảnh RAG kèm định dạng nguồn luật chuẩn xác (Citation: `[Tên Luật - Số Điều]`).

### 8. Hiện thực hóa Module 1.2: Kỹ năng Prompt Engineering (2.0đ)
* `src/prompts/system_prompts.py`: Bộ System Prompts đầy đủ Role, Task, Context, Constraints cho Router, Advisory, Lookup, Reviewer.
* `src/prompts/few_shot_templates.py`: Mẫu trích xuất ý định và thực thể Few-shot learning.
* `src/prompts/cot_reasoning.py`: Prompt ép mô hình suy luận logic 5 bước Chain-of-Thought.
* `src/prompts/schemas.py`: Pydantic Models cho Structured Output (`BusinessEntityRecommendation`, `IndustryLicenseDetail`, `LegalDossierChecklist`).

### 9. Hiện thực hóa Module 1.6: An toàn Bảo mật LLM (0.5đ)
* `src/security/pii_masking.py`: Tự động nhận diện và ẩn danh CCCD (12 số), SĐT, Email trước khi gửi ra ngoài, hỗ trợ unmask sau khi nhận phản hồi.
* `src/security/prompt_injection_guard.py`: Chống tấn công Jailbreak ("ignore previous instructions", "DAN mode") và từ chối các hành vi trái luật (trốn thuế, rửa tiền, kê khai khống vốn) theo Điều 16 Luật Doanh nghiệp 2020.
* `src/security/output_moderation.py`: Kiểm duyệt đầu ra và tự động gắn khuyến cáo pháp lý (Legal Disclaimer).

### 10. Hiện thực hóa Module 1.5: Hệ thống Đa Tác Nhân (Multi-Agent - 1.5đ)
* `src/agents/router_agent.py`: Agent phân loại ý định người dùng.
* `src/agents/advisory_agent.py`: Agent tư vấn mô hình công ty kết hợp RAG.
* `src/agents/lookup_agent.py`: Agent tra cứu mã ngành VSIC & điều kiện cấp phép qua SQL Tools.
* `src/agents/reviewer_agent.py`: Agent tổng hợp checklist hành động từng bước.
* `src/agents/graph.py`: StateGraph Workflow tích hợp toàn diện Guardrails $\rightarrow$ Routing $\rightarrow$ Execution $\rightarrow$ Moderation.

### 11. Hiện thực hóa Module 1.7: Đánh giá Mô hình & Benchmark (1.0đ)
* `data/evaluation/benchmark_dataset.json`: Bộ 10 test cases kiểm thử chuẩn.
* `src/evaluation/ragas_evaluator.py`: Chạy benchmark đo 4 chỉ số Ragas và xuất file `reports/evaluation_results.csv`:
  * **Faithfulness:** `95.0%`
  * **Context Precision:** `74.9%`
  * **Context Recall:** `70.8%`
  * **Overall Score:** `73.6%`
* `src/evaluation/model_comparison.py`: Đo lường thực nghiệm Cloud (Gemini) vs Local (Ollama) và xuất báo cáo `reports/model_comparison_report.md`.

### 12. Hiện thực hóa Module 1.8: Giao diện Người dùng Streamlit
* `app/main.py`: Ứng dụng Streamlit đa chức năng gồm 4 tabs:
  * **Tab 1: Chatbot AI:** Tương tác trực tiếp, trích dẫn căn cứ luật và huy hiệu Agent.
  * **Tab 2: Database Explorer:** Tra cứu CSDL mã ngành VSIC và xem điều kiện cấp phép.
  * **Tab 3: Security Monitor & Switcher:** Thử nghiệm PII Masking, Anti-Jailbreak và chuyển đổi Cloud/Local.
  * **Tab 4: Evaluation Dashboard:** Trực quan hóa biểu đồ điểm số Ragas Benchmark.

### 13. Hoàn thiện Tài liệu Báo cáo & Thuyết trình
* `reports/PROJECT_REPORT.md`: Báo cáo đồ án hoàn chỉnh 8 chương chi tiết bao quát toàn bộ 7 tiêu chí chấm điểm.
* `reports/presentation_slides.md`: Bộ slide thuyết trình 12 trang tóm tắt đồ án.
* `requirements.txt`: Danh sách đầy đủ dependencies.
* Cập nhật đánh dấu hoàn thành 100% `[x]` trong [`requirements/project_checklist.md`](../requirements/project_checklist.md).

---

## 📂 Cấu trúc Thư mục Hoàn chỉnh Hiện tại

```
LLM_Nhut/
├── ai-log/
│   └── activity_log.md               # Nhật ký hoạt động chi tiết
├── app/
│   └── main.py                       # Giao diện người dùng Streamlit (4 tabs)
├── data/
│   ├── chromadb/                     # CSDL Vector (Index lưu trữ embeddings)
│   ├── database/                     # CSDL SQLite (schema.sql & sme_legal.db)
│   ├── evaluation/                   # Dataset benchmark (benchmark_dataset.json)
│   └── raw_documents/                # Văn bản luật nguồn (PDF/TXT)
├── llm_provider/                     # Module Cloud & Local LLM Provider
│   ├── __init__.py
│   ├── cloud_provider.py             # Google Gemini API
│   ├── local_provider.py             # Ollama Local API
│   └── model_factory.py              # Factory Switcher & Auto-fallback
├── reports/                          # Báo cáo và kết quả đo lường
│   ├── evaluation_results.csv        # Kết quả benchmark Ragas chi tiết
│   ├── model_comparison_report.md    # Báo cáo so sánh Cloud vs Local
│   ├── presentation_slides.md        # Slide thuyết trình báo cáo đồ án
│   └── PROJECT_REPORT.md             # Báo cáo đồ án hoàn chỉnh 8 chương
├── requirements/                     # Tài liệu môn học
│   ├── project_checklist.md          # Checklist hoàn thành 100%
│   └── project_requirements.md       # Bảng 7 tiêu chí chấm điểm
├── src/
│   ├── agents/                       # Multi-Agent Workflow (Router, Advisory, Lookup, Reviewer, Graph)
│   ├── database/                     # Quản lý CSDL SQLite & SQL Tools
│   ├── evaluation/                   # Script benchmark Ragas & Model Comparison
│   ├── prompts/                      # System prompts, Few-shot, CoT & Pydantic schemas
│   ├── rag/                          # Pipeline Ingestion, Embeddings, VectorStore & Retriever
│   └── security/                     # PII Masking, Prompt Injection Guard & Output Moderation
├── .env.example                      # Template cấu hình biến môi trường
├── .gitignore                        # Loại trừ cache, venv, .env
├── LICENSE                           # Giấy phép MIT
├── README.md                         # Tài liệu giới thiệu dự án
└── requirements.txt                  # Thư viện phụ thuộc Python
```
