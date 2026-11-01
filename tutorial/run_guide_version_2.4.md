# 🧪 HƯỚNG DẪN KIỂM THỬ PHIÊN BẢN 2.4 (TEST & RUN GUIDE VERSION 2.4)
### ⚖️ DỰ ÁN: LEGALTECH PLATFORM • BẢN ĐỒ TIẾN TRÌNH TỐ TỤNG & KÉT BẰNG CHỨNG THÔNG MINH
> 📌 **Phiên bản:** Version 2.4 | **Môi trường:** Python 3.10+ • Streamlit • LangGraph

---

## 🎯 I. TỔNG QUAN NÂNG CẤP TẠI VERSION 2.4

Phiên bản 2.4 hiện thực hóa các đột phá UX/UI từ nghiên cứu Insight người dùng:
1. **Interactive Legal Roadmap (Bản đồ Tiến trình Tố tụng Trực quan):**
   * Hiển thị lộ trình 4 bước cho 4 bài toán pháp lý đời sống: Đòi nợ con nợ trốn, Tranh chấp đất đai, Bạo lực học đường, Ly hôn & quyền nuôi con.
   * Ghi rõ mốc thời hạn luật định (Deadline) và cơ quan có thẩm quyền xử lý.
2. **Smart Evidence Vault & Evidentiary Weight Meter (Két Bằng chứng & Thước đo Giá trị Chứng cứ):**
   * Cho phép đương sự tick chọn danh mục tài liệu đang có (Văn bản công chứng, Vi bằng thừa phát lại, Sao kê ngân hàng, Giấy viết tay, Tin nhắn Zalo/SMS...).
   * AI tự động chấm điểm độ mạnh chứng cứ (0 - 100%) theo Bộ luật Tố tụng Dân sự 2015 và đưa ra cảnh báo khẩn cấp củng cố chứng cứ.

---

## 🔬 II. KỊCH BẢN KIỂM THỬ THỰC TẾ TRÊN WEB

### KỊCH BẢN 1: Kiểm tra Bản đồ Tiến trình Tố tụng (Tab 2: Studio)
1. Mở web `http://localhost:8501`.
2. Chuyển sang **Tab 2: 🧰 Legal Tools Studio**.
3. Chọn công cụ **`3. 🏛️ Social Cases Legal Center & Smart Evidence Vault`**.
4. Chọn vụ việc: *"1. 💰 Đòi nợ khi con nợ bỏ trốn / cắt liên lạc"*.
5. Bấm vào tab **"🗺️ Bản đồ Tiến trình Tố tụng (Visual Stepper)"**.
6. **Kỳ vọng:**
   - Bước 1: Lập Vi bằng & Cố định Chứng cứ Giao dịch (Thời hạn: 1 - 3 ngày tại Văn phòng Thừa phát lại).
   - Bước 2: Xác minh Nơi cư trú Cuối cùng của Con nợ (Công an cấp xã).
   - Bước 3: Nộp Đơn Khởi kiện & Niêm yết Xét xử Vắng mặt (TAND).
   - Bước 4: Yêu cầu Thi hành án hoặc Chuyển Cơ quan Điều tra (Điều 175 BLHS).

### KỊCH BẢN 2: Kiểm tra Két Bằng Chứng & Thước đo Giá trị Chứng cứ
1. Cũng tại mục số 3, chuyển sang tab **"🗄️ Két Bằng Chứng (Smart Evidence Vault)"**.
2. Thử nghiệm **Trường hợp Rủi ro (Chỉ có tin nhắn):**
   - Chỉ tick vào ô *"Ảnh chụp màn hình tin nhắn Zalo / SMS / Messenger"*.
   - **Kỳ vọng:** Điểm chứng cứ thấp (`~40/100`), cảnh báo đỏ xuất hiện: *"🚨 CẢNH BÁO QUAN TRỌNG: Bạn chỉ có ảnh chụp màn hình. Hãy ra ngay Văn phòng Thừa phát lại để Lập Vi Bằng..."*.
3. Thử nghiệm **Trường hợp Vững chắc (Có sao kê và vi bằng):**
   - Tick thêm *"Sao kê tài khoản có dấu đỏ ngân hàng"* và *"Vi bằng do Văn phòng Thừa phát lại lập"*.
   - **Kỳ vọng:** Điểm số tăng vọt lên mức `>= 85/100` (Rất Vững Chắc), thanh đo chuyển màu xanh an toàn!
