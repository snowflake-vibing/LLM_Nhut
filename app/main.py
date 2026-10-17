"""
LegalTech Platform - Streamlit Application - Version 2.0 (Major Release)
Giao diện người dùng với In-Chat Generative UI, Thẩm định Hợp đồng, Soạn thảo Hồ sơ,
Tra cứu Hybrid và Quản lý Memory Bank (Continual Optimization).
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
from src.tools.contract_scanner import ContractVulnerabilityScanner
from src.agents.memory_store import LegalMemoryStore
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
    page_title="LegalTech Platform - v2.0",
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

if "memory_store" not in st.session_state:
    st.session_state.memory_store = LegalMemoryStore()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "👋 **Xin chào! Tôi là Trợ lý AI Trí tuệ Pháp lý Toàn diện (LegalTech Platform v2.0 - Major Release).**\n\n"
                "Hệ thống Version 2.0 đã được nâng cấp với các công cụ đột phá:\n"
                "- 🛡️ **Quét Lỗ hổng & Chấm điểm Hợp đồng:** Phát hiện cạm bẫy phạt quá 8%, thử việc quá hạn, thiếu bất khả kháng và xuất báo cáo Word (.docx).\n"
                "- 💬 **In-Chat Interactive Canvas:** Bạn có thể yêu cầu tạo hồ sơ hoặc thẩm định văn bản ngay trong khung chat này.\n"
                "- 📚 **Tri thức Đa luật Đa tầng:** Bao quát Luật Doanh nghiệp 2020, Bộ luật Dân sự 2015, Bộ luật Lao động 2019 và Luật Thương mại 2005 kèm link Cổng TT Chính phủ.\n"
                "- 📝 **Tự động Soạn thảo Hồ sơ:** Xuất trọn bộ biểu mẫu thành lập doanh nghiệp chuẩn Nghị định 01/2021/NĐ-CP.\n\n"
                "👉 *Bạn muốn thẩm định một bản hợp đồng, tra cứu ngành nghề hay tạo hồ sơ doanh nghiệp?*"
            ),
            "agent": "SystemGreeting",
            "citations": [],
            "action_type": None,
            "action_data": None
        }
    ]

# ==================== SIDEBAR: GIỚI THIỆU & ĐIỀU HƯỚNG TABS ====================
with st.sidebar:
    st.title("⚖️ LegalTech Platform")
    st.caption("Nền tảng Trí tuệ Pháp lý & Thẩm định Hợp đồng • **v2.0 (Major Release)**")
    st.markdown("---")

    # 📌 MENU ĐIỀU HƯỚNG CÁC CHỨC NĂNG (TABS BÊN TRÁI)
    st.subheader("📑 Danh mục Chức năng")
    tab_options = [
        "💬 Khung Chat & Command Center",
        "🛡️ Thẩm định & Quét Lỗ hổng Hợp đồng",
        "📝 Soạn thảo Hồ sơ Doanh nghiệp (.docx)",
        "📚 Tra cứu CSDL Mã ngành & Giấy phép (Hybrid)",
        "🔐 Giám sát Bảo mật, Switcher & Memory Bank",
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
        "🛡️ **Kiến trúc Version 2.0:**\n"
        "- In-Chat Generative Actions\n"
        "- Contract Vulnerability Scanner\n"
        "- Hierarchical RAG (Dân sự, Lao động, Thương mại)\n"
        "- Dynamic Few-shot Memory Bank"
    )


# ==================== KHU VỰC HIỂN THỊ NỘI DUNG CHÍNH ====================

# 💬 TAB 1: KHUNG CHAT & COMMAND CENTER (IN-CHAT GENERATIVE ACTIONS)
if selected_tab == "💬 Khung Chat & Command Center":
    st.header("💬 Trợ lý Trí tuệ Pháp lý & Command Center")
    st.caption("Trung tâm Điều phối Đa tác nhân • Tương tác trực tiếp công cụ trong luồng hội thoại")

    # Gợi ý nhanh các câu lệnh
    st.markdown("💡 **Lối tắt thao tác nhanh (Quick Actions):**")
    qc1, qc2, qc3 = st.columns(3)
    quick_prompt = None
    with qc1:
        if st.button("🛡️ Quét thử Hợp đồng mẫu phạt 15%"):
            quick_prompt = "Hãy kiểm tra rủi ro hợp đồng này: 'Hợp đồng mua bán hàng hóa quy định nếu Bên B chậm thanh toán thì phải chịu phạt vi phạm 15% giá trị hợp đồng và không có điều khoản bất khả kháng.'"
    with qc2:
        if st.button("📝 Kích hoạt Tạo hồ sơ Doanh nghiệp"):
            quick_prompt = "Tôi muốn tạo bộ hồ sơ đăng ký thành lập công ty TNHH 1 thành viên ngành phần mềm"
    with qc3:
        if st.button("🔍 Tra cứu ngành kinh tế mới"):
            quick_prompt = "Tôi muốn mở doanh nghiệp dịch vụ livestream bán hàng và affiliate marketing thì đăng ký mã ngành gì?"

    # Hiển thị lịch sử chat
    for idx, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

            # 1. Hiển thị Interactive Action Widget nếu có
            action_type = msg.get("action_type")
            action_data = msg.get("action_data")

            if action_type == "CONTRACT_AUDIT_ACTION" and action_data:
                with st.expander("🔍 Thẻ Chi tiết Thẩm định & Tải Báo cáo (.docx)", expanded=True):
                    sc1, sc2 = st.columns([1, 2])
                    with sc1:
                        st.metric("Điểm An toàn Pháp lý", f"{action_data.get('score', 0)} / 100")
                        st.markdown(f"**Trạng thái:** {action_data.get('status_label', '')}")
                    with sc2:
                        st.markdown(f"**Số lỗ hổng phát hiện:** `{action_data.get('findings_count', 0)}`")
                        docx_audit = st.session_state.contract_scanner.export_audit_report_docx(action_data)
                        st.download_button(
                            label="📥 Tải Báo cáo Thẩm định Hợp đồng (.docx)",
                            data=docx_audit,
                            file_name=f"Bao_Cao_Tham_Dinh_Hop_Dong_{idx}.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            key=f"dl_audit_{idx}"
                        )

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

            # 2. Hiển thị Citations
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

    # Nhận input từ chat box hoặc nút quick action
    user_input = st.chat_input("Nhập câu hỏi, yêu cầu soạn hồ sơ hoặc dán điều khoản hợp đồng cần kiểm tra...")
    if quick_prompt:
        user_input = quick_prompt

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("AI Agents đang phân tích, đối chiếu quy tắc luật và chuẩn bị phản hồi..."):
                result = st.session_state.workflow.process(user_input)

            resp_text = result["response"]
            st.markdown(resp_text)

            citations = result.get("citations", [])
            action_type = result.get("action_type")
            action_data = result.get("action_data")

            # Hiển thị Interactive Widget tương ứng
            if action_type == "CONTRACT_AUDIT_ACTION" and action_data:
                with st.expander("🔍 Thẻ Chi tiết Thẩm định & Tải Báo cáo (.docx)", expanded=True):
                    sc1, sc2 = st.columns([1, 2])
                    with sc1:
                        st.metric("Điểm An toàn Pháp lý", f"{action_data.get('score', 0)} / 100")
                        st.markdown(f"**Trạng thái:** {action_data.get('status_label', '')}")
                    with sc2:
                        st.markdown(f"**Số lỗ hổng phát hiện:** `{action_data.get('findings_count', 0)}`")
                        docx_audit = st.session_state.contract_scanner.export_audit_report_docx(action_data)
                        st.download_button(
                            label="📥 Tải Báo cáo Thẩm định Hợp đồng (.docx)",
                            data=docx_audit,
                            file_name="Bao_Cao_Tham_Dinh_Hop_Dong_Moi.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        )

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
                "citations": citations,
                "action_type": action_type,
                "action_data": action_data
            })

# 🛡️ TAB 2: THẨM ĐỊNH & QUÉT LỖ HỔNG HỢP ĐỒNG (CHUYÊN SÂU TOÀN MÀN HÌNH)
elif selected_tab == "🛡️ Thẩm định & Quét Lỗ hổng Hợp đồng":
    st.header("🛡️ Thẩm định & Quét Lỗ hổng Hợp đồng Chuyên sâu")
    st.caption("Công cụ Phân tích Cạm bẫy Pháp lý • Chấm điểm An toàn (0 - 100) • Gợi ý Điều khoản Thay thế (Redlining)")

    st.markdown("Chọn một mẫu hợp đồng thử nghiệm hoặc dán nội dung hợp đồng của bạn vào ô bên dưới:")

    sample_contracts = {
        "Hợp đồng 1: Mua bán Hàng hóa (Dính bẫy phạt 15% & thiếu Bất khả kháng)": (
            "HỢP ĐỒNG MUA BÁN HÀNG HÓA\n"
            "Điều 1: Bên A bán cho Bên B lô hàng linh kiện máy tính với tổng giá trị 200.000.000 VNĐ.\n"
            "Điều 2: Bên B thanh toán trong vòng 15 ngày kể từ ngày nhận hàng.\n"
            "Điều 3 (Phạt vi phạm): Nếu Bên B chậm thanh toán, Bên B phải chịu phạt vi phạm bằng 15% tổng giá trị hợp đồng.\n"
            "Điều 4: Tranh chấp phát sinh sẽ được đưa ra giải quyết tại Tòa án có thẩm quyền."
        ),
        "Hợp đồng 2: Hợp đồng Thử việc (Vi phạm thời gian thử việc 90 ngày)": (
            "HỢP ĐỒNG THỬ VIỆC\n"
            "Điều 1: Công ty tuyển dụng ông Nguyễn Văn A làm vị trí Lập trình viên Backend.\n"
            "Điều 2 (Thời gian thử việc): Thời gian thử việc là 03 tháng (90 ngày) kể từ ngày ký.\n"
            "Điều 3: Mức lương thử việc bằng 85% mức lương chính thức.\n"
            "Điều 4: Trong thời gian thử việc, công ty có quyền giữ bản chính bằng đại học của người lao động để làm tin."
        ),
        "Hợp đồng 3: Hợp đồng Thuê Nhà mở Quán (Điều khoản một chiều bất lợi)": (
            "HỢP ĐỒNG THUÊ MẶT BẰNG KINH DOANH\n"
            "Điều 1: Bên A cho Bên B thuê căn nhà số 45 Nguyễn Huệ để mở quán cà phê, thời hạn 3 năm.\n"
            "Điều 2: Tiền thuê là 30.000.000 VNĐ/tháng, đặt cọc 3 tháng tiền nhà.\n"
            "Điều 3 (Đơn phương chấm dứt): Bên A có quyền đơn phương lấy lại nhà bất kỳ lúc nào chỉ cần báo trước 7 ngày mà không phải trả lại tiền cọc hay bồi thường chi phí sửa chữa cho Bên B.\n"
            "Điều 4: Không áp dụng bất kỳ lý do miễn trừ nào kể cả thiên tai, dịch bệnh phong tỏa."
        )
    }

    selected_sample = st.selectbox("Chọn mẫu kiểm thử nhanh:", list(sample_contracts.keys()))
    contract_input = st.text_area(
        "Nội dung văn bản hợp đồng cần thẩm định:",
        value=sample_contracts[selected_sample],
        height=220
    )

    if st.button("🔍 Bắt đầu Quét Lỗ hổng & Chấm điểm Hợp đồng"):
        with st.spinner("AI Scanner đang đối chiếu quy chuẩn pháp luật và phân tích rủi ro..."):
            scan_out = st.session_state.contract_scanner.scan(contract_input)

        col_sc1, col_sc2 = st.columns([1, 2])
        with col_sc1:
            st.metric("Điểm An toàn Pháp lý (Risk Score)", f"{scan_out['score']} / 100")
            st.markdown(f"**Đánh giá:** {scan_out['status_label']}")
            st.markdown(f"**Số vấn đề phát hiện:** `{scan_out['findings_count']}`")
        with col_sc2:
            st.subheader("💡 Ý kiến Thẩm định của Luật sư AI:")
            st.write(scan_out["ai_review"])

        st.markdown("---")
        st.subheader("📋 Bảng Danh mục Cạm bẫy Pháp lý & Đề xuất Điều khoản Thay thế (Redlining)")
        for idx, f in enumerate(scan_out["findings"], 1):
            badge = "🔴" if f["level"] == "CRITICAL" else ("🟡" if f["level"] == "WARNING" else "🔵")
            with st.expander(f"{badge} Vấn đề {idx}: {f['title']}", expanded=True):
                st.markdown(f"- **Đoạn trích rủi ro:** `{f['clause_snippet']}`")
                st.markdown(f"- **Căn cứ pháp lý vi phạm:** **{f['legal_basis']}** - [🔗 Kiểm chứng tại Cổng TT Chính phủ]({f['verify_url']})")
                st.markdown(f"- **Phân tích rủi ro:** {f['risk_explanation']}")
                st.success(f"**✍️ Điều khoản Đề xuất Thay thế (Clause Redlining):**\n\n*{f['suggested_replacement']}*")

        # Nút tải báo cáo Word
        st.markdown("---")
        docx_report = st.session_state.contract_scanner.export_audit_report_docx(scan_out)
        st.download_button(
            label="📥 Tải về Bản Báo cáo Thẩm định Pháp lý Đầy đủ (.docx)",
            data=docx_report,
            file_name="Bao_Cao_Tham_Dinh_Rui_Ro_Hop_Dong.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

# 📝 TAB 3: SOẠN THẢO HỒ SƠ DOANH NGHIỆP TỰ ĐỘNG (.DOCX)
elif selected_tab == "📝 Soạn thảo Hồ sơ Doanh nghiệp (.docx)":
    st.header("📝 Tự động Soạn thảo Bộ Hồ sơ Đăng ký Doanh nghiệp")
    st.caption("Chuẩn biểu mẫu Nghị định 01/2021/NĐ-CP và Luật Doanh nghiệp 2020 • Xuất file Word (.docx) dùng ngay")

    with st.form("dossier_form_dedicated"):
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

    st.subheader("⚖️ Kết quả Thẩm định Pháp lý Doanh nghiệp (AI Legal Check)")
    alerts = validate_dossier_legal_compliance(dossier_data)
    is_name_valid, _ = validate_company_name(form_company_name)

    if is_name_valid:
        st.success(f"✅ **Tên doanh nghiệp hợp lệ:** '{form_company_name}' tuân thủ Điều 37, 38, 39, 41 Luật Doanh nghiệp 2020.")
    for alert in alerts:
        if alert.startswith("🚫"):
            st.error(alert)
        elif alert.startswith("⚠️"):
            st.warning(alert)
        else:
            st.info(alert)

    st.markdown("---")
    st.subheader("📥 Tải về Bộ Hồ sơ Hoàn chỉnh (.docx)")
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

# 📚 TAB 4: TRA CỨU CSDL MÃ NGÀNH & GIẤY PHÉP (HYBRID RETRIEVAL & PAGINATION)
elif selected_tab == "📚 Tra cứu CSDL Mã ngành & Giấy phép (Hybrid)":
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

        st.subheader(f"1. Kết quả từ CSDL SQLite VSIC 2018 ({len(industries)} kết quả)")
        if industries:
            df_ind = pd.DataFrame(industries)
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

        if web_hits:
            st.markdown("---")
            st.subheader(f"2. Kết quả Mở rộng từ Web Search & Ngành Kinh tế Mới ({len(web_hits)} kết quả)")
            for hit in web_hits:
                with st.expander(f"🌐 {hit['title']}"):
                    st.markdown(f"**Nội dung:** {hit['snippet']}")
                    st.markdown(f"**Nguồn xác thực:** [🔗 Truy cập văn bản]({hit['url']})")

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

# 🔐 TAB 5: GIÁM SÁT BẢO MẬT, SWITCHER & MEMORY BANK (CONTINUAL OPTIMIZATION)
elif selected_tab == "🔐 Giám sát Bảo mật, Switcher & Memory Bank":
    st.header("🔐 Giám sát Bảo mật & Ngân hàng Ký ức Tri thức (Memory Bank)")
    st.caption("Hiện thực hóa Tiêu chí 7: Bảo mật LLM & Cơ chế Tối ưu Liên tục Không Cần Đổi Trọng số")

    # 1. PII Flow Diagram
    st.subheader("1. Sơ đồ Luồng Bảo vệ Dữ liệu Cá nhân (PII Masking Flow)")
    p1, p2, p3, p4 = st.columns(4)
    with p1:
        st.info("👤 **Bước 1: Input Người dùng**\n\nChứa thông tin thật:\n- CCCD: `079201004567`\n- SĐT: `0912345678`")
    with p2:
        st.warning("🛡️ **Bước 2: Local PII Masker**\n\nChe giấu cục bộ:\n- CCCD $\\rightarrow$ `[CCCD_0]`\n- Bảng map lưu RAM máy")
    with p3:
        st.success("☁️ **Bước 3: Cloud LLM API**\n\nGemini chỉ nhận được:\n*\"Tôi là cá nhân [CCCD_0]\"*\n*(Không lộ thông tin)*")
    with p4:
        st.info("🔄 **Bước 4: Local Unmasker**\n\nKhôi phục dữ liệu gốc:\nRáp lại CCCD/SĐT thật trước khi trả về cho bạn.")

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

    # 4. MEMORY BANK
    st.markdown("---")
    st.subheader("4. Ngân hàng Ký ức Tri thức Động (Dynamic Few-Shot Memory Bank)")
    st.caption("Cơ chế tự học hỏi từ các tình huống pháp lý chuẩn và phản hồi người dùng (Continual Learning without Weight Training)")

    cases = st.session_state.memory_store.cases
    st.markdown(f"Hiện có **{len(cases)}** tình huống pháp lý chuẩn được nạp tự động vào ngữ cảnh suy luận (In-Context Learning):")

    for c in cases:
        with st.expander(f"📌 {c.get('title', 'Tình huống pháp lý')}"):
            st.markdown(f"- **Vấn đề cốt lõi:** `{c.get('key_risk', '')}`")
            st.markdown(f"- **Giải pháp vàng:** {c.get('golden_solution', '')}")
            st.markdown(f"- **Căn cứ pháp luật:** `{c.get('legal_basis', '')}`")

    with st.expander("➕ Ghi nhận một Kinh nghiệm / Tình huống Pháp lý Mới vào Memory Bank"):
        with st.form("add_memory_form"):
            new_title = st.text_input("Tiêu đề tình huống:")
            new_query = st.text_input("Câu hỏi / Từ khóa tìm kiếm:")
            new_solution = st.text_area("Giải pháp chuẩn:")
            new_basis = st.text_input("Căn cứ pháp luật:")
            submit_mem = st.form_submit_button("Lưu vào Memory Bank")
            if submit_mem and new_title and new_solution:
                st.session_state.memory_store.record_feedback(new_title, new_query, new_solution, new_basis)
                st.success("✅ Đã ghi nhận kinh nghiệm mới vào Memory Bank! Mô hình sẽ tự động bốc ví dụ này trong các lần tư vấn tiếp theo.")

# 📊 TAB 6: ĐÁNH GIÁ MÔ HÌNH RAGAS
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
