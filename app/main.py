"""
LegalTech Platform - Streamlit Application - Version 2.7 (The Specialized Multi-Agent Swarm Platform)
Giao diện 2 Tab chuẩn phong cách NotebookLM:
- TAB 1: 💬 AI Legal Chatbot & Command Center (In-Chat Everything & Interactive Widgets)
- TAB 2: 🧰 Legal Tools Studio (Trưng bày & Thực thi Độc lập Toàn bộ Công cụ)
"""

import os
import sys
import json
import math
import pandas as pd
import streamlit as st

# Thêm đường dẫn gốc vào hệ thống import
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from llm_provider.model_factory import ModelFactory, ProviderType
from src.agents import LegalMultiAgentWorkflow
from src.database import DatabaseManager
from src.security import PIIMasker, PromptInjectionGuard, EphemeralPrivacyManager
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
from src.agents.holistic_evaluator import HolisticAuditEngine
from src.agents.citizen_intake_agent import CitizenIntakeAgent
from src.agents.memory_store import LegalMemoryStore
from src.dossier import (
    generate_registration_request_docx,
    generate_company_charter_docx,
    generate_member_list_docx,
    generate_full_dossier_docx,
    validate_dossier_legal_compliance,
    validate_company_name,
    DynamicLegalDrafter,
)

# Cấu hình giao diện Streamlit
st.set_page_config(
    page_title="LegalTech Platform - v3.0",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Khởi tạo trạng thái Session
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

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "👋 **Xin chào bạn! Tôi là Luật sư Dân gian Đồng hành (LegalTech Platform v3.0 - Citizen-Centric Diagnostic Platform).**\n\n"
                "🎯 **Định hướng trọng tâm:** Tôi chuyên sâu hỗ trợ **Cá nhân & Người dân** trong các vấn đề đời sống thiết thực:\n"
                "- 🏡 **Đất đai & Ranh giới:** Hàng xóm lấn đất, tranh chấp lối đi chung, sổ đỏ cha ông.\n"
                "- 💸 **Đòi nợ & Vay mượn:** Nợ khó đòi, con nợ cắt liên lạc, giấy viết tay hoặc chỉ có tin nhắn Zalo.\n"
                "- 💔 **Hôn nhân & Gia đình:** Thuận tình hoặc đơn phương ly hôn, tranh chấp nuôi con và chia tài sản.\n"
                "- 🛡️ **Lừa đảo & Bạo lực:** Lừa đảo qua mạng, chuyển khoản, bạo lực học đường, xâm phạm danh dự.\n\n"
                "💡 **Nguyên tắc hỗ trợ:** Tôi sẽ **hỏi thăm từng bước để nắm chắc sự việc, tuyệt đối không trả lời dồn dập** khiến bạn bị ngợp. Bạn có thể gõ câu chuyện hoặc bấm các lựa chọn nhanh!"
            ),
            "agent": "CitizenIntakeAgent",
            "citations": [],
            "action_type": None,
            "action_data": None
        }
    ]

if "citizen_intake" not in st.session_state:
    st.session_state.citizen_intake = CitizenIntakeAgent(st.session_state.factory)

if "evidence_parser" not in st.session_state:
    st.session_state.evidence_parser = MultimodalEvidenceParser(st.session_state.factory)

# ==================== SIDEBAR: KIẾN TRÚC & MODEL SWITCHER ====================
with st.sidebar:
    st.title("⚖️ LegalTech Platform")
    st.caption("Trợ Lý Luật Sư Dân Gian Đồng Hành 24/7 • **v3.0**")
    st.markdown("---")

    # ⚡ CẤU HÌNH MODEL SWITCHER (TIÊU CHÍ 3 UIT)
    st.subheader("⚡ Chế độ Mô hình (Model Switcher)")
    current_mode = st.session_state.factory.current_provider_type.value
    selected_mode = st.radio(
        "Chọn môi trường LLM:",
        options=["cloud", "local"],
        format_func=lambda x: "☁️ Cloud Model (Google Gemini)" if x == "cloud" else "💻 Local Model (Ollama / Qwen 2.5)",
        index=0 if current_mode == "cloud" else 1
    )

    if selected_mode != current_mode:
        st.session_state.factory.set_provider(selected_mode)
        st.session_state.health = st.session_state.factory.check_health()
        st.success(f"Đã chuyển sang chế độ: **{selected_mode.upper()}**")

    # 📡 KIỂM TRA TRẠNG THÁI KẾT NỐI
    st.markdown("---")
    st.subheader("📡 Trạng thái Kết nối (Health)")
    if "health" not in st.session_state:
        st.session_state.health = st.session_state.factory.check_health()
    health = st.session_state.health

    c1, c2 = st.columns(2)
    with c1:
        if health["cloud"]["available"]:
            st.markdown("🟢 **Cloud:** Sẵn sàng")
        else:
            st.markdown("🟡 **Cloud:** Chưa có Key")
    with c2:
        if health["local"]["available"]:
            st.markdown("🟢 **Local:** Online")
        else:
            st.markdown("🔴 **Local:** Offline")

    st.caption(f"Cloud: `{health['cloud']['model']}`")
    st.caption(f"Local: `{health['local']['model']}`")
    if st.button("🔄 Kiểm tra lại kết nối", use_container_width=True):
        st.session_state.health = st.session_state.factory.check_health()
        st.rerun()

    # 👓 CHẾ ĐỘ TRỢ NĂNG DÀNH CHO NGƯỜI CAO TUỔI
    st.markdown("---")
    st.subheader("👓 Trợ Năng & Dễ Tiếp Cận")
    elderly_mode = st.toggle("Chế độ Chữ Lớn (Người Cao Tuổi)", value=False, key="elderly_mode_toggle")
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
        st.caption("🟢 Đã bật giao diện phóng to chữ, giãn dòng thoáng và tương phản cao.")

    # 🛡️ BẢO MẬT & XÓA DẤU VẾT KHẨN CẤP (PANIC WIPE)
    st.markdown("---")
    st.subheader("🛡️ Quyền Riêng Tư Tuyệt Đối")
    st.caption("Dữ liệu chỉ nằm trong bộ nhớ tạm (RAM) của bạn, không lưu vĩnh viễn.")
    if st.button("🚨 XÓA SẠCH DẤU VẾT (Panic Wipe)", use_container_width=True, type="primary"):
        EphemeralPrivacyManager.panic_wipe_session_state(st.session_state)
        st.toast("Đã xóa sạch 100% lịch sử và dữ liệu phiên làm việc!", icon="🛡️")
        st.rerun()

    st.markdown("---")
    st.info(
        "⚖️ **Trụ cột Version 3.0:**\n"
        "- Citizen-Centric Diagnostic Intake\n"
        "- Multi-Turn Socratic Intake\n"
        "- 360° Holistic Audit Matrix\n"
        "- Senior Accessibility Mode (19px)\n"
        "- Emotional Rant De-Noiser\n"
        "- Zero-Trust Ephemeral Wipe\n"
        "- Telegram Bot Sub-Second"
    )


