# ⚖️ LegalTech SME Assistant
### Trợ lý AI Hỗ trợ Tư vấn & Tự động Hóa Thủ tục Pháp lý cho Doanh nghiệp Vừa và Nhỏ (SMEs & Hộ Kinh Doanh)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![Ollama](https://img.shields.io/badge/Local_LLM-Ollama-black.svg)](https://ollama.ai/)
[![Gemini](https://img.shields.io/badge/Cloud_LLM-Gemini_3.5_Flash_Lite-4285F4.svg)](https://aistudio.google.com/)

---

## 📜 NGUYÊN TẮC HOẠT ĐỘNG DỰ ÁN (PROJECT RULES)
> 🚨 **QUY ĐỊNH BẮT BUỘC:** Mọi tác vụ phát triển của AI hoặc người đóng góp phải tuân thủ nghiêm ngặt tài liệu:  
> 👉 **[`RULES.md`](./RULES.md)** *(Quy chuẩn đọc đầu tiên, quy tắc đặt tên version preview/requirements và an toàn bảo mật).*

---

## 🚀 QUẢN LÝ PHIÊN BẢN & LỘ TRÌNH (VERSIONING & ROADMAP)

* **Phiên bản Hiện tại (Version 1.0 - Completed):**
  * Hoàn thành đầy đủ 7 tiêu chí chấm điểm của giảng viên (Multi-Agent, RAG, SQLite VSIC 2018, Cloud Gemini + Local Ollama, Benchmark Ragas 95%, PII Masking & Anti-Jailbreak).
  * Checklist nghiệm thu: [`requirements/project_checklist.md`](./requirements/project_checklist.md).
* **Đánh giá Phiên bản 1 (Preview Version 1):**
  * Tổng hợp 4 nhận xét người dùng & phản biện chuyên sâu của AI Engineer: [`requirements/preview_version_1.md`](./requirements/preview_version_1.md).
* **Yêu cầu Kỹ thuật Phiên bản 1.1 (Requirements Version 1.1):**
  * Lộ trình nâng cấp: Trích dẫn kèm Link kiểm chứng, Bộ tạo hồ sơ doanh nghiệp tự động (.docx), Tra cứu Hybrid (CSDL + Web Search): [`requirements/requirements_version_1.1.md`](./requirements/requirements_version_1.1.md).

---

## 📖 1. Giới thiệu Đề tài & Bài toán Doanh nghiệp (Business Case)
Khi thành lập hoặc mở rộng kinh doanh tại Việt Nam, các **Doanh nghiệp vừa và nhỏ (SMEs), Startup và Hộ kinh doanh cá thể** đối mặt với rào cản pháp lý rất lớn:
* **Nỗi đau (Pain points):** Hệ thống luật pháp (Luật Doanh nghiệp, Luật Đầu tư, Luật Thuế), nghị định, thông tư phức tạp; thủ tục xin giấy phép con (ATVSTP, PCCC, giấy phép môi trường...) phân tán; chi phí thuê văn phòng luật sư tư vấn vượt quá ngân sách ban đầu.
* **Giải pháp:** **LegalTech SME Assistant** là hệ thống AI Agent hỗ trợ:
  * Phân tích ý tưởng kinh doanh $\rightarrow$ Định hướng mô hình doanh nghiệp tối ưu (TNHH, Cổ phần, Hộ cá thể).
  * Tự động tra cứu mã ngành kinh tế (VSIC) từ Cơ sở dữ liệu quốc gia SQLite.
  * Truy xuất điều kiện cấp phép con chính xác từ các văn bản pháp luật chính thống (RAG).
  * Hướng dẫn soạn thảo checklist hồ sơ pháp lý từng bước.

---

## 🎯 2. Đáp ứng 7 Tiêu chí Đánh giá Dự án AI Engineer

| STT | Tiêu chí | Trọng số | Triển khai trong Dự án |
| :---: | :--- | :---: | :--- |
| **1** | **Ứng dụng LLM Doanh nghiệp** | **1.0 đ** | Giải quyết bài toán tư vấn pháp lý và thành lập doanh nghiệp thực tế, tiết kiệm thời gian và chi phí cho SMEs. |
| **2** | **Kỹ năng Prompting** | **2.0 đ** | Áp dụng Few-shot Prompting (mẫu trích xuất pháp lý), Chain-of-Thought (tư duy logic đối chiếu điều luật) và Structured Output (JSON Schema hồ sơ thành lập). |
| **3** | **Cloud Server & Local Model** | **2.5 đ** | Hỗ trợ chuyển đổi linh hoạt (*Model Switcher*):<br>• **Local Model:** Ollama (Qwen 2.5 / Llama 3) xử lý thông tin nội bộ nhạy cảm.<br>• **Cloud Model:** Google Gemini 3.5 Flash Lite cho các tác vụ tổng hợp chuyên sâu. |
| **4** | **Vector DB & Đọc CSDL** | **1.5 đ** | • **RAG (Vector DB - ChromaDB):** Đọc & phân tích văn bản Luật Doanh nghiệp 2020, Nghị định 01/2021/NĐ-CP.<br>• **CSDL (SQLite):** Bảng Hệ thống ngành kinh tế Việt Nam (VSIC), Bảng quản lý tiến độ hồ sơ. |
| **5** | **AI Agents & Đa Tác Nhân** | **1.5 đ** | Kiến trúc Multi-Agent Workflow:<br>• *Legal Router Agent:* Phân loại nhu cầu & ý định người dùng.<br>• *Entity Advisory Agent:* Tư vấn mô hình tổ chức doanh nghiệp.<br>• *Industry Lookup Agent:* Tra cứu mã ngành & điều kiện cấp phép.<br>• *Document Reviewer Agent:* Rà soát tính hợp lệ của checklist hồ sơ. |
| **6** | **Đánh giá mô hình LLM** | **1.0 đ** | Sử dụng framework **Ragas** đo lường: Faithfulness (95.0%), Answer Relevance, Context Precision. Báo cáo so sánh Local vs Cloud. |
| **7** | **Bảo mật LLM** | **0.5 đ** | • **PII Data Masking:** Tự động che dấu CCCD/CMND, số điện thoại, email trước khi gọi LLM ngoài.<br>• **Prompt Injection Guard:** Chặn câu lệnh bẻ khóa system prompt hoặc yêu cầu trốn thuế, vi phạm Điều 16 Luật Doanh nghiệp. |

---

## 🏛️ 3. Kiến trúc Hệ thống (System Architecture)

```mermaid
flowchart TD
    User["👤 Người dùng (SMEs / Startup)"] --> UI["🖥️ Giao diện Streamlit (Menu Tabs bên trái)"]
    UI --> Guardrails["🛡️ Lớp Bảo mật (PII Masking & Prompt Injection Defense)"]
    
    subgraph MultiAgentEngine ["🤖 Multi-Agent Orchestrator"]
        Guardrails --> RouterAgent["Legal Router Agent"]
        RouterAgent --> AdvisoryAgent["Entity Advisory Agent\n(Tư vấn mô hình DN)"]
        RouterAgent --> IndustryAgent["Industry Lookup Agent\n(Tra cứu mã ngành & giấy phép con)"]
        RouterAgent --> ReviewerAgent["Document Checklist Agent\n(Rà soát & Soạn hồ sơ)"]
    end

    subgraph DataLayer ["🗄️ Tầng Dữ liệu & Tri thức"]
        IndustryAgent --> SQLDB[("💾 CSDL Mã ngành VSIC\n(SQLite: sme_legal.db)")]
        AdvisoryAgent --> VectorDB[("📚 Vector DB (ChromaDB)\nLuật Doanh nghiệp 2020")]
        ReviewerAgent --> VectorDB
    end

    subgraph LLMExecutionEngine ["⚡ LLM Execution Switcher"]
        MultiAgentEngine --> Switcher{"Chế độ triển khai"}
        Switcher -->|"Dữ liệu nội bộ / Nhạy cảm"| LocalLLM["💻 Local Model (Ollama / Qwen 2.5)"]
        Switcher -->|"Tổng hợp chuyên sâu"| CloudLLM["☁️ Cloud Model (Gemini 3.5 Flash Lite)"]
    end
```

---

## 📂 4. Cấu trúc Thư mục Dự án Hiện tại

```
LLM_Nhut/
├── app/
│   └── main.py                  # Giao diện người dùng Streamlit (Menu Tab bên trái)
├── data/
│   ├── chromadb/                # CSDL Vector (Index lưu trữ embeddings)
│   ├── database/                # CSDL SQLite (schema.sql & sme_legal.db)
│   ├── evaluation/              # Dataset benchmark (benchmark_dataset.json)
│   └── raw_documents/           # Văn bản luật nguồn (PDF/TXT)
├── llm_provider/                # Module Cloud & Local LLM Provider
│   ├── __init__.py
│   ├── cloud_provider.py        # Tích hợp Google Gemini API
│   ├── local_provider.py        # Tích hợp Ollama Local API
│   └── model_factory.py         # Factory Switcher & Auto-fallback
├── reports/                     # Báo cáo và kết quả đo lường
│   ├── evaluation_results.csv   # Kết quả benchmark Ragas chi tiết
│   ├── model_comparison_report.md # Báo cáo so sánh Cloud vs Local
│   ├── presentation_slides.md   # Slide thuyết trình báo cáo đồ án
│   └── PROJECT_REPORT.md        # Báo cáo đồ án hoàn chỉnh 8 chương
├── requirements/                # Quản lý yêu cầu & Phiên bản
│   ├── preview_version_1.md     # Đánh giá Version 1 & Phản biện kỹ thuật
│   ├── project_checklist.md     # Checklist nghiệm thu Version 1 (100% [x])
│   ├── project_requirements.md  # 7 tiêu chí chấm điểm ban đầu
│   └── requirements_version_1.1.md # Yêu cầu kỹ thuật nâng cấp cho Version 1.1
├── src/
│   ├── agents/                  # Multi-Agent Workflow (Router, Advisory, Lookup, Reviewer, Graph)
│   ├── database/                # Quản lý CSDL SQLite & SQL Tools
│   ├── evaluation/              # Script benchmark Ragas & Model Comparison
│   ├── prompts/                 # System prompts, Few-shot, CoT & Pydantic schemas
│   ├── rag/                     # Pipeline Ingestion, Embeddings, VectorStore & Retriever
│   └── security/                # PII Masking, Prompt Injection Guard & Output Moderation
├── tutorial/
│   └── run_guide.md             # Hướng dẫn chi tiết quy trình chạy dự án từ A đến Z
├── .env.example                 # Template cấu hình biến môi trường
├── .gitignore                   # Loại trừ cache, venv, .env
├── LICENSE                      # Giấy phép MIT
├── README.md                    # Tài liệu tổng quan dự án
└── RULES.md                     # Quy định hoạt động bắt buộc cho AI
```

---

## 🚀 5. Hướng dẫn Khởi chạy Nhanh

Xem hướng dẫn chi tiết từng bước tại: 👉 **[`tutorial/run_guide.md`](./tutorial/run_guide.md)**

```bash
# 1. Kích hoạt môi trường ảo
.\venv\Scripts\Activate.ps1

# 2. Khởi tạo CSDL SQLite (nếu chưa chạy)
python src/database/init_db.py

# 3. Khởi chạy giao diện web Streamlit
streamlit run app/main.py
```
Mở trình duyệt tại: `http://localhost:8501`.