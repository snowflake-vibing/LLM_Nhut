"""
SQL Tools Module
Cung cấp các Tool Calling functions cho AI Agent tra cứu CSDL pháp lý doanh nghiệp.
"""

import json
from typing import List, Dict, Any
from .db_manager import DatabaseManager


_db_manager = DatabaseManager()


def search_industry_tool(keyword: str) -> str:
    """
    Công cụ tra cứu mã ngành kinh tế Việt Nam (VSIC 2018).
    Sử dụng khi người dùng hỏi về mở quán, làm phần mềm, bán hàng online, kinh doanh ngành gì...
    Args:
        keyword: Từ khóa ngành nghề (Ví dụ: 'cà phê', 'phần mềm', 'bán lẻ', 'vận tải'...).
    Returns:
        JSON string chứa danh sách mã ngành và điều kiện kinh doanh.
    """
    results = _db_manager.search_industry(keyword)
    if not results:
        return f"Không tìm thấy mã ngành kinh tế nào khớp với từ khóa '{keyword}'."
    return json.dumps(results, ensure_ascii=False, indent=2)


def get_sub_license_tool(keyword: str) -> str:
    """
    Công cụ tra cứu giấy phép con (điều kiện an toàn thực phẩm, PCCC, giấy phép rượu...).
    Args:
        keyword: Tên giấy phép hoặc ngành nghề liên quan (Ví dụ: 'thực phẩm', 'PCCC', 'rượu'...).
    Returns:
        JSON string chứa cơ quan cấp, thời gian xử lý, lệ phí và hồ sơ yêu cầu.
    """
    results = _db_manager.get_license_info(keyword)
    if not results:
        return f"Không tìm thấy thông tin giấy phép con khớp với từ khóa '{keyword}'."
    return json.dumps(results, ensure_ascii=False, indent=2)


def get_registration_steps_tool(entity_type: str) -> str:
    """
    Công cụ lấy quy trình từng bước đăng ký thủ tục kinh doanh.
    Args:
        entity_type: Một trong các giá trị: 'HO_KINH_DOANH', 'TNHH_1TV', 'CO_PHAN'.
    Returns:
        JSON string chứa các bước, cơ quan tiếp nhận và văn bản đầu ra.
    """
    norm_type = entity_type.upper().strip()
    if "HỘ" in norm_type or "HO" in norm_type:
        code = "HO_KINH_DOANH"
    elif "CỔ PHẦN" in norm_type or "CO_PHAN" in norm_type or "JSC" in norm_type:
        code = "CO_PHAN"
    else:
        code = "TNHH_1TV"

    results = _db_manager.get_checklist(code)
    if not results:
        return f"Không tìm thấy quy trình cho loại hình '{entity_type}'."
    return json.dumps(results, ensure_ascii=False, indent=2)


def query_legal_database_tool(sql_query: str) -> str:
    """
    Công cụ chạy câu truy vấn SQL SELECT tùy biến trên cơ sở dữ liệu pháp lý SME.
    Chỉ dùng khi cần tổng hợp hoặc lọc dữ liệu nâng cao.
    Args:
        sql_query: Câu lệnh SQL bắt đầu bằng SELECT.
    """
    try:
        results = _db_manager.execute_safe_sql(sql_query)
        return json.dumps(results, ensure_ascii=False, indent=2)
    except Exception as e:
        return f"Lỗi thực thi SQL: {str(e)}"