# ==================== NỘI DUNG CHÍNH: 2 TABS ====================

# ================================================================
# TAB 1: 💬 AI LEGAL CHATBOT & COMMAND CENTER (IN-CHAT EVERYTHING)
# ================================================================
# ==================== TRỢ LÝ LUẬT SƯ AI DÂN GIAN (BỀ NỔI DÂN SINH) ====================
st.header("⚖️ Trợ Lý Luật Sư AI Dân Gian")
st.caption("Lắng nghe ân cần • Hỏi từng bước rõ ràng • Hỗ trợ pháp lý dân sinh 1-chạm 24/7")

# BANNER ĐỊNH HƯỚNG TRỌNG TÂM CÁ NHÂN & NGƯỜI DÂN
st.info(
    "🎯 **Định Hướng Trọng Tâm:** 👨‍👩‍👧 **Dành Cho Cá Nhân & Người Dân** — "
    "*Luật sư đồng hành lắng nghe, hỏi từng bước để nắm chắc sự việc, tuyệt đối không trả lời dồn dập. "
    "(Phạm vi Doanh nghiệp & Công ty đang được đặt ở chế độ chờ)*"
)

quick_prompt = None

# 📎 1. KHUNG NẠP TÀI LIỆU & ẢNH CHỨNG CỨ TRỰC TIẾP TRONG CHAT
with st.expander("📎 Nạp Tài Liệu & Ảnh Chứng Cứ (PDF, Word, Ảnh Giấy Nợ Viết Tay, Sổ Đỏ, Zalo)", expanded=False):
    st.caption("Tải lên hình ảnh hoặc tài liệu để AI bóc tách nội dung và chấm điểm giá trị chứng cứ theo BLTTDS 2015:")
    uploaded_ev_file = st.file_uploader(
        "Chọn file tài liệu hoặc ảnh chụp chứng cứ:",
        type=["pdf", "docx", "txt", "png", "jpg", "jpeg"],
        key="in_chat_file_uploader"
    )
    if uploaded_ev_file is not None:
        with st.spinner("Đang bóc tách văn bản và giám định giá trị chứng cứ..."):
            parse_res = st.session_state.evidence_parser.parse_uploaded_file(uploaded_ev_file)

        ev_col1, ev_col2 = st.columns([1, 2])
        with ev_col1:
            st.metric("Điểm Giá Trị Chứng Cứ", f"{parse_res['evidence_score']} / 100")
            st.markdown(f"**Xếp hạng:** `{parse_res['evidence_grade']}`")
        with ev_col2:
            st.info(f"💡 **Lời khuyên tố tụng:** {parse_res['action_advice']}")

        with st.expander("📄 Xem Nội dung Văn bản Bóc tách được từ tệp:", expanded=False):
            st.text_area("Trích xuất nội dung:", value=parse_res["extracted_text"][:2000], height=120)

        if st.button("💬 Đưa Tài Liệu Này Vào Cuộc Trò Chuyện Với Luật Sư", key="btn_send_file_to_chat"):
            quick_prompt = (
                f"Tôi vừa tải lên tài liệu/chứng cứ: '{parse_res['file_name']}'. "
                f"Nội dung bóc tách được tóm lược như sau:\n\"{parse_res['extracted_text'][:800]}\"\n"
                f"Xin Luật sư giám định và tư vấn quyền lợi pháp lý cho tôi dựa trên tài liệu này."
            )

