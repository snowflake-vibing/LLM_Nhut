"""
Module: DivorceSettlementCalculator - Máy Tính Chia Tài Sản & Bảo Vệ Quyền Nuôi Con Khi Ly Hôn
Thiết kế riêng cho các cặp vợ chồng, đặc biệt bảo vệ người vợ ở nhà nội trợ và quyền lợi trẻ em.
Căn cứ pháp lý:
- Luật Hôn nhân và Gia đình 2014:
  + Điều 33, 43: Tài sản chung và Tài sản riêng của vợ chồng.
  + Điều 59: Nguyên tắc giải quyết tài sản của vợ chồng khi ly hôn.
    (Khoản 2: "Công việc của vợ, chồng trong gia đình được coi như lao động có thu nhập").
  + Điều 81: Việc trông nom, chăm sóc, nuôi dưỡng, giáo dục con sau khi ly hôn.
    (Khoản 3: Con dưới 36 tháng tuổi được giao cho mẹ trực tiếp nuôi).
    (Khoản 2: Con từ đủ 07 tuổi trở lên phải xem xét nguyện vọng của con).
  + Điều 82, 116: Nghĩa vụ và mức cấp dưỡng nuôi con.
"""

from typing import Dict, Any, List


class DivorceSettlementCalculator:
    # Mức lương cơ sở hiện hành tham chiếu (2.340.000 VNĐ/tháng từ 01/07/2024 theo NĐ 73/2024/NĐ-CP)
    BASE_SALARY_VND = 2_340_000

    @classmethod
    def calculate_settlement(
        cls,
        husband_separate_assets: float,
        wife_separate_assets: float,
        common_assets_value: float,
        common_debts_value: float,
        wife_is_homemaker: bool = True,
        children: List[Dict[str, Any]] = None,
        non_custodial_parent_income: float = 15_000_000
    ) -> Dict[str, Any]:
        """
        Phân định tài sản và nghĩa vụ nuôi con khi ly hôn:
        - husband_separate_assets: Tài sản riêng của chồng (có trước hôn nhân hoặc tặng cho riêng)
        - wife_separate_assets: Tài sản riêng của vợ
        - common_assets_value: Tổng tài sản chung tích lũy trong thời kỳ hôn nhân
        - common_debts_value: Tổng nợ chung của vợ chồng
        - wife_is_homemaker: Người vợ có phải làm nội trợ/ở nhà chăm con không
        - children: Danh sách con [{"name": "Bé A", "age_months": 24}, {"name": "Bé B", "age_months": 96}]
        - non_custodial_parent_income: Thu nhập hàng tháng của người không trực tiếp nuôi con
        """
        if children is None:
            children = []

        # 1. Phân chia Tài sản
        # Giá trị tài sản chung thuần túy sau khi trừ nợ
        net_common_assets = max(0.0, common_assets_value - common_debts_value)
        
        # Nguyên tắc Điều 59: Chia đôi có tính công sức
        # Điểm mấu chốt: Người nội trợ được tính như lao động tạo ra thu nhập tương đương
        husband_common_share = net_common_assets / 2.0
        wife_common_share = net_common_assets / 2.0

        husband_total_received = husband_separate_assets + husband_common_share
        wife_total_received = wife_separate_assets + wife_common_share

        # 2. Quyền trực tiếp nuôi con (Điều 81)
        custody_analysis = []
        for child in children:
            name = child.get("name", "Con chung")
            age_months = child.get("age_months", 36)
            age_years = age_months / 12.0

            if age_months < 36:
                rule = "ƯU TIÊN GIAO CHO MẸ NUÔI (Điều 81.3 Luật HNGĐ)"
                explanation = (
                    f"{name} hiện {age_months} tháng tuổi (< 36 tháng). Theo luật, Tòa án mặc định giao cho Mẹ "
                    f"trực tiếp nuôi dưỡng, trừ khi người mẹ không đủ điều kiện hoặc hai bên có thỏa thuận khác."
                )
                recommended_custodian = "Người Mẹ"
            elif age_years >= 7:
                rule = "BẮT BUỘC LẤY Ý KIẾN NGUYỆN VỌNG CỦA CON (Điều 81.2 Luật HNGĐ)"
                explanation = (
                    f"{name} hiện {int(age_years)} tuổi (>= 7 tuổi). Tòa án sẽ phát phiếu nguyện vọng "
                    f"để con tự bày tỏ muốn ở với Bố hay Mẹ. Tòa án tôn trọng ý kiến của cháu."
                )
                recommended_custodian = "Theo nguyện vọng của con và điều kiện kinh tế"
            else:
                rule = "XEM XÉT ĐIỀU KIỆN MỌI MẶT CỦA BỐ VÀ MẸ (Điều 81.2 Luật HNGĐ)"
                explanation = (
                    f"{name} hiện {int(age_years)} tuổi (từ 3 đến dưới 7 tuổi). Bên nào chứng minh được "
                    f"môi trường sống, thời gian chăm sóc và điều kiện học tập tốt hơn cho bé sẽ được ưu tiên."
                )
                recommended_custodian = "Thỏa thuận hoặc Tòa quyết định theo lợi ích tốt nhất của trẻ"

            custody_analysis.append({
                "child_name": name,
                "age_display": f"{int(age_years)} tuổi ({age_months} tháng)",
                "rule": rule,
                "explanation": explanation,
                "recommended_custodian": recommended_custodian
            })

        # 3. Mức cấp dưỡng nuôi con (Điều 82, 116)
        # Thực tiễn xét xử: 20% - 30% thu nhập hàng tháng, hoặc tối thiểu 50% lương cơ sở (1.170.000 VNĐ)
        num_children = len(children)
        if num_children > 0:
            if non_custodial_parent_income > 0:
                # 25% thu nhập cho 1 con, hoặc 40% cho 2 con
                rate = 0.25 if num_children == 1 else (0.40 if num_children == 2 else 0.50)
                monthly_support_total = max(
                    cls.BASE_SALARY_VND * 0.5 * num_children,
                    non_custodial_parent_income * rate
                )
            else:
                monthly_support_total = cls.BASE_SALARY_VND * 0.5 * num_children
            monthly_support_per_child = monthly_support_total / num_children
        else:
            monthly_support_total = 0.0
            monthly_support_per_child = 0.0

        # Lời khuyên vàng dân sinh
        legal_advice = [
            "⚖️ ĐIỀU QUAN TRỌNG: Nếu một bên ở nhà làm nội trợ, pháp luật coi công sức đó ngang bằng người đi làm kiếm tiền (Khoản 2 Điều 59). Tuyệt đối không có chuyện 'ở nhà nuôi con là ra đi tay trắng'!",
            "🏠 TÀI SẢN RIÊNG: Đất đai/tiền bạc do bố mẹ tặng cho riêng trước khi cưới hoặc lập văn bản tặng cho riêng trong thời kỳ hôn nhân là tài sản riêng 100%, không bị chia đôi.",
            "👶 NGUYÊN TẮC VÌ TRẺ EM: Việc giành quyền nuôi con dựa trên 'Lợi ích tốt nhất về mọi mặt của trẻ', không phải ai giàu hơn là đương nhiên được nuôi.",
            "🤝 KHUYẾN NGHỊ: Nếu thuận tình ly hôn và tự thỏa thuận được phân chia tài sản, thủ tục sẽ xong trong vòng 1-2 tháng, án phí chỉ 300.000 VNĐ."
        ]

        return {
            "net_common_assets": net_common_assets,
            "husband_share_common": husband_common_share,
            "wife_share_common": wife_common_share,
            "husband_total_assets": husband_total_received,
            "wife_total_received": wife_total_received,
            "wife_homemaker_protected": wife_is_homemaker,
            "custody_analysis": custody_analysis,
            "monthly_child_support_per_child": round(monthly_support_per_child, 0),
            "monthly_child_support_total": round(monthly_support_total, 0),
            "legal_advice": legal_advice,
            "formatted_summary": (
                f"Tài sản chung chia đôi: {cls.format_currency(wife_common_share)}/người | "
                f"Cấp dưỡng nuôi con khuyến nghị: {cls.format_currency(monthly_support_per_child)}/tháng/cháu"
            )
        }

    @staticmethod
    def format_currency(amount: float) -> str:
        return f"{int(amount):,} VNĐ".replace(",", ".")
