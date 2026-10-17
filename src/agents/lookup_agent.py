"""
Industry Lookup Agent Module
Chuyên trách tra cứu mã ngành kinh tế VSIC và điều kiện cấp phép con bằng CSDL SQL
kết hợp Web Search Tool (Kiến trúc Hybrid Retrieval).
"""

import sys
import os
import json
import re
from typing import Dict, Any, List

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from llm_provider.model_factory import ModelFactory
from src.prompts import INDUSTRY_LOOKUP_SYSTEM_PROMPT
from src.database import search_industry_tool, get_sub_license_tool
from src.tools.web_search_tool import search_web_legal


class IndustryLookupAgent:
    """
    Agent tra cứu mã ngành kinh tế (VSIC 2018) và các điều kiện cấp phép chuyên ngành.
    Hỗ trợ kiến trúc Hybrid: Ưu tiên SQLite nội bộ, tự động kích hoạt Web Search Tool khi cần.
    """

    def __init__(self, factory: ModelFactory = None):
        self.factory = factory or ModelFactory()

    def _extract_keyword(self, user_query: str) -> str:
        """Trích xuất từ khóa ngành nghề từ truy vấn người dùng."""
        # Danh mục từ khóa phổ biến và mới
        candidate_keywords = [
            "thương mại điện tử", "livestream", "trí tuệ nhân tạo", "logistics",
            "năng lượng mặt trời", "game online", "cà phê", "đồ uống", "ăn uống",
            "nhà hàng", "quán ăn", "phần mềm", "bán lẻ", "mỹ phẩm", "bất động sản",
            "vận tải", "giáo dục", "du lịch", "dược phẩm", "xây dựng", "thời trang"
        ]
        q_lower = user_query.lower()
        for kw in candidate_keywords:
            if kw in q_lower:
                return kw

        # Nếu không trúng danh mục trên, tách cụm từ chính
        cleaned = re.sub(r"(tôi muốn|mở|kinh doanh|thành lập|công ty|ngành|nghề|tra cứu|hỏi về|tư vấn)", "", q_lower).strip()
        words = cleaned.split()
        if len(words) >= 2:
            return " ".join(words[:3])
        elif len(words) == 1:
            return words[0]
        return "phần mềm"

    def lookup(self, user_query: str) -> Dict[str, Any]:
        """
        Tìm kiếm CSDL SQL và Web Search mở rộng, sau đó tổng hợp giải đáp cho người dùng.
        """
        matched_kw = self._extract_keyword(user_query)

        # 1. Gọi CSDL SQL nội bộ
        industry_data = search_industry_tool(matched_kw)
        license_data = get_sub_license_tool(matched_kw)

        citations = []
        web_search_used = False
        web_info_text = ""

        # Kiểm tra nếu SQLite không có dữ liệu
        no_db_industry = "Không tìm thấy" in industry_data
        no_db_license = "Không tìm thấy" in license_data

        if no_db_industry:
            # 2. Kích hoạt Web Search Tool
            web_search_used = True
            web_results = search_web_legal(matched_kw, max_results=3)
            if web_results:
                web_parts = []
                for hit in web_results:
                    web_parts.append(f"- Tiêu đề: {hit['title']}\n  Nội dung: {hit['snippet']}\n  Nguồn: {hit['url']}")
                    citations.append({
                        "law_title": hit.get("title", "Tra cứu ngành nghề mở rộng"),
                        "article": hit.get("source", "Web Search / Cổng TT Chính phủ"),
                        "header": hit.get("title", ""),
                        "verify_url": hit.get("url", "https://vanban.chinhphu.vn/"),
                        "text_snippet": hit.get("snippet", "")[:200],
                        "full_text": hit.get("snippet", "")
                    })
                web_info_text = "\n\n=== DỮ LIỆU TÌM KIẾM TỪ INTERNET & CỔNG TT CHÍNH PHỦ (WEB SEARCH TOOL) ===\n" + "\n".join(web_parts)
        else:
            # Gán citation từ SQLite nếu có
            try:
                raw_inds = json.loads(industry_data)
                for ind in raw_inds[:2]:
                    citations.append({
                        "law_title": "Hệ thống ngành kinh tế Việt Nam (VSIC 2018)",
                        "article": f"Mã ngành {ind.get('code')}",
                        "header": ind.get("name", ""),
                        "verify_url": "https://vanban.chinhphu.vn/?pageid=27160&docid=193188",
                        "text_snippet": f"Ngành nghề: {ind.get('name')}. Điều kiện: {ind.get('license_required', 'Không có')}",
                        "full_text": ind.get("description", "")
                    })
            except Exception:
                pass

        prompt = (
            f"Người dùng hỏi: \"{user_query}\"\n\n"
            f"DỮ LIỆU TỪ CƠ SỞ DỮ LIỆU MÃ NGÀNH VSIC 2018 (SQL DB):\n{industry_data}\n\n"
            f"DỮ LIỆU ĐIỀU KIỆN GIẤY PHÉP CON (SQL DB):\n{license_data}"
            f"{web_info_text}\n\n"
            f"Hãy giải thích rõ ràng cho người dùng:\n"
            f"1. Các mã ngành kinh tế phù hợp cần đăng ký (mã số và tên gọi chuẩn).\n"
            f"2. Ngành này có thuộc danh mục kinh doanh có điều kiện hay không.\n"
            f"3. Cần chuẩn bị những giấy phép con (sub-licenses) hoặc thủ tục chuyên ngành nào trước khi hoạt động.\n"
            f"4. Nếu có kết quả tra cứu mở rộng từ Web Search, hãy nêu rõ nguồn và link kiểm chứng."
        )

        try:
            response = self.factory.generate(
                prompt=prompt,
                system_prompt=INDUSTRY_LOOKUP_SYSTEM_PROMPT
            )
        except Exception:
            response = (
                f"### Kết quả tra cứu mã ngành kinh tế và giấy phép con:\n"
                f"Dựa trên dữ liệu hệ thống ngành kinh tế Việt Nam (VSIC) và tìm kiếm thông tin:\n\n"
                f"- **Mã ngành:** `{industry_data}`\n"
                f"- **Giấy phép con:** `{license_data}`\n"
            )
            if web_search_used:
                response += f"\n*(Đã tự động kích hoạt Web Search Tool do từ khóa '{matched_kw}' chưa có trong CSDL cục bộ)*"

        return {
            "response": response,
            "raw_industry_data": industry_data,
            "raw_license_data": license_data,
            "citations": citations,
            "web_search_used": web_search_used,
            "agent": "IndustryLookupAgent",
        }
