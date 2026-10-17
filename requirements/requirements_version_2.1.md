# 📋 YÊU CẦU KỸ THUẬT PHIÊN BẢN 2.1 (REQUIREMENTS VERSION 2.1)
### ⚖️ ĐỀ TÀI: LEGALTECH PLATFORM • HỆ THỐNG LUẬT SƯ AI TRỰC TUYẾN & STUDIO CÔNG CỤ (THE LEGAL AI LAWYER & STUDIO PLATFORM)

> 📌 **Tài liệu tham chiếu:** Kế thừa từ đánh giá và phản biện kỹ thuật tại [`requirements/preview_version_2.0.md`](./preview_version_2.0.md).

---

## 🎯 1. Mục tiêu Phiên bản 2.1
Nâng tầm LegalTech Platform thành một **Luật sư Trực tuyến Toàn năng (AI Online Lawyer)** kết hợp giao diện tối giản theo phong cách **NotebookLM (Chỉ 2 Tab: Chatbot Đa năng & Tools Studio)**:
1. **Phân tích Hợp đồng 2 Chiều Đối kháng (Bilateral Exploitation Analysis):** Dò xem bên ra luật có thể lợi dụng kẽ hở nào, bên theo luật có thể bị ép hoặc lợi dụng điểm gì để đưa ra góc nhìn đa chiều.
2. **Bộ Giải pháp 4 Case Đời sống Xã hội Phức tạp:** Bạo lực học đường (trách nhiệm nhà trường), Tranh chấp đất đai ranh giới sổ đỏ, Kiện đòi nợ khi con nợ bỏ trốn, Ly hôn tranh chấp quyền nuôi con & chia tài sản.
3. **Soạn thảo Văn bản Pháp lý Đa dạng theo Yêu cầu (On-Demand Document Generator):** Tự động soạn thảo bất kỳ loại văn bản/đơn từ pháp lý nào theo văn phong chuẩn mực và xuất file Word (.docx).
4. **Trải nghiệm 2 Tab (The 2-Tab NotebookLM Experience):**
   - **Tab 1:** 💬 AI Chatbot tích hợp toàn bộ các tool, triệu hồi Interactive Widget ngay trong khung chat qua lệnh text tự nhiên.
   - **Tab 2:** 🧰 Legal Tools Studio trưng bày tất cả các tool hiện có để chạy thử độc lập.

---

## 🛠️ 2. Danh mục Yêu cầu Kỹ thuật Cụ thể

### 🚀 Yêu cầu 1: Phân tích Lợi dụng Hợp đồng 2 Chiều Đối kháng (Bilateral Exploitation Analysis)
* **Mô tả:** Nâng cấp `src/tools/contract_scanner.py`:
  * Đối với mỗi điều khoản trong hợp đồng/biên bản, AI phải phân tích từ 2 góc nhìn đối nghịch:
    * 🔴 **Góc nhìn Bên Soạn thảo (Bên ra luật):** Có thể lợi dụng câu từ mơ hồ này để trì hoãn nghĩa vụ, áp đặt mức phạt hoặc chối bỏ bồi thường như thế nào?
    * 🟡 **Góc nhìn Bên Ký kết (Bên theo luật):** Có thể bị dính bẫy gì, hoặc có thể vận dụng quy định bắt buộc nào của luật để phản bác?
  * **Đầu ra:** Bảng ma trận đối kháng trực quan (Bilateral Exploitation Matrix) và đề xuất điều khoản dung hòa (Neutral Balanced Clause).

---

### 🚀 Yêu cầu 2: Cơ sở Tri thức & Kịch bản 4 Case Pháp lý Xã hội Thực tế
* **Mô tả:** Mở rộng tri thức nguồn và xây dựng kịch bản giải quyết chuyên sâu cho 4 case:
  1. **Case 1: Bạo lực học đường & Trách nhiệm của nhà trường:**
     - Căn cứ: Điều 599 BLDS 2015 (Bồi thường thiệt hại do người dưới 15 tuổi gây ra trong thời gian trường học quản lý), Nghị định 80/2017/NĐ-CP về môi trường giáo dục an toàn.
     - Quy trình: Giám định thương tật, yêu cầu bồi thường chi phí y tế & tổn thất tinh thần, mẫu đơn khiếu nại nhà trường / tố giác công an.
  2. **Case 2: Tranh chấp Sổ đỏ & Xây dựng Lấn chiếm ranh giới:**
     - Căn cứ: Luật Đất đai (Điều 202, 203) & Bộ luật Dân sự 2015 (Quyền đối với bất động sản liền kề - Điều 175).
     - Quy trình: Hòa giải cơ sở tại UBND xã/phường (thủ tục bắt buộc trước khi khởi kiện), đơn yêu cầu đo đạc địa chính, đơn khởi kiện TAND.
  3. **Case 3: Chủ nợ khởi kiện khi con nợ cố tình bỏ trốn:**
     - Căn cứ: Điều 463 BLDS 2015 (Hợp đồng vay tài sản), Điều 39, 40 Bộ luật Tố tụng Dân sự 2015 (Tòa án nơi cư trú cuối cùng), Điều 175 Bộ luật Hình sự (Tội lạm dụng tín nhiệm chiếm đoạt tài sản).
     - Quy trình: Thu thập bằng chứng chuyển khoản/giấy nợ, thông báo tìm kiếm người vắng mặt, chuyển đơn tố giác nếu có dấu hiệu tẩu tán tài sản bỏ trốn.
  4. **Case 4: Ly hôn, Phân chia tài sản & Tranh chấp quyền nuôi con:**
     - Căn cứ: Luật Hôn nhân và Gia đình 2014 (Điều 59 - nguyên tắc chia tài sản chung, Điều 81 - quyền nuôi con dưới 36 tháng tuổi và con từ đủ 7 tuổi phải hỏi ý kiến).
     - Quy trình: Đơn ly hôn thuận tình / đơn phương, thỏa thuận cấp dưỡng và phân chia tài sản chung/riêng.

