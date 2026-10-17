"""
Router Agent Module
Phân loại ý định của người dùng để điều hướng tới Agent chuyên trách thích hợp
bao gồm Thẩm định Hợp đồng, Soạn thảo Hồ sơ và Tra cứu Pháp luật (Version 2.0).
"""

import sys
import os
import json
from typing import Dict, Any

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from llm_provider.model_factory import ModelFactory
from src.prompts import ROUTER_SYSTEM_PROMPT, FEW_SHOT_ROUTER_EXAMPLES


class RouterAgent:
    """
    Agent phân loại và điều phối ý định người dùng (Legal Intent Router - v2.0).
    """

    def __init__(self, factory: ModelFactory = None):
        self.factory = factory or ModelFactory()

    def route(self, query: str) -> Dict[str, Any]:
        """
        Phân tích câu hỏi và trả về intent.
        Intents hỗ trợ:
        - CONTRACT_AUDIT: Thẩm định hợp đồng, phát hiện lỗ hổng, rà soát điều khoản rủi ro.
        - DOSSIER_CREATION: Soạn thảo hồ sơ đăng ký doanh nghiệp, điều lệ, giấy đề nghị.
        - INDUSTRY_LOOKUP: Tra cứu mã ngành kinh tế VSIC, điều kiện giấy phép con.
        - REGISTRATION_STEPS: Lộ trình thủ tục, checklist hành động từng bước.
        - ENTITY_ADVISORY: Tư vấn lựa chọn loại hình tổ chức (Hộ kinh doanh, TNHH, Cổ phần).
        """
        prompt = (
            f"{FEW_SHOT_ROUTER_EXAMPLES}\n\n"
            f"Bây giờ hãy phân loại yêu cầu của người dùng:\n"
            f"Người dùng: \"{query}\"\n"
            f"Trả về kết quả JSON với format: {{\"intent\": \"CONTRACT_AUDIT\" | \"DOSSIER_CREATION\" | \"ENTITY_ADVISORY\" | \"INDUSTRY_LOOKUP\" | \"REGISTRATION_STEPS\"}}"
        )

        try:
            raw_response = self.factory.generate(
                prompt=prompt,
                system_prompt=ROUTER_SYSTEM_PROMPT
            )
            raw_clean = raw_response.strip()
            if "{" in raw_clean and "}" in raw_clean:
                start = raw_clean.find("{")
                end = raw_clean.rfind("}") + 1
                parsed = json.loads(raw_clean[start:end])
                if "intent" in parsed:
                    return parsed

            if "CONTRACT" in raw_clean or "AUDIT" in raw_clean:
                return {"intent": "CONTRACT_AUDIT"}
            if "DOSSIER" in raw_clean:
                return {"intent": "DOSSIER_CREATION"}
            if "INDUSTRY" in raw_clean:
                return {"intent": "INDUSTRY_LOOKUP"}
            if "STEPS" in raw_clean or "REGISTRATION" in raw_clean:
                return {"intent": "REGISTRATION_STEPS"}
            return {"intent": "ENTITY_ADVISORY"}
        except Exception:
            pass

        # Heuristics dự phòng
        q_lower = query.lower()
        if any(k in q_lower for k in ["hợp đồng", "thẩm định", "lỗ hổng", "quét rủi ro", "phạt vi phạm", "thử việc", "đơn phương chấm dứt", "bất khả kháng"]):
            return {"intent": "CONTRACT_AUDIT"}
        if any(k in q_lower for k in ["tạo hồ sơ", "soạn hồ sơ", "làm giấy đề nghị", "viết điều lệ", "mẫu đơn"]):
            return {"intent": "DOSSIER_CREATION"}
        if any(k in q_lower for k in ["mã ngành", "giấy phép con", "atvstp", "pccc", "ngành nghề", "vsic"]):
            return {"intent": "INDUSTRY_LOOKUP"}
        if any(k in q_lower for k in ["thủ tục", "các bước", "nộp ở đâu", "bao lâu", "checklist"]):
            return {"intent": "REGISTRATION_STEPS"}
        return {"intent": "ENTITY_ADVISORY"}
