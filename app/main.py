"""
LegalTech Platform - Streamlit Application - Version 3.0 (Citizen-Centric Workstation)
Thiết kế tinh gọn cho Cá nhân & Người dân:
- 👤 Cấp Account Riêng & Nút Vào Nhanh Demo 1-Chạm (4 Personas Đời Thực: Bác Ba, Chị Lan, Anh Hoàng, Cụ Sáu)
- 📖 Interactive Onboarding Tutorial Cho Người Mới Bắt Đầu (Hướng dẫn 4 bước trực quan)
- 💬 Khung Chat Tinh Gọn: Xóa sạch toàn bộ nút test kỹ thuật thừa thãi, chỉ giữ hội thoại ân cần và tình huống dân sinh
- 🧮 Hộp Công Cụ Dân Sinh 1-Chạm (10 Tiện ích độc lập tách riêng tại Tab 2)
"""

import os
import sys
import json
import math
import pandas as pd
import streamlit as st

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from llm_provider.model_factory import ModelFactory, ProviderType
from src.agents import LegalMultiAgentWorkflow
from src.database import DatabaseManager
from src.security import (
    PIIMasker,
    PromptInjectionGuard,
    EphemeralPrivacyManager,
    CitizenAccountManager,
    OnboardingTutorial,
)
from src.tools.web_search_tool import hybrid_industry_search
from src.tools.contract_scanner import ContractVulnerabilityScanner
from src.tools.social_cases_knowledge import SocialCasesKnowledgeEngine, SOCIAL_CASES_DATA
from src.tools.evidence_vault_engine import EvidenceVaultEngine, EVIDENCE_CATALOG
from src.tools.plain_language_engine import PlainLanguageEngine
from src.tools.emotional_rant_parser import EmotionalRantParser
from src.tools.citizen_legal_tools import CitizenLegalTools
from src.tools.multimodal_evidence_parser import MultimodalEvidenceParser
from src.tools.instant_petition_generator import InstantPetitionGenerator
from src.tools.litigation_simulator import LegalLitigationSimulator
from src.tools.voice_narrator import VoiceNarrator
from src.tools.litigation_dossier_generator import LitigationDossierGenerator
from src.tools.citizen_wizard import CitizenDiagnosticFunnel
from src.tools.plain_legal_glossary import PlainLegalGlossary
from src.tools.usury_trap_detector import UsuryTrapDetector
from src.tools.court_jurisdiction_guide import CourtJurisdictionGuide
from src.tools.divorce_settlement_calculator import DivorceSettlementCalculator
from src.tools.inheritance_distribution_engine import InheritanceDistributionEngine
from src.agents.holistic_evaluator import HolisticAuditEngine
from src.agents.citizen_intake_agent import CitizenIntakeAgent
from src.agents.memory_store import LegalMemoryStore
from src.dossier import DynamicLegalDrafter

# Cấu hình giao diện Streamlit
st.set_page_config(
    page_title="LegalTech Platform - Trợ Lý Luật Sư Dân Gian v3.0",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== PHONG CÁCH GIAO DIỆN CHUYÊN NGHIỆP (360 SOFTWARE HOUSE STANDARDS) ====================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

/* Hero Section Banner */
.pro-hero-banner {
    background: linear-gradient(135deg, #0B192C 0%, #1E3E62 60%, #000000 100%);
    color: #FFFFFF;
    padding: 2.2rem 2.4rem;
    border-radius: 18px;
    margin-bottom: 1.5rem;
    box-shadow: 0 10px 25px -5px rgba(11, 25, 44, 0.3), 0 8px 10px -6px rgba(11, 25, 44, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.12);
}

.pro-badge {
    display: inline-block;
    background: rgba(59, 130, 246, 0.25);
    border: 1px solid rgba(96, 165, 250, 0.5);
    color: #93C5FD;
    padding: 0.35rem 0.85rem;
    border-radius: 9999px;
    font-size: 0.82rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
}

.pro-title {
    font-size: 2.1rem;
    font-weight: 800;
    line-height: 1.25;
    margin-bottom: 0.6rem;
    color: #FFFFFF;
}

.pro-subtitle {
    font-size: 1.05rem;
    color: #CBD5E1;
    line-height: 1.6;
    max-width: 950px;
    margin-bottom: 1.2rem;
}

.trust-badge-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.6rem;
    margin-top: 0.8rem;
}

.trust-badge {
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.15);
    color: #E2E8F0;
    padding: 0.35rem 0.8rem;
    border-radius: 8px;
    font-size: 0.85rem;
    font-weight: 600;
}

/* 3 Trụ Cột Giá Trị Cốt Lõi */
.pillar-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    padding: 1.2rem;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
    height: 100%;
}

/* Tabs Styling Hiện Đại */
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
    background-color: #F1F5F9;
    padding: 6px;
    border-radius: 12px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: 600;
    color: #475569;
    background-color: transparent;
    transition: all 0.2s ease;
}

.stTabs [aria-selected="true"] {
    background-color: #FFFFFF !important;
    color: #1E3E62 !important;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.06);
}

/* Chân Trang Chuyên Nghiệp */
.pro-footer-container {
    margin-top: 3.5rem;
    padding: 2rem 1.5rem 1rem 1.5rem;
    border-top: 1px solid #E2E8F0;
    background: #F8FAFC;
    border-radius: 14px;
    color: #64748B;
    font-size: 0.88rem;
    line-height: 1.7;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)


# ==================== KHỞI TẠO TRẠNG THÁI SESSION ====================
if "account_mgr" not in st.session_state:
    st.session_state.account_mgr = CitizenAccountManager()

if "current_user" not in st.session_state:
    st.session_state.current_user = CitizenAccountManager.get_default_guest()

if "show_tutorial" not in st.session_state:
    st.session_state.show_tutorial = True

if "factory" not in st.session_state:
    st.session_state.factory = ModelFactory()

if "workflow" not in st.session_state:
    st.session_state.workflow = LegalMultiAgentWorkflow(st.session_state.factory)

if "db_manager" not in st.session_state:
    st.session_state.db_manager = DatabaseManager()

if "contract_scanner" not in st.session_state:
    st.session_state.contract_scanner = ContractVulnerabilityScanner(st.session_state.factory)

if "dynamic_drafter" not in st.session_state:
    st.session_state.dynamic_drafter = DynamicLegalDrafter(st.session_state.factory)

if "memory_store" not in st.session_state:
    st.session_state.memory_store = LegalMemoryStore()

if "plain_engine" not in st.session_state:
    st.session_state.plain_engine = PlainLanguageEngine(st.session_state.factory)

if "rant_parser" not in st.session_state:
    st.session_state.rant_parser = EmotionalRantParser(st.session_state.factory)

if "citizen_intake" not in st.session_state:
    st.session_state.citizen_intake = CitizenIntakeAgent(st.session_state.factory)

if "evidence_parser" not in st.session_state:
    st.session_state.evidence_parser = MultimodalEvidenceParser(st.session_state.factory)

