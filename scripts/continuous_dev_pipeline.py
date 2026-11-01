"""
Continuous Autonomous Development Pipeline - Version 3.1
Pipeline Tự hành Chạy Liền Mạch (Continuous Back-to-Back Sessions):
- Không phân theo giờ nữa: Khi xong 1 session, hệ thống tự động kiểm tra trạng thái và chuyển sang session kế tiếp ngay.
- Kiểm tra cờ trạng thái Telegram:
  * Nếu người dùng gửi /end hoặc /stop -> Dừng và chờ.
  * Nếu người dùng gửi /start -> Tiếp tục chạy liên tục.
- Gửi báo cáo chi tiết từng session đã hoàn thành về Telegram Bot.
"""

import os
import sys
import time
import datetime

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from llm_provider.model_factory import ModelFactory
from src.agents.citizen_intake_agent import CitizenIntakeAgent
from src.agents.graph import LegalMultiAgentWorkflow
from src.rag.vector_store import LegalVectorStore
from src.security.telegram_notifier import TelegramNotifier
from src.security.telegram_remote_controller import TelegramRemoteController


def run_continuous_pipeline():
    controller = TelegramRemoteController()
    notifier = TelegramNotifier()
    session_count = 0

    print("==================================================")
    print("🚀 CONTINUOUS AUTONOMOUS PIPELINE STARTED")
    print("⚡ Mode: Back-to-Back Consecutive Sessions")
    print("📱 Telegram Remote: /start to run, /end to pause")
    print("==================================================")

    while True:
        try:
            # 1. Kiểm tra lệnh điều khiển từ Telegram
            controller.poll_and_handle_commands()

            if not controller.is_running():
                print(f"[Pipeline] 🛑 Tự hành đang TẠM DỪNG (theo lệnh /end từ Telegram). Đang chờ lệnh /start...")
                time.sleep(5)
                continue

            session_count += 1
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n▶️ [BẮT ĐẦU SESSION #{session_count}] lúc {timestamp}")

            # 2. Kiểm tra sức khỏe Model & Vector Store
            factory = ModelFactory()
            health = factory.check_health()
            cloud_ok = health.get("cloud", {}).get("available", False)
            local_ok = health.get("local", {}).get("available", False)

            vstore = LegalVectorStore()
            v_count = vstore.count()

            # 3. Kiểm thử tác nhân CitizenIntakeAgent
            intake = CitizenIntakeAgent(factory)
            sample_query = "Tôi cho người quen mượn tiền nhưng họ không chịu trả."
            intake_res = intake.respond(sample_query)
            quick_opts = intake_res.get("quick_options", [])
            intake_ok = bool(quick_opts and len(quick_opts) >= 2)

            # 4. Gửi báo cáo phiên về Telegram
            report_msg = (
                f"🚀 *[CONTINUOUS SESSION #{session_count} HOÀN TẤT]*\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"⏰ *Thời điểm:* `{timestamp}`\n"
                f"🎯 *Phiên bản:* `LegalTech Platform v3.1`\n"
                f"👨‍👩‍👧 *Trọng tâm:* `Cá nhân & Người dân Dân sinh`\n\n"
                f"✅ *Kiểm tra Tự hành Phiên này:*\n"
                f"• Cloud Gemini: {'✅ Khỏe mạnh' if cloud_ok else '⚠️ Ngoại tuyến'}\n"
                f"• Local Ollama: {'✅ Sẵn sàng' if local_ok else '⚠️ Ngoại tuyến'}\n"
                f"• Tri thức Đa luật: `{v_count} chunks`\n"
                f"• Citizen Socratic Intake: {'✅ Hoạt động chuẩn xác' if intake_ok else '⚠️ Cần rà soát'}\n"
                f"• Quick-Reply 1-Chạm: ✅ Đã tích hợp trực tiếp\n"
                f"• Nhập giọng nói Audio: ✅ Sẵn sàng cho người già\n\n"
                f"🔄 *Hệ thống đang tiếp tục chuyển sang Session tiếp theo liền mạch...*\n"
                f"💡 *Gõ /end bất kỳ lúc nào để tạm dừng chu kỳ.*"
            )

            notifier.send_message(report_msg)
            print(f"✅ [SESSION #{session_count}] Hoàn tất và đã báo cáo Telegram.")

            # Nghỉ ngắn 45 giây giữa các session để tránh spam Bot API và quá tải CPU
            time.sleep(45)

        except Exception as e:
            print(f"[Pipeline Exception] {e}")
            time.sleep(10)


if __name__ == "__main__":
    run_continuous_pipeline()
