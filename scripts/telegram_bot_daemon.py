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

if sys.stdout is None:
    sys.stdout = open(os.devnull, 'w', encoding='utf-8')
elif hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

if sys.stderr is None:
    sys.stderr = open(os.devnull, 'w', encoding='utf-8')
elif hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

load_dotenv()

from src.security.telegram_remote_controller import TelegramRemoteController
from src.agents.graph import LegalMultiAgentWorkflow
from src.agents.holistic_evaluator import HolisticAuditEngine
from src.agents.citizen_intake_agent import CitizenIntakeAgent
from src.agents.grumpy_auditor_agent import GrumpyQualityAuditorAgent
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
                    status_text = "🟢 Đang chạy ngầm (Silent Sentry)" if curr_st == "running" else "🔴 Đang tạm dừng (Paused)"
                    controller.send_reply(
                        f"ℹ️ *[TRẠNG THÁI HỆ THỐNG HIỆN TẠI]*\n"
                        f"━━━━━━━━━━━━━━━━━━━━\n"
                        f"Trạng thái: *{status_text}* (Chống spam: Tự động im lặng 24/7)\n"
                        f"Phiên bản: *LegalTech Platform v3.0 (Citizen-Centric Workstation)*\n"
                        f"Kiến trúc: *10 Công Cụ Dân Sinh 1-Chạm • LangGraph Hybrid AI*\n\n"
                        f"💡 *Các lệnh chủ động theo yêu cầu:*\n"
                        f"• `/session` - Chạy 1 phiên kiểm định khắt khe & bứt phá (6.0đ ➔ >= 9.0đ)\n"
                        f"• `/audit` - Xuất Bảng Đánh Giá Đa Chiều 360° (UI, UX, Backend, Testing)\n"
                        f"• `/critic` - Mời Giám khảo khó tính vào soi lỗi\n"
                        f"• `/end` - Tạm dừng tự hành | `/start` - Tiếp tục tự hành\n"
                        f"• Nhắn tin tâm sự hoặc hỏi luật trực tiếp để nhận tư vấn ngay lập tức!"
                    )
                    continue

                elif text in ["/session", "/breakthrough", "/butpha", "session", "breakthrough", "butpha"]:
                    controller.send_reply("⏳ *Đang tiến hành Chu kỳ Kiểm định Khắt khe & Bứt phá Dân sinh...*")
                    from scripts.continuous_dev_pipeline import run_single_breakthrough_session
                    sess_res = run_single_breakthrough_session(session_num=1, send_telegram=False)
                    controller.send_reply(sess_res["report_msg"])
                    controller.set_state(controller.get_state().get("status", "running"), "/session", update_id)
                    continue

                elif text in ["/audit", "/eval", "/danhgia", "/matrix", "audit", "danhgia", "danh gia"]:
                    controller.send_reply("⏳ *Đang tiến hành kiểm định toàn diện 360° (UI • UX • Backend • Testing)...*")
                    audit_engine = HolisticAuditEngine()
                    summary_report = audit_engine.generate_telegram_summary()
                    controller.send_reply(summary_report)
                    controller.set_state(controller.get_state().get("status", "running"), "/audit", update_id)
                    continue

                elif text in ["/critic", "/grumpy", "/khotinh", "critic", "khotinh"]:
                    controller.send_reply("🧐 *Đang mời Lão Giám Khảo Khó Tính vào soi lỗi và chấm điểm khắt khe...*")
                    grumpy_agent = GrumpyQualityAuditorAgent()
                    critic_report = grumpy_agent.generate_telegram_report()
                    controller.send_reply(critic_report)
                    controller.set_state(controller.get_state().get("status", "running"), "/critic", update_id)
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

                # 2. XỬ LÝ TƯ VẤN PHÁP LÝ CHO CÁ NHÂN & NGƯỜI DÂN (THĂM KHÁM TỪNG BƯỚC, KHÔNG DỒN DẬP)
                controller.send_reply("👂 *Luật sư Dân gian đang lắng nghe và suy ngẫm tình huống của bạn...*")

                intake_agent = CitizenIntakeAgent()
                intake_res = intake_agent.respond(text)
                intake_text = intake_res.get("response", "")
                quick_opts = intake_res.get("quick_options", [])
                suggested_followups = intake_res.get("suggested_followups", [])

                opts_str = ""
                if quick_opts:
                    opts_str = "\n\n👉 *Lựa chọn trả lời nhanh:*\n" + "\n".join(
                        [f"• `{opt}`" for opt in quick_opts]
                    )

                follow_str = ""
                if suggested_followups:
                    follow_str = "\n\n💡 *Gợi ý câu hỏi bạn có thể hỏi tiếp:*\n" + "\n".join(
                        [f"• {fq}" for fq in suggested_followups[:3]]
                    )

                reply_msg = (
                    f"{intake_text}"
                    f"{opts_str}"
                    f"{follow_str}\n\n"
                    f"━━━━━━━━━━━━━━━━━━━━\n"
                    f"👨‍👩‍👧 *Phạm vi:* `Cá nhân & Đời sống Dân sinh`\n"
                    f"💡 *Gõ câu trả lời, hoặc gõ /audit để xem bảng đánh giá hệ thống.*"
                )
                controller.send_reply(reply_msg)
                controller.set_state(controller.get_state().get("status", "running"), "citizen_chat", update_id)

        except Exception as e:
            print(f"[Telegram Daemon Exception] {e}")
            time.sleep(2)


if __name__ == "__main__":
    run_telegram_daemon()
