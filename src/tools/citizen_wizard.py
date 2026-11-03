"""
Citizen Diagnostic Funnel (Phễu Chẩn Đoán Dân Sinh 3 Phút) - Version 3.0
Cho phép người dân yếu thế, người già, người ít học bóc tách tranh chấp pháp lý
chỉ qua 3-5 câu trắc nghiệm đơn giản (Có / Không / Lựa chọn 1-chạm), KHÔNG BẮT GÕ PHÍM.
Hỗ trợ 4 loại tranh chấp phổ biến nhất: Đòi nợ, Tranh chấp đất đai, Hôn nhân ly hôn, Thừa kế di sản.
"""

from typing import Dict, Any, List, Optional


class CitizenDiagnosticFunnel:
    """
    Phễu trắc nghiệm chẩn đoán pháp lý 1-chạm cho người dân.
    """

    CATEGORIES = {
        "DEBT": "💸 Đòi nợ & Vay mượn tài sản",
        "LAND": "🏡 Tranh chấp đất đai & Lối đi chung",
        "DIVORCE": "💔 Hôn nhân & Ly hôn",
        "INHERITANCE": "📜 Tranh chấp di sản thừa kế"
    }

    DIAGNOSTIC_TREES = {
        "DEBT": {
            "title": "Chẩn đoán Đòi nợ & Vay mượn",
            "steps": [
                {
                    "step_id": 1,
                    "question": "Khoản vay mượn này có giấy tờ hay chỉ thỏa thuận miệng?",
                    "options": [
                        {"label": "Có giấy viết tay / hợp đồng vay", "next_step": 2, "evidence_level": "HIGH"},
                        {"label": "Chỉ có tin nhắn Zalo / chuyển khoản", "next_step": 2, "evidence_level": "MEDIUM"},
                        {"label": "Cho vay miệng, không có tin nhắn gì", "next_step": 2, "evidence_level": "LOW"}
                    ]
                },
                {
                    "step_id": 2,
                    "question": "Thời hạn trả nợ đã quá hạn bao lâu?",
                    "options": [
                        {"label": "Dưới 3 năm kể từ ngày hẹn trả", "next_step": 3, "sol_status": "VALID"},
                        {"label": "Đã quá 3 năm không đòi", "next_step": 3, "sol_status": "EXPIRED_RISK"},
                        {"label": "Vay không hẹn ngày trả cụ thể", "next_step": 3, "sol_status": "NEED_DEMAND_NOTICE"}
                    ]
                },
                {
                    "step_id": 3,
                    "question": "Bên vay hiện tại có thái độ như thế nào?",
                    "options": [
                        {"label": "Cắt liên lạc, trốn tránh, chặn số", "conclude": "ABUSE_TRUST_OR_LAWSUIT"},
                        {"label": "Thừa nhận nợ nhưng hứa lèo, khất mãi", "conclude": "CIVIL_LAWSUIT"},
                        {"label": "Có dấu hiệu tẩu tán tài sản / bán nhà", "conclude": "URGENT_INJUNCTION"}
                    ]
                }
            ],
            "conclusions": {
                "ABUSE_TRUST_OR_LAWSUIT": {
                    "diagnosis": "Vụ việc có dấu hiệu trốn tránh trả nợ, có thể khởi kiện dân sự hoặc tố giác hành vi lạm dụng tín nhiệm chiếm đoạt tài sản nếu có hành vi bỏ trốn.",
                    "action_1": "Lập vi bằng lưu trữ ngay tin nhắn Zalo, sao kê chuyển khoản.",
                    "action_2": "Nộp đơn khởi kiện đòi nợ tại TAND cấp Quận/Huyện nơi người vay cư trú (Mẫu 23-DS).",
                    "action_3": "Nếu họ chuyển hộ khẩu bỏ trốn: Làm đơn tố giác tội phạm gửi Cơ quan CSĐT Công an Quận/Huyện."
                },
                "CIVIL_LAWSUIT": {
                    "diagnosis": "Tranh chấp hợp đồng vay tài sản thuần túy dân sự theo Điều 463 BLDS 2015.",
                    "action_1": "Gửi thông báo đòi nợ bằng văn bản chuyển phát bảo đảm (tạo chứng cứ chốt nợ).",
                    "action_2": "Khởi kiện TAND thụ lý để yêu cầu tính lãi suất chậm trả 10%/năm theo Điều 468 BLDS.",
                    "action_3": "Chuẩn bị đơn đề nghị Tòa áp dụng biện pháp khẩn cấp tạm thời phong tỏa tài khoản."
                },
                "URGENT_INJUNCTION": {
                    "diagnosis": "Tình huống KHẨN CẤP: Nguy cơ tẩu tán tài sản dẫn đến bản án vô hiệu trên thực tế.",
                    "action_1": "Nộp đơn khởi kiện đồng thời kèm ĐƠN YÊU CẦU ÁP DỤNG BIỆN PHÁP KHẨN CẤP TẠM THỜI (BPKCTT).",
                    "action_2": "Yêu cầu Tòa án phong tỏa tài sản/bất động sản của con nợ ngay lập tức theo Điều 114 BLTTDS.",
                    "action_3": "Nộp tiền bảo đảm tương đương theo yêu cầu của Tòa để được phong tỏa."
                }
            }
        },
        "LAND": {
            "title": "Chẩn đoán Tranh chấp Đất đai",
            "steps": [
                {
                    "step_id": 1,
                    "question": "Mảnh đất tranh chấp đã có Sổ đỏ (Giấy chứng nhận QSDĐ) chưa?",
                    "options": [
                        {"label": "Đã có Sổ đỏ đứng tên tôi/gia đình", "next_step": 2, "cert": "YES"},
                        {"label": "Chưa có Sổ đỏ (đất cha ông để lại, giấy tờ cũ)", "next_step": 2, "cert": "OLD_PAPER"},
                        {"label": "Không có giấy tờ gì, chỉ khai hoang", "next_step": 2, "cert": "NO"}
                    ]
                },
                {
                    "step_id": 2,
                    "question": "Vụ việc đã qua thủ tục Hòa giải tại UBND xã/phường chưa?",
                    "options": [
                        {"label": "Đã hòa giải nhưng KHÔNG THÀNH (có biên bản)", "next_step": 3, "concil": "DONE_FAILED"},
                        {"label": "Chưa từng nộp đơn ra UBND xã/phường", "next_step": 3, "concil": "NOT_YET"},
                        {"label": "UBND xã/phường ngâm hồ sơ không giải quyết", "next_step": 3, "concil": "DELAYED"}
                    ]
                },
                {
                    "step_id": 3,
                    "question": "Bản chất hành vi của bên kia là gì?",
                    "options": [
                        {"label": "Xây tường, rào lấn chiếm sang ranh giới đất", "conclude": "LAND_ENCROACHMENT"},
                        {"label": "Bịt lối đi chung, không cho đi qua", "conclude": "PASSAGEWAY_DISPUTE"},
                        {"label": "Cấp trùng Sổ đỏ sang tên người khác", "conclude": "ADMIN_LAWSUIT"}
                    ]
                }
            ],
            "conclusions": {
                "LAND_ENCROACHMENT": {
                    "diagnosis": "Tranh chấp ranh giới quyền sử dụng đất theo Luật Đất đai 2024.",
                    "action_1": "Bắt buộc phải có Biên bản Hòa giải không thành tại UBND cấp Xã trước khi Tòa thụ lý (Điều 235 Luật Đất đai).",
                    "action_2": "Yêu cầu Văn phòng đăng ký đất đai trích đo hiện trạng ranh giới thực tế.",
                    "action_3": "Nộp đơn khởi kiện yêu cầu tháo dỡ công trình lấn chiếm và trả lại hiện trạng đất ban đầu."
                },
                "PASSAGEWAY_DISPUTE": {
                    "diagnosis": "Tranh chấp quyền về lối đi qua bất động sản liền kề theo Điều 254 BLDS 2015.",
                    "action_1": "Pháp luật quy định chủ sở hữu bất động sản bị vây bọc có quyền yêu cầu mở một lối đi hợp lý.",
                    "action_2": "Nộp đơn yêu cầu UBND xã hòa giải xác định lối đi chung lịch sử.",
                    "action_3": "Nếu hòa giải không thành, nộp đơn kiện ra TAND, Tòa sẽ cử hội đồng thẩm định tại chỗ."
                },
                "ADMIN_LAWSUIT": {
                    "diagnosis": "Cấp Giấy chứng nhận trùng lặp hoặc sai đối tượng - Có yếu tố hủy quyết định hành chính.",
                    "action_1": "Thu thập bản sao hồ sơ cấp sổ đỏ tại Phòng Tài nguyên & Môi trường.",
                    "action_2": "Khởi kiện TAND cấp Tỉnh yêu cầu hủy GCNQSDĐ cấp sai quy định.",
                    "action_3": "Yêu cầu tạm dừng mọi giao dịch chuyển nhượng/thế chấp đối với thửa đất."
                }
            }
        }
    }

    @classmethod
    def get_funnel(cls, category: str = "DEBT") -> Dict[str, Any]:
        """Lấy cây chẩn đoán cho lĩnh vực tương ứng."""
        cat_key = category.upper()
        if cat_key not in cls.DIAGNOSTIC_TREES:
            cat_key = "DEBT"
        return cls.DIAGNOSTIC_TREES[cat_key]

    @classmethod
    def evaluate_answers(cls, category: str, answers: Dict[int, int]) -> Dict[str, Any]:
        """
        Đánh giá câu trả lời của người dân và đưa ra kết luận chẩn đoán tức thì.
        answers: {1: option_index, 2: option_index, 3: option_index}
        """
        tree = cls.get_funnel(category)
        steps = tree["steps"]
        
        # Xác định conclusion key dựa vào câu trả lời cuối cùng
        last_step = steps[-1]
        last_ans_idx = answers.get(last_step["step_id"], 0)
        options = last_step["options"]
        if 0 <= last_ans_idx < len(options):
            conclusion_key = options[last_ans_idx].get("conclude", list(tree["conclusions"].keys())[0])
        else:
            conclusion_key = list(tree["conclusions"].keys())[0]

        result = tree["conclusions"].get(conclusion_key, list(tree["conclusions"].values())[0])
        
        return {
            "category": category,
            "category_name": cls.CATEGORIES.get(category.upper(), "Dân sự"),
            "diagnosis_title": tree["title"],
            "conclusion_key": conclusion_key,
            "diagnosis": result["diagnosis"],
            "step_1": result["action_1"],
            "step_2": result["action_2"],
            "step_3": result["action_3"],
            "summary_advice": (
                f"💡 Lời khuyên 3 bước hành động ngay:\n"
                f"1. {result['action_1']}\n"
                f"2. {result['action_2']}\n"
                f"3. {result['action_3']}"
            )
        }