---

### 🚀 Yêu cầu 3: Engine Soạn thảo Văn bản Pháp lý Đa dạng theo Form Thông minh (Smart Pre-filled Form with Placeholder Fallback)
* **Mô tả:** Xây dựng `src/dossier/dynamic_drafter.py`:
  * **Cơ chế Form Thông minh Điền sẵn (Pre-filled by AI):**
    * Khi người dùng chọn hoặc yêu cầu một loại văn bản (ví dụ: *Đơn khởi kiện đòi nợ*, *Đơn yêu cầu hòa giải tranh chấp đất đai*, *Đơn tố cáo bạo lực học đường*, *Đơn ly hôn thuận tình*, *Hợp đồng dịch vụ*...), AI sẽ **tự động soạn thảo và điền sẵn 100% các nội dung pháp lý cốt lõi, chuẩn mực**:
      - Quốc hiệu, Tiêu ngữ, Tên loại đơn chuẩn tố tụng.
      - Cơ quan có thẩm quyền tiếp nhận (TAND huyện/tỉnh, UBND xã/phường, Công an...).
      - Toàn bộ nội dung sự việc mẫu, các căn cứ pháp luật và các yêu cầu đề nghị giải quyết.
  * **Xử lý Thông tin Cá nhân Linh hoạt (Flexible Placeholders):**
    * Các trường thông tin nhân thân (Họ tên, ngày sinh, số CCCD, địa chỉ, số tiền tranh chấp, vị trí thửa đất...):
      - Nếu người dùng có nhập $\rightarrow$ Tự động ráp dữ liệu thật vào văn bản.
      - **Nếu người dùng chưa biết hoặc bỏ trống** $\rightarrow$ AI tự động chèn các **chuỗi giữ chỗ chuẩn hóa dạng chấm dòng hoặc ngoặc vuông**:  
        *`Ông/Bà: ........................................, CCCD số: ........................................ cấp ngày: ...../...../......... tại: ........................................`*  
        hoặc: *`[HỌ VÀ TÊN NGƯỜI KHỞI KIỆN]`*, *`[SỐ TIỀN YÊU CẦU ĐÒI NỢ]`*.
    * Người dùng không bị áp lực phải có đầy đủ thông tin mới tạo được, có thể tải về file Word (.docx) và điền tay hoặc bổ sung sau bất cứ lúc nào!
  * **Xuất file Word (.docx) chuẩn:** Căn lề chuẩn văn bản tư pháp Việt Nam (Nghị quyết 01/2017/NQ-HĐTP và Nghị định 30/2020/NĐ-CP).

---

### 🚀 Yêu cầu 4: Tái cấu trúc Giao diện Streamlit thành 2 Tab (The NotebookLM Experience)
* **Mô tả:** Tối giản hóa toàn bộ giao diện thành đúng **2 Tab**:
  * **Tab 1: 💬 AI Legal Chatbot & Command Center (In-Chat Everything):**
    - Nhận diện câu lệnh text tự nhiên của người dùng.
    - Kích hoạt và hiển thị interactive widgets (Quét hợp đồng 2 chiều, Soạn văn bản on-demand, Tra cứu ngành nghề, Tải file Word) ngay tại bong bóng chat.
    - Có các nút gợi ý nhanh cho 4 case đời sống thực tế.
  * **Tab 2: 🧰 Legal Tools Studio (Trung tâm Công cụ Độc lập):**
    - Trưng bày dạng thẻ (Cards) tất cả các công cụ của hệ thống: *Contract Scanner, Dynamic Drafter, Hybrid Industry Lookup, PII Masker, Model Switcher, Memory Bank, Ragas Benchmark*.
    - Cho phép chạy thử từng tool độc lập trên giao diện studio.

---

## 📅 3. Lộ trình Triển khai Version 2.1
1. [ ] **Sprint 2.1.1:** Nâng cấp Engine Phân tích Hợp đồng 2 Chiều Đối kháng (Bilateral Exploitation Analysis).
2. [ ] **Sprint 2.1.2:** Bổ sung Tri thức & Workflow xử lý 4 Case Tình huống Đời sống Xã hội.
3. [ ] **Sprint 2.1.3:** Xây dựng Engine Soạn thảo Văn bản Pháp lý Đa dạng theo Yêu cầu (Dynamic Drafter .docx).
4. [ ] **Sprint 2.1.4:** Tái cấu trúc Giao diện Streamlit thành 2 Tab chuẩn phong cách NotebookLM.
