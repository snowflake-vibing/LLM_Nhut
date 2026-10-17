"""
Document Reviewer & Checklist Agent Module
Tổng hợp lộ trình pháp lý từng bước và danh mục hồ sơ cần nộp.
"""

import sys
import os
from typing import Dict, Any

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from llm_provider.model_factory import ModelFactory
from src.prompts import CHECKLIST_REVIEWER_SYSTEM_PROMPT
from src.database import get_registration_steps_tool


class DocumentReviewerAgent:
    """
    Agent rà soát và thiết lập checklist hoàn thiện hồ sơ cho người dùng.
    """

    def __init__(self, factory: ModelFactory = None):
        self.factory = factory or ModelFactory()

    def generate_checklist(self, user_query: str, entity_type: str = "TNHH_1TV") -> Dict[str, Any]:
        """
        Sinh bản lộ trình thủ tục chi tiết kèm checklist hành động.
        """
        steps_data = get_registration_steps_tool(entity_type)

        prompt = (
            f"Yêu cầu của người dùng: \"{user_query}\"\n"
            f"Loại hình doanh nghiệp: {entity_type}\n\n"
            f"DỮ LIỆU CÁC BƯỚC ĐĂNG KÝ TỪ CƠ SỞ DỮ LIỆU:\n{steps_data}\n\n"
            f"Hãy xây dựng một Bản Kế hoạch & Checklist Hành động (Actionable Checklist) "
            f"với các bước [ ] rõ ràng, ghi rõ cơ quan tiếp nhận hồ sơ, thời gian xử lý và văn bản nhận được."
        )

        try:
            response = self.factory.generate(
                prompt=prompt,
                system_prompt=CHECKLIST_REVIEWER_SYSTEM_PROMPT
            )
        except Exception:
            response = (
                f"### Lộ trình & Checklist Thủ tục Đăng ký ({entity_type}):\n"
                f"- [ ] **Bước 1: Chuẩn bị thông tin:** Tên công ty, trụ sở chính, vốn điều lệ và bản sao CCCD.\n"
                f"- [ ] **Bước 2: Nộp hồ sơ:** Nộp online qua Cổng dangkykinhdoanh.gov.vn hoặc Bộ phận Một cửa UBND.\n"
                f"- [ ] **Bước 3: Nhận Giấy chứng nhận Đăng ký Doanh nghiệp:** Trong 03 ngày làm việc.\n"
                f"- [ ] **Bước 4: Sau thành lập:** Khắc dấu pháp nhân, mở tài khoản ngân hàng, mua chữ ký số kê khai thuế môn bài.\n"
                f"- [ ] **Bước 5: Hoàn tất góp vốn:** Đảm bảo góp đủ 100% vốn cam kết trong vòng 90 ngày [Điều 47 Luật Doanh nghiệp 2020].\n"
            )

        citations = [
            {
                "law_title": "Nghị định 01/2021/NĐ-CP về đăng ký doanh nghiệp",
                "article": "Điều 23, 24",
                "header": "Hồ sơ, trình tự, thủ tục đăng ký doanh nghiệp",
                "verify_url": "https://vanban.chinhphu.vn/?pageid=27160&docid=202613",
                "text_snippet": "Quy định chi tiết về hồ sơ đăng ký doanh nghiệp, tiếp nhận và giải quyết hồ sơ qua Cổng thông tin quốc gia.",
                "full_text": "Nghị định số 01/2021/NĐ-CP quy định chi tiết về hồ sơ, trình tự, thủ tục đăng ký doanh nghiệp, đăng ký hộ kinh doanh..."
            },
            {
                "law_title": "Luật Doanh nghiệp 2020",
                "article": "Điều 47, 75",
                "header": "Thời hạn góp vốn thành lập công ty (90 ngày)",
                "verify_url": "https://vanban.chinhphu.vn/?pageid=27160&docid=200676",
                "text_snippet": "Chủ sở hữu, thành viên phải góp vốn cho công ty đủ và đúng loại tài sản đã cam kết khi đăng ký thành lập doanh nghiệp trong thời hạn 90 ngày.",
                "full_text": "Điều 47, 75 Luật Doanh nghiệp 2020: Thành viên phải góp vốn phần vốn góp cho công ty đủ và đúng loại tài sản đã cam kết trong thời hạn 90 ngày kể từ ngày được cấp Giấy chứng nhận đăng ký doanh nghiệp."
            }
        ]

        return {
            "response": response,
            "entity_type": entity_type,
            "raw_steps": steps_data,
            "citations": citations,
            "agent": "DocumentReviewerAgent",
        }