# 🧮 2. HỘP CÔNG CỤ DÂN SINH 1-CHẠM (IN-CHAT TOOLBAR)
with st.expander("🧮 Hộp Công Cụ Dân Sinh 1-Chạm (Tính Án Phí • Xuất Đơn • Thời Hiệu • Thẩm Quyền • Giả Lập Tố Tụng • Trọn Bộ Hồ Sơ)", expanded=False):
    tool_tab1, tool_tab2, tool_tab3, tool_tab4, tool_tab5, tool_tab6 = st.tabs([
        "💰 1. Tính Án Phí Tòa Án (NQ 326)",
        "📝 2. Xuất Đơn Khởi Kiện (.docx)",
        "⏳ 3. Kiểm Tra Thời Hiệu Khởi Kiện",
        "🏛️ 4. Xác Định Thẩm Quyền Tiếp Nhận Đơn",
        "⚖️ 5. Giả Lập Bàn Cờ Tố Tụng 2 Chiều",
        "📦 6. Xuất Trọn Bộ Hồ Sơ Tố Tụng (.docx)"
    ])
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
        st.markdown("##### 📝 Xuất Đơn Khởi Kiện Chuẩn Mẫu 23-DS (Nghị quyết 01/2017/NQ-HĐTP)")
        st.caption("Điền thông tin cơ bản để AI lập tức đóng gói Đơn khởi kiện chuẩn nộp Tòa án:")
        pf_c1, pf_c2 = st.columns(2)
        with pf_c1:
            p_court = st.text_input("Tòa án nhân dân thụ lý:", value="TAND Quận 1, TP. Hồ Chí Minh", key="pf_court")
            p_pl_name = st.text_input("Họ tên Người khởi kiện:", value="Nguyễn Thị Lan", key="pf_pl_name")
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

    with tool_tab3:
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

    with tool_tab3:
        st.markdown("##### 🏛️ Tra Cứu Cơ Quan Thẩm Quyền Giải Quyết")
        auth_c1, auth_c2, auth_c3 = st.columns(3)
        with auth_c1:
            auth_type = st.selectbox("Dạng vụ việc:", ["Tranh chấp đất đai", "Đòi nợ / Hợp đồng", "Lừa đảo qua mạng"], key="auth_type_in")
        with auth_c2:
            auth_dist = st.text_input("Quận / Huyện của bên kia / nơi có đất:", value="Quận 1", key="auth_dist_in")
        with auth_c3:
            auth_prov = st.text_input("Tỉnh / Thành phố:", value="TP. Hồ Chí Minh", key="auth_prov_in")
        if st.button("Xác Định Cơ Quan Có Thẩm Quyền", key="btn_check_auth"):
            auth_res = CitizenLegalTools.locate_competent_authority(auth_type, auth_dist, auth_prov)
            st.success(f"📍 **Bước 1 (Tiếp nhận đầu tiên):** {auth_res['stage_1']}")
            st.caption(auth_res['stage_1_desc'])
            st.warning(f"⚖️ **Bước 2 (Giải quyết tiếp theo):** {auth_res['stage_2']}")
            st.caption(auth_res['stage_2_desc'])
            st.info(f"💡 **Mẹo dân sinh:** {auth_res['hotline_tip']}")

    with tool_tab5:
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
            
            # Hiển thị tỷ lệ thắng
            st.metric("🎯 Dự Báo Tỷ Lệ Thắng Kiện Tại Tòa", f"{sim_res['win_rate']}%", delta="Khả thi tố tụng")
            st.markdown(f"> 🏛️ **Dự báo phán quyết của Tòa:** *{sim_res['court_forecast']}*")

            col_att, col_def = st.columns(2)
            with col_att:
                st.success("⚔️ **MŨI TẤN CÔNG CỦA NGUYÊN ĐƠN (BẠN):**")
                for atk in sim_res["plaintiff_attack"]:
                    st.markdown(f"• {atk}")
            with col_def:
                st.error("🛡️ **CHIÊU BÀI PHẢN ĐÒN CỦA ĐỐI PHƯƠNG (CON NỢ/BỊ ĐƠN):**")
                for d_cnt in sim_res["defendant_counter"]:
                    st.markdown(f"• {d_cnt}")

            st.info("💡 **KẾ SÁCH HÓA GIẢI & CHIẾN THUẬT NẮM CHẮC CHIẾN THẮNG:**")
            for tac in sim_res["winning_tactics"]:
                st.markdown(f"👉 **{tac}**")

    with tool_tab6:
        st.markdown("##### 📦 Xuất Trọn Gói Bộ Hồ Sơ Tố Tụng Hoàn Chỉnh (Nộp TAND)")
        st.caption("Tự động kết hợp: Đơn khởi kiện chuẩn Mẫu 23-DS + Bảng tạm tính án phí NQ 326 + Báo cáo bàn cờ đối kháng 2 chiều + Danh mục chứng cứ vào 1 file Word .docx duy nhất:")
        
        dos_c1, dos_c2 = st.columns(2)
        with dos_c1:
            dos_court = st.text_input("Tòa án thụ lý:", value="Tòa án nhân dân Quận 1, TP. Hồ Chí Minh", key="dos_court_in")
            dos_plaintiff = st.text_input("Họ tên Người khởi kiện (Bạn):", value="Nguyễn Văn A", key="dos_plaintiff_in")
            dos_year = st.text_input("Năm sinh:", value="1985", key="dos_year_in")
            dos_id = st.text_input("Số CCCD:", value="079085012345", key="dos_id_in")
            dos_addr = st.text_input("Nơi cư trú người khởi kiện:", value="Số 123 Lê Lợi, Phường Bến Nghé, Quận 1, TP.HCM", key="dos_addr_in")
            dos_phone = st.text_input("Điện thoại liên hệ:", value="0901234567", key="dos_phone_in")
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

