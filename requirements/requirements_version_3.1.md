# 📋 ĐẶC TẢ YÊU CẦU KỸ THUẬT PHIÊN BẢN 3.1 (REQUIREMENTS VERSION 3.1)
### The Continuous Autonomous Pipeline & Voice-Enabled Accessibility Platform

> **Tài liệu tham chiếu:** [`RULES.md`](../RULES.md) | File đánh giá tiền đề: [`preview_version_3.0.md`](./preview_version_3.0.md)  
> **Trạng thái:** [x] ĐÃ HOÀN THÀNH 100% & VERIFIED

---

## 🎯 1. MỤC TIÊU PHIÊN BẢN 3.1

1. Chuyển đổi toàn bộ quy trình tự hành từ cơ chế định kỳ mỗi 1 giờ sang **Pipeline Tự hành Liền Mạch (Continuous Back-to-Back Sessions)**: Chạy session kế tiếp ngay khi session trước hoàn thành; chỉ dừng khi người dùng gửi lệnh `/end`.
2. Nâng cấp trải nghiệm tương tác dân sinh: **Nút bấm lựa chọn nhanh 1-chạm (Clickable Quick-Reply Pills)** và **Hỗ trợ thu âm giọng nói trực tiếp (Speech-to-Text Audio Input)** cho người cao tuổi.

---

## 🛠️ 2. CHI TIẾT TÍNH NĂNG VÀ MÃ NGUỒN

### 2.1. Pipeline Tự Hành Liền Mạch (`scripts/continuous_dev_pipeline.py`)
- [x] Tạo script `scripts/continuous_dev_pipeline.py` vận hành theo vòng lặp vô tận:
  - Kiểm tra trạng thái điều khiển Telegram (`controller.is_running()`).
  - Thực thi kiểm tra sức khỏe Model (Cloud Gemini & Local Ollama), Vector DB tri thức đa luật, và kiểm thử `CitizenIntakeAgent`.
  - Tự động sinh báo cáo tiến độ chi tiết theo số thứ tự session và gửi về Telegram.
  - Nghỉ ngắn 45 giây để bảo vệ rate limit của Bot API trước khi tự động chuyển sang session tiếp theo.

### 2.2. Nút Bấm Lựa Chọn Nhanh 1-Chạm (`app/main.py`)
- [x] Chuyển đổi các gợi ý dạng text thành `st.button` tương tác trực tiếp (`use_container_width=True`).
- [x] Khi người dùng bấm nút, hệ thống tự động gán vào `st.session_state.pending_quick_input` và kích hoạt `st.rerun()` để xử lý ngay lập tức mà không cần gõ phím.

### 2.3. Cổng Thu Âm Giọng Nói Dành Cho Người Già & Mắt Kém (`app/main.py`)
- [x] Tích hợp `st.audio_input` ngay dưới khung chat.
- [x] Cho phép thu âm lời nói mộc mạc và gửi trực tiếp tới Luật sư Dân gian.

---

## 🧪 3. KẾT QUẢ KIỂM THỬ TỰ ĐỘNG

- Streamlit AppTest: **`PASS 100% with no exceptions!`**
- Continuous Pipeline: Chạy ổn định, tự động báo cáo từng session về Telegram.
