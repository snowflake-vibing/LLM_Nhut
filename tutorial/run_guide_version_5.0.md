# 🚀 HƯỚNG DẪN KIỂM THỬ VÀ VẬN HÀNH PHIÊN BẢN 5.0 (RUN GUIDE VERSION 5.0)
### The 2-Way Adversarial Courtroom Simulator & Strategic Litigation Forecaster

> **Phiên bản:** 5.0 (Major Release)  
> **Thời điểm cập nhật:** 2026-11-01  
> **Mục tiêu:** Hướng dẫn trải nghiệm Đột phá Công nghệ Bàn cờ Tố tụng 2 Chiều, Dự báo Tỷ lệ Thắng kiện và Bóc tách Kế sách Hóa giải Chiêu phản đòn của Bị đơn dành cho Người dân.

---

## 🖥️ 1. TRẢI NGHIỆM TRÊN GIAO DIỆN WEB STREAMLIT

1. Khởi chạy ứng dụng:
   ```powershell
   Set-Location D:\LLM\LLM_Nhut
   .\venv\Scripts\streamlit.exe run app\main.py
   ```
2. Mở trình duyệt tại `http://localhost:8501`.
3. Tại **Tab 1: 💬 AI Legal Chatbot & Command Center**:
   - Tìm mục `🧮 Hộp Công Cụ Dân Sinh 1-Chạm`.
   - Bấm vào tab **`⚖️ 5. Giả Lập Bàn Cờ Tố Tụng 2 Chiều`**.
   - Kiểm tra các thông số mẫu:
     - **Tóm tắt tình huống tranh chấp**: *"Tôi cho người quen vay 150 triệu từ tháng 3/2023, có giấy viết tay và tin nhắn Zalo hứa trả. Đến hạn người này chặn số, không chịu trả tiền."*
     - **Tài liệu chứng cứ có trong tay**: *"Giấy nợ viết tay ký nhận, sao kê chuyển khoản ngân hàng 150 triệu, tin nhắn xác nhận nợ trên Zalo."*
     - **Bên kia có dấu hiệu tẩu tán tài sản**: Bật tick chọn.
     - **Đã từng gửi thông báo đòi nợ**: Bật tick chọn.
   - Bấm nút **`⚔️ Khởi Động Bàn Cờ Tố Tụng & Dự Báo Tỷ Lệ Thắng Kiện`**.
   - Quan sát kết quả hiển thị đột phá:
     - **Thước đo Dự báo Tỷ lệ Thắng kiện**: 85% (Hiển thị thanh tiến trình xanh mượt, cấp độ rủi ro: Thấp).
     - **Phán quyết Dự kiến của Tòa**: Căn cứ Điều 463 BLDS 2015, chấp nhận toàn bộ yêu cầu khởi kiện.
     - **3 Đòn Tấn Công Sắc Bén của Nguyên đơn**: Nêu rõ 3 căn cứ xác lập quan hệ vay, sao kê ngân hàng và yêu cầu tiền lãi.
     - **3 Chiêu Bài Phản Đòn Bị Đơn Thường Dùng**: Phản bác tính xác thực chữ ký, lấy cớ góp vốn kinh doanh, câu giờ trì hoãn thời hiệu.
     - **3 Kế Sách Hóa Giải Tuyệt Đối**: Yêu cầu giám định chữ ký, xuất trình sao kê Zalo có công chứng/vi bằng, nộp đơn áp dụng Biện pháp khẩn cấp tạm thời (phong tỏa tài khoản).

---

## 🔄 2. KẾT NỐI VỚI HỘP CÔNG CỤ DÂN SINH TOÀN DIỆN

Tại cùng Hộp công cụ Dân sinh, người dân có thể phối hợp liên hoàn:
1. **Kiểm tra Thời hiệu (Tab 3):** Đảm bảo chưa quá 3 năm theo Điều 429 BLDS 2015.
2. **Tính Án Phí (Tab 2):** Dự trù ngay 7.500.000 VNĐ tạm ứng án phí theo NQ 326/2016.
3. **Giả Lập Bàn Cờ (Tab 5):** Thấy trước toàn bộ kịch bản phiên tòa tranh tụng.
4. **Xuất Đơn Khởi Kiện (Tab 4):** Bấm 1 nút sinh ngay file Word Mẫu 23-DS có điền sẵn chứng cứ và thẩm quyền Tòa án để nộp trực tiếp.

---

## 🧪 3. KIỂM THỬ HỒI QUY TỰ ĐỘNG BẰNG APPTEST

```powershell
Set-Location D:\LLM\LLM_Nhut
.\venv\Scripts\python.exe -c "from streamlit.testing.v1 import AppTest; at = AppTest.from_file('app/main.py', default_timeout=20).run(); assert not at.exception; print('AppTest PASS 100%!')"
```
