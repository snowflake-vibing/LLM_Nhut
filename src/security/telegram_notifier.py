"""
Telegram Notifier Module - Version 2.3
Hỗ trợ gửi thông báo giám sát và cảnh báo hệ thống 24/7 trực tiếp về điện thoại người dùng qua Telegram Bot API.
"""

import os
import requests
from typing import Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()


class TelegramNotifier:
    """
    Quản lý kết nối và gửi thông báo qua Telegram Bot.
    """

    def __init__(
        self,
        bot_token: Optional[str] = None,
        chat_id: Optional[str] = None,
    ):
        self.bot_token = bot_token or os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
        self.chat_id = chat_id or os.getenv("TELEGRAM_CHAT_ID", "").strip()

    def is_configured(self) -> bool:
        """Kiểm tra xem Bot Token và Chat ID đã được cấu hình đầy đủ hay chưa."""
        return bool(
            self.bot_token
            and self.chat_id
            and self.bot_token != "your_telegram_bot_token_here"
            and self.chat_id != "your_telegram_chat_id_here"
        )

    def send_message(self, text: str, parse_mode: str = "Markdown") -> bool:
        """
        Gửi thông báo văn bản tới Telegram Chat ID đã cấu hình.
        """
        if not self.is_configured():
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
                return True
            # Fallback nếu lỗi cú pháp Markdown: gửi dạng plain text
            payload.pop("parse_mode", None)
            fallback_resp = requests.post(endpoint, json=payload, timeout=15)
            return fallback_resp.status_code == 200
        except Exception:
            return False

    def send_watchdog_report(self, report_data: Dict[str, Any]) -> bool:
        """
        Định dạng và gửi bản tin sức khỏe hệ thống định kỳ (Watchdog Report).
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

        return self.send_message(message, parse_mode="Markdown")