if "messages" not in st.session_state:
    user_name = st.session_state.current_user.get("name", "Bạn")
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                f"👋 **Kính chào {user_name}! Tôi là Luật sư Dân gian Đồng hành (LegalTech Platform v3.0).**\n\n"
                "Tôi ở đây để **lắng nghe, hỏi thăm từng bước và bảo vệ quyền lợi hợp pháp** cho bạn trong các vấn đề đời sống:\n"
                "- 🏡 **Đất đai & Ranh giới:** Hàng xóm lấn chiếm đất, bít lối đi chung, sổ đỏ thừa kế.\n"
                "- 🛑 **Vay mượn & Bẫy tín dụng đen:** Vay app nóng, bị đe dọa, nợ khó đòi, tính lãi vượt trần 20%/năm.\n"
                "- 💔 **Hôn nhân & Gia đình:** Thuận tình ly hôn, công sức nội trợ của người vợ, quyền nuôi con nhỏ.\n"
                "- 📜 **Di sản Thừa kế:** Phân chia đất đai cha mẹ, bảo vệ suất thừa kế bắt buộc 2/3 không phụ thuộc di chúc.\n\n"
                "💡 *Bạn hãy chia sẻ sự việc bằng lời nói đời thường hoặc bấm chọn các tình huống bên dưới, tôi sẽ hỗ trợ bạn ngay!*"
            ),
            "agent": "CitizenIntakeAgent",
            "citations": [],
            "action_type": None,
            "action_data": None
        }
    ]

# ==================== SIDEBAR: TÀI KHOẢN, DEMO & TRỢ NĂNG ====================
with st.sidebar:
    st.title("⚖️ Trợ Lý Dân Gian")
    st.caption("Đồng Hành Pháp Lý Cá Nhân 24/7 • **v3.0**")
    st.markdown("---")

    # 1. THẺ THÔNG TIN TÀI KHOẢN HIỆN TẠI
    cur_u = st.session_state.current_user
    st.markdown(f"#### {cur_u.get('avatar', '👤')} Tài Khoản Đang Dùng")
    st.markdown(f"**Họ và tên:** `{cur_u.get('name')}`")
    st.markdown(f"**Lĩnh vực quan tâm:** *{cur_u.get('category', 'Dân sự')}*")
    if cur_u.get("phone") and cur_u.get("phone") != "Chưa đăng ký":
        st.caption(f"SĐT: {cur_u.get('phone')}")

    # 2. NÚT VÀO NHANH TÀI KHOẢN DEMO (1-CHẠM PERSONAS ĐỜI THỰC)
    st.markdown("##### ⚡ Vào Nhanh Tài Khoản Demo (1-Chạm):")
    st.caption("Trải nghiệm ngay 4 tình huống đời thực không cần đăng ký:")

    d_col1, d_col2 = st.columns(2)
    with d_col1:
        if st.button("🧑‍🌾 Bác Ba (Đất)", use_container_width=True, help="Bác Ba: Tranh chấp ranh giới đất & lối đi Tiền Giang"):
            persona = CitizenAccountManager.get_demo_persona("bac_ba")
            st.session_state.current_user = persona
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": f"👋 Kính chào **Bác Ba**! Tôi đã nắm được sự việc Bác đang bị hàng xóm lấn 1.5m đất vườn và rào bít lối đi chung tại Tiền Giang. Bác hãy gửi thêm thông tin để tôi hướng dẫn thủ tục hòa giải bắt buộc tại xã ngay nhé!",
                    "agent": "CitizenIntakeAgent",
                    "citations": [],
                    "action_type": None,
                    "action_data": None
                },
                {
                    "role": "user",
                    "content": persona["initial_prompt"]
                }
            ]
            st.toast(f"Đã đăng nhập: {persona['name']}", icon="🧑‍🌾")
            st.rerun()

    with d_col2:
        if st.button("👩‍🏭 Chị Lan (Vay)", use_container_width=True, help="Chị Lan: Dính bẫy app vay tín dụng đen Bình Dương"):
            persona = CitizenAccountManager.get_demo_persona("chi_lan")
            st.session_state.current_user = persona
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": f"👋 Chào **Chị Lan**! Em đừng quá lo sợ trước lời đe dọa của đối tượng cho vay app. Theo Điều 468 BLDS và Điều 201 BLHS, mức lãi 400k/ngày trên khoản 16tr là có dấu hiệu hình sự. Em DỪNG TRẢ LÃI NGAY, tôi sẽ giúp em làm Đơn tố giác gửi Công an!",
                    "agent": "CitizenIntakeAgent",
                    "citations": [],
                    "action_type": None,
                    "action_data": None
                },
                {
                    "role": "user",
                    "content": persona["initial_prompt"]
                }
            ]
            st.toast(f"Đã đăng nhập: {persona['name']}", icon="👩‍🏭")
            st.rerun()

    d_col3, d_col4 = st.columns(2)
    with d_col3:
        if st.button("👨‍💼 Anh Hoàng (Ly hôn)", use_container_width=True, help="Anh Hoàng: Thuận tình ly hôn, nhà chung 2.4 tỷ, con 22 tháng"):
            persona = CitizenAccountManager.get_demo_persona("anh_hoang")
            st.session_state.current_user = persona
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": f"👋 Chào **Anh Hoàng**! Thuận tình ly hôn là quyết định văn minh. Với căn chung cư 2.4 tỷ (nợ 300tr) và bé 22 tháng tuổi, luật ưu tiên mẹ nuôi con dưới 36 tháng và công sức nội trợ của vợ được tính ngang lao động tạo thu nhập. Tôi sẽ lập phương án thỏa thuận tối ưu cho 2 bên!",
                    "agent": "CitizenIntakeAgent",
                    "citations": [],
                    "action_type": None,
                    "action_data": None
                },
                {
                    "role": "user",
                    "content": persona["initial_prompt"]
                }
            ]
            st.toast(f"Đã đăng nhập: {persona['name']}", icon="👨‍💼")
            st.rerun()

    with d_col4:
        if st.button("👴 Cụ Sáu (Thừa kế)", use_container_width=True, help="Cụ Sáu: Chia thừa kế đất hương hỏa cha mẹ 3 tỷ cho 4 anh em"):
            persona = CitizenAccountManager.get_demo_persona("cu_sau")
            st.session_state.current_user = persona
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": f"👋 Kính chào **Cụ Sáu**! Di sản cha mẹ để lại không có di chúc sẽ được chia đều cho 4 người con theo Hàng thừa kế thứ nhất (Điều 651 BLDS). Nếu Cụ muốn giữ đất làm nhà thờ họ, các anh em có thể thỏa thuận nhận tiền đền bù tương ứng phần suất.",
                    "agent": "CitizenIntakeAgent",
                    "citations": [],
                    "action_type": None,
                    "action_data": None
                },
                {
                    "role": "user",
                    "content": persona["initial_prompt"]
                }
            ]
            st.toast(f"Đã đăng nhập: {persona['name']}", icon="👴")
            st.rerun()

    # 3. ĐĂNG KÝ TÀI KHOẢN CÁ NHÂN RIÊNG HOẶC QUAY VỀ KHÁCH
    with st.expander("👤 Cấp / Đăng Ký Tài Khoản Riêng", expanded=False):
        new_name = st.text_input("Họ và tên của bạn:", placeholder="VD: Trần Văn Bình", key="reg_name_in")
        new_phone = st.text_input("Số điện thoại liên hệ:", placeholder="0901234567", key="reg_phone_in")
        new_note = st.text_area("Tóm tắt vụ việc cần hỗ trợ:", placeholder="VD: Tranh chấp tiền cọc thuê nhà...", key="reg_note_in")
        if st.button("💾 Lưu & Đăng Nhập Tài Khoản Này", use_container_width=True):
            if new_name.strip():
                uid = f"CITIZEN_{len(new_name)}_{abs(hash(new_name + new_phone)) % 10000}"
                saved = st.session_state.account_mgr.save_account(uid, new_name.strip(), new_phone.strip(), new_note.strip())
                saved["avatar"] = "👤"
                saved["category"] = "Tài khoản cá nhân"
                st.session_state.current_user = saved
                st.success(f"Đã tạo và đăng nhập tài khoản: **{new_name}**")
                st.rerun()
            else:
                st.warning("Vui lòng nhập họ tên của bạn.")

    if cur_u.get("id") != "GUEST_CITIZEN":
        if st.button("🚪 Đăng xuất / Quay về Khách", use_container_width=True):
            st.session_state.current_user = CitizenAccountManager.get_default_guest()
            st.rerun()

    st.markdown("---")

    # 4. HƯỚNG DẪN SỬ DỤNG (TUTORIAL TOGGLE)
    if st.button("📖 Bật / Tắt Hướng Dẫn Nhanh", use_container_width=True):
        st.session_state.show_tutorial = not st.session_state.show_tutorial
        st.rerun()

    # 5. TRỢ NĂNG NGƯỜI CAO TUỔI
    st.subheader("👓 Trợ Năng Cho Người Già")
    elderly_mode = st.toggle("Chữ Lớn (19px) & Dễ Đọc", value=False, key="elderly_mode_toggle")
    if elderly_mode:
        st.markdown("""
        <style>
            html, body, [class*="css"], .stMarkdown, p, span, label, div {
                font-size: 19px !important;
                line-height: 1.8 !important;
            }
            .stButton>button {
                font-size: 19px !important;
                padding: 10px 20px !important;
                font-weight: bold !important;
            }
            .stTextInput>div>div>input, .stTextArea textarea {
                font-size: 19px !important;
            }
        </style>
        """, unsafe_allow_html=True)

    # 6. BẢO MẬT KHẨN CẤP (PANIC WIPE)
    st.subheader("🛡️ Quyền Riêng Tư")
    if st.button("🚨 XÓA SẠCH DẤU VẾT (Panic Wipe)", use_container_width=True, type="primary"):
        EphemeralPrivacyManager.panic_wipe_session_state(st.session_state)
        st.session_state.current_user = CitizenAccountManager.get_default_guest()
        st.toast("Đã xóa sạch 100% dữ liệu phiên làm việc!", icon="🛡️")
        st.rerun()

    # 7. THU GỌN TOÀN BỘ CÀI ĐẶT KỸ THUẬT VÀO ĐÁY SIDEBAR (KHÔNG LÀM RỐI NGƯỜI DÂN)
    with st.expander("⚙️ Cài Đặt Môi Trường LLM & Kết Nối", expanded=False):
        current_mode = st.session_state.factory.current_provider_type.value
        selected_mode = st.radio(
            "Môi trường LLM:",
            options=["cloud", "local"],
            format_func=lambda x: "☁️ Cloud (Google Gemini)" if x == "cloud" else "💻 Local (Ollama / Qwen)",
            index=0 if current_mode == "cloud" else 1,
            key="cfg_mode_select"
        )
        if selected_mode != current_mode:
            st.session_state.factory.set_provider(selected_mode)
            st.session_state.health = st.session_state.factory.check_health()
            st.success(f"Đã chuyển: {selected_mode.upper()}")
        
        if "health" not in st.session_state:
            st.session_state.health = st.session_state.factory.check_health()
        h = st.session_state.health
        st.caption(f"Cloud: `{'Sẵn sàng' if h['cloud']['available'] else 'Chưa có Key'}` | Local: `{'Online' if h['local']['available'] else 'Offline'}`")
        if st.button("🔄 Kiểm tra kết nối", key="btn_recheck_health"):
            st.session_state.health = st.session_state.factory.check_health()
            st.rerun()


