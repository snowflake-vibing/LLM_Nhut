# 🧪 HƯỚNG DẪN KIỂM THỬ PHIÊN BẢN 2.2 (TEST & RUN GUIDE VERSION 2.2)
### ⚖️ DỰ ÁN: LEGALTECH PLATFORM • HỆ ĐIỀU PHỐI LANGGRAPH CHUẨN QUỐC TẾ & TỰ HÀNH ĐỊNH KỲ
> 📌 **Phiên bản:** Version 2.2 | **Môi trường:** Python 3.10+ • Streamlit • `langgraph>=0.2.0`

---

## 🎯 I. TỔNG QUAN NÂNG CẤP TẠI VERSION 2.2

Trong phiên bản Version 2.2, hệ thống đã chính thức tích hợp kho mã nguồn **`langchain-ai/langgraph`** trực tiếp vào lõi xử lý:
1. **Lõi Đa tác nhân LangGraph có trạng thái (`LegalAgentState`):**
   * Định hình quy trình xử lý thông qua `StateGraph`, `START`, `END` và cơ chế rẽ nhánh điều kiện (*Conditional Routing*).
   * 100% các Agent (Router, Bóc tách Hợp đồng, 4 Tình huống Xã hội, Soạn thảo Biểu mẫu, Tra cứu Ngành nghề, Hồ sơ DN) hoạt động dưới dạng các Node độc lập.
2. **Trực quan hóa Đồ thị Tác nhân (Mermaid Graph Visualizer):**
   * Tích hợp công cụ thứ 9 trong **Tab 2: 🧰 Legal Tools Studio**, hiển thị toàn bộ đồ thị mạng lưới tác nhân LangGraph và cho phép kích hoạt chạy kiểm thử trực tiếp trên giao diện web.
3. **Bộ Tự hành & Giám sát Định kỳ (Autonomous Hourly Watchdog Suite):**
   * Module `scripts/hourly_agent_watchdog.py` tự động kiểm tra Model Cloud/Local, số lượng vector chunks, chạy regression test và ghi log tại `reports/watchdog_log.txt`.
4. **Chuẩn hóa File Cấu hình:**
   * Cung cấp file `requirements.txt` chuẩn hóa để cài đặt dự án chỉ với một dòng lệnh.

---

## 🚀 II. HƯỚNG DẪN KHỞI CHẠY HỆ THỐNG

### 1. Cài đặt môi trường & Thư viện:
```bash
# Kích hoạt virtual environment
.\venv\Scripts\activate

# Cài đặt toàn bộ thư viện cần thiết (bao gồm langgraph)
pip install -r requirements.txt
```

### 2. Khởi chạy Ứng dụng Web:
```bash
streamlit run app/main.py
```
*Truy cập trình duyệt tại địa chỉ:* `http://localhost:8501`

---

## 🔬 III. KỊCH BẢN KIỂM THỬ THỰC TẾ (TEST SUITE)

### KỊCH BẢN 1: Kiểm tra Đồ thị LangGraph trên Web (Tab 2: Studio)
1. Truy cập Web `http://localhost:8501`.
2. Chuyển sang **Tab 2: 🧰 Legal Tools Studio**.
3. Tại menu xổ xuống, chọn **`9. 🌐 LangGraph Multi-Agent Visualizer (Sơ đồ Mạng lưới Tác nhân LangGraph)`**.
4. **Kỳ vọng:**
   - Hệ thống hiển thị tài liệu kiến trúc LangGraph StateGraph.
   - Sơ đồ mạng lưới tác nhân dạng Mermaid kết nối từ `guardrail_node` $\rightarrow$ `router_node` $\rightarrow$ 7 nhánh chuyên môn $\rightarrow$ `moderator_node` $\rightarrow$ `END`.
   - Bấm nút **"🚀 Chạy Kiểm thử Watchdog Trực tiếp ngay bây giờ"**: Giao diện hiển thị kết quả kiểm tra Model, 53 Chunks Vector DB và 3 kịch bản Agent PASS 100%.

