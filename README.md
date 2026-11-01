# ⚖️ LegalTech Platform
### Trạm Làm Việc Pháp Lý Đa Năng In-Chat, Giám Định Chứng Cứ Đa Phương Tiện & Bộ Công Cụ Dân Sinh 1-Chạm • Phiên bản 4.0 (The In-Chat Multi-Tool Legal Workstation)

[![Version: 4.0](https://img.shields.io/badge/Version-4.0_(Major_Release_Multi--Tool_Workstation)-brightgreen.svg)](#quản-lý-phiên-bản--lộ-trình-versioning--roadmap)
[![Multimodal](https://img.shields.io/badge/Evidence-Multimodal_OCR_%26_Risk_Score-indigo.svg)](#)
[![In-Chat Tools](https://img.shields.io/badge/Tools-Court_Fee_%26_Statute_Checker-blue.svg)](#)
[![Dual Suggestions](https://img.shields.io/badge/UX-Dual_Action_Suggestions-orange.svg)](#)
[![Scope](https://img.shields.io/badge/Focus-Individuals_%26_Citizens-blueviolet.svg)](#tầm-nhìn-chiến-lược-project-vision)
[![Interaction](https://img.shields.io/badge/UX-Socratic_Step--by--Step_Intake-orange.svg)](#triết-lý-tương-tác-vàng-core-philosophy)
[![Accessibility](https://img.shields.io/badge/Accessibility-Senior_%26_Low--Tech_Mode-informational.svg)](#)
[![Privacy](https://img.shields.io/badge/Security-Zero--Trust_Panic_Wipe-red.svg)](#)
[![Audit Score](https://img.shields.io/badge/360°_Audit_Score-9.43%2F10.0-gold.svg)](#)
[![Antigravity](https://img.shields.io/badge/Orchestrator-Google_Antigravity-blue.svg)](https://deepmind.google/)
[![LangGraph](https://img.shields.io/badge/Multi--Agent-LangGraph_StateGraph-orange.svg)](https://github.com/langchain-ai/langgraph)
[![Telegram Daemon](https://img.shields.io/badge/Telegram_Bot-Real--time_Daemon_<1s-0088cc.svg)](https://telegram.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit_(2_Tabs_NotebookLM)-FF4B4B.svg)](https://streamlit.io/)

---

## 🎯 TẦM NHÌN CHIẾN LƯỢC (PROJECT VISION)

> **"Dân chủ hóa và nhân văn hóa công nghệ pháp lý cho mọi người dân Việt Nam."**  
> 
> Một sản phẩm LegalTech thực sự có giá trị không phải là một "tech-demo" phô diễn công nghệ dễ dãi, mà phải là sản phẩm **phục vụ được những người yếu thế nhất trong xã hội**:
> - **Người già & người ít thạo công nghệ:** Cần giao diện chữ lớn, tương phản cao, thao tác 1 chạm, không đòi hỏi kỹ năng số phức tạp.
> - **Người dân bình thường khi gặp biến cố:** Khi bị quỵt nợ, tranh chấp đất đai với hàng xóm, trục trặc hôn nhân hay bị lừa đảo qua mạng thường rất hoang mang, uất ức và "nói không đâu vào đâu". Họ không thể hiểu và sẽ sợ hãi nếu AI lập tức "xả" một tràng dài điều luật khô khan.
> - **Triết lý Thăm khám Từng bước (Socratic Intake):** AI đóng vai một **Vị Luật sư Dân gian Đồng hành** — biết lắng nghe, xoa dịu cảm xúc, hỏi từng bước (tối đa 1-2 câu ngắn) để nắm chắc tình tiết và bằng chứng trước khi kết luận, kèm các nút chọn nhanh (Quick-Reply Pills) để người dân chỉ cần bấm chọn.
> - **Phạm vi Doanh nghiệp & Công ty:** Tạm thời được đưa vào chế độ chờ (Standby) tại Studio để dự án dồn 100% tâm huyết giải quyết bài toán dân sinh đời sống trước mắt.

---

## 💡 TRIẾT LÝ TƯƠNG TÁC VÀNG (CORE INTERACTION PRINCIPLES)

```mermaid
flowchart TD
    A["👤 Người Dân Kể Câu Chuyện / Tâm Sự Hoang Mang"] --> B["👂 1. Lắng nghe & Trấn an cảm xúc (De-Noiser)"]
    B --> C["❓ 2. Hỏi 1-2 câu xác thực then chốt (Không dồn dập)"]
    C --> D["🔘 3. Gợi ý lựa chọn nhanh dạng A/B/C / Có-Không"]
    D --> E["✅ Người dân chỉ cần 1 chạm để xác nhận"]
    E --> F["📋 4. Đưa ra lộ trình 3 bước bình dân, thấu tình đạt lý"]
    F -.-> G["⚖️ Điều luật trích dẫn & đơn từ được giấu gọn trong Expander"]
```

1. 🚫 **TUYỆT ĐỐI KHÔNG TRẢ LỜI DỒN DẬP:** Không trút tràng dài điều luật Bộ luật Dân sự hay Tố tụng vào tin nhắn chính khiến người dân bị ngợp hoặc bất an.
2. ❓ **HỎI ĐỂ CHẮC CHẮN (Socratic Legal Intake):** Luôn hỏi 1-2 câu trọng tâm để làm rõ:
   - *Thời điểm xảy ra sự việc?*
   - *Bằng chứng hiện có (Giấy viết tay, sao kê ngân hàng, tin nhắn Zalo, hay chỉ nói miệng)?*
   - *Mục tiêu ưu tiên (Hòa giải lấy lại tiền, báo Công an, hay khởi kiện ra Tòa)?*
3. 🔘 **LỰA CHỌN TRẢ LỜI NHANH (Quick-Reply Pills):** Tự động sinh ra các nút bấm gợi ý để người già hoặc người dùng điện thoại chỉ cần bấm chọn thay vì phải gõ bàn phím dài dòng.
4. 👵 **TRỢ NĂNG NGƯỜI CAO TUỔI (Senior Accessible Mode):** Nút bật/tắt tức thì trên thanh Sidebar phóng to font chữ lên **19px**, tăng line-height **1.85**, chống mỏi mắt.
5. 🚨 **BẢO MẬT ZERO-TRUST & NÚT XÓA DẤU VẾT (Panic Wipe):** 1-click giải phóng sạch RAM, bảo vệ an toàn tính mạng cho nạn nhân bạo lực gia đình hoặc người bị theo dõi.
6. 📱 **ĐA KÊNH THƯỜNG TRỰC (<1 GIÂY):** Hoạt động đồng bộ trên Web Streamlit và Bot Telegram Daemon 24/7 (`@SnowflakeVibingBot`).

---

## 📜 NGUYÊN TẮC HOẠT ĐỘNG DỰ ÁN (PROJECT RULES)
> 🚨 **QUY ĐỊNH BẮT BUỘC:** Mọi tác vụ phát triển của AI hoặc người đóng góp phải tuân thủ nghiêm ngặt tài liệu:  
> 👉 **[`RULES.md`](./RULES.md)** *(Quy chuẩn đọc đầu tiên, quy tắc đặt tên version preview/requirements và an toàn bảo mật).*

---

## 🚀 QUẢN LÝ PHIÊN BẢN & LỘ TRÌNH (VERSIONING & ROADMAP)

* **Yêu cầu Kỹ thuật Phiên bản 1.0 (Requirements Version 1.0):**
  * Đặc tả 7 tiêu chí chấm điểm ban đầu của giảng viên: [`requirements/requirements_version_1.md`](./requirements/requirements_version_1.md).
* **Đánh giá Phiên bản 1.0 (Preview Version 1):**
  * Tổng hợp nhận xét người dùng & phản biện kỹ thuật sơ khởi: [`requirements/preview_version_1.md`](./requirements/preview_version_1.md).
* **Yêu cầu Kỹ thuật Phiên bản 1.1 (Requirements Version 1.1) - [ĐÃ HOÀN THÀNH]:**
  * 4 nâng cấp thực chiến: Link kiểm chứng Cổng TT Chính phủ, Bộ tạo hồ sơ doanh nghiệp (.docx), Tra cứu Hybrid (CSDL + Web Search), Trực quan hóa PII: [`requirements/requirements_version_1.1.md`](./requirements/requirements_version_1.1.md).
* **Đánh giá Phiên bản 1.1 (Preview Version 1.1):**
  * Đánh giá v1.1, phân tích yêu cầu Tool Thẩm định Lỗ hổng Hợp đồng, In-Chat Generative UI, mở rộng phạm vi toàn bộ văn bản cho cá nhân/doanh nghiệp: [`requirements/preview_version_1.1.md`](./requirements/preview_version_1.1.md).
* **Yêu cầu Kỹ thuật Phiên bản 2.0 (Requirements Version 2.0 - Major Release) - [ĐÃ HOÀN THÀNH 100%]:**
  * Đại tu toàn diện kiến trúc: Quét cạm bẫy hợp đồng, chấm điểm rủi ro pháp lý (0-100), In-Chat Interactive Canvas, Hierarchical RAG Đa luật: [`requirements/requirements_version_2.0.md`](./requirements/requirements_version_2.0.md).
* **Đánh giá Phiên bản 2.0 (Preview Version 2.0):**
  * Đánh giá v2.0, phân tích yêu cầu "Luật sư Online phân tích 2 chiều đối kháng", giải quyết 4 case xã hội, soạn thảo văn bản on-demand và tái cấu trúc thành 2 Tab NotebookLM: [`requirements/preview_version_2.0.md`](./requirements/preview_version_2.0.md).
* **Yêu cầu Kỹ thuật Phiên bản 2.1 (Requirements Version 2.1) - [ĐÃ HOÀN THÀNH 100%]:**
  * The Legal AI Lawyer & Studio Platform: Phân tích hợp đồng 2 chiều đối kháng, 4 case đời sống xã hội, Smart Pre-filled Form with Placeholder Fallback và giao diện 2 Tab NotebookLM: [`requirements/requirements_version_2.1.md`](./requirements/requirements_version_2.1.md).
  * Hướng dẫn chạy và kịch bản test chi tiết: [`tutorial/run_guide_version_2.1.md`](./tutorial/run_guide_version_2.1.md).
* **Đánh giá Phiên bản 2.1 (Preview Version 2.1):**
  * Đánh giá v2.1, phân tích yêu cầu tích hợp chính thức thư viện mã nguồn mở LangGraph (`langchain-ai/langgraph`), trực quan hóa sơ đồ mạng lưới tác nhân và cơ chế tự hành định kỳ (Hourly Watchdog): [`requirements/preview_version_2.1.md`](./requirements/preview_version_2.1.md).
* **Yêu cầu Kỹ thuật Phiên bản 2.2 (Requirements Version 2.2) - [ĐÃ HOÀN THÀNH 100%]:**
  * Tích hợp chính thức LangGraph Stateful Architecture (`StateGraph`, `START`, `END`, Conditional Routing Edges), hiển thị sơ đồ Mermaid thời gian thực và Bộ kiểm thử tự hành định kỳ mỗi 1 giờ: [`requirements/requirements_version_2.2.md`](./requirements/requirements_version_2.2.md).
  * Hướng dẫn chạy và kịch bản test chi tiết: [`tutorial/run_guide_version_2.2.md`](./tutorial/run_guide_version_2.2.md).
* **Đánh giá Phiên bản 2.2 (Preview Version 2.2):**
  * Đánh giá v2.2, giải quyết bài toán chạy ngầm 24/7 khi máy tính tắt nguồn qua GitHub Actions và kênh báo cáo tức thời qua Telegram Bot: [`requirements/preview_version_2.2.md`](./requirements/preview_version_2.2.md).
* **Yêu cầu Kỹ thuật Phiên bản 2.3 (Requirements Version 2.3) - [ĐÃ HOÀN THÀNH 100%]:**
  * The Cloud Autonomous Watchdog & 24/7 Telegram Alert Platform: GitHub Actions Cron mỗi 1 giờ, Telegram Bot Notifier tự động gửi báo cáo sức khỏe hệ thống về điện thoại: [`requirements/requirements_version_2.3.md`](./requirements/requirements_version_2.3.md).
  * Hướng dẫn thiết lập Telegram Bot & GitHub Secrets: [`tutorial/run_guide_version_2.3.md`](./tutorial/run_guide_version_2.3.md).
* **Đánh giá Phiên bản 2.3 (Preview Version 2.3):**
  * Đánh giá v2.3, bước chuyển mình sang chế độ phát triển tự hành liên tục (Continuous Autonomous Development Loop) và báo cáo thay đổi qua Telegram: [`requirements/preview_version_2.3.md`](./requirements/preview_version_2.3.md).
* **Yêu cầu Kỹ thuật Phiên bản 2.4 (Requirements Version 2.4) - [ĐÃ HOÀN THÀNH 100%]:**
  * The Interactive Legal Roadmap & Smart Evidence Vault: Bản đồ tiến trình tố tụng trực quan (Visual Stepper), Két bằng chứng & Thước đo giá trị chứng cứ (Evidentiary Weight Meter 0-100%): [`requirements/requirements_version_2.4.md`](./requirements/requirements_version_2.4.md).
  * Hướng dẫn kiểm thử chi tiết: [`tutorial/run_guide_version_2.4.md`](./tutorial/run_guide_version_2.4.md).
* **Đánh giá Phiên bản 2.4 (Preview Version 2.4):**
  * Đánh giá v2.4, phân tích rào cản thuật ngữ tố tụng và giải pháp bộ chuyển đổi văn phong song ngữ (Plain-Language Dual-Persona Switcher): [`requirements/preview_version_2.4.md`](./requirements/preview_version_2.4.md).
* **Yêu cầu Kỹ thuật Phiên bản 2.5 (Requirements Version 2.5) - [ĐÃ HOÀN THÀNH 100%]:**
  * The Plain-Language Dual-Persona Platform: Chuyển đổi văn phong tư pháp sang ngôn ngữ bình dân gần gũi như bạn bè, thấu tình đạt lý với 1-click in-chat: [`requirements/requirements_version_2.5.md`](./requirements/requirements_version_2.5.md).
  * Hướng dẫn kiểm thử chi tiết: [`tutorial/run_guide_version_2.5.md`](./tutorial/run_guide_version_2.5.md).
* **Đánh giá Phiên bản 2.5 (Preview Version 2.5):**
  * Đánh giá v2.5, giải pháp điều khiển từ xa qua Telegram (/start, /end, /status) kết hợp sức mạnh tự hành Google Antigravity: [`requirements/preview_version_2.5.md`](./requirements/preview_version_2.5.md).
* **Yêu cầu Kỹ thuật Phiên bản 2.6 (Requirements Version 2.6) - [ĐÃ HOÀN THÀNH 100%]:**
  * The Telegram Remote Control & Antigravity Platform: Điều khiển chu kỳ tự hành 100% từ xa trên điện thoại qua lệnh `/start` và `/end`, phối hợp Antigravity Scheduler & Watchdog: [`requirements/requirements_version_2.6.md`](./requirements/requirements_version_2.6.md).
  * Hướng dẫn kiểm thử chi tiết: [`tutorial/run_guide_version_2.6.md`](./tutorial/run_guide_version_2.6.md).
* **Đánh giá Phiên bản 2.6 (Preview Version 2.6):**
  * Đánh giá v2.6, phân tích nguyên nhân Telegram chậm phản hồi và yêu cầu hệ thống Đa Tác Nhân chuyên trách + Phản biện 2 vai (QA Tester & First-Time Customer): [`requirements/preview_version_2.6.md`](./requirements/preview_version_2.6.md).
* **Yêu cầu Kỹ thuật Phiên bản 2.7 (Requirements Version 2.7) - [ĐÃ HOÀN THÀNH 100%]:**
  * The Specialized Multi-Agent Swarm Platform: Phân rã 4 Tác nhân chuyên trách, Adversarial Dual-Persona Tester Agent (Senior QA & Khách hàng mới tinh), và Real-time Telegram Daemon Agent phản hồi tức thì < 1s: [`requirements/requirements_version_2.7.md`](./requirements/requirements_version_2.7.md).
  * Hướng dẫn kiểm thử chi tiết: [`tutorial/run_guide_version_2.7.md`](./tutorial/run_guide_version_2.7.md).
* **Đánh giá Phiên bản 2.7 (Preview Version 2.7):**
  * Phản biện gắt gao của User về thái độ "dễ dãi" của tech-demo, đặt con người yếu thế làm trọng tâm: Người cao tuổi, người không hiểu luật nói hoang mang lộn xộn, tốc độ tải trang và bảo mật dữ liệu tuyệt đối: [`requirements/preview_version_2.7.md`](./requirements/preview_version_2.7.md).
* **Yêu cầu Kỹ thuật Phiên bản 2.8 (Requirements Version 2.8) - [ĐÃ HOÀN THÀNH 100%]:**
  * Human-Centric LegalTech & Zero-Trust Ephemeral Privacy: Chế độ trợ năng Người cao tuổi (Chữ lớn 19px, độ tương phản cao), Bộ lọc tâm sự hoang mang/uất ức (Emotional Rant De-Noiser), Nút Xóa Sạch Dấu Vết Khẩn Cấp (Panic Wipe): [`requirements/requirements_version_2.8.md`](./requirements/requirements_version_2.8.md).
  * Hướng dẫn kiểm thử chi tiết: [`tutorial/run_guide_version_2.8.md`](./tutorial/run_guide_version_2.8.md).
* **Đánh giá Phiên bản 2.8 (Preview Version 2.8):**
  * Đánh giá v2.8 và phân tích yêu cầu bộ máy kiểm định độc lập đa chiều toàn diện 360° (UI, UX, Backend, Testing): [`requirements/preview_version_2.8.md`](./requirements/preview_version_2.8.md).
* **Yêu cầu Kỹ thuật Phiên bản 2.9 (Requirements Version 2.9) - [ĐÃ HOÀN THÀNH 100%]:**
  * The Holistic 360° Multi-Dimensional Audit & Benchmark Suite: Ma trận kiểm định 4 trụ cột x 5 tiêu chí vi mô (= 20 chỉ số), tích hợp công cụ thứ 10 trong Studio và lệnh `/audit` trực tiếp trên Telegram: [`requirements/requirements_version_2.9.md`](./requirements/requirements_version_2.9.md).
  * Hướng dẫn kiểm thử chi tiết: [`tutorial/run_guide_version_2.9.md`](./tutorial/run_guide_version_2.9.md).
* **Đánh giá Phiên bản 2.9 (Preview Version 2.9):**
  * Phân tích chỉ đạo chiến lược của User: Chuyển toàn bộ trọng tâm sang Cá nhân & Người dân; loại bỏ thói quen trả lời dồn dập, chuyển sang đối thoại thăm khám từng bước để nắm chắc sự việc: [`requirements/preview_version_2.9.md`](./requirements/preview_version_2.9.md).
* **Yêu cầu Kỹ thuật Phiên bản 3.0 (Requirements Version 3.0 - Major Release) - [ĐÃ HOÀN THÀNH 100%]:**
  * The Citizen-Centric Conversational Intake & Multi-Turn Socratic Diagnostic Platform: Tác nhân thăm khám dân sinh (`CitizenIntakeAgent`), đối thoại 1-2 câu hỏi xác minh, gợi ý lựa chọn nhanh (Quick-reply pills), ẩn điều luật chuyên sâu trong Expander: [`requirements/requirements_version_3.0.md`](./requirements/requirements_version_3.0.md).
  * Hướng dẫn kiểm thử chi tiết: [`tutorial/run_guide_version_3.0.md`](./tutorial/run_guide_version_3.0.md).
* **Đánh giá Phiên bản 3.0 (Preview Version 3.0):**
  * Phân tích chỉ đạo của User: Chuyển toàn bộ quy trình tự hành sang chạy liên tục liền mạch từng phiên (Back-to-Back Sessions), nâng cấp nút bấm 1-chạm và cổng thu âm giọng nói: [`requirements/preview_version_3.0.md`](./requirements/preview_version_3.0.md).
* **Yêu cầu Kỹ thuật Phiên bản 3.1 (Requirements Version 3.1) - [ĐÃ HOÀN THÀNH 100%]:**
  * The Continuous Autonomous Pipeline & Voice-Enabled Accessibility Platform: Pipeline tự hành chạy liền mạch (`scripts/continuous_dev_pipeline.py`), nút bấm trả lời 1-chạm trong chat, và cổng thu âm giọng nói cho người cao tuổi: [`requirements/requirements_version_3.1.md`](./requirements/requirements_version_3.1.md).
  * Hướng dẫn kiểm thử chi tiết: [`tutorial/run_guide_version_3.1.md`](./tutorial/run_guide_version_3.1.md).
* **Đánh giá Phiên bản 3.1 (Preview Version 3.1):**
  * Phản biện quyết liệt của User: Yêu cầu bước nhảy vọt thực chiến, nạp file tài liệu & ảnh chứng cứ, tích hợp bộ công cụ tính án phí, thời hiệu và gợi ý 2 chiều thông minh: [`requirements/preview_version_3.1.md`](./requirements/preview_version_3.1.md).
* **Yêu cầu Kỹ thuật Phiên bản 4.0 (Requirements Version 4.0 - Major Release) - [ĐÃ HOÀN THÀNH 100%]:**
  * The In-Chat Multi-Tool Autonomous Legal Workstation & Multimodal Evidence Diagnostic Engine: Bóc tách & giám định file PDF/Word/Ảnh giấy nợ viết tay, Sổ đỏ (`MultimodalEvidenceParser`), bộ công cụ tính án phí NQ 326, kiểm tra thời hiệu BLDS, tra thẩm quyền Tòa án (`CitizenLegalTools`), và hệ thống gợi ý kép thông minh: [`requirements/requirements_version_4.0.md`](./requirements/requirements_version_4.0.md).
  * Hướng dẫn kiểm thử chi tiết: [`tutorial/run_guide_version_4.0.md`](./tutorial/run_guide_version_4.0.md).

---

## 🌟 ĐỘT PHÁ CÔNG NGHỆ TRONG PHIÊN BẢN 4.0 (IN-CHAT WORKSTATION, MULTIMODAL & TOOLS)

1. 📎 **Nạp & Giám Định Chứng Cứ Đa Phương Tiện In-Chat (`src/tools/multimodal_evidence_parser.py`):**
   - Người dân có thể tải trực tiếp vào khung chat: File PDF, Word, và **Hình ảnh chụp thực tế** (ảnh giấy nợ viết tay, sao kê ngân hàng, ảnh Sổ đỏ, ảnh tin nhắn Zalo).
   - Hệ thống tự động bóc tách chữ, xác định nghĩa vụ tài sản, ngày tháng, chữ ký, con dấu.
   - Chấm điểm **Thước đo Giá trị Chứng cứ (0 - 100 điểm)** theo BLTTDS 2015 và đưa ra lời khuyên lập Vi bằng kịp thời.
   - 1-click đưa toàn bộ nội dung giám định vào cuộc trò chuyện cùng Luật sư AI.

2. 🧮 **Bộ Công Cụ Pháp Lý Dân Sinh 1-Chạm (`src/tools/citizen_legal_tools.py`):**
   - 💰 **Tính Án Phí Tòa Án (Nghị quyết 326/2016/UBTVQH14):** Nhập số tiền tranh chấp $\rightarrow$ Xuất ngay án phí sơ thẩm và tiền tạm ứng án phí phải nộp trước (50%).
   - ⏳ **Kiểm Tra Thời Hiệu Khởi Kiện (Điều 429, 588, 623 BLDS 2015):** Nhập ngày xảy ra sự việc $\rightarrow$ Cảnh báo chính xác số ngày/tháng còn lại trước khi mất quyền khởi kiện.
   - 🏛️ **Tra Cứu Cơ Quan Thẩm Quyền:** Phân định rõ UBND cấp xã (đối với hòa giải đất đai), Cơ quan Công an (đối với tố giác lừa đảo), và Tòa án nhân dân cấp huyện.

3. 💡 **Hệ Thống Gợi Ý Kép Thông Minh (Dual-Action Dynamic Chips):**
   - **Hàng 1:** Gợi ý câu trả lời nhanh (A/B/C hoặc Có/Không) để người dân bấm 1 chạm trả lời luật sư.
   - **Hàng 2:** Gợi ý sẵn các câu hỏi đào sâu then chốt (ví dụ: *Án phí bao nhiêu? Có phong tỏa tài khoản con nợ được không? Lập vi bằng Zalo thế nào?*) để người dân chỉ cần bấm chạm là được giải đáp ngay!

---

## 🌟 ĐỘT PHÁ CÔNG NGHỆ TRONG PHIÊN BẢN 3.1 (CONTINUOUS PIPELINE & 1-TOUCH ACCESSIBILITY)

1. 🔄 **Pipeline Tự Hành Chạy Liền Mạch (Continuous Back-to-Back Pipeline - `scripts/continuous_dev_pipeline.py`):**
   - **Không phân theo giờ nữa:** Khi vừa hoàn thành một phiên (session), hệ thống tự động kiểm tra cờ điều khiển trên Telegram và chuyển tiếp ngay sang session kế tiếp mà không phải chờ đợi mốc 1 giờ.
   - Tự động báo cáo tiến độ chi tiết từng session đã hoàn thành về Telegram Bot.
   - Dễ dàng tạm dừng bằng lệnh `/end` hoặc tiếp tục bằng lệnh `/start` từ xa trên điện thoại.

2. 👆 **Nút Bấm Trả Lời Nhanh 1-Chạm (Clickable Interactive Quick-Reply Pills):**
   - Biến các phương án gợi ý A/B/C thành các nút bấm thực sự trong khung chat. Người già và người không thạo công nghệ chỉ cần bấm 1 chạm là gửi tin nhắn ngay lập tức.

3. 🎙️ **Cổng Thu Âm Giọng Nói Dành Cho Người Già & Mắt Kém (`st.audio_input`):**
   - Người dân có thể thu âm trực tiếp lời nói mộc mạc của mình để gửi đến Luật sư Dân gian mà không cần gõ bàn phím.

---

## 🌟 ĐỘT PHÁ CÔNG NGHỆ TRONG PHIÊN BẢN 3.0 (CITIZEN-CENTRIC SOCRATIC INTAKE)

1. 👨‍👩‍👧 **Tác Nhân Thăm Khám Pháp Lý Dân Sinh (`src/agents/citizen_intake_agent.py`):**
   - **Tuyệt đối không trả lời dồn dập:** Không xả hàng tràng điều luật khô khan vào tin nhắn chính khiến người dân bị ngợp hoặc hoang mang.
   - **Hỏi để nắm chắc sự việc:** Chỉ hỏi tối đa 1 đến 2 câu hỏi trọng tâm nhất nhằm xác minh: Thời gian, chứng cứ (Giấy viết tay / Sao kê Zalo), và mục tiêu mong muốn (Hòa giải, đòi tiền, tố giác, kiện tụng).
   - **Gợi ý lựa chọn nhanh (Quick-Reply Pills):** Tự động sinh ra 3-4 nút bấm A/B/C hoặc Có/Không để người già và người ít dùng công nghệ chỉ cần bấm chọn.

2. 💬 **Đại Tu Giao Diện Tab 1 Chatbot Streamlit:**
   - Banner thông báo định hướng: `🎯 Định Hướng Trọng Tâm: 👨‍👩‍👧 Dành Cho Cá Nhân & Người Dân`.
   - Toàn bộ điều luật phức tạp, thẩm định hợp đồng đối kháng và biểu mẫu được thu gọn trong Expander `⚖️ Xem Thêm Căn Cứ Điều Luật & Hồ Sơ Đính Kèm` để người dân dễ thở.

3. 📱 **Trò Chuyện Thăm Khám Từng Bước trên Telegram Bot Daemon:**
   - Bot lắng nghe câu chuyện của người dân và phản hồi ngắn gọn, hỏi 1 câu xác minh then chốt kèm danh sách lựa chọn nhanh.

---

## 🌟 ĐỘT PHÁ CÔNG NGHỆ TRONG PHIÊN BẢN 2.9 (HOLISTIC 360° AUDIT MATRIX)

1. 📊 **Bộ Máy Kiểm Định Đa Chiều Toàn Diện 360° (`src/agents/holistic_evaluator.py`):**
   - **🎨 1. UI (Giao diện - 9.34/10):** Chữ lớn 19px trợ năng, phân cấp 2 Tab NotebookLM, nút Panic Wipe nổi bật, biểu đồ LangGraph Mermaid & Stepper tiến trình.
   - **💖 2. UX (Trải nghiệm - 9.52/10):** Đơn giản hóa cho người ít rành công nghệ, Emotional De-Noiser trấn an tâm lý, câu hỏi Có/Không, vùng an toàn tâm lý khẩn cấp.
   - **⚙️ 3. Backend (Kiến trúc & Bảo mật - 9.44/10):** LangGraph Stateful routing, RAG đa bộ luật có link Chính phủ kiểm chứng, Zero-Trust RAM-only không lưu vết, dự phòng chịu lỗi.
   - **🧪 4. Testing (Kiểm thử & QA - 9.44/10):** Chống bẻ khóa Jailbreak/Prompt Injection, stress-test dữ liệu hỗn loạn/tiếng lóng, CI/CD AppTest tự động hóa, Telegram Daemon sub-second <1s.
   - 🎯 **Điểm Tổng Hợp Toàn Diện (Weighted Score):** **`9.43 / 10.0`** *(Xếp loại: Xuất sắc Toàn diện)*.

2. 🧰 **Công cụ Studio Thứ 10 trong Streamlit (`Tab 2 - Legal Tools Studio`):**
   - Bảng điều khiển trực quan 5 metric cards, 4 tabs chuyên sâu cho từng trụ cột.
   - Nút 1-click kiểm định lại hệ thống và nút đẩy báo cáo trực tiếp đến Telegram.

3. 📱 **Tích Hợp Lệnh `/audit` Thời Gian Thực trên Telegram Daemon:**
   - Người dùng gõ `/audit`, `/eval`, hoặc hỏi đánh giá trực tiếp trong chat Telegram, bot phản hồi ngay trong tích tắc (<1s) ma trận điểm số chi tiết.

---

## 🏛️ KIẾN TRÚC HỆ THỐNG PHIÊN BẢN 3.0 (SYSTEM ARCHITECTURE)

```mermaid
flowchart TD
    Citizen["👤 Người Dân / Cá Nhân Yếu Thế / Người Cao Tuổi"] --> EntryPoint{"Kênh Tiếp Nhận"}
    
    EntryPoint -->|"Web App"| WebUI["🖥️ Streamlit NotebookLM (Chế độ Trợ Năng 19px)"]
    EntryPoint -->|"Điện thoại"| TelegramBot["📱 Telegram Daemon 24/7 (<1s Response)"]

    WebUI --> PanicWipe["🚨 Zero-Trust Panic Wipe (1-Click RAM Cleanup)"]
    
    subgraph HumanCentricLayer ["💖 Tầng Tiếp Nhận & Thăm Khám Dân Sinh (Citizen Intake)"]
        WebUI --> EmotionalParser["💬 Emotional Rant De-Noiser\n(Xoa dịu uất ức & bóc tách sự việc)"]
        TelegramBot --> EmotionalParser
        EmotionalParser --> SocraticIntake["👨‍👩‍👧 Citizen Socratic Intake Agent\n(Hỏi 1-2 câu để chắc chắn sự việc • Quick-Reply Pills)"]
    end

    subgraph LangGraphCore ["🤖 Lõi Điều Phối Đa Tác Nhân (Official LangGraph)"]
        SocraticIntake --> Guardrails["🛡️ Guardrails (PII Masking & Anti-Jailbreak)"]
        Guardrails --> RouterNode["Stateful Router Node"]
        RouterNode -->|"Tranh chấp đất đai / Đòi nợ / Ly hôn"| SocialCases["🏛️ Social Cases Engine"]
        RouterNode -->|"Kiểm tra hợp đồng cá nhân"| ContractAudit["🛡️ Bilateral Contract Scanner"]
        RouterNode -->|"Cần nộp đơn cơ quan chức năng"| SmartDrafter["📝 Smart Legal Drafter (.docx)"]
    end

    subgraph KnowledgeLayer ["📚 Tầng Tri Thức Pháp Luật & Căn Cứ Thực Địa"]
        SocialCases --> HierarchicalRAG[("Hierarchical RAG (Dân sự, Đất đai, HNGĐ)")]
        ContractAudit --> RuleEngine["Deterministic Rule Engine"]
        SmartDrafter --> TemplateBank[("Biểu mẫu chuẩn hóa & Dòng kẻ giữ chỗ")]
        HierarchicalRAG --> GovPortal["🔗 Cổng TT Điện Tử Chính Phủ (vanban.chinhphu.vn)"]
    end

    subgraph AuditTesting ["🧪 Bộ Máy Đánh Giá Đa Chiều 360°"]
        LangGraphCore --> DualPersona["Adversarial Critic (Senior QA & Khách hàng mới tinh)"]
        DualPersona --> HolisticAudit["360° Holistic Audit Matrix (UI • UX • Backend • Testing: 9.43/10)"]
    end
```

---

## 🎓 MINH CHỨNG 7 TIÊU CHÍ ĐÁNH GIÁ CỦA GIẢNG VIÊN (UIT CRITERIA)

| Tiêu Chí UIT | Trọng Số | Hiện Thực Hóa Xuất Sắc Trong Phiên Bản 3.0 | Module Code Tham Chiếu |
| :--- | :---: | :--- | :--- |
| **1. Ứng dụng LLM** | 1.0đ | Giải quyết trọn vẹn 4 bài toán dân sinh đời sống nhạy cảm: Đòi nợ khi con nợ bỏ trốn, tranh chấp đất đai ranh giới, thuận tình/đơn phương ly hôn và bạo lực học đường; kèm module soạn thảo hợp đồng thương mại cho doanh nghiệp ở Tab 2. | [`src/tools/social_cases_knowledge.py`](./src/tools/social_cases_knowledge.py)<br>[`src/dossier/dynamic_drafter.py`](./src/dossier/dynamic_drafter.py) |
| **2. Kỹ năng Prompting** | 2.0đ | Kỹ thuật Few-Shot, Chain-of-Thought (CoT), Socratic Clarification, trích xuất Structured Output JSON, và bộ chuyển đổi ngôn ngữ bình dân (Plain-Language). | [`src/agents/citizen_intake_agent.py`](./src/agents/citizen_intake_agent.py)<br>[`src/tools/plain_language_engine.py`](./src/tools/plain_language_engine.py) |
| **3. Cloud & Local LLM** | 2.5đ | Bộ chuyển mạch Model Switcher linh hoạt giữa Google Gemini Cloud API (`gemini-3.5-flash-lite`) và Local Ollama (`qwen2.5`), tự động fallback khi mất kết nối. | [`llm_provider/model_factory.py`](./llm_provider/model_factory.py)<br>[`llm_provider/cloud_provider.py`](./llm_provider/cloud_provider.py) |
| **4. Vector DB & RAG** | 1.5đ | Hierarchical RAG đa bộ luật (Dân sự, Lao động, Thương mại, Đất đai, HNGĐ, Doanh nghiệp) với 53 chunks được lập chỉ mục, kết hợp tra cứu CSDL SQLite VSIC 2018. | [`src/rag/hierarchical_rag.py`](./src/rag/hierarchical_rag.py)<br>[`src/database/db_manager.py`](./src/database/db_manager.py) |
| **5. AI Agents & LangGraph** | 1.5đ | Xây dựng đồ thị có trạng thái chuẩn `langchain-ai/langgraph` (`StateGraph`, `START`, `END`, Conditional Routing), phân rã 6 tác nhân độc lập kèm sơ đồ Mermaid trực quan. | [`src/agents/graph.py`](./src/agents/graph.py)<br>[`src/agents/citizen_intake_agent.py`](./src/agents/citizen_intake_agent.py) |
| **6. Đánh giá Mô hình** | 1.0đ | Benchmark Ragas (Faithfulness, Relevance, Context Precision, Recall) kết hợp Bộ Máy Kiểm Định Đa Chiều 360° (UI, UX, Backend, Testing) đạt 9.43/10 điểm. | [`src/evaluation/ragas_evaluator.py`](./src/evaluation/ragas_evaluator.py)<br>[`src/agents/holistic_evaluator.py`](./src/agents/holistic_evaluator.py) |
| **7. Bảo mật LLM** | 0.5đ | Mặt nạ hóa PII Masking, Prompt Injection Guard chống jailbreak, Output Moderation, và cơ chế Zero-Trust Panic Wipe dọn sạch session trong RAM. | [`src/security/pii_masker.py`](./src/security/pii_masker.py)<br>[`src/security/ephemeral_privacy.py`](./src/security/ephemeral_privacy.py) |

---

## 🚀 HƯỚNG DẪN KHỞI CHẠY NHANH

### 1. Khởi động Giao diện Web Streamlit (Version 3.0):
```powershell
# Di chuyển vào thư mục dự án
Set-Location D:\LLM\LLM_Nhut

# Khởi chạy ứng dụng
.\venv\Scripts\streamlit.exe run app\main.py
```
👉 Truy cập trình duyệt tại: `http://localhost:8501`.

### 2. Khởi động Tiến trình Telegram Bot Daemon (24/7):
```powershell
Set-Location D:\LLM\LLM_Nhut
.\venv\Scripts\python.exe scripts\telegram_bot_daemon.py
```
👉 Mở ứng dụng Telegram và nhắn tin trực tiếp với bot: `@SnowflakeVibingBot`.

---

## 📂 CẤU TRÚC THƯ MỤC DỰ ÁN

```
LLM_Nhut/
├── app/
│   └── main.py                  # Giao diện Streamlit 2-Tab NotebookLM (Chatbot Dân Sinh & Tools Studio)
├── data/
│   ├── chromadb/                # CSDL Vector (53 chunks đa luật)
│   ├── database/                # SQLite (schema.sql & sme_legal.db) + legal_memory_bank.json
│   ├── evaluation/              # Dataset benchmark Ragas
│   └── raw_documents/           # 8 bộ luật nguồn chính thống
├── deploy/
│   └── hourly_watchdog.yml      # Cấu hình GitHub Actions tự hành 24/7 trên Cloud
├── llm_provider/                # Quản lý Cloud Gemini & Local Ollama
├── requirements/                # Quản lý lộ trình phiên bản từ v1.0 đến v3.0 theo chuẩn RULES.md
├── scripts/
│   ├── hourly_agent_watchdog.py # Giám sát sức khỏe hệ thống định kỳ
│   └── telegram_bot_daemon.py   # Daemon Telegram tương tác thời gian thực (<1s)
├── src/
│   ├── agents/                  # Multi-Agent LangGraph, CitizenIntakeAgent, HolisticAuditEngine
│   ├── database/                # Quản lý CSDL SQLite
│   ├── dossier/                 # Tạo lập hồ sơ & biểu mẫu pháp lý thông minh (.docx)
│   ├── evaluation/              # Ragas benchmark & Model comparison
│   ├── rag/                     # Hierarchical RAG engine
│   ├── security/                # PII Masker, Prompt Injection, Ephemeral Panic Wipe, Telegram Notifier
│   └── tools/                   # Plain-Language Switcher, Emotional Rant De-Noiser, Contract Scanner
├── tutorial/                    # Hướng dẫn kiểm thử chi tiết từng phiên bản
├── .env.example                 # Mẫu khai báo biến môi trường (an toàn bảo mật)
├── LICENSE                      # Giấy phép mã nguồn mở MIT
├── README.md                    # Tài liệu tổng quan & Tầm nhìn chiến lược dự án
└── RULES.md                     # Quy định hoạt động bắt buộc cho AI
```

---

*© 2026 LegalTech Platform. Phát triển vì sự công bằng và an toàn pháp lý cho mọi người dân Việt Nam.*
