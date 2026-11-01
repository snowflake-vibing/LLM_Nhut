"""
Citizen In-Chat Legal Tools Suite - Version 4.0
Bộ công cụ tính toán & định vị tố tụng tự động phục vụ người dân:
1. CourtFeeCalculator: Tính án phí dân sự sơ thẩm theo Nghị quyết 326/2016/UBTVQH14.
2. StatuteOfLimitationsChecker: Kiểm tra thời hiệu khởi kiện theo Bộ luật Dân sự 2015.
3. CompetentAuthorityLocator: Xác định thẩm quyền Tòa án, UBND xã hoặc Cơ quan Công an tiếp nhận đơn.
4. InstantPetitionGenerator: Soạn thảo đơn từ dân sự chuẩn mực 1-chạm (.docx).
"""

import datetime
from typing import Dict, Any, Optional


class CitizenLegalTools:
    """
    Hệ thống công cụ hỗ trợ người dân tự tra cứu và tính toán pháp lý độc lập.
    """

    @staticmethod
    def calculate_court_fee(dispute_amount_vnd: float) -> Dict[str, Any]:
        """
        Tính án phí dân sự sơ thẩm có giá ngạch theo Danh mục ban hành kèm Nghị quyết 326/2016/UBTVQH14.
        """
        amount = float(dispute_amount_vnd)
        if amount <= 0:
            return {
                "dispute_amount": 0,
                "court_fee_vnd": 300000,
                "advance_fee_vnd": 150000,
                "bracket": "Tranh chấp không có giá ngạch hoặc không có số tiền",
                "explanation": "Án phí cố định là 300.000 VNĐ. Tiền tạm ứng án phí phải nộp trước là 50% = 150.000 VNĐ."
            }

        fee = 0
        bracket_desc = ""

        if amount <= 6000000:
            fee = 300000
            bracket_desc = "Từ 6.000.000 VNĐ trở xuống: Cố định 300.000 VNĐ"
        elif amount <= 400000000:
            fee = amount * 0.05
            bracket_desc = "Từ trên 6 triệu đến 400 triệu VNĐ: 5% giá trị tranh chấp"
        elif amount <= 800000000:
            fee = 20000000 + (amount - 400000000) * 0.04
            bracket_desc = "Từ trên 400 triệu đến 800 triệu VNĐ: 20 triệu + 4% phần vượt quá 400 triệu"
        elif amount <= 2000000000:
            fee = 36000000 + (amount - 800000000) * 0.03
            bracket_desc = "Từ trên 800 triệu đến 2 tỷ VNĐ: 36 triệu + 3% phần vượt quá 800 triệu"
        elif amount <= 4000000000:
            fee = 72000000 + (amount - 2000000000) * 0.02
            bracket_desc = "Từ trên 2 tỷ đến 4 tỷ VNĐ: 72 triệu + 2% phần vượt quá 2 tỷ"
        else:
            fee = 112000000 + (amount - 4000000000) * 0.001
            bracket_desc = "Từ trên 4 tỷ VNĐ: 112 triệu + 0.1% phần vượt quá 4 tỷ"

        advance_fee = fee * 0.5  # Tạm ứng án phí sơ thẩm là 50%

        return {
            "dispute_amount": amount,
            "court_fee_vnd": round(fee),
            "advance_fee_vnd": round(advance_fee),
            "bracket": bracket_desc,
            "legal_basis": "Nghị quyết số 326/2016/UBTVQH14 của Ủy ban Thường vụ Quốc hội",
            "formatted_fee": f"{round(fee):,} VNĐ",
            "formatted_advance": f"{round(advance_fee):,} VNĐ"
        }

    @staticmethod
    def check_statute_of_limitations(incident_date_str: str, domain: str = "CONTRACT") -> Dict[str, Any]:
        """
        Kiểm tra thời hiệu khởi kiện theo Bộ luật Dân sự 2015.
        - CONTRACT / DEBT: 03 năm (Điều 429 BLDS).
        - TORT (Bồi thường ngoài hợp đồng): 03 năm (Điều 588 BLDS).
        - INHERITANCE (Thừa kế bất động sản 30 năm, động sản 10 năm - Điều 623 BLDS).
        """
        try:
            # Hỗ trợ định dạng YYYY-MM-DD hoặc DD/MM/YYYY
            if "/" in incident_date_str:
                parts = incident_date_str.split("/")
                incident_date = datetime.date(int(parts[2]), int(parts[1]), int(parts[0]))
            else:
                incident_date = datetime.date.fromisoformat(incident_date_str)
        except Exception:
            return {
                "is_valid_date": False,
                "message": "Định dạng ngày không hợp lệ. Vui lòng nhập dạng DD/MM/YYYY (ví dụ: 15/06/2023)."
            }

        today = datetime.date.today()
        delta_days = (today - incident_date).days

        if domain in ["CONTRACT", "DEBT", "LOAN"]:
            limit_years = 3
            legal_article = "Điều 429 Bộ luật Dân sự 2015 (Thời hiệu khởi kiện về hợp đồng là 03 năm)"
        elif domain in ["TORT", "DAMAGE", "SCHOOL_VIOLENCE"]:
            limit_years = 3
            legal_article = "Điều 588 Bộ luật Dân sự 2015 (Thời hiệu yêu cầu bồi thường thiệt hại là 03 năm)"
        elif domain in ["INHERITANCE_LAND"]:
            limit_years = 30
            legal_article = "Điều 623 Bộ luật Dân sự 2015 (Thời hiệu chia di sản bất động sản là 30 năm)"
        else:
            limit_years = 3
            legal_article = "Điều 429 Bộ luật Dân sự 2015"

        expiry_date = incident_date.replace(year=incident_date.year + limit_years)
        remaining_days = (expiry_date - today).days

        is_expired = remaining_days <= 0

        return {
            "is_valid_date": True,
            "incident_date": incident_date.strftime("%d/%m/%Y"),
            "expiry_date": expiry_date.strftime("%d/%m/%Y"),
            "remaining_days": max(0, remaining_days),
            "is_expired": is_expired,
            "legal_article": legal_article,
            "status_label": "⚠️ ĐÃ HẾT THỜI HIỆU KHỞI KIỆN" if is_expired else f"🟢 CÒN THỜI HIỆU ({remaining_days} ngày)",
            "warning": (
                "Vụ việc của bạn đã vượt quá thời hiệu luật định! Tòa án có thể từ chối giải quyết nếu bên kia yêu cầu áp dụng thời hiệu."
                if is_expired else
                f"Bạn còn khoảng {remaining_days // 30} tháng {remaining_days % 30} ngày để nộp đơn khởi kiện bảo vệ quyền lợi."
            )
        }

    @staticmethod
    def locate_competent_authority(dispute_type: str, defendant_district: str, defendant_province: str) -> Dict[str, Any]:
        """
        Xác định thẩm quyền tiếp nhận đơn theo Bộ luật Tố tụng Dân sự 2015 và Luật Đất đai.
        """
        dtype = dispute_type.upper()
        if "LAND" in dtype or "ĐẤT" in dtype:
            return {
                "stage_1": f"UBND xã/phường nơi có đất tranh chấp ({defendant_district}, {defendant_province})",
                "stage_1_desc": "Bắt buộc hòa giải cơ sở tại UBND cấp xã theo Điều 202 Luật Đất đai. Không được kiện thẳng ra Tòa nếu chưa có Biên bản hòa giải không thành.",
                "stage_2": f"Tòa án nhân dân {defendant_district}, {defendant_province}",
                "stage_2_desc": "Nộp đơn khởi kiện giải quyết tranh chấp đất đai theo Điều 203 Luật Đất đai và Điều 39 BLTTDS sau khi hòa giải xã không thành.",
                "hotline_tip": "Ghé bộ phận Địa chính - Xây dựng tại UBND xã/phường để nộp đơn yêu cầu hòa giải trước."
            }
        elif "FRAUD" in dtype or "LỪA" in dtype or "CHIẾM ĐOẠT" in dtype:
            return {
                "stage_1": f"Cơ quan Cảnh sát điều tra (Công an) {defendant_district}, {defendant_province}",
                "stage_1_desc": "Nộp 'Đơn Tố giác Tội phạm' theo Điều 144, 145 Bộ luật Tố tụng Hình sự 2015 về hành vi Lừa đảo chiếm đoạt tài sản (Điều 174 BLHS) hoặc Lạm dụng tín nhiệm (Điều 175 BLHS).",
                "stage_2": f"Viện Kiểm sát nhân dân {defendant_district}",
                "stage_2_desc": "Cơ quan kiểm sát việc giải quyết nguồn tin tố giác tội phạm nếu quá 20 ngày Công an chưa phản hồi.",
                "hotline_tip": "Khi nộp đơn cần gửi kèm sao kê tài khoản ngân hàng và vi bằng tin nhắn lừa đảo."
            }
        else:  # DEBT, CONTRACT, DIVORCE
            return {
                "stage_1": f"Tòa án nhân dân {defendant_district}, {defendant_province}",
                "stage_1_desc": "Tòa án nơi bị đơn cư trú hoặc làm việc có thẩm quyền giải quyết sơ thẩm (Điều 35, Điều 39 Bộ luật Tố tụng Dân sự 2015).",
                "stage_2": "Trung tâm Trợ giúp Pháp lý Nhà nước (Nếu là hộ nghèo hoặc người cao tuổi)",
                "stage_2_desc": "Được cử Luật sư miễn phí 100% bào chữa theo Luật Trợ giúp Pháp lý 2017.",
                "hotline_tip": "Nộp đơn tại Tổ Hành chính Tư pháp của TAND cấp quận/huyện để lấy giấy biên nhận đơn."
            }
