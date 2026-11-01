# 🚀 HƯỚNG DẪN KIỂM THỬ VÀ VẬN HÀNH PHIÊN BẢN 4.0 (RUN GUIDE VERSION 4.0)
### The In-Chat Multi-Tool Autonomous Legal Workstation & Multimodal Evidence Diagnostic Engine

> **Phiên bản:** 4.0 (Major Release)  
> **Thời điểm cập nhật:** 2026-11-01  
> **Mục tiêu:** Hướng dẫn nạp tài liệu/ảnh chứng cứ, sử dụng bộ công cụ pháp lý in-chat và trải nghiệm gợi ý kép thông minh.

---

## 🖥️ 1. TRẢI NGHIỆM TRÊN GIAO DIỆN WEB STREAMLIT

1. Khởi chạy ứng dụng:
   ```powershell
   Set-Location D:\LLM\LLM_Nhut
   .\venv\Scripts\streamlit.exe run app\main.py
   ```
2. Mở trình duyệt tại `http://localhost:8501`.
3. Tại **Tab 1: 💬 AI Legal Chatbot & Command Center**:
   - **Thử nghiệm 1: Nạp Tài Liệu & Ảnh Chứng Cứ:**
     - Mở mục `📎 Nạp Tài Liệu & Ảnh Chứng Cứ`.
     - Tải lên một file PDF, Word hoặc Ảnh chụp giấy nợ / sao kê.
     - Quan sát AI lập tức chấm điểm giá trị chứng cứ (0-100) và đưa ra lời khuyên tố tụng.
     - Bấm nút `💬 Đưa Tài Liệu Này Vào Cuộc Trò Chuyện Với Luật Sư`.
   - **Thử nghiệm 2: Sử Dụng Hộp Công Cụ Dân Sinh 1-Chạm:**
     - Mở mục `🧮 Hộp Công Cụ Dân Sinh 1-Chạm`.
     - Chuyển qua tab *💰 Tính Án Phí*, nhập 300 triệu $\rightarrow$ Xem kết quả án phí và tiền tạm ứng phải nộp ngay.
     - Chuyển qua tab *⏳ Kiểm Tra Thời Hiệu*, nhập ngày trả nợ $\rightarrow$ Xem số ngày còn lại trước khi hết quyền kiện.
     - Chuyển qua tab *🏛️ Xác Định Thẩm Quyền*, chọn Đất đai $\rightarrow$ Nhận chỉ dẫn cơ quan UBND xã và Tòa án.
   - **Thử nghiệm 3: Gợi Ý Kép Thông Minh:**
     - Sau mỗi câu trả lời của AI, quan sát thấy 2 hàng nút bấm:
       1. *👉 Gợi ý lựa chọn nhanh (để trả lời câu hỏi của luật sư).*
       2. *💡 Câu hỏi đào sâu bạn có thể hỏi Luật sư ngay (bấm 1 chạm để hỏi).*

---

## 📱 2. TRẢI NGHIỆM TRÊN TELEGRAM BOT (@SnowflakeVibingBot)

1. Mở app Telegram và nhắn tin với `@SnowflakeVibingBot`.
2. Gửi một câu chuyện nợ nần hoặc đất đai.
3. Quan sát: Bot phản hồi vừa kèm danh sách lựa chọn trả lời nhanh, vừa gợi ý sẵn các câu hỏi đào sâu bạn nên hỏi tiếp!

---

## 🧪 3. KIỂM THỬ HỒI QUY TỰ ĐỘNG BẰNG APPTEST

```powershell
Set-Location D:\LLM\LLM_Nhut
.\venv\Scripts\python.exe -c "from streamlit.testing.v1 import AppTest; at = AppTest.from_file('app/main.py', default_timeout=20).run(); assert not at.exception; print('AppTest PASS 100%!')"
```
