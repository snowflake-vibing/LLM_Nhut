"""
Module: UsuryTrapDetector - Máy Quét Bẫy Tín Dụng Đen & Lãi Suất Cắt Cổ
Thiết kế riêng cho người dân nghèo, lao động tự do, công nhân, người dính bốc bát họ/app đen.
Căn cứ pháp lý:
- Điều 468 Bộ luật Dân sự 2015: Trần lãi suất thỏa thuận không quá 20%/năm. Phần vượt quá vô hiệu.
- Điều 201 Bộ luật Hình sự 2015 (sửa đổi 2017): Tội cho vay lãi nặng trong giao dịch dân sự
  (Lãi suất gấp 5 lần mức trần tối đa = 100%/năm và thu lợi bất chính từ 30 triệu đồng trở lên).
- Nghị quyết 01/2021/NQ-HĐTP hướng dẫn áp dụng Điều 201 Bộ luật Hình sự.
"""

from typing import Dict, Any, List
import math


class UsuryTrapDetector:
    CIVIL_CEILING_RATE = 0.20  # 20%/năm theo Điều 468 BLDS 2015
    CRIMINAL_THRESHOLD_MULTIPLIER = 5  # Gấp 5 lần mức cao nhất theo Điều 201 BLHS 2015
    CRIMINAL_CEILING_RATE = CIVIL_CEILING_RATE * CRIMINAL_THRESHOLD_MULTIPLIER  # 100%/năm
    CRIMINAL_ILLICIT_PROFIT_THRESHOLD = 30_000_000  # 30 triệu đồng

    @classmethod
    def analyze_loan(
        cls,
        principal_amount: float,
        actual_received_amount: float,
        term_days: int,
        periodic_interest_fee: float,
        fee_cycle_days: int = 1,
        hidden_fees: float = 0.0
    ) -> Dict[str, Any]:
        """
        Phân tích chi tiết một giao dịch vay:
        - principal_amount: Số tiền ghi trên giấy nợ/app (gốc danh nghĩa)
        - actual_received_amount: Số tiền người dân thực sự cầm về tay (sau khi bị trừ đầu trừ đuôi)
        - term_days: Thời hạn vay (ví dụ: 30 ngày, 50 ngày bốc bát họ)
        - periodic_interest_fee: Số tiền lãi/phí phải đóng theo chu kỳ
        - fee_cycle_days: Chu kỳ đóng tiền (1 = hàng ngày, 7 = hàng tuần, 30 = hàng tháng)
        - hidden_fees: Phí hồ sơ, phí giải ngân, tiền bảo hiểm khoản vay...
        """
        if actual_received_amount <= 0 or term_days <= 0:
            raise ValueError("Số tiền thực nhận và thời hạn vay phải lớn hơn 0.")

        # Số kỳ thanh toán
        num_cycles = max(1.0, term_days / max(1, fee_cycle_days))
        total_interest_paid = (periodic_interest_fee * num_cycles) + hidden_fees
        
        # Tiền bị cắt ngay từ đầu (nếu có: ghi vay 10 triệu chỉ đưa 8 triệu -> cắt 2 triệu)
        initial_cut = max(0.0, principal_amount - actual_received_amount)
        real_cost_of_borrowing = total_interest_paid + initial_cut

        # Tính lãi suất thực tế theo năm (Effective Annualized Interest Rate dựa trên vốn thực nhận)
        # Lãi suất ngày = Chi phí vay thực / (Vốn thực nhận * Số ngày)
        daily_rate = real_cost_of_borrowing / (actual_received_amount * term_days)
        annualized_rate = daily_rate * 365.0
        annualized_percent = annualized_rate * 100.0

        # Mức lãi trần theo Luật Dân sự (20%/năm)
        legal_civil_interest = actual_received_amount * (cls.CIVIL_CEILING_RATE / 365.0) * term_days
        excess_interest = max(0.0, real_cost_of_borrowing - legal_civil_interest)

        # Đánh giá dấu hiệu hình sự (Điều 201 BLHS)
        is_criminal_rate = annualized_rate >= cls.CRIMINAL_CEILING_RATE
        illicit_profit = excess_interest  # Tiền thu lợi bất chính theo NQ 01/2021/NQ-HĐTP
        is_criminal_offense = is_criminal_rate and (illicit_profit >= cls.CRIMINAL_ILLICIT_PROFIT_THRESHOLD)

        # Phân loại mức độ nguy hiểm
        if is_criminal_offense:
            severity = "CRIMINAL_ALERT"
            color = "🔴 ĐỎ BÁO ĐỘNG (DẤU HIỆU TỘI PHẠM HÌNH SỰ)"
            status_text = "Hợp đồng này có dấu hiệu rõ ràng của Tội cho vay lãi nặng trong giao dịch dân sự (Điều 201 BLHS 2015)!"
        elif is_criminal_rate:
            severity = "EXTREME_USURY"
            color = "🟠 CAM NGUY HIỂM (LÃI CẮT CỔ TÍN DỤNG ĐEN)"
            status_text = "Lãi suất vượt trên 100%/năm (gấp hơn 5 lần trần pháp luật). Có dấu hiệu tín dụng đen!"
        elif annualized_rate > cls.CIVIL_CEILING_RATE:
            severity = "CIVIL_EXCESS"
            color = "🟡 VÀNG CẢNH BÁO (VƯỢT TRẦN DÂN SỰ)"
            status_text = "Lãi suất vượt trần 20%/năm theo Điều 468 Bộ luật Dân sự 2015. Phần lãi vượt không có giá trị pháp lý!"
        else:
            severity = "LEGAL"
            color = "🟢 XANH AN TOÀN (TRONG HẠN MỨC PHÁP LUẬT)"
            status_text = "Lãi suất nằm trong giới hạn cho phép của pháp luật dân sự."

        # Khuyến nghị hành động dân sinh
        recommendations = []
        if severity in ["CRIMINAL_ALERT", "EXTREME_USURY"]:
            recommendations.append("🛑 DỪNG NGAY việc trả thêm lãi cắt cổ. Pháp luật không bảo hộ mức lãi suất này.")
            recommendations.append(f"💰 Bạn đã bị tính chênh lệch bất hợp pháp: {cls.format_currency(excess_interest)}. Số tiền này được trừ thẳng vào nợ gốc hoặc buộc bên cho vay hoàn trả.")
            recommendations.append("🛡️ Thu thập toàn bộ bằng chứng: Tin nhắn SMS, Zalo, lịch sử chuyển khoản, ghi âm cuộc gọi đe dọa, hợp đồng vay/giấy tay.")
            recommendations.append("📝 Nộp ĐƠN TỐ GIÁC TỘI PHẠM đến Cơ quan Cảnh sát Điều tra Công an Quận/Huyện nơi bên cho vay hoạt động.")
            recommendations.append("👨‍👩‍👧 Báo ngay cho người thân và chính quyền xã/phường nếu bị đe dọa, tạt sơn, khủng bố tinh thần.")
        elif severity == "CIVIL_EXCESS":
            recommendations.append(f"⚖️ Theo Điều 468 BLDS 2015, bạn chỉ có nghĩa vụ trả lãi tối đa 20%/năm (tương đương {cls.format_currency(legal_civil_interest)}).")
            recommendations.append(f"💵 Phần lãi vượt trần {cls.format_currency(excess_interest)} là vô hiệu, bạn có quyền từ chối thanh toán.")
        else:
            recommendations.append("✅ Giao dịch trong hạn mức hợp pháp. Hãy thanh toán đúng kỳ hạn để tránh phát sinh lãi quá hạn.")

        return {
            "principal_nominal": principal_amount,
            "actual_received": actual_received_amount,
            "initial_cut": initial_cut,
            "term_days": term_days,
            "total_borrowing_cost": real_cost_of_borrowing,
            "annualized_percent": round(annualized_percent, 2),
            "civil_legal_max_interest": round(legal_civil_interest, 0),
            "excess_interest_amount": round(excess_interest, 0),
            "illicit_profit": round(illicit_profit, 0),
            "severity": severity,
            "color_badge": color,
            "status_text": status_text,
            "is_criminal_rate": is_criminal_rate,
            "is_criminal_offense": is_criminal_offense,
            "recommendations": recommendations,
            "formatted_summary": (
                f"Lãi suất thực tế: {round(annualized_percent, 1)}%/năm | "
                f"Trần luật: 20%/năm | Lãi bất hợp pháp: {cls.format_currency(excess_interest)}"
            )
        }

    @classmethod
    def generate_criminal_denunciation_template(cls, loan_analysis: Dict[str, Any], borrower_info: Dict[str, str], lender_info: Dict[str, str]) -> str:
        """Sinh mẫu Đơn tố giác tội phạm cho vay lãi nặng chuẩn gửi Cơ quan Điều tra Công an Quận/Huyện."""
        police_dept = lender_info.get("police_dept", "Cơ quan Cảnh sát Điều tra Công an Huyện/Quận...")
        return f"""CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc
--------------------

ĐƠN TỐ GIÁC TỘI PHẠM
(V/v: Hành vi Cho vay lãi nặng trong giao dịch dân sự theo Điều 201 Bộ luật Hình sự 2015)

Kính gửi: {police_dept}

TÔI LÀ:
- Họ và tên: {borrower_info.get('full_name', '................................')}
- Năm sinh: {borrower_info.get('birth_year', '..........')} | Số CCCD: {borrower_info.get('cccd', '........................')}
- Nơi cư trú: {borrower_info.get('address', '................................')}
- Số điện thoại liên hệ: {borrower_info.get('phone', '........................')}

TỐ GIÁC HÀNH VI CỦA:
- Họ tên/Tên nhóm đối tượng: {lender_info.get('name', '................................')}
- Số điện thoại/Tài khoản/App: {lender_info.get('contact', '........................')}
- Địa chỉ/Khu vực hoạt động: {lender_info.get('address', '................................')}

NỘI DUNG SỰ VIỆC:
Do hoàn cảnh khó khăn đột xuất, vào ngày ..../..../........, tôi có thỏa thuận vay số tiền trên danh nghĩa là {cls.format_currency(loan_analysis.get('principal_nominal', 0))}.
Tuy nhiên thực tế tôi chỉ nhận được {cls.format_currency(loan_analysis.get('actual_received', 0))} sau khi bị bên cho vay cắt phí giải ngân bất hợp pháp.

Qua tính toán đối chiếu quy định pháp luật:
1. Lãi suất thực tế đối tượng áp dụng lên đến {loan_analysis.get('annualized_percent', 0)}%/năm (gấp {round(loan_analysis.get('annualized_percent', 0)/20, 1)} lần trần 20%/năm theo Điều 468 BLDS 2015, vượt xa mức 100%/năm theo Khoản 1 Điều 201 BLHS).
2. Số tiền lãi và phụ phí trái pháp luật ước tính là: {cls.format_currency(loan_analysis.get('excess_interest_amount', 0))}.
3. Khi tôi không đủ khả năng đóng tiếp mức lãi cắt cổ trên, đối tượng đã có hành vi gọi điện uy hiếp, nhắn tin bôi nhọ danh dự, đe dọa người thân của tôi.

TÀI LIỆU, CHỨNG CỨ KÈM THEO:
1. Bản sao Giấy nợ / Ảnh chụp màn hình ứng dụng vay tiền (Zalo/App/SMS).
2. Lịch sử sao kê chuyển khoản tiền gốc và các lần thanh toán tiền lãi.
3. Bản ghi âm cuộc gọi / tin nhắn đe dọa, khủng bố tinh thần (nếu có).
4. Bản photo CCCD của tôi.

KÍNH ĐỀ NGHỊ:
Kính đề nghị Quý Cơ quan Cảnh sát Điều tra xem xét thụ lý, tiến hành xác minh và xử lý nghiêm minh hành vi cho vay lãi nặng theo đúng quy định tại Điều 201 Bộ luật Hình sự 2015, bảo vệ quyền lợi hợp pháp cho bản thân tôi và gia đình.

Tôi xin cam đoan các thông tin khai báo trên là hoàn toàn đúng sự thật.

........., ngày .... tháng .... năm 20...
NGƯỜI LÀM ĐƠN
(Ký và ghi rõ họ tên)
"""

    @staticmethod
    def format_currency(amount: float) -> str:
        return f"{int(amount):,} VNĐ".replace(",", ".")
