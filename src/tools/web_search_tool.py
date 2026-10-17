"""
Web Search Tool Module
Cung cấp khả năng tìm kiếm mở rộng trên Internet cho các ngành nghề mới,
công nghệ cao hoặc chưa có trong CSDL nội bộ SQLite (Kiến trúc Hybrid Search).
"""

import json
from typing import List, Dict, Any, Optional

# Thư viện tìm kiếm DuckDuckGo
try:
    try:
        from ddgs import DDGS
    except ImportError:
        from duckduckgo_search import DDGS
    HAS_DDGS = True
except ImportError:
    HAS_DDGS = False

# Cơ sở tri thức ngành nghề kinh doanh mới & công nghệ cao (Fallback Online Legal Catalog)
EMERGING_INDUSTRIES_CATALOG = [
    {
        "keyword": "thương mại điện tử",
        "code": "4791",
        "name": "Bán lẻ theo yêu cầu đặt hàng qua bưu điện hoặc qua internet (Sàn TMĐT, Website bán hàng)",
        "is_conditional": 1,
        "license_required": "Thông báo website TMĐT bán hàng hoặc Đăng ký website cung cấp dịch vụ TMĐT",
        "regulatory_authority": "Cục Thương mại điện tử và Kinh tế số - Bộ Công Thương",
        "legal_basis": "Nghị định 52/2013/NĐ-CP và Nghị định 85/2021/NĐ-CP",
        "verify_url": "http://online.gov.vn",
        "description": "Bán lẻ mọi mặt hàng qua mạng internet, ứng dụng di động; cung cấp sàn giao dịch trực tuyến cho bên thứ ba."
    },
    {
        "keyword": "livestream",
        "code": "7310",
        "name": "Quảng cáo (Tiếp thị số, Livestream bán hàng, Affiliate Marketing)",
        "is_conditional": 0,
        "license_required": "Không yêu cầu giấy phép con riêng, nhưng phải kê khai doanh thu thuế đầy đủ",
        "regulatory_authority": "Sở Kế hoạch & Đầu tư, Chi cục Thuế quản lý",
        "legal_basis": "Luật Doanh nghiệp 2020, Thông tư 40/2021/TT-BTC về thuế HKD và cá nhân kinh doanh",
        "verify_url": "https://vanban.chinhphu.vn/?pageid=27160&docid=200676",
        "description": "Dịch vụ quảng bá sản phẩm, người có ảnh hưởng (KOL/KOC) nhận hoa hồng tiếp thị liên kết."
    },
    {
        "keyword": "trí tuệ nhân tạo",
        "code": "6201",
        "name": "Lập trình máy vi tính (Nghiên cứu & Ứng dụng Trí tuệ nhân tạo AI, LLM, SaaS)",
        "is_conditional": 0,
        "license_required": "Ngành nghề được ưu đãi cao nhất: Thuế suất TNDN 10% trong 15 năm, miễn 4 năm, giảm 50% trong 9 năm tiếp theo",
        "regulatory_authority": "Bộ Thông tin và Truyền thông / Bộ Khoa học và Công nghệ",
        "legal_basis": "Luật Công nghệ thông tin 2006, Nghị định 218/2013/NĐ-CP, Quyết định 38/2020/QĐ-TTg",
        "verify_url": "https://vanban.chinhphu.vn/?pageid=27160&docid=171926",
        "description": "Sản xuất phần mềm ứng dụng AI, xử lý dữ liệu lớn, điện toán đám mây và dịch vụ phần mềm tự động hóa."
    },
    {
        "keyword": "logistics",
        "code": "5229",
        "name": "Hoạt động dịch vụ hỗ trợ khác liên quan đến vận tải (Dịch vụ Logistics bên thứ 3 - 3PL)",
        "is_conditional": 1,
        "license_required": "Đăng ký điều kiện kinh doanh dịch vụ logistics theo Nghị định 163/2017/NĐ-CP",
        "regulatory_authority": "Sở Công Thương / Sở Giao thông Vận tải",
        "legal_basis": "Nghị định 163/2017/NĐ-CP quy định về kinh doanh dịch vụ logistics",
        "verify_url": "https://vanban.chinhphu.vn/?pageid=27160&docid=192461",
        "description": "Giao nhận hàng hóa, môi giới thuê phương tiện, xử lý kho bãi và chứng từ vận tải đa phương thức."
    },
    {
        "keyword": "năng lượng mặt trời",
        "code": "4321",
        "name": "Lắp đặt hệ thống điện (Điện mặt trời mái nhà, hệ thống năng lượng tái tạo)",
        "is_conditional": 1,
        "license_required": "Thỏa thuận đấu nối với Điện lực địa phương (EVN), thẩm duyệt PCCC công trình",
        "regulatory_authority": "Bộ Công Thương, Tập đoàn Điện lực Việt Nam (EVN), Cục Cảnh sát PCCC",
        "legal_basis": "Luật Điện lực 2004 (sửa đổi 2022), Nghị định 135/2024/NĐ-CP về điện mặt trời tự sản tự tiêu",
        "verify_url": "https://vanban.chinhphu.vn/?pageid=27160&docid=211756",
        "description": "Thi công, lắp đặt tấm pin quang điện, biến tần inverter và đấu nối lưới điện phân phối."
    },
    {
        "keyword": "game online",
        "code": "6201",
        "name": "Phát hành và vận hành trò chơi điện tử trên mạng (Game G1, G2, G3, G4)",
        "is_conditional": 1,
        "license_required": "Giấy phép cung cấp dịch vụ trò chơi điện tử G1 hoặc Giấy chứng nhận đăng ký G2, G3, G4",
        "regulatory_authority": "Cục Phát thanh, Truyền hình và Thông tin điện tử - Bộ TT&TT",
        "legal_basis": "Nghị định 72/2013/NĐ-CP và Nghị định 27/2018/NĐ-CP",
        "verify_url": "https://vanban.chinhphu.vn/?pageid=27160&docid=168673",
        "description": "Phát hành trò chơi trực tuyến có tương tác nhiều người chơi, có hệ thống thanh toán nạp thẻ."
    }
]


