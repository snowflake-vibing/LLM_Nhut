"""
Interactive Legal Roadmap & Evidence Vault Engine - Version 2.4
Quản lý tiến trình tố tụng trực quan (Visual Stepper) và thẩm định giá trị chứng cứ (Evidentiary Weight Meter).
Tuân thủ Bộ luật Tố tụng Dân sự 2015, Luật Đất đai, Luật Hôn nhân & Gia đình 2014, Bộ luật Dân sự 2015.
"""

from typing import Dict, Any, List


LEGAL_ROADMAPS: Dict[str, Dict[str, Any]] = {
    "SCHOOL_BULLYING": {
        "title": "Bản đồ Tiến trình Xử lý Bạo lực Học đường & Trách nhiệm Nhà trường",
        "legal_basis": "Điều 599 BLDS 2015, Nghị định 80/2017/NĐ-CP, Thông tư 38/2019/TT-BLĐTBXH",
        "steps": [
            {
                "step_number": 1,
                "step_name": "Sơ cứu & Hồ sơ Y tế Khẩn cấp",
                "timeframe": "Trong vòng 24 giờ đầu",
                "authority": "Bệnh viện / Cơ sở y tế có thẩm quyền",
                "action": "Đưa trẻ đi khám, yêu cầu cấp Giấy chứng nhận thương tích, lưu giữ toàn bộ hóa đơn viện phí, chụp ảnh thương tích đa góc độ.",
                "status_badge": "Bắt buộc khẩn cấp"
            },
            {
                "step_number": 2,
                "step_name": "Làm việc với Nhà trường & Trích xuất Camera",
                "timeframe": "2 - 3 ngày làm việc",
                "authority": "Ban Giám hiệu Nhà trường",
                "action": "Gửi Đơn yêu cầu giải quyết vụ việc, lập biên bản làm việc 3 bên (Nhà trường - Phụ huynh nạn nhân - Phụ huynh học sinh gây bạo lực), trích xuất camera giám sát.",
                "status_badge": "Trách nhiệm liên đới (Đ.599 BLDS)"
            },
            {
                "step_number": 3,
                "step_name": "Trưng cầu Giám định Tỷ lệ Tổn thương Cơ thể",
                "timeframe": "5 - 7 ngày",
                "authority": "Trung tâm Giám định Pháp y Tỉnh/Thành phố",
                "action": "Thực hiện giám định thương tật và đánh giá sang chấn tâm lý để làm căn cứ khởi kiện hoặc truy cứu trách nhiệm hình sự.",
                "status_badge": "Chứng cứ định lượng"
            },
            {
                "step_number": 4,
                "step_name": "Khởi kiện Bồi thường hoặc Tố giác Hành vi",
                "timeframe": "Theo luật định",
                "authority": "TAND cấp Huyện / Cơ quan Cảnh sát Điều tra",
                "action": "Nếu nhà trường chối bỏ trách nhiệm: Nộp đơn khởi kiện yêu cầu trường và phụ huynh bồi thường liên đới; nộp đơn tố cáo cơ quan công an nếu có dấu hiệu cố ý gây thương tích.",
                "status_badge": "Chế tài tư pháp"
            }
        ]
    },
    "LAND_BOUNDARY": {
        "title": "Bản đồ Tiến trình Giải quyết Tranh chấp Ranh giới Đất đai",
        "legal_basis": "Điều 202, 203 Luật Đất đai, Điều 175, 176 BLDS 2015",
        "steps": [
            {
                "step_number": 1,
                "step_name": "Thu thập Hồ sơ Địa chính & Hiện trạng Ranh giới",
                "timeframe": "5 - 10 ngày",
                "authority": "Chi nhánh Văn phòng Đăng ký Đất đai",
                "action": "Trích lục bản đồ địa chính, Giấy chứng nhận QSDĐ, biên bản cắm mốc ranh giới trước đây, chụp ảnh công trình lấn chiếm.",
                "status_badge": "Hồ sơ gốc"
            },
            {
                "step_number": 2,
                "step_name": "Hòa giải Bắt buộc tại UBND Cấp Xã",
                "timeframe": "Tối đa 45 ngày (Luật định)",
                "authority": "Hội đồng Hòa giải Tranh chấp Đất đai Cấp Xã",
                "action": "Nộp đơn yêu cầu hòa giải tại UBND xã nơi có đất. Đây là thủ tục TIỀN TỐ TỤNG BẮT BUỘC theo Điều 202 Luật Đất đai.",
                "status_badge": "Thủ tục bắt buộc"
            },
            {
                "step_number": 3,
                "step_name": "Lập Biên bản Hòa giải & Khởi kiện TAND",
                "timeframe": "Trong vòng 15 ngày sau hòa giải",
                "authority": "Tòa án Nhân dân cấp Huyện nơi có đất",
                "action": "Nếu hòa giải không thành: Nhận Biên bản hòa giải không thành có chữ ký Chủ tịch xã, nộp Đơn khởi kiện yêu cầu tháo dỡ phần lấn chiếm.",
                "status_badge": "Khởi kiện sơ thẩm"
            },
            {
                "step_number": 4,
                "step_name": "Xem xét Thẩm định tại Chỗ & Phán quyết",
                "timeframe": "4 - 6 tháng",
                "authority": "Hội đồng Xét xử Tòa án Nhân dân",
                "action": "Tòa phối hợp cơ quan tài nguyên môi trường đo đạc thực tế, tuyên buộc bên lấn chiếm trả lại ranh giới đất theo đúng Sổ đỏ đã cấp.",
                "status_badge": "Bản án có hiệu lực"
            }
        ]
    },
    "DEBT_COLLECTION": {
        "title": "Bản đồ Tiến trình Khởi kiện Đòi nợ khi Con nợ Bỏ trốn",
        "legal_basis": "Điều 463, 466 BLDS 2015; Điều 39, 40 BLTTDS 2015; Điều 175 BLHS",
        "steps": [
            {
                "step_number": 1,
                "step_name": "Lập Vi bằng & Cố định Chứng cứ Giao dịch",
                "timeframe": "1 - 3 ngày",
                "authority": "Văn phòng Thừa phát lại",
                "action": "Lập Vi bằng ghi nhận sao kê tài khoản nhận tiền, tin nhắn xác nhận vay mượn qua Zalo/SMS, ghi âm cuộc gọi cam kết trả nợ.",
                "status_badge": "Hợp pháp hóa chứng cứ số"
            },
            {
                "step_number": 2,
                "step_name": "Xác minh Nơi cư trú Cuối cùng của Con nợ",
                "timeframe": "7 - 10 ngày",
                "authority": "Công an Cấp Xã nơi con nợ từng thường trú/tạm trú",
                "action": "Yêu cầu cơ quan công an xác nhận thông tin con nợ từng cư trú tại địa bàn nhưng hiện không có mặt để áp dụng Điều 40 BLTTDS.",
                "status_badge": "Căn cứ thẩm quyền Tòa"
            },
            {
                "step_number": 3,
                "step_name": "Nộp Đơn Khởi kiện & Niêm yết Xét xử Vắng mặt",
                "timeframe": "4 - 6 tháng",
                "authority": "Tòa án Nhân dân nơi cư trú cuối cùng",
                "action": "Tòa án thụ lý và thực hiện thủ tục niêm yết tống đạt công khai theo luật. Sau thời hạn niêm yết, Tòa tiến hành xét xử vắng mặt con nợ.",
                "status_badge": "Xử vắng mặt hợp lệ"
            },
            {
                "step_number": 4,
                "step_name": "Yêu cầu Thi hành án hoặc Chuyển Cơ quan Điều tra",
                "timeframe": "Theo yêu cầu thi hành án",
                "authority": "Chi cục THADS / Cơ quan Cảnh sát Điều tra",
                "action": "Kê biên phong tỏa tài sản con nợ đứng tên. Nếu con nợ có thủ đoạn gian dối tẩu tán tài sản rồi bỏ trốn, nộp đơn tố giác tội 'Lạm dụng tín nhiệm chiếm đoạt tài sản' (Đ.175 BLHS).",
                "status_badge": "Chế tài tối đa"
            }
        ]
    },
    "DIVORCE_CUSTODY": {
        "title": "Bản đồ Tiến trình Ly hôn, Quyền Nuôi con & Phân chia Tài sản",
        "legal_basis": "Điều 51, 55, 59, 81 Luật Hôn nhân & Gia đình 2014",
        "steps": [
            {
                "step_number": 1,
                "step_name": "Chuẩn bị Hồ sơ Nhân thân & Bằng chứng Tài sản",
                "timeframe": "3 - 5 ngày",
                "authority": "Đương sự tự chuẩn bị",
                "action": "Đăng ký kết hôn (bản chính), Khai sinh con, CCCD hai vợ chồng, Sổ đỏ, sổ tiết kiệm, sao kê tài khoản ngân hàng để chứng minh tài sản chung.",
                "status_badge": "Hồ sơ khởi đầu"
            },
            {
                "step_number": 2,
                "step_name": "Nộp Đơn & Hòa giải tại Trung tâm Hòa giải Tòa án",
                "timeframe": "20 - 30 ngày",
                "authority": "Hòa giải viên Tòa án Nhân dân",
                "action": "Tiến hành hòa giải đoàn tụ hoặc hòa giải thuận tình ly hôn theo Luật Hòa giải, đối thoại tại Tòa án.",
                "status_badge": "Hòa giải tư pháp"
            },
            {
                "step_number": 3,
                "step_name": "Giao nộp Chứng cứ Quyền Nuôi con & Tài chính",
                "timeframe": "1 - 2 tháng",
                "authority": "Thẩm phán được phân công",
                "action": "Mẹ cung cấp bằng chứng con dưới 36 tháng tuổi (Khoản 3 Đ.81). Chứng minh điều kiện thu nhập, chỗ ở, thời gian chăm sóc trẻ. Trẻ từ 7 tuổi trở lên Tòa lấy ý kiến bằng văn bản.",
                "status_badge": "Quyết định nuôi con"
            },
            {
                "step_number": 4,
                "step_name": "Phán quyết Chia Đôi Tài sản có Tính Công sức",
                "timeframe": "4 - 6 tháng",
                "authority": "Hội đồng Xét xử Sơ thẩm",
                "action": "Tài sản chung vợ chồng về nguyên tắc chia đôi nhưng tính đến công sức đóng góp, lỗi của mỗi bên và bảo vệ quyền lợi hợp pháp của người vợ/con chưa thành niên.",
                "status_badge": "Phán quyết có hiệu lực"
            }
        ]
    }
}


