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
from src.tools.social_cases_knowledge import SocialCasesKnowledgeEngine


class RouterAgent:
    """
    Agent phân loại và điều phối ý định người dùng (Legal Intent Router - v2.1).
    """

    def __init__(self, factory: ModelFactory = None):
        self.factory = factory or ModelFactory()

    def route(self, query: str) -> Dict[str, Any]:
        """
        Phân tích câu hỏi và trả về intent.
        Intents hỗ trợ:
        - SOCIAL_CASE_ADVISORY: 4 case xã hội phức tạp (Bạo lực học đường, Đất đai, Đòi nợ, Ly hôn).
        - DYNAMIC_DRAFT: Soạn thảo văn bản pháp lý đa dạng với Form thông minh & Placeholder linh hoạt.
        - CONTRACT_AUDIT: Thẩm định hợp đồng, phát hiện lỗ hổng, rà soát điều khoản rủi ro.
        - DOSSIER_CREATION: Soạn thảo hồ sơ đăng ký doanh nghiệp.
        - INDUSTRY_LOOKUP: Tra cứu mã ngành kinh tế VSIC, điều kiện giấy phép con.
        - REGISTRATION_STEPS: Lộ trình thủ tục, checklist hành động từng bước.
        - ENTITY_ADVISORY: Tư vấn lựa chọn loại hình tổ chức (Hộ kinh doanh, TNHH, Cổ phần).
        """
        q_lower = query.lower()

        # 1. Kiểm tra 4 Case Xã hội Cốt lõi
        matched_case = SocialCasesKnowledgeEngine.match_case(query)
        if matched_case:
            # Nếu người dùng muốn trực tiếp soạn thảo đơn từ của case đó
            if any(k in q_lower for k in ["soạn", "tạo đơn", "viết đơn", "mẫu đơn", "tải đơn", "in đơn"]):
                return {"intent": "DYNAMIC_DRAFT", "case_id": matched_case}
            return {"intent": "SOCIAL_CASE_ADVISORY", "case_id": matched_case}

        # 2. Kiểm tra Ý định Soạn thảo Văn bản Linh hoạt
        if any(k in q_lower for k in [
            "soạn đơn", "mẫu đơn", "viết hợp đồng", "tạo văn bản", "soạn hợp đồng",
            "đơn ly hôn", "đơn khởi kiện", "đơn tố cáo", "đơn khiếu nại", "đơn hòa giải"
        ]):
            return {"intent": "DYNAMIC_DRAFT"}

        # 3. Phân loại bằng LLM
        prompt = (
            f"{FEW_SHOT_ROUTER_EXAMPLES}\n\n"
            f"Bây giờ hãy phân loại yêu cầu của người dùng:\n"
            f"Người dùng: \"{query}\"\n"
            f"Trả về kết quả JSON với format: {{\"intent\": \"CONTRACT_AUDIT\" | \"DOSSIER_CREATION\" | \"DYNAMIC_DRAFT\" | \"ENTITY_ADVISORY\" | \"INDUSTRY_LOOKUP\" | \"REGISTRATION_STEPS\"}}"
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
            if "DYNAMIC" in raw_clean or "DRAFT" in raw_clean:
                return {"intent": "DYNAMIC_DRAFT"}
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
        if any(k in q_lower for k in ["hợp đồng", "thẩm định", "lỗ hổng", "quét rủi ro", "phạt vi phạm", "thử việc", "đơn phương chấm dứt", "bất khả kháng"]):
            return {"intent": "CONTRACT_AUDIT"}
        if any(k in q_lower for k in ["tạo hồ sơ", "soạn hồ sơ", "làm giấy đề nghị", "viết điều lệ"]):
            return {"intent": "DOSSIER_CREATION"}
        if any(k in q_lower for k in ["mã ngành", "giấy phép con", "atvstp", "pccc", "ngành nghề", "vsic"]):
            return {"intent": "INDUSTRY_LOOKUP"}
        if any(k in q_lower for k in ["thủ tục", "các bước", "nộp ở đâu", "bao lâu", "checklist"]):
            return {"intent": "REGISTRATION_STEPS"}
        return {"intent": "ENTITY_ADVISORY"}
