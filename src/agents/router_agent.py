"""
Router Agent Module
Phân loại ý định của người dùng để điều hướng tới Agent chuyên trách thích hợp.
"""

import sys
import os
import json
from typing import Dict, Any

# Hỗ trợ tìm kiếm package ở thư mục gốc
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from llm_provider.model_factory import ModelFactory
from src.prompts import ROUTER_SYSTEM_PROMPT, FEW_SHOT_ROUTER_EXAMPLES


class RouterAgent:
    """
    Agent phân loại và điều phối ý định người dùng (Legal Intent Router).
    """

    def __init__(self, factory: ModelFactory = None):
        self.factory = factory or ModelFactory()

    def route(self, query: str) -> Dict[str, Any]:
        """
        Phân tích câu hỏi và trả về intent.
        """
        prompt = (
            f"{FEW_SHOT_ROUTER_EXAMPLES}\n\n"
            f"Bây giờ hãy phân loại câu hỏi của người dùng:\n"
            f"Người dùng: \"{query}\"\n"
            f"Trả về kết quả JSON với format: {{\"intent\": \"ENTITY_ADVISORY\" | \"INDUSTRY_LOOKUP\" | \"REGISTRATION_STEPS\" | \"GENERAL_LEGAL_QA\"}}"
        )

        try:
            raw_response = self.factory.generate(
                prompt=prompt,
                system_prompt=ROUTER_SYSTEM_PROMPT
            )
            # Trích xuất JSON từ phản hồi
            raw_clean = raw_response.strip()
            if "{" in raw_clean and "}" in raw_clean:
                start = raw_clean.find("{")
                end = raw_clean.rfind("}") + 1
                return json.loads(raw_clean[start:end])
            if "INDUSTRY" in raw_clean:
                return {"intent": "INDUSTRY_LOOKUP"}
            if "STEPS" in raw_clean or "REGISTRATION" in raw_clean:
                return {"intent": "REGISTRATION_STEPS"}
            return {"intent": "ENTITY_ADVISORY"}
        except Exception:
            # Quy tắc heuristics dự phòng nếu không gọi được LLM
            q_lower = query.lower()
            if any(k in q_lower for k in ["mã ngành", "giấy phép con", "atvstp", "pccc", "ngành nghề"]):
                return {"intent": "INDUSTRY_LOOKUP"}
            if any(k in q_lower for k in ["thủ tục", "các bước", "hồ sơ", "nộp ở đâu", "bao lâu"]):
                return {"intent": "REGISTRATION_STEPS"}
            return {"intent": "ENTITY_ADVISORY"}
