"""
Module: InheritanceDistributionEngine - Máy Tính Phân Chia Di Sản Thừa Kế Dân Gian
Thiết kế riêng cho các gia đình phân chia di sản đất đai, nhà cửa, tránh xung đột tranh chấp.
Căn cứ pháp lý:
- Bộ luật Dân sự 2015:
  + Điều 651: Người thừa kế theo pháp luật (Hàng thừa kế thứ 1, 2, 3).
  + Điều 644: Người thừa kế không phụ thuộc vào nội dung của di chúc (Bảo vệ vợ/chồng, cha mẹ, con chưa thành niên).
  + Điều 658: Thứ tự ưu tiên thanh toán nghĩa vụ tài sản và các chi phí liên quan đến thừa kế.
  + Điều 623: Thời hiệu thừa kế (30 năm đối với bất động sản, 10 năm đối với động sản).
"""

from typing import Dict, Any, List


class InheritanceDistributionEngine:

    @classmethod
    def calculate_statutory_inheritance(
        cls,
        total_estate_value: float,
        funeral_expenses: float = 0.0,
        unpaid_debts: float = 0.0,
        has_spouse: bool = True,
        parents_alive_count: int = 0,
        children_count: int = 2,
        will_estate_given_to_third_party: float = 0.0,
        minor_children_count: int = 0,
        disabled_adult_children_count: int = 0
    ) -> Dict[str, Any]:
        """
        Tính toán chia di sản thừa kế theo pháp luật và bảo vệ suất thừa kế bắt buộc (Điều 644 BLDS 2015).
        - total_estate_value: Tổng giá trị di sản người chết để lại (nhà, đất, tiền gửi...)
        - funeral_expenses: Chi phí mai táng hợp lý (ưu tiên trừ trước theo Điều 658)
        - unpaid_debts: Tiền nợ của người chết phải trả trước khi chia
        - has_spouse: Vợ/chồng của người chết còn sống không
        - parents_alive_count: Số lượng cha/mẹ của người chết còn sống (cha mẹ đẻ + nuôi)
        - children_count: Tổng số con (con đẻ + con nuôi hợp pháp)
        - will_estate_given_to_third_party: Số tiền di chúc đem cho người ngoài / không cho gia đình
        - minor_children_count: Số con chưa thành niên (< 18 tuổi)
        - disabled_adult_children_count: Số con đã thành niên nhưng mất khả năng lao động
        """
        # 1. Di sản thực tế còn lại sau nghĩa vụ tài sản (Điều 658)
        net_estate = max(0.0, total_estate_value - funeral_expenses - unpaid_debts)

        # 2. Xác định Hàng thừa kế thứ nhất (Điều 651)
        heirs_rank_1_count = (1 if has_spouse else 0) + parents_alive_count + children_count
        
        if heirs_rank_1_count <= 0:
            return {
                "error": "Không có người thừa kế hàng thứ nhất. Cần xét sang Hàng thừa kế thứ 2 (Ông bà, anh chị em ruột)."
            }

        # 3. Một suất thừa kế theo pháp luật (nếu không có di chúc)
        legal_share_per_person = net_estate / heirs_rank_1_count

        # 4. Suất bắt buộc không phụ thuộc nội dung di chúc theo Điều 644 BLDS 2015:
        # Bằng 2/3 của một suất thừa kế theo pháp luật
        mandatory_share_2_thirds = (2.0 / 3.0) * legal_share_per_person

        # Số người thuộc diện bảo vệ theo Điều 644:
        # Vợ/chồng + Cha mẹ còn sống + Con chưa thành niên + Con tàn tật mất sức lao động
        protected_beneficiaries_count = (
            (1 if has_spouse else 0) +
            parents_alive_count +
            minor_children_count +
            disabled_adult_children_count
        )

        total_mandatory_protection = protected_beneficiaries_count * mandatory_share_2_thirds

        # Phân tích kịch bản
        distribution_plan = []
        if has_spouse:
            distribution_plan.append({
                "relation": "Vợ / Chồng",
                "count": 1,
                "share_per_person": legal_share_per_person,
                "mandatory_minimum": mandatory_share_2_thirds,
                "note": "Thuộc Hàng 1 & Được bảo vệ 2/3 suất theo Điều 644 kể cả khi di chúc truất quyền!"
            })
        if parents_alive_count > 0:
            distribution_plan.append({
                "relation": "Cha / Mẹ (đẻ hoặc nuôi)",
                "count": parents_alive_count,
                "share_per_person": legal_share_per_person,
                "mandatory_minimum": mandatory_share_2_thirds,
                "note": "Thuộc Hàng 1 & Được bảo vệ 2/3 suất theo Điều 644."
            })
        if children_count > 0:
            distribution_plan.append({
                "relation": "Các Con (đẻ hoặc nuôi)",
                "count": children_count,
                "share_per_person": legal_share_per_person,
                "mandatory_minimum": mandatory_share_2_thirds if (minor_children_count > 0 or disabled_adult_children_count > 0) else 0.0,
                "note": f"Gồm {minor_children_count} con chưa thành niên (được bảo vệ 2/3 suất) và {children_count - minor_children_count} con đã thành niên."
            })

        # Cảnh báo pháp lý di sản
        statute_years = 30  # Bất động sản theo Điều 623
        alerts = [
            f"⏳ THỜI HIỆU YÊU CẦU CHIA DI SẢN: 30 năm đối với Bất động sản (nhà đất) và 10 năm đối với Động sản (tiền, vàng, xe) kể từ thời điểm mở thừa kế (ngày người để lại di sản mất). Quá thời hạn này, di sản thuộc về người đang quản lý!",
            f"📜 BẢO VỆ SUẤT BẮT BUỘC: Nếu người mất lập di chúc cho hết người ngoài hoặc một người duy nhất, thì Vợ/Chồng, Cha Mẹ, Con chưa đủ 18 tuổi VẪN ĐƯƠNG NHIÊN ĐƯỢC HƯỞNG ít nhất {cls.format_currency(mandatory_share_2_thirds)} (2/3 suất theo Điều 644 BLDS).",
            f"🤝 HÒA GIẢI DÒNG HỌ: Nên lập 'Văn bản thỏa thuận phân chia di sản thừa kế' tại Văn phòng Công chứng có mặt đầy đủ các đồng thừa kế để sang tên Sổ đỏ hợp pháp, tránh kiện tụng."
        ]

        return {
            "net_estate_value": net_estate,
            "heirs_rank_1_total": heirs_rank_1_count,
            "legal_share_per_person": round(legal_share_per_person, 0),
            "mandatory_protection_share_2_thirds": round(mandatory_share_2_thirds, 0),
            "distribution_plan": distribution_plan,
            "statute_limitations_years": statute_years,
            "alerts": alerts,
            "formatted_summary": (
                f"Di sản thuần: {cls.format_currency(net_estate)} | "
                f"Chia {heirs_rank_1_count} suất hàng 1: {cls.format_currency(legal_share_per_person)}/suất | "
                f"Suất bảo vệ 2/3: {cls.format_currency(mandatory_share_2_thirds)}"
            )
        }

    @staticmethod
    def format_currency(amount: float) -> str:
        return f"{int(amount):,} VNĐ".replace(",", ".")
