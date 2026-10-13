"""
Output Moderation & Disclaimer Module
Kiểm duyệt đầu ra, đảm bảo tính chuẩn mực và tự động đính kèm khuyến cáo pháp lý (Legal Disclaimer).
"""

from typing import Tuple


class OutputModerator:
    """
    Kiểm duyệt nội dung câu trả lời của mô hình và bổ sung tuyên bố từ chối trách nhiệm.
    """

    LEGAL_DISCLAIMER = (
        "\n\n---\n"
        "*⚠️ KHUYẾN CÁO PHÁP LÝ: Thông tin do Trợ lý AI cung cấp mang tính chất tham khảo và định hướng thủ tục hành chính "
        "dựa trên các văn bản quy phạm pháp luật hiện hành. Người dùng nên tham vấn ý kiến chính thức từ cơ quan đăng ký kinh doanh "
        "hoặc luật sư chuyên trách trước khi thực hiện các giao dịch thực tế.*"
    )

    FORBIDDEN_OUTPUT_PATTERNS = [
        "hướng dẫn trốn thuế thành công",
        "cách thức kê khai khống vốn không bị phát hiện",
        "làm giả con dấu",
    ]

    def moderate_and_append_disclaimer(self, output_text: str) -> Tuple[str, bool]:
        """
        Kiểm tra đầu ra và tự động gắn khuyến cáo pháp lý.
        Returns:
            Tuple[final_output, is_approved]
        """
        lower_output = output_text.lower()
        for pattern in self.FORBIDDEN_OUTPUT_PATTERNS:
            if pattern in lower_output:
                return (
                    "Phát hiện nội dung không phù hợp với chuẩn mực an toàn pháp lý. Câu trả lời đã bị thu hồi.",
                    False
                )

        if OutputModerator.LEGAL_DISCLAIMER not in output_text:
            output_text += OutputModerator.LEGAL_DISCLAIMER

        return output_text, True
