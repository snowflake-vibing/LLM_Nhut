"""
Telegram Remote Controller Module - Version 2.6
Cho phép người dùng điều khiển dừng/bắt đầu chu kỳ tự hành trực tiếp từ chat Telegram qua lệnh /start và /end.
"""

import os
import json
import datetime
import requests
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

STATE_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "data", "autonomous_state.json"
)


class TelegramRemoteController:
    """
    Quản lý trạng thái tự hành và lắng nghe lệnh điều khiển từ Telegram (/start, /end, /status).
    """

    def __init__(self, bot_token: Optional[str] = None, chat_id: Optional[str] = None):
        self.bot_token = bot_token or os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
        self.chat_id = chat_id or os.getenv("TELEGRAM_CHAT_ID", "").strip()
        self._ensure_state_file()

    def _ensure_state_file(self):
        """Khởi tạo file lưu trữ trạng thái nếu chưa tồn tại."""
        os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
        if not os.path.exists(STATE_FILE):
            default_state = {
                "status": "running",
                "last_command": "/start",
                "updated_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "last_update_id": 0,
            }
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(default_state, f, ensure_ascii=False, indent=2)

    def get_state(self) -> Dict[str, Any]:
        """Đọc trạng thái hoạt động hiện tại."""
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"status": "running", "last_command": "/start", "last_update_id": 0}

    def set_state(self, status: str, last_command: str, last_update_id: Optional[int] = None):
        """Cập nhật trạng thái hoạt động."""
        current = self.get_state()
        current["status"] = status
        current["last_command"] = last_command
        current["updated_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if last_update_id is not None:
            current["last_update_id"] = last_update_id

        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(current, f, ensure_ascii=False, indent=2)

    def is_running(self) -> bool:
        """Kiểm tra xem hệ thống có đang ở trạng thái cho phép tự hành hay không."""
        return self.get_state().get("status") == "running"

    def send_reply(self, text: str) -> bool:
        """Gửi phản hồi trực tiếp về Telegram."""
        if not self.bot_token or not self.chat_id:
            return False
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        try:
            r = requests.post(url, json={"chat_id": self.chat_id, "text": text, "parse_mode": "Markdown"}, timeout=10)
            if r.status_code == 200:
                return True
            # Fallback nếu Markdown lỗi
            r_plain = requests.post(url, json={"chat_id": self.chat_id, "text": text}, timeout=10)
            return r_plain.status_code == 200
        except Exception:
            return False

    def poll_and_handle_commands(self) -> Dict[str, Any]:
        """
        Quét các tin nhắn mới nhất từ Telegram để xử lý lệnh /start, /end, /status.
        """
        if not self.bot_token:
            return {"command_found": None, "current_status": "running"}

        state = self.get_state()
        last_id = state.get("last_update_id", 0)

        url = f"https://api.telegram.org/bot{self.bot_token}/getUpdates?offset={last_id + 1}"
        try:
            resp = requests.get(url, timeout=10)
            data = resp.json()
        except Exception:
            return {"command_found": None, "current_status": state.get("status")}

        if not data.get("ok") or not data.get("result"):
            return {"command_found": None, "current_status": state.get("status")}

        command_handled = None
        new_last_id = last_id

        for item in data["result"]:
            new_last_id = max(new_last_id, item.get("update_id", 0))
            msg = item.get("message", {})
            from_chat_id = str(msg.get("chat", {}).get("id", ""))
            text = msg.get("text", "").strip()

            # Chỉ xử lý lệnh từ đúng người dùng đã cấu hình
            if self.chat_id and from_chat_id != self.chat_id:
                continue

            if text in ["/end", "/stop", "end", "stop"]:
                self.set_state("paused", "/end", new_last_id)
                self.send_reply(
                    "🛑 *[ĐÃ TẠM DỪNG CHẾ ĐỘ TỰ HÀNH]*\n"
                    "━━━━━━━━━━━━━━━━━━━━\n"
                    "Theo lệnh `/end` của bạn, Antigravity AI Agent đã tạm dừng các chu kỳ phát triển.\n\n"
                    "👉 Gõ `/start` bất kỳ lúc nào để khởi động lại!"
                )
                command_handled = "/end"

            elif text in ["/start", "/resume", "start", "resume"]:
                self.set_state("running", "/start", new_last_id)
                self.send_reply(
                    "🚀 *[ĐÃ KHỞI ĐỘNG LẠI CHẾ ĐỘ TỰ HÀNH]*\n"
                    "━━━━━━━━━━━━━━━━━━━━\n"
                    "Theo lệnh `/start` của bạn, Antigravity AI Agent tiếp tục các chu kỳ phát triển tự hành và sẽ báo cáo đều đặn về đây!"
                )
                command_handled = "/start"

            elif text in ["/status", "status"]:
                curr_st = self.get_state().get("status", "running")
                status_text = "🟢 Đang chạy (Running)" if curr_st == "running" else "🔴 Đang tạm dừng (Paused)"
                self.send_reply(
                    f"ℹ️ *[TRẠNG THÁI HỆ THỐNG HIỆN TẠI]*\n"
                    f"━━━━━━━━━━━━━━━━━━━━\n"
                    f"Trạng thái: *{status_text}*\n"
                    f"Phiên bản: *LegalTech Platform v2.5*\n"
                    f"Lệnh điều khiển: Gõ `/end` để dừng, `/start` để tiếp tục."
                )
                command_handled = "/status"

        if new_last_id > last_id and not command_handled:
            # Cập nhật update_id ngay cả khi không có command để không đọc lại tin cũ
            self.set_state(state.get("status", "running"), state.get("last_command", "/start"), new_last_id)

        return {
            "command_found": command_handled,
            "current_status": self.get_state().get("status", "running")
        }
