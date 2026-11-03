"""
Plain Legal Glossary (Từ Điển Dân Dã Hóa Thuật Ngữ Pháp Luật) - Version 3.0
Tự động quét và giải thích bình dân hóa 100% thuật ngữ pháp lý chuyên ngành
để người già, người ít học không bị sợ hãi khi đọc câu trả lời của AI hoặc văn bản Tòa án.
"""

from typing import Dict, Any, List
import re


class PlainLegalGlossary:
    """
    Từ điển chuyển ngữ pháp luật sang tiếng đời thường.
    """

    GLOSSARY = {
        "bpkctt": {
            "term": "BPKCTT (Biện pháp khẩn cấp tạm thời)",
            "plain_meaning": "Lệnh Tòa án phong tỏa khẩn cấp tài sản (nhà đất, tài khoản ngân hàng) để bên kia không kịp bán tống bán tháo tẩu tán trước khi xử án.",
            "example": "Ví dụ: Con nợ định bán nhà chuồn đi, bạn xin Tòa BPKCTT để cấm phòng công chứng cho sang tên."
        },
        "biện pháp khẩn cấp tạm thời": {
            "term": "Biện pháp khẩn cấp tạm thời",
            "plain_meaning": "Lệnh Tòa án phong tỏa khẩn cấp tài sản để đối phương không thể tẩu tán tài sản trước khi xét xử.",
            "example": "Ví dụ: Đóng băng tài khoản ngân hàng của con nợ ngay lập tức."
        },
        "thời hiệu khởi kiện": {
            "term": "Thời hiệu khởi kiện",
            "plain_meaning": "Hạn chót mà pháp luật cho phép bạn nộp đơn kiện ra Tòa án (sau thời hạn này Tòa sẽ từ chối giải quyết, coi như mất quyền kiện).",
            "example": "Ví dụ: Tranh chấp hợp đồng vay nợ thời hiệu là 3 năm kể từ ngày hẹn trả nợ."
        },
        "thời hiệu": {
            "term": "Thời hiệu",
            "plain_meaning": "Thời hạn có giá trị hiệu lực do luật định.",
            "example": "Hết thời hiệu thì không còn quyền yêu cầu Tòa can thiệp."
        },
        "thụ lý": {
            "term": "Thụ lý vụ án",
            "plain_meaning": "Tòa án chính thức nhận đơn, vào sổ theo dõi và bắt đầu mở hồ sơ giải quyết vụ việc sau khi bạn đã nộp tiền tạm ứng án phí.",
            "example": "Ví dụ: Khi Tòa thông báo 'Đã thụ lý', nghĩa là hồ sơ của bạn đã được Tòa chấp thuận vào cuộc."
        },
        "phản tố": {
            "term": "Yêu cầu phản tố",
            "plain_meaning": "Bị đơn (người bị kiện) kiện ngược lại người đi kiện ngay trong cùng một vụ án.",
            "example": "Ví dụ: Bạn kiện đòi nợ 100 triệu, bên kia kiện ngược lại bảo bạn làm hỏng đồ của họ trị giá 120 triệu."
        },
        "vi bằng": {
            "term": "Vi bằng (Thừa phát lại)",
            "plain_meaning": "Một văn bản có đóng dấu của Thừa phát lại làm chứng và ghi nhận chính xác những gì mắt thấy tai nghe (tin nhắn Zalo, hình ảnh hiện trạng, giao nhận tiền) để làm bằng chứng thép trước Tòa.",
            "example": "Ví dụ: Người vay chặn Zalo xóa tin nhắn, bạn đi lập vi bằng chụp màn hình tin nhắn để họ không chối cãi được."
        },
        "tạm ứng án phí": {
            "term": "Tạm ứng án phí",
            "plain_meaning": "Khoản tiền bạn phải đóng trước cho Nhà nước (thường bằng 50% tổng án phí) để Tòa án bắt đầu làm việc. Nếu bạn thắng kiện, bên thua kiện phải trả lại tiền này cho bạn.",
            "example": "Ví dụ: Tranh chấp 100 triệu, án phí là 5 triệu thì bạn nộp tạm ứng 2.5 triệu."
        },
        "đơn phương ly hôn": {
            "term": "Đơn phương ly hôn",
            "plain_meaning": "Một bên muốn ly hôn nhưng bên kia không đồng ý, hoặc bên kia bỏ đi biệt tích.",
            "example": "Chỉ cần một người nộp đơn, Tòa vẫn giải quyết nếu có căn cứ mâu thuẫn trầm trọng."
        },
        "thỏa thuận": {
            "term": "Thỏa thuận",
            "plain_meaning": "Hai bên cùng bàn bạc và đồng ý bằng lòng với nhau.",
            "example": "Thỏa thuận miệng hay giấy tờ đều có giá trị nếu có chứng cứ chứng minh."
        }
    }

    @classmethod
    def scan_and_annotate(cls, text: str) -> Dict[str, Any]:
        """
        Quét đoạn văn bản và tìm các thuật ngữ cần giải thích.
        Trả về danh sách các thuật ngữ được tìm thấy kèm giải nghĩa bình dân.
        """
        if not text:
            return {"annotated_terms": [], "count": 0}

        found_terms = []
        lower_text = text.lower()
        for key, info in cls.GLOSSARY.items():
            pattern = r'\b' + re.escape(key) + r'\b'
            if re.search(pattern, lower_text):
                found_terms.append(info)

        return {
            "annotated_terms": found_terms,
            "count": len(found_terms)
        }

    @classmethod
    def format_glossary_box(cls, found_terms: List[Dict[str, str]]) -> str:
        """Định dạng khung ghi chú bình dân cho người dùng."""
        if not found_terms:
            return ""

        lines = ["💡 **Góc Giải Thích Bình Dân (Từ ngữ Tòa án dịch sang tiếng đời thường):**"]
        for item in found_terms:
            lines.append(f"• **{item['term']}:** {item['plain_meaning']} *(Ví dụ: {item['example']})*")
        return "\n".join(lines)
