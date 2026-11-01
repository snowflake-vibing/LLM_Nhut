# 📋 ĐẶC TẢ YÊU CẦU KỸ THUẬT PHIÊN BẢN 5.1 (REQUIREMENTS VERSION 5.1)
### The Voice-First Two-Way Assistant & Complete Judicial Litigation Dossier Platform

> **Tài liệu tham chiếu:** [`RULES.md`](../RULES.md) | File đánh giá tiền đề: [`preview_version_5.0.md`](./preview_version_5.0.md)  
> **Trạng thái:** [x] ĐÃ HOÀN THÀNH 100% & VERIFIED

---

## 🎯 1. MỤC TIÊU PHIÊN BẢN 5.1

Hiện thực hóa cam kết xóa bỏ rào cản công nghệ và dân chủ hóa pháp lý cho **Người cao tuổi, người khiếm thị và người dân bình thường**:
1. **Trợ Lý Âm Thanh Song Phương (Two-Way Voice Assistant):**
   - Đọc to câu trả lời của AI bằng giọng đọc tiếng Việt truyền cảm thông qua công nghệ Text-to-Speech (TTS), biến tương tác chữ thành trải nghiệm nghe nhìn sống động, không cần căng mắt đọc chữ.
2. **Bộ Đóng Gói Hồ Sơ Tố Tụng Trọn Gói (.docx) (`LitigationDossierGenerator`):**
   - Tự động tích hợp:
     - Phần 1: Đơn khởi kiện chuẩn Mẫu 23-DS của Hội đồng Thẩm phán TANDTC.
     - Phần 2: Bảng giải trình & Dự trù Án phí tạm ứng theo Nghị quyết 326/2016/UBTVQH14.
     - Phần 3: Báo cáo Kịch bản Bàn cờ Tố tụng 2 Chiều & Biện pháp khẩn cấp tạm thời hóa giải mưu mẹo đối phương.
     - Phần 4: Danh mục tài liệu chứng cứ nộp kèm Tòa án.
   - Xuất ra 1 file Word `.docx` trọn gói duy nhất có thể in ngay lập tức.
3. **Tích hợp liền mạch vào Web Streamlit và Giao diện Chatbot Tab 1.**

---

## 🛠️ 2. CHI TIẾT TÍNH NĂNG VÀ MÃ NGUỒN

### 2.1. Module Trợ Lý Phát Thanh Âm Thanh (`src/tools/voice_narrator.py`)
- Lớp `VoiceNarrator`:
  - Hàm `generate_speech(text: str, lang: str = 'vi', slow: bool = False) -> bytes`:
    - Làm sạch các ký tự markdown (`*`, `#`, `_`, URL, code blocks) để âm thanh phát âm mạch lạc, chuẩn văn phong đời sống.
    - Sinh dữ liệu nhị phân MP3 sử dụng `gTTS`.
    - Trả về đối tượng `BytesIO` để phát trực tiếp trên `st.audio`.

### 2.2. Động Cơ Đóng Gói Bộ Hồ Sơ Tố Tụng Trọn Gói (`src/tools/litigation_dossier_generator.py`)
- Lớp `LitigationDossierGenerator`:
  - Hàm `build_complete_dossier(...) -> BytesIO`:
    - Tạo tài liệu Word chuẩn A4.
    - Soạn thảo chuẩn quy cách văn bản tư pháp: Quốc hiệu, Tiêu ngữ, Mục lục hồ sơ, 4 Phần cấu thành hoàn chỉnh.
    - Có bảng biểu minh họa, chữ ký của người khởi kiện và hướng dẫn nộp hồ sơ tại bộ phận một cửa TAND.

### 2.3. Tích Hợp UI Streamlit (`app/main.py`)
- Thêm nút nghe giọng đọc **`🔊 Nghe Lời Giải Thích Bằng Giọng Nói`** ngay dưới các phản hồi của AI trong Chat.
- Bổ sung tùy chọn **`📦 6. Xuất Trọn Gói Bộ Hồ Sơ Tố Tụng (.docx)`** trong Hộp Công Cụ Dân Sinh 1-Chạm.

---

## 🧪 3. TIÊU CHÍ NGHIỆM THU (ACCEPTANCE CRITERIA)

1. Sinh file âm thanh MP3 tiếng Việt đọc rõ ràng, không lỗi chính tả hay vướng thẻ Markdown.
2. Sinh file Word `.docx` hoàn chỉnh không lỗi định dạng, mở được trên MS Word, WPS Office.
3. Kiểm thử tự động `streamlit.testing.v1.AppTest` PASS 100%.
4. Cập nhật đầy đủ `tutorial/run_guide_version_5.1.md` và `README.md`.
