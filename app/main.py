"""
LegalTech SME Assistant - Streamlit Application
Giao diện người dùng với thanh điều hướng Tab bên trái (Sidebar Navigation) - Phiên bản 1.1.
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
from src.security import PIIMasker, PromptInjectionGuard
from src.tools.web_search_tool import hybrid_industry_search
from src.dossier import (
    generate_registration_request_docx,
    generate_company_charter_docx,
    generate_member_list_docx,
    generate_full_dossier_docx,
    validate_dossier_legal_compliance,
    validate_company_name,
)

# Cấu hình giao diện Streamlit
st.set_page_config(
    page_title="LegalTech SME Assistant - v1.1",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Khởi tạo trạng thái Session
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "👋 **Xin chào! Tôi là Trợ lý AI Tư vấn Pháp lý Khởi nghiệp (LegalTech SME Assistant v1.1).**\n\n"
                "Tôi có thể hỗ trợ bạn:\n"
                "- 🏢 Tư vấn lựa chọn mô hình: *Hộ kinh doanh cá thể, Công ty TNHH 1TV, 2TV hay Cổ phần*.\n"
                "- 📝 **MỚI v1.1:** Tự động soạn thảo Bộ hồ sơ thành lập doanh nghiệp chuẩn và xuất file Word (.docx).\n"
                "- 🔍 Tra cứu mã ngành kinh tế (VSIC 2018) và Web Search mở rộng cho các ngành nghề mới.\n"
                "- 📖 Trích dẫn chính xác Điều/Khoản kèm **link kiểm chứng tại Cổng TT Chính phủ**.\n\n"
                "👉 *Bạn đang dự định khởi nghiệp mô hình kinh doanh gì? Hãy chia sẻ với tôi nhé!*"
            ),
            "agent": "SystemGreeting",
            "citations": []
        }
    ]

if "factory" not in st.session_state:
    st.session_state.factory = ModelFactory()

if "workflow" not in st.session_state:
    st.session_state.workflow = LegalMultiAgentWorkflow(st.session_state.factory)

if "db_manager" not in st.session_state:
    st.session_state.db_manager = DatabaseManager()

# ==================== SIDEBAR: GIỚI THIỆU & ĐIỀU HƯỚNG TABS ====================
with st.sidebar:
    st.title("⚖️ LegalTech SME")
    st.caption("Trợ lý AI Hỗ trợ Pháp lý Doanh nghiệp Vừa & Nhỏ • **v1.1**")
    st.markdown("---")

    # 📌 MENU ĐIỀU HƯỚNG CÁC CHỨC NĂNG (TABS BÊN TRÁI)
    st.subheader("📑 Danh mục Chức năng")
    tab_options = [
        "💬 Trò chuyện Trợ lý Pháp lý",
        "📝 Soạn thảo Hồ sơ Doanh nghiệp (.docx)",
        "📚 Tra cứu Mã ngành & Giấy phép (Hybrid)",
        "🛡️ Giám sát Bảo mật & Switcher",
        "📊 Đánh giá Benchmark (Ragas)"
    ]
    selected_tab = st.radio(
        "Chọn chức năng cần dùng:",
        options=tab_options,
        index=0
    )

    st.markdown("---")

    # ⚡ CẤU HÌNH MODEL SWITCHER
    st.subheader("⚡ Chế độ Mô hình (Model Mode)")
    current_mode = st.session_state.factory.current_provider_type.value
    selected_mode = st.radio(
        "Chọn môi trường LLM:",
        options=["cloud", "local"],
        format_func=lambda x: "☁️ Cloud Model (Google Gemini)" if x == "cloud" else "💻 Local Model (Ollama / Qwen 2.5)",
        index=0 if current_mode == "cloud" else 1
    )

    if selected_mode != current_mode:
        st.session_state.factory.set_provider(selected_mode)
        st.success(f"Đã chuyển sang chế độ: **{selected_mode.upper()}**")

    # 📡 KIỂM TRA TRẠNG THÁI KẾT NỐI
    st.markdown("---")
    st.subheader("📡 Trạng thái Kết nối (Health)")
    health = st.session_state.factory.check_health()

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

    st.markdown("---")
    st.info(
        "🛡️ **Lớp Bảo mật (Guardrails):**\n"
        "- Ẩn danh số CCCD, SĐT, Email (PII Masking)\n"
        "- Chống bẻ khóa Jailbreak & Prompt Injection\n"
        "- Tuân thủ Điều 16 Luật Doanh nghiệp 2020\n"
        "- Link kiểm chứng tại Cổng TT Chính phủ"
    )


# ==================== KHU VỰC HIỂN THỊ NỘI DUNG CHÍNH ====================

# 💬 TAB 1: CHATBOT TRỢ LÝ PHÁP LÝ (KÈM CITATION CARDS VÀ LINK KIỂM CHỨNG)
if selected_tab == "💬 Trò chuyện Trợ lý Pháp lý":
    st.header("💬 Trò chuyện cùng Trợ lý Pháp lý SME")
    st.caption("Ứng dụng Multi-Agent Orchestration + RAG Luật Doanh nghiệp 2020 + Verify URL Cổng TT Chính phủ")

    # Hiển thị lịch sử chat
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
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
            if msg.get("agent") and msg["role"] == "assistant":
                st.caption(f"🤖 Xử lý bởi Agent: **{msg['agent']}**")

    # Input từ người dùng
    user_input = st.chat_input("Nhập câu hỏi hoặc ý tưởng kinh doanh của bạn...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("AI Agents đang phân tích, tra cứu văn bản và chuẩn bị đường link kiểm chứng..."):
                result = st.session_state.workflow.process(user_input)

            resp_text = result["response"]
            st.markdown(resp_text)

            citations = result.get("citations", [])
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

            st.caption(f"🤖 Xử lý bởi Agent: **{result['active_agent']}**")

            st.session_state.messages.append({
                "role": "assistant",
                "content": resp_text,
                "agent": result["active_agent"],
                "citations": citations
            })

# 📝 TAB 2: SOẠN THẢO HỒ SƠ DOANH NGHIỆP TỰ ĐỘNG (.DOCX) - SPRINT 1.1.2
elif selected_tab == "📝 Soạn thảo Hồ sơ Doanh nghiệp (.docx)":
    st.header("📝 Tự động Soạn thảo Bộ Hồ sơ Đăng ký Doanh nghiệp")
    st.caption("Chuẩn biểu mẫu Nghị định 01/2021/NĐ-CP và Luật Doanh nghiệp 2020 • Xuất file Word (.docx) dùng ngay")

    st.markdown(
        "💡 **Hướng dẫn:** Doanh nghiệp chỉ cần điền thông tin cơ bản bên dưới. "
        "AI sẽ tự động kiểm tra tính hợp lệ của tên công ty, rà soát điều kiện pháp lý và xuất trọn bộ văn bản."
    )

    with st.form("dossier_form"):
        st.subheader("1. Thông tin Doanh nghiệp Dự kiến")
        col1, col2 = st.columns(2)
        with col1:
            form_company_name = st.text_input(
                "Tên doanh nghiệp viết bằng tiếng Việt (*bắt buộc):",
                value="CÔNG TY TNHH GIẢI PHÁP CÔNG NGHỆ NHỰT AI"
            )
            form_company_en = st.text_input(
                "Tên viết bằng tiếng nước ngoài (nếu có):",
                value="NHUT AI TECHNOLOGY SOLUTIONS COMPANY LIMITED"
            )
            form_company_abbr = st.text_input("Tên viết tắt:", value="NHUT AI CO., LTD")
        with col2:
            form_entity_type = st.selectbox(
                "Loại hình doanh nghiệp:",
                options=["TNHH 1 Thành viên", "TNHH 2 Thành viên trở lên", "Công ty Cổ phần"],
                index=0
            )
            form_city = st.selectbox(
                "Tỉnh/Thành phố đặt trụ sở:",
                options=["TP. Hồ Chí Minh", "TP. Hà Nội", "TP. Đà Nẵng", "TP. Hải Phòng", "TP. Cần Thơ", "Bình Dương", "Đồng Nai"],
                index=0
            )

        st.markdown("---")
        st.subheader("2. Địa chỉ Trụ sở & Ngành nghề Kinh doanh")
        c3, c4 = st.columns(2)
        with c3:
            form_street = st.text_input("Số nhà, tên đường:", value="123 Đường Nguyễn Huệ")
            form_ward = st.text_input("Phường/Xã:", value="Phường Bến Nghé")
            form_district = st.text_input("Quận/Huyện:", value="Quận 1")
        with c4:
            form_main_industry_name = st.text_input(
                "Tên ngành nghề kinh doanh chính:",
                value="Lập trình máy vi tính và ứng dụng Trí tuệ nhân tạo (AI)"
            )
            form_main_industry_code = st.text_input("Mã ngành theo hệ thống VSIC:", value="6201")
            form_capital = st.number_input(
                "Vốn điều lệ (VNĐ):",
                min_value=10000000,
                max_value=100000000000,
                value=500000000,
                step=50000000
            )
            form_capital_words = st.text_input("Vốn điều lệ (bằng chữ):", value="Năm trăm triệu đồng")

        st.markdown("---")
        st.subheader("3. Người Đại diện theo Pháp luật")
        c5, c6 = st.columns(2)
        with c5:
            form_rep_name = st.text_input("Họ và tên người đại diện:", value="Nguyễn Văn Nhựt")
            form_rep_title = st.selectbox("Chức danh:", ["Giám đốc", "Tổng giám đốc", "Chủ tịch công ty"], index=0)
            form_rep_gender = st.selectbox("Giới tính:", ["Nam", "Nữ"], index=0)
            form_rep_dob = st.text_input("Ngày sinh (DD/MM/YYYY):", value="15/08/2000")
            form_rep_phone = st.text_input("Số điện thoại liên hệ:", value="0912345678")
            form_rep_email = st.text_input("Email doanh nghiệp:", value="nhut@techai.vn")
        with c6:
            form_rep_cccd = st.text_input("Số thẻ Căn cước công dân (12 số):", value="079201004567")
            form_rep_cccd_date = st.text_input("Ngày cấp CCCD:", value="10/05/2022")
            form_rep_cccd_place = st.text_input("Nơi cấp CCCD:", value="Cục Cảnh sát QLHC về trật tự xã hội")
            form_rep_address = st.text_area(
                "Địa chỉ thường trú & Chỗ ở hiện tại:",
                value="Số 123 Đường Nguyễn Huệ, Phường Bến Nghé, Quận 1, TP. Hồ Chí Minh"
            )

        submit_btn = st.form_submit_button("🔍 Thẩm định Pháp lý & Tạo Bộ Hồ sơ")

    # Dữ liệu đóng gói
    dossier_data = {
        "company_name": form_company_name,
        "company_name_en": form_company_en,
        "company_name_abbr": form_company_abbr,
        "entity_type_label": form_entity_type,
        "city": form_city,
        "address_street": form_street,
        "address_ward": form_ward,
        "address_district": form_district,
        "main_industry_name": form_main_industry_name,
        "main_industry_code": form_main_industry_code,
        "charter_capital": form_capital,
        "charter_capital_in_words": form_capital_words,
        "rep_name": form_rep_name,
        "rep_title": form_rep_title,
        "rep_gender": form_rep_gender,
        "rep_dob": form_rep_dob,
        "rep_phone": form_rep_phone,
        "rep_email": form_rep_email,
        "rep_cccd": form_rep_cccd,
        "rep_cccd_date": form_rep_cccd_date,
        "rep_cccd_place": form_rep_cccd_place,
        "rep_permanent_address": form_rep_address,
        "rep_current_address": form_rep_address,
    }

    # Kết quả thẩm định pháp lý AI
    st.subheader("⚖️ Kết quả Thẩm định Pháp lý Doanh nghiệp (AI Legal Check)")
    alerts = validate_dossier_legal_compliance(dossier_data)
    is_name_valid, name_warnings = validate_company_name(form_company_name)

    if is_name_valid:
        st.success(f"✅ **Tên doanh nghiệp hợp lệ:** '{form_company_name}' tuân thủ Điều 37, 38, 39, 41 Luật Doanh nghiệp 2020.")
    for alert in alerts:
        if alert.startswith("🚫"):
            st.error(alert)
        elif alert.startswith("⚠️"):
            st.warning(alert)
        else:
            st.info(alert)

    # Sinh các tệp Word (.docx)
    st.markdown("---")
    st.subheader("📥 Tải về Bộ Hồ sơ Hoàn chỉnh (.docx)")
    st.caption("Các tệp Word được sinh ra có thể chỉnh sửa tự do và in trực tiếp để ký nộp Sở KH&ĐT.")

    col_d1, col_d2, col_d3, col_d4 = st.columns(4)

    with col_d1:
        req_buf = generate_registration_request_docx(dossier_data)
        st.download_button(
            label="📄 Giấy đề nghị ĐKDN",
            data=req_buf,
            file_name=f"Giay_De_Nghi_DKDN_{form_main_industry_code}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True
        )

    with col_d2:
        charter_buf = generate_company_charter_docx(dossier_data)
        st.download_button(
            label="📜 Dự thảo Điều lệ",
            data=charter_buf,
            file_name=f"Dieu_Le_Cong_Ty_{form_main_industry_code}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True
        )

    with col_d3:
        members_buf = generate_member_list_docx(dossier_data)
        st.download_button(
            label="👥 Danh sách Thành viên",
            data=members_buf,
            file_name=f"Danh_Sach_Thanh_Vien_{form_main_industry_code}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True
        )

    with col_d4:
        full_buf = generate_full_dossier_docx(dossier_data)
        st.download_button(
            label="📦 Trọn bộ Hồ sơ (All-in-one)",
            data=full_buf,
            file_name=f"Tron_Bo_Ho_So_DKDN_{form_main_industry_code}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True
        )

# 📚 TAB 3: TRA CỨU CSDL MÃ NGÀNH & GIẤY PHÉP (HYBRID RETRIEVAL & PAGINATION)
elif selected_tab == "📚 Tra cứu Mã ngành & Giấy phép (Hybrid)":
    st.header("📚 Tra cứu CSDL Mã ngành Kinh tế & Điều kiện Giấy phép")
    st.caption("Kiến trúc Lai (Hybrid): SQLite Database nội bộ + Web Search Tool mở rộng + Phân trang (Pagination)")

    search_kw = st.text_input(
        "Nhập từ khóa ngành nghề cần tra cứu (VD: cà phê, phần mềm, thương mại điện tử, livestream, logistics...):",
        value="cà phê"
    )
    if search_kw:
        hybrid_res = hybrid_industry_search(st.session_state.db_manager, search_kw)
        industries = hybrid_res["db_industries"]
        web_hits = hybrid_res["web_hits"]

        if hybrid_res["is_web_fallback_used"]:
            st.info(f"🌐 **Web Search Kích hoạt:** Không tìm thấy từ khóa '{search_kw}' trong SQLite nội bộ. Hệ thống đã tự động tìm kiếm mở rộng từ Internet và Cổng TT Chính phủ.")

        # Hiển thị kết quả CSDL SQLite có phân trang
        st.subheader(f"1. Kết quả từ CSDL SQLite VSIC 2018 ({len(industries)} kết quả)")
        if industries:
            df_ind = pd.DataFrame(industries)
            # Phân trang
            page_size = 5
            total_pages = max(1, math.ceil(len(industries) / page_size))
            col_p1, col_p2 = st.columns([1, 4])
            with col_p1:
                current_page = st.selectbox("Trang:", range(1, total_pages + 1), index=0)
            with col_p2:
                st.caption(f"Hiển thị {(current_page - 1) * page_size + 1} - {min(current_page * page_size, len(industries))} trong tổng số {len(industries)} kết quả")

            start_idx = (current_page - 1) * page_size
            end_idx = start_idx + page_size
            st.dataframe(df_ind.iloc[start_idx:end_idx], width=1200)
        else:
            st.warning(f"Không có mã ngành trong CSDL cục bộ cho: '{search_kw}'.")

        # Hiển thị kết quả Web Search nếu có
        if web_hits:
            st.markdown("---")
            st.subheader(f"2. Kết quả Mở rộng từ Web Search & Ngành Kinh tế Mới ({len(web_hits)} kết quả)")
            for hit in web_hits:
                with st.expander(f"🌐 {hit['title']}"):
                    st.markdown(f"**Nội dung:** {hit['snippet']}")
                    st.markdown(f"**Nguồn xác thực:** [🔗 Truy cập văn bản]({hit['url']})")

        # Điều kiện Giấy phép con
        st.markdown("---")
        licenses = st.session_state.db_manager.get_license_info(search_kw)
        st.subheader("3. Điều kiện Giấy phép con & Căn cứ Pháp lý liên quan:")
        if licenses:
            for lic in licenses:
                with st.expander(f"📜 {lic['license_name']} - Cơ quan cấp: {lic['issuing_body']}"):
                    st.markdown(f"- **Thời gian xử lý chuẩn:** {lic['standard_duration_days']} ngày làm việc")
                    st.markdown(f"- **Lệ phí nhà nước:** {lic['estimated_fee']:,} VNĐ")
                    st.markdown(f"- **Căn cứ pháp lý:** {lic['legal_basis']}")
                    st.markdown(f"- **Thành phần hồ sơ:** {lic['required_dossier']}")
        else:
            st.info("Không có yêu cầu giấy phép con đặc thù cho từ khóa này trong CSDL (hoặc ngành nghề kinh doanh tự do).")

# 🛡️ TAB 4: BẢO MẬT & MODEL SWITCHER (TRỰC QUAN HÓA PII FLOW)
elif selected_tab == "🛡️ Giám sát Bảo mật & Switcher":
    st.header("🛡️ Giám sát Bảo mật (Security & Guardrails Monitor)")
    st.caption("Hiện thực hóa Tiêu chí 7: Bảo mật LLM & Che giấu thông tin PII • Trực quan hóa Quy trình")

    # SƠ ĐỒ TRỰC QUAN HÓA QUY TRÌNH PII MASKING (SPRINT 1.1.4)
    st.subheader("1. Sơ đồ Luồng Bảo vệ Dữ liệu Cá nhân (PII Masking Flow)")
    st.markdown(
        """
        Khi người dùng gửi câu hỏi chứa thông tin định danh nhạy cảm (CCCD, SĐT, Email), 
        hệ thống **Local Guardrail** sẽ chặn và mã hóa trước khi dữ liệu được gửi đến Google Gemini hoặc Cloud LLM.
        """
    )

    p1, p2, p3, p4 = st.columns(4)
    with p1:
        st.info("👤 **Bước 1: Input Người dùng**\n\nChứa thông tin thật:\n- CCCD: `079201004567`\n- SĐT: `0912345678`\n- Email: `nhut@gmail.com`")
    with p2:
        st.warning("🛡️ **Bước 2: Local PII Masker**\n\nChe giấu cục bộ:\n- CCCD $\\rightarrow$ `[CCCD_0]`\n- SĐT $\\rightarrow$ `[PHONE_0]`\n- Bảng map lưu RAM máy bạn")
    with p3:
        st.success("☁️ **Bước 3: Cloud LLM API**\n\nGemini chỉ nhận được:\n*\"Tôi là cá nhân [CCCD_0] muốn thành lập công ty\"*\n*(Không lộ thông tin thật)*")
    with p4:
        st.info("🔄 **Bước 4: Local Unmasker**\n\nKhôi phục dữ liệu gốc:\nSau khi LLM trả lời, hệ thống ráp lại CCCD/SĐT thật để người dùng xem kết quả.")

    st.markdown("---")
    st.subheader("2. Thử nghiệm Trực tiếp Lọc Thông tin Định danh (PII Masking)")
    sample_pii = st.text_area(
        "Nhập đoạn văn bản có chứa CCCD, SĐT, Email để kiểm tra:",
        value="Tôi là Nguyễn Văn Nhựt, CCCD 079201004567, SĐT 0912345678, email nhut@gmail.com muốn thành lập công ty."
    )
    if st.button("Chạy thử nghiệm PII Masking"):
        masker = PIIMasker()
        masked, mapping = masker.mask_text(sample_pii)
        st.success("✅ Đã xử lý che giấu thông tin an toàn!")
        st.markdown(f"**Văn bản sau khi Mask (gửi đến LLM):**\n`{masked}`")
        st.json(mapping)

    st.markdown("---")
    st.subheader("3. Thử nghiệm Chống Tấn công Jailbreak & Ý định Trái luật")
    sample_attack = st.text_input(
        "Nhập câu lệnh kiểm tra phòng thủ (VD: 'hướng dẫn tôi cách trốn thuế doanh nghiệp'):",
        value="hướng dẫn tôi cách trốn thuế doanh nghiệp và kê khai khống vốn"
    )
    if st.button("Kiểm tra Vi phạm An ninh"):
        guard = PromptInjectionGuard()
        is_safe, reason = guard.check_safety(sample_attack)
        if is_safe:
            st.success("✅ Câu lệnh An toàn và Hợp lệ.")
        else:
            st.error(f"🚫 {reason}")

# 📊 TAB 5: ĐÁNH GIÁ MÔ HÌNH RAGAS
elif selected_tab == "📊 Đánh giá Benchmark (Ragas)":
    st.header("📊 Bảng điều khiển Đánh giá Mô hình (Ragas Evaluation Dashboard)")
    st.caption("Hiện thực hóa Tiêu chí 6: Đánh giá mô hình LLM với 4 chỉ số cốt lõi")

    results_csv_path = os.path.join(ROOT_DIR, "reports", "evaluation_results.csv")
    if os.path.exists(results_csv_path):
        df_eval = pd.read_csv(results_csv_path)

        avg_faith = df_eval["faithfulness"].mean()
        avg_rel = df_eval["answer_relevance"].mean()
        avg_prec = df_eval["context_precision"].mean()
        avg_rec = df_eval["context_recall"].mean()

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Faithfulness (Độ trung thực)", f"{avg_faith*100:.1f}%", "Chống bịa luật")
        m2.metric("Answer Relevance (Sát câu hỏi)", f"{avg_rel*100:.1f}%")
        m3.metric("Context Precision (Độ chính xác)", f"{avg_prec*100:.1f}%")
        m4.metric("Context Recall (Độ bao phủ)", f"{avg_rec*100:.1f}%")

        st.subheader("Bảng dữ liệu Test Cases chi tiết:")
        st.dataframe(df_eval, width=1200)

        st.subheader("Biểu đồ so sánh 4 chỉ số chất lượng RAG:")
        chart_data = pd.DataFrame({
            "Chỉ số": ["Faithfulness", "Answer Relevance", "Context Precision", "Context Recall"],
            "Điểm số": [avg_faith, avg_rel, avg_prec, avg_rec]
        }).set_index("Chỉ số")
        st.bar_chart(chart_data)
    else:
        st.warning("Chưa tìm thấy file kết quả đánh giá. Hãy chạy script `python src/evaluation/ragas_evaluator.py` để sinh kết quả.")
