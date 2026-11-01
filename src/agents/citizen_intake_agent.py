"""
Citizen Socratic Legal Intake Agent - Version 3.0
Tác nhân Thăm khám Pháp lý Từng bước Dành riêng cho Cá nhân & Người dân:
- Không trả lời dồn dập hay trút một đống điều luật phức tạp.
- Lắng nghe, trấn an và đặt tối đa 1-2 câu hỏi gợi mở trọng tâm.
- Cung cấp sẵn các lựa chọn trả lời nhanh (A/B/C hoặc Có/Không) để người già và người ít thạo công nghệ dễ tương tác.
- Chỉ đưa ra phương án xử lý khi đã làm rõ sự việc và bằng chứng thực tế.
"""

from typing import Dict, Any, List, Optional
from llm_provider.model_factory import ModelFactory


class CitizenIntakeAgent:
    """
    Tác nhân đồng hành cùng người dân: Thăm khám từng bước, hỏi kỹ để bảo vệ quyền lợi chắc chắn.
    """

    def __init__(self, factory: Optional[ModelFactory] = None):
        self.factory = factory or ModelFactory()

    def analyze_intake_stage(self, history: List[Dict[str, str]], latest_query: str) -> Dict[str, Any]:
        """
        Phân tích chặng thăm khám hiện tại dựa trên lịch sử hội thoại:
        - STAGE 1: TRIAGE_AND_CLARIFY (Lắng nghe sự việc sơ bộ & hỏi 1-2 câu then chốt).
        - STAGE 2: EVIDENCE_CHECK (Hỏi về tài liệu, chứng cứ người dân đang nắm giữ).
        - STAGE 3: GOAL_CONFIRMATION (Hỏi mục tiêu người dân muốn đạt được: hòa giải, đòi tiền, tố giác hay kiện tụng).
        - STAGE 4: ACTIONABLE_ADVICE (Tổng kết phương án 3 bước bình dân khi đã đủ thông tin).
        """
        # Nếu chưa có lịch sử đối thoại hoặc mới nhắn 1 câu -> Stage 1
        user_msgs = [m for m in history if m.get("role") == "user"]
        msg_count = len(user_msgs)

        q_lower = latest_query.lower()

        # Nhận diện các lĩnh vực phổ biến của người dân
        topic = "CIVIL_GENERAL"
        if any(k in q_lower for k in ["đất", "ranh", "sổ đỏ", "lấn", "ngõ", "nhà"]):
            topic = "LAND_DISPUTE"
        elif any(k in q_lower for k in ["nợ", "mượn tiền", "vay", "quỵt", "trốn", "đòi nợ"]):
            topic = "DEBT_COLLECTION"
        elif any(k in q_lower for k in ["ly hôn", "con", "chồng", "vợ", "tài sản chung", "nuôi con"]):
            topic = "FAMILY_DIVORCE"
        elif any(k in q_lower for k in ["lừa", "mạng", "app", "chuyển khoản", "chiếm đoạt"]):
            topic = "ONLINE_FRAUD"
        elif any(k in q_lower for k in ["đánh", "chửi", "đe dọa", "xúc phạm", "hành hung"]):
            topic = "ASSAULT_THREAT"

        return {
            "msg_count": msg_count,
            "topic": topic,
            "is_citizen_scope": True
        }

    def respond(self, query: str, history: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
        """
        Sinh phản hồi thăm khám từng bước:
        - Trấn an, đồng cảm ngắn gọn.
        - Đặt 1-2 câu hỏi xác minh tình tiết cốt lõi (Không hỏi dồn dập).
        - Đưa ra 2-4 nút chọn nhanh (Quick-reply options).
        """
        history = history or []
        stage_info = self.analyze_intake_stage(history, query)
        msg_count = stage_info["msg_count"]
        topic = stage_info["topic"]

        system_prompt = (
            "Bạn là 'Luật sư Dân gian Đồng hành' - chuyên gia pháp lý tận tụy dành riêng cho CÁ NHÂN VÀ NGƯỜI DÂN VIỆT NAM.\n"
            "NGUYÊN TẮC VÀNG BẮT BUỘC:\n"
            "1. TUYỆT ĐỐI KHÔNG TRẢ LỜI DỒN DẬP: Không liệt kê một tràng dài các điều luật khô khan, không xả chữ khiến người dân bị ngợp hoặc hoang mang.\n"
            "2. HỎI ĐỂ CHẮC CHẮN: Luôn hỏi 1 hoặc tối đa 2 câu hỏi trọng tâm nhất để xác định rõ sự việc, chứng cứ hoặc mong muốn của người dân trước khi kết luận.\n"
            "3. NGÔN TỪ GẦN GŨI: Xưng hô 'mình' và 'bạn' (hoặc bác/cô/chú nếu người lớn tuổi), mộc mạc như một người bạn hiểu luật đang ngồi lắng nghe bên tách trà.\n"
            "4. ĐÍNH KÈM CÁC LỰA CHỌN TRẢ LỜI NHANH (A/B/C hoặc Có/Không): Để người dân (đặc biệt là người già hoặc người không quen bấm phím) có thể chọn ngay.\n\n"
            "Cấu trúc phản hồi chuẩn:\n"
            "- Lời chào & đồng cảm ngắn (1-2 câu).\n"
            "- Ghi nhận sơ bộ vấn đề của bạn.\n"
            "- 1 đến 2 câu hỏi thăm khám ngắn gọn để hiểu chắc chắn sự việc.\n"
            "- Gợi ý các lựa chọn trả lời nhanh."
        )

        prompt = (
            f"Vấn đề người dân đang chia sẻ:\n\"{query}\"\n\n"
            f"Số lượt trao đổi trước đó: {msg_count}\n"
            f"Lĩnh vực đời sống nhận diện: {topic}\n\n"
            f"Hãy phản hồi theo đúng nguyên tắc: Đồng cảm -> Hỏi 1-2 câu xác thực then chốt -> Đưa ra các gợi ý trả lời nhanh dạng [A], [B], [C]."
        )

        try:
            ai_reply = self.factory.generate(prompt=prompt, system_prompt=system_prompt)
        except Exception:
            # Fallback kịch bản thăm khám mẫu chuẩn mực
            if topic == "DEBT_COLLECTION":
                ai_reply = (
                    "Chào bạn, mình hiểu chuyện nợ nần tiền bạc lúc này đang làm bạn rất mệt mỏi và sốt ruột.\n\n"
                    "Để mình tư vấn chính xác phương án đòi lại tiền đúng luật cho bạn, bạn cho mình hỏi 1 ý quan trọng này trước nhé:\n\n"
                    "👉 **Khi cho vay, hai bên có lập giấy tờ viết tay, hợp đồng vay tiền không; hay chỉ có tin nhắn Zalo / biên lai chuyển khoản ngân hàng?**\n\n"
                    "*(Bạn có thể trả lời nhanh theo các lựa chọn bên dưới nhé)*"
                )
            elif topic == "LAND_DISPUTE":
                ai_reply = (
                    "Chào bạn, chuyện đất đai ranh giới với hàng xóm xưa nay rất phức tạp và dễ gây ức chế.\n\n"
                    "Để cùng bạn giải quyết dứt điểm mà không để hàng xóm lấn lướt, bạn cho mình hỏi 1 câu này trước:\n\n"
                    "👉 **Thửa đất nhà bạn hiện tại đã được cấp Giấy chứng nhận quyền sử dụng đất (Sổ đỏ / Sổ hồng) có sơ đồ ranh giới rõ ràng chưa?**\n\n"
                    "*(Bạn chỉ cần nhắn 'Có sổ rồi' hoặc 'Chưa có sổ' nhé)*"
                )
            elif topic == "FAMILY_DIVORCE":
                ai_reply = (
                    "Chào bạn, mình rất chia sẻ với những trăn trở gia đình mà bạn đang phải trải qua.\n\n"
                    "Để hướng dẫn bạn thủ tục bảo vệ quyền nuôi con và tài sản tốt nhất, bạn cho mình hỏi thăm:\n\n"
                    "👉 **Hiện tại hai vợ chồng bạn có thể ngồi lại để thuận tình thỏa thuận được không, hay một bên kiên quyết không đồng ý ly hôn?**\n\n"
                    "*(Bạn chọn giúp mình: Thuận tình hay Đơn phương nhé)*"
                )
            else:
                ai_reply = (
                    "Chào bạn, mình đã lắng nghe chia sẻ của bạn. Bạn hãy yên tâm, mình sẽ đồng hành gỡ rối từng bước cùng bạn.\n\n"
                    "Để chắc chắn về phương án tốt nhất, cho mình hỏi 1 câu ngắn gọn này nhé:\n\n"
                    "👉 **Sự việc này xảy ra cách đây bao lâu rồi, và bạn có đang giữ giấy tờ, hình ảnh hay tin nhắn gì làm chứng không?**"
                )

        # Trích xuất options trả lời nhanh và câu hỏi đào sâu gợi ý
        quick_options = self._extract_quick_options(topic, query)
        suggested_followups = self._extract_suggested_followups(topic, query)

        return {
            "agent": "CitizenIntakeAgent (Luật sư Thăm khám Dân gian)",
            "response": ai_reply,
            "topic": topic,
            "quick_options": quick_options,
            "suggested_followups": suggested_followups,
            "scope": "CITIZEN_INDIVIDUAL"
        }

    def _extract_suggested_followups(self, topic: str, query: str) -> List[str]:
        """Tạo danh sách các câu hỏi pháp lý gợi ý để người dân có thể hỏi thêm Luật sư trong 1 chạm."""
        if topic == "DEBT_COLLECTION":
            return [
                "💰 Án phí Tòa án đòi khoản nợ này tính hết bao nhiêu?",
                "❄️ Làm sao yêu cầu Tòa phong tỏa tài khoản con nợ tránh tẩu tán?",
                "🏃 Nếu con nợ bỏ trốn khỏi địa phương thì Tòa có xử vắng mặt không?",
                "📜 Chi phí và thủ tục lập Vi bằng tin nhắn Zalo ra sao?"
            ]
        elif topic == "LAND_DISPUTE":
            return [
                "🏛️ Nộp đơn yêu cầu hòa giải ở bộ phận nào tại UBND xã/phường?",
                "🛑 Làm sao yêu cầu đình chỉ hàng xóm đang xây lấn chiếm ranh giới?",
                "📐 Chi phí đo đạc lại hiện trạng ranh giới đất hết bao nhiêu?",
                "⏳ Thời hạn UBND xã hòa giải tranh chấp đất đai tối đa bao lâu?"
            ]
        elif topic == "FAMILY_DIVORCE":
            return [
                "👶 Con dưới 36 tháng tuổi mẹ có đương nhiên được quyền nuôi không?",
                "🏠 Nhà đất chung đứng tên 2 người nhưng tiền bố mẹ tôi cho thì chia sao?",
                "💸 Mức cấp dưỡng nuôi con thông thường Tòa án ấn định là bao nhiêu?",
                "⚡ Nếu một bên kiên quyết không ký thì nộp đơn ly hôn đơn phương ở đâu?"
            ]
        elif topic == "ONLINE_FRAUD":
            return [
                "👮 Đơn tố giác tội phạm lừa đảo qua mạng gồm những tài liệu gì?",
                "🏦 Ngân hàng có được phép đóng băng tài khoản người nhận tiền không?",
                "⏳ Công an nhận đơn tố giác thì bao lâu sẽ phản hồi kết quả?"
            ]
        else:
            return [
                "💰 Vụ việc này nếu kiện ra Tòa án thì hết bao nhiêu án phí?",
                "⏳ Thời hiệu khởi kiện vụ việc của tôi còn lại bao nhiêu thời gian?",
                "🏛️ Tôi cần nộp đơn đến cơ quan cụ thể nào có thẩm quyền giải quyết?"
            ]

    def _extract_quick_options(self, topic: str, query: str) -> List[str]:
        """Tạo danh sách các nút bấm trả lời nhanh phù hợp từng tình huống."""
        if topic == "DEBT_COLLECTION":
            return [
                "📝 Có giấy viết tay / hợp đồng vay",
                "📱 Chỉ có tin nhắn Zalo / sao kê ngân hàng",
                "🗣️ Chỉ thỏa thuận miệng, không có giấy tờ",
                "🏃 Con nợ đã cắt liên lạc, bỏ trốn"
            ]
        elif topic == "LAND_DISPUTE":
            return [
                "📗 Đã có Sổ đỏ chính chủ rõ ranh giới",
                "📄 Chưa có sổ đỏ (đất cha ông để lại)",
                "🧱 Hàng xóm đang xây lấn chiếm thực tế",
                "🤝 Muốn hòa giải tại UBND xã/phường"
            ]
        elif topic == "FAMILY_DIVORCE":
            return [
                "🤝 Cả hai cùng thuận tình ly hôn",
                "⚡ Đơn phương ly hôn (một bên không đồng ý)",
                "👶 Đang tranh chấp quyền trực tiếp nuôi con",
                "🏠 Có tranh chấp phân chia nhà đất chung"
            ]
        elif topic == "ONLINE_FRAUD":
            return [
                "💳 Đã chuyển khoản qua tài khoản ngân hàng",
                "📸 Vẫn còn giữ toàn bộ tin nhắn & ảnh bằng chứng",
                "👮 Muốn làm đơn tố giác ra cơ quan Công an"
            ]
        else:
            return [
                "✅ Có giấy tờ / bằng chứng rõ ràng",
                "⚠️ Chỉ có thỏa thuận bằng lời nói",
                "🤝 Muốn giải quyết hòa bình, không ra tòa",
                "⚖️ Muốn khởi kiện chính thức ra Tòa án"
            ]
