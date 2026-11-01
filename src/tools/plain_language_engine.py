"""
Plain-Language Legal Engine - Version 2.5
Bộ chuyển đổi Văn phong Pháp lý sang Ngôn ngữ Bình dân (Plain-Language Dual-Persona Switcher).
Gỡ bỏ rào cản thuật ngữ hàn lâm, giải thích thấu tình đạt lý như một người bạn luật sư tận tâm.
"""

from typing import Dict, Any, Optional
from llm_provider.model_factory import ModelFactory


LEGAL_GLOSSARY_PLAIN_EXPLANATIONS: Dict[str, str] = {
    "đương sự": "Các bên liên quan trực tiếp đến vụ việc (người đi kiện hoặc người bị kiện)",
    "thời hiệu khởi kiện": "Hạn chót mà pháp luật cho phép bạn nộp đơn kiện ra Tòa (nếu để quá hạn này thì Tòa sẽ không thụ lý nữa)",
    "vi bằng": "Biên bản ghi nhận sự thật (tin nhắn, giao nhận tiền, hiện trạng) do Thừa phát lại lập, có giá trị như bằng chứng thép trước Tòa",
    "thừa phát lại": "Chuyên viên pháp lý độc lập được Nhà nước bổ nhiệm để đi lập bằng chứng và tống đạt giấy tờ",
    "niêm yết công khai": "Tòa án dán thông báo tại UBND xã và trên báo đài khi đối phương cố tình trốn tránh, sau đó Tòa vẫn xử vắng mặt bình thường",
    "nghĩa vụ liên đới": "Cả hai bên cùng chịu trách nhiệm đền bù; nếu một bên chối thì bên còn lại vẫn phải bồi thường toàn bộ",
    "tài sản chung": "Nhà đất, tiền bạc kiếm được trong thời gian cưới nhau; về nguyên tắc chia đôi có tính đến công sức vun vén của mỗi người",
    "thẩm định tại chỗ": "Thẩm phán và cơ quan tài nguyên môi trường đến tận mảnh đất đo đạc thực tế xem ai lấn chiếm của ai",
    "bồi thường thiệt hại ngoài hợp đồng": "Đền bù thiệt hại khi gây tổn hại đến sức khỏe, danh dự, tài sản của người khác dù hai bên không có hợp đồng ký kết"
}


class PlainLanguageEngine:
    """
    Engine dịch thuật và chuyển hóa văn phong tư pháp sang ngôn ngữ bình dân.
    """

    def __init__(self, factory: Optional[ModelFactory] = None):
        self.factory = factory or ModelFactory()

    def translate_to_plain_language(self, technical_legal_text: str) -> str:
        """
        Dùng LLM chuyển hóa văn bản tư pháp hàn lâm sang phong cách đàm thoại gần gũi, thấu tình đạt lý.
        """
        system_prompt = (
            "Bạn là một Người Bạn Luật Sư (Legal Compassionate Mentor). Nhiệm vụ của bạn là đọc một lời tư vấn "
            "pháp lý mang tính hàn lâm/tố tụng và DIỄN GIẢI LẠI HOÀN TOÀN sang ngôn ngữ bình dân, mộc mạc, gần gũi như "
            "đang ngồi uống cà phê tâm sự và khuyên bảo một người bạn thân đang gặp khó khăn.\n\n"
            "QUY TẮC BẮT BUỘC:\n"
            "1. Tuyệt đối không dùng từ ngữ quá trang nghiêm hoặc phức tạp. Giải thích thuật ngữ bằng ví von đời thường.\n"
            "2. Giữ vững 100% bản chất pháp lý, căn cứ luật và quyền lợi của người dân.\n"
            "3. Trình bày ngắn gọn theo 3 mục rõ ràng:\n"
            "   - 💡 Tóm lại câu chuyện của bạn bằng lời bình dân\n"
            "   - 🧭 3 Bước bạn nên làm ngay hôm nay (Dễ làm, không cần sợ hãi)\n"
            "   - ⚠️ Lời khuyên chân thành để tránh bị thiệt thòi hoặc bị đối phương lừa\n"
        )

        prompt = f"Hãy diễn giải lại toàn bộ đoạn tư vấn pháp lý sau đây sang ngôn ngữ bình dân dễ hiểu nhất:\n\n{technical_legal_text}"

        try:
            return self.factory.generate(prompt=prompt, system_prompt=system_prompt)
        except Exception:
            # Fallback nếu mất mạng: thay thế từ điển cục bộ
            fallback = technical_legal_text
            for term, exp in LEGAL_GLOSSARY_PLAIN_EXPLANATIONS.items():
                fallback = fallback.replace(term, f"**{term}** (*{exp}*)")
            return f"### ☕ Giải thích Bình dân (Fallback Mode):\n\n{fallback}"