# GỢI Ý NHANH CÁC TÌNH HUỐNG THỰC TẾ DÂN SINH
st.markdown("💡 **Lối tắt tình huống đời sống thường gặp:**")
r1_col1, r1_col2, r1_col3 = st.columns(3)
r2_col1, r2_col2, r2_col3 = st.columns(3)

with r1_col1:
    if st.button("🏫 Bạo lực học đường (Trách nhiệm trường)"):
        quick_prompt = "Con tôi bị bạo lực học đường có thương tích nhưng nhà trường không chịu trách nhiệm vì nói xảy ra ngoài tầm mắt giáo viên. Luật sư cho tôi biết nhà trường có phải bồi thường không và thủ tục xử lý ra sao?"

with r1_col2:
    if st.button("🏡 Tranh chấp Sổ đỏ & Lấn chiếm ranh giới"):
        quick_prompt = "Hàng xóm nhà tôi xây hàng rào lấn sang đất của tôi hơn 1 mét rưỡi. Tôi đã có Sổ đỏ chính chủ. Tôi có cần hòa giải ở xã trước không và làm đơn gì?"

with r1_col3:
    if st.button("💸 Khởi kiện Đòi nợ khi Con nợ bỏ trốn"):
        quick_prompt = "Tôi có cho bạn vay 300 triệu có giấy nhận tiền và sao kê ngân hàng, nhưng nay đến hạn con nợ cắt liên lạc và bỏ trốn khỏi địa phương. Tôi muốn khởi kiện đòi nợ thì nộp đơn ở đâu?"

with r2_col1:
    if st.button("💔 Ly hôn, Chia tài sản & Quyền nuôi con"):
        quick_prompt = "Vợ chồng tôi muốn thuận tình ly hôn. Có 2 con (1 bé 2 tuổi, 1 bé 8 tuổi) và 1 căn nhà chung. Chúng tôi muốn làm đơn thỏa thuận phân chia quyền nuôi con và tài sản thì thủ tục thế nào?"

with r2_col2:
    if st.button("🛡️ Quét Hợp đồng Đối kháng (Phạt 15%)"):
        quick_prompt = "Hãy thẩm định hợp đồng mua bán này: 'Nếu Bên B chậm thanh toán thì phải chịu phạt vi phạm 15% tổng giá trị hợp đồng và bồi thường 100 triệu, đồng thời không áp dụng bất kỳ lý do bất khả kháng nào.'"

with r2_col3:
    if st.button("📝 Kích hoạt Form Soạn thảo Văn bản Thông minh"):
        quick_prompt = "Tôi muốn soạn thảo một văn bản pháp lý với mẫu điền sẵn căn cứ và placeholder thông tin cá nhân."

