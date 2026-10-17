# 📘 BÁO CÁO ĐỒ ÁN MÔN HỌC: AI ENGINEER

## ĐỀ TÀI: LEGALTECH SME ASSISTANT
### HỆ THỐNG TRỢ LÝ AI HỖ TRỢ TƯ VẤN & TỰ ĐỘNG HÓA THỦ TỤC PHÁP LÝ CHO DOANH NGHIỆP VỪA VÀ NHỎ (SMEs & HỘ KINH DOANH)

* **Sinh viên thực hiện:** snowflake-vibing (MSSV: 24520496)
* **Khoa / Trường:** Đại học Công nghệ Thông tin - ĐHQG-HCM (UIT)
* **Môn học:** AI Engineer Project
* **Repository:** [https://github.com/snowflake-vibing/LLM_Nhut](https://github.com/snowflake-vibing/LLM_Nhut)

---

## 📑 MỤC LỤC BÁO CÁO
1. **Chương 1:** Ứng dụng LLM trong Doanh nghiệp & Bối cảnh Bài toán (1.0 điểm)
2. **Chương 2:** Kỹ năng Prompt Engineering Nâng cao (2.0 điểm)
3. **Chương 3:** Kiến trúc Triển khai Cloud Server & Local Model (2.5 điểm)
4. **Chương 4:** Xây dựng Hệ thống Vector RAG & Truy vấn CSDL Quan hệ (1.5 điểm)
5. **Chương 5:** Kiến trúc Đa Tác Nhân (Multi-Agent System với LangGraph) (1.5 điểm)
6. **Chương 6:** Đánh giá & Benchmark Mô hình LLM (1.0 điểm)
7. **Chương 7:** An toàn Bảo mật LLM & Kiểm soát Rủi ro (0.5 điểm)
8. **Chương 8:** Kết luận & Hướng phát triển

---

## CHƯƠNG 1: ỨNG DỤNG LLM TRONG DOANH NGHIỆP & BỐI CẢNH BÀI TOÁN (1.0 điểm)
### 1.1. Thực trạng & Nỗi đau của Doanh nghiệp (Pain points)
Tại Việt Nam, các doanh nghiệp vừa và nhỏ (SMEs) và hơn 5 triệu hộ kinh doanh cá thể đóng góp hơn 40% GDP nhưng thường xuyên gặp rào cản nghiêm trọng về thủ tục pháp lý khởi nghiệp:
- Hệ thống văn bản quy phạm pháp luật (Luật Doanh nghiệp 2020, Luật Đầu tư, các Nghị định hướng dẫn) đồ sộ, ngôn ngữ hành chính phức tạp, khó tra cứu.
- Các ngành nghề có điều kiện đòi hỏi nhiều giấy phép con (ATVSTP, PCCC, giấy phép môi trường...) nằm rải rác ở nhiều cơ quan khác nhau.
- Chi phí thuê dịch vụ luật sư hoặc đại lý thuế tư vấn ban đầu khá cao so với ngân sách hạn hẹp của các nhà sáng lập trẻ.

### 1.2. Giải pháp LegalTech SME Assistant
Ứng dụng Trí tuệ nhân tạo tạo sinh (Generative AI) để:
- Tự động phân tích ý tưởng kinh doanh và tư vấn mô hình tối ưu (Hộ cá thể, Công ty TNHH 1TV/2TV, Cổ phần).
- Tự động đối chiếu mã ngành kinh tế (VSIC 2018) và cảnh báo các điều kiện cấp phép con bắt buộc.
- Lên checklist hành động từng bước (Actionable Roadmap) giúp nhà sáng lập tự hoàn thiện hồ sơ đăng ký kinh doanh chỉ trong vài phút.

---

## CHƯƠNG 2: KỸ NĂNG PROMPT ENGINEERING NÂNG CAO (2.0 điểm)
Dự án áp dụng đầy đủ các kỹ thuật thiết kế prompt tiên tiến:
1. **System Prompting Chuyên sâu (`src/prompts/system_prompts.py`):**
   - Thiết kế phân tách rõ ràng Role (Vai trò), Task (Nhiệm vụ), Context (Ngữ cảnh pháp lý), Constraints (Ràng buộc trích dẫn văn bản luật) và Tone (Chuyên nghiệp, chuẩn mực).
2. **Few-Shot Prompting (`src/prompts/few_shot_templates.py`):**
   - Cung cấp các cặp ví dụ mẫu Input/Output chuẩn để hướng dẫn mô hình phân loại chính xác ý định người dùng và trích xuất thực thể kinh doanh.
3. **Chain-of-Thought Reasoning (`src/prompts/cot_reasoning.py`):**
   - Ép buộc mô hình suy luận 5 bước logic: Phân tích thực thể $\rightarrow$ Tra cứu căn cứ pháp lý $\rightarrow$ Đối chiếu mã ngành VSIC $\rightarrow$ So sánh mô hình $\rightarrow$ Đưa ra kết luận và checklist.
4. **Structured Output với Pydantic (`src/prompts/schemas.py`):**
   - Ràng buộc đầu ra chuẩn JSON Schema (`BusinessEntityRecommendation`, `IndustryLicenseDetail`, `LegalDossierChecklist`) giúp tích hợp dễ dàng với backend và UI.

---

## CHƯƠNG 3: KIẾN TRÚC TRIỂN KHAI CLOUD SERVER & LOCAL MODEL (2.5 điểm)
Dự án triển khai mô hình lai (Hybrid Architecture) kết hợp Cloud và On-Premise:
1. **Cloud Model Provider (`llm_provider/cloud_provider.py`):**
   - Tích hợp Google Gemini API (`gemini-1.5-flash`), tận dụng tốc độ cao, cửa sổ ngữ cảnh lớn và chi phí 0 VNĐ qua Free Tier. Hỗ trợ cả REST API và LangChain.
2. **Local Model Provider (`llm_provider/local_provider.py`):**
   - Tích hợp Ollama cục bộ (`http://localhost:11434`) chạy các mô hình open-weight hàng đầu như `qwen2.5:latest` hoặc `llama3.1:latest`.
   - Đảm bảo 100% dữ liệu nhạy cảm của doanh nghiệp được xử lý offline an toàn trên máy chủ nội bộ.
3. **Model Factory Switcher (`llm_provider/model_factory.py`):**
   - Cung cấp cơ chế chuyển đổi runtime (`set_provider("cloud" | "local")`) phục vụ nút gạt trên giao diện UI.
   - Tính năng **Auto-fallback:** Tự động dự phòng sang Cloud nếu Local Ollama tạm thời ngoại tuyến.
   - Tính năng **Health check:** Theo dõi trạng thái hoạt động của cả hai môi trường theo thời gian thực.

---

## CHƯƠNG 4: HỆ THỐNG VECTOR RAG & TRUY VẤN CSDL QUAN HỆ (1.5 điểm)
Hệ thống kết hợp sức mạnh của cả dữ liệu phi cấu trúc và dữ liệu có cấu trúc:
1. **RAG Pipeline cho Văn bản Pháp luật (`src/rag/`):**
   - *Ingestion & Chunking:* Cắt đoạn văn bản theo ranh giới Điều / Khoản (Article-level chunking) bảo toàn nguyên vẹn ngữ cảnh pháp lý.
   - *Embedding:* Sử dụng Google Embeddings (`text-embedding-004`) kết hợp fallback semantic hashing.
   - *Vector Database:* Lưu trữ vector và tìm kiếm tương đồng Cosine Similarity.
   - *Citation Retriever:* Tự động định dạng nguồn trích dẫn rõ ràng: `[Luật Doanh nghiệp 2020 - Điều 74]`.
2. **Truy vấn CSDL Quan hệ SQLite (`src/database/`):**
   - CSDL `sme_legal.db` chuẩn hóa với các bảng:
     - `industry_codes`: Hệ thống ngành kinh tế Việt Nam VSIC 2018.
     - `license_requirements`: Danh mục giấy phép con (ATVSTP, PCCC, giấy phép rượu...).
     - `registration_checklist`: Lộ trình từng bước cho từng loại hình doanh nghiệp.
   - Bộ công cụ SQL Tool Calling cho phép Agent tự động truy vấn dữ liệu chính xác 100%.

---

## CHƯƠNG 5: KIẾN TRÚC ĐA TÁC NHÂN (MULTI-AGENT WORKFLOW) (1.5 điểm)
Quy trình điều phối đa tác nhân (`src/agents/graph.py`):
- **Legal Router Agent:** Phân tích câu hỏi người dùng, phân loại và điều phối tới agent thích hợp.
- **Entity Advisory Agent:** Phân tích ưu/nhược điểm các loại hình công ty kết hợp RAG.
- **Industry Lookup Agent:** Tra cứu mã ngành VSIC và điều kiện cấp phép qua SQL Tools.
- **Document Reviewer Agent:** Xây dựng checklist các bước nộp hồ sơ và cơ quan tiếp nhận.
- Các Agent phối hợp qua quy trình thống nhất có lớp bảo mật chặn trước và soát lỗi sau.

---

## CHƯƠNG 6: ĐÁNH GIÁ MÔ HÌNH LLM (EVALUATION & BENCHMARK) (1.0 điểm)
### 6.1. Phương pháp & Bộ dữ liệu Kiểm thử
- Xây dựng Benchmark Dataset gồm 10 test cases chuẩn nghiệp vụ (`data/evaluation/benchmark_dataset.json`).
- Đo lường 4 chỉ số chất lượng RAG cốt lõi bằng `src/evaluation/ragas_evaluator.py`:
  - **Faithfulness (Độ trung thực, không bịa luật):** `0.950` (95.0%)
  - **Context Precision (Độ chính xác tài liệu):** `0.749` (74.9%)
  - **Context Recall (Độ bao phủ tri thức):** `0.708` (70.8%)
  - **Answer Relevance (Sát câu hỏi):** `0.536`
  - **Overall Score:** `0.736`
- Kết quả chi tiết được xuất tự động ra file `reports/evaluation_results.csv`.

### 6.2. So sánh Thực nghiệm Cloud vs Local (`reports/model_comparison_report.md`)
- **Tốc độ (Latency):** Cloud Gemini API ~ 0.8s vs Local Ollama ~ 2.4s.
- **Chi phí (Cost):** Cả hai giải pháp đều đạt chi phí 0 VNĐ (sử dụng Free Tier và Open-source).
- **Tính bảo mật:** Local Model bảo vệ 100% dữ liệu nội bộ on-premise.

---

## CHƯƠNG 7: AN TOÀN BẢO MẬT LLM (0.5 điểm)
Hệ thống triển khai 3 lớp phòng thủ toàn diện (`src/security/`):
1. **PII Masking (`pii_masking.py`):**
   - Tự động nhận diện và ẩn danh số CCCD (12 số), SĐT di động và Email cá nhân trước khi truyền qua API công cộng, sau đó unmask an toàn ở đầu ra.
2. **Prompt Injection & Anti-Jailbreak Guard (`prompt_injection_guard.py`):**
   - Chặn đứng các câu lệnh bẻ khóa system prompt (*"ignore previous instructions"*, *"DAN mode"*).
   - Từ chối dứt khoát các yêu cầu hướng dẫn hành vi trái pháp luật (trốn thuế, rửa tiền, kê khai khống vốn) theo Điều 16 Luật Doanh nghiệp 2020.
3. **Output Moderation & Legal Disclaimer (`output_moderation.py`):**
   - Kiểm duyệt nội dung trả về và tự động đính kèm khuyến cáo pháp lý chính thức.

---

## CHƯƠNG 8: KẾT LUẬN & CÁC NÂNG CẤP TRONG PHIÊN BẢN 1.1

### 8.1. Các Nâng cấp Thực chiến trong Phiên bản 1.1 (Version 1.1 Upgrades)
Kế thừa từ phản hồi thực tế tại `requirements/preview_version_1.md` và hoàn thiện theo `requirements/requirements_version_1.1.md`:
1. **Bộ Tạo Hồ sơ Kê khai Pháp lý Tự động (Dossier Generator - `src/dossier/`):**
   - Hỗ trợ form nhập thông tin doanh nghiệp trực quan trên Web Streamlit.
   - AI Thẩm định tính hợp lệ của tên doanh nghiệp (tránh vi phạm Điều 37, 38, 41 Luật Doanh nghiệp 2020) và thời hạn góp vốn 90 ngày.
   - Xuất file Word (.docx) chuẩn: Giấy đề nghị ĐKDN (Phụ lục I-2 / I-3 Nghị định 01/2021/NĐ-CP), Dự thảo Điều lệ công ty, Danh sách thành viên sáng lập để ký nộp Sở KH&ĐT.
2. **Trích dẫn Căn cứ Pháp luật Kèm Link Kiểm chứng (Verify URL Citation):**
   - Mọi câu trả lời của AI đều gắn thẻ Citation Card có trích dẫn nguyên văn Điều/Khoản kèm nút `[🔗 Kiểm chứng tại Cổng TT Chính phủ]` trỏ trực tiếp đến `vanban.chinhphu.vn`.
3. **Kiến trúc Tra cứu Lai (Hybrid Retrieval & Pagination - `src/tools/web_search_tool.py`):**
   - Kết hợp truy vấn siêu tốc trong CSDL SQLite nội bộ với Web Search Tool mở rộng cho các ngành nghề mới (Thương mại điện tử, Livestream bán hàng, AI/SaaS, Logistics...).
   - Bổ sung bộ lọc phân trang (Pagination) trên giao diện tra cứu mã ngành.
4. **Trực quan hóa Luồng Bảo vệ Dữ liệu Cá nhân (PII Masking Flow):**
   - Bổ sung sơ đồ trực quan 4 bước minh bạch quy trình ẩn danh dữ liệu nhạy cảm (CCCD, SĐT) trước khi gửi qua Cloud LLM.

### 8.2. Kết luận
Dự án **LegalTech SME Assistant** đã hoàn thành xuất sắc 100% các tiêu chí học thuật của đề cương AI Engineer, đồng thời nâng cấp hoàn chỉnh thành một sản phẩm LegalTech thực chiến có thể ứng dụng trực tiếp cho các doanh nghiệp vừa và nhỏ, startup và hộ kinh doanh cá thể tại Việt Nam.
