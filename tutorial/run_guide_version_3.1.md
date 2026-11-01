# 🚀 HƯỚNG DẪN KIỂM THỬ VÀ VẬN HÀNH PHIÊN BẢN 3.1 (RUN GUIDE VERSION 3.1)
### The Continuous Autonomous Pipeline & Voice-Enabled Accessibility Platform

> **Phiên bản:** 3.1  
> **Thời điểm cập nhật:** 2026-11-01  
> **Mục tiêu:** Hướng dẫn vận hành Pipeline chạy liền mạch từng phiên và trải nghiệm tính năng bấm 1-chạm / thu âm giọng nói.

---

## 🔄 1. KHỞI CHẠY PIPELINE TỰ HÀNH LIỀN MẠCH (BACK-TO-BACK SESSIONS)

Để hệ thống tự động chạy session kế tiếp ngay khi session trước hoàn tất:
```powershell
Set-Location D:\LLM\LLM_Nhut
.\venv\Scripts\python.exe scripts\continuous_dev_pipeline.py
```
* **Điều khiển từ xa trên Telegram:**
  - Gõ `/end` $\rightarrow$ Tạm dừng chu kỳ tự hành.
  - Gõ `/start` $\rightarrow$ Tiếp tục chạy liên tục.

---

## 🖥️ 2. TRẢI NGHIỆM GIAO DIỆN WEB STREAMLIT

```powershell
Set-Location D:\LLM\LLM_Nhut
.\venv\Scripts\streamlit.exe run app\main.py
```
1. **Thử nghiệm Nút bấm 1-chạm:**
   - Chat một câu hỏi bất kỳ (ví dụ: *"Tôi cho bạn vay tiền nhưng nay bạn không trả"*).
   - Khi AI phản hồi, bấm trực tiếp vào một trong các nút chọn nhanh như `[📝 Có giấy viết tay]` hoặc `[📱 Chỉ có tin nhắn Zalo]`.
   - Hệ thống tự động tiếp nhận câu trả lời và tiếp tục thăm khám bước tiếp theo!
2. **Thử nghiệm Thu âm Giọng nói:**
   - Mở mục `🎙️ Nhập Liệu Bằng Giọng Nói (Dành cho Người già / Mắt kém)`.
   - Bấm nút đỏ để thu âm lời nói và gửi đến Luật sư.

---

## 🧪 3. KIỂM THỬ HỒI QUY TỰ ĐỘNG BẰNG APPTEST

```powershell
Set-Location D:\LLM\LLM_Nhut
.\venv\Scripts\python.exe -c "from streamlit.testing.v1 import AppTest; at = AppTest.from_file('app/main.py', default_timeout=20).run(); assert not at.exception; print('AppTest PASS 100%!')"
```
