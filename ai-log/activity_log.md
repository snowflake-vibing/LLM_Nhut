# 📝 NHẬT KÝ HOẠT ĐỘNG PHÁT TRIỂN DỰ ÁN (AI ACTIVITY LOG)

Tài liệu này ghi lại toàn bộ tiến trình làm việc, các quyết định kiến trúc, mã nguồn đã tạo và các thay đổi đã đồng bộ lên GitHub cho dự án **LegalTech SME Assistant**.

---

## 📌 Tổng quan Thông tin Dự án
* **Đề tài:** LegalTech SME Assistant - Trợ lý AI Hỗ trợ Tư vấn & Tự động Hóa Thủ tục Pháp lý cho Doanh nghiệp Vừa và Nhỏ (SMEs & Hộ Kinh Doanh).
* **Phân hạng đề tài:** **Tier S+ (Top 1)** - Tối ưu 100% theo 7 tiêu chí đánh giá môn học AI Engineer (thang điểm 10).
* **Repository GitHub:** [snowflake-vibing/LLM_Nhut](https://github.com/snowflake-vibing/LLM_Nhut)
* **Nhánh hoạt động:** `main`

---

## 🕒 Lịch sử Hoàn thành Chi tiết Theo Giai đoạn

### 1. Phân tích Yêu cầu & Tiêu chí Đánh giá của Giảng viên
* **Nội dung:** Giải thích chi tiết bản chất kỹ thuật và điểm số tương ứng của 7 tiêu chí trong đề cương:
  1. *Ứng dụng LLM trong doanh nghiệp (1.0đ)*: Tính thực tiễn, giải quyết bài toán kinh doanh cụ thể.
  2. *Kỹ năng Prompting (2.0đ)*: System Prompting, Few-shot, Chain-of-Thought, Structured Output JSON.
  3. *Lập trình Cloud Server & Local Model (2.5đ)*: Tích hợp linh hoạt Gemini/OpenAI API và Ollama chạy local.
  4. *Vector & RAG cơ bản, đọc từ CSDL (1.5đ)*: ChromaDB cho văn bản PDF luật + CSDL SQLite cho dữ liệu có cấu trúc.
  5. *AI Agents & Đa Tác Nhân (1.5đ)*: LangGraph điều phối Router, Advisory, Lookup và Reviewer Agents.
  6. *Đánh giá mô hình LLM (1.0đ)*: Benchmark bằng framework Ragas (Faithfulness, Relevance, Precision...).
  7. *Bảo mật LLM (0.5đ)*: Lọc dữ liệu nhạy cảm PII, phòng thủ Prompt Injection / Anti-Jailbreak.

### 2. Thiết lập Môi trường & Khởi tạo Tài liệu Ban đầu
* **Kết nối & Clone Repository:** Clone mã nguồn từ GitHub về thư mục cục bộ `D:\LLM\LLM_Nhut`.
* **Tạo thư mục & tài liệu `requirements/`:**
  * Tạo file [`requirements/project_requirements.md`](../requirements/project_requirements.md): Tổng hợp chi tiết yêu cầu, rubric điểm, tech stack và lộ trình 6 giai đoạn.
  * Commit: `docs: add project requirements and grading criteria` (Đã push lên GitHub).

### 3. Đánh giá & Phân hạng Đề tài (Tier List Ranking)
* Phân tích và xếp hạng 5 đề tài tiềm năng theo khả năng đạt điểm tuyệt đối:
  * **Tier S+ (Lựa chọn chính thức):** Trợ lý Pháp lý & Thủ tục Doanh nghiệp nhỏ (LegalTech SME Assistant).
  * **Tier S:** Trợ lý CSKH & Tra cứu Đơn hàng E-Commerce.
  * **Tier A+:** Trợ lý Nhân sự Nội bộ & Quản lý Nghỉ phép (Enterprise HR).
  * **Tier A:** Trợ lý Thẩm định Hồ sơ Vay Ngân hàng (Fintech Loan).
  * **Tier C:** Tư vấn & Báo cáo Thị trường Crypto (nhiều rủi ro pháp lý và khó đo lường Ground Truth).

### 4. Cập nhật Tài liệu Kiến trúc Dự án
* Cập nhật file [`README.md`](../README.md) hoàn chỉnh bao gồm:
  * Giới thiệu bối cảnh doanh nghiệp và bài toán giải quyết.
  * Bảng ánh xạ 7 tiêu chí đánh giá vào từng module kỹ thuật.
  * Sơ đồ kiến trúc Mermaid Diagram (Luồng dữ liệu giữa User, Guardrails, Multi-Agent LangGraph, CSDL SQL, ChromaDB, Cloud/Local LLM).
  * Cấu trúc cây thư mục chuẩn và hướng dẫn khởi chạy nhanh.
  * Commit: `docs: update README with Tier S+ LegalTech SME Assistant project overview` (Đã push lên GitHub).

### 5. Xây dựng Bản Checklist Sản phẩm Bàn giao (Project Deliverables)
* Tạo file [`requirements/project_checklist.md`](../requirements/project_checklist.md):
  * Liệt kê chi tiết từng file mã nguồn, file dữ liệu, kịch bản kiểm thử, báo cáo Ragas, slide và đồ án cần nộp.
  * Commit: `docs: add project deliverables and completion checklist` (Đã push lên GitHub).

### 6. Hiện thực hóa Module 1.1: Cloud & Local LLM Provider (2.5 điểm)
Xây dựng trọn bộ mã nguồn tầng Provider với khả năng chuyển đổi linh hoạt:
* **`llm_provider/cloud_provider.py`:**
  * Kết nối Google Gemini API (model mặc định: `gemini-1.5-flash`).
  * Hỗ trợ gọi trực tiếp qua Gemini REST API (không bắt buộc cài package ngoài) lẫn tích hợp LangChain `ChatGoogleGenerativeAI`.
  * Hỗ trợ các hàm `generate()`, `stream()` (hiển thị câu trả lời dạng gõ chữ) và `is_available()`.
* **`llm_provider/local_provider.py`:**
  * Kết nối Ollama nội bộ qua cổng `http://localhost:11434` (model: `qwen2.5:latest` hoặc `llama3.1:latest`).
  * Tự động kiểm tra trạng thái hoạt động của Ollama (`is_available()`) và danh sách model đã tải (`list_models()`).
  * Hỗ trợ hàm `generate()` và `stream()`.
* **`llm_provider/model_factory.py`:**
  * Áp dụng **Factory Pattern** và **Model Switcher** cho phép đổi model runtime bằng một dòng code hoặc nút gạt trên UI (`set_provider("cloud" | "local")`).
  * Tích hợp hàm `check_health()` trả về trạng thái kết nối của cả 2 môi trường để hiển thị lên Dashboard.
  * Cơ chế **Auto-fallback:** Tự động dự phòng sang Cloud nếu Local bị tắt hoặc lỗi kết nối.
* **Các file phụ trợ:**
  * `llm_provider/__init__.py`: Package export cho việc import module sạch sẽ.
  * `.env.example`: Hướng dẫn cấu hình API Key và model name.
  * `.gitignore`: Loại bỏ cache `__pycache__`, file ảo `.venv` và file bí mật `.env`.
* **Kiểm thử tự động:** Đã chạy script test `python -c "from llm_provider import ModelFactory; ..."` và hàm `check_health()` phản hồi chính xác 100%.

### 7. Tái cấu trúc (Refactor) Thư mục Mã nguồn
* Theo yêu cầu của người dùng, thực hiện chuyển đổi cấu trúc:
  * Di chuyển toàn bộ các file từ `src/llm_providers/` sang thư mục gốc [`llm_provider/`](../llm_provider/).
  * Cập nhật đánh dấu hoàn thành `[x]` cho 3 mục của phần 1.1 trong checklist.
  * Commit: `refactor: move llm provider files to llm_provider folder` (Đã push lên GitHub).

---

## 📂 Cấu trúc Thư mục Hiện tại của Repository

```
LLM_Nhut/
├── ai-log/
│   └── activity_log.md          # [Mới tạo] Toàn bộ nhật ký hoạt động chi tiết
├── llm_provider/                # Module Cloud & Local LLM Provider (Tiêu chí 3: 2.5đ)
│   ├── __init__.py              # Export module
│   ├── cloud_provider.py        # Tích hợp Google Gemini API
│   ├── local_provider.py        # Tích hợp Ollama Local API
│   └── model_factory.py         # Factory Pattern & Model Switcher
├── requirements/                # Tài liệu yêu cầu & kế hoạch dự án
│   ├── project_checklist.md     # Danh sách output cần có & tiến độ hoàn thành
│   └── project_requirements.md  # Chi tiết 7 tiêu chí chấm điểm của giảng viên
├── .env.example                 # File mẫu cấu hình biến môi trường
├── .gitignore                   # Cấu hình bỏ qua cache và file nhạy cảm
├── LICENSE                      # Giấy phép mã nguồn mở MIT
└── README.md                    # Tài liệu tổng quan dự án chính thức
```

---

## 🚀 Lịch sử Commit trên Nhánh `main`
1. `docs: add project requirements and grading criteria`
2. `docs: update README with Tier S+ LegalTech SME Assistant project overview`
3. `docs: add project deliverables and completion checklist`
4. `feat(llm): implement cloud provider, local provider, and model factory switcher`
5. `chore: add .gitignore and untrack pycache`
6. `refactor: move llm provider files to llm_provider folder`
