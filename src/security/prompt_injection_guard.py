"""
Prompt Injection & Jailbreak Guard Module
Phát hiện và ngăn chặn các hành vi tấn công prompt injection,
yêu cầu bẻ khóa system prompt hoặc yêu cầu hướng dẫn lách luật, trốn thuế trái phép.
"""

import re
from typing import Tuple


class PromptInjectionGuard:
    """
    Lớp bảo vệ đầu vào (Input Guardrails) chống tấn công Jailbreak và lạm dụng pháp lý.
    """

    # Danh sách từ khóa tấn công kỹ thuật
    INJECTION_PATTERNS = [
        r"ignore\s+(all\s+)?(previous|above)\s+instructions",
        r"disregard\s+(all\s+)?(previous|above)",
        r"you\s+are\s+now\s+(DAN|unfiltered|jailbroken)",
        r"reveal\s+(your\s+)?(system\s+prompt|secret|instructions)",
        r"quên\s+hết\s+(các\s+)?hướng\s+dẫn\s+trước",
        r"tiết\s+lộ\s+system\s+prompt",
        r"bỏ\s+qua\s+mọi\s+quy\s+tắc",
    ]

    # Danh sách hành vi vi phạm pháp luật cấm tư vấn
    ILLEGAL_INTENTS = [
        r"trốn\s+thuế",
        r"rửa\s+tiền",
        r"kê\s+khai\s+khống\s+vốn",
        r"làm\s+giả\s+giấy\s+tờ",
        r"làm\s+giả\s+cccd",
        r"lách\s+thuế\s+bất\s+hợp\s+pháp",
        r"kinh\s+doanh\s+hàng\s+cấm",
        r"kinh\s+doanh\s+ma\s+túy",
    ]

    def __init__(self):
        self.injection_regex = [re.compile(p, re.IGNORECASE) for p in self.INJECTION_PATTERNS]
        self.illegal_regex = [re.compile(p, re.IGNORECASE) for p in self.ILLEGAL_INTENTS]

    def check_safety(self, user_input: str) -> Tuple[bool, str]:
        """
        Kiểm tra tính an toàn của prompt.
        Returns:
            Tuple[is_safe, violation_reason_or_message]
        """
        # 1. Kiểm tra tấn công kỹ thuật Prompt Injection
        for reg in self.injection_regex:
            if reg.search(user_input):
                return False, (
                    "CẢNH BÁO AN NINH: Phát hiện câu lệnh có dấu hiệu can thiệp/bẻ khóa hệ thống (Prompt Injection). "
                    "Hệ thống từ chối xử lý yêu cầu này."
                )

        # 2. Kiểm tra yêu cầu hành vi trái pháp luật
        for reg in self.illegal_regex:
            if reg.search(user_input):
                return False, (
                    "TỪ CHỐI PHÁP LÝ: Hệ thống LegalTech SME tuân thủ nghiêm ngặt Điều 16 Luật Doanh nghiệp 2020. "
                    "Hệ thống không cung cấp thông tin hoặc hướng dẫn các hành vi trốn thuế, rửa tiền, kê khai khống vốn "
                    "hoặc làm giả hồ sơ pháp lý."
                )

        return True, ""