# HIỂN THỊ TOÀN BỘ LỊCH SỬ CHAT
for idx, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

        action_type = msg.get("action_type")
        action_data = msg.get("action_data")

        # 1. WIDGET QUÉT HỢP ĐỒNG 2 CHIỀU ĐỐI KHÁNG TRỰC TIẾP TRONG CHAT
        if action_type == "CONTRACT_AUDIT_ACTION" and action_data:
            with st.expander("🛡️ Thẻ Phân tích Đối kháng 2 Chiều & Báo cáo Thẩm định (.docx)", expanded=True):
                sc1, sc2 = st.columns([1, 2])
                with sc1:
                    st.metric("Điểm An toàn Pháp lý", f"{action_data.get('score', 0)} / 100")
                    st.markdown(f"**Xếp hạng:** {action_data.get('status_label', '')}")
                    st.markdown(f"**Số lỗ hổng phát hiện:** `{action_data.get('findings_count', 0)}`")
                with sc2:
                    docx_audit = st.session_state.contract_scanner.export_audit_report_docx(action_data)
                    st.download_button(
                        label="📥 Tải Báo cáo Thẩm định Đối kháng (.docx)",
                        data=docx_audit,
                        file_name=f"Bao_Cao_Tham_Dinh_Doi_Khang_{idx}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        key=f"dl_audit_{idx}"
                    )

                # Bảng Ma trận Đối kháng 2 Chiều trực quan
                findings = action_data.get("findings", [])
                if findings:
                    st.markdown("##### ⚖️ Ma trận Bóc tách Cạm bẫy 2 Chiều (Bilateral Exploitation):")
                    matrix_rows = []
                    for f in findings:
                        matrix_rows.append({
                            "Điều khoản / Căn cứ": f.get("legal_basis", ""),
                            "🔴 Bên ra luật lợi dụng gì?": f.get("issuer_exploitation", ""),
                            "🟡 Bên theo luật bị ép ra sao?": f.get("adherent_exploitation", ""),
                            "✍️ Điều khoản thay thế cân bằng": f.get("suggested_replacement", "")
                        })
                    st.table(pd.DataFrame(matrix_rows))

        # 2. WIDGET SOẠN THẢO VĂN BẢN THÔNG MINH (SMART PRE-FILLED FORM & PLACEHOLDERS)
        elif action_type == "DYNAMIC_DRAFT_ACTION":
            with st.expander("📝 Biểu mẫu Soạn thảo Văn bản Thông minh (Smart Pre-filled Form)", expanded=True):
                st.info(
                    "💡 **Cơ chế Form Thông minh:** Toàn bộ căn cứ pháp luật và nội dung tranh tụng chuẩn mực đã được AI điền sẵn 100%. "
                    "Bạn chỉ cần nhập các thông tin cá nhân bạn biết; **trường nào chưa rõ có thể để trống** — hệ thống sẽ tự động chèn dòng kẻ giữ chỗ "
                    "`........................` để bạn tải về in ra điền tay hoặc ký tên!"
                )

                case_id = (action_data or {}).get("case_id", "CUSTOM") if isinstance(action_data, dict) else "CUSTOM"

                # Chọn loại văn bản muốn xuất
                doc_options = {
                    "DEBT_COLLECTION": "1. Đơn khởi kiện đòi nợ khi con nợ bỏ trốn (Điều 463 BLDS, Điều 39 BLTTDS)",
                    "LAND_DISPUTE": "2. Đơn yêu cầu hòa giải tranh chấp ranh giới đất đai (Điều 202 Luật Đất đai)",
                    "SCHOOL_VIOLENCE": "3. Đơn khiếu nại bạo lực học đường & yêu cầu nhà trường bồi thường (Điều 599 BLDS)",
                    "DIVORCE_AND_CUSTODY": "4. Đơn thuận tình ly hôn, thỏa thuận quyền nuôi con & chia tài sản (Luật HNGĐ)",
                    "SERVICE_CONTRACT": "5. Hợp đồng dịch vụ thương mại cân bằng chuẩn mực (Luật Thương mại 2005)",
                    "CUSTOM": "6. Soạn thảo văn bản tùy chọn bất kỳ qua Trí tuệ AI"
                }

                default_key = case_id if case_id in doc_options else "DEBT_COLLECTION"
                selected_doc_key = st.selectbox(
                    "Chọn mẫu văn bản cần tải về:",
                    options=list(doc_options.keys()),
                    format_func=lambda k: doc_options[k],
                    index=list(doc_options.keys()).index(default_key),
                    key=f"sel_doc_{idx}"
                )

                # Form nhập thông tin nhân thân linh hoạt
                f_vals = {}
                with st.form(f"dynamic_form_{idx}"):
                    st.caption("*(Điền các trường bạn biết, để trống trường chưa biết để AI chèn dòng giữ chỗ)*")

                    if selected_doc_key == "DEBT_COLLECTION":
                        df_c1, df_c2 = st.columns(2)
                        with df_c1:
                            f_vals["court_name"] = st.text_input("Tòa án nhân dân tiếp nhận đơn:", placeholder="VD: TAND Quận 1, TP. Hồ Chí Minh", key=f"f_court_{idx}")
                            f_vals["plaintiff_name"] = st.text_input("Họ và tên Người khởi kiện (Chủ nợ):", placeholder="VD: Nguyễn Văn A", key=f"f_pl_name_{idx}")
                            f_vals["plaintiff_cccd"] = st.text_input("CCCD Chủ nợ:", placeholder="07920100xxxx", key=f"f_pl_cccd_{idx}")
                            f_vals["plaintiff_phone"] = st.text_input("Số điện thoại Chủ nợ:", placeholder="0912345678", key=f"f_pl_phone_{idx}")
                        with df_c2:
                            f_vals["defendant_name"] = st.text_input("Họ và tên Người bị kiện (Con nợ):", placeholder="VD: Trần Văn B", key=f"f_df_name_{idx}")
                            f_vals["defendant_address"] = st.text_input("Nơi cư trú cuối cùng của con nợ:", placeholder="Số 45 Lê Lợi, Phường Bến Nghé, Quận 1", key=f"f_df_addr_{idx}")
                            f_vals["principal_amount"] = st.text_input("Số tiền nợ gốc (VNĐ):", placeholder="VD: 300.000.000 VNĐ", key=f"f_amount_{idx}")
                            f_vals["interest_amount"] = st.text_input("Số tiền lãi yêu cầu tính thêm:", placeholder="VD: 15.000.000 VNĐ", key=f"f_interest_{idx}")
                            f_vals["total_amount"] = f_vals["principal_amount"]

                    elif selected_doc_key == "LAND_DISPUTE":
                        df_c1, df_c2 = st.columns(2)
                        with df_c1:
                            f_vals["ubnd_name"] = st.text_input("UBND cấp xã tiếp nhận đơn hòa giải:", placeholder="VD: UBND Phường Linh Trung, TP. Thủ Đức", key=f"f_ubnd_{idx}")
                            f_vals["applicant_name"] = st.text_input("Họ và tên người làm đơn:", placeholder="VD: Lê Thị C", key=f"f_app_name_{idx}")
                            f_vals["parcel_info"] = st.text_input("Thông tin thửa đất tranh chấp:", placeholder="Thửa đất số 12, Tờ bản đồ số 45", key=f"f_parcel_{idx}")
                        with df_c2:
                            f_vals["neighbor_name"] = st.text_input("Họ và tên hộ hàng xóm liền kề:", placeholder="VD: Hoàng Văn D", key=f"f_neighbor_{idx}")
                            f_vals["encroachment_desc"] = st.text_input("Mô tả hành vi lấn chiếm ranh giới:", placeholder="Xây tường rào lấn sang mốc giới 1.5 mét", key=f"f_encroach_{idx}")

                    elif selected_doc_key == "SCHOOL_VIOLENCE":
                        df_c1, df_c2 = st.columns(2)
                        with df_c1:
                            f_vals["school_name"] = st.text_input("Tên trường học xảy ra vụ việc:", placeholder="VD: Trường THCS Nguyễn Du", key=f"f_school_{idx}")
                            f_vals["parent_name"] = st.text_input("Họ tên phụ huynh đứng đơn:", placeholder="VD: Vũ Văn E", key=f"f_parent_{idx}")
                            f_vals["student_name"] = st.text_input("Họ tên học sinh bị bạo lực:", placeholder="VD: Cháu Vũ Minh F (Lớp 8A)", key=f"f_student_{idx}")
                        with df_c2:
                            f_vals["education_department"] = st.text_input("Phòng/Sở GD&ĐT quản lý:", placeholder="VD: Phòng GD&ĐT Quận 3", key=f"f_dept_{idx}")
                            f_vals["medical_cost"] = st.text_input("Chi phí y tế & viện phí yêu cầu bồi thường:", placeholder="VD: 25.000.000 VNĐ", key=f"f_med_cost_{idx}")

                    elif selected_doc_key == "DIVORCE_AND_CUSTODY":
                        df_c1, df_c2 = st.columns(2)
                        with df_c1:
                            f_vals["court_name"] = st.text_input("Tòa án nhân dân nộp đơn:", placeholder="VD: TAND Huyện Bình Chánh", key=f"f_div_court_{idx}")
                            f_vals["husband_name"] = st.text_input("Họ và tên Người chồng:", placeholder="VD: Đặng Văn G", key=f"f_husband_{idx}")
                            f_vals["wife_name"] = st.text_input("Họ và tên Người vợ:", placeholder="VD: Phạm Thị H", key=f"f_wife_{idx}")
                        with df_c2:
                            f_vals["custody_agreement"] = st.text_input("Thỏa thuận quyền nuôi con & cấp dưỡng:", placeholder="Mẹ nuôi con nhỏ 2 tuổi, cha cấp dưỡng 5 triệu/tháng", key=f"f_custody_{idx}")
                            f_vals["property_division"] = st.text_input("Thỏa thuận tài sản chung:", placeholder="Tự thỏa thuận không yêu cầu Tòa án giải quyết", key=f"f_prop_{idx}")

                    elif selected_doc_key == "SERVICE_CONTRACT":
                        df_c1, df_c2 = st.columns(2)
                        with df_c1:
                            f_vals["party_a_name"] = st.text_input("Bên A (Bên thuê dịch vụ):", placeholder="VD: CÔNG TY TNHH ALPHA", key=f"f_pa_{idx}")
                            f_vals["party_b_name"] = st.text_input("Bên B (Bên cung ứng dịch vụ):", placeholder="VD: CÔNG TY CP BETA", key=f"f_pb_{idx}")
                        with df_c2:
                            f_vals["service_scope"] = st.text_input("Phạm vi dịch vụ cung cấp:", placeholder="Thiết kế và triển khai phần mềm quản lý", key=f"f_scope_{idx}")
                            f_vals["contract_value"] = st.text_input("Giá trị hợp đồng:", placeholder="VD: 150.000.000 VNĐ", key=f"f_val_{idx}")

                    else:
                        f_vals["custom_prompt"] = st.text_area(
                            "Mô tả chi tiết văn bản pháp lý bạn muốn AI soạn thảo:",
                            value="Soạn thảo Giấy ủy quyền quản lý tài sản nhà đất hợp pháp có điều khoản giới hạn phạm vi ủy quyền.",
                            key=f"f_custom_{idx}"
                        )

                    btn_generate = st.form_submit_button("⚡ Cập nhật & Tạo Văn bản (.docx)")

                # Xử lý xuất file Word (.docx) an toàn không giật lag
                if selected_doc_key == "DEBT_COLLECTION":
                    doc_blob = st.session_state.dynamic_drafter.draft_debt_lawsuit(f_vals)
                    file_title = "Don_Khoi_Kien_Doi_No.docx"

                elif selected_doc_key == "LAND_DISPUTE":
                    doc_blob = st.session_state.dynamic_drafter.draft_land_dispute(f_vals)
                    file_title = "Don_Yeu_Cau_Hoa_Giai_Dat_Dai.docx"

                elif selected_doc_key == "SCHOOL_VIOLENCE":
                    doc_blob = st.session_state.dynamic_drafter.draft_school_violence_complaint(f_vals)
                    file_title = "Don_Khieu_Nai_Bao_Luc_Hoc_Duong.docx"

                elif selected_doc_key == "DIVORCE_AND_CUSTODY":
                    doc_blob = st.session_state.dynamic_drafter.draft_divorce_petition(f_vals)
                    file_title = "Don_Thuan_Tinh_Ly_Hon.docx"

                elif selected_doc_key == "SERVICE_CONTRACT":
                    doc_blob = st.session_state.dynamic_drafter.draft_service_contract(f_vals)
                    file_title = "Hop_Dong_Dich_Vu_Thuong_Mai.docx"

                else:
                    cust_key = f"cust_blob_{idx}"
                    if btn_generate or cust_key not in st.session_state:
                        st.session_state[cust_key] = st.session_state.dynamic_drafter.draft_custom_document(
                            f_vals.get("custom_prompt", "Văn bản pháp lý theo yêu cầu")
                        )
                    doc_blob = st.session_state[cust_key]
                    file_title = "Van_Ban_Phap_Ly_Theo_Yeu_Cau.docx"

                st.download_button(
                    label=f"📥 Tải ngay File Word: {file_title}",
                    data=doc_blob,
                    file_name=file_title,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    key=f"dl_dynamic_doc_{idx}"
                )

        # 3. WIDGET SOẠN HỒ SƠ DOANH NGHIỆP TRONG CHAT
        elif action_type == "DOSSIER_CREATION_ACTION":
            with st.expander("📝 Form Tạo Nhanh Bộ Hồ sơ Thành lập Doanh nghiệp", expanded=True):
                st.info("Nhấn nút bên dưới để tạo và tải về trọn bộ file Word mẫu chuẩn quy định của Bộ KH&ĐT:")
                default_dossier = {
                    "company_name": "CÔNG TY TNHH CÔNG NGHỆ NHỰT AI",
                    "entity_type_label": "Công ty TNHH 1 Thành viên",
                    "city": "TP. Hồ Chí Minh",
                    "address_street": "123 Đường Nguyễn Huệ",
                    "address_ward": "Phường Bến Nghé",
                    "address_district": "Quận 1",
                    "main_industry_name": "Lập trình máy vi tính (AI & SaaS)",
                    "main_industry_code": "6201",
                    "charter_capital": 500000000,
                    "charter_capital_in_words": "Năm trăm triệu đồng",
                    "rep_name": "Nguyễn Văn Nhựt",
                    "rep_title": "Giám đốc",
                    "rep_gender": "Nam",
                    "rep_dob": "15/08/2000",
                    "rep_phone": "0912345678",
                    "rep_email": "nhut@techai.vn",
                    "rep_cccd": "079201004567",
                    "rep_cccd_date": "10/05/2022",
                    "rep_cccd_place": "Cục Cảnh sát QLHC về trật tự xã hội",
                    "rep_permanent_address": "TP. Hồ Chí Minh",
                    "rep_current_address": "TP. Hồ Chí Minh"
                }
                doc_buf = generate_full_dossier_docx(default_dossier)
                st.download_button(
                    label="📦 Tải Trọn bộ Hồ sơ Mẫu ĐKDN (.docx)",
                    data=doc_buf,
                    file_name=f"Tron_Bo_Ho_So_DKDN_Mau_{idx}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    key=f"dl_dossier_{idx}"
                )

        # 4. HIỂN THỊ CITATIONS XÁC THỰC
        citations = msg.get("citations", [])
        if citations:
            with st.expander(f"📖 Căn cứ pháp luật trích dẫn ({len(citations)} tài liệu kiểm chứng)"):
                for c in citations:
                    if isinstance(c, dict):
                        st.markdown(f"**📌 {c.get('law_title', 'Văn bản quy phạm')} - {c.get('article', '')}**")
                        if c.get("header"):
                            st.caption(f"Tiêu đề: *{c.get('header')}*")
                        if c.get("text_snippet"):
                            st.info(f"\"{c.get('text_snippet')}\"")
                        verify_url = c.get("verify_url", "https://vanban.chinhphu.vn/")
                        st.markdown(f"[🔗 Kiểm chứng tại Cổng Thông tin điện tử Chính phủ]({verify_url})")
                        st.markdown("---")
                    else:
                        st.markdown(f"- `{c}`")

        if msg["role"] == "assistant" and msg.get("content") and not msg.get("content", "").startswith("👋"):
            with st.expander("☕ Xem Diễn giải sang Ngôn ngữ Bình dân (Dễ hiểu cho người dân)", expanded=False):
                plain_cached_key = f"plain_cache_{idx}"
                if plain_cached_key not in st.session_state:
                    with st.spinner("Đang chuyển hóa sang văn phong bình dân gần gũi..."):
                        st.session_state[plain_cached_key] = st.session_state.plain_engine.translate_to_plain_language(msg["content"])
                st.markdown(st.session_state[plain_cached_key])

            # 🔊 TÍCH HỢP TRỢ LÝ PHÁT THANH ÂM THANH (TTS) CHO NGƯỜI CAO TUỔI / MẮT KÉM
            tts_cache_key = f"tts_audio_{idx}"
            tts_btn_key = f"tts_btn_{idx}"
            if tts_cache_key not in st.session_state:
                if st.button("🔊 Đọc to lời giải thích bằng giọng nói (Tiếng Việt)", key=tts_btn_key, help="Dành cho người già, người khiếm thị hoặc người mắt kém"):
                    with st.spinner("Đang chuyển đổi câu trả lời thành giọng đọc truyền cảm..."):
                        audio_fp = VoiceNarrator.generate_speech(msg["content"])
                        if audio_fp:
                            st.session_state[tts_cache_key] = audio_fp.read()
                            st.rerun()
            else:
                st.markdown("🔊 **Giọng đọc phát thanh viên Luật sư:**")
                st.audio(st.session_state[tts_cache_key], format="audio/mp3")

        if msg.get("quick_options") and idx == len(st.session_state.messages) - 1:
            st.markdown("👉 **Lựa chọn nhanh (Bấm 1 chạm để trả lời ngay):**")
            q_cols = st.columns(min(len(msg["quick_options"]), 4))
            for q_i, opt in enumerate(msg["quick_options"]):
                with q_cols[q_i % len(q_cols)]:
                    if st.button(opt, key=f"qopt_click_{idx}_{q_i}", use_container_width=True):
                        st.session_state.pending_quick_input = opt
                        st.rerun()

        if msg.get("suggested_followups") and idx == len(st.session_state.messages) - 1:
            st.markdown("💡 **Câu hỏi gợi ý bạn có thể hỏi Luật sư (Bấm 1 chạm):**")
            s_cols = st.columns(min(len(msg["suggested_followups"]), 3))
            for s_i, fq in enumerate(msg["suggested_followups"][:3]):
                with s_cols[s_i % len(s_cols)]:
                    if st.button(fq, key=f"fq_click_{idx}_{s_i}", use_container_width=True):
                        st.session_state.pending_quick_input = fq
                        st.rerun()

        if msg.get("agent") and msg["role"] == "assistant":
            st.caption(f"🤖 Xử lý bởi Agent: **{msg['agent']}**")

