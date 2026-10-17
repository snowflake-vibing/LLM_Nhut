"""
Dynamic Memory & Few-Shot Store Module
Quản lý cơ chế 'Học liên tục không cần đổi trọng số' (Continual Learning without Weight Training).
Lưu trữ các mẫu thẩm định hợp đồng thành công, án lệ tham chiếu và phản hồi hữu ích của người dùng.
"""

import os
import json
from typing import List, Dict, Any, Optional

DEFAULT_MEMORY_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "data", "database", "legal_memory_bank.json"
)

# Tập dữ liệu Few-shot ban đầu về thẩm định hợp đồng & soạn thảo chuẩn
SEED_MEMORY_CASES = [
    {
        "id": "case_penalty_cap",
        "category": "commercial_contract",
        "title": "Xử lý mức phạt vi phạm vượt trần trong hợp đồng mua bán thương mại",
        "user_query": "hợp đồng phạt vi phạm 12% có hợp pháp không",
        "key_risk": "Vi phạm Điều 301 Luật Thương mại 2005 (trần 8%)",
        "golden_solution": (
            "Điều khoản phạt 12% vi phạm điều cấm của Luật Thương mại 2005 (Điều 301). "
            "Giải pháp tối ưu: Tách riêng mức Phạt vi phạm = 8% và Bồi thường toàn bộ thiệt hại thực tế phát sinh (Điều 302)."
        ),
        "legal_basis": "Điều 301, 302 Luật Thương mại 2005"
    },
    {
        "id": "case_probation_period",
        "category": "labor_contract",
        "title": "Thẩm định thời gian thử việc vị trí chuyên viên kỹ thuật",
        "user_query": "công ty cho thử việc 3 tháng vị trí kỹ sư phần mềm",
        "key_risk": "Vi phạm Khoản 2 Điều 25 Bộ luật Lao động 2019 (tối đa 60 ngày)",
        "golden_solution": (
            "Vị trí kỹ sư/chuyên môn cao đẳng trở lên chỉ được thử việc tối đa 60 ngày. "
            "Thỏa thuận 3 tháng (90 ngày) là trái luật. Cần yêu cầu điều chỉnh lại 60 ngày và nhận lương ít nhất 85%."
        ),
        "legal_basis": "Điều 25, 26 Bộ luật Lao động 2019"
    },
    {
        "id": "case_nda_trade_secret",
        "category": "ip_and_nda",
        "title": "Thỏa thuận bảo mật thông tin và không cạnh tranh (NDA / Non-compete)",
        "user_query": "thỏa thuận cấm nhân viên làm cho đối thủ sau nghỉ việc",
        "key_risk": "Xung đột quyền tự do việc làm theo Điều 35 Hiến pháp và Điều 5 BLLĐ",
        "golden_solution": (
            "Không được cấm quyền làm việc chung chung. Chỉ được bảo vệ bí mật kinh doanh, bí mật công nghệ "
            "theo Khoản 2 Điều 21 BLLĐ 2019 kèm khoản tiền đền bù/hỗ trợ bảo mật tương xứng."
        ),
        "legal_basis": "Khoản 2 Điều 21 Bộ luật Lao động 2019 & Luật Sở hữu trí tuệ"
    }
]


class LegalMemoryStore:
    """
    Kho lưu trữ tri thức động phục vụ Dynamic In-Context Learning.
    """

    def __init__(self, memory_path: str = None):
        self.memory_path = memory_path or DEFAULT_MEMORY_PATH
        self._load()

    def _load(self):
        if os.path.exists(self.memory_path):
            try:
                with open(self.memory_path, "r", encoding="utf-8") as f:
                    self.cases = json.load(f)
                    return
            except Exception:
                pass
        self.cases = list(SEED_MEMORY_CASES)
        self._save()

    def _save(self):
        os.makedirs(os.path.dirname(self.memory_path), exist_ok=True)
        with open(self.memory_path, "w", encoding="utf-8") as f:
            json.dump(self.cases, f, ensure_ascii=False, indent=2)

    def retrieve_similar_cases(self, query: str, limit: int = 2) -> List[Dict[str, Any]]:
        """
        Tìm kiếm các tình huống thẩm định tương đồng trong Memory Bank để nạp vào prompt.
        """
        q_lower = query.lower()
        scored = []
        for c in self.cases:
            score = 0
            for word in q_lower.split():
                if len(word) >= 3 and (word in c["user_query"].lower() or word in c["title"].lower()):
                    score += 1
            if score > 0:
                scored.append((score, c))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scored[:limit]]

    def record_feedback(self, title: str, user_query: str, golden_solution: str, legal_basis: str):
        """
        Ghi nhận một tình huống giải quyết xuất sắc vào Memory Store.
        """
        new_case = {
            "id": f"case_user_{len(self.cases) + 1}",
            "category": "user_contributed",
            "title": title,
            "user_query": user_query,
            "key_risk": "Tình huống thực tế đã được kiểm chứng",
            "golden_solution": golden_solution,
            "legal_basis": legal_basis
        }
        self.cases.append(new_case)
        self._save()
