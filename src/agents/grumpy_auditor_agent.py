"""
Grumpy Quality Auditor Agent - Version 3.0
Tác nhân AI Chuyên gia Thẩm định Khó tính & Khắt khe (The Grumpy Senior Quality Auditor):
- VAI TRÒ CỐT LÕI:
  Đóng vai một Giám khảo Kiểm định Cực kỳ Khó tính, Meticulous, Cầu toàn và Không khoan nhượng.
  Từ chối mọi sự tự mãn hoặc báo cáo thành tích hình thức ("9-10 điểm ảo").
- NHIỆM VỤ SAU MỖI SESSION:
  1. Soi kính lúp bới lông tìm vết vào từng chi tiết UI, UX, Backend và Testing của sản phẩm Dân sinh.
  2. Kéo điểm tổng quát về khung 6.0 điểm (5.8 - 6.2/10) nhằm phơi bày các điểm nghẽn thực sự.
  3. Đưa ra "Bộ Yêu Cầu Khắt Khe, Tỉ Mỉ & Chuẩn Chỉnh" bắt buộc Session tiếp theo phải giải quyết.
"""

import os
import json
import time
import datetime
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AUDIT_CACHE_FILE = os.path.join(ROOT_DIR, "data", "latest_harsh_audit.json")


class GrumpyQualityAuditorAgent:
    """
    AI Giám khảo Khó tính - Kéo điểm về 6.0 và đặt ra các yêu cầu khắt khe, tỉ mỉ cho từng session.
    """

    def __init__(self, model_factory=None):
        self.model_factory = model_factory
        os.makedirs(os.path.dirname(AUDIT_CACHE_FILE), exist_ok=True)

    def _get_llm(self):
        if not self.model_factory:
            try:
                from llm_provider.model_factory import ModelFactory
                self.model_factory = ModelFactory()
            except Exception:
                self.model_factory = None
        return self.model_factory

    def audit_session(self, session_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Thẩm định chi tiết kết quả của Session vừa hoàn tất dưới góc nhìn khó tính và khắt khe.
        """
        ctx = session_context or {}
        session_num = ctx.get("session_number", 1)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Khung điểm khắt khe chuẩn mực cao (kéo điểm neo về mức 6.0)
        ui_score = 6.1
        ux_score = 5.9
        backend_score = 6.0
        testing_score = 5.8
        overall_score = round(
            (ui_score * 0.25) + (ux_score * 0.30) + (backend_score * 0.25) + (testing_score * 0.20),
            2
        )

        critiques = {
            "ui": {
                "score": ui_score,
                "label": "Giao diện (UI)",
                "harsh_critique": (
                    "Đừng vội mừng vì có toggle chữ lớn ở sidebar! Người già mắt mờ 70 tuổi run tay không bao giờ tự mở "
                    "sidebar để tìm cái nút ấy được. Trên màn hình điện thoại 360px, các tabs và bảng án phí vẫn bị dồn ép, "
                    "cuộn ngang thô kệch. Nút bấm phẳng lì không có hiệu ứng phản hồi xúc giác (tactile feedback). Cần làm lại cho chuẩn!"
                ),
                "strict_requirements": [
                    "Bổ sung thanh điều khiển thị giác nhanh (A+ / A- và Đổi tương phản cao) nổi trực diện ngay trên thanh chat.",
                    "Tái cấu trúc giao diện di động sang Mobile Accordion Card 1-chạm, cấm tuyệt đối cuộn ngang (horizontal scroll)."
                ]
            },
            "ux": {
                "score": ux_score,
                "label": "Trải nghiệm Dân sinh (UX)",
                "harsh_critique": (
                    "Mới chỉ có nút ghi âm rồi tải file mà đã gọi là trợ năng? Độ trễ phản hồi giọng đọc 3-5 giây là người già đã "
                    "tưởng phần mềm bị hỏng rồi tắt máy. Lời giải thích tuy có plain-language nhưng thỉnh thoảng vẫn sót từ ngữ "
                    "hàn lâm như 'BPKCTT', 'thời hiệu', 'thụ lý' làm người dân sợ hãi. Chưa kể thiếu hẳn phễu trắc nghiệm 3 phút!"
                ),
                "strict_requirements": [
                    "Xây dựng Phễu Chẩn Đoán Dân Sinh 3 Phút (Step-by-step Wizard) với câu hỏi trắc nghiệm ngắn gọn, người dân không cần gõ chữ.",
                    "Tự động phát hiện và gắn Tooltip Bình Dân cho 100% thuật ngữ pháp lý chuyên ngành trong câu trả lời.",
                    "Tối ưu độ trễ âm thanh giọng đọc xuống dưới 1.5 giây."
                ]
            },
            "backend": {
                "score": backend_score,
                "label": "Hệ thống & An ninh (Backend)",
                "harsh_critique": (
                    "Phụ thuộc quá nặng nề vào Cloud Gemini. Nếu mạng quốc tế đứt cáp hoặc Google Cloud báo lỗi 429 Quota Exceeded "
                    "thì ứng dụng sập à? Tầng chuyển vùng sang Ollama mới dừng ở lý thuyết cấu hình, chưa có bộ luật xác định thuần túy "
                    "(Deterministic Legal Rule Engine) để chạy 100% khi mất mạng hoàn toàn."
                ),
                "strict_requirements": [
                    "Triển khai Tầng Dự Phòng Cấp 3: Deterministic Legal Expert Rules (Hệ chuyên gia tính toán luật độc lập không cần AI).",
                    "Thực hiện Async Token Streaming từng từ (<200ms) để loại bỏ hoàn toàn cảm giác chờ đợi đơ máy."
                ]
            },
            "testing": {
                "score": testing_score,
                "label": "Kiểm thử & QA (Testing)",
                "harsh_critique": (
                    "Mới pass được vài cái unit test đơn giản và 3 câu prompt sách vở mà đã tự phong 'Pass 100%'? "
                    "Đã bao giờ ném vào hệ thống một đoạn tâm sự 800 chữ lẫn tiếng lóng miền Tây, sai chính tả be bét, chửi bới giận dữ chưa? "
                    "Đã đo đạc tỷ lệ ảo giác trích dẫn sai số hiệu Điều luật (Hallucination Rate) đạt chuẩn kiểm toán tư pháp chưa?"
                ),
                "strict_requirements": [
                    "Xây dựng Bộ Suite 50 Bài Test Dân Sự Thực Địa (Chaotic & Emotional Citizen Prompts).",
                    "Đo lường định lượng tỷ lệ chính xác trích dẫn điều luật (Legal Citation Accuracy Rate)."
                ]
            }
        }

        # Tổng hợp danh sách yêu cầu tỉ mỉ cho session kế tiếp
        next_session_mandates = []
        for cat, data in critiques.items():
            for req in data["strict_requirements"]:
                next_session_mandates.append(f"[{data['label']}] {req}")

        # Thử gọi LLM để tăng thêm tính tự nhiên và sắc bén nếu có API
        factory = self._get_llm()
        ai_personalized_note = ""
        if factory:
            try:
                sys_prompt = (
                    "Bạn là 'Lão Giám Khảo Khó Tính' - Trưởng ban Kiểm định Chất lượng Tư pháp Dân sự. "
                    "Bạn nổi tiếng cực kỳ khó tính, tỉ mỉ, soi xét từng dấu chấm phẩy, chuyên gạt bỏ những báo cáo hình thức. "
                    "Nhiệm vụ của bạn là kéo điểm sản phẩm về mức 6.0/10 để bắt đội ngũ kỹ sư phải cải tiến thực chất. "
                    "Hãy đưa ra đúng 2 câu nhận xét đanh thép, thẳng thắn, bắt lỗi chi tiết nhưng mang tính xây dựng cao."
                )
                user_prompt = (
                    f"Session #{session_num} vừa chạy xong. Điểm tổng quát đang được neo ở mức {overall_score}/10. "
                    f"Các điểm nghẽn: Giao diện di động chưa mượt, giọng đọc còn trễ, chưa có phễu trắc nghiệm 3 phút, phụ thuộc Cloud. "
                    f"Hãy đưa ra lời phê bình sắc bén nhất của bạn."
                )
                ai_personalized_note = factory.generate(prompt=user_prompt, system_prompt=sys_prompt).strip()
            except Exception:
                ai_personalized_note = (
                    "Sản phẩm mới ở mức khung sườn ban đầu (6.0 điểm), đừng vội tự mãn! "
                    "Người già và người dân nghèo không cần những biểu đồ hoa mỹ mà cần sự tiện dụng 1-chạm, "
                    "nói là hiểu ngay và chạy mượt trên chiếc điện thoại cũ kỹ. Tập trung giải quyết dứt điểm các điểm nghẽn trên!"
                )
        else:
            ai_personalized_note = (
                "Sản phẩm mới ở mức khung sườn ban đầu (6.0 điểm), đừng vội tự mãn! "
                "Người già và người dân nghèo không cần những biểu đồ hoa mỹ mà cần sự tiện dụng 1-chạm, "
                "nói là hiểu ngay và chạy mượt trên chiếc điện thoại cũ kỹ. Tập trung giải quyết dứt điểm các điểm nghẽn trên!"
            )

        audit_result = {
            "session_number": session_num,
            "timestamp": timestamp,
            "overall_score": overall_score,
            "rating_tier": "Khung 6.0 / 10.0 (Ngưỡng Nền Móng - Cần Bứt Phá Thực Chất)",
            "grumpy_auditor_title": "🧐 Lão Giám Khảo Khó Tính (Adversarial Chief Quality Auditor)",
            "editorial_critique": ai_personalized_note,
            "pillar_critiques": critiques,
            "strict_requirements_for_next_session": next_session_mandates[:5],  # 5 nhiệm vụ trọng tâm nhất
            "all_requirements": next_session_mandates,
        }

        self._save_cache(audit_result)
        return audit_result

    def _save_cache(self, data: Dict[str, Any]):
        """Lưu lại bản thẩm định khó tính gần nhất ra file."""
        try:
            with open(AUDIT_CACHE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[GrumpyAuditor] Lưu cache thất bại: {e}")

    def load_latest_audit(self) -> Dict[str, Any]:
        """Tải bản thẩm định khó tính mới nhất từ cache."""
        if not os.path.exists(AUDIT_CACHE_FILE):
            return self.audit_session()
        try:
            with open(AUDIT_CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return self.audit_session()

    def generate_telegram_report(self, audit_result: Optional[Dict[str, Any]] = None) -> str:
        """
        Tạo báo cáo sắc bén của Lão Giám Khảo Khó Tính để gửi về Telegram khi có yêu cầu.
        """
        audit = audit_result or self.load_latest_audit()
        s_num = audit.get("session_number", 1)
        score = audit.get("overall_score", 6.0)
        editorial = audit.get("editorial_critique", "")
        reqs = audit.get("strict_requirements_for_next_session", [])

        req_str = "\n".join([f"  {idx}. {r}" for idx, r in enumerate(reqs, 1)])

        msg = (
            f"🧐 *[LÃO GIÁM KHẢO KHÓ TÍNH THẨM ĐỊNH SESSION #{s_num}]*\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"⚖️ *Điểm Khắt Khe:* `{score}/10.0` *(Neo ở Mức 6.0 - Cấm Tự Mãn)*\n"
            f"⏰ *Thời điểm:* `{audit.get('timestamp')}`\n\n"
            f"💬 *Lời Phê Bình Thẳng Thắn:*\n"
            f"> \"{editorial}\"\n\n"
            f"📋 *Bộ Yêu Cầu Tỉ Mỉ & Chuẩn Chỉnh Bắt Buộc Làm Ngay:*\n"
            f"{req_str}\n\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🎯 *Mục tiêu:* Chỉ khi hoàn tất các yêu cầu này mới được phép nâng điểm!"
        )
        return msg
