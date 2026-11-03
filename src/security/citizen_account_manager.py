"""
Module: CitizenAccountManager - Hệ Thống Tài Khoản Công Dân & Đăng Nhập Nhanh Demo 1-Chạm
Quản lý hồ sơ cá nhân người dân, lịch sử tư vấn, và các persona demo thực chiến đời sống.
"""

import os
import json
import datetime
from typing import Dict, Any, List, Optional

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ACCOUNTS_FILE = os.path.join(ROOT_DIR, "data", "citizen_profiles.json")


class CitizenAccountManager:
    """Quản lý thông tin tài khoản người dùng và các tài khoản demo mẫu."""

    # 4 Tài Khoản Demo Đại Diện Cho 4 Nhóm Đối Tượng Dân Sinh Đời Thực
    DEMO_PERSONAS = {
        "bac_ba": {
            "id": "DEMO_BAC_BA",
            "name": "Bác Ba (Nông dân - Tiền Giang)",
            "avatar": "🧑‍🌾",
            "phone": "0918xxxxxx",
            "category": "🏡 Tranh chấp Đất đai & Lối đi",
            "description": "Bị hàng xóm xây tường lấn 1.5m ranh giới đất nông nghiệp và bít lối đi chung đã sử dụng 20 năm.",
            "initial_prompt": "Chào Luật sư, tôi là nông dân ở Tiền Giang. Nhà hàng xóm mới xây tường lấn sang phần đất vườn nhà tôi 1.5 mét và còn rào bít cả lối đi chung của xóm. Tôi có Sổ đỏ cấp năm 2003. Tôi phải làm gì trước, có cần ra xã hòa giải không?",
            "case_data": {
                "dispute_type": "LAND_DISPUTE",
                "province": "Tiền Giang",
                "district": "Huyện Châu Thành",
                "has_certificate": True,
                "urgency": "Cao (Đang xây tường)"
            }
        },
        "chi_lan": {
            "id": "DEMO_CHI_LAN",
            "name": "Chị Lan (Công nhân may - Bình Dương)",
            "avatar": "👩‍🏭",
            "phone": "0987xxxxxx",
            "category": "🛑 Bẫy Tín Dụng Đen & Nợ Lương",
            "description": "Vay qua app nóng 20 triệu nhưng thực nhận 16 triệu, lãi 400k/ngày, bị gọi điện đe dọa người thân.",
            "initial_prompt": "Luật sư cứu em với! Em là công nhân ở KCN Sóng Thần. Do con ốm em lỡ vay qua app online 20 triệu nhưng họ chỉ chuyển 16 triệu, bắt mỗi ngày đóng 400.000 tiền lãi. Nay em không đủ tiền đóng thì họ gọi điện đe dọa con em, dọa gửi ảnh bôi nhọ lên Zalo. Mức lãi này có vi phạm hình sự không và em phải làm đơn gửi ai?",
            "case_data": {
                "dispute_type": "USURY_LOAN",
                "principal": 20000000,
                "actual_received": 16000000,
                "daily_fee": 400000,
                "severity": "CRIMINAL_ALERT"
            }
        },
        "anh_hoang": {
            "id": "DEMO_ANH_HOANG",
            "name": "Anh Hoàng (Nhân viên văn phòng - Hà Nội)",
            "avatar": "👨‍💼",
            "phone": "0904xxxxxx",
            "category": "💔 Ly Hôn & Quyền Nuôi Con",
            "description": "Hai vợ chồng đồng thuận ly hôn, có 1 căn chung cư 2.4 tỷ và bé gái 22 tháng tuổi.",
            "initial_prompt": "Chào Luật sư, vợ chồng tôi tính cách không hòa hợp nên muốn thuận tình ly hôn văn minh. Chúng tôi có một căn chung cư mua chung trị giá 2.4 tỷ (còn nợ ngân hàng 300 triệu) và 1 bé gái 22 tháng tuổi. Vợ tôi làm nội trợ ở nhà. Luật sư hướng dẫn giúp tôi cách thỏa thuận phân chia tài sản và quyền nuôi con theo đúng luật để thủ tục Tòa án nhanh nhất.",
            "case_data": {
                "dispute_type": "DIVORCE_MUTUAL",
                "common_asset": 2400000000,
                "common_debt": 300000000,
                "child_age_months": 22
            }
        },
        "cu_sau": {
            "id": "DEMO_CU_SAU",
            "name": "Cụ Sáu (Cán bộ hưu trí 72 tuổi - Đà Nẵng)",
            "avatar": "👴",
            "phone": "0935xxxxxx",
            "category": "📜 Thừa Kế Đất Hương Hỏa",
            "description": "Cha mẹ mất không để lại di chúc, để lại thửa đất 300m2 cho 4 anh em phân chia.",
            "initial_prompt": "Kính chào Luật sư, tôi năm nay 72 tuổi ở Đà Nẵng. Cha mẹ tôi mất cách đây 5 năm không để lại di chúc, có để lại thửa đất hương hỏa 300m2 (trị giá khoảng 3 tỷ đồng). Gia đình có 4 anh em ruột. Nay một người em đòi bán hết chia tiền nhưng tôi muốn giữ lại làm nhà thờ họ. Xin hỏi luật pháp quy định phân chia di sản hàng thứ nhất này như thế nào?",
            "case_data": {
                "dispute_type": "INHERITANCE_LAND",
                "estate_value": 3000000000,
                "heirs_count": 4
            }
        }
    }

    def __init__(self):
        self._ensure_storage()

    def _ensure_storage(self):
        os.makedirs(os.path.dirname(ACCOUNTS_FILE), exist_ok=True)
        if not os.path.exists(ACCOUNTS_FILE):
            with open(ACCOUNTS_FILE, "w", encoding="utf-8") as f:
                json.dump({}, f, ensure_ascii=False, indent=2)

    def load_accounts(self) -> Dict[str, Any]:
        try:
            with open(ACCOUNTS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def save_account(self, user_id: str, name: str, phone: str = "", note: str = "") -> Dict[str, Any]:
        accounts = self.load_accounts()
        acc = {
            "id": user_id,
            "name": name,
            "phone": phone,
            "note": note,
            "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "is_demo": False
        }
        accounts[user_id] = acc
        try:
            with open(ACCOUNTS_FILE, "w", encoding="utf-8") as f:
                json.dump(accounts, f, ensure_ascii=False, indent=2)
        except Exception:
            pass
        return acc

    @classmethod
    def get_demo_persona(cls, persona_key: str) -> Optional[Dict[str, Any]]:
        return cls.DEMO_PERSONAS.get(persona_key)

    @classmethod
    def get_default_guest(cls) -> Dict[str, Any]:
        return {
            "id": "GUEST_CITIZEN",
            "name": "Công Dân Vãng Lai",
            "avatar": "👤",
            "phone": "Chưa đăng ký",
            "category": "Cá nhân & Dân sự",
            "is_demo": False
        }
