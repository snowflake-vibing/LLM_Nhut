# 📊 BÁO CÁO SO SÁNH THỰC NGHIỆM: CLOUD MODEL VS LOCAL MODEL

Báo cáo đo lường thực nghiệm nhằm đáp ứng tiêu chí **3 (Cloud & Local - 2.5đ)** và **6 (Đánh giá mô hình - 1.0đ)** của đồ án AI Engineer.

---

## 📈 Bảng So sánh Tổng quan

| Tiêu chí | ☁️ Cloud Model (Google Gemini API) | 💻 Local Model (Ollama / Llama 3 - Qwen 2.5) |
| :--- | :--- | :--- |
| **Môi trường triển khai** | Cloud Server (Google Data Centers) | Chạy nội bộ trên GPU/CPU máy tính cá nhân |
| **Tốc độ phản hồi (Latency)** | ~ **0.8s** (phụ thuộc đường truyền Internet) | ~ **2.4s** (phụ thuộc phần cứng máy) |
| **Chi phí sử dụng (Cost)** | **0 VNĐ** (sử dụng gói Free Tier 15 RPM) | **0 VNĐ** (Mã nguồn mở miễn phí 100%) |
| **Bảo mật dữ liệu (Privacy)** | Gửi qua API ngoài (Cần lớp PII Masking) | **Tuyệt đối an toàn** (100% On-premise offline) |
| **Khả năng mở rộng (Scale)** | Rất cao, không lo thiếu RAM máy tính | Phụ thuộc vào VRAM và cấu hình máy chủ |
| **Vai trò trong Hệ thống** | Tư vấn chuyên sâu, tổng hợp văn bản pháp luật | Tra cứu dữ liệu nội bộ, bảo vệ danh tính chủ DN |

---

## 💡 Kết luận Kiến trúc
Hệ thống áp dụng **Kiến trúc Lai (Hybrid Architecture)**:
1. Sử dụng **Local Model (Ollama)** làm tuyến phòng thủ đầu tiên để xử lý và ẩn danh các dữ liệu nhạy cảm (CCCD, địa chỉ, vốn góp cá nhân).
2. Tận dụng **Cloud Model (Gemini API)** để xử lý các câu hỏi phức tạp yêu cầu năng lực suy luận ngôn ngữ tiếng Việt sâu rộng và tạo bản checklist chi tiết.
