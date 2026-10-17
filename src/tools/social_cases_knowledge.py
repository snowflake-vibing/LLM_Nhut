"""
Social Cases Legal Knowledge & Advisory Engine - Version 2.1
Cơ sở tri thức và quy trình xử lý chuyên sâu cho 4 tình huống pháp lý đời sống phức tạp:
1. Bạo lực học đường & Trách nhiệm của nhà trường
2. Tranh chấp ranh giới Sổ đỏ & Xây dựng lấn chiếm
3. Chủ nợ khởi kiện đòi nợ khi con nợ cố tình bỏ trốn
4. Ly hôn, Phân chia tài sản & Tranh chấp quyền nuôi con
"""

from typing import Dict, Any, List, Optional


SOCIAL_CASES_DATA = {
    "SCHOOL_VIOLENCE": {
        "title": "Bạo lực học đường & Trách nhiệm bồi thường của Nhà trường",
        "keywords": ["bạo lực học đường", "đánh nhau ở trường", "trường không chịu trách nhiệm", "học sinh bị đánh", "thương tích trong trường"],
        "key_laws": [
            "Điều 599 Bộ luật Dân sự 2015: Trách nhiệm của nhà trường đối với thiệt hại do người dưới 15 tuổi gây ra.",
            "Điều 584, 590 Bộ luật Dân sự 2015: Căn cứ phát sinh và chi phí bồi thường thiệt hại do sức khỏe bị xâm phạm.",
            "Nghị định 80/2017/NĐ-CP: Quy định về môi trường giáo dục an toàn, lành mạnh, thân thiện, phòng, chống bạo lực học đường."
        ],
        "core_doctrine": (
            "Theo Khoản 1 Điều 599 BLDS 2015: Người dưới 15 tuổi gây thiệt hại trong thời gian trường học trực tiếp quản lý "
            "thì NHÀ TRƯỜNG PHẢI BỒI THƯỜNG THIỆT HẠI PHÁT SINH. Nhà trường chỉ được miễn trách nhiệm nếu chứng minh được "
            "mình hoàn toàn không có lỗi trong công tác quản lý, giám sát học sinh."
        ),
        "practical_steps": [
            "Bước 1 - Lập biên bản y tế và giám định thương tật: Đưa học sinh đi khám/nhập viện ngay lập tức, lưu giữ toàn bộ hóa đơn viện phí, bệnh án, kết luận thương tích làm chứng cứ pháp lý vững chắc.",
            "Bước 2 - Yêu cầu Ban giám hiệu nhà trường trích xuất camera & lập biên bản: Gửi văn bản chính thức yêu cầu nhà trường tổ chức buổi làm việc ba bên (Gia đình nạn nhân - Nhà trường - Phụ huynh học sinh gây bạo lực).",
            "Bước 3 - Gửi Đơn khiếu nại đến Phòng/Sở GD&ĐT và Đơn tố cáo đến Công an: Nếu nhà trường thoái thác trách nhiệm, gửi đơn khiếu nại hành chính và đơn đề nghị cơ quan công an thụ lý xác minh hành vi cố ý gây thương tích."
        ],
        "default_doc_type": "SCHOOL_VIOLENCE_COMPLAINT"
    },

    "LAND_DISPUTE": {
        "title": "Tranh chấp Ranh giới Sổ đỏ & Xây dựng Lấn chiếm Đất đai",
        "keywords": ["tranh chấp ranh giới", "sổ đỏ", "lấn chiếm đất", "xây lấn sang nhà", "ranh giới thửa đất", "đo đạc đất"],
        "key_laws": [
            "Điều 175, 176 Bộ luật Dân sự 2015: Ranh giới giữa các bất động sản và mốc giới ngăn cách.",
            "Điều 202 Luật Đất đai: Thủ tục bắt buộc hòa giải tranh chấp đất đai tại UBND cấp xã/phường nơi có đất.",
            "Điều 203 Luật Đất đai: Thẩm quyền giải quyết tranh chấp đất đai của Tòa án nhân dân khi đương sự có Sổ đỏ (GCN QSDĐ)."
        ],
        "core_doctrine": (
            "Theo Điều 175 BLDS 2015, người sử dụng đất không được lấn, chiếm hoặc thay đổi mốc giới ngăn cách. "
            "Đặc biệt, theo Điều 202 Luật Đất đai, HÒA GIẢI TẠI UBND CẤP XÃ NƠI CÓ ĐẤT LÀ THỦ TỤC BẮT BUỘC TIỀN TỐ TỤNG. "
            "Tòa án nhân dân sẽ trả lại đơn khởi kiện nếu chưa có Biên bản hòa giải không thành của UBND cấp xã."
        ),
        "practical_steps": [
            "Bước 1 - Giữ nguyên hiện trạng & thu thập hồ sơ địa chính: Sao y Sổ đỏ, trích lục bản đồ địa chính, chụp ảnh/quay phim hiện trường công trình xây dựng có dấu hiệu lấn mốc giới.",
            "Bước 2 - Nộp Đơn yêu cầu hòa giải tranh chấp đất đai tại UBND xã/phường: UBND xã có trách nhiệm tổ chức phiên hòa giải trong thời hạn tối đa 45 ngày và lập biên bản hòa giải thành/không thành.",
            "Bước 3 - Khởi kiện tại Tòa án nhân dân cấp huyện nơi có đất: Nếu hòa giải không thành, nộp Đơn khởi kiện buộc tháo dỡ công trình lấn chiếm, trả lại nguyên trạng ranh giới đất theo Sổ đỏ."
        ],
        "default_doc_type": "LAND_DISPUTE_PETITION"
    },

    "DEBT_COLLECTION": {
        "title": "Khởi kiện Đòi nợ & Xử lý khi Con nợ Cố tình Bỏ trốn",
        "keywords": ["đòi nợ", "con nợ bỏ trốn", "vay tiền không trả", "quỵt nợ", "chủ nợ", "khởi kiện đòi nợ"],
        "key_laws": [
            "Điều 463, 466 Bộ luật Dân sự 2015: Hợp đồng vay tài sản và nghĩa vụ trả đủ nợ khi đến hạn.",
            "Điều 39, 40 Bộ luật Tố tụng Dân sự 2015: Thẩm quyền của Tòa án nơi cư trú hoặc nơi làm việc cuối cùng của bị đơn.",
            "Điều 175 Bộ luật Hình sự 2015 (sửa đổi 2017): Tội lạm dụng tín nhiệm chiếm đoạt tài sản (hành vi bỏ trốn để chiếm đoạt tiền vay từ 4.000.000đ trở lên)."
        ],
        "core_doctrine": (
            "Nếu con nợ vay tiền rồi cố tình cắt liên lạc, rời khỏi nơi cư trú nhằm không trả nợ: "
            "1. Về Dân sự: Chủ nợ vẫn có quyền nộp Đơn khởi kiện tại Tòa án nơi con nợ cư trú cuối cùng theo Điều 40 BLTTDS. Tòa án sẽ niêm yết công khai và xét xử vắng mặt. "
            "2. Về Hình sự: Nếu có dấu hiệu bỏ trốn, tẩu tán tài sản để quỵt nợ, hành vi này có dấu hiệu cấu thành Tội Lạm dụng tín nhiệm chiếm đoạt tài sản theo Điều 175 BLHS, thuộc thẩm quyền Cơ quan Cảnh sát điều tra."
        ),
        "practical_steps": [
            "Bước 1 - Tổng hợp chuỗi bằng chứng giao dịch: Hợp đồng vay/giấy mượn nợ viết tay, sao kê ủy nhiệm chi ngân hàng, tin nhắn/ghi âm xác nhận nợ và thời hạn hoàn trả.",
            "Bước 2 - Gửi văn bản thông báo đòi nợ & Xác nhận nơi cư trú: Gửi thư bảo đảm hoặc liên hệ Công an xã/phường nơi con nợ thường trú để xin giấy xác nhận tình trạng cư trú thực tế.",
            "Bước 3 - Lựa chọn thủ tục: Nộp Đơn khởi kiện dân sự đòi nợ tại TAND hoặc nộp Đơn tố giác tội phạm tại Cơ quan Cảnh sát điều tra (Công an cấp huyện) nếu con nợ có hành vi lừa dối, bỏ trốn chiếm đoạt tài sản."
        ],
        "default_doc_type": "DEBT_COLLECTION_LAWSUIT"
    },

    "DIVORCE_AND_CUSTODY": {
        "title": "Ly hôn, Phân chia Tài sản & Tranh chấp Quyền nuôi con",
        "keywords": ["ly hôn", "chia tài sản", "quyền nuôi con", "giành quyền nuôi con", "thuận tình ly hôn", "đơn phương ly hôn", "cấp dưỡng"],
        "key_laws": [
            "Điều 55, 56 Luật Hôn nhân và Gia đình 2014: Thủ tục Thuận tình ly hôn và Ly hôn đơn phương.",
            "Điều 59 Luật Hôn nhân và Gia đình 2014: Nguyên tắc giải quyết tài sản chung (chia đôi có tính đến công sức, hoàn cảnh và lỗi của các bên).",
            "Điều 81 Luật Hôn nhân và Gia đình 2014: Quyền nuôi con - Con dưới 36 tháng tuổi giao cho mẹ; Con từ đủ 7 tuổi phải hỏi ý kiến, nguyện vọng của con."
        ],
        "core_doctrine": (
            "Về quyền nuôi con: Ưu tiên thỏa thuận của vợ chồng vì sự phát triển toàn diện của con. "
            "Nếu không thỏa thuận được: Con dưới 36 tháng tuổi theo luật giao người mẹ nuôi dưỡng (trừ phi mẹ không đủ điều kiện); "
            "Con từ đủ 7 tuổi trở lên, Tòa án bắt buộc phải ghi nhận ý kiến nguyện vọng bằng văn bản của con. "
            "Về tài sản: Tài sản riêng hình thành trước hôn nhân hoặc được tặng cho/thừa kế riêng thuộc về người đó; tài sản chung tạo lập trong thời kỳ hôn nhân chia đôi nhưng có xem xét tỷ lệ đóng góp."
        ),
        "practical_steps": [
            "Bước 1 - Hoàn thiện hồ sơ pháp lý: Giấy đăng ký kết hôn (bản gốc), CCCD gắn chip hai bên, Giấy khai sinh của các con, giấy tờ chứng minh tài sản chung (Sổ đỏ, đăng ký xe, sổ tiết kiệm...).",
            "Bước 2 - Lựa chọn hình thức ly hôn: Thuận tình ly hôn (nộp tại TAND nơi cư trú của một trong hai bên) hoặc Đơn phương ly hôn (nộp tại TAND nơi bị đơn cư trú).",
            "Bước 3 - Tham gia phiên hòa giải tại Tòa án và chuẩn bị chứng cứ chứng minh điều kiện nuôi dạy con (thu nhập ổn định, thời gian chăm sóc, nhân thân tốt)."
        ],
        "default_doc_type": "DIVORCE_PETITION"
    }
}


