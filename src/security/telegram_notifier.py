"""
Telegram Notifier Module - Version 3.0
Hỗ trợ gửi thông báo giám sát và cảnh báo hệ thống 24/7 trực tiếp về điện thoại người dùng qua Telegram Bot API.
Tích hợp bộ lọc chống spam thông minh (Smart Deduplication & Semantic Similarity Filter):
- Tự động so sánh tin nhắn mới với tin nhắn gần nhất đã gửi thành công.
- Nếu tin nhắn mới không có thay đổi bứt phá hoặc tương đồng cao (>= 75% nội dung sau khi chuẩn hóa),
  hệ thống sẽ TỰ ĐỘNG BỎ QUA không gửi Telegram để tránh làm phiền người dùng ("chạy liên tục nhưng không nhắn liên tục").
"""

import os
import re
import json
import difflib
import datetime
import requests
from typing import Optional, Dict, Any, Tuple
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LAST_MESSAGE_FILE = os.path.join(ROOT_DIR, "data", "last_telegram_message.json")


class TelegramNotifier:
    """
    Quản lý kết nối, gửi thông báo qua Telegram Bot và tự động lọc chống spam nội dung lặp lại.
    """

    def __init__(
        self,
        bot_token: Optional[str] = None,
        chat_id: Optional[str] = None,
    ):
        self.bot_token = bot_token or os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
        self.chat_id = chat_id or os.getenv("TELEGRAM_CHAT_ID", "").strip()
        self._ensure_storage()

    def _ensure_storage(self):
        """Đảm bảo thư mục data/ sẵn sàng để lưu vết tin nhắn gần nhất."""
        os.makedirs(os.path.dirname(LAST_MESSAGE_FILE), exist_ok=True)

    def is_configured(self) -> bool:
        """Kiểm tra xem Bot Token và Chat ID đã được cấu hình đầy đủ hay chưa."""
        return bool(
            self.bot_token
            and self.chat_id
            and self.bot_token != "your_telegram_bot_token_here"
            and self.chat_id != "your_telegram_chat_id_here"
        )

    @staticmethod
    def normalize_text(text: str) -> str:
        """
        Loại bỏ các yếu tố nhiễu động (thời gian, ngày tháng, số session, markdown)
        để so sánh bản chất nội dung cốt lõi của thông điệp.
        """
        if not text:
            return ""
        # 1. Xóa định dạng ngày tháng: YYYY-MM-DD, DD/MM/YYYY, DD-MM-YYYY
        cleaned = re.sub(r'\b\d{4}[-/]\d{1,2}[-/]\d{1,2}\b', '', text)
        cleaned = re.sub(r'\b\d{1,2}[-/]\d{1,2}[-/]\d{4}\b', '', cleaned)
        # 2. Xóa giờ phút giây: HH:MM:SS, HH:MM
        cleaned = re.sub(r'\b\d{1,2}:\d{2}(:\d{2})?\b', '', cleaned)
        # 3. Xóa số phiên/session: #123, Session #123, Phiên #123
        cleaned = re.sub(r'#\d+', '', cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r'\bsession\s*\d*\b', '', cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r'\bphiên\s*\d*\b', '', cleaned, flags=re.IGNORECASE)
        # 4. Xóa các ký tự định dạng markdown và biểu tượng thừa
        cleaned = re.sub(r'[*_`~#\[\]\(\)\-\>\=\|•━]', ' ', cleaned)
        # 5. Chuẩn hóa khoảng trắng và chuyển chữ thường
        cleaned = re.sub(r'\s+', ' ', cleaned).strip().lower()
        return cleaned

    def _load_last_message(self) -> Dict[str, Any]:
        """Tải bản ghi tin nhắn gần nhất đã gửi thành công."""
        if not os.path.exists(LAST_MESSAGE_FILE):
            return {}
        try:
            with open(LAST_MESSAGE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def _save_last_message(self, text: str):
        """Lưu lại nội dung tin nhắn vừa gửi thành công."""
        try:
            record = {
                "text": text,
                "normalized": self.normalize_text(text),
                "sent_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            with open(LAST_MESSAGE_FILE, "w", encoding="utf-8") as f:
                json.dump(record, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[TelegramNotifier] Lưu vết tin nhắn thất bại: {e}")

    def check_is_substantially_different(
        self, text: str, threshold: float = 0.75
    ) -> Tuple[bool, float, str]:
        """
        So sánh tin nhắn mới với tin nhắn gần nhất đã gửi thành công.
        Trả về: (is_different, similarity_ratio, reason)
        - Nếu similarity_ratio >= threshold (vd 75% trở lên): coi là "chả khác nhau gì mấy" -> False
        - Nếu similarity_ratio < threshold: có sự thay đổi bứt phá -> True
        """
        last_record = self._load_last_message()
        if not last_record or not last_record.get("text"):
            return True, 0.0, "Tin nhắn đầu tiên của hệ thống"

        norm_new = self.normalize_text(text)
        norm_last = last_record.get("normalized", self.normalize_text(last_record.get("text", "")))

        if not norm_new:
            return False, 1.0, "Nội dung rỗng sau khi chuẩn hóa"

        if norm_new == norm_last:
            return False, 1.0, "Nội dung hoàn toàn trùng khớp sau khi chuẩn hóa (không đổi)"

        similarity = difflib.SequenceMatcher(None, norm_new, norm_last).ratio()
        if similarity >= threshold:
            return (
                False,
                similarity,
                f"Tương đồng {similarity * 100:.1f}% so với tin trước (ngưỡng {threshold * 100:.0f}%), không có thay đổi bứt phá"
            )

        return (
            True,
            similarity,
            f"Nội dung có thay đổi bứt phá (khác biệt {(1 - similarity) * 100:.1f}%)"
        )

    def send_message(
        self,
        text: str,
        parse_mode: str = "Markdown",
        check_similarity: bool = True,
        similarity_threshold: float = 0.75,
        force: bool = False,
    ) -> bool:
        """
        Gửi thông báo văn bản tới Telegram Chat ID đã cấu hình.
        - check_similarity: Tự động so sánh với tin nhắn trước đó, nếu chả khác gì mấy thì không gửi.
        - similarity_threshold: Ngưỡng tương đồng (mặc định 0.75 - 75%).
        - force: Cưỡng chế gửi (bỏ qua kiểm tra độ tương đồng).
        """
        if not self.is_configured():
            return False

        if not force and check_similarity:
            is_diff, sim_ratio, reason = self.check_is_substantially_different(text, similarity_threshold)
            if not is_diff:
                print(f"[TelegramNotifier] 🔕 BỎ QUA GỬI TELEGRAM: {reason} (Chống spam liên tục theo chỉ đạo).")
                return False

        endpoint = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": parse_mode,
            "disable_web_page_preview": True,
        }

        try:
            resp = requests.post(endpoint, json=payload, timeout=15)
            if resp.status_code == 200:
                self._save_last_message(text)
                return True
            # Fallback nếu lỗi cú pháp Markdown: gửi dạng plain text
            payload.pop("parse_mode", None)
            fallback_resp = requests.post(endpoint, json=payload, timeout=15)
            if fallback_resp.status_code == 200:
                self._save_last_message(text)
                return True
            return False
        except Exception as e:
            print(f"[TelegramNotifier Error] {e}")
            return False

    def send_watchdog_report(self, report_data: Dict[str, Any], check_similarity: bool = True) -> bool:
        """
        Định dạng và gửi bản tin sức khỏe hệ thống định kỳ (Watchdog Report).
        Tự động bỏ qua nếu báo cáo không có gì thay đổi so với báo cáo gần nhất.
        """
        timestamp = report_data.get("timestamp", "Vừa xong")
        cloud_status = report_data.get("cloud_status", "N/A")
        local_status = report_data.get("local_status", "N/A")
        vector_count = report_data.get("vector_count", 0)
        agent_status = report_data.get("agent_status", "N/A")
        git_status = report_data.get("git_status", "N/A")

        message = (
            f"⚖️ *[LEGALTECH AI WATCHDOG 24/7]*\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"⏱️ *Thời gian:* `{timestamp}`\n"
            f"☁️ *Cloud Gemini:* {cloud_status}\n"
            f"💻 *Local Ollama:* {local_status}\n"
            f"📚 *Vector Chunks:* `{vector_count}` chunks\n"
            f"🌐 *LangGraph Workflow:* {agent_status}\n"
            f"📦 *Git Status:* {git_status}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"✅ *Hệ thống hoạt động ổn định 24/7!*"
        )

        return self.send_message(message, parse_mode="Markdown", check_similarity=check_similarity)
