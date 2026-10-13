"""
Entity Advisory Agent Module
Tư vấn lựa chọn mô hình tổ chức doanh nghiệp tối ưu kết hợp tri thức RAG Luật Doanh nghiệp 2020.
"""

import sys
import os
from typing import Dict, Any, List

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from llm_provider.model_factory import ModelFactory
from src.prompts import ADVISORY_SYSTEM_PROMPT, COT_REASONING_PROMPT
from src.rag import LegalRetriever


class EntityAdvisoryAgent:
    """
    Agent tư vấn loại hình doanh nghiệp (Hộ kinh doanh, TNHH 1TV, TNHH 2TV+, Cổ phần).
    """

    def __init__(self, factory: ModelFactory = None, retriever: LegalRetriever = None):
        self.factory = factory or ModelFactory()
        self.retriever = retriever or LegalRetriever()

    def advise(self, user_query: str) -> Dict[str, Any]:
        """
        Thực hiện tư vấn có trích xuất căn cứ pháp luật và suy luận CoT.
        """
        # 1. RAG Retrieval
        context, citations = self.retriever.format_context_with_citations(user_query, top_k=3)

        # 2. Xây dựng prompt có Chain-of-Thought
        full_prompt = (
            f"{COT_REASONING_PROMPT}\n\n"
            f"=== CĂN CỨ VĂN BẢN QUY PHẠM PHÁP LUẬT ĐƯỢC TRÍCH XUẤT ===\n"
            f"{context}\n\n"
            f"=== YÊU CẦU CỦA NGƯỜI DÙNG ===\n"
            f"\"{user_query}\"\n\n"
            f"Hãy đưa ra phân tích chi tiết, so sánh các phương án và đề xuất giải pháp tối ưu nhất cho người dùng. "
            f"Luôn ghi rõ căn cứ trích dẫn ở cuối câu trả lời."
        )

        try:
            response = self.factory.generate(
                prompt=full_prompt,
                system_prompt=ADVISORY_SYSTEM_PROMPT
            )
        except Exception as e:
            response = (
                f"### Tư vấn loại hình doanh nghiệp:\n"
                f"Dựa trên yêu cầu của bạn, nếu bạn khởi nghiệp với quy mô vừa và nhỏ:\n"
                f"- **Công ty TNHH 1 Thành viên:** Phù hợp nếu bạn làm chủ một mình, bảo toàn tài sản cá nhân nhờ chế độ trách nhiệm hữu hạn trong phạm vi vốn góp [Luật Doanh nghiệp 2020 - Điều 74].\n"
                f"- **Hộ kinh doanh cá thể:** Thủ tục kế toán đơn giản, phù hợp kinh doanh địa điểm cố định nhưng chịu trách nhiệm vô hạn bằng toàn bộ tài sản [Nghị định 01/2021/NĐ-CP - Điều 79].\n\n"
                f"*(Lưu ý: Mô hình đang chạy ở chế độ offline fallback)*"
            )

        return {
            "response": response,
            "citations": citations,
            "agent": "EntityAdvisoryAgent",
        }