# ==================== NỘI DUNG CHÍNH: 2 TABS RÕ RÀNG ====================

# HERO BANNER & THƯƠNG HIỆU CHUYÊN NGHIỆP (FIRST IMPRESSION & BRAND IDENTITY)
cur_name = st.session_state.current_user.get("name", "Công Dân")
cur_av = st.session_state.current_user.get("avatar", "👤")

st.markdown(f"""
<div class="pro-hero-banner">
    <div class="pro-badge">⚖️ NỀN TẢNG TRỢ GIÚP PHÁP LÝ CÔNG DÂN VIỆT NAM • VERSION 3.0</div>
    <div class="pro-title">Trợ Lý Luật Sư AI Dân Gian — Bình Dân, Chuẩn Xác & Miễn Phí 24/7</div>
    <div class="pro-subtitle">
        Đồng hành cùng người dân, người già và các đối tượng yếu thế. Tháo gỡ nỗi lo về 
        <b>Đất đai, Bẫy tín dụng đen, Thuận tình ly hôn và Di sản thừa kế</b> bằng ngôn ngữ đời thường, 
        hỏi thăm từng bước rõ ràng và tự động đóng gói hồ sơ tư pháp chuẩn Nghị quyết HĐTP TAND Tối cao.
    </div>
    <div class="trust-badge-row">
        <span class="trust-badge">🏛️ Chuẩn Mẫu 23-DS & NQ 326/2016 TANDTC</span>
        <span class="trust-badge">🔒 Bảo Mật Tuyệt Đối (Zero-Trust Privacy)</span>
        <span class="trust-badge">⚡ Phản Hồi Tức Thì &lt; 1 Giây</span>
        <span class="trust-badge">👵 Chế Độ Trợ Năng Chữ Lớn 19px</span>
        <span class="trust-badge">👤 Đang phục vụ: {cur_av} {cur_name}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# 3 TRỤ CỘT GIÁ TRỊ CỐT LÕI (VALUE PROPOSITIONS)
col_p1, col_p2, col_p3 = st.columns(3)
with col_p1:
    st.markdown("""
    <div class="pillar-card">
        <h4>🤝 Lắng Nghe & Dân Dã Hóa</h4>
        <p style="color: #64748B; font-size: 0.92rem;">
            Không dùng thuật ngữ hàn lâm đao to búa lớn. Luật sư AI kiên nhẫn hỏi từng bước, 
            không trả lời dồn dập, giúp người dân dễ hiểu và an tâm trình bày sự việc.
        </p>
    </div>
    """, unsafe_allow_html=True)
with col_p2:
    st.markdown("""
    <div class="pillar-card">
        <h4>⚖️ Chuẩn Mực Tố Tụng Tư Pháp</h4>
        <p style="color: #64748B; font-size: 0.92rem;">
            Tính đúng 100% án phí sơ thẩm (NQ 326), kiểm tra thời hiệu khởi kiện (BLDS 2015), 
            và chỉ đúng Tòa án có thẩm quyền tiếp nhận đơn 1-cửa theo Điều 39 BLTTDS.
        </p>
    </div>
    """, unsafe_allow_html=True)
with col_p3:
    st.markdown("""
    <div class="pillar-card">
        <h4>🛡️ Bảo Vệ Người Yếu Thế</h4>
        <p style="color: #64748B; font-size: 0.92rem;">
            Bảo vệ công sức nội trợ của người vợ khi ly hôn (Điều 59.2), ngăn chặn app cho vay 
            lãi nặng (Điều 201 BLHS) và bảo vệ 2/3 suất thừa kế bắt buộc cho con nhỏ.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True)

