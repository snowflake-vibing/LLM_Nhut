# 🚀 HƯỚNG DẪN KIỂM THỬ VÀ VẬN HÀNH PHIÊN BẢN 3.0 (RUN GUIDE VERSION 3.0)
### The Citizen-Centric Conversational Intake & Multi-Turn Socratic Diagnostic Platform

> **Phiên bản:** 3.0 (Major Release)  
> **Thời điểm cập nhật:** 2026-11-01  
> **Mục tiêu:** Hướng dẫn trải nghiệm luồng thăm khám pháp lý từng bước dành cho người dân, không trả lời dồn dập.

---

## 🖥️ 1. TRẢI NGHIỆM TRÊN GIAO DIỆN STREAMLIT WEB

1. Khởi động ứng dụng:
   ```powershell
   Set-Location D:\LLM\LLM_Nhut
   .\venv\Scripts\streamlit.exe run app\main.py
   ```
2. Mở trình duyệt tại `http://localhost:8501`.
3. Tại **Tab 1: 💬 AI Legal Chatbot & Command Center**:
   - Nhận diện Banner: `🎯 Định Hướng Trọng Tâm: 👨‍👩‍👧 Dành Cho Cá Nhân & Người Dân`.
   - Gõ một tình huống dân sinh bất kỳ, ví dụ:
     > *"Tôi cho anh họ vay 80 triệu làm ăn, hẹn 3 tháng mà nay 1 năm rồi đòi mãi không trả còn chửi bới."*
   - Quan sát câu trả lời của AI:
     - Không "xả" cả tràng điều luật Bộ luật Dân sự.
     - Lắng nghe và hỏi đúng 1 câu: *"Hai bên có giấy vay nợ viết tay không hay chỉ chuyển khoản/tin nhắn?"*
     - Xuất hiện các nút chọn nhanh để trả lời ngay mà không cần gõ chữ.
     - Các điều khoản chi tiết được ẩn gọn gàng trong Expander thu gọn phía dưới.

---

## 📱 2. TRẢI NGHIỆM TRÊN TELEGRAM BOT (@SnowflakeVibingBot)

1. Mở app Telegram và tìm bot `@SnowflakeVibingBot`.
2. Gửi một câu chuyện:
   > *"Hàng xóm lấn đất nhà tôi xây nhà, tôi phải làm sao"*
3. Quan sát: Bot phản hồi tức thì (<1s) với phong cách luật sư thăm khám từng bước và đưa ra các phương án chọn nhanh.

---

## 🧪 3. KIỂM THỬ HỒI QUY TỰ ĐỘNG BẰNG APPTEST

```powershell
Set-Location D:\LLM\LLM_Nhut
.\venv\Scripts\python.exe -c "from streamlit.testing.v1 import AppTest; at = AppTest.from_file('app/main.py', default_timeout=20).run(); assert not at.exception; print('AppTest PASS 100%!')"
```
