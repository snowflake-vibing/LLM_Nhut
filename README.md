# ⚖️ LegalTech SME Assistant
### Trợ lý AI Hỗ trợ Tư vấn & Tự động Hóa Thủ tục Pháp lý cho Doanh nghiệp Vừa và Nhỏ (SMEs & Hộ Kinh Doanh) • Phiên bản 1.1

[![Version: 1.1](https://img.shields.io/badge/Version-1.1-brightgreen.svg)](#quản-lý-phiên-bản--lộ-trình-versioning--roadmap)
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

* **Yêu cầu Kỹ thuật Phiên bản 1 (Requirements Version 1.0):**
  * Đặc tả 7 tiêu chí chấm điểm ban đầu của giảng viên: [`requirements/requirements_version_1.md`](./requirements/requirements_version_1.md).
* **Đánh giá Phiên bản 1 (Preview Version 1):**
  * Tổng hợp 4 nhận xét người dùng & phản biện chuyên sâu của AI Engineer: [`requirements/preview_version_1.md`](./requirements/preview_version_1.md).
* **Yêu cầu Kỹ thuật Phiên bản 1.1 (Requirements Version 1.1) - [ĐÃ HOÀN THÀNH]:**
  * 4 nâng cấp thực chiến: Link kiểm chứng Cổng TT Chính phủ, Bộ tạo hồ sơ doanh nghiệp (.docx), Tra cứu Hybrid (CSDL + Web Search), Trực quan hóa PII: [`requirements/requirements_version_1.1.md`](./requirements/requirements_version_1.1.md).

---

## 🌟 TÍNH NĂNG MỚI NÂNG CẤP TRONG PHIÊN BẢN 1.1

1. 📝 **Bộ Tạo Hồ sơ Pháp lý Tự động (Dossier Generator):**
   * Cho phép nhập thông tin doanh nghiệp, đại diện pháp luật, thành viên góp vốn.
   * AI thẩm định tên doanh nghiệp (tránh vi phạm Điều 37, 38, 41 Luật Doanh nghiệp 2020) và thời hạn góp vốn 90 ngày.
   * Tự động sinh và tải về trọn bộ file Word (.docx) chuẩn: **Giấy đề nghị ĐKDN (Nghị định 01/2021/NĐ-CP)**, **Dự thảo Điều lệ công ty**, **Danh sách thành viên sáng lập**.
2. 🔗 **Trích dẫn Căn cứ Pháp luật & Link Kiểm chứng Chính phủ (Verify URL):**
   * Mỗi câu trả lời của AI đều gắn thẻ **Citation Card** có trích dẫn nguyên văn Điều/Khoản kèm nút `[🔗 Kiểm chứng tại Cổng TT Chính phủ]` trỏ trực tiếp đến `vanban.chinhphu.vn`.
3. 🌐 **Kiến trúc Tra cứu Lai (Hybrid Retrieval & Pagination):**
   * Ưu tiên tra cứu nhanh trong CSDL SQLite nội bộ.
   * Tự động kích hoạt **Web Search Tool** khi gặp các ngành nghề mới (Thương mại điện tử, Livestream bán hàng, AI/SaaS, Logistics...).
   * Hỗ trợ bộ lọc phân trang (Pagination) xem toàn bộ danh mục ngành kinh tế VSIC.
4. 🛡️ **Trực quan hóa Luồng Bảo vệ Dữ liệu Cá nhân (PII Masking Flow):**
   * Sơ đồ minh họa 4 bước minh bạch: *Người dùng $\rightarrow$ Local Masker $\rightarrow$ Cloud Gemini $\rightarrow$ Local Unmasker*, cam kết không lộ số CCCD, SĐT hay email lên đám mây.

---

## 📖 1. Giới thiệu Đề tài & Bài toán Doanh nghiệp (Business Case)
Khi thành lập hoặc mở rộng kinh doanh tại Việt Nam, các **Doanh nghiệp vừa và nhỏ (SMEs), Startup và Hộ kinh doanh cá thể** đối mặt với rào cản pháp lý rất lớn:
* **Nỗi đau (Pain points):** Hệ thống luật pháp (Luật Doanh nghiệp, Luật Đầu tư, Luật Thuế), nghị định, thông tư phức tạp; thủ tục xin giấy phép con (ATVSTP, PCCC, giấy phép môi trường...) phân tán; chi phí thuê văn phòng luật sư tư vấn vượt quá ngân sách ban đầu.
* **Giải pháp:** **LegalTech SME Assistant** là hệ thống AI Agent hỗ trợ:
  * Phân tích ý tưởng kinh doanh $\rightarrow$ Định hướng mô hình doanh nghiệp tối ưu (TNHH, Cổ phần, Hộ cá thể).
  * Tự động tra cứu mã ngành kinh tế (VSIC) từ Cơ sở dữ liệu quốc gia SQLite kết hợp Web Search.
  * Truy xuất điều kiện cấp phép con chính xác từ các văn bản pháp luật chính thống (RAG).
  * Tự động tạo lập hồ sơ pháp lý (.docx) chuẩn hóa cho Sở KH&ĐT.

---

## 🎯 2. Đáp ứng 7 Tiêu chí Đánh giá Dự án AI Engineer

| STT | Tiêu chí | Trọng số | Triển khai trong Dự án |
| :---: | :--- | :---: | :--- |
| **1** | **Ứng dụng LLM Doanh nghiệp** | **1.0 đ** | Giải quyết bài toán tư vấn pháp lý và thành lập doanh nghiệp thực tế, tiết kiệm thời gian và chi phí cho SMEs. |
| **2** | **Kỹ năng Prompting** | **2.0 đ** | Áp dụng Few-shot Prompting (mẫu trích xuất pháp lý), Chain-of-Thought (tư duy logic đối chiếu điều luật) và Structured Output (JSON Schema hồ sơ thành lập). |
| **3** | **Cloud Server & Local Model** | **2.5 đ** | Hỗ trợ chuyển đổi linh hoạt (*Model Switcher*):<br>• **Local Model:** Ollama (Qwen 2.5) xử lý thông tin nội bộ nhạy cảm.<br>• **Cloud Model:** Google Gemini 3.5 Flash Lite cho các tác vụ tổng hợp chuyên sâu. |
| **4** | **Vector DB & Đọc CSDL** | **1.5 đ** | • **RAG (Vector DB - ChromaDB):** Đọc & phân tích văn bản Luật Doanh nghiệp 2020, Nghị định 01/2021/NĐ-CP.<br>• **CSDL (SQLite):** Bảng Hệ thống ngành kinh tế Việt Nam (VSIC), Bảng quản lý tiến độ hồ sơ. |
| **5** | **AI Agents & Đa Tác Nhân** | **1.5 đ** | Kiến trúc Multi-Agent Workflow:<br>• *Legal Router Agent:* Phân loại nhu cầu & ý định người dùng.<br>• *Entity Advisory Agent:* Tư vấn mô hình tổ chức doanh nghiệp.<br>• *Industry Lookup Agent:* Tra cứu mã ngành & giấy phép con.<br>• *Document Reviewer Agent:* Rà soát tính hợp lệ của checklist hồ sơ. |
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
        RouterAgent --> AdvisoryAgent["Entity Advisory Agent\n(Tư vấn mô hình DN & Verify URL)"]
        RouterAgent --> IndustryAgent["Industry Lookup Agent\n(Hybrid SQLite + Web Search)"]
        RouterAgent --> ReviewerAgent["Document Checklist Agent\n(Rà soát & Checklist)"]
    end

    subgraph DossierEngine ["📝 Document & Dossier Engine (v1.1)"]
        UI --> DossierGen["Bộ Tạo Hồ sơ (.docx)\nGiấy đề nghị, Điều lệ, Danh sách TV"]
        DossierGen --> LegalValidator["AI Thẩm định Tên DN (Điều 37, 38, 41)"]
    end

    subgraph DataLayer ["🗄️ Tầng Dữ liệu & Tri thức"]
        IndustryAgent --> SQLDB[("💾 CSDL Mã ngành VSIC\n(SQLite: sme_legal.db)")]
        IndustryAgent --> WebSearch["🌐 Web Search Tool\n(DuckDuckGo / DDGS)"]
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

## 📂 4. Cấu trúc Thư mục Dự án

```
LLM_Nhut/
├── app/
│   └── main.py                  # Giao diện người dùng Streamlit (Menu 5 Tab bên trái)
├── data/
│   ├── chromadb/                # CSDL Vector (Index lưu trữ embeddings)
│   ├── database/                # CSDL SQLite (schema.sql & sme_legal.db)
│   ├── evaluation/              # Dataset benchmark (benchmark_dataset.json)
│   └── raw_documents/           # Văn bản luật nguồn (PDF/TXT)
├── llm_provider/                # Module Cloud & Local LLM Provider
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
│   ├── requirements_version_1.md # 7 tiêu chí chấm điểm Version 1.0
│   └── requirements_version_1.1.md # Yêu cầu kỹ thuật nâng cấp Version 1.1
├── src/
│   ├── agents/                  # Multi-Agent Workflow (Router, Advisory, Lookup, Reviewer, Graph)
│   ├── database/                # Quản lý CSDL SQLite & SQL Tools
│   ├── dossier/                 # [MỚI v1.1] Document Generator (.docx) & Legal Validator
│   ├── evaluation/              # Script benchmark Ragas & Model Comparison
│   ├── prompts/                 # System prompts, Few-shot, CoT & Pydantic schemas
│   ├── rag/                     # Pipeline Ingestion, Embeddings, VectorStore & Retriever (Verify URLs)
│   ├── security/                # PII Masking, Prompt Injection Guard & Output Moderation
│   └── tools/                   # [MỚI v1.1] Web Search Tool & Hybrid Retrieval
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