# NÚT HƯỚNG DẪN NHANH
tut_col1, tut_col2 = st.columns([3, 1])
with tut_col2:
    if st.button("📖 Hướng Dẫn Sử Dụng Nhanh", key="btn_top_tutorial", use_container_width=True):
        st.session_state.show_tutorial = not st.session_state.show_tutorial
        st.rerun()

# 📖 ONBOARDING TUTORIAL CHO NGƯỜI MỚI (HIỂN THỊ KHI ĐƯỢC BẬT)
if st.session_state.show_tutorial:
    with st.container():
        st.info("👋 **HƯỚNG DẪN 4 BƯỚC CHO NGƯỜI MỚI SỬ DỤNG TRONG 1 PHÚT:**")
        tut_steps = OnboardingTutorial.get_tutorial_steps()
        t_cols = st.columns(4)
        for idx, t in enumerate(tut_steps):
            with t_cols[idx]:
                st.markdown(f"### {t['icon']} Bước {t['step']}")
                st.markdown(f"**{t['title']}**")
                st.caption(t["desc"])

        if st.button("✅ Tôi đã hiểu - Bắt đầu ngay!", key="btn_close_tut", type="primary"):
            st.session_state.show_tutorial = False
            st.rerun()
        st.markdown("---")

quick_prompt = None

# PHÂN TÁCH GIAO DIỆN THÀNH 2 TAB: TAB 1 CHAT TINH GỌN & TAB 2 HỘP CÔNG CỤ DÂN SINH
main_tab_chat, main_tab_tools = st.tabs([
    "💬 Luật Sư Đồng Hành (Khung Chat Tinh Gọn)",
    "🧮 Hộp Công Cụ Dân Sinh 1-Chạm (10 Tiện Ích)"
])

# ================================================================
# TAB 1: 💬 KHUNG CHAT TINH GỌN (LOẠI BỎ TOÀN BỘ CÁC NÚT TEST THỪA)
# ================================================================
with main_tab_chat:

    # 4 LỐI TẮT TÌNH HUỐNG THỰC TẾ DÂN SINH (KHÔNG CÓ TEST KỸ THUẬT)
    st.markdown("💡 **Lối tắt tình huống thực tế thường gặp (Bấm 1-chạm để hỏi ngay):**")
    p_c1, p_c2, p_c3, p_c4 = st.columns(4)
    with p_c1:
        if st.button("🏡 Tranh chấp lấn ranh đất", use_container_width=True):
            quick_prompt = "Hàng xóm nhà tôi xây hàng rào lấn sang đất của tôi hơn 1 mét rưỡi. Tôi đã có Sổ đỏ chính chủ. Tôi có cần hòa giải ở xã trước không và làm đơn gì?"
    with p_c2:
        if st.button("🛑 Bẫy app vay & lãi cắt cổ", use_container_width=True):
            quick_prompt = "Tôi bị app vay tiền nóng trừ phí giải ngân, tính lãi hơn 100%/năm và gọi điện đe dọa người thân. Luật sư hướng dẫn tôi cách xử lý và làm đơn tố giác tội phạm gửi Công an."
    with p_c3:
        if st.button("💔 Thuận tình ly hôn & nuôi con", use_container_width=True):
            quick_prompt = "Vợ chồng tôi muốn thuận tình ly hôn. Có 1 căn nhà chung 2 tỷ và con nhỏ 2 tuổi. Vợ tôi ở nhà nội trợ thì tài sản chia thế nào và ai được quyền nuôi con?"
    with p_c4:
        if st.button("📜 Chia thừa kế đất cha mẹ", use_container_width=True):
            quick_prompt = "Cha mẹ tôi mất không để lại di chúc, có để lại thửa đất 300m2 cho 4 anh em. Xin luật sư cho biết theo luật thì chia thừa kế hàng thứ nhất thế nào và có thời hiệu bao nhiêu năm?"

    # KHUNG NẠP CHỨNG CỨ / ẢNH CHỤP GỌN GÀNG (EXPANDER THU NHỎ)
    with st.expander("📎 Gửi Ảnh / Tài Liệu Chứng Cứ (Sổ Đỏ, Giấy Vay Viết Tay, Tin Nhắn Zalo)", expanded=False):
        uploaded_ev_file = st.file_uploader(
            "Chọn ảnh chụp hoặc file tài liệu:",
            type=["pdf", "docx", "txt", "png", "jpg", "jpeg"],
            key="chat_clean_file_uploader"
        )
        if uploaded_ev_file is not None:
            with st.spinner("Đang bóc tách văn bản và giám định giá trị chứng cứ..."):
                parse_res = st.session_state.evidence_parser.parse_uploaded_file(uploaded_ev_file)

            ev_col1, ev_col2 = st.columns([1, 2])
            with ev_col1:
                st.metric("Điểm Giá Trị Chứng Cứ", f"{parse_res['evidence_score']} / 100")
                st.markdown(f"**Xếp hạng:** `{parse_res['evidence_grade']}`")
            with ev_col2:
                st.info(f"💡 **Lời khuyên:** {parse_res['action_advice']}")

            if st.button("💬 Đưa Tài Liệu Này Vào Cuộc Trò Chuyện", key="btn_send_file_to_clean_chat"):
                quick_prompt = (
                    f"Tôi vừa tải lên tài liệu/chứng cứ: '{parse_res['file_name']}'. "
                    f"Nội dung tóm lược:\n\"{parse_res['extracted_text'][:600]}\"\n"
                    f"Xin Luật sư giám định và tư vấn quyền lợi cho tôi."
                )

    st.markdown("---")

    # HIỂN THỊ LỊCH SỬ CHAT (HOÀN TOÀN TINH GỌN)
    for idx, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

            action_type = msg.get("action_type")
            action_data = msg.get("action_data")

            # XUẤT ĐƠN / VĂN BẢN KHI CẦN THIẾT CHO CÔNG DÂN
            if action_type == "DYNAMIC_DRAFT_ACTION":
                with st.expander("📝 Tải Về Mẫu Văn Bản Chuẩn Tư Pháp", expanded=True):
                    st.caption("AI đã điền sẵn căn cứ pháp luật và mẫu chuẩn. Bạn có thể tải về file Word để in ra điền tay hoặc ký tên:")
                    case_id = (action_data or {}).get("case_id", "DEBT_COLLECTION") if isinstance(action_data, dict) else "DEBT_COLLECTION"
                    doc_buf = st.session_state.dynamic_drafter.draft_debt_lawsuit({"court_name": "TAND Quận/Huyện", "plaintiff_name": cur_name, "principal_amount": "150.000.000 VNĐ"})
                    st.download_button(
                        label="📥 Tải Ngay Đơn Khởi Kiện Chuẩn (.docx)",
                        data=doc_buf,
                        file_name=f"Van_Ban_Phap_Ly_{cur_name.replace(' ', '_')}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        key=f"dl_clean_doc_{idx}"
                    )

            # DIỄN GIẢI BÌNH DÂN & ĐỌC TO CHO NGƯỜI CAO TUỔI
            if msg["role"] == "assistant" and msg.get("content") and not msg.get("content", "").startswith("👋"):
                c_action1, c_action2 = st.columns([1, 1])
                with c_action1:
                    with st.expander("☕ Xem Lời Giải Thích Dân Dã", expanded=False):
                        plain_cached_key = f"plain_cache_{idx}"
                        if plain_cached_key not in st.session_state:
                            st.session_state[plain_cached_key] = st.session_state.plain_engine.translate_to_plain_language(msg["content"])
                        st.markdown(st.session_state[plain_cached_key])
                with c_action2:
                    tts_cache_key = f"tts_audio_{idx}"
                    if tts_cache_key not in st.session_state:
                        if st.button("🔊 Đọc to câu trả lời", key=f"tts_btn_{idx}", help="Dành cho người già, người mắt kém"):
                            audio_fp = VoiceNarrator.generate_speech(msg["content"])
                            if audio_fp:
                                st.session_state[tts_cache_key] = audio_fp.read()
                                st.rerun()
                    else:
                        st.audio(st.session_state[tts_cache_key], format="audio/mp3")

            # LỰA CHỌN TRẢ LỜI NHANH 1-CHẠM
            if msg.get("quick_options") and idx == len(st.session_state.messages) - 1:
                st.markdown("👉 **Lựa chọn trả lời nhanh:**")
                q_cols = st.columns(min(len(msg["quick_options"]), 4))
                for q_i, opt in enumerate(msg["quick_options"]):
                    with q_cols[q_i % len(q_cols)]:
                        if st.button(opt, key=f"qopt_click_{idx}_{q_i}", use_container_width=True):
                            st.session_state.pending_quick_input = opt
                            st.rerun()

            # CÂU HỎI GỢI Ý
            if msg.get("suggested_followups") and idx == len(st.session_state.messages) - 1:
                st.markdown("💡 **Câu hỏi gợi ý:**")
                f_cols = st.columns(min(len(msg["suggested_followups"]), 3))
                for f_i, fq in enumerate(msg["suggested_followups"][:3]):
                    with f_cols[f_i % len(f_cols)]:
                        if st.button(f"👉 {fq}", key=f"fup_click_{idx}_{f_i}", use_container_width=True):
                            st.session_state.pending_quick_input = fq
                            st.rerun()

    # XỬ LÝ NHẬP LIỆU CHAT
    pending_text = getattr(st.session_state, "pending_quick_input", None)
    if pending_text:
        del st.session_state.pending_quick_input
        user_input = pending_text
    elif quick_prompt:
        user_input = quick_prompt
    else:
        user_input = st.chat_input("Nhập câu chuyện hoặc câu hỏi pháp lý của bạn...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Luật sư Dân gian đang lắng nghe và phân tích sự việc..."):
                intake_res = st.session_state.citizen_intake.respond(user_input)
                reply_text = intake_res.get("response", "")
                q_opts = intake_res.get("quick_options", [])
                f_ups = intake_res.get("suggested_followups", [])

                st.markdown(reply_text)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": reply_text,
                    "agent": "CitizenIntakeAgent",
                    "citations": [],
                    "action_type": None,
                    "action_data": None,
                    "quick_options": q_opts,
                    "suggested_followups": f_ups
                })
        st.rerun()


