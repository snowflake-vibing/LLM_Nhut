# 📋 ĐẶC TẢ YÊU CẦU KỸ THUẬT PHIÊN BẢN 4.1 (REQUIREMENTS VERSION 4.1)
### The Evolutionary Breakthrough & Instant Judicial Petition Platform

> **Tài liệu tham chiếu:** [`RULES.md`](../RULES.md) | File đánh giá tiền đề: [`preview_version_4.0.md`](./preview_version_4.0.md)  
> **Trạng thái:** [x] ĐÃ HOÀN THÀNH 100% & VERIFIED

---

## 🎯 1. MỤC TIÊU PHIÊN BẢN 4.1

Chuyển đổi toàn diện bản chất của mỗi Session tự hành: Mỗi session là một **Bước Nhảy Vọt Công Nghệ & Giá Trị Thực Chiến (Evolutionary Breakthrough)**:
1. Tích hợp máy sinh Đơn khởi kiện chuẩn Mẫu số 23-DS (Nghị quyết số 01/2017/NQ-HĐTP của Hội đồng Thẩm phán TANDTC) và Đơn tố giác tội phạm dạng file Word (.docx) 1-chạm.
2. Tích hợp trực tiếp công cụ xuất đơn vào Hộp công cụ Dân sinh của Tab 1.
3. Thiết lập Pipeline Tự hành Chuyển hóa Đột phá (`scripts/continuous_dev_pipeline.py`).

---

## 🛠️ 2. CHI TIẾT TÍNH NĂNG VÀ MÃ NGUỒN

### 2.1. Máy Sinh Đơn Tư Pháp Tức Thì (`src/tools/instant_petition_generator.py`)
- [x] Tạo lớp `InstantPetitionGenerator`:
  - `generate_lawsuit_petition_docx(data)`: Sinh Đơn khởi kiện theo chuẩn Mẫu số 23-DS (Quốc hiệu, Tiêu ngữ, TAND có thẩm quyền, Người khởi kiện, Bị kiện, Nội dung tranh chấp, Căn cứ Điều 468 BLDS 2015, Danh mục tài liệu chứng cứ, Lời cam đoan).
  - `generate_denunciation_petition_docx(data)`: Sinh Đơn tố giác tội phạm lừa đảo qua mạng gửi Cơ quan CSĐT Công an và Viện kiểm sát (Điều 144, 145 BLTTHS 2015, Điều 174 BLHS).

### 2.2. Tích hợp Tab Xuất Đơn Khởi Kiện Trong Chatbot Tab 1 (`app/main.py`)
- [x] Bổ sung Tab `"📝 2. Xuất Đơn Khởi Kiện (.docx)"` trong Hộp công cụ dân sinh.
- [x] Điền nhanh thông tin tranh chấp $\rightarrow$ Bấm nút $\rightarrow$ Tải file Word chuẩn văn thư về máy chỉ trong 1 giây.

### 2.3. Pipeline Đột Phá Tự Hành Liền Mạch (`scripts/continuous_dev_pipeline.py`)
- [x] Tự động đo lường và thẩm định các đột phá: Án phí thực tế, thời hiệu thực tế, và kích thước file Word tạo ra trong từng phiên.
- [x] Báo cáo chi tiết sự bứt phá của app về Telegram Bot sau mỗi phiên.

---

## 🧪 3. KẾT QUẢ KIỂM THỬ

- Streamlit AppTest: **`PASS 100% with no exceptions!`**
- Kiểm thử tạo Đơn khởi kiện Mẫu 23-DS: Thành công tạo file `.docx` kích thước chuẩn văn thư, đầy đủ căn cứ pháp lý và danh mục chứng cứ.