# KIỂM TRA LỰA CHỌN BẤM NHANH TỪ GIAO DIỆN
if "pending_quick_input" in st.session_state and st.session_state.pending_quick_input:
    quick_prompt = st.session_state.pending_quick_input
    st.session_state.pending_quick_input = None

# HỖ TRỢ NHẬP LIỆU BẰNG GIỌNG NÓI DÀNH CHO NGƯỜI CAO TUỔI
with st.expander("🎙️ Nhập Liệu Bằng Giọng Nói (Dành cho Người già / Mắt kém / Không tiện gõ phím)", expanded=False):
    st.caption("Bấm nút micro để thu âm lời nói của bạn, sau đó bấm 'Gửi Lời Nói Đến Luật Sư':")
    audio_val = st.audio_input("Thu âm lời nói của bạn:")
    if audio_val is not None:
        st.audio(audio_val)
        if st.button("📤 Gửi Lời Nói Đến Luật Sư", key="btn_send_voice_audio"):
            quick_prompt = "Tôi gửi lời nói trình bày: Tôi đang gặp khúc mắc pháp lý đời sống, nhờ Luật sư lắng nghe và hỏi từng bước để tháo gỡ giúp tôi."

# XỬ LÝ INPUT TỪ CHAT BOX HOẶC QUICK ACTION
user_input = st.chat_input("Hỏi luật sư, yêu cầu soạn đơn từ, hoặc dán điều khoản hợp đồng cần thẩm định...")
if quick_prompt:
    user_input = quick_prompt

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Luật sư Dân gian đang lắng nghe và suy ngẫm tình huống của bạn..."):
            intake_res = st.session_state.citizen_intake.respond(user_input, st.session_state.messages)

        resp_text = intake_res["response"]
        quick_opts = intake_res.get("quick_options", [])
        st.markdown(resp_text)

        # Lựa chọn trả lời nhanh
        if quick_opts:
            st.markdown("👉 **Gợi ý lựa chọn nhanh (Bấm 1 chạm để trả lời ngay):**")
            btn_cols = st.columns(len(quick_opts))
            for q_i, opt in enumerate(quick_opts):
                with btn_cols[q_i]:
                    if st.button(opt, key=f"qopt_live_{q_i}", use_container_width=True):
                        st.session_state.pending_quick_input = opt
                        st.rerun()

        suggested_followups = intake_res.get("suggested_followups", [])
        if suggested_followups:
            st.markdown("💡 **Câu hỏi đào sâu bạn có thể hỏi Luật sư ngay (Bấm 1 chạm):**")
            s_cols = st.columns(min(len(suggested_followups), 3))
            for s_i, fq in enumerate(suggested_followups[:3]):
                with s_cols[s_i % len(s_cols)]:
                    if st.button(fq, key=f"fq_live_{s_i}", use_container_width=True):
                        st.session_state.pending_quick_input = fq
                        st.rerun()

        # Tra cứu sâu điều luật & giải pháp tố tụng (Ẩn trong Expander để không làm rối mắt người dân)
        with st.expander("⚖️ Xem Thêm Căn Cứ Điều Luật & Hồ Sơ Đính Kèm (Tra Cứu Sâu)", expanded=False):
            with st.spinner("Đang liên kết mạng lưới LangGraph để rà soát quy phạm..."):
                result = st.session_state.workflow.process(user_input)

            full_legal_text = result["response"]
            st.markdown(full_legal_text)

            citations = result.get("citations", [])
            action_type = result.get("action_type")
            action_data = result.get("action_data")

            if action_type == "CONTRACT_AUDIT_ACTION" and action_data:
                sc1, sc2 = st.columns([1, 2])
                with sc1:
                    st.metric("Điểm An toàn Pháp lý", f"{action_data.get('score', 0)} / 100")
                with sc2:
                    docx_audit = st.session_state.contract_scanner.export_audit_report_docx(action_data)
                    st.download_button(
                        label="📥 Tải Báo cáo Thẩm định Đối kháng (.docx)",
                        data=docx_audit,
                        file_name="Bao_Cao_Tham_Dinh_Doi_Khang.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    )

            if citations:
                st.markdown("#### 📖 Văn bản quy phạm pháp luật kiểm chứng:")
                for c in citations:
                    if isinstance(c, dict):
                        st.markdown(f"**📌 {c.get('law_title', 'Văn bản quy phạm')} - {c.get('article', '')}**")
                        verify_url = c.get("verify_url", "https://vanban.chinhphu.vn/")
                        st.markdown(f"[🔗 Kiểm chứng tại Cổng Thông tin điện tử Chính phủ]({verify_url})")

        st.caption("🤖 Xử lý bởi: **CitizenIntakeAgent (Luật sư Thăm khám Dân gian)** • Định hướng: Cá nhân & Người dân")

        st.session_state.messages.append({
            "role": "assistant",
            "content": resp_text,
            "agent": "CitizenIntakeAgent",
            "quick_options": quick_opts,
            "suggested_followups": suggested_followups,
            "citations": citations if 'citations' in locals() else [],
            "action_type": action_type if 'action_type' in locals() else None,
            "action_data": action_data if 'action_data' in locals() else None
        })

