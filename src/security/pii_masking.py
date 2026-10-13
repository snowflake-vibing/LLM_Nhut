"""
PII Masking Module
Bảo vệ dữ liệu nhạy cảm của người dùng (CCCD/CMND, Số điện thoại, Email, Địa chỉ)
bằng kỹ thuật Masking & Pseudonymization trước khi gửi yêu cầu qua Cloud API.
"""

import re
from typing import Tuple, Dict


class PIIMasker:
    """
    Nhận diện và mã hóa/che giấu thông tin định danh cá nhân (Personally Identifiable Information).
    """

    def __init__(self):
        # Regex cho CCCD Việt Nam (12 số) hoặc CMND cũ (9 số)
        self.cccd_pattern = re.compile(r"\b(?:\d{12}|\d{9})\b")
        # Regex cho số điện thoại di động VN
        self.phone_pattern = re.compile(r"\b(?:0|84|\+84)(?:3|5|7|8|9)\d{8}\b")
        # Regex cho email
        self.email_pattern = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")

    def mask_text(self, text: str) -> Tuple[str, Dict[str, str]]:
        """
        Che dấu các thông tin PII và lưu lại bảng ánh xạ mapping để có thể unmask nếu cần.
        """
        mapping = {}
        masked = text

        # 1. Mask CCCD
        cccd_matches = self.cccd_pattern.findall(masked)
        for i, match in enumerate(set(cccd_matches)):
            placeholder = f"[MASKED_CCCD_{i+1}]"
            mapping[placeholder] = match
            masked = masked.replace(match, placeholder)

        # 2. Mask Phone
        phone_matches = self.phone_pattern.findall(masked)
        for i, match in enumerate(set(phone_matches)):
            placeholder = f"[MASKED_PHONE_{i+1}]"
            mapping[placeholder] = match
            masked = masked.replace(match, placeholder)

        # 3. Mask Email
        email_matches = self.email_pattern.findall(masked)
        for i, match in enumerate(set(email_matches)):
            placeholder = f"[MASKED_EMAIL_{i+1}]"
            mapping[placeholder] = match
            masked = masked.replace(match, placeholder)

        return masked, mapping

    def unmask_text(self, text: str, mapping: Dict[str, str]) -> str:
        """Khôi phục lại thông tin gốc từ chuỗi đã che dấu."""
        unmasked = text
        for placeholder, original in mapping.items():
            unmasked = unmasked.replace(placeholder, original)
        return unmasked
