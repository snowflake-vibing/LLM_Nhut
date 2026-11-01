"""
Real-time Telegram Interactive Bot Daemon Agent - Version 2.7
Tiến trình nền chạy liên tục (Daemon) phản hồi tin nhắn tức thời (< 1 giây) từ Telegram:
- Xử lý lệnh điều khiển tự hành (/start, /end, /status).
- Hỗ trợ tư vấn pháp lý trực tiếp 24/7 ngay trong khung chat Telegram bằng lõi LangGraph.
"""

import os
import sys
import time
import requests
from dotenv import load_dotenv

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

load_dotenv()

from src.security.telegram_remote_controller import TelegramRemoteController
from src.agents.graph import LegalMultiAgentWorkflow


def run_telegram_daemon():
    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id_target = os.getenv("TELEGRAM_CHAT_ID", "").strip()

    if not token or not chat_id_target:
        print("[Telegram Daemon] ❌ Lỗi: Chưa cấu hình TELEGRAM_BOT_TOKEN hoặc TELEGRAM_CHAT_ID trong .env!")
        return

    print("==================================================")
    print("🤖 TELEGRAM INTERACTIVE BOT DAEMON AGENT STARTED")
    print(f"📡 Target Chat ID: {chat_id_target}")
    print("⚡ Real-time Long-polling Mode: Active (Sub-second response)")
    print("==================================================")

    controller = TelegramRemoteController()
    workflow = None  # Lazy loading để khởi động cực nhanh

    state = controller.get_state()
    offset = state.get("last_update_id", 0) + 1

    while True:
        try:
            url = f"https://api.telegram.org/bot{token}/getUpdates?offset={offset}&timeout=10"
            resp = requests.get(url, timeout=15)
            if resp.status_code != 200:
                time.sleep(2)
                continue

            data = resp.json()
            if not data.get("ok") or not data.get("result"):
                time.sleep(1)
                continue

            for item in data["result"]:
                update_id = item.get("update_id", 0)
                offset = max(offset, update_id + 1)

                msg = item.get("message", {})
                from_chat_id = str(msg.get("chat", {}).get("id", ""))
                text = msg.get("text", "").strip()

                if not text:
                    continue

                # Chỉ phản hồi tin nhắn từ đúng chủ nhân
                if from_chat_id != chat_id_target:
                    continue

                print(f"[Telegram Daemon] 📩 Nhận tin nhắn từ User: '{text}'")

                # 1. XỬ LÝ LỆNH ĐIỀU KHIỂN TỰ HÀNH
                if text in ["/end", "/stop", "end", "stop"]:
                    controller.set_state("paused", "/end", update_id)
                    controller.send_reply(
                        "🛑 *[ĐÃ TẠM DỪNG CHẾ ĐỘ TỰ HÀNH]*\n"
                        "━━━━━━━━━━━━━━━━━━━━\n"
                        "Theo lệnh `/end` của bạn, Antigravity AI Agent đã tạm dừng các chu kỳ phát triển.\n\n"
                        "👉 Gõ `/start` bất kỳ lúc nào để khởi động lại!"
                    )
                    continue

                elif text in ["/start", "/resume", "start", "resume"]:
                    controller.set_state("running", "/start", update_id)
                    controller.send_reply(
                        "🚀 *[ĐÃ KHỞI ĐỘNG LẠI CHẾ ĐỘ TỰ HÀNH]*\n"
                        "━━━━━━━━━━━━━━━━━━━━\n"
                        "Theo lệnh `/start` của bạn, Antigravity AI Agent tiếp tục các chu kỳ phát triển tự hành và sẽ báo cáo đều đặn về đây!"
                    )
                    continue

                elif text in ["/status", "status"]:
                    curr_st = controller.get_state().get("status", "running")
                    status_text = "🟢 Đang chạy (Running)" if curr_st == "running" else "🔴 Đang tạm dừng (Paused)"
                    controller.send_reply(
                        f"ℹ️ *[TRẠNG THÁI HỆ THỐNG HIỆN TẠI]*\n"
                        f"━━━━━━━━━━━━━━━━━━━━\n"
                        f"Trạng thái Tự hành: *{status_text}*\n"
                        f"Phiên bản: *LegalTech Platform v2.7 (Multi-Agent Swarm)*\n"
                        f"Kiến trúc: *LangGraph + Dual-Persona Tester*\n\n"
                        f"💡 *Bạn có thể gõ câu hỏi pháp lý bất kỳ để tôi tư vấn ngay tại đây!*"
                    )
                    continue

                # 2. XỬ LÝ CÂU HỎI TƯ VẤN PHÁP LÝ TRỰC TIẾP TRÊN TELEGRAM
                controller.send_reply("⚖️ *Luật sư AI đang tra cứu và xử lý qua mạng lưới LangGraph...*")

                if workflow is None:
                    workflow = LegalMultiAgentWorkflow()

                res = workflow.process(text)
                resp_content = res.get("response", "Đã xử lý xong.")
                agent_name = res.get("active_agent", "LegalMultiAgent")

                reply_msg = (
                    f"{resp_content}\n\n"
                    f"━━━━━━━━━━━━━━━━━━━━\n"
                    f"🤖 *Xử lý bởi:* `{agent_name}`\n"
                    f"💡 *Gõ /status để xem trạng thái hoặc /end để tạm dừng.*"
                )
                controller.send_reply(reply_msg)
                controller.set_state(controller.get_state().get("status", "running"), "chat", update_id)

        except Exception as e:
            print(f"[Telegram Daemon Exception] {e}")
            time.sleep(2)


if __name__ == "__main__":
    run_telegram_daemon()
