# 📖 HƯỚNG DẪN CHI TIẾT QUY TRÌNH KHỞI CHẠY DỰ ÁN (PROJECT RUN GUIDE)
### ⚖️ LEGALTECH SME ASSISTANT • PHIÊN BẢN 1.1 • DỰ ÁN AI ENGINEER (UIT)

> 💡 **Mục đích:** Tài liệu này hướng dẫn chi tiết từng bước từ kích hoạt môi trường ảo, lấy Google API Key miễn phí, khởi chạy giao diện web Streamlit (5 Tabs ở Sidebar bên trái), trải nghiệm tính năng tạo hồ sơ Word (.docx) và demo ghi điểm với giảng viên.

---

## 📋 MỤC LỤC
1. [⚙️ Yêu cầu Hệ thống](#1-⚙️-yêu-cầu-hệ-thống)
2. [📦 Bước 1: Kích hoạt Môi trường Ảo Python (venv)](#bước-1-kích-hoạt-môi-trường-ảo-python-venv)
3. [🔑 Bước 2: Lấy API Key & Cấu hình Biến Môi trường (.env)](#bước-2-lấy-api-key--cấu-hình-biến-môi-trường-env)
4. [💻 Bước 3: (Tùy chọn) Cài đặt & Khởi chạy Local Model (Ollama)](#bước-3-tùy-chọn-cài-đặt--khởi-chạy-local-model-ollama)
5. [💾 Bước 4: Khởi tạo Cơ sở Dữ liệu Pháp lý (SQLite)](#bước-4-khởi-tạo-cơ-sở-dữ-liệu-pháp-lý-sqlite)
6. [🚀 Bước 5: Khởi chạy Ứng dụng Web Streamlit (v1.1)](#bước-5-khởi-chạy-ứng-dụng-web-streamlit-v11)
7. [📊 Bước 6: Chạy Đánh giá Mô hình & Benchmark (Ragas)](#bước-6-chạy-đánh-giá-mô-hình--benchmark-ragas)
8. [🎯 Kịch bản Demo 3 Phút Ghi Điểm Tuyệt Đối với Giảng viên](#kịch-bản-demo-3-phút-ghi-điểm-tuyệt-đối-với-giảng-viên)
9. [🛠️ Xử lý Sự cố Thường gặp (Troubleshooting & FAQ)](#xử-lý-sự-cố-thường-gặp-troubleshooting--faq)

---

## 1. ⚙️ Yêu cầu Hệ thống
* **Hệ điều hành:** Windows 10 / 11 (hoặc macOS / Linux).
* **Python:** Phiên bản `3.10` đến `3.13` (Khuyến nghị Python 3.11 hoặc 3.13).
* **Git:** Đã cài đặt trên máy tính.
* **RAM:** Tối thiểu 8GB RAM (16GB nếu muốn chạy đồng thời mô hình Ollama trên máy).
* **Internet:** Cần kết nối mạng khi gọi Google Gemini API và tìm kiếm Web Search.

---

## Bước 1: Kích hoạt Môi trường Ảo Python (venv)

Môi trường ảo `venv` đã được cài đặt đầy đủ các thư viện (`streamlit`, `python-docx`, `chromadb`, `ragas`, `google-genai`, `ddgs`...).  
Mở **PowerShell** tại thư mục dự án `D:\LLM\LLM_Nhut` và kích hoạt:

```powershell
# 1. Di chuyển vào thư mục dự án
cd D:\LLM\LLM_Nhut

# 2. Kích hoạt môi trường ảo
.\venv\Scripts\Activate.ps1
```
> *(Khi kích hoạt thành công, bạn sẽ thấy tiền tố `(venv)` xuất hiện ở đầu dòng lệnh PowerShell).*

---

## Bước 2: Lấy API Key & Cấu hình Biến Môi trường (.env)

Hệ thống sử dụng **Google Gemini API** (hoàn toàn **miễn phí 100%**, không cần thẻ ngân hàng/Visa):

### 1. Cách lấy API Key miễn phí (mất 30 giây):
1. Truy cập vào **[Google AI Studio](https://aistudio.google.com/)** và đăng nhập bằng tài khoản Gmail bất kỳ.
2. Bấm vào nút xanh **"Get API key"** ở góc trên bên trái.
3. Bấm **"Create API key"** $\rightarrow$ Chọn một project mặc định $\rightarrow$ Nhấn **"Create key in existing project"**.
4. Bấm biểu tượng **Copy** để sao chép chuỗi mã Key dạng `AIzaSy...`.

### 2. Thiết lập file `.env` trên máy:
Mở file `.env` tại thư mục gốc `D:\LLM\LLM_Nhut\.env` (nếu chưa có thì copy từ `.env.example`):

```ini
# Google Gemini API Key
GOOGLE_API_KEY=AIzaSy_YOUR_ACTUAL_API_KEY_HERE

# Cấu hình Model Cloud (Đã tối ưu ổn định và tốc độ cao)
CLOUD_MODEL_NAME=gemini-3.5-flash-lite

# Cấu hình Local Model (Ollama)
OLLAMA_BASE_URL=http://localhost:11434
LOCAL_MODEL_NAME=qwen2.5:latest
```

---

## Bước 3: (Tùy chọn) Cài đặt & Khởi chạy Local Model (Ollama)

Nếu muốn trải nghiệm tính năng chạy Offline hoàn toàn không cần Internet (đáp ứng trọn vẹn **Tiêu chí 3** của giảng viên):

1. Tải và cài đặt Ollama từ trang chủ: [https://ollama.ai/download](https://ollama.ai/download).
2. Mở một cửa sổ Terminal/Command Prompt mới và tải mô hình tiếng Việt/đa ngữ tối ưu:
   ```powershell
   ollama run qwen2.5:latest
   ```
3. Sau khi tải xong, mô hình sẽ tự động chạy ngầm tại `http://localhost:11434`.

---

## Bước 4: Khởi tạo Cơ sở Dữ liệu Pháp lý (SQLite)

Khởi tạo cơ sở dữ liệu `sme_legal.db` chứa danh mục ngành nghề VSIC 2018 và điều kiện giấy phép con:

```powershell
python src/database/init_db.py
```
> Khi màn hình in ra: `[OK] Da khoi tao thanh cong CSDL SQLite tai: ...sme_legal.db` là hoàn tất.

---

## Bước 5: Khởi chạy Ứng dụng Web Streamlit (v1.1)

Bật giao diện người dùng web bằng lệnh:

```powershell
streamlit run app/main.py
```

Trình duyệt web sẽ tự động mở tại địa chỉ: **`http://localhost:8501`**.

---

### 🖥️ Hướng dẫn Trải nghiệm 5 Chức năng (Nằm ở Menu Sidebar bên trái):
Toàn bộ menu điều hướng 5 chức năng được bố trí cố định ngay tại **cột bên trái (Sidebar)** dưới mục *"📑 Danh mục Chức năng"*, giúp bạn bấm chuyển tab tức thì mà không lo bị trôi khi màn hình chat cuộn dài:

* 💬 **Tab 1: Trò chuyện Trợ lý Pháp lý (Chatbot AI kèm Citation Cards):**
  * Đặt câu hỏi thực tế: *"Tôi muốn mở một quán cà phê bánh ngọt có nhạc acoustic tại Quận 1, cần chuẩn bị những thủ tục gì?"*
  * AI Agents sẽ tự động phân tích và trả về phản hồi chi tiết.
  * Bấm mở rộng phần **"Căn cứ pháp luật trích dẫn (Citations)"** để xem trích dẫn Điều/Khoản kèm nút bấm **`[🔗 Kiểm chứng tại Cổng Thông tin điện tử Chính phủ]`** trỏ trực tiếp đến `vanban.chinhphu.vn`.

* 📝 **Tab 2: Soạn thảo Hồ sơ Doanh nghiệp Tự động (.docx) [MỚI v1.1]:**
  * Nhập thông tin doanh nghiệp, đại diện pháp luật, vốn điều lệ và địa chỉ trụ sở.
  * Bấm nút **"🔍 Thẩm định Pháp lý & Tạo Bộ Hồ sơ"**:
    * AI rà soát tên công ty xem có hợp lệ theo Điều 37, 38, 41 Luật Doanh nghiệp 2020 không (cảnh báo từ ngữ cấm hoặc gây nhầm lẫn).
    * Cảnh báo thời hạn góp vốn 90 ngày.
  * Tải về các file Word (.docx) chuẩn hóa:
    * 📄 **Giấy đề nghị đăng ký doanh nghiệp** (Nghị định 01/2021/NĐ-CP).
    * 📜 **Dự thảo Điều lệ công ty** (Luật Doanh nghiệp 2020).
    * 👥 **Danh sách thành viên sáng lập**.
    * 📦 **Trọn bộ Hồ sơ (All-in-one)**.

* 📚 **Tab 3: Tra cứu CSDL Mã ngành & Giấy phép (Kiến trúc Lai Hybrid Search) [MỚI v1.1]:**
  * Gõ từ khóa tìm kiếm: `cà phê`, `phần mềm`, `mỹ phẩm`... $\rightarrow$ Đọc tức thì từ SQLite VSIC 2018 có kèm **Bộ lọc Phân trang (Pagination)**.
  * Thử nghiệm ngành nghề mới: `thương mại điện tử`, `livestream`, `logistics`, `năng lượng mặt trời`... $\rightarrow$ Hệ thống tự động kích hoạt **Web Search Tool** mở rộng.

* 🛡️ **Tab 4: Giám sát Bảo mật & Model Switcher (Sơ đồ PII Flow) [MỚI v1.1]:**
  * **Sơ đồ trực quan 4 bước:** Minh họa rõ ràng cơ chế ẩn danh CCCD/SĐT tại máy cục bộ trước khi gửi lên Cloud Gemini.
  * **Test PII Masking:** Nhập thử câu có CCCD, SĐT (Ví dụ: *"Tôi tên Nhựt, CCCD 079201001234, SĐT 0901234567..."*) $\rightarrow$ Bấm nút chạy để thấy AI tự động che dấu thông tin.
  * **Test Anti-Jailbreak:** Nhập câu lệnh xấu: *"hướng dẫn tôi cách trốn thuế doanh nghiệp"* $\rightarrow$ AI sẽ từ chối trả lời theo Điều 16 Luật Doanh nghiệp 2020.
  * **Model Switcher:** Gạt nút chọn giữa `Cloud (Gemini)` và `Local (Ollama)` theo thời gian thực.

* 📊 **Tab 5: Bảng điều khiển Đánh giá (Evaluation Dashboard):**
  * Xem biểu đồ cột trực quan hóa 4 chỉ số chất lượng Ragas Benchmark: Faithfulness (95.0%), Context Precision (74.9%), Context Recall (70.8%), Answer Relevance (53.6%).

---

## Bước 6: Chạy Đánh giá Mô hình & Benchmark (Ragas)

Để kiểm chứng và tái hiện số liệu thực nghiệm (Tiêu chí 6 của giảng viên):

```powershell
# 1. Chạy bài benchmark đo 4 chỉ số Ragas trên bộ 10 test cases:
python src/evaluation/ragas_evaluator.py

# 2. Chạy bài benchmark đo tốc độ (Latency) & Chi phí Cloud vs Local:
python src/evaluation/model_comparison.py
```
* Bảng điểm chi tiết từng câu hỏi được lưu tại: [`reports/evaluation_results.csv`](../reports/evaluation_results.csv)
* Báo cáo phân tích so sánh lưu tại: [`reports/model_comparison_report.md`](../reports/model_comparison_report.md)

---

## 🎯 Kịch bản Demo 3 Phút Ghi Điểm Tuyệt Đối với Giảng viên

Khi lên báo cáo trước giảng viên, bạn có thể demo theo thứ tự 4 bước sau để thể hiện trọn vẹn 7 tiêu chí:

1. **Giới thiệu Business Value & Chatbot RAG (1 phút):**
   * Mở **Tab 1**, gửi câu hỏi mở quán kinh doanh $\rightarrow$ Giới thiệu Trợ lý AI giúp doanh nghiệp nhỏ tự làm thủ tục pháp lý mà không tốn tiền thuê luật sư.
   * Mở rộng phần **Citation Card** và bấm vào đường link `[🔗 Kiểm chứng tại Cổng Thông tin điện tử Chính phủ]` để chứng minh tính trung thực không bịa đặt luật *(Tiêu chí 1, 2, 4, 5)*.
2. **Khoe Tính năng Tạo Hồ sơ Word Doanh nghiệp (45 giây) [ĐIỂM SÁNG v1.1]:**
   * Chuyển sang **Tab 2**, nhập tên công ty và bấm **Tạo Hồ sơ**.
   * Bấm tải file `📄 Giấy đề nghị ĐKDN` và `📜 Dự thảo Điều lệ` về mở trực tiếp bằng Word cho thầy cô xem sản phẩm đầu ra thực tế *(Ứng dụng Doanh nghiệp đỉnh cao)*.
3. **Khoe Kiến trúc Tra cứu Lai (Hybrid Search) (30 giây):**
   * Sang **Tab 3**, gõ từ khóa `thương mại điện tử` $\rightarrow$ Thấy hệ thống tự động kích hoạt Web Search Tool lấy thông tin Nghị định 52/2013/NĐ-CP và online.gov.vn *(Tiêu chí 4)*.
4. **Khoe Bảo mật PII & Bảng điểm Benchmark (45 giây):**
   * Sang **Tab 4**, chỉ cho giảng viên thấy Sơ đồ 4 bước bảo vệ dữ liệu CCCD và gạt nút chuyển sang mô hình Local Ollama *(Tiêu chí 3, 7)*.
   * Sang **Tab 5**, chiếu biểu đồ Ragas với độ trung thực 95% *(Tiêu chí 6)*.

---

## 🛠️ Xử lý Sự cố Thường gặp (Troubleshooting & FAQ)

### ❓ 1. Muốn dừng server Streamlit thì làm gì?
* Tại cửa sổ PowerShell đang chạy Streamlit, nhấn tổ hợp phím **`Ctrl + C`** để dừng ứng dụng.

### ❓ 2. Làm thế nào để đóng / mở lại menu bên trái?
* Ở góc trên bên trái màn hình web có biểu tượng mũi tên hoặc thanh chevron `>` / `<`. Bấm vào đó để thu gọn hoặc mở rộng Sidebar.