# ================================================================
# TAB 2: 🧮 HỘP CÔNG CỤ DÂN SINH 1-CHẠM (10 TIỆN ÍCH CHUYÊN BIỆT)
# ================================================================
with main_tab_tools:
    st.markdown("#### 🧮 Hộp Công Cụ Dân Sinh 1-Chạm")
    st.caption("Các tiện ích tính toán và tra cứu pháp lý chuyên biệt phục vụ đời sống hàng ngày của người dân:")

    tool_tab0, tool_tab1, tool_tab2, tool_tab3, tool_tab4, tool_tab5, tool_tab6, tool_tab7, tool_tab8, tool_tab9 = st.tabs([
        "🧭 0. Phễu 3 Phút",
        "💰 1. Án Phí NQ 326",
        "🛑 2. Bẫy Tín Dụng Đen",
        "🏛️ 3. Tòa Án & 1 Cửa",
        "👨‍👩‍👧 4. Ly Hôn & Con Cái",
        "📜 5. Thừa Kế Đất Đai",
        "📝 6. Đơn Mẫu 23-DS",
        "⏳ 7. Thời Hiệu",
        "⚖️ 8. Giả Lập Tố Tụng",
        "📦 9. Trọn Gói Hồ Sơ"
    ])

    with tool_tab0:
        st.markdown("##### 🧭 Phễu Chẩn Đoán Pháp Lý 3 Phút (Không Cần Gõ Chữ)")
        st.caption("Dành cho người già, người ít am hiểu luật: Chọn nhanh các phương án để AI đưa ra chẩn đoán và 3 bước hành động ngay:")
        wiz_cat = st.selectbox(
            "Chọn lĩnh vực vụ việc cần chẩn đoán:",
            options=["DEBT", "LAND"],
            format_func=lambda x: "💸 Đòi nợ & Vay mượn tài sản" if x == "DEBT" else "🏡 Tranh chấp đất đai & Lối đi",
            key="wiz_cat_select"
        )
        tree = CitizenDiagnosticFunnel.get_funnel(wiz_cat)
        user_answers = {}
        for s in tree["steps"]:
            opts = [o["label"] for o in s["options"]]
            sel = st.radio(f"**Bước {s['step_id']}: {s['question']}**", options=range(len(opts)), format_func=lambda i: opts[i], key=f"wiz_step_{s['step_id']}")
            user_answers[s["step_id"]] = sel

        if st.button("🚀 Chẩn Đoán Tức Thì & Nhận Lời Khuyên 3 Bước", key="btn_run_wizard"):
            diag = CitizenDiagnosticFunnel.evaluate_answers(wiz_cat, user_answers)
            st.success(f"**Kết luận chẩn đoán:** {diag['diagnosis']}")
            st.markdown(f"**1.** {diag['step_1']}")
            st.markdown(f"**2.** {diag['step_2']}")
            st.markdown(f"**3.** {diag['step_3']}")

    with tool_tab1:
        st.markdown("##### 💰 Tính Án Phí Dân Sự Sơ Thẩm (Nghị quyết số 326/2016/UBTVQH14)")
        c_fee_input = st.number_input("Nhập số tiền tranh chấp (VNĐ):", min_value=0, value=100000000, step=10000000, key="calc_fee_in")
        if st.button("Tính Án Phí Ngay", key="btn_calc_fee"):
            calc_res = CitizenLegalTools.calculate_court_fee(c_fee_input)
            cf_c1, cf_c2 = st.columns(2)
            with cf_c1:
                st.metric("Tiền Tạm Ứng Án Phí (Nộp trước 50%)", calc_res["formatted_advance"])
            with cf_c2:
                st.metric("Tổng Án Phí Sơ Thẩm Toàn Bộ", calc_res["formatted_fee"])
            st.caption(f"📌 **Khung áp dụng:** {calc_res['bracket']}")

    with tool_tab2:
        st.markdown("##### 🛑 Máy Quét Bẫy Tín Dụng Đen & Cầm Cố Cắt Cổ")
        st.caption("Bảo vệ người vay tiền nóng, bốc bát họ, app vay online theo Điều 468 BLDS và Điều 201 BLHS:")
        us_c1, us_c2 = st.columns(2)
        with us_c1:
            u_principal = st.number_input("Số tiền ghi trên giấy vay/app (Gốc danh nghĩa):", min_value=1000000, value=20000000, step=1000000, key="u_pr_in")
            u_actual = st.number_input("Số tiền THỰC NHẬN về tay (sau khi bị trừ phí):", min_value=500000, value=16000000, step=1000000, key="u_act_in")
            u_days = st.number_input("Thời hạn vay (Số ngày, vd 30 hoặc 50 ngày):", min_value=1, value=50, step=5, key="u_days_in")
        with us_c2:
            u_periodic_fee = st.number_input("Tiền lãi/phí phải đóng mỗi kỳ (VNĐ):", min_value=0, value=400000, step=50000, key="u_pfee_in")
            u_cycle = st.selectbox("Chu kỳ đóng tiền:", [1, 7, 30], format_func=lambda x: "Mỗi ngày" if x == 1 else ("Mỗi tuần" if x == 7 else "Mỗi tháng"), key="u_cycle_in")
            u_hidden = st.number_input("Các khoản phụ phí khác (phí hồ sơ, bảo hiểm...):", min_value=0, value=500000, step=100000, key="u_hid_in")

        if st.button("🔍 Quét Lãi Suất & Kiểm Tra Dấu Hiệu Tín Dụng Đen", key="btn_check_usury"):
            u_res = UsuryTrapDetector.analyze_loan(u_principal, u_actual, int(u_days), u_periodic_fee, int(u_cycle), u_hidden)
            st.markdown(f"### {u_res['color_badge']}")
            st.warning(f"**Tình trạng:** {u_res['status_text']}")
            
            u_m1, u_m2, u_m3 = st.columns(3)
            with u_m1:
                st.metric("Lãi Suất Thực Tế", f"{u_res['annualized_percent']}% / năm")
            with u_m2:
                st.metric("Trần Cho Phép (Điều 468)", "20.0% / năm")
            with u_m3:
                st.metric("Tiền Lãi Vượt Trần Bất Hợp Pháp", UsuryTrapDetector.format_currency(u_res['excess_interest_amount']))

            st.markdown("##### 🛡️ Hướng Dẫn Hành Động Cứu Nguy Cho Người Dân:")
            for rec in u_res["recommendations"]:
                st.markdown(rec)

            if u_res["severity"] in ["CRIMINAL_ALERT", "EXTREME_USURY"]:
                st.markdown("---")
                denounce_txt = UsuryTrapDetector.generate_criminal_denunciation_template(
                    u_res,
                    {"full_name": cur_name, "birth_year": "1990", "cccd": "079090xxxxxx", "address": "TP. Hồ Chí Minh", "phone": cur_u.get("phone", "090xxxxxxx")},
                    {"name": "Đối tượng cho vay lãi nóng", "contact": "App vay / SĐT đối tượng", "address": "Khu vực cư trú", "police_dept": "Cơ quan CSĐT Công an Quận/Huyện"}
                )
                st.download_button(
                    "📥 Tải Mẫu Đơn Tố Giác Tội Phạm (.txt)",
                    data=denounce_txt,
                    file_name="Don_To_Giac_Cho_Vay_Lai_Nang_Dieu_201_BLHS.txt",
                    mime="text/plain",
                    key="dl_denounce_btn"
                )

    with tool_tab3:
        st.markdown("##### 🏛️ Tra Cứu Tòa Án Thẩm Quyền & Hành Trang Ra Tòa 1 Cửa")
        st.caption("Tránh bị Tòa trả lại đơn (Điều 192 BLTTDS 2015), tra cứu địa chỉ chính xác và danh mục giấy tờ cần mang:")
        cj_c1, cj_c2, cj_c3 = st.columns(3)
        with cj_c1:
            cj_type = st.selectbox(
                "Lĩnh vực vụ việc:",
                options=list(CourtJurisdictionGuide.DISPUTE_CATEGORIES.keys()),
                format_func=lambda k: CourtJurisdictionGuide.DISPUTE_CATEGORIES[k]["title"],
                key="cj_type_in"
            )
        with cj_c2:
            cj_prov = st.selectbox("Tỉnh / Thành phố nơi xảy ra việc/bị đơn cư trú:", ["HỒ CHÍ MINH", "HÀ NỘI", "ĐÀ NẴNG", "TỈNH KHÁC"], key="cj_prov_in")
        with cj_c3:
            cj_dist = st.text_input("Quận / Huyện cụ thể:", value="QUẬN 1", key="cj_dist_in")

        if st.button("📍 Tra Cứu Tòa Án & Lập Danh Mục Hành Trang 1 Cửa", key="btn_run_jurisdiction"):
            cj_res = CourtJurisdictionGuide.resolve_jurisdiction_and_checklist(cj_type, cj_prov, cj_dist)
            st.success(f"🏛️ **Tòa Án Thụ Lý Thẩm Quyền:** {cj_res['target_court_name']}")
            st.markdown(f"📍 **Địa chỉ nộp đơn:** {cj_res['target_court_address']} *(ĐT: {cj_res['target_court_phone']})*")
            st.markdown(f"🏢 **Nơi nộp tiền tạm ứng án phí:** {cj_res['target_thads_name']} ({cj_res['target_thads_address']})")
            
            if cj_res["mandatory_pre_litigation"]:
                st.error(f"⚠️ **LƯU Ý SỐNG CÒN:** {cj_res['pre_litigation_notice']}")
            
            st.markdown(f"##### 🎒 Danh Mục Hồ Sơ Cần Chuẩn Bị (Checklist Hành Trang):")
            for idx, doc in enumerate(cj_res["required_dossier"], 1):
                st.markdown(f"**{idx}.** {doc}")

    with tool_tab4:
        st.markdown("##### 👨‍👩‍👧 Máy Tính Chia Tài Sản & Bảo Vệ Con Cái Khi Ly Hôn")
        st.caption("Bảo vệ công sức nội trợ của người vợ (Điều 59.2) và quyền lợi của con nhỏ (Điều 81 Luật HNGĐ 2014):")
        div_c1, div_c2 = st.columns(2)
        with div_c1:
            d_common_asset = st.number_input("Tổng tài sản chung tạo lập trong hôn nhân (nhà, đất, tiền gửi):", min_value=0, value=1200000000, step=50000000, key="d_asset_in")
            d_common_debt = st.number_input("Tổng nợ chung của 2 vợ chồng (nếu có):", min_value=0, value=200000000, step=20000000, key="d_debt_in")
            d_homemaker = st.checkbox("Người vợ ở nhà làm nội trợ, chăm sóc gia đình?", value=True, key="d_hm_in")
        with div_c2:
            d_income_supporter = st.number_input("Thu nhập hàng tháng của người không trực tiếp nuôi con (VNĐ):", min_value=0, value=20000000, step=1000000, key="d_inc_in")
            d_child_age = st.number_input("Tuổi của con nhỏ nhất (tháng tuổi):", min_value=1, value=24, step=6, key="d_cage_in")

        if st.button("⚖️ Phân Tích Tài Sản & Quyền Nuôi Con", key="btn_calc_divorce"):
            mock_children = [{"name": "Con chung", "age_months": int(d_child_age)}]
            div_res = DivorceSettlementCalculator.calculate_settlement(
                0, 0, d_common_asset, d_common_debt, d_homemaker, mock_children, d_income_supporter
            )
            st.success(f"🏠 **Tài sản chung thuần túy sau khi trừ nợ:** {DivorceSettlementCalculator.format_currency(div_res['net_common_assets'])}")
            
            dc1, dc2 = st.columns(2)
            with dc1:
                st.metric("Phần Chia Người Vợ (50%)", DivorceSettlementCalculator.format_currency(div_res['wife_share_common']))
            with dc2:
                st.metric("Phần Chia Người Chồng (50%)", DivorceSettlementCalculator.format_currency(div_res['husband_share_common']))

            st.markdown("##### 👶 Phân Tích Quyền Trực Tiếp Nuôi Con & Cấp Dưỡng:")
            for c_info in div_res["custody_analysis"]:
                st.info(f"**{c_info['child_name']} ({c_info['age_display']}):** {c_info['rule']}\n\n👉 {c_info['explanation']}")
            
            st.metric("Mức Cấp Dưỡng Khuyến Nghị Cho Bé", f"{DivorceSettlementCalculator.format_currency(div_res['monthly_child_support_per_child'])} / tháng")

    with tool_tab5:
        st.markdown("##### 📜 Phân Chia Di Sản Thừa Kế Đất Đai Dân Gian (BLDS 2015)")
        st.caption("Tính toán phân chia di sản hàng thứ nhất (Điều 651) và bảo vệ suất bắt buộc 2/3 không phụ thuộc di chúc (Điều 644):")
        inh_c1, inh_c2 = st.columns(2)
        with inh_c1:
            inh_total = st.number_input("Tổng trị giá di sản (Nhà đất, sổ tiết kiệm, vàng):", min_value=0, value=3000000000, step=100000000, key="inh_tot_in")
            inh_debt = st.number_input("Chi phí mai táng + tiền nợ của người chết (nếu có):", min_value=0, value=100000000, step=10000000, key="inh_debt_in")
            inh_spouse = st.checkbox("Người vợ / chồng của người chết còn sống?", value=True, key="inh_sp_in")
        with inh_c2:
            inh_parents = st.number_input("Số cha, mẹ của người chết còn sống:", min_value=0, max_value=2, value=1, key="inh_par_in")
            inh_children = st.number_input("Tổng số người con (con đẻ + con nuôi):", min_value=1, max_value=10, value=3, key="inh_ch_in")
            inh_minor = st.number_input("Trong đó có bao nhiêu con chưa đủ 18 tuổi:", min_value=0, max_value=10, value=1, key="inh_min_in")

        if st.button("⚖️ Tính Chia Di Sản Chuẩn Bộ Luật Dân Sự", key="btn_calc_inheritance"):
            inh_res = InheritanceDistributionEngine.calculate_statutory_inheritance(
                inh_total, 0, inh_debt, inh_spouse, int(inh_parents), int(inh_children), 0, int(inh_minor), 0
            )
            st.success(f"🏡 **Di sản thực tế đem chia:** {InheritanceDistributionEngine.format_currency(inh_res['net_estate_value'])}")
            
            im1, im2 = st.columns(2)
            with im1:
                st.metric(f"Mỗi Suất Hàng 1 ({inh_res['heirs_rank_1_total']} người)", InheritanceDistributionEngine.format_currency(inh_res['legal_share_per_person']))
            with im2:
                st.metric("Suất Bảo Vệ 2/3 (Điều 644)", InheritanceDistributionEngine.format_currency(inh_res['mandatory_protection_share_2_thirds']))

    with tool_tab6:
        st.markdown("##### 📝 Xuất Đơn Khởi Kiện Chuẩn Mẫu 23-DS (Nghị quyết 01/2017/NQ-HĐTP)")
        st.caption("Điền thông tin cơ bản để AI lập tức đóng gói Đơn khởi kiện chuẩn nộp Tòa án:")
        pf_c1, pf_c2 = st.columns(2)
        with pf_c1:
            p_court = st.text_input("Tòa án nhân dân thụ lý:", value="TAND Quận 1, TP. Hồ Chí Minh", key="pf_court")
            p_pl_name = st.text_input("Họ tên Người khởi kiện:", value=cur_name, key="pf_pl_name")
            p_claim_money = st.text_input("Số tiền đòi / Giá trị khởi kiện:", value="150.000.000 VNĐ", key="pf_claim_money")
        with pf_c2:
            p_df_name = st.text_input("Họ tên Người bị kiện:", value="Trần Văn Nam", key="pf_df_name")
            p_df_addr = st.text_input("Nơi cư trú người bị kiện:", value="Phường Bến Nghé, Quận 1, TP.HCM", key="pf_df_addr")
            p_dispute = st.text_input("Quan hệ pháp luật tranh chấp:", value="Đòi nợ vay theo hợp đồng vay tài sản", key="pf_dispute")

        if st.button("🚀 Xuất File Word Đơn Khởi Kiện Chuẩn 1-Chạm", key="btn_gen_petition_direct"):
            petition_data = {
                "court_name": p_court,
                "plaintiff_name": p_pl_name,
                "claim_amount": p_claim_money,
                "defendant_name": p_df_name,
                "defendant_address": p_df_addr,
                "dispute_title": p_dispute
            }
            pet_buf = InstantPetitionGenerator.generate_lawsuit_petition_docx(petition_data)
            st.download_button(
                label="📥 Tải Ngay Đơn Khởi Kiện Đã Điền (.docx)",
                data=pet_buf,
                file_name="Don_Khoi_Kien_Dan_Su_Mau_23DS.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                key="dl_pet_direct_btn"
            )
            st.success("Đã sinh đơn khởi kiện chuẩn hình thức tư pháp thành công!")

    with tool_tab7:
        st.markdown("##### ⏳ Kiểm Tra Thời Hiệu Khởi Kiện (Điều 429, 588, 623 BLDS 2015)")
        sol_c1, sol_c2 = st.columns(2)
        with sol_c1:
            sol_date = st.text_input("Ngày phát sinh sự việc / Ngày hết hạn trả nợ (DD/MM/YYYY):", value="15/05/2023", key="sol_date_in")
        with sol_c2:
            sol_domain = st.selectbox("Lĩnh vực tranh chấp:", ["Hợp đồng / Nợ vay (3 năm)", "Bồi thường thiệt hại (3 năm)", "Thừa kế đất đai (30 năm)"], key="sol_domain_in")
        if st.button("Kiểm Tra Thời Hiệu", key="btn_check_sol"):
            d_key = "CONTRACT" if "Hợp đồng" in sol_domain else ("INHERITANCE_LAND" if "Thừa kế" in sol_domain else "TORT")
            sol_res = CitizenLegalTools.check_statute_of_limitations(sol_date, d_key)
            if sol_res.get("is_valid_date"):
                st.markdown(f"**Trạng thái:** `{sol_res['status_label']}`")
                st.info(f"💡 {sol_res['warning']} *(Căn cứ: {sol_res['legal_article']})*")
            else:
                st.error(sol_res.get("message"))

    with tool_tab8:
        st.markdown("##### ⚖️ Giả Lập Bàn Cờ Đối Kháng & Dự Báo Tỷ Lệ Thắng Kiện")
        st.caption("AI giả lập phiên Tòa: Bên khởi kiện tấn công gì, đối phương sẽ phản đòn gì và kế sách hóa giải:")
        sim_c1, sim_c2 = st.columns(2)
        with sim_c1:
            sim_case = st.selectbox("Dạng tranh chấp cần giả lập:", ["Đòi nợ vay tiền (Dân sự)", "Tranh chấp đất đai ranh giới (Đất đai)", "Ly hôn tranh chấp tài sản & con (HNGĐ)"], key="sim_case_in")
        with sim_c2:
            sim_ev = st.selectbox("Chứng cứ hiện có của bạn:", ["Có hợp đồng / giấy viết tay chính chủ", "Có Vi bằng / Công chứng nhà nước", "Chỉ có tin nhắn Zalo / chuyển khoản", "Chỉ có lời nói miệng"], key="sim_ev_in")

        if st.button("🚀 Bắt Đầu Giả Lập Phiên Tòa Đối Kháng", key="btn_run_sim"):
            simulator = LegalLitigationSimulator()
            sim_res = simulator.simulate_case(sim_case, "Tranh chấp dân sự thực tế", sim_ev)
            st.metric("🎯 Dự Báo Tỷ Lệ Thắng Kiện Tại Tòa", f"{sim_res['win_rate']}%", delta="Khả thi tố tụng")
            st.markdown(f"> 🏛️ **Dự báo phán quyết của Tòa:** *{sim_res['court_forecast']}*")

    with tool_tab9:
        st.markdown("##### 📦 Xuất Trọn Gói Bộ Hồ Sơ Tố Tụng Hoàn Chỉnh (Nộp TAND)")
        st.caption("Tự động kết hợp: Đơn khởi kiện chuẩn Mẫu 23-DS + Bảng tạm tính án phí NQ 326 + Báo cáo bàn cờ đối kháng 2 chiều + Danh mục chứng cứ vào 1 file Word .docx duy nhất:")
        
        dos_c1, dos_c2 = st.columns(2)
        with dos_c1:
            dos_court = st.text_input("Tòa án thụ lý:", value="Tòa án nhân dân Quận 1, TP. Hồ Chí Minh", key="dos_court_in")
            dos_plaintiff = st.text_input("Họ tên Người khởi kiện (Bạn):", value=cur_name, key="dos_plaintiff_in")
            dos_year = st.text_input("Năm sinh:", value="1985", key="dos_year_in")
            dos_id = st.text_input("Số CCCD:", value="079085012345", key="dos_id_in")
            dos_addr = st.text_input("Nơi cư trú người khởi kiện:", value="Số 123 Lê Lợi, Phường Bến Nghé, Quận 1, TP.HCM", key="dos_addr_in")
            dos_phone = st.text_input("Điện thoại liên hệ:", value=cur_u.get("phone", "0901234567"), key="dos_phone_in")
        with dos_c2:
            dos_defendant = st.text_input("Họ tên Người bị kiện (Con nợ/Bên vi phạm):", value="Trần Thị B", key="dos_def_in")
            dos_def_addr = st.text_input("Nơi cư trú người bị kiện:", value="Số 456 Hai Bà Trưng, Phường Tân Định, Quận 1, TP.HCM", key="dos_def_addr_in")
            dos_amount = st.number_input("Tổng số tiền yêu cầu đòi (VNĐ):", min_value=1000000, value=150000000, step=10000000, key="dos_amt_in")
            dos_summary = st.text_area("Tóm tắt nội dung khởi kiện:", value="Bên bị kiện đã vay của tôi số tiền 150.000.000 VNĐ vào ngày 15/03/2023, có viết giấy nhận nợ hẹn trả vào ngày 15/09/2023. Tuy nhiên đến nay bên bị kiện cố tình trốn tránh, chặn liên lạc và không thực hiện nghĩa vụ trả nợ.", key="dos_sum_in")

        if st.button("🚀 Đóng Gói Toàn Diện & Xuất File Word Bộ Hồ Sơ (.docx)", key="btn_gen_full_dossier"):
            with st.spinner("Đang biên soạn trọn bộ hồ sơ tư pháp chuyên nghiệp..."):
                calc_fee = CitizenLegalTools.calculate_court_fee(dos_amount)
                dossier_stream = LitigationDossierGenerator.generate_dossier_docx(
                    court_name=dos_court,
                    plaintiff_name=dos_plaintiff,
                    plaintiff_year=dos_year,
                    plaintiff_id=dos_id,
                    plaintiff_address=dos_addr,
                    plaintiff_phone=dos_phone,
                    defendant_name=dos_defendant,
                    defendant_address=dos_def_addr,
                    claim_amount=float(dos_amount),
                    dispute_summary=dos_summary,
                    court_fee_details=calc_fee
                )
                st.success("✅ Đã hoàn tất biên soạn Bộ Hồ Sơ Tố Tụng Hoàn Chỉnh chuẩn quy cách tư pháp!")
                st.download_button(
                    label="📥 Tải Ngay Bộ Hồ Sơ Tố Tụng Trọn Gói (.docx)",
                    data=dossier_stream,
                    file_name=f"Bo_Ho_So_To_Tung_Tron_Goi_TAND_{dos_plaintiff.replace(' ', '_')}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    key="dl_full_litigation_dossier"
                )


