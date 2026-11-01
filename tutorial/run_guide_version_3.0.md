# 🚀 HƯỚNG DẪN KIỂM THỬ VÀ VẬN HÀNH PHIÊN BẢN 3.0 (RUN GUIDE VERSION 3.0)
### The Citizen-Centric Conversational Legal Workstation & Multimodal Judicial Suite

> **Phiên bản:** 3.0 (Major Release)  
> **Thời điểm cập nhật:** 2026-11-01  
> **Tài liệu tham chiếu:** [`requirements_version_3.0.md`](../requirements/requirements_version_3.0.md)

---

## 🖥️ 1. KHỞI CHẠY HỆ THỐNG TRÊN WEB STREAMLIT

1. Mở PowerShell và di chuyển vào thư mục dự án:
   ```powershell
   Set-Location D:\LLM\LLM_Nhut
   .\venv\Scripts\streamlit.exe run app\main.py
   ```
2. Truy cập trình duyệt tại `http://localhost:8501`.

---

## 🧭 2. KỊCH BẢN TRẢI NGHIỆM CÁC NĂNG LỰC ĐỘT PHÁ

### Kịch bản 1: Thăm Khám Socratic & Tương Tác 2 Chiều Bằng Giọng Nói (Voice-to-Voice)
1. Tại khung chat, bấm vào biểu tượng Micro (`Thu âm giọng nói`) để nói câu chuyện của bạn (hoặc bấm chọn nút tình huống *"💸 Khởi kiện Đòi nợ khi Con nợ bỏ trốn"*).
2. Quan sát AI phản hồi:
   - Trấn an cảm xúc ngắn gọn, không trút tràng dài điều luật.
   - Hỏi đúng 1 câu then chốt về chứng cứ.
   - Hiển thị các nút bấm trả lời nhanh (**Quick Options**) và gợi ý câu hỏi tiếp theo (**Suggested Follow-ups**).
3. Bấm nút **`🔊 Đọc to lời giải thích bằng giọng nói (Tiếng Việt)`**: Lắng nghe trợ lý cất giọng đọc truyền cảm, ấm áp dành cho người cao tuổi/người khiếm thị.

### Kịch bản 2: Bàn Cờ Tố Tụng 2 Chiều & Dự Báo Tỷ Lệ Thắng Kiện
1. Mở mục `🧮 Hộp Công Cụ Dân Sinh 1-Chạm`.
2. Chọn tab **`⚖️ 5. Giả Lập Bàn Cờ Tố Tụng 2 Chiều`**.
3. Chọn dạng tranh chấp và loại chứng cứ hiện có, bấm **`🚀 Bắt Đầu Giả Lập Phiên Tòa Đối Kháng`**.
4. Quan sát:
   - Dự báo Tỷ lệ Thắng kiện (0 - 100%) và Phán quyết dự kiến của Tòa.
   - 3 Mũi tấn công của Nguyên đơn vs 3 Chiêu bài phản đòn của Bị đơn (chối nợ, chối chữ ký, nại hùn vốn).
   - Kế sách hóa giải: Đơn yêu cầu Biện pháp khẩn cấp tạm thời (phong tỏa tài khoản) và lập Vi bằng.

### Kịch bản 3: Xuất Trọn Gói Bộ Hồ Sơ Tố Tụng (.docx)
1. Chọn tab **`📦 6. Xuất Trọn Bộ Hồ Sơ Tố Tụng (.docx)`**.
2. Kiểm tra thông tin Tòa án, Người khởi kiện, Bị đơn, Số tiền tranh chấp.
3. Bấm **`🚀 Đóng Gói Toàn Diện & Xuất File Word Bộ Hồ Sơ (.docx)`**.
4. Tải file Word về: Xem trọn gói 4 phần (Đơn Mẫu 23-DS, Bảng án phí NQ 326, Báo cáo bàn cờ tố tụng, Danh mục chứng cứ kèm chữ ký).

---

## 📱 3. ĐIỀU KHIỂN VÀ TƯ VẤN TRÊN TELEGRAM (@SnowflakeVibingBot)

1. Mở Telegram, nhắn tin cho bot `@SnowflakeVibingBot`.
2. Gửi câu hỏi pháp lý: Bot phản hồi tức thì (<1s) theo đúng phong cách Socratic gần gũi.
3. Các lệnh quản trị từ xa:
   - `/status`: Kiểm tra trạng thái hệ thống.
   - `/audit`: Chạy ma trận đánh giá 360 độ (UI, UX, Backend, Testing).
   - `/end`: Tạm dừng hệ thống tự hành.
   - `/start`: Kích hoạt tiếp tục.

---

## 🧪 4. KIỂM THỬ HỒI QUY TỰ ĐỘNG BẰNG APPTEST

```powershell
Set-Location D:\LLM\LLM_Nhut
.\venv\Scripts\python.exe -c "from streamlit.testing.v1 import AppTest; at = AppTest.from_file('app/main.py', default_timeout=20).run(); assert not at.exception; print('AppTest PASS 100%!')"
```