EVIDENCE_CATALOG: Dict[str, Dict[str, Any]] = {
    "NOTARIZED_DOC": {
        "name": "Văn bản công chứng / Chứng thực nhà nước",
        "weight": 95,
        "category": "Chứng cứ trực tiếp vững chắc",
        "legal_ref": "Điều 92 BLTTDS 2015: Những tình tiết, sự kiện không phải chứng minh",
        "advice": "Tài liệu này có giá trị chứng minh tuyệt đối trước Tòa mà không cần thẩm tra lại, trừ khi có bằng chứng chứng minh văn bản bị làm giả."
    },
    "BAILIFF_RECORD": {
        "name": "Vi bằng do Văn phòng Thừa phát lại lập",
        "weight": 90,
        "category": "Chứng cứ trực tiếp có giá trị nguồn",
        "legal_ref": "Nghị định 08/2020/NĐ-CP về tổ chức và hoạt động của Thừa phát lại",
        "advice": "Vi bằng có giá trị chứng cứ để Tòa án xem xét khi giải quyết vụ việc. Rất tối ưu khi ghi nhận tin nhắn điện thoại, giao nhận tiền hoặc hiện trạng lấn chiếm."
    },
    "BANK_STATEMENT": {
        "name": "Sao kê tài khoản có dấu đỏ ngân hàng",
        "weight": 85,
        "category": "Dữ liệu giao dịch tài chính chuẩn",
        "legal_ref": "Điều 94, 95 BLTTDS 2015: Dữ liệu điện tử được xác thực",
        "advice": "Chứng minh rõ ràng dòng tiền chuyển đi, thời gian, số tài khoản thụ hưởng. Cực kỳ có giá trị trong vụ việc đòi nợ và chứng minh tài sản chung."
    },
    "HANDWRITTEN_NOTE": {
        "name": "Giấy viết tay có chữ ký / Điểm chỉ",
        "weight": 65,
        "category": "Chứng cứ còn tiềm ẩn tranh chấp",
        "legal_ref": "Điều 100 BLTTDS 2015: Giám định chữ ký, chữ viết",
        "advice": "Nếu đối phương chối bỏ chữ ký, cần làm thủ tục yêu cầu Tòa án trưng cầu giám định chữ ký/chữ viết tại Phân viện Khoa học Hình sự."
    },
    "DIGITAL_CHAT_SCREENSHOT": {
        "name": "Ảnh chụp màn hình tin nhắn Zalo / SMS / Messenger",
        "weight": 40,
        "category": "Dữ liệu điện tử chưa được bảo chứng",
        "legal_ref": "Điều 95 BLTTDS 2015: Thông điệp dữ liệu điện tử",
        "advice": "Ảnh chụp màn hình rất dễ bị đối phương phản bác là giả mạo hoặc photoshop. BẮT BUỘC NÊN mang điện thoại đến Văn phòng Thừa phát lại để LẬP VI BẰNG trước khi nộp cho Tòa án."
    },
    "AUDIO_RECORDING": {
        "name": "File ghi âm cuộc gọi / Trò chuyện",
        "weight": 50,
        "category": "Tài liệu nghe nhìn cần xác minh nguồn gốc",
        "legal_ref": "Điều 95 BLTTDS 2015: Tài liệu nghe nhìn",
        "advice": "Người giao nộp file ghi âm phải trình bày rõ xuất xứ, không được cắt ghép chỉnh sửa, và có thể phải nộp kèm văn bản chuyển dịch lời thoại (transcription)."
    },
    "WITNESS_STATEMENT": {
        "name": "Lời khai của người làm chứng",
        "weight": 45,
        "category": "Nguồn chứng cứ phụ trợ",
        "legal_ref": "Điều 99 BLTTDS 2015: Lời khai của người làm chứng",
        "advice": "Chỉ có giá trị khi người làm chứng trực tiếp nhìn thấy/nghe thấy sự việc và cam đoan chịu trách nhiệm hình sự nếu khai gian dối trước Tòa."
    }
}


