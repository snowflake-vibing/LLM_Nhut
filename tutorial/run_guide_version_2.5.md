# 🧪 HƯỚNG DẪN KIỂM THỬ PHIÊN BẢN 2.5 (TEST & RUN GUIDE VERSION 2.5)
### ⚖️ DỰ ÁN: LEGALTECH PLATFORM • BỘ CHUYỂN ĐỔI VĂN PHONG BÌNH DÂN (PLAIN-LANGUAGE SWITCHER)
> 📌 **Phiên bản:** Version 2.5 | **Môi trường:** Python 3.10+ • Streamlit • Dual-Persona LLM

---

## 🎯 I. TỔNG QUAN NÂNG CẤP TẠI VERSION 2.5

Phiên bản 2.5 bổ sung tính năng **Bộ Chuyển đổi Văn phong Song ngữ (Plain-Language Dual-Persona Switcher)**:
- Người dùng không còn bị rào cản bởi các thuật ngữ tư pháp nặng nề.
- Dưới mỗi câu trả lời tư vấn pháp lý trong Tab 1, người dùng có thể bấm mở rộng **"☕ Xem Diễn giải sang Ngôn ngữ Bình dân"** để đọc bản tóm lược ấm áp, mộc mạc như một người bạn luật sư đang trò chuyện bên ly cà phê.

---

## 🔬 II. KỊCH BẢN KIỂM THỬ TRỰC TIẾP TRÊN WEB

1. Khởi động Web: `streamlit run app/main.py`.
2. Tại **Tab 1: 💬 AI Legal Chatbot & Command Center**, nhập câu hỏi:
   > *"Tôi cho bạn vay 200 triệu đồng có giấy viết tay và tin nhắn Zalo, đến nay bạn tôi cắt liên lạc và dọn nhà đi nơi khác thì tôi phải làm sao?"*
3. **Kỳ vọng:**
   - Trợ lý ảo phản hồi bản tư vấn chuẩn mực viện dẫn Điều 463 BLDS, Điều 39, 40 BLTTDS (Tòa án nơi cư trú cuối cùng, niêm yết xử vắng mặt).
   - Ngay bên dưới câu trả lời, xuất hiện mục mở rộng: **`☕ Xem Diễn giải sang Ngôn ngữ Bình dân (Dễ hiểu cho người dân)`**.
   - Bấm vào mục mở rộng: Hệ thống hiển thị bản diễn giải bình dân với 3 mục rõ ràng:
     - 💡 *Tóm lại câu chuyện của bạn bằng lời bình dân*
     - 🧭 *3 Bước bạn nên làm ngay hôm nay (Dễ làm, không cần sợ hãi)*
     - ⚠️ *Lời khuyên chân thành để tránh bị đối phương lừa*