# ==================== CHÂN TRANG CHUYÊN NGHIỆP (CREDIBILITY & SOCIAL PROOF) ====================
st.markdown("""
<div class="pro-footer-container">
    <div style="font-weight: 700; color: #1E293B; font-size: 1rem; margin-bottom: 0.4rem;">
        ⚖️ NỀN TẢNG PHÁP LÝ DÂN GIAN — CÔNG NGHỆ VÌ CÔNG BẰNG XÃ HỘI
    </div>
    <div>
        Căn cứ pháp lý chính thống: Bộ luật Dân sự 2015 • Bộ luật Tố tụng Dân sự 2015 • Luật Hôn nhân & Gia đình 2014 • Luật Đất đai 2024.<br>
        Dữ liệu đối chiếu trực tiếp từ Cổng Thông tin điện tử Chính phủ (<a href="https://vanban.chinhphu.vn" target="_blank" style="color: #2563EB;">vanban.chinhphu.vn</a>) và TAND Tối cao.
    </div>
    <div style="margin-top: 0.6rem; color: #94A3B8; font-size: 0.82rem;">
        🛡️ Quyền riêng tư: Hệ thống không lưu trữ vĩnh viễn dữ liệu nhạy cảm. Toàn bộ thông tin được mã hóa và xóa sạch khi kết thúc phiên.<br>
        Bản quyền © 2026 LegalTech Platform v3.0. Phát triển vì lợi ích cộng đồng người dân Việt Nam.
    </div>
</div>
""", unsafe_allow_html=True)

