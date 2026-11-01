# 🧪 HƯỚNG DẪN KIỂM THỬ PHIÊN BẢN 2.8 (TEST & RUN GUIDE VERSION 2.8)
### ⚖️ DỰ ÁN: LEGALTECH PLATFORM • TRỢ NĂNG NGƯỜI CAO TUỔI, GẠN LỌC CẢM XÚC & BẢO MẬT KHẨN CẤP
> 📌 **Phiên bản:** Version 2.8 | **Môi trường:** Python 3.10+ • Streamlit • Ephemeral Privacy

---

## 🎯 I. TỔNG QUAN NÂNG CẤP TẠI VERSION 2.8

Phiên bản 2.8 giải quyết triệt để các góc khuất thực tế của người dùng:
1. **Chế độ Chữ Lớn (Người Cao Tuổi & Trợ Năng):**
   - Font chữ 19px, giãn dòng rộng rãi, độ tương phản cao, nút bấm to bản giúp người già mắt kém hoặc người không rành công nghệ thao tác dễ dàng.
2. **Bộ Gạn Lọc Cảm Xúc & Dẫn Dắt Socratic (Emotional Rant De-Noiser):**
   - Người dùng đau khổ, uất ức nhắn tin lộn xộn, dài dòng, không đầu không đuôi $\rightarrow$ AI tự động xoa dịu cảm xúc trước, bóc tách 3 điểm sự thật cốt lõi và đưa ra câu hỏi trắc nghiệm `Có` / `Không` để định hướng.
3. **Nút Xóa Dấu Vết Khẩn Cấp (Panic Wipe 1-Click):**
   - Nút đỏ nổi bật tại Sidebar: Bấm 1 click là xóa sạch 100% dữ liệu, tin nhắn, tài liệu tạm trong bộ nhớ RAM, bảo vệ người dùng trước nguy cơ bị xem trộm thiết bị.

---

## 🔬 II. KỊCH BẢN KIỂM THỬ TRỰC TIẾP TRÊN WEB

### Kịch bản 1: Kiểm thử Chế độ Người cao tuổi (Chữ lớn & Giãn dòng)
1. Mở web: `streamlit run app/main.py`.
2. Trên Sidebar bên trái, gạt bật **"👓 Chế độ Chữ Lớn (Người Cao Tuổi)"**.
3. **Kỳ vọng:** Toàn bộ chữ trên trang web phóng to rõ ràng (19px), các khoảng cách thoáng đãng, người lớn tuổi nhìn vào đọc được ngay mà không cần đeo kính.

### Kịch bản 2: Kiểm thử Người dùng "nói không đâu vào đâu / hoảng loạn"
1. Tại khung chat Tab 1, dán một đoạn tâm sự lộn xộn, bức xúc:
   > *"Trời ơi cứu tôi với! Tôi uất ức quá không chịu nổi! Thằng bạn khốn nạn nó vay tiền tôi từ năm ngoái đến giờ nó chặn số tôi rồi, nhà nó cũng chuyển đi đâu mất tiêu, tôi mất ăn mất ngủ mấy tháng nay, cả gia đình tôi đang bế tắc cùng cực, tôi có cầm tờ giấy viết tay của nó mà giờ chẳng biết phải làm sao cả, luật sư cứu tôi với!"*
2. **Kỳ vọng:**
   - AI **không trả lời khô khan bằng một đống điều luật**.
   - AI hiển thị lời trấn an tâm lý ấm áp, xoa dịu nỗi đau.
   - Bóc tách rõ 3 điểm cốt lõi (Ai vi phạm? Thiệt hại bao nhiêu? Thời gian nào?).
   - Dẫn dắt người dùng bằng các câu hỏi ngắn dễ trả lời.

### Kịch bản 3: Kiểm thử Nút Xóa Dấu Vết Khẩn Cấp (Panic Wipe)
1. Sau khi chat hoặc tạo tài liệu, bấm nút đỏ **"🚨 XÓA SẠCH DẤU VẾT (Panic Wipe)"** trên Sidebar.
2. **Kỳ vọng:** Màn hình lập tức tải lại trong 0.1 giây, toàn bộ tin nhắn nhạy cảm biến mất hoàn toàn, trả về trạng thái ẩn danh an toàn tuyệt đối.
