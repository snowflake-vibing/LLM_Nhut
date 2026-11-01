# 📋 ĐÁNH GIÁ PHIÊN BẢN 2.1 & ĐỊNH HƯỚNG NÂNG CẤP (PREVIEW VERSION 2.1)
### ⚖️ DỰ ÁN: LEGALTECH PLATFORM • BƯỚC TIẾN CHÍNH THỨC SANG HỆ ĐIỀU PHỐI LANGGRAPH CHUẨN MỰC
> 📌 **Tài liệu tham chiếu:** Kế thừa từ kết quả kiểm thử và phản hồi của người dùng ngày 01/11/2026 về việc tích hợp mã nguồn chuẩn `langchain-ai/langgraph` và cơ chế giám sát tự động định kỳ (Hourly Watchdog).

---

## 📌 I. TỔNG QUAN PHẢN HỒI VÀ YÊU CẦU NÂNG CẤP TỪ NGƯỜI DÙNG

Sau khi phiên bản **Version 2.1 (The Legal AI Lawyer & Studio Platform)** hoàn thành với kiến trúc 2 Tab chuẩn NotebookLM, người dùng đưa ra định hướng chiến lược tiếp theo:
1. **Tích hợp chính thức Framework LangGraph (`langchain-ai/langgraph`):**
   * Chuyển hóa toàn bộ quy trình Multi-Agent từ code logic rẽ nhánh thông thường sang mô hình **Stateful Graph** của thư viện LangGraph chuẩn mực quốc tế (`StateGraph`, `START`, `END`, `TypedDict` AgentState, Conditional Edges).
   * Trực quan hóa đồ thị thực thi tác nhân (Agent Execution Graph Diagram) ngay trên giao diện web bằng Mermaid để người dùng và Hội đồng phản biện UIT quan sát trực tiếp luồng suy luận của từng tác nhân.
2. **Cơ chế Giám sát & Tự hành Định kỳ (Hourly Agent Watchdog & Cron Scheduler):**
   * Người dùng là người khởi xướng ý tưởng (Ideator / Product Owner).
   * Hệ thống AI Agent đóng vai trò kỹ sư tự hành (Autonomous Lead Engineer), định kỳ mỗi 1 giờ tự động chạy test kiểm tra sức khỏe hệ thống (Model Cloud/Local, Vector Store, Multi-Agent workflow, Git status) và báo cáo.

---

## 🔬 II. PHÂN TÍCH KỸ THUẬT DƯỚI GÓC ĐỘ ĐỀ CƯƠNG UIT (7 TIÊU CHÍ)

| Tiêu chí UIT | Hiện trạng tại Version 2.1 | Đột phá khi tích hợp LangGraph tại Version 2.2 |
| :--- | :--- | :--- |
| **1. Ứng dụng Doanh nghiệp (1.0đ)** | Soạn hồ sơ và bóc tách hợp đồng đối kháng 2 chiều. | Bổ sung State Checkpointer lưu trữ trạng thái phiên tư vấn dài kỳ của doanh nghiệp. |
| **2. Prompting Skills (2.0đ)** | CoT, Few-shot và Structured Output chuẩn JSON. | Từng Node trong LangGraph sở hữu Prompt Template chuyên biệt hóa sâu theo từng nghiệp vụ. |
| **3. Model Switcher (2.5đ)** | Chuyển đổi linh hoạt Gemini Cloud & Ollama Local. | StateGraph độc lập hoàn toàn với Provider, cho phép từng Node chạy model khác nhau nếu cần. |
| **4. Vector DB & RAG (1.5đ)** | 53 chunks đa luật (Dân sự, Đất đai, HNGĐ, Doanh nghiệp). | LangGraph Node kết hợp truy xuất Vector DB + CSDL SQLite một cách tuần tự và minh bạch. |
| **5. AI Agents & Đa Tác Nhân (1.5đ)** | Router gọi function thủ công (`if/elif`). | ⭐ **NÂNG TẦM ĐẲNG CẤP VÀNG:** Sử dụng chính thức `langgraph.graph.StateGraph`, `TypedDict` State, Conditional Edges chuẩn quốc tế, xuất sơ đồ Mermaid trực quan thời gian thực. |
| **6. Benchmark Ragas (1.0đ)** | Bộ test Ragas đánh giá độ trung thực và liên quan. | Kiểm thử tự động trên đồ thị LangGraph với điểm đánh giá đầu ra của từng Node. |
| **7. Bảo mật LLM (0.5đ)** | Guardrails PII Masking và Anti-Jailbreak. | Tích hợp thành `guardrail_node` đầu vào và `moderator_node` đầu ra bắt buộc trong đồ thị LangGraph. |

---

## 🚀 III. ĐỀ XUẤT LỘ TRÌNH CHO VERSION 2.2 (THE STATEFUL LANGGRAPH ORCHESTRATION)

Để đảm bảo tính nhất quán và hoàn thiện tối đa, các hạng mục cần triển khai trong `requirements_version_2.2.md`:
1. **Thiết lập `LegalAgentState`:** Định nghĩa kiểu dữ liệu trạng thái (`TypedDict`) truyền nhận giữa các Node trong đồ thị.
2. **Xây dựng `LegalMultiAgentStateGraph`:**
   - `guardrail_node` $\rightarrow$ `router_node` $\rightarrow$ (Rẽ nhánh điều kiện conditional edges) $\rightarrow$ Node chuyên môn (`social_case_node`, `contract_audit_node`, `dynamic_draft_node`, `dossier_node`, `industry_lookup_node`, `entity_advisory_node`) $\rightarrow$ `moderator_node` $\rightarrow$ `END`.
3. **Mermaid Graph Visualizer:** Thêm component hiển thị sơ đồ trực quan của đồ thị tác nhân LangGraph ngay tại Tab 2 (Legal Tools Studio) và trong bong bóng chat.
4. **Tạo `requirements.txt` chuẩn hóa:** Khai báo chính thức `langgraph>=0.2.0`, `langchain-core`, `google-genai`, `streamlit`, `python-docx`, `chromadb`.
5. **Kịch bản Watchdog 1 Giờ:** Script `scripts/hourly_agent_watchdog.py` phục vụ kiểm tra tự động và ghi nhật ký định kỳ.
6. **Đồng bộ tài liệu & Git:** Cập nhật `README.md`, `tutorial/run_guide_version_2.2.md`, commit và push lên repository `snowflake-vibing/LLM_Nhut`.
