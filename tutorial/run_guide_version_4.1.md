# 🚀 HƯỚNG DẪN KIỂM THỬ VÀ VẬN HÀNH PHIÊN BẢN 4.1 (RUN GUIDE VERSION 4.1)
### The Evolutionary Breakthrough & Instant Judicial Petition Platform

> **Phiên bản:** 4.1  
> **Thời điểm cập nhật:** 2026-11-01  
> **Mục tiêu:** Hướng dẫn trải nghiệm công cụ xuất Đơn khởi kiện chuẩn Mẫu 23-DS của TANDTC và Pipeline tự hành đột phá.

---

## 🖥️ 1. TRẢI NGHIỆM TRÊN GIAO DIỆN WEB STREAMLIT

1. Khởi chạy ứng dụng:
   ```powershell
   Set-Location D:\LLM\LLM_Nhut
   .\venv\Scripts\streamlit.exe run app\main.py
   ```
2. Mở trình duyệt tại `http://localhost:8501`.
3. Tại **Tab 1: 💬 AI Legal Chatbot & Command Center**:
   - Mở mục `🧮 Hộp Công Cụ Dân Sinh 1-Chạm`.
   - Chọn tab **`📝 2. Xuất Đơn Khởi Kiện (.docx)`**.
   - Kiểm tra các trường thông tin điền sẵn (TAND thụ lý, Người khởi kiện, Số tiền đòi, Người bị kiện).
   - Bấm nút **`🚀 Xuất File Word Đơn Khởi Kiện Chuẩn 1-Chạm`**.
   - Bấm nút tải về file Word `Don_Khoi_Kien_Dan_Su_Mau_23DS.docx`.
   - Mở file trên Microsoft Word: Quan sát văn bản đã được định dạng chuẩn A4, đúng Quốc hiệu, Tiêu ngữ, căn cứ pháp luật và danh mục chứng cứ tố tụng!

---

## 🔄 2. THEO DÕI PIPELINE ĐỘT PHÁ TRÊN TELEGRAM (@SnowflakeVibingBot)

1. Mở app Telegram, kiểm tra các tin nhắn báo cáo từ `@SnowflakeVibingBot`.
2. Quan sát: Mỗi session báo cáo rõ **sự thay đổi bứt phá của app** (không chỉ là thông báo hệ thống hoạt động ổn, mà chỉ rõ các năng lực mới: Giám định chứng cứ, tính án phí, sinh đơn từ tư pháp).
3. Gõ `/end` để tạm dừng hoặc `/start` để tiếp tục.

---

## 🧪 3. KIỂM THỬ HỒI QUY TỰ ĐỘNG BẰNG APPTEST

```powershell
Set-Location D:\LLM\LLM_Nhut
.\venv\Scripts\python.exe -c "from streamlit.testing.v1 import AppTest; at = AppTest.from_file('app/main.py', default_timeout=20).run(); assert not at.exception; print('AppTest PASS 100%!')"
```
