# 📖 HƯỚNG DẪN CHI TIẾT QUY TRÌNH KHỞI CHẠY DỰ ÁN (PROJECT RUN GUIDE)
### ⚖️ LEGALTECH SME ASSISTANT • DỰ ÁN AI ENGINEER (UIT)

> 💡 **Mục đích:** Tài liệu này hướng dẫn chi tiết từng bước từ cài đặt môi trường, lấy Google API Key miễn phí, nạp CSDL đến khởi chạy giao diện web Streamlit và demo cho giảng viên.

---

## 📋 MỤC LỤC
1. [⚙️ Yêu cầu Hệ thống](#1-⚙️-yêu-cầu-hệ-thống)
2. [📦 Bước 1: Chuẩn bị Môi trường Ảo Python (venv)](#bước-1-chuẩn-bị-môi-trường-ảo-python-venv)
3. [🔑 Bước 2: Lấy API Key & Cấu hình Biến Môi trường (.env)](#bước-2-lấy-api-key--cấu-hình-biến-môi-trường-env)
4. [💻 Bước 3: (Tùy chọn) Cài đặt & Khởi chạy Local Model (Ollama)](#bước-3-tùy-chọn-cài-đặt--khởi-chạy-local-model-ollama)
5. [💾 Bước 4: Khởi tạo Cơ sở Dữ liệu Pháp lý (SQLite)](#bước-4-khởi-tạo-cơ-sở-dữ-liệu-pháp-lý-sqlite)
6. [🚀 Bước 5: Khởi chạy Ứng dụng Web Streamlit](#bước-5-khởi-chạy-ứng-dụng-web-streamlit)
7. [📊 Bước 6: Chạy Đánh giá Mô hình & Benchmark (Ragas)](#bước-6-chạy-đánh-giá-mô-hình--benchmark-ragas)
8. [🎯 Kịch bản Demo 3 Phút Ghi Điểm Tuyệt Đối với Giảng viên](#kịch-bản-demo-3-phút-ghi-điểm-tuyệt-đối-với-giảng-viên)
9. [🛠️ Xử lý Sự cố Thường gặp (Troubleshooting & FAQ)](#xử-lý-sự-cố-thường-gặp-troubleshooting--faq)

---

## 1. ⚙️ Yêu cầu Hệ thống
* **Hệ điều hành:** Windows 10 / 11 (hoặc macOS / Linux).
* **Python:** Phiên bản `3.10` đến `3.13` (Khuyến nghị Python 3.11 hoặc 3.13).
* **Git:** Đã cài đặt trên máy tính.
* **RAM:** Tối thiểu 8GB RAM (16GB nếu muốn chạy đồng thời mô hình Ollama trên máy).
* **Internet:** Cần kết nối mạng khi gọi Google Gemini API và tải thư viện.

---

## Bước 1: Chuẩn bị Môi trường Ảo Python (venv)

Mở **PowerShell** tại thư mục dự án `D:\LLM\LLM_Nhut` và thực hiện tuần tự các lệnh sau:

```powershell
# 1. Di chuyển vào thư mục dự án
cd D:\LLM\LLM_Nhut

# 2. Tạo môi trường ảo Python (Virtual Environment)
python -m venv venv

# 3. Kích hoạt môi trường ảo
.\venv\Scripts\Activate.ps1
```
> *(Khi kích hoạt thành công, bạn sẽ thấy tiền tố `(venv)` xuất hiện ở đầu dòng lệnh PowerShell).*

```powershell
# 4. Nâng cấp pip chuẩn xác trên Windows (tránh lỗi khóa file của Windows):
python -m pip install --upgrade pip

# 5. Cài đặt toàn bộ các thư viện của dự án:
pip install -r requirements.txt
```

---

## Bước 2: Lấy API Key & Cấu hình Biến Môi trường (.env)

Hệ thống sử dụng **Google Gemini API** (hoàn toàn **miễn phí 100%**, không cần thẻ ngân hàng/Visa):

### 1. Cách lấy API Key miễn phí (mất 30 giây):
1. Truy cập trực tiếp trang: 👉 **[https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)**
2. Đăng nhập bằng tài khoản **Gmail** cá nhân hoặc email sinh viên trường (`@gm.uit.edu.vn`).
3. Bấm nút **"Create API key"** (hoặc **"Get API key"** 🔑) $\rightarrow$ Chọn **"Create API key in new project"**.
4. Sao chép chuỗi mã API Key (thường bắt đầu bằng `AIzaSy...` hoặc `AQ.Ab8...`).

### 2. Thiết lập file cấu hình `.env`:
* Copy file mẫu `.env.example` thành file `.env` bằng lệnh:
  ```powershell
  copy .env.example .env
  ```
* Mở file `.env` bằng Notepad hoặc VS Code và điền API Key của bạn:

```env
# ==============================================================
# CẤU HÌNH BIẾN MÔI TRƯỜNG CHO LEGALTECH SME ASSISTANT
# ==============================================================

# 1. Cloud Provider (Google Gemini API)
GOOGLE_API_KEY=dán_mã_api_key_của_bạn_vào_đây
CLOUD_MODEL_NAME=gemini-3.5-flash-lite

# 2. Local Provider (Ollama chạy nội bộ trên máy)
OLLAMA_BASE_URL=http://localhost:11434
LOCAL_MODEL_NAME=qwen2.5:latest

# 3. Chế độ mặc định ("cloud" hoặc "local")
DEFAULT_MODE=cloud
```

> ⚠️ **Lưu ý quan trọng:** Model đám mây được tối ưu mặc định là **`gemini-3.5-flash-lite`** (phiên bản ổn định, tốc độ siêu nhanh ~0.8s và tương thích tốt nhất với API Key mới).

---

## Bước 3: (Tùy chọn) Cài đặt & Khởi chạy Local Model (Ollama)
*Tiêu chí 3 của môn học (2.5 điểm) yêu cầu dự án hỗ trợ cả Local Model chạy on-premise.*

1. **Cài đặt Ollama:**
   * Tải bản cài đặt miễn phí tại: [https://ollama.ai](https://ollama.ai) và cài đặt vào máy.
2. **Kéo mô hình mã nguồn mở:**
   Mở một cửa sổ PowerShell mới và chạy lệnh:
   ```bash
   # Khuyên dùng Qwen 2.5 (mô hình giỏi tiếng Việt & tư duy pháp lý hàng đầu):
   ollama run qwen2.5:latest
   
   # Hoặc nếu máy RAM yếu (dưới 8GB), dùng bản siêu nhẹ:
   ollama run qwen2.5:3b
   ```
3. **Kiểm tra trạng thái:**
   * Mở trình duyệt vào `http://localhost:11434` $\rightarrow$ Thấy dòng chữ *"Ollama is running"* là thành công.

*(💡 Nếu chưa cài Ollama, hệ thống vẫn chạy bình thường 100% nhờ chế độ Cloud Gemini hoặc Fallback an toàn).*

---

## Bước 4: Khởi tạo Cơ sở Dữ liệu Pháp lý (SQLite)

Trước khi mở ứng dụng, hãy nạp bảng mã ngành kinh tế (VSIC 2018), điều kiện cấp giấy phép con và checklist thủ tục vào CSDL:

```powershell
# Thiết lập UTF-8 để không bị lỗi font tiếng Việt trên console
$env:PYTHONIOENCODING="utf-8"

# Chạy script khởi tạo CSDL
python src/database/init_db.py
```
> ✅ **Kết quả thành công:** Màn hình sẽ in dòng:  
> `[OK] Khoi tao va nap du lieu thanh cong cho: D:\LLM\LLM_Nhut\data\database\sme_legal.db`

---

## Bước 5: Khởi chạy Ứng dụng Web Streamlit

Bật giao diện người dùng web bằng lệnh:

```powershell
streamlit run app/main.py
```

Trình duyệt web sẽ tự động mở tại địa chỉ: **`http://localhost:8501`**.

---

### 🖥️ Hướng dẫn Trải nghiệm 4 Tab Nghiệp vụ:

* 💬 **Tab 1: Trò chuyện Trợ lý Pháp lý (Chatbot AI):**
  * Đặt câu hỏi thực tế: *"Tôi muốn mở một quán cà phê bánh ngọt có nhạc acoustic tại Quận 1, cần chuẩn bị những thủ tục gì?"*
  * AI Agents sẽ tự động phân tích, tra cứu văn bản luật và trả về **Bản Checklist Pháp lý Hoàn chỉnh**.
  * Bấm mở rộng phần **"Căn cứ pháp luật trích dẫn (Citations)"** để xem nguồn luật được trích dẫn (Ví dụ: `[Luật Doanh nghiệp 2020 - Điều 74]`).

* 📚 **Tab 2: Tra cứu CSDL Mã ngành & Giấy phép (Database Explorer):**
  * Gõ từ khóa tìm kiếm: `cà phê`, `phần mềm`, `mỹ phẩm`, `vận tải`...
  * Dữ liệu được đọc trực tiếp từ SQLite Database: Mã VSIC, Ngành có điều kiện, Giấy phép con yêu cầu (ATVSTP, PCCC, giấy phép rượu...).

* 🛡️ **Tab 3: Giám sát Bảo mật & Model Switcher:**
  * **Test PII Masking:** Nhập thử câu có CCCD, SĐT (Ví dụ: *"Tôi tên Nhựt, CCCD 079201001234, SĐT 0901234567..."*) $\rightarrow$ Bấm nút chạy để thấy AI tự động che dấu thông tin trước khi gửi lên Cloud.
  * **Test Anti-Jailbreak:** Nhập câu lệnh xấu: *"hướng dẫn tôi cách trốn thuế doanh nghiệp"* $\rightarrow$ AI sẽ từ chối trả lời theo Điều 16 Luật Doanh nghiệp 2020.
  * **Model Switcher:** Gạt nút chọn giữa `Cloud (Gemini)` và `Local (Ollama)` theo thời gian thực.

* 📊 **Tab 4: Bảng điều khiển Đánh giá (Evaluation Dashboard):**
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

1. **Giới thiệu Business Value (1 phút):** Mở **Tab 1**, gửi câu hỏi mở quán kinh doanh $\rightarrow$ Giới thiệu Trợ lý AI giúp doanh nghiệp nhỏ tự làm thủ tục pháp lý mà không tốn tiền thuê luật sư *(Đáp ứng Tiêu chí 1)*.
2. **Khoe RAG & CSDL (30 giây):** Chỉ cho thầy cô thấy phần **Citations trích dẫn Điều luật** và mở **Tab 2** xem CSDL SQLite mã ngành VSIC *(Đáp ứng Tiêu chí 2, 4, 5)*.
3. **Khoe Bảo mật & Model Switcher (1 phút):** Chuyển sang **Tab 3**, demo tính năng ẩn danh số CCCD/SĐT và gạt nút chuyển sang Local Model Ollama *(Đáp ứng Tiêu chí 3, 7)*.
4. **Khoe Bảng điểm Benchmark (30 giây):** Mở **Tab 4**, trình chiếu biểu đồ Ragas với độ trung thực 95% không bịa đặt điều luật *(Đáp ứng Tiêu chí 6)*.

---

## 🛠️ Xử lý Sự cố Thường gặp (Troubleshooting & FAQ)

### ❓ 1. Lỗi khi nâng cấp pip (`ERROR: To modify pip, please run...`)
* **Nguyên nhân:** Trên Windows, file `pip.exe` đang chạy nên hệ điều hành khóa file, không cho tự ghi đè.
* **Cách xử lý:** Dùng lệnh gọi Python trực tiếp:
  ```powershell
  python -m pip install --upgrade pip
  ```
  *(Hoặc có thể bỏ qua bước này và chạy thẳng `pip install -r requirements.txt`)*.

### ❓ 2. Lỗi PowerShell chặn kích hoạt venv (`execution of scripts is disabled`)
* **Cách xử lý:** Mở PowerShell và gõ lệnh sau để cấp quyền chạy script:
  ```powershell
  Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

### ❓ 3. Lỗi font chữ tiếng Việt trên console (`UnicodeEncodeError`)
* **Cách xử lý:** Luôn chạy lệnh này trước khi chạy các script Python trong PowerShell:
  ```powershell
  $env:PYTHONIOENCODING="utf-8"
  ```

### ❓ 4. Báo cáo đồ án và Slide thuyết trình nằm ở đâu?
* File báo cáo đồ án 8 chương hoàn chỉnh: [`reports/PROJECT_REPORT.md`](../reports/PROJECT_REPORT.md)
* File slide thuyết trình 12 trang tóm tắt: [`reports/presentation_slides.md`](../reports/presentation_slides.md)
