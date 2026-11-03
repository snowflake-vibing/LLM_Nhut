"""
Module: CourtJurisdictionGuide - Hướng Dẫn Thẩm Quyền Tòa Án & Hành Trang Ra Tòa 1 Cửa
Thiết kế riêng cho người dân tránh bị Tòa trả lại đơn (Điều 192 BLTTDS 2015).
Căn cứ pháp lý:
- Bộ luật Tố tụng Dân sự 2015:
  + Điều 35: Thẩm quyền của Tòa án nhân dân cấp huyện.
  + Điều 37: Thẩm quyền của Tòa án nhân dân cấp tỉnh (khi có đương sự/tài sản ở nước ngoài).
  + Điều 39: Thẩm quyền của Tòa án theo lãnh thổ (đất đai, nơi cư trú của bị đơn).
  + Điều 40: Thẩm quyền theo sự lựa chọn của người khởi kiện.
- Luật Đất đai 2013 / 2024 (Điều 202, 203 / Điều 236): Bắt buộc hòa giải tại UBND cấp xã với tranh chấp ai là người có quyền sử dụng đất.
- Luật Hôn nhân & Gia đình 2014: Thẩm quyền vụ việc thuận tình & đơn phương ly hôn.
"""

from typing import Dict, Any, List


class CourtJurisdictionGuide:
    # Bản đồ mẫu một số TAND cấp huyện trọng điểm và Chi cục THADS
    DISTRICT_COURTS_DB = {
        "HỒ CHÍ MINH": {
            "QUẬN 1": {
                "court_name": "Tòa án nhân dân Quận 1, TP. Hồ Chí Minh",
                "court_address": "Số 136 đường Lê Thị Hồng Gấm, Phường Nguyễn Thái Bình, Quận 1, TP.HCM",
                "court_phone": "028 3829 7467",
                "thads_name": "Chi cục Thi hành án dân sự Quận 1",
                "thads_address": "Số 138 Lê Thị Hồng Gấm, Phường Nguyễn Thái Bình, Quận 1, TP.HCM"
            },
            "QUẬN BÌNH THẠNH": {
                "court_name": "Tòa án nhân dân Quận Bình Thạnh, TP. Hồ Chí Minh",
                "court_address": "Số 457 đường Phan Chu Trinh, Phường 12, Quận Bình Thạnh, TP.HCM",
                "court_phone": "028 3841 2307",
                "thads_name": "Chi cục Thi hành án dân sự Quận Bình Thạnh",
                "thads_address": "Số 20/4 đường Phan Đăng Lưu, Phường 14, Quận Bình Thạnh, TP.HCM"
            },
            "THÀNH PHỐ THỦ ĐỨC": {
                "court_name": "Tòa án nhân dân Thành phố Thủ Đức, TP. Hồ Chí Minh",
                "court_address": "Số 1400 đường Đồng Văn Cống, Phường Thạnh Mỹ Lợi, TP. Thủ Đức, TP.HCM",
                "court_phone": "028 3740 6848",
                "thads_name": "Chi cục Thi hành án dân sự TP. Thủ Đức",
                "thads_address": "Số 1402 Đồng Văn Cống, Phường Thạnh Mỹ Lợi, TP. Thủ Đức, TP.HCM"
            },
            "HUYỆN BÌNH CHÁNH": {
                "court_name": "Tòa án nhân dân Huyện Bình Chánh, TP. Hồ Chí Minh",
                "court_address": "Số 398 đường Tân Túc, Thị trấn Tân Túc, Huyện Bình Chánh, TP.HCM",
                "court_phone": "028 3760 0340",
                "thads_name": "Chi cục Thi hành án dân sự Huyện Bình Chánh",
                "thads_address": "Đường số 6, Khu Trung tâm Hành chính Bình Chánh, Thị trấn Tân Túc, TP.HCM"
            }
        },
        "HÀ NỘI": {
            "QUẬN HOÀN KIẾM": {
                "court_name": "Tòa án nhân dân Quận Hoàn Kiếm, TP. Hà Nội",
                "court_address": "Số 41 phố Hai Bà Trưng, Phường Tràng Tiền, Quận Hoàn Kiếm, Hà Nội",
                "court_phone": "024 3825 3694",
                "thads_name": "Chi cục Thi hành án dân sự Quận Hoàn Kiếm",
                "thads_address": "Số 41 Hai Bà Trưng, Quận Hoàn Kiếm, Hà Nội"
            },
            "QUẬN CẦU GIẤY": {
                "court_name": "Tòa án nhân dân Cầu Giấy, TP. Hà Nội",
                "court_address": "Phố Tôn Thất Thuyết, Phường Dịch Vọng Hậu, Quận Cầu Giấy, Hà Nội",
                "court_phone": "024 3795 0321",
                "thads_name": "Chi cục Thi hành án dân sự Quận Cầu Giấy",
                "thads_address": "Khu đô thị Dịch Vọng, Phường Dịch Vọng, Cầu Giấy, Hà Nội"
            },
            "QUẬN ĐỐNG ĐA": {
                "court_name": "Tòa án nhân dân Quận Đống Đa, TP. Hà Nội",
                "court_address": "Số 58 phố Đào Duy Anh, Phường Phương Mai, Quận Đống Đa, Hà Nội",
                "court_phone": "024 3577 0212",
                "thads_name": "Chi cục Thi hành án dân sự Quận Đống Đa",
                "thads_address": "Số 59 phố Hoàng Cầu, Phường Ô Chợ Dừa, Đống Đa, Hà Nội"
            }
        },
        "ĐÀ NẴNG": {
            "QUẬN HẢI CHÂU": {
                "court_name": "Tòa án nhân dân Quận Hải Châu, TP. Đà Nẵng",
                "court_address": "Số 48 đường Trần Phú, Phường Hải Châu 1, Quận Hải Châu, Đà Nẵng",
                "court_phone": "0236 382 1215",
                "thads_name": "Chi cục Thi hành án dân sự Quận Hải Châu",
                "thads_address": "Số 106 đường 3 Tháng 2, Phường Thuận Phước, Hải Châu, Đà Nẵng"
            }
        }
    }

    DISPUTE_CATEGORIES = {
        "LAND_DISPUTE": {
            "title": "Tranh chấp Quyền sử dụng đất & Ranh giới bất động sản",
            "jurisdiction_rule": "BẮT BUỘC nộp tại TAND nơi CÓ BẤT ĐỘNG SẢN (Điểm c Khoản 1 Điều 39 BLTTDS 2015). Không phụ thuộc nơi bị đơn ở.",
            "mandatory_pre_litigation": True,
            "pre_litigation_notice": "BẮT BUỘC phải qua thủ tục Hòa giải tại UBND xã/phường nơi có đất. Không có biên bản này, Tòa án sẽ TRẢ LẠI ĐƠN NGAY!",
            "required_dossier": [
                "Đơn khởi kiện chuẩn Mẫu số 23-DS (bản chính).",
                "Biên bản hòa giải tranh chấp đất đai tại UBND cấp xã (kết luận hòa giải không thành) - Bản chính.",
                "Bản sao y công chứng Giấy chứng nhận QSDĐ (Sổ đỏ/sổ hồng) hoặc các giấy tờ theo Điều 100/137 Luật Đất đai.",
                "Trích lục bản đồ địa chính / Sơ đồ hiện trạng vị trí thửa đất tranh chấp.",
                "Bản sao y CCCD/Hộ chiếu của người khởi kiện.",
                "Tài liệu chứng minh nơi cư trú của người bị kiện (xác nhận thông tin cư trú CT07/CT08 do Công an cấp)."
            ]
        },
        "DIVORCE_UNILATERAL": {
            "title": "Ly hôn Đơn phương (Một bên yêu cầu ly hôn)",
            "jurisdiction_rule": "Nộp tại TAND cấp Huyện nơi BỊ ĐƠN (vợ hoặc chồng bị yêu cầu ly hôn) đang cư trú hoặc làm việc (Điểm a Khoản 1 Điều 39 BLTTDS 2015).",
            "mandatory_pre_litigation": False,
            "pre_litigation_notice": "Không bắt buộc hòa giải cơ sở tại tổ dân phố. Tòa án sẽ tự tổ chức hòa giải sau khi thụ lý.",
            "required_dossier": [
                "Đơn khởi kiện ly hôn (bản chính).",
                "Giấy chứng nhận đăng ký kết hôn (Bản gốc hoặc bản trích lục kết hôn).",
                "Bản sao y công chứng Giấy khai sinh của các con chung.",
                "Bản sao y CCCD của cả hai vợ chồng.",
                "Giấy xác nhận thông tin nơi cư trú của người bị kiện (Mẫu CT07 Công an xã/phường).",
                "Giấy tờ chứng minh tài sản chung / nợ chung (Sổ đỏ, cavet xe, sổ tiết kiệm...) nếu có yêu cầu chia tài sản."
            ]
        },
        "DIVORCE_MUTUAL": {
            "title": "Thuận tình Ly hôn (Cả hai vợ chồng đồng thuận)",
            "jurisdiction_rule": "Hai vợ chồng có quyền LỰA CHỌN nộp tại TAND nơi cư trú/làm việc của người vợ HOẶC người chồng (Điểm h Khoản 2 Điều 39 BLTTDS 2015).",
            "mandatory_pre_litigation": False,
            "pre_litigation_notice": "Thủ tục giải quyết Việc dân sự (nhanh hơn khởi kiện vụ án). Cả 2 cùng ký đơn.",
            "required_dossier": [
                "Đơn yêu cầu công nhận thuận tình ly hôn (cả 2 vợ chồng cùng ký tên).",
                "Giấy chứng nhận đăng ký kết hôn (Bản gốc).",
                "Bản sao y Giấy khai sinh của các con chung.",
                "Bản sao y CCCD của hai vợ chồng.",
                "Văn bản thỏa thuận phân chia tài sản và mức cấp dưỡng nuôi con (nếu có)."
            ]
        },
        "DEBT_CONTRACT": {
            "title": "Đòi nợ vay tiền / Tranh chấp Hợp đồng dân sự",
            "jurisdiction_rule": "Nộp tại TAND cấp Huyện nơi BỊ ĐƠN cư trú/làm việc. Nếu trong hợp đồng có thỏa thuận bằng văn bản chọn Tòa nơi người cho vay cư trú thì được nộp tại Tòa của người cho vay.",
            "mandatory_pre_litigation": False,
            "pre_litigation_notice": "Không bắt buộc hòa giải tại xã. Khuyến khích lập Vi bằng ghi nhận tin nhắn khất nợ trước khi kiện.",
            "required_dossier": [
                "Đơn khởi kiện Mẫu số 23-DS (bản chính).",
                "Hợp đồng vay tiền / Giấy mượn tiền viết tay / Ảnh chụp thỏa thuận vay (bản chính hoặc sao y).",
                "Sao kê tài khoản ngân hàng chứng minh đã chuyển tiền giải ngân.",
                "Tin nhắn SMS/Zalo, băng ghi âm thừa nhận nợ hoặc khất nợ (nên lập Vi bằng Thừa phát lại).",
                "Bản sao y CCCD người khởi kiện và giấy tờ cư trú của người vay tiền."
            ]
        },
        "LABOR_WRONGFUL_TERMINATION": {
            "title": "Tranh chấp Lao động (Bị công ty sa thải trái luật / nợ lương)",
            "jurisdiction_rule": "Người lao động được QUYỀN LỰA CHỌN nộp tại TAND nơi công ty đặt trụ sở HOẶC TAND nơi mình trực tiếp làm việc (Điều 40 BLTTDS 2015).",
            "mandatory_pre_litigation": False,
            "pre_litigation_notice": "Tranh chấp sa thải, đơn phương chấm dứt HĐLĐ KHÔNG BẮT BUỘC qua Hòa giải viên lao động (Điều 188 Bộ luật Lao động 2019).",
            "required_dossier": [
                "Đơn khởi kiện lao động (bản chính).",
                "Hợp đồng lao động, phụ lục hợp đồng (bản chính hoặc sao y).",
                "Quyết định sa thải / Quyết định chấm dứt HĐLĐ của công ty.",
                "Bảng lương, sao kê ngân hàng nhận lương 06 tháng gần nhất.",
                "Bản sao y CCCD của người lao động."
            ]
        }
    }

    @classmethod
    def resolve_jurisdiction_and_checklist(
        cls,
        dispute_type: str,
        province: str,
        district: str,
        has_foreign_element: bool = False
    ) -> Dict[str, Any]:
        """
        Tra cứu chính xác Tòa án thụ lý, các lưu ý thủ tục và checklist giấy tờ cần mang.
        """
        norm_dispute = dispute_type.upper().strip()
        if norm_dispute not in cls.DISPUTE_CATEGORIES:
            norm_dispute = "DEBT_CONTRACT"

        dispute_meta = cls.DISPUTE_CATEGORIES[norm_dispute]

        # Kiểm tra thẩm quyền Tỉnh hay Huyện (Điều 35 vs Điều 37 BLTTDS)
        prov_upper = province.upper().strip()
        dist_upper = district.upper().strip()

        if has_foreign_element:
            court_level = "PROVINCIAL"
            target_court_name = f"Tòa án nhân dân tỉnh/thành phố {province} (Cấp Tỉnh thụ lý do có đương sự/tài sản ở nước ngoài)"
            target_court_address = f"Trụ sở TAND Cấp Tỉnh tại {province}"
            target_thads_name = f"Cục Thi hành án dân sự tỉnh/thành phố {province}"
            target_thads_address = f"Cục THADS tỉnh {province}"
            phone = "Tra cứu tổng đài TAND Cấp Tỉnh"
        else:
            court_level = "DISTRICT"
            dist_data = cls.DISTRICT_COURTS_DB.get(prov_upper, {}).get(dist_upper)
            if dist_data:
                target_court_name = dist_data["court_name"]
                target_court_address = dist_data["court_address"]
                target_thads_name = dist_data["thads_name"]
                target_thads_address = dist_data["thads_address"]
                phone = dist_data["court_phone"]
            else:
                target_court_name = f"Tòa án nhân dân {district}, tỉnh/thành phố {province}"
                target_court_address = f"Bộ phận Tiếp nhận & Xử lý đơn (Một cửa) - TAND {district}, {province}"
                target_thads_name = f"Chi cục Thi hành án dân sự {district}, {province}"
                target_thads_address = f"Chi cục THADS {district}, {province}"
                phone = "Bộ phận Một cửa TAND cấp Huyện"

        # Quy trình 4 bước hành động cho người dân
        action_steps = [
            f"Bước 1: Chuẩn bị đủ {len(dispute_meta['required_dossier'])} loại giấy tờ trong Checklist bên dưới (gồm bản chính để đối chiếu và ít nhất 02 bản sao y công chứng).",
            f"Bước 2: Mang toàn bộ hồ sơ đến nộp trực tiếp tại BỘ PHẬN TIẾP NHẬN ĐƠN (Một cửa) của: {target_court_name}. Yêu cầu nhận Giấy xác nhận đã nhận đơn khởi kiện.",
            f"Bước 3: Trong thời hạn 08 ngày làm việc, nhận Thông báo nộp tiền tạm ứng án phí từ Tòa án (nếu đơn hợp lệ).",
            f"Bước 4: Cầm Thông báo sang {target_thads_name} để nộp tiền tạm ứng án phí, sau đó nộp lại Biên lai cho Tòa án để chính thức thụ lý vụ án."
        ]

        return {
            "dispute_title": dispute_meta["title"],
            "jurisdiction_rule": dispute_meta["jurisdiction_rule"],
            "mandatory_pre_litigation": dispute_meta["mandatory_pre_litigation"],
            "pre_litigation_notice": dispute_meta["pre_litigation_notice"],
            "target_court_name": target_court_name,
            "target_court_address": target_court_address,
            "target_court_phone": phone,
            "target_thads_name": target_thads_name,
            "target_thads_address": target_thads_address,
            "required_dossier": dispute_meta["required_dossier"],
            "action_steps": action_steps,
            "formatted_summary": (
                f"Tòa thụ lý: {target_court_name} | Địa chỉ: {target_court_address} | "
                f"Hồ sơ cần: {len(dispute_meta['required_dossier'])} loại giấy tờ"
            )
        }
