# 🚀 HƯỚNG DẪN KIỂM THỬ VÀ VẬN HÀNH PHIÊN BẢN 5.1 (RUN GUIDE VERSION 5.1)
### The Voice-First Two-Way Assistant & Complete Judicial Litigation Dossier Platform

> **Phiên bản:** 5.1  
> **Thời điểm cập nhật:** 2026-11-01  
> **Mục tiêu:** Hướng dẫn trải nghiệm Trợ lý âm thanh phát thanh viên tiếng Việt (TTS) và Công cụ xuất Trọn gói Bộ Hồ Sơ Tố Tụng Hoàn Chỉnh (.docx) nộp TAND.

---

## 🖥️ 1. TRẢI NGHIỆM TRỢ LÝ PHÁT THANH VIÊN ÂM THANH (VIETNAMESE TTS)

1. Mở ứng dụng Streamlit tại `http://localhost:8501`.
2. Tại **Tab 1: 💬 AI Legal Chatbot**:
   - Gõ một câu hỏi bất kỳ, ví dụ: *"Tôi bị người ta mượn 50 triệu không trả thì làm sao?"* hoặc bấm nút gợi ý *"💸 Khởi kiện Đòi nợ khi Con nợ bỏ trốn"*.
   - Sau khi AI phản hồi, ngay dưới câu trả lời sẽ xuất hiện nút:
     **`🔊 Đọc to lời giải thích bằng giọng nói (Tiếng Việt)`**.
   - Bấm nút này: Hệ thống tự động làm sạch ký tự markdown và sinh giọng đọc tiếng Việt truyền cảm, phát trực tiếp trên thanh điều khiển âm thanh.
   - Người cao tuổi, người mắt kém hoặc người khiếm thị chỉ cần bấm nút và lắng nghe tư vấn tận tình như đang nói chuyện với luật sư ngoài đời!

---

## 📦 2. TRẢI NGHIỆM XUẤT TRỌN GÓI BỘ HỒ SƠ TỐ TỤNG (.DOCX)

1. Tại khung Chatbot Tab 1, bấm mở mục `🧮 Hộp Công Cụ Dân Sinh 1-Chạm`.
2. Chọn tab **`📦 6. Xuất Trọn Bộ Hồ Sơ Tố Tụng (.docx)`**.
3. Điền các trường thông tin:
   - **Tòa án thụ lý:** Tòa án nhân dân Quận 1, TP. Hồ Chí Minh
   - **Người khởi kiện:** Nguyễn Văn A (CCCD, địa chỉ, số điện thoại)
   - **Người bị kiện:** Trần Thị B
   - **Số tiền đòi:** 150.000.000 VNĐ
4. Bấm **`🚀 Đóng Gói Toàn Diện & Xuất File Word Bộ Hồ Sơ (.docx)`**.
5. Bấm nút tải về: `Bo_Ho_So_To_Tung_Tron_Goi_TAND_Nguyen_Van_A.docx`.
6. Mở file Word và kiểm tra cấu trúc 4 phần trọn vẹn:
   - **Phần I:** Đơn khởi kiện chuẩn Mẫu 23-DS của Hội đồng Thẩm phán TANDTC.
   - **Phần II:** Bảng giải trình & Dự trù án phí tạm ứng NQ 326/2016 (Giá ngạch 150 triệu $\rightarrow$ Tạm ứng án phí 3.750.000 VNĐ nộp Chi cục THADS).
   - **Phần III:** Báo cáo Bàn cờ tố tụng 2 chiều, đề xuất Đơn yêu cầu Biện pháp khẩn cấp tạm thời (phong tỏa tài khoản, kê biên).
   - **Phần IV:** Danh mục chứng cứ kèm theo và chữ ký xác nhận của Người khởi kiện.

---

## 🧪 3. KIỂM THỬ HỒI QUY TỰ ĐỘNG BẰNG APPTEST

```powershell
Set-Location D:\LLM\LLM_Nhut
.\venv\Scripts\python.exe -c "from streamlit.testing.v1 import AppTest; at = AppTest.from_file('app/main.py', default_timeout=20).run(); assert not at.exception; print('AppTest PASS 100%!')"
```
