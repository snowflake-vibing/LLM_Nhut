"""
Module: OnboardingTutorial - Hướng Dẫn Sử Dụng Nhanh Cho Người Mới
Giúp người dân, người già, người không rành công nghệ nắm bắt cách dùng app trong 1 phút.
"""

from typing import List, Dict, Any


class OnboardingTutorial:
    """Cung cấp nội dung và các bước hướng dẫn người mới sử dụng."""

    STEPS = [
        {
            "step": 1,
            "icon": "🚀",
            "title": "Vào Nhanh Bằng Tài Khoản Demo (1-Chạm)",
            "desc": "Không cần đăng ký phức tạp! Bạn chỉ cần bấm vào một trong 4 hồ sơ mẫu (Bác Ba - Đất đai, Chị Lan - Vay tiền, Anh Hoàng - Ly hôn, Cụ Sáu - Thừa kế) để trải nghiệm ngay."
        },
        {
            "step": 2,
            "icon": "💬",
            "title": "Tâm Sự Bằng Tiếng Đời Thường",
            "desc": "Trình bày câu chuyện của bạn bằng ngôn ngữ tự nhiên hoặc gửi ảnh giấy nợ/sổ đỏ. Hệ thống tự động hiểu và không bắt bẻ thuật ngữ luật hàn lâm."
        },
        {
            "step": 3,
            "icon": "⚖️",
            "title": "Luật Sư AI Thăm Khám Từng Bước",
            "desc": "Luật sư sẽ lắng nghe ân cần, hỏi từng bước để nắm rõ sự việc, tuyệt đối không trả lời dồn dập khiến bạn bị bối rối."
        },
        {
            "step": 4,
            "icon": "📦",
            "title": "Nhận Kết Quả & Hồ Sơ Hoàn Chỉnh",
            "desc": "Tính án phí, phát hiện bẫy tín dụng đen, tra cứu Tòa án thẩm quyền và tải về Đơn khởi kiện chuẩn Mẫu 23-DS (.docx) nộp Tòa án!"
        }
    ]

    @classmethod
    def get_tutorial_steps(cls) -> List[Dict[str, Any]]:
        return cls.STEPS
