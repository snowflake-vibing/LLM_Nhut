# 📑 BẢN ĐẶC TẢ YÊU CẦU KỸ THUẬT PHIÊN BẢN 2.2 (REQUIREMENTS VERSION 2.2)
### ⚖️ DỰ ÁN: LEGALTECH PLATFORM • LANGGRAPH MULTI-AGENT STATEFUL ENGINE & AUTOMATED WATCHDOG
> 📌 **Ngày ban hành:** 01/11/2026 | **Kế thừa:** `preview_version_2.1.md` và quy chuẩn `RULES.md`

---

## 🎯 MỤC TIÊU PHÁT TRIỂN (SPRINT GOALS)

Nâng cấp lõi điều phối Multi-Agent của hệ thống LegalTech từ luồng điều phối tùy biến sang **thư viện LangGraph chính thức (`langchain-ai/langgraph`)**, kết hợp cơ chế kiểm tra tự động định kỳ (Hourly Watchdog Agent):
1. **Official LangGraph Architecture:** Triển khai `StateGraph(LegalAgentState)` với các Node độc lập, rẽ nhánh điều kiện (*Conditional Edges*), thu thập Citations và chuẩn hóa Guardrails.
2. **Interactive Graph Visualization:** Cung cấp sơ đồ Mermaid thể hiện trực quan toàn bộ mạng lưới tác nhân LangGraph ngay trên giao diện Web Streamlit.
3. **Hourly Watchdog & Health Check Suite:** Cung cấp script tự động kiểm tra định kỳ sức khỏe của hệ thống tác nhân và cơ sở dữ liệu.
4. **Chuẩn hóa Dependencies:** Tạo file `requirements.txt` đầy đủ, đảm bảo cài đặt và chạy tức thì trên mọi môi trường.

---

## 📋 CHI TIẾT CÁC TÁC VỤ KỸ THUẬT (SPRINT BACKLOG)

### SPRINT 1: XÂY DỰNG LÕI ĐIỀU PHỐI LANGGRAPH (`src/agents/graph.py`)
- [x] **Task 1.1:** Định nghĩa `LegalAgentState(TypedDict)` bao gồm các trường:
  - `raw_query`: Câu hỏi/yêu cầu gốc của người dùng.
  - `masked_query`: Chuỗi sau khi che giấu PII.
  - `pii_mapping`: Bảng ánh xạ phục hồi thông tin cá nhân.
  - `intent`: Ý định được phân loại (`SOCIAL_CASE_ADVISORY`, `DYNAMIC_DRAFT`, `CONTRACT_AUDIT`, `DOSSIER_CREATION`, `INDUSTRY_LOOKUP`, `REGISTRATION_STEPS`, `ENTITY_ADVISORY`).
  - `active_agent`: Tên tác nhân đang trực tiếp phản hồi.
  - `response`: Văn bản phản hồi trung gian và hoàn thiện.
  - `citations`: Danh sách trích dẫn căn cứ pháp lý.
  - `action_type`: Mã hành động In-Chat tương tác (`DYNAMIC_DRAFT_ACTION`, `CONTRACT_AUDIT_ACTION`, `DOSSIER_CREATION_ACTION`, v.v.).
  - `action_data`: Dữ liệu đính kèm cho widget tương tác.
  - `is_safe`: Cờ kiểm tra an toàn Guardrails.
  - `error`: Thông báo lỗi nếu vi phạm an toàn hoặc ngoại lệ.
- [x] **Task 1.2:** Triển khai các Node xử lý độc lập:
  - `guardrail_node`: Chạy PromptInjectionGuard & PIIMasker.
  - `router_node`: RouterAgent phân tích ý định.
  - `social_case_node`: SocialCasesKnowledgeEngine xử lý 4 case đời sống.
  - `contract_audit_node`: ContractVulnerabilityScanner bóc tách đối kháng 2 chiều.
  - `dynamic_draft_node`: Kích hoạt Smart Form điền sẵn căn cứ pháp luật.
  - `dossier_node`: Hồ sơ thành lập doanh nghiệp theo Nghị định 01/2021/NĐ-CP.
  - `industry_lookup_node`: Tra cứu ngành nghề kinh doanh và điều kiện gia nhập thị trường.
  - `registration_steps_node`: Quy trình đăng ký và thủ tục hành chính.
  - `advisory_node`: RAG tư vấn pháp lý chuyên sâu.
  - `moderator_node`: Khôi phục PII, kiểm duyệt văn phong và gắn Disclaimer tư pháp.
- [x] **Task 1.3:** Kết nối Graph bằng `StateGraph`, `START`, `END` và hàm `route_decision` cho Conditional Edges.
- [x] **Task 1.4:** Biên dịch đồ thị (`workflow.compile()`) và cung cấp phương thức `get_mermaid_code()` để trích xuất mã Mermaid trực quan.

---

### SPRINT 2: HIỂN THỊ SƠ ĐỒ ĐỒ THỊ LANGGRAPH TRÊN GIAO DIỆN WEB (`app/main.py`)
- [x] **Task 2.1:** Tại Tab 2 (🧰 Legal Tools Studio), thêm mục **"🌐 Sơ đồ Mạng lưới Đa tác nhân LangGraph (Stateful Graph Visualizer)"** hiển thị đồ thị tương tác.
- [x] **Task 2.2:** Tại Tab 1 (💬 AI Legal Chatbot), hiển thị metadata về chuỗi Node LangGraph đã kích hoạt khi thực thi yêu cầu của người dùng.

---

### SPRINT 3: XÂY DỰNG HOURLY WATCHDOG SCRIPT (`scripts/hourly_agent_watchdog.py`)
- [x] **Task 3.1:** Viết script kiểm tra tự động:
  - Kiểm tra trạng thái Model Cloud Gemini và Model Local Ollama.
  - Kiểm tra Vector Store (số lượng chunks và độ nguyên vẹn của index).
  - Chạy thử nghiệm 1 chu trình LangGraph giả lập end-to-end.
  - Ghi log ra file `reports/watchdog_log.txt` với timestamp chuẩn ISO.

---

### SPRINT 4: ĐỒNG BỘ DEPENDENCIES, HƯỚNG DẪN & GIT SYNC
- [x] **Task 4.1:** Tạo file `requirements.txt` chuẩn hóa ở thư mục gốc.
- [x] **Task 4.2:** Viết hướng dẫn kiểm thử chi tiết `tutorial/run_guide_version_2.2.md`.
- [x] **Task 4.3:** Cập nhật `README.md` thể hiện phiên bản Version 2.2, sơ đồ LangGraph và các hướng dẫn chạy mới nhất.
- [x] **Task 4.4:** Chạy kiểm thử hồi quy (Regression Test) đảm bảo 100% chức năng hoạt động hoàn hảo.
- [x] **Task 4.5:** Thực hiện Git Commit theo chuẩn Conventional Commits và `git push origin main` lên GitHub repository `https://github.com/snowflake-vibing/LLM_Nhut`.
