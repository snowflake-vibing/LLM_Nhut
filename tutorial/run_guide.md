# 📖 HƯỚNG DẪN CHI TIẾT QUY TRÌNH KHỞI CHẠY DỰ ÁN (PROJECT RUN GUIDE)

Tài liệu này hướng dẫn chi tiết từ A đến Z cách cài đặt, cấu hình và khởi chạy dự án **LegalTech SME Assistant** trên máy tính cá nhân (hệ điều hành Windows).

---

## 📋 MỤC LỤC
1. [Yêu cầu Hệ thống](#1-yêu-cầu-hệ-thống)
2. [Bước 1: Chuẩn bị Môi trường Python](#bước-1-chuẩn-bị-môi-trường-python)
3. [Bước 2: Cấu hình Biến Môi trường (.env)](#bước-2-cấu-hình-biến-môi-trường-env)
4. [Bước 3: (Tùy chọn) Cài đặt & Khởi chạy Local Model (Ollama)](#bước-3-tùy-chọn-cài-đặt--khởi-chạy-local-model-ollama)
5. [Bước 4: Khởi tạo Cơ sở Dữ liệu Pháp lý](#bước-4-khởi-tạo-cơ-sở-dữ-liệu-pháp-lý)
6. [Bước 5: Khởi chạy Ứng dụng Web Streamlit](#bước-5-khởi-chạy-ứng-dụng-web-streamlit)
7. [Bước 6: Chạy Đánh giá Mô hình & Benchmark (Ragas)](#bước-6-chạy-đánh-giá-mô-hình--benchmark-ragas)
8. [Xử lý Sự cố Thường gặp (Troubleshooting & FAQ)](#xử-lý-sự-cố-thường-gặp-troubleshooting--faq)

---

## 1. Yêu cầu Hệ thống
* **Hệ điều hành:** Windows 10/11 (hoặc macOS/Linux).
* **Python:** Phiên bản `3.10` trở lên (Khuyến nghị 3.10 - 3.13).
* **Git:** Đã cài đặt để quản lý mã nguồn.
* **RAM:** Tối thiểu 8GB (Nếu chạy Local Model 3B/7B mượt mà thì khuyến nghị 16GB RAM).

---

## Bước 1: Chuẩn bị Môi trường Python

Mở **PowerShell** hoặc **Command Prompt** tại thư mục dự án `D:\LLM\LLM_Nhut`:

```powershell
# 1. Di chuyển vào thư mục dự án
cd D:\LLM\LLM_Nhut

# 2. Tạo môi trường ảo Python (Virtual Environment)
python -m venv venv

# 3. Kích hoạt môi trường ảo
# Trên Windows PowerShell:
.\venv\Scripts\Activate.ps1
# (Nếu dùng CMD: .\venv\Scripts\activate.bat)

# 4. Cập nhật pip và cài đặt toàn bộ thư viện dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Bước 2: Cấu hình Biến Môi trường (.env)

Hệ thống hỗ trợ gọi mô hình **Google Gemini API** hoàn toàn miễn phí mà không cần thẻ tín dụng:

1. **Lấy API Key miễn phí:**
   - Truy cập trang: [https://aistudio.google.com](https://aistudio.google.com)
   - Đăng nhập bằng tài khoản Google cá nhân hoặc email trường.
   - Nhấn vào nút **"Get API key"** $\rightarrow$ chọn **"Create API key"** $\rightarrow$ Sao chép khóa bí mật.

2. **Tạo file cấu hình `.env`:**
   - Tạo file `.env` tại thư mục gốc của dự án (copy từ `.env.example`):
   ```powershell
   copy .env.example .env
   ```
   - Mở file `.env` và dán API Key vào:
   ```env
   # Cloud Provider (Miễn phí từ Google AI Studio)
   GOOGLE_API_KEY=AIzaSy...your_actual_key_here
   CLOUD_MODEL_NAME=gemini-1.5-flash

   # Local Provider (Ollama cục bộ)
   OLLAMA_BASE_URL=http://localhost:11434
   LOCAL_MODEL_NAME=qwen2.5:latest

   # Chế độ mặc định ("cloud" hoặc "local")
   DEFAULT_MODE=cloud
   ```

---

## Bước 3: (Tùy chọn) Cài đặt & Khởi chạy Local Model (Ollama)
*Tiêu chí 3 của môn học yêu cầu hỗ trợ cả Local Model chạy nội bộ.*

1. **Tải phần mềm Ollama:**
   - Truy cập [https://ollama.ai](https://ollama.ai) và tải bản cài đặt cho Windows (`OllamaSetup.exe`).
   - Cài đặt như một phần mềm bình thường.
2. **Tải mô hình mã nguồn mở về máy:**
   Mở PowerShell mới và gõ lệnh:
   ```bash
   # Khuyến nghị mô hình Qwen 2.5 (rất giỏi tiếng Việt & tư duy pháp lý):
   ollama run qwen2.5:latest
   
   # Hoặc mô hình Llama 3.1 của Meta:
   ollama run llama3.1:latest
   ```
3. **Kiểm tra trạng thái:**
   - Mở trình duyệt vào địa chỉ: `http://localhost:11434` $\rightarrow$ Nếu thấy dòng *"Ollama is running"* là thành công.

*(Lưu ý: Nếu chưa cài Ollama, hệ thống sẽ tự động sử dụng chế độ Cloud Gemini hoặc Fallback an toàn).*

---

## Bước 4: Khởi tạo Cơ sở Dữ liệu Pháp lý

Chạy script sau để nạp bảng mã ngành kinh tế Việt Nam (VSIC 2018), điều kiện cấp giấy phép con và checklist thủ tục:

```powershell
# Thiết lập UTF-8 cho console PowerShell
$env:PYTHONIOENCODING="utf-8"

# Chạy script khởi tạo CSDL SQLite
python src/database/init_db.py
```
> Kết quả thành công sẽ xuất hiện thông báo:  
> `[OK] Khoi tao va nap du lieu thanh cong cho: D:\LLM\LLM_Nhut\data\database\sme_legal.db`

---

## Bước 5: Khởi chạy Ứng dụng Web Streamlit

Khởi động giao diện người dùng web:

```powershell
streamlit run app/main.py
```

Trình duyệt sẽ tự động mở địa chỉ: **`http://localhost:8501`**.

### 🖥️ Hướng dẫn trải nghiệm 4 Tab trên giao diện:
* **Tab 1: 💬 Trò chuyện Trợ lý Pháp lý (Chatbot):**
  * Nhập câu hỏi khởi nghiệp: *"Tôi muốn mở quán cà phê bánh ngọt có nhạc acoustic tại Quận 1, cần chuẩn bị những thủ tục gì?"*
  * Xem AI Agent tư vấn loại hình, trích xuất căn cứ Điều/Khoản luật trong mục **"Căn cứ pháp luật trích dẫn"**.
* **Tab 2: 📚 Tra cứu CSDL Mã ngành & Giấy phép:**
  * Nhập từ khóa: `cà phê`, `phần mềm`, `mỹ phẩm` để xem trực tiếp bảng dữ liệu VSIC và thông tin lệ phí/thời gian cấp giấy phép con.
* **Tab 3: 🛡️ Giám sát Bảo mật & Model Switcher:**
  * Thử nghiệm nhập đoạn văn bản chứa CCCD, SĐT để xem cơ chế **PII Masking** che dấu dữ liệu.
  * Thử nghiệm nhập lệnh jailbreak/trốn thuế để xem cơ chế **Anti-Jailbreak Defense** từ chối vi phạm.
  * Gạt nút radio chuyển đổi linh hoạt giữa **Cloud Model** và **Local Model**.
* **Tab 4: 📊 Bảng điều khiển Đánh giá (Evaluation Dashboard):**
  * Xem biểu đồ cột trực quan hóa 4 chỉ số đo lường Ragas Benchmark (Faithfulness, Relevance, Precision, Recall).

---

## Bước 6: Chạy Đánh giá Mô hình & Benchmark (Ragas)

Để tái hiện lại kết quả đánh giá thực nghiệm (Tiêu chí 6 của giảng viên):

```powershell
# 1. Chạy đánh giá chất lượng RAG trên bộ 10 benchmark test cases:
python src/evaluation/ragas_evaluator.py

# 2. Chạy bài đo so sánh tốc độ (Latency) & Chi phí giữa Cloud vs Local:
python src/evaluation/model_comparison.py
```
* Kết quả chi tiết dạng bảng sẽ lưu tại: [`reports/evaluation_results.csv`](../reports/evaluation_results.csv)
* Báo cáo phân tích so sánh sẽ lưu tại: [`reports/model_comparison_report.md`](../reports/model_comparison_report.md)

---

## Xử lý Sự cố Thường gặp (Troubleshooting & FAQ)

### ❓ 1. Lỗi PowerShell không cho kích hoạt venv (`execution of scripts is disabled`)
* **Nguyên nhân:** Chính sách bảo mật ExecutionPolicy mặc định của Windows.
* **Cách khắc phục:** Mở PowerShell với quyền Administrator và gõ:
  ```powershell
  Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

### ❓ 2. Lỗi tiếng Việt trên màn hình console (`UnicodeEncodeError: 'charmap' codec...`)
* **Cách khắc phục:** Thiết lập biến môi trường UTF-8 trong PowerShell trước khi chạy lệnh:
  ```powershell
  $env:PYTHONIOENCODING="utf-8"
  ```

### ❓ 3. Lỗi gọi Cloud API (`GOOGLE_API_KEY chưa được cấu hình`)
* **Cách khắc phục:** Đảm bảo bạn đã đổi tên file `.env.example` thành `.env` và điền chính xác mã API Key lấy từ Google AI Studio.

### ❓ 4. Báo cáo & Slide thuyết trình đồ án nằm ở đâu?
* Toàn bộ tài liệu báo cáo học thuật đã được soạn thảo sẵn trong thư mục `reports/`:
  * Báo cáo đồ án 8 chương: [`reports/PROJECT_REPORT.md`](../reports/PROJECT_REPORT.md)
  * Slide thuyết trình 12 trang: [`reports/presentation_slides.md`](../reports/presentation_slides.md)
