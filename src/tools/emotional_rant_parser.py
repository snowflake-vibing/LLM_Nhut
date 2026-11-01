"""
Emotional Disjointed Rant Parser & Socratic Guide - Version 2.8
Chuyên biệt hóa xử lý người dùng không hiểu luật, nói chuyện lộn xộn, dài dòng, ngập tràn cảm xúc uất ức.
Trấn an tâm lý trước tiên -> Bóc tách cốt lõi sự việc -> Dẫn dắt bằng câu hỏi Có/Không đơn giản.
"""

import re
from typing import Dict, Any, Optional
from llm_provider.model_factory import ModelFactory


EMOTIONAL_KEYWORDS = [
    "cứu tôi với", "uất ức", "tức quá", "khóc", "bế tắc", "trời ơi", "lừa đảo",
    "bị ép", "không còn cách nào", "khốn nạn", "đè đầu", "mất hết", "sợ quá",
    "không biết làm sao", "tuyệt vọng", "oan ức", "bất công", "giúp gia đình tôi"
]


class EmotionalRantParser:
    """
    Bộ gạn lọc cảm xúc và dẫn dắt Socratic cho người dùng nói chuyện không đâu vào đâu.
    """

    def __init__(self, factory: Optional[ModelFactory] = None):
        self.factory = factory or ModelFactory()

    def is_emotional_or_disjointed(self, text: str) -> bool:
        """Nhận diện câu chuyện mang tính cảm xúc lộn xộn hoặc dài dòng bế tắc."""
        text_lower = text.lower()
        has_keywords = any(kw in text_lower for kw in EMOTIONAL_KEYWORDS)
        is_long_or_rambling = len(text.split()) > 40
        has_multiple_exclamations = text.count("!") >= 2 or text.count("?") >= 2
        return has_keywords or (is_long_or_rambling and has_multiple_exclamations)

    def parse_and_clarify(self, raw_rant: str) -> Dict[str, Any]:
        """
        Trấn an tâm lý, bóc tách sự việc và sinh bộ câu hỏi dẫn dắt từng bước.
        """
        system_prompt = (
            "Bạn là một Luật Sư Trưởng kiêm Chuyên Gia Tâm Lý Xã Hội (Empathetic Senior Legal Counselor). "
            "Trước mặt bạn là một người dân nghèo, người già hoặc người không am hiểu công nghệ/pháp luật. "
            "Họ đang vô cùng đau khổ, uất ức, vừa khóc vừa kể một câu chuyện dài dòng, lộn xộn, không đầu không đuôi.\n\n"
            "NHIỆM VỤ CỦA BẠN TUÂN THỦ NGHIÊM NGẶT 3 BƯỚC:\n"
            "BƯỚC 1 - TRẤN AN & LÀM CHỖ DỰA: Viết 1-2 câu ngắn xoa dịu nỗi đau, khẳng định rằng bạn đang lắng nghe, "
            "pháp luật luôn có cách bảo vệ người lương thiện, và họ không hề cô độc.\n"
            "BƯỚC 2 - GẠN ĐỤC KHƠI TRONG: Bóc tách câu chuyện lộn xộn của họ thành 3 ý cốt lõi mộc mạc:\n"
            "  - Đối tượng gây tổn hại là ai?\n"
            "  - Thiệt hại cụ thể mà họ phải gánh chịu là gì?\n"
            "  - Thời điểm xảy ra sự việc ước tính khi nào?\n"
            "BƯỚC 3 - BỘ CÂU HỎI HƯỚNG DẪN TỪNG BƯỚC (SOCRATIC GUIDE): Đưa ra 3 câu hỏi cực kỳ ngắn gọn, dễ hiểu "
            "để họ chỉ cần trả lời 'CÓ' hoặc 'KHÔNG' (hoặc chọn 1 trong 2 đáp án đơn giản), ví dụ: 'Bác có giữ giấy viết tay không ạ?', 'Có ai nhìn thấy sự việc không ạ?'.\n\n"
            "Văn phong phải cực kỳ ấm áp, kính trọng, xưng hô gần gũi ('Bác/Cô/Chú/Bạn' và 'Cháu/Tôi'). Tuyệt đối không dùng thuật ngữ hàn lâm."
        )

        prompt = f"Lời chia sẻ đầy cảm xúc của người dùng:\n\"\"\"{raw_rant}\"\"\""

        try:
            clarification_text = self.factory.generate(prompt=prompt, system_prompt=system_prompt)
        except Exception:
            clarification_text = (
                "❤️ **Xin bạn hãy bình tĩnh, tôi đã lắng nghe trọn vẹn câu chuyện của bạn!**\n\n"
                "Tôi hiểu bạn đang rất hoang mang và lo lắng. Hãy hít một hơi thật sâu, pháp luật luôn có cơ chế "
                "bảo vệ quyền lợi chính đáng cho bạn. Chúng ta sẽ cùng nhau tháo gỡ từng bước một cách bình tĩnh nhất nhé.\n\n"
                "👉 **Để giúp bạn xử lý ngay, xin bạn trả lời nhanh 3 câu hỏi đơn giản này giúp tôi:**\n"
                "1. Bạn có giữ bất kỳ giấy tờ, tin nhắn hay bằng chứng nào về việc này không? (Có / Không)\n"
                "2. Việc này xảy ra cách đây bao lâu rồi ạ?\n"
                "3. Đối phương hiện có còn ở địa phương không hay đã bỏ trốn?"
            )

        return {
            "is_emotional": True,
            "response": clarification_text,
            "quick_yes_no_options": [
                "1. Có, tôi có giữ giấy tờ/tin nhắn",
                "2. Không, tôi không có giấy tờ gì cả",
                "3. Tôi không chắc chắn"
            ]
        }
