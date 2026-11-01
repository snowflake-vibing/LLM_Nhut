# 🚀 HƯỚNG DẪN KIỂM THỬ VÀ VẬN HÀNH PHIÊN BẢN 2.9 (RUN GUIDE VERSION 2.9)
### The Holistic 360° Multi-Dimensional Audit & Benchmark Platform

> **Phiên bản:** 2.9  
> **Thời điểm cập nhật:** 2026-11-01  
> **Mục tiêu:** Hướng dẫn kích hoạt và kiểm thử Ma trận Đánh giá 360° (UI • UX • Backend • Testing) trên cả Giao diện Streamlit và Bot Telegram.

---

## 🖥️ 1. KIỂM THỬ TRÊN GIAO DIỆN STREAMLIT WEB

1. Khởi động ứng dụng Streamlit:
   ```powershell
   Set-Location D:\LLM\LLM_Nhut
   .\venv\Scripts\streamlit.exe run app\main.py
   ```
2. Truy cập trình duyệt tại `http://localhost:8501`.
3. Chuyển sang Tab 2: **🧰 Legal Tools Studio (NotebookLM Style)**.
4. Tại hộp chọn công cụ, chọn mục thứ 10:
   👉 **`10. 📊 Holistic 360° System Audit Matrix (Kiểm Định Đa Chiều UI • UX • Backend • Testing)`**.
5. Quan sát:
   - 5 thẻ điểm số tổng quan: Overall Score, UI, UX, Backend, Testing.
   - 4 tab chuyên sâu chứa 20 tiêu chí vi mô kèm giải thích và ghi chú thực địa.
   - Bấm nút **"🔄 Chạy Lại Kiểm Định Đa Chiều Thời Gian Thực"** để kích hoạt chu kỳ audit mới.
   - Bấm nút **"📱 Gửi Báo Cáo Kiểm Định Này Đến Telegram Bot"** để đẩy báo cáo trực tiếp về điện thoại.

---

## 📱 2. KIỂM THỬ TRÊN TELEGRAM BOT (@SnowflakeVibingBot)

Tiến trình Daemon chạy nền thường trực (<1s) luôn sẵn sàng phản hồi:
1. Mở đoạn chat với bot Telegram `@SnowflakeVibingBot`.
2. Gõ lệnh:
   ```text
   /audit
   ```
   *(hoặc `/eval`, `/danhgia`, hoặc nhắn câu hỏi tự nhiên như "đánh giá toàn diện app cho tôi xem")*.
3. Bot sẽ ngay lập tức trả về **Bảng Đánh Giá Đa Chiều Toàn Diện 360°** với đầy đủ điểm số của 4 trụ cột và kết luận tổng thể!

---

## 🧪 3. KIỂM THỬ TỰ ĐỘNG BẰNG APPTEST

Chạy script kiểm thử tự động của Streamlit để bảo đảm không có lỗi runtime:
```powershell
Set-Location D:\LLM\LLM_Nhut
.\venv\Scripts\python.exe -c "from streamlit.testing.v1 import AppTest; at = AppTest.from_file('app/main.py', default_timeout=20).run(); assert not at.exception; print('AppTest PASS 100%!')"
```
