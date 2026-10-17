# 📜 NGUYÊN TẮC HOẠT ĐỘNG VÀ QUY CHUẨN DỰ ÁN (PROJECT RULES)
### ⚠️ TÀI LIỆU BẮT BUỘC ĐỌC CHO AI TRƯỚC KHI THỰC HIỆN BẤT KỲ TÁC VỤ NÀO

---

## 🚨 ĐIỀU 1: NGUYÊN TẮC BẮT BUỘC ĐỌC ĐẦU TIÊN (MANDATORY FIRST STEP)
* Mỗi khi AI bắt đầu làm việc, nhận yêu cầu mới hoặc tiếp tục phát triển dự án này, **AI BẮT BUỘC PHẢI ĐỌC FILE `RULES.md` NÀY ĐẦU TIÊN**.
* Mọi hành động sửa đổi code, tạo file tài liệu hoặc cấu trúc thư mục đều phải tuân thủ nghiêm ngặt các quy định dưới đây.

---

## 🔄 ĐIỀU 2: QUY TẮC QUẢN LÝ PHIÊN BẢN (VERSION & PREVIEW MANAGEMENT)

### 2.1. Quy tắc Đặt tên File Chuẩn xác:
Mọi file đánh giá (*Preview*) và file yêu cầu (*Requirements*) phải được đặt trong thư mục `requirements/` và tuân theo định dạng tên chính xác theo chuẩn SemVer:
* **File Đánh giá / Phản hồi của Version hiện tại:**  
  `requirements/preview_version_<N>.md`  
  *(Ví dụ: `preview_version_1.md` đánh giá cho bản Version 1.0)*
* **File Yêu cầu kỹ thuật cho Version kế tiếp:**  
  `requirements/requirements_version_<X.Y>.md`  
  *(Ví dụ: Khi tạo `preview_version_1.md` thì BẮT BUỘC phải tạo ngay `requirements_version_1.1.md`)*

### 2.2. Tính Đồng bộ Bắt buộc:
1. **Mỗi khi tạo một file Preview (`preview_version_<N>.md`):**  
   $\rightarrow$ BẮT BUỘC phải tạo đồng thời file **Requirements tương ứng cho version mới** (`requirements_version_<X.Y>.md`) dựa trên các điểm đã đánh giá và phản biện.
2. **Cập nhật `README.md` ngay lập tức:**  
   $\rightarrow$ BẮT BUỘC phải cập nhật file `README.md` tại thư mục gốc để:
   * Cập nhật số phiên bản hiện tại (*Current Version*) và lộ trình phiên bản tiếp theo.
   * Dẫn link tới file `preview_version_<N>.md` và `requirements_version_<X.Y>.md`.
   * Ghi nhận ngắn gọn các tính năng mới đã hoàn thành hoặc đang được nâng cấp.

---

## 🛡️ ĐIỀU 3: QUY TẮC AN TOÀN BẢO MẬT (SECURITY RULES)
* **Tuyệt đối KHÔNG hardcode hoặc commit API Key thật lên GitHub** (kể cả trong file `.md`, code Python hay file cấu hình).
* Mọi API Key bí mật chỉ được lưu trong file `.env` cục bộ trên máy và file này luôn phải nằm trong `.gitignore`.
* Trong các file hướng dẫn hoặc code mẫu, chỉ được sử dụng chuỗi giữ chỗ (*placeholder*) như `your_actual_key_here`.

---

## 📋 ĐIỀU 4: BẢO TOÀN 7 TIÊU CHÍ CHẤM ĐIỂM CỦA GIẢNG VIÊN
Mọi tính năng mới được thêm vào hoặc sửa đổi trong các version tiếp theo **KHÔNG ĐƯỢC LÀM MẤT HOẶC SUY GIẢM** 7 tiêu chí cốt lõi trong đề cương của giảng viên:
1. *Ứng dụng LLM trong doanh nghiệp (1.0đ)*
2. *Kỹ năng Prompting (Few-shot, CoT, Structured Output) (2.0đ)*
3. *Lập trình Cloud Server & Local Model (Model Switcher) (2.5đ)*
4. *Vector DB & RAG cơ bản, đọc từ CSDL SQL (1.5đ)*
5. *AI Agents và Đa Tác Nhân (1.5đ)*
6. *Đánh giá mô hình LLM (Benchmark Ragas) (1.0đ)*
7. *Bảo mật LLM (PII Masking, Anti-Jailbreak) (0.5đ)*

---

## 📦 ĐIỀU 5: QUY TẮC ĐỒNG BỘ GIT & GITHUB
* Sau khi hoàn thành bất kỳ tác vụ nào (tạo file, refactor, sửa bug), AI phải kiểm tra trạng thái (`git status`), tạo commit với thông điệp rõ ràng theo chuẩn Conventional Commits (`feat:`, `docs:`, `fix:`, `refactor:`) và đẩy (`git push origin main`) lên GitHub cho người dùng.
