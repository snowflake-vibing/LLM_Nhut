# 🧪 HƯỚNG DẪN KIỂM THỬ PHIÊN BẢN 2.3 (TEST & RUN GUIDE VERSION 2.3)
### ⚖️ DỰ ÁN: LEGALTECH PLATFORM • TỰ HÀNH CLOUD 24/7 QUA GITHUB ACTIONS & BÁO CÁO TELEGRAM
> 📌 **Phiên bản:** Version 2.3 | **Môi trường:** Python 3.11 • GitHub Actions 24/7 • Telegram Bot API

---

## 🎯 I. TỔNG QUAN NÂNG CẤP TẠI VERSION 2.3

Phiên bản 2.3 giải quyết dứt điểm bài toán **"Chạy ngầm định kỳ 24/7 ngay cả khi máy tính cá nhân đã tắt nguồn"**:
1. **GitHub Actions 24/7 Workflow (`deploy/hourly_watchdog.yml`):**
   * Kích hoạt tự động mỗi 1 giờ trên máy chủ Cloud độc lập của GitHub/Microsoft.
   * Chạy toàn bộ regression test kiểm tra Model Cloud, Vector DB và luồng LangGraph.
2. **Kênh Thông báo Tức thời về Điện thoại (Telegram Bot Notifier):**
   * Tự động gửi tin nhắn báo cáo sức khỏe hệ thống về tài khoản Telegram của bạn sau mỗi chu kỳ kiểm tra.

---

## 📱 II. HƯỚNG DẪN 2 PHÚT THIẾT LẬP TELEGRAM BOT

Để nhận thông báo trực tiếp về điện thoại của bạn:

### Bước 1: Lấy `TELEGRAM_BOT_TOKEN` (Miễn phí 100%)
1. Mở ứng dụng Telegram trên điện thoại hoặc máy tính.
2. Tìm kiếm bot chính thức: **`@BotFather`** (có tích xanh).
3. Gửi lệnh: `/newbot`
4. Đặt tên hiển thị cho Bot (ví dụ: `My LegalTech Watchdog`) và username (ví dụ: `legaltech_watchdog_bot`).
5. `@BotFather` sẽ gửi lại cho bạn chuỗi **HTTP API Token** có dạng:
   `7123456789:AAFlxyz...` (Đây chính là `TELEGRAM_BOT_TOKEN`).

### Bước 2: Lấy `TELEGRAM_CHAT_ID` của bạn
1. Tìm kiếm bot: **`@userinfobot`** trên Telegram.
2. Bấm **Start** (`/start`).
3. Bot sẽ trả về thông tin cá nhân của bạn, bao gồm dòng:
   `Id: 123456789` (Đây chính là `TELEGRAM_CHAT_ID`).
4. **Quan trọng:** Mở bot bạn vừa tạo ở Bước 1 và bấm nút **Start** một lần để cho phép bot gửi tin nhắn cho bạn.

---

## 🔐 III. CẤU HÌNH BÍ MẬT (SECRETS CONFIGURATION)

### 1. Cấu hình chạy trên máy cá nhân (Local):
Mở file `.env` tại thư mục gốc và dán 2 giá trị vừa lấy:
```env
TELEGRAM_BOT_TOKEN=7123456789:AAFlxyz...
TELEGRAM_CHAT_ID=123456789
```

### 2. Cấu hình chạy tự hành 24/7 trên Cloud (GitHub Actions):
Để GitHub Cloud có thể tự chạy khi bạn tắt máy và bắn tin nhắn về điện thoại:
1. Truy cập repository của bạn trên GitHub: `https://github.com/snowflake-vibing/LLM_Nhut`
2. Vào tab **Actions** $\rightarrow$ chọn **New workflow** $\rightarrow$ chọn **Set up a workflow yourself** (đặt tên file là `hourly_watchdog.yml`).
3. Dán toàn bộ nội dung từ file mẫu `deploy/hourly_watchdog.yml` vào và bấm **Commit changes**.
4. Vào **Settings** $\rightarrow$ chọn mục **Secrets and variables** $\rightarrow$ chọn **Actions**.
5. Bấm nút **New repository secret** và thêm 3 biến sau:
   - `GOOGLE_API_KEY`: Key Gemini của bạn.
   - `TELEGRAM_BOT_TOKEN`: Token bot lấy từ `@BotFather`.
   - `TELEGRAM_CHAT_ID`: ID cá nhân lấy từ `@userinfobot`.

---

## 🔬 IV. KỊCH BẢN KIỂM THỬ THỰC TẾ

### KỊCH BẢN 1: Chạy Thử nghiệm Watchdog gửi Telegram tại Cục bộ (Local CLI)
Sau khi điền token vào `.env`, chạy lệnh:
```powershell
python scripts/hourly_agent_watchdog.py
```
**Kỳ vọng:**
- Màn hình console xuất thông báo:
  `[Telegram] 📱 Đã gửi thông báo thành công về điện thoại qua Telegram Bot! ✅`
- Điện thoại của bạn ting ting nhận được tin nhắn từ Bot với đầy đủ trạng thái Model, Vector Chunks và LangGraph Workflow.

### KỊCH BẢN 2: Kích hoạt Thủ công trên GitHub Actions (Cloud)
1. Vào tab **Actions** trên GitHub repository: `https://github.com/snowflake-vibing/LLM_Nhut/actions`.
2. Chọn workflow **"⏱️ 24/7 Autonomous LegalTech Watchdog & Agent Regression"**.
3. Bấm **Run workflow** $\rightarrow$ chọn branch `main` $\rightarrow$ bấm nút xanh **Run workflow**.
4. **Kỳ vọng:**
   - GitHub Cloud khởi tạo máy ảo Ubuntu, cài đặt dependencies và thực thi kiểm thử.
   - Sau ~45 giây, workflow hoàn thành tích xanh ✅ và điện thoại của bạn nhận được tin nhắn báo cáo từ Telegram Bot!
