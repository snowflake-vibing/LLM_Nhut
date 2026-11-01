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
from src.agents.holistic_evaluator import HolisticAuditEngine
from src.tools.emotional_rant_parser import EmotionalRantParser


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
                        f"Phiên bản: *LegalTech Platform v2.9 (Holistic 360° Audit Suite)*\n"
                        f"Kiến trúc: *LangGraph + 4-Trụ Cột (UI • UX • Backend • Testing)*\n\n"
                        f"💡 *Các lệnh hữu ích:*\n"
                        f"• `/audit` - Xuất Bảng Đánh Giá Đa Chiều 360° (UI, UX, Backend, Testing)\n"
                        f"• `/end` - Tạm dừng tự hành | `/start` - Tiếp tục tự hành\n"
                        f"• Nhắn tin tâm sự hoặc hỏi luật trực tiếp để nhận tư vấn ngay lập tức!"
                    )
                    continue

                elif text in ["/audit", "/eval", "/danhgia", "/matrix", "audit", "danhgia", "danh gia"]:
                    controller.send_reply("⏳ *Đang tiến hành kiểm định toàn diện 360° (UI • UX • Backend • Testing)...*")
                    audit_engine = HolisticAuditEngine()
                    summary_report = audit_engine.generate_telegram_summary()
                    controller.send_reply(summary_report)
                    controller.set_state(controller.get_state().get("status", "running"), "/audit", update_id)
                    continue

                # Kiểm tra nếu người dùng yêu cầu đánh giá tự nhiên
                lower_text = text.lower()
                if any(k in lower_text for k in ["đánh giá", "kiểm định", "chấm điểm", "audit", "đánh giá app", "đánh giá bot"]):
                    controller.send_reply("⏳ *Đang kích hoạt Bộ máy Kiểm định Đa Chiều 360°...*")
                    audit_engine = HolisticAuditEngine()
                    summary_report = audit_engine.generate_telegram_summary()
                    controller.send_reply(summary_report)
                    controller.set_state(controller.get_state().get("status", "running"), "audit_query", update_id)
                    continue

                # 2. XỬ LÝ CÂU HỎI TƯ VẤN PHÁP LÝ TRỰC TIẾP TRÊN TELEGRAM
                rant_parser = EmotionalRantParser()
                is_rant = rant_parser.is_emotional_rant(text)

                if is_rant:
                    controller.send_reply("💬 *Phát hiện tâm sự uất ức / hoang mang. Đang bóc tách sự việc và trấn an tâm lý...*")
                else:
                    controller.send_reply("⚖️ *Luật sư AI đang tra cứu và xử lý qua mạng lưới LangGraph...*")

                if workflow is None:
                    workflow = LegalMultiAgentWorkflow()

                res = workflow.process(text)
                resp_content = res.get("response", "Đã xử lý xong.")
                agent_name = res.get("active_agent", "LegalMultiAgent")

                if is_rant:
                    empathy_res = rant_parser.parse_and_soothe(text)
                    reply_msg = (
                        f"🤝 *[LỜI TRẤN AN & BÓC TÁCH TÌNH HUỐNG]*\n\n"
                        f"{empathy_res['comfort_message']}\n\n"
                        f"📋 *3 Điểm Cốt Lõi:*\n" +
                        "\n".join([f"• {f}" for f in empathy_res['facts']]) + "\n\n"
                        f"❓ *Câu hỏi giúp tháo gỡ (Trả lời Có / Không):*\n" +
                        "\n".join([f"{i+1}. {q}" for i, q in enumerate(empathy_res['yes_no_questions'])]) + "\n\n"
                        f"━━━━━━━━━━━━━━━━━━━━\n"
                        f"⚖️ *Căn Cứ Pháp Lý & Phương Án:*\n"
                        f"{resp_content}\n\n"
                        f"🤖 *Xử lý bởi:* `{agent_name}` + `EmotionalRantDeNoiser`"
                    )
                else:
                    reply_msg = (
                        f"{resp_content}\n\n"
                        f"━━━━━━━━━━━━━━━━━━━━\n"
                        f"🤖 *Xử lý bởi:* `{agent_name}`\n"
                        f"💡 *Gõ /audit để xem bảng đánh giá 360° hoặc /end để tạm dừng.*"
                    )
                controller.send_reply(reply_msg)
                controller.set_state(controller.get_state().get("status", "running"), "chat", update_id)

        except Exception as e:
            print(f"[Telegram Daemon Exception] {e}")
            time.sleep(2)


if __name__ == "__main__":
    run_telegram_daemon()