class SocialCasesKnowledgeEngine:
    """
    Engine cung cấp tri thức chuyên sâu và giải pháp pháp lý thực chiến cho 4 case đời sống.
    """

    @classmethod
    def match_case(cls, query: str) -> Optional[str]:
        q_norm = query.lower()
        for case_id, info in SOCIAL_CASES_DATA.items():
            for kw in info["keywords"]:
                if kw in q_norm:
                    return case_id
        return None

    @classmethod
    def get_case_solution(cls, case_id: str) -> Optional[Dict[str, Any]]:
        return SOCIAL_CASES_DATA.get(case_id)

    @classmethod
    def generate_advisory_text(cls, case_id: str) -> str:
        case_info = SOCIAL_CASES_DATA.get(case_id)
        if not case_info:
            return ""

        laws_formatted = "\n".join([f"- {law}" for law in case_info["key_laws"]])
        steps_formatted = "\n".join([f"{step}" for step in case_info["practical_steps"]])

        text = (
            f"### ⚖️ Hướng dẫn Pháp lý Chiến lược: {case_info['title']}\n\n"
            f"#### 📖 Căn cứ Pháp luật Trọng tâm:\n{laws_formatted}\n\n"
            f"#### 💡 Góc nhìn Phân tích của Luật sư:\n{case_info['core_doctrine']}\n\n"
            f"#### 🚀 Lộ trình 3 Bước Xử lý Thực tế:\n{steps_formatted}\n\n"
            f"👉 *Hệ thống đã chuẩn bị sẵn Biểu mẫu Văn bản/Đơn từ pháp lý chuẩn hóa bên dưới. "
            f"Bạn có thể kiểm tra hoặc tải ngay file Word (.docx) để hoàn tất thủ tục!*"
        )
        return text