class EvidenceVaultEngine:
    """
    Engine phân tích lộ trình pháp lý và chấm điểm độ mạnh chứng cứ.
    """

    @staticmethod
    def get_roadmap(case_id: str) -> Dict[str, Any]:
        """Lấy lộ trình chi tiết cho từng vụ việc."""
        return LEGAL_ROADMAPS.get(case_id, LEGAL_ROADMAPS["DEBT_COLLECTION"])

    @staticmethod
    def evaluate_evidence_portfolio(selected_keys: List[str]) -> Dict[str, Any]:
        """
        Đánh giá danh mục chứng cứ mà người dùng đang sở hữu.
        """
        if not selected_keys:
            return {
                "score": 0,
                "rating": "Chưa có chứng cứ",
                "color": "gray",
                "summary": "Bạn chưa chọn chứng cứ nào. Vui lòng tick chọn các tài liệu hiện có để AI phân tích độ mạnh pháp lý.",
                "actionable_tips": [
                    "Bắt đầu thu thập ngay các tài liệu văn bản gốc hoặc sao kê ngân hàng.",
                    "Lập Vi bằng tại Văn phòng Thừa phát lại đối với các chứng cứ điện tử."
                ]
            }

        total_weight = 0
        items_detail = []
        has_notarized_or_bailiff = False
        has_only_screenshot = True

        for k in selected_keys:
            info = EVIDENCE_CATALOG.get(k)
            if info:
                total_weight += info["weight"]
                items_detail.append(info)
                if k in ["NOTARIZED_DOC", "BAILIFF_RECORD"]:
                    has_notarized_or_bailiff = True
                if k not in ["DIGITAL_CHAT_SCREENSHOT", "AUDIO_RECORDING"]:
                    has_only_screenshot = False

        avg_score = min(100, int((total_weight / (len(selected_keys) * 100)) * 100 + (10 if has_notarized_or_bailiff else 0)))

        if avg_score >= 80:
            rating = "Rất Vững Chắc (High Evidentiary Weight)"
            color = "green"
            summary = "Hồ sơ chứng cứ của bạn có giá trị pháp lý rất cao, khả năng được Tòa án chấp thuận gần như tuyệt đối."
        elif avg_score >= 60:
            rating = "Khá Tốt (Moderate Weight)"
            color = "blue"
            summary = "Hồ sơ có giá trị chứng minh nhưng cần bổ sung thêm xác nhận của cơ quan chuyên môn để chống phản tố."
        else:
            rating = "Rủi Ro Cao (Weak / Unverified Weight)"
            color = "red"
            summary = "Chứng cứ hiện tại chủ yếu là dữ liệu điện tử hoặc giấy tờ dễ bị chối bỏ chữ ký. Nguy cơ bị Tòa bác yêu cầu nếu đối phương phủ nhận."

        tips = []
        if has_only_screenshot:
            tips.append("🚨 CẢNH BÁO QUAN TRỌNG: Bạn chỉ có ảnh chụp màn hình. Hãy ra ngay Văn phòng Thừa phát lại để Lập Vi Bằng (chi phí ~1-2 triệu VNĐ), biến tin nhắn Zalo thành chứng cứ không thể chối cãi!")
        if "HANDWRITTEN_NOTE" in selected_keys and not has_notarized_or_bailiff:
            tips.append("💡 Giấy viết tay nên kết hợp với sao kê ngân hàng để chứng minh giao dịch thực tế đã phát sinh.")
        if not tips:
            tips.append("✅ Hồ sơ đã rất chuẩn mực. Bạn có thể tiến hành nộp hồ sơ khởi kiện ngay.")

        return {
            "score": avg_score,
            "rating": rating,
            "color": color,
            "summary": summary,
            "items_detail": items_detail,
            "actionable_tips": tips
        }