---

### KỊCH BẢN 2: Kiểm thử LangGraph Điều phối Tình huống Xã hội (Tab 1: Chatbot)
1. Tại **Tab 1: 💬 AI Legal Chatbot & Command Center**, nhập:
   > *"Tôi và chồng chuẩn bị ly hôn, có một bé gái 2 tuổi và căn nhà chung mua sau hôn nhân. Cho tôi hỏi về quyền nuôi con và chia tài sản."*
2. **Kỳ vọng:**
   - LangGraph kích hoạt `guardrail_node` (kiểm tra an toàn) $\rightarrow$ `router_node` nhận diện intent `SOCIAL_CASE_ADVISORY` $\rightarrow$ chuyển tiếp tới `social_case_node` $\rightarrow$ `moderator_node`.
   - Chatbot phản hồi chi tiết:
     - Con dưới 36 tháng tuổi ưu tiên giao cho người mẹ trực tiếp nuôi dưỡng (Khoản 3 Điều 81 Luật Hôn nhân & Gia đình 2014).
     - Căn nhà chung chia đôi có tính đến công sức đóng góp (Điều 59).
   - Ngay trong bong bóng chat hiển thị **Biểu mẫu Tự động Soạn thảo Văn bản Thông minh (Placeholder Form)** cho phép người dùng điền thông tin và tải file Word (.docx) dùng ngay.

---

### KỊCH BẢN 3: Kiểm thử Thẩm định Hợp đồng Đối kháng 2 Chiều qua LangGraph (Tab 1)
1. Tại khung chat Tab 1, nhập đoạn điều khoản:
   > *"Thẩm định giúp tôi điều khoản: Bên A có toàn quyền phạt Bên B 40% giá trị hợp đồng nếu chậm tiến độ 3 ngày và Bên B phải bồi thường vô điều kiện."*
2. **Kỳ vọng:**
   - LangGraph kích hoạt `contract_audit_node`.
   - Hệ thống xuất kết quả phân tích 2 chiều:
     - **Bên A (Bên ra luật):** Lợi dụng từ ngữ để áp đặt chế tài vượt trần luật định.
     - **Bên B (Bên theo luật):** Bị ép vào thế bất lợi; có quyền căn cứ Điều 301 Luật Thương mại 2005 (mức phạt tối đa chỉ là 8%) để phản đòn và yêu cầu hủy bỏ điều khoản phạt 40%.
   - Điểm rủi ro hiển thị trực quan và cho phép xuất Báo cáo Thẩm định Word (.docx).

---

### KỊCH BẢN 4: Chạy Watchdog Tự động từ Dòng lệnh (CLI)
Mở PowerShell và chạy:
```powershell
python scripts/hourly_agent_watchdog.py
```
**Kỳ vọng đầu ra:**
```text
==================================================
⏱️ WATCHDOG EXECUTION AT: 2026-11-01 ...
==================================================

[1/4] Checking Model Providers...
 - Cloud Gemini (gemini-3.5-flash-lite): ✅ AVAILABLE
 - Local Ollama (qwen2.5:latest): ✅ AVAILABLE

[2/4] Checking Legal Vector Store...
 - Total Indexed Legal Chunks: 53 ✅

[3/4] Testing LangGraph Multi-Agent Workflow...
 - Scenario 'Social Cases': Agent [SocialCasesAdvisoryAgent (LangGraph)] -> ✅ PASS
 - Scenario 'Contract Audit': Agent [ContractVulnerabilityScanner (LangGraph)] -> ✅ PASS
 - Scenario 'Guardrails': Agent [SecurityGuardrail] -> ✅ PASS

[4/4] Checking Git Repository Status...
 - Git working tree clean (Synced with main) ✅

==================================================
🎯 WATCHDOG CYCLE COMPLETED SUCCESSFULLY
==================================================
```
