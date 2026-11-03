"""
Deterministic Legal Rules Engine - Version 3.0
Tầng Dự Phòng Cấp 3 (Fallback Level 3):
Hệ chuyên gia tính toán và định vị tư pháp hoạt động ĐỘC LẬP 100% không phụ thuộc vào bất kỳ LLM nào.
Khi mất mạng hoàn toàn, hết quota Cloud Gemini hoặc Ollama offline, hệ thống vẫn trả về kết quả
chuẩn xác tuyệt đối theo quy định của Quốc hội và Tòa án nhân dân tối cao.
"""

from typing import Dict, Any, Optional
import datetime


class DeterministicLegalRules:
    """
    Bộ quy tắc tư pháp xác định chạy 100% Offline không cần AI.
    """

    @staticmethod
    def calculate_court_fee_expert(claim_amount: float) -> Dict[str, Any]:
        """Tính án phí theo Nghị quyết 326/2016/UBTVQH14."""
        amount = max(0.0, float(claim_amount))
        
        if amount <= 6000000:
            fee = 300000.0
            bracket = "Dưới hoặc bằng 6.000.000 VNĐ: Án phí cố định 300.000 VNĐ"
        elif amount <= 400000000:
            fee = amount * 0.05
            bracket = "Từ 6.000.000 đến 400.000.000 VNĐ: 5% giá trị tranh chấp"
        elif amount <= 800000000:
            fee = 20000000.0 + (amount - 400000000.0) * 0.04
            bracket = "Từ 400.000.000 đến 800.000.000 VNĐ: 20 triệu + 4% phần vượt 400 triệu"
        elif amount <= 2000000000:
            fee = 36000000.0 + (amount - 800000000.0) * 0.03
            bracket = "Từ 800.000.000 đến 2 tỷ VNĐ: 36 triệu + 3% phần vượt 800 triệu"
        elif amount <= 4000000000:
            fee = 72000000.0 + (amount - 2000000000.0) * 0.02
            bracket = "Từ 2 tỷ đến 4 tỷ VNĐ: 72 triệu + 2% phần vượt 2 tỷ"
        else:
            fee = 112000000.0 + (amount - 4000000000.0) * 0.001
            bracket = "Trên 4 tỷ VNĐ: 112 triệu + 0.1% phần vượt 4 tỷ"

        advance = fee * 0.5
        return {
            "claim_amount": amount,
            "total_fee": round(fee),
            "advance_payment": round(advance),
            "formatted_fee": f"{round(fee):,} VNĐ".replace(",", "."),
            "formatted_advance": f"{round(advance):,} VNĐ".replace(",", "."),
            "bracket": bracket,
            "legal_basis": "Nghị quyết số 326/2016/UBTVQH14 của Ủy ban Thường vụ Quốc hội",
            "is_offline_deterministic": True
        }

    @staticmethod
    def check_statute_of_limitations_expert(due_date_str: str, dispute_type: str = "CONTRACT") -> Dict[str, Any]:
        """Tính thời hiệu khởi kiện chính xác theo Điều 429 BLDS 2015."""
        date_formats = ["%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"]
        due_date = None
        for fmt in date_formats:
            try:
                due_date = datetime.datetime.strptime(due_date_str.strip(), fmt)
                break
            except Exception:
                continue

        if not due_date:
            return {
                "valid_format": False,
                "message": "Không nhận diện được định dạng ngày (vui lòng nhập dạng DD/MM/YYYY hoặc YYYY-MM-DD)"
            }

        now = datetime.datetime.now()
        years_diff = (now - due_date).days / 365.25

        # Tranh chấp hợp đồng: 3 năm (Điều 429 BLDS 2015)
        # Bồi thường thiệt hại ngoài hợp đồng: 3 năm (Điều 588 BLDS 2015)
        # Thừa kế: Bất động sản 30 năm, Động sản 10 năm (Điều 623 BLDS 2015)
        limit_years = 3
        if dispute_type.upper() == "INHERITANCE_REALTY":
            limit_years = 30
        elif dispute_type.upper() == "INHERITANCE_MOVABLE":
            limit_years = 10

        is_expired = years_diff > limit_years
        remaining_days = max(0, int((limit_years * 365.25) - (now - due_date).days))

        return {
            "valid_format": True,
            "due_date": due_date.strftime("%d/%m/%Y"),
            "dispute_type": dispute_type,
            "limit_years": limit_years,
            "is_expired": is_expired,
            "remaining_days": remaining_days,
            "status_label": "ĐÃ HẾT THỜI HIỆU (Nguy cơ bị đình chỉ vụ án)" if is_expired else f"CÒN THỜI HIỆU (Còn khoảng {remaining_days} ngày)",
            "advice": (
                "⚠️ Đã quá thời hạn khởi kiện 3 năm. Nếu bên vay yêu cầu Tòa áp dụng thời hiệu, Tòa sẽ đình chỉ giải quyết. Bạn cần tìm chứng cứ chứng minh con nợ đã có hành vi thừa nhận nghĩa vụ hoặc khất nợ lại để tính lại thời hiệu từ đầu (Điều 157 BLDS 2015)."
                if is_expired else
                "✅ Vụ việc đang trong thời hiệu an toàn. Hãy tiến hành nộp đơn khởi kiện sớm để tránh việc bị kéo dài hết thời hạn."
            ),
            "legal_basis": "Điều 429 và Điều 157 Bộ luật Dân sự 2015",
            "is_offline_deterministic": True
        }