def search_web_legal(query: str, max_results: int = 4) -> List[Dict[str, Any]]:
    """
    Tìm kiếm thông tin ngành nghề và giấy phép con trên Internet.
    Sử dụng DuckDuckGo Search API, kết hợp cơ sở dữ liệu mở rộng cho các ngành kinh tế mới.
    """
    clean_query = query.strip()
    web_results = []

    # 1. Tra cứu trong Catalog Ngành nghề mới
    q_lower = clean_query.lower()
    for item in EMERGING_INDUSTRIES_CATALOG:
        if item["keyword"] in q_lower or any(word in item["name"].lower() for word in q_lower.split()):
            web_results.append({
                "source": "Catalog Ngành Kinh tế Mới & Công nghệ",
                "title": f"Mã ngành {item['code']}: {item['name']}",
                "snippet": f"Điều kiện: {item['license_required']}. Căn cứ pháp lý: {item['legal_basis']}. Cơ quan: {item['regulatory_authority']}",
                "url": item["verify_url"],
                "data": item
            })

    # 2. Thử nghiệm tìm kiếm trực tiếp với DuckDuckGo nếu có kết nối
    if HAS_DDGS and len(web_results) < max_results:
        try:
            search_term = f"mã ngành VSIC điều kiện thành lập {clean_query} thuvienphapluat vanban chinhphu"
            ddgs = DDGS()
            raw_hits = list(ddgs.text(search_term, max_results=max_results))
            for hit in raw_hits:
                web_results.append({
                    "source": "DuckDuckGo Web Search",
                    "title": hit.get("title", "Thông tin pháp luật"),
                    "snippet": hit.get("body", ""),
                    "url": hit.get("href", "https://vanban.chinhphu.vn/"),
                    "data": None
                })
        except Exception:
            pass  # Khi offline hoặc rate-limited, fallback catalog đã bảo đảm có dữ liệu

    return web_results[:max_results]


def hybrid_industry_search(db_manager, keyword: str) -> Dict[str, Any]:
    """
    Kiến trúc Hybrid Search:
    - BƯỚC 1: Truy vấn CSDL nội bộ SQLite (nhanh, chuẩn VSIC 2018).
    - BƯỚC 2: Nếu không thấy hoặc số lượng < 1, tự động kích hoạt Web Search mở rộng.
    """
    clean_kw = keyword.strip()
    db_industries = db_manager.search_industry(clean_kw)
    db_licenses = db_manager.get_license_info(clean_kw)

    is_web_fallback_used = False
    web_hits = []

    if not db_industries and not db_licenses:
        # Kích hoạt tìm kiếm web
        is_web_fallback_used = True
        web_hits = search_web_legal(clean_kw)

    return {
        "keyword": clean_kw,
        "db_industries": db_industries,
        "db_licenses": db_licenses,
        "is_web_fallback_used": is_web_fallback_used,
        "web_hits": web_hits,
        "total_results": len(db_industries) + len(web_hits)
    }
