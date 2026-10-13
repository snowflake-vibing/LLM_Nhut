"""
Industry Lookup Agent Module
Chuyên trách tra cứu mã ngành kinh tế VSIC và điều kiện cấp phép con bằng CSDL SQL.
"""

import sys
import os
import json
from typing import Dict, Any

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from llm_provider.model_factory import ModelFactory
from src.prompts import INDUSTRY_LOOKUP_SYSTEM_PROMPT
from src.database import search_industry_tool, get_sub_license_tool


class IndustryLookupAgent:
    """
    Agent tra cứu mã ngành kinh tế (VSIC 2018) và các điều kiện cấp phép chuyên ngành.
    """

    def __init__(self, factory: ModelFactory = None):
        self.factory = factory or ModelFactory()

    def lookup(self, user_query: str) -> Dict[str, Any]:
        """
        Tìm kiếm CSDL và tổng hợp giải đáp cho người dùng.
        """
        # Trích xuất từ khóa tìm kiếm
        keywords = ["cà phê", "đồ uống", "ăn uống", "phần mềm", "bán lẻ", "mỹ phẩm", "bất động sản", "vận tải", "giáo dục"]
        matched_kw = "phần mềm"
        for kw in keywords:
            if kw in user_query.lower():
                matched_kw = kw
                break

        # Gọi CSDL SQL
        industry_data = search_industry_tool(matched_kw)
        license_data = get_sub_license_tool(matched_kw)

        prompt = (
            f"Người dùng hỏi: \"{user_query}\"\n\n"
            f"DỮ LIỆU TỪ CƠ SỞ DỮ LIỆU MÃ NGÀNH VSIC 2018:\n{industry_data}\n\n"
            f"DỮ LIỆU ĐIỀU KIỆN GIẤY PHÉP CON:\n{license_data}\n\n"
            f"Hãy giải thích rõ ràng cho người dùng: Các mã ngành phù hợp cần đăng ký, "
            f"ngành này có điều kiện hay không, và cần chuẩn bị những giấy phép con nào trước khi hoạt động."
        )

        try:
            response = self.factory.generate(
                prompt=prompt,
                system_prompt=INDUSTRY_LOOKUP_SYSTEM_PROMPT
            )
        except Exception:
            response = (
                f"### Kết quả tra cứu mã ngành kinh tế và giấy phép con:\n"
                f"Dựa trên dữ liệu hệ thống ngành kinh tế Việt Nam (VSIC):\n\n"
                f"```json\n{industry_data}\n```\n\n"
                f"**Điều kiện cấp phép chuyên ngành:**\n"
                f"```json\n{license_data}\n```\n"
            )

        return {
            "response": response,
            "raw_industry_data": industry_data,
            "raw_license_data": license_data,
            "agent": "IndustryLookupAgent",
        }
