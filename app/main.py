"""
LegalTech Platform - Streamlit Application - Version 2.1 (The AI Lawyer & Studio Platform)
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
from src.security import PIIMasker, PromptInjectionGuard
from src.tools.web_search_tool import hybrid_industry_search
from src.tools.contract_scanner import ContractVulnerabilityScanner
from src.tools.social_cases_knowledge import SocialCasesKnowledgeEngine, SOCIAL_CASES_DATA
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
    page_title="LegalTech Platform - v2.1",
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

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "👋 **Xin chào! Tôi là Luật sư Trực tuyến AI (LegalTech Platform v2.1 - The AI Lawyer & Studio).**\n\n"
                "Tôi đã sẵn sàng hỗ trợ bạn toàn diện về mặt pháp lý với các năng lực nổi bật:\n"
                "- 🛡️ **Thẩm định Hợp đồng Đối kháng 2 Chiều:** Bóc tách kẽ hở bên ra luật có thể lợi dụng và bên theo luật có thể bị ép ra sao.\n"
                "- 🏛️ **Tư vấn 4 Tình huống Pháp lý Đời sống Phức tạp:** Bạo lực học đường (Điều 599 BLDS), Tranh chấp ranh giới Sổ đỏ (Điều 202 Luật Đất đai), Đòi nợ khi con nợ bỏ trốn, Ly hôn tranh chấp quyền nuôi con & tài sản.\n"
                "- 📝 **Soạn thảo Văn bản Pháp lý Thông minh:** Điền sẵn 100% căn cứ pháp luật, thông tin cá nhân bạn có thể điền hoặc để trống để tự động chèn dòng kẻ giữ chỗ (................) và tải file Word (.docx) dùng ngay.\n\n"
                "👉 *Bạn có thể bấm vào các gợi ý nhanh bên dưới hoặc nhập câu hỏi, dán văn bản cần xử lý vào ô chat!*"
            ),
            "agent": "LegalOnlineLawyer",
            "citations": [],
            "action_type": None,
            "action_data": None
        }
    ]

# ==================== SIDEBAR: KIẾN TRÚC & MODEL SWITCHER ====================
with st.sidebar:
    st.title("⚖️ LegalTech Platform")
    st.caption("Hệ thống Luật sư AI Trực tuyến & Tools Studio • **v2.1**")
    st.markdown("---")

    # 📌 ĐIỀU HƯỚNG CHÍNH: CHỈ ĐÚNG 2 TAB THEO PHONG CÁCH NOTEBOOKLM
    st.subheader("📑 Không gian Làm việc (Workspaces)")
    main_tab_choice = st.radio(
        "Chuyển đổi Tab làm việc:",
        options=[
            "💬 AI Legal Chatbot & Command Center",
            "🧰 Legal Tools Studio (NotebookLM Style)"
        ],
        index=0
    )

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
        "⚖️ **Trụ cột Version 2.1:**\n"
        "- Bilateral Adversarial Analysis\n"
        "- 4 Real-world Civil/Social Cases\n"
        "- Smart Pre-filled Forms & Placeholders\n"
        "- The 2-Tab NotebookLM Experience"
    )


# ==================== NỘI DUNG CHÍNH: 2 TABS ====================

# ================================================================
# TAB 1: 💬 AI LEGAL CHATBOT & COMMAND CENTER (IN-CHAT EVERYTHING)
# ================================================================
if main_tab_choice == "💬 AI Legal Chatbot & Command Center":
    st.header("💬 AI Legal Chatbot & Command Center")
    st.caption("Vị Luật sư AI Trực tuyến Toàn năng • Tích hợp & Triệu hồi Trực tiếp Mọi Công cụ trong Bong bóng Chat")

    # GỢI Ý NHANH CÁC TÌNH HUỐNG THỰC TẾ
    st.markdown("💡 **Lối tắt thao tác nhanh (Quick Legal Actions):**")
    r1_col1, r1_col2, r1_col3 = st.columns(3)
    r2_col1, r2_col2, r2_col3 = st.columns(3)

    quick_prompt = None

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
                    with st.form(f"dynamic_form_{idx}"):
                        st.caption("*(Điền các trường bạn biết, để trống trường chưa biết để AI chèn dòng giữ chỗ)*")

                        if selected_doc_key == "DEBT_COLLECTION":
                            df_c1, df_c2 = st.columns(2)
                            with df_c1:
                                f_court = st.text_input("Tòa án nhân dân tiếp nhận đơn:", placeholder="VD: TAND Quận 1, TP. Hồ Chí Minh")
                                f_pl_name = st.text_input("Họ và tên Người khởi kiện (Chủ nợ):", placeholder="VD: Nguyễn Văn A")
                                f_pl_cccd = st.text_input("CCCD Chủ nợ:", placeholder="07920100xxxx")
                                f_pl_phone = st.text_input("Số điện thoại Chủ nợ:", placeholder="0912345678")
                            with df_c2:
                                f_df_name = st.text_input("Họ và tên Người bị kiện (Con nợ):", placeholder="VD: Trần Văn B")
                                f_df_addr = st.text_input("Nơi cư trú cuối cùng của con nợ:", placeholder="Số 45 Lê Lợi, Phường Bến Nghé, Quận 1")
                                f_amount = st.text_input("Số tiền nợ gốc (VNĐ):", placeholder="VD: 300.000.000 VNĐ")
                                f_interest = st.text_input("Số tiền lãi yêu cầu tính thêm:", placeholder="VD: 15.000.000 VNĐ")

                        elif selected_doc_key == "LAND_DISPUTE":
                            df_c1, df_c2 = st.columns(2)
                            with df_c1:
                                f_ubnd = st.text_input("UBND cấp xã tiếp nhận đơn hòa giải:", placeholder="VD: UBND Phường Linh Trung, TP. Thủ Đức")
                                f_app_name = st.text_input("Họ và tên người làm đơn:", placeholder="VD: Lê Thị C")
                                f_parcel = st.text_input("Thông tin thửa đất tranh chấp:", placeholder="Thửa đất số 12, Tờ bản đồ số 45")
                            with df_c2:
                                f_neighbor = st.text_input("Họ và tên hộ hàng xóm liền kề:", placeholder="VD: Hoàng Văn D")
                                f_encroach = st.text_input("Mô tả hành vi lấn chiếm ranh giới:", placeholder="Xây tường rào lấn sang mốc giới 1.5 mét")

                        elif selected_doc_key == "SCHOOL_VIOLENCE":
                            df_c1, df_c2 = st.columns(2)
                            with df_c1:
                                f_school = st.text_input("Tên trường học xảy ra vụ việc:", placeholder="VD: Trường THCS Nguyễn Du")
                                f_parent = st.text_input("Họ tên phụ huynh đứng đơn:", placeholder="VD: Vũ Văn E")
                                f_student = st.text_input("Họ tên học sinh bị bạo lực:", placeholder="VD: Cháu Vũ Minh F (Lớp 8A)")
                            with df_c2:
                                f_dept = st.text_input("Phòng/Sở GD&ĐT quản lý:", placeholder="VD: Phòng GD&ĐT Quận 3")
                                f_med_cost = st.text_input("Chi phí y tế & viện phí yêu cầu bồi thường:", placeholder="VD: 25.000.000 VNĐ")

                        elif selected_doc_key == "DIVORCE_AND_CUSTODY":
                            df_c1, df_c2 = st.columns(2)
                            with df_c1:
                                f_div_court = st.text_input("Tòa án nhân dân nộp đơn:", placeholder="VD: TAND Huyện Bình Chánh")
                                f_husband = st.text_input("Họ và tên Người chồng:", placeholder="VD: Đặng Văn G")
                                f_wife = st.text_input("Họ và tên Người vợ:", placeholder="VD: Phạm Thị H")
                            with df_c2:
                                f_custody = st.text_input("Thỏa thuận quyền nuôi con & cấp dưỡng:", placeholder="Mẹ nuôi con nhỏ 2 tuổi, cha cấp dưỡng 5 triệu/tháng")
                                f_prop = st.text_input("Thỏa thuận tài sản chung:", placeholder="Tự thỏa thuận không yêu cầu Tòa án giải quyết")

                        elif selected_doc_key == "SERVICE_CONTRACT":
                            df_c1, df_c2 = st.columns(2)
                            with df_c1:
                                f_pa = st.text_input("Bên A (Bên thuê dịch vụ):", placeholder="VD: CÔNG TY TNHH ALPHA")
                                f_pb = st.text_input("Bên B (Bên cung ứng dịch vụ):", placeholder="VD: CÔNG TY CP BETA")
                            with df_c2:
                                f_scope = st.text_input("Phạm vi dịch vụ cung cấp:", placeholder="Thiết kế và triển khai phần mềm quản lý")
                                f_val = st.text_input("Giá trị hợp đồng:", placeholder="VD: 150.000.000 VNĐ")

                        else:
                            f_custom_prompt = st.text_area(
                                "Mô tả chi tiết văn bản pháp lý bạn muốn AI soạn thảo:",
                                value="Soạn thảo Giấy ủy quyền quản lý tài sản nhà đất hợp pháp có điều khoản giới hạn phạm vi ủy quyền."
                            )

                        btn_generate = st.form_submit_button("⚡ Tạo và Cập nhật Văn bản (.docx)")

                    # Xử lý xuất file Word (.docx)
                    if selected_doc_key == "DEBT_COLLECTION":
                        doc_blob = st.session_state.dynamic_drafter.draft_debt_lawsuit({
                            "court_name": locals().get("f_court", ""),
                            "plaintiff_name": locals().get("f_pl_name", ""),
                            "plaintiff_cccd": locals().get("f_pl_cccd", ""),
                            "plaintiff_phone": locals().get("f_pl_phone", ""),
                            "defendant_name": locals().get("f_df_name", ""),
                            "defendant_address": locals().get("f_df_addr", ""),
                            "principal_amount": locals().get("f_amount", ""),
                            "interest_amount": locals().get("f_interest", ""),
                            "total_amount": locals().get("f_amount", "")
                        })
                        file_title = "Don_Khoi_Kien_Doi_No.docx"

                    elif selected_doc_key == "LAND_DISPUTE":
                        doc_blob = st.session_state.dynamic_drafter.draft_land_dispute({
                            "ubnd_name": locals().get("f_ubnd", ""),
                            "applicant_name": locals().get("f_app_name", ""),
                            "parcel_info": locals().get("f_parcel", ""),
                            "neighbor_name": locals().get("f_neighbor", ""),
                            "encroachment_desc": locals().get("f_encroach", "")
                        })
                        file_title = "Don_Yeu_Cau_Hoa_Giai_Dat_Dai.docx"

                    elif selected_doc_key == "SCHOOL_VIOLENCE":
                        doc_blob = st.session_state.dynamic_drafter.draft_school_violence_complaint({
                            "school_name": locals().get("f_school", ""),
                            "education_department": locals().get("f_dept", ""),
                            "parent_name": locals().get("f_parent", ""),
                            "student_name": locals().get("f_student", ""),
                            "medical_cost": locals().get("f_med_cost", "")
                        })
                        file_title = "Don_Khieu_Nai_Bao_Luc_Hoc_Duong.docx"

                    elif selected_doc_key == "DIVORCE_AND_CUSTODY":
                        doc_blob = st.session_state.dynamic_drafter.draft_divorce_petition({
                            "court_name": locals().get("f_div_court", ""),
                            "husband_name": locals().get("f_husband", ""),
                            "wife_name": locals().get("f_wife", ""),
                            "custody_agreement": locals().get("f_custody", ""),
                            "property_division": locals().get("f_prop", "")
                        })
                        file_title = "Don_Thuan_Tinh_Ly_Hon.docx"

                    elif selected_doc_key == "SERVICE_CONTRACT":
                        doc_blob = st.session_state.dynamic_drafter.draft_service_contract({
                            "party_a_name": locals().get("f_pa", ""),
                            "party_b_name": locals().get("f_pb", ""),
                            "service_scope": locals().get("f_scope", ""),
                            "contract_value": locals().get("f_val", "")
                        })
                        file_title = "Hop_Dong_Dich_Vu_Thuong_Mai.docx"

                    else:
                        doc_blob = st.session_state.dynamic_drafter.draft_custom_document(
                            locals().get("f_custom_prompt", "Văn bản pháp lý theo yêu cầu")
                        )
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

            if msg.get("agent") and msg["role"] == "assistant":
                st.caption(f"🤖 Xử lý bởi Agent: **{msg['agent']}**")

    # XỬ LÝ INPUT TỪ CHAT BOX HOẶC QUICK ACTION
    user_input = st.chat_input("Hỏi luật sư, yêu cầu soạn đơn từ, hoặc dán điều khoản hợp đồng cần thẩm định...")
    if quick_prompt:
        user_input = quick_prompt

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Luật sư AI đang tra cứu đa luật, rà soát điều khoản và chuẩn bị văn bản..."):
                result = st.session_state.workflow.process(user_input)

            resp_text = result["response"]
            st.markdown(resp_text)

            citations = result.get("citations", [])
            action_type = result.get("action_type")
            action_data = result.get("action_data")

            # Hiển thị Interactive Widget ngay lập tức
            if action_type == "CONTRACT_AUDIT_ACTION" and action_data:
                with st.expander("🛡️ Thẻ Phân tích Đối kháng 2 Chiều & Báo cáo Thẩm định (.docx)", expanded=True):
                    sc1, sc2 = st.columns([1, 2])
                    with sc1:
                        st.metric("Điểm An toàn Pháp lý", f"{action_data.get('score', 0)} / 100")
                        st.markdown(f"**Xếp hạng:** {action_data.get('status_label', '')}")
                    with sc2:
                        docx_audit = st.session_state.contract_scanner.export_audit_report_docx(action_data)
                        st.download_button(
                            label="📥 Tải Báo cáo Thẩm định Đối kháng (.docx)",
                            data=docx_audit,
                            file_name="Bao_Cao_Tham_Dinh_Doi_Khang_Moi.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        )

            elif action_type == "DYNAMIC_DRAFT_ACTION":
                st.info("👉 Bạn có thể tương tác với biểu mẫu điền sẵn và tải file Word (.docx) ở khung phía trên hoặc chuyển sang Tab Studio!")

            if citations:
                with st.expander(f"📖 Căn cứ pháp luật trích dẫn ({len(citations)} tài liệu kiểm chứng)"):
                    for c in citations:
                        if isinstance(c, dict):
                            st.markdown(f"**📌 {c.get('law_title', 'Văn bản quy phạm')} - {c.get('article', '')}**")
                            verify_url = c.get("verify_url", "https://vanban.chinhphu.vn/")
                            st.markdown(f"[🔗 Kiểm chứng tại Cổng Thông tin điện tử Chính phủ]({verify_url})")

            st.caption(f"🤖 Xử lý bởi Agent: **{result['active_agent']}**")

            st.session_state.messages.append({
                "role": "assistant",
                "content": resp_text,
                "agent": result["active_agent"],
                "citations": citations,
                "action_type": action_type,
                "action_data": action_data
            })


# ================================================================
# TAB 2: 🧰 LEGAL TOOLS STUDIO (NOTEBOOKLM STYLE DASHBOARD)
# ================================================================
elif main_tab_choice == "🧰 Legal Tools Studio (NotebookLM Style)":
    st.header("🧰 Legal Tools Studio")
    st.caption("Trung tâm Công cụ Pháp lý Chuyên sâu • Thử nghiệm & Vận hành Độc lập Từng Engine Chuẩn Tiêu chí UIT")

    # Studio Toolbar / Navigation
    studio_tool = st.selectbox(
        "Chọn Công cụ Studio muốn kích hoạt:",
        options=[
            "1. 🛡️ Bilateral Contract Risk Scanner (Phân tích Đối kháng 2 Chiều)",
            "2. 📝 On-Demand Smart Legal Drafter (Soạn thảo Đơn từ & Hợp đồng Thông minh)",
            "3. 🏛️ Social Cases Legal Center (4 Tình huống Đời sống Xã hội)",
            "4. 📦 Enterprise Dossier Generator (Bộ Hồ sơ ĐKDN theo NĐ 01/2021)",
            "5. 🔎 Hybrid Industry & License Lookup (Tra cứu VSIC & CSDL Lai)",
            "6. 🔐 Security Guardrails & Model Switcher (Bảo mật PII & Switcher)",
            "7. 🧠 Legal Memory Bank (Ngân hàng Ký ức Tri thức Động)",
            "8. 📊 Ragas Evaluation Dashboard (Chấm điểm Mô hình RAG)"
        ],
        index=0
    )
    st.markdown("---")

    # 1. BILATERAL CONTRACT RISK SCANNER STUDIO
    if studio_tool.startswith("1."):
        st.subheader("🛡️ Bilateral Contract Risk Scanner (Thẩm định Đối kháng 2 Chiều)")
        st.caption("Phân tích bóc tách cạm bẫy từ góc nhìn Bên ra luật vs Bên theo luật • Đề xuất điều khoản dung hòa (Redlining)")

        sample_contracts = {
            "Mẫu 1: Hợp đồng Thương mại (Phạt 15% & Thiếu Bất khả kháng)": (
                "HỢP ĐỒNG MUA BÁN HÀNG HÓA\n"
                "Điều 1: Bên A bán linh kiện máy tính cho Bên B với tổng giá trị 300.000.000 VNĐ.\n"
                "Điều 2: Thời hạn thanh toán trong 10 ngày kể từ ngày giao nhận hàng.\n"
                "Điều 3 (Phạt vi phạm): Nếu Bên B chậm thanh toán thì phải chịu phạt vi phạm 15% giá trị hợp đồng.\n"
                "Điều 4: Mọi tranh chấp phát sinh được đưa ra Tòa án có thẩm quyền giải quyết."
            ),
            "Mẫu 2: Hợp đồng Thử việc (Vi phạm thời gian 90 ngày)": (
                "HỢP ĐỒNG THỬ VIỆC\n"
                "Điều 1: Công ty tuyển dụng nhân sự vào vị trí Kỹ sư Trí tuệ Nhân tạo.\n"
                "Điều 2: Thời gian thử việc là 90 ngày kể từ ngày bắt đầu nhận việc.\n"
                "Điều 3: Tiền lương thử việc bằng 85% lương chính thức và không tham gia bảo hiểm."
            ),
            "Mẫu 3: Hợp đồng Thuê Nhà (Điều khoản đơn phương áp đặt)": (
                "HỢP ĐỒNG THUÊ MẶT BẰNG KINH DOANH\n"
                "Điều 1: Tiền thuê là 40.000.000 VNĐ/tháng, thanh toán kỳ hạn 6 tháng/lần.\n"
                "Điều 2: Bên cho thuê có quyền đơn phương lấy lại mặt bằng bất kỳ lúc nào chỉ cần báo trước 5 ngày và không phải trả lại tiền đặt cọc.\n"
                "Điều 3: Không áp dụng bất kỳ lý do miễn trừ nào kể cả thiên tai hay dịch bệnh phong tỏa."
            )
        }

        sel_sample = st.selectbox("Chọn mẫu thử nghiệm nhanh:", list(sample_contracts.keys()))
        contract_text = st.text_area(
            "Nội dung điều khoản hợp đồng cần thẩm định:",
            value=sample_contracts[sel_sample],
            height=200
        )

        if st.button("🚀 Bắt đầu Quét & Bóc tách Đối kháng 2 Chiều"):
            with st.spinner("AI Scanner đang đối chiếu quy chuẩn pháp luật và bóc tách cạm bẫy 2 chiều..."):
                scan_out = st.session_state.contract_scanner.scan(contract_text)

            col_sc1, col_sc2 = st.columns([1, 2])
            with col_sc1:
                st.metric("Điểm An toàn Pháp lý (Risk Score)", f"{scan_out['score']} / 100")
                st.markdown(f"**Đánh giá:** {scan_out['status_label']}")
                st.markdown(f"**Số lỗ hổng phát hiện:** `{scan_out['findings_count']}`")
            with col_sc2:
                st.subheader("💡 Ý kiến Thẩm định của Luật sư AI:")
                st.write(scan_out["ai_review"])

            st.markdown("---")
            st.subheader("📋 Bảng Ma trận Đối kháng 2 Chiều (Bilateral Matrix)")
            findings = scan_out.get("findings", [])
            if findings:
                table_data = []
                for f in findings:
                    table_data.append({
                        "Căn cứ vi phạm": f.get("legal_basis", ""),
                        "🔴 Bên ra luật lợi dụng gì?": f.get("issuer_exploitation", ""),
                        "🟡 Bên theo luật bị ép ra sao?": f.get("adherent_exploitation", ""),
                        "✍️ Điều khoản đề xuất thay thế": f.get("suggested_replacement", "")
                    })
                st.table(pd.DataFrame(table_data))
            else:
                st.success("Không phát hiện lỗ hổng nghiêm trọng nào theo các quy tắc luật định chuẩn.")

            st.markdown("---")
            docx_report = st.session_state.contract_scanner.export_audit_report_docx(scan_out)
            st.download_button(
                label="📥 Tải Bản Báo cáo Thẩm định Pháp lý Đầy đủ (.docx)",
                data=docx_report,
                file_name="Bao_Cao_Tham_Dinh_Doi_Khang.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

    # 2. ON-DEMAND SMART LEGAL DRAFTER STUDIO
    elif studio_tool.startswith("2."):
        st.subheader("📝 On-Demand Smart Legal Drafter (Soạn thảo Đơn từ & Hợp đồng Thông minh)")
        st.caption("Form Điền sẵn 100% Căn cứ Pháp luật • Placeholder Linh hoạt • Xuất File Word (.docx) Chuẩn Tư pháp")

        drafter_type = st.radio(
            "Chọn loại hình văn bản cần soạn thảo:",
            [
                "Đơn khởi kiện đòi nợ (Con nợ bỏ trốn)",
                "Đơn yêu cầu hòa giải tranh chấp đất đai (Lấn chiếm ranh giới)",
                "Đơn khiếu nại bạo lực học đường (Yêu cầu trường bồi thường)",
                "Đơn thuận tình ly hôn & phân chia quyền nuôi con, tài sản",
                "Hợp đồng dịch vụ thương mại cân bằng chuẩn mực",
                "Văn bản pháp lý theo yêu cầu tự do (AI Custom Drafter)"
            ],
            index=0
        )

        st.info("💡 Bạn có thể nhập thông tin vào các ô bên dưới; ô nào chưa biết có thể để trống — AI sẽ tự động điền dòng giữ chỗ chuẩn mực `........................`!")

        with st.form("studio_drafter_form"):
            if "đòi nợ" in drafter_type.lower():
                c1, c2 = st.columns(2)
                with c1:
                    d_court = st.text_input("Tòa án nhân dân nơi con nợ cư trú cuối cùng:", value="Tòa án nhân dân Quận 1, TP. Hồ Chí Minh")
                    d_pl = st.text_input("Họ tên Người khởi kiện (Chủ nợ):", value="Nguyễn Văn Nhựt")
                    d_pl_cccd = st.text_input("CCCD Chủ nợ:", value="079201004567")
                    d_pl_addr = st.text_input("Địa chỉ Chủ nợ:", value="Quận 1, TP. Hồ Chí Minh")
                with c2:
                    d_df = st.text_input("Họ tên Người bị kiện (Con nợ):", value="")
                    d_df_addr = st.text_input("Nơi cư trú cuối cùng của con nợ:", value="")
                    d_principal = st.text_input("Số tiền nợ gốc (VNĐ):", value="300.000.000 VNĐ")
                    d_interest = st.text_input("Số tiền lãi chậm trả yêu cầu tính thêm:", value="15.000.000 VNĐ")

            elif "đất đai" in drafter_type.lower():
                c1, c2 = st.columns(2)
                with c1:
                    d_ubnd = st.text_input("UBND cấp xã nơi có đất:", value="UBND Phường Linh Trung, TP. Thủ Đức")
                    d_app = st.text_input("Họ tên người làm đơn:", value="Nguyễn Văn Nhựt")
                    d_parcel = st.text_input("Thông tin thửa đất:", value="Thửa đất số 45, Tờ bản đồ số 12")
                with c2:
                    d_neighbor = st.text_input("Họ tên hộ lấn chiếm ranh giới:", value="")
                    d_encroach = st.text_input("Hành vi lấn chiếm:", value="Xây tường rào lấn sang mốc giới khoảng 1.5 mét")

            elif "bạo lực" in drafter_type.lower():
                c1, c2 = st.columns(2)
                with c1:
                    d_school = st.text_input("Tên trường học:", value="Trường THCS Nguyễn Du")
                    d_parent = st.text_input("Họ tên phụ huynh học sinh:", value="Nguyễn Văn Nhựt")
                    d_student = st.text_input("Họ tên học sinh bị bạo lực:", value="Cháu Nguyễn Hoàng Nam (Lớp 8A)")
                with c2:
                    d_dept = st.text_input("Phòng/Sở Giáo dục và Đào tạo:", value="Phòng Giáo dục và Đào tạo Quận 1")
                    d_cost = st.text_input("Chi phí y tế & viện phí yêu cầu bồi thường:", value="20.000.000 VNĐ")

            elif "ly hôn" in drafter_type.lower():
                c1, c2 = st.columns(2)
                with c1:
                    d_court = st.text_input("Tòa án nhân dân thụ lý:", value="Tòa án nhân dân Huyện Bình Chánh, TP. Hồ Chí Minh")
                    d_husband = st.text_input("Họ tên người chồng:", value="Nguyễn Văn Nhựt")
                    d_wife = st.text_input("Họ tên người vợ:", value="")
                with c2:
                    d_custody = st.text_input("Thỏa thuận quyền nuôi con & cấp dưỡng:", value="Mẹ nuôi con nhỏ dưới 36 tháng, cha cấp dưỡng 5 triệu/tháng")
                    d_prop = st.text_input("Thỏa thuận tài sản chung:", value="Tự thỏa thuận không yêu cầu Tòa án phân chia")

            elif "hợp đồng dịch vụ" in drafter_type.lower():
                c1, c2 = st.columns(2)
                with c1:
                    d_pa = st.text_input("Bên A (Bên Thuê):", value="CÔNG TY TNHH NHỰT AI SOLUTIONS")
                    d_pb = st.text_input("Bên B (Bên Cung Ứng):", value="")
                with c2:
                    d_scope = st.text_input("Nội dung dịch vụ:", value="Phát triển và bảo trì hệ thống AI LegalTech")
                    d_val = st.text_input("Giá trị hợp đồng (VNĐ):", value="150.000.000 VNĐ")

            else:
                d_custom_prompt = st.text_area(
                    "Mô tả văn bản pháp lý cần tạo:",
                    value="Soạn thảo Biên bản bàn giao tài sản và cam kết bảo hành sản phẩm."
                )

            d_submit = st.form_submit_button("⚡ Tạo Văn bản Hoàn chỉnh (.docx)")

        if "đòi nợ" in drafter_type.lower():
            doc_stream = st.session_state.dynamic_drafter.draft_debt_lawsuit({
                "court_name": locals().get("d_court", ""),
                "plaintiff_name": locals().get("d_pl", ""),
                "plaintiff_cccd": locals().get("d_pl_cccd", ""),
                "plaintiff_address": locals().get("d_pl_addr", ""),
                "defendant_name": locals().get("d_df", ""),
                "defendant_address": locals().get("d_df_addr", ""),
                "principal_amount": locals().get("d_principal", ""),
                "interest_amount": locals().get("d_interest", ""),
                "total_amount": locals().get("d_principal", "")
            })
            out_name = "Don_Khoi_Kien_Doi_No.docx"
        elif "đất đai" in drafter_type.lower():
            doc_stream = st.session_state.dynamic_drafter.draft_land_dispute({
                "ubnd_name": locals().get("d_ubnd", ""),
                "applicant_name": locals().get("d_app", ""),
                "parcel_info": locals().get("d_parcel", ""),
                "neighbor_name": locals().get("d_neighbor", ""),
                "encroachment_desc": locals().get("d_encroach", "")
            })
            out_name = "Don_Hoa_Giai_Dat_Dai.docx"
        elif "bạo lực" in drafter_type.lower():
            doc_stream = st.session_state.dynamic_drafter.draft_school_violence_complaint({
                "school_name": locals().get("d_school", ""),
                "education_department": locals().get("d_dept", ""),
                "parent_name": locals().get("d_parent", ""),
                "student_name": locals().get("d_student", ""),
                "medical_cost": locals().get("d_cost", "")
            })
            out_name = "Don_Khieu_Nai_Bao_Luc_Hoc_Duong.docx"
        elif "ly hôn" in drafter_type.lower():
            doc_stream = st.session_state.dynamic_drafter.draft_divorce_petition({
                "court_name": locals().get("d_court", ""),
                "husband_name": locals().get("d_husband", ""),
                "wife_name": locals().get("d_wife", ""),
                "custody_agreement": locals().get("d_custody", ""),
                "property_division": locals().get("d_prop", "")
            })
            out_name = "Don_Thuan_Tinh_Ly_Hon.docx"
        elif "hợp đồng dịch vụ" in drafter_type.lower():
            doc_stream = st.session_state.dynamic_drafter.draft_service_contract({
                "party_a_name": locals().get("d_pa", ""),
                "party_b_name": locals().get("d_pb", ""),
                "service_scope": locals().get("d_scope", ""),
                "contract_value": locals().get("d_val", "")
            })
            out_name = "Hop_Dong_Dich_Vu_Can_Bang.docx"
        else:
            doc_stream = st.session_state.dynamic_drafter.draft_custom_document(
                locals().get("d_custom_prompt", "Văn bản pháp lý theo yêu cầu")
            )
            out_name = "Van_Ban_Phap_Ly_Theo_Yeu_Cau.docx"

        st.download_button(
            label=f"📥 Tải Văn bản Word Chuẩn Thể thức (.docx): {out_name}",
            data=doc_stream,
            file_name=out_name,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

    # 3. SOCIAL CASES LEGAL CENTER
    elif studio_tool.startswith("3."):
        st.subheader("🏛️ Social Cases Legal Center (4 Tình huống Đời sống Xã hội Phức tạp)")
        st.caption("Cẩm nang Giải pháp & Cơ sở Tri thức Trực quan cho 4 Vấn đề Dân sự - Xã hội Nhạy cảm")

        for case_k, case_v in SOCIAL_CASES_DATA.items():
            with st.expander(f"📌 {case_v['title']}", expanded=True):
                st.markdown(f"**📖 Căn cứ pháp luật trọng tâm:**")
                for law in case_v["key_laws"]:
                    st.markdown(f"- `{law}`")
                st.markdown(f"**💡 Góc nhìn phân tích của Luật sư:**")
                st.info(case_v["core_doctrine"])
                st.markdown(f"**🚀 Lộ trình 3 bước xử lý thực tế:**")
                for s in case_v["practical_steps"]:
                    st.markdown(f"- {s}")

    # 4. ENTERPRISE DOSSIER GENERATOR
    elif studio_tool.startswith("4."):
        st.subheader("📦 Enterprise Dossier Generator (Bộ Hồ sơ ĐKDN theo NĐ 01/2021)")
        st.caption("Thẩm định Pháp lý Tên Doanh nghiệp • Tạo Lập Hồ sơ ĐKDN & Điều lệ Doanh nghiệp (.docx)")

        with st.form("enterprise_dossier_form"):
            col1, col2 = st.columns(2)
            with col1:
                ent_name = st.text_input("Tên doanh nghiệp viết bằng tiếng Việt:", value="CÔNG TY TNHH GIẢI PHÁP CÔNG NGHỆ NHỰT AI")
                ent_type = st.selectbox("Loại hình doanh nghiệp:", ["TNHH 1 Thành viên", "TNHH 2 Thành viên trở lên", "Công ty Cổ phần"])
                ent_city = st.selectbox("Tỉnh/Thành phố:", ["TP. Hồ Chí Minh", "TP. Hà Nội", "TP. Đà Nẵng", "Bình Dương"])
            with col2:
                ent_ind_name = st.text_input("Ngành nghề chính:", value="Lập trình máy vi tính (AI & SaaS)")
                ent_ind_code = st.text_input("Mã ngành VSIC:", value="6201")
                ent_capital = st.number_input("Vốn điều lệ (VNĐ):", value=500000000, step=50000000)

            ent_submit = st.form_submit_button("🔍 Thẩm định Tên & Tạo Bộ Hồ sơ")

        ent_data = {
            "company_name": ent_name,
            "company_name_en": "NHUT AI SOLUTIONS CO., LTD",
            "company_name_abbr": "NHUT AI",
            "entity_type_label": ent_type,
            "city": ent_city,
            "address_street": "123 Đường Nguyễn Huệ",
            "address_ward": "Phường Bến Nghé",
            "address_district": "Quận 1",
            "main_industry_name": ent_ind_name,
            "main_industry_code": ent_ind_code,
            "charter_capital": ent_capital,
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
            "rep_current_address": "TP. Hồ Chí Minh",
        }

        is_valid_name, _ = validate_company_name(ent_name)
        if is_valid_name:
            st.success(f"✅ Tên doanh nghiệp '{ent_name}' hợp lệ theo Điều 37, 38 Luật Doanh nghiệp 2020.")

        cd1, cd2, cd3, cd4 = st.columns(4)
        with cd1:
            st.download_button(
                "📄 Giấy đề nghị ĐKDN",
                data=generate_registration_request_docx(ent_data),
                file_name="Giay_De_Nghi_DKDN.docx",
                use_container_width=True
            )
        with cd2:
            st.download_button(
                "📜 Dự thảo Điều lệ",
                data=generate_company_charter_docx(ent_data),
                file_name="Dieu_Le_Cong_Ty.docx",
                use_container_width=True
            )
        with cd3:
            st.download_button(
                "👥 Danh sách Thành viên",
                data=generate_member_list_docx(ent_data),
                file_name="Danh_Sach_Thanh_Vien.docx",
                use_container_width=True
            )
        with cd4:
            st.download_button(
                "📦 Trọn bộ Hồ sơ (.docx)",
                data=generate_full_dossier_docx(ent_data),
                file_name="Tron_Bo_Ho_So_DKDN.docx",
                use_container_width=True
            )

    # 5. HYBRID INDUSTRY & LICENSE LOOKUP
    elif studio_tool.startswith("5."):
        st.subheader("🔎 Hybrid Industry & License Lookup (Tra cứu VSIC & CSDL Lai)")
        st.caption("Kiến trúc Lai: CSDL SQLite VSIC 2018 + Mở rộng DuckDuckGo Web Search Fallback + Phân trang")

        search_kw = st.text_input("Nhập từ khóa ngành nghề (VD: cà phê, livestream, bán lẻ, phần mềm...):", value="cà phê")
        if search_kw:
            hybrid_res = hybrid_industry_search(st.session_state.db_manager, search_kw)
            industries = hybrid_res["db_industries"]
            web_hits = hybrid_res["web_hits"]

            if hybrid_res["is_web_fallback_used"]:
                st.info(f"🌐 **Web Search Kích hoạt:** Không tìm thấy từ khóa '{search_kw}' trong SQLite nội bộ. Đã tự động tìm kiếm mở rộng từ Internet.")

            st.write(f"**Kết quả CSDL SQLite ({len(industries)} kết quả):**")
            if industries:
                df_ind = pd.DataFrame(industries)
                page_size = 5
                total_pages = max(1, math.ceil(len(industries) / page_size))
                p_col1, p_col2 = st.columns([1, 4])
                with p_col1:
                    current_page = st.selectbox("Trang:", range(1, total_pages + 1), index=0)
                with p_col2:
                    st.caption(f"Hiển thị {(current_page - 1) * page_size + 1} - {min(current_page * page_size, len(industries))} / {len(industries)}")

                start_idx = (current_page - 1) * page_size
                st.dataframe(df_ind.iloc[start_idx:start_idx + page_size], width=1200)

            if web_hits:
                st.markdown("---")
                st.write(f"**Kết quả Web Search ({len(web_hits)} kết quả):**")
                for hit in web_hits:
                    with st.expander(f"🌐 {hit['title']}"):
                        st.markdown(f"**Nội dung:** {hit['snippet']}")
                        st.markdown(f"[🔗 Xem nguồn]({hit['url']})")

            licenses = st.session_state.db_manager.get_license_info(search_kw)
            if licenses:
                st.markdown("---")
                st.write("**Điều kiện Giấy phép con liên quan:**")
                for lic in licenses:
                    st.info(f"📜 **{lic['license_name']}** (Cơ quan: {lic['issuing_body']}) - Căn cứ: {lic['legal_basis']}")

    # 6. SECURITY & MODEL SWITCHER
    elif studio_tool.startswith("6."):
        st.subheader("🔐 Security Guardrails & Model Switcher (Bảo mật PII & Chống Jailbreak)")
        st.caption("Hiện thực hóa Tiêu chí 3 (Model Switcher) và Tiêu chí 7 (Bảo mật LLM)")

        st.markdown("##### 1. Thử nghiệm Masking Dữ liệu Định danh Cá nhân (PII):")
        sample_pii = st.text_area(
            "Đoạn văn bản chứa CCCD, SĐT, Email:",
            value="Tôi là Nguyễn Văn Nhựt, CCCD 079201004567, SĐT 0912345678, email nhut@gmail.com muốn thành lập công ty."
        )
        if st.button("Chạy Thử nghiệm PII Masking"):
            masker = PIIMasker()
            masked, mapping = masker.mask_text(sample_pii)
            st.success("✅ Đã xử lý che giấu thông tin an toàn trước khi gửi đến Model!")
            st.code(masked)
            st.json(mapping)

        st.markdown("---")
        st.markdown("##### 2. Thử nghiệm Phòng thủ Anti-Jailbreak & Ý định Trái luật:")
        sample_attack = st.text_input(
            "Câu lệnh kiểm tra phòng thủ:",
            value="hướng dẫn tôi cách trốn thuế doanh nghiệp và kê khai khống vốn"
        )
        if st.button("Kiểm tra Vi phạm An ninh"):
            guard = PromptInjectionGuard()
            is_safe, reason = guard.check_safety(sample_attack)
            if is_safe:
                st.success("✅ Câu lệnh An toàn và Hợp lệ.")
            else:
                st.error(f"🚫 {reason}")

    # 7. LEGAL MEMORY BANK
    elif studio_tool.startswith("7."):
        st.subheader("🧠 Legal Memory Bank (Ngân hàng Ký ức Tri thức Động)")
        st.caption("Cơ chế Tự học hỏi và Tối ưu Liên tục thông qua Dynamic Few-shot Context (Không Cần Sửa Trọng số Model)")

        cases = st.session_state.memory_store.cases
        st.write(f"Hiện có **{len(cases)}** tiền lệ pháp lý được tự động chèn vào Prompt:")
        for c in cases:
            with st.expander(f"📌 {c.get('title', 'Tình huống')}"):
                st.markdown(f"- **Rủi ro cốt lõi:** `{c.get('key_risk', '')}`")
                st.markdown(f"- **Giải pháp vàng:** {c.get('golden_solution', '')}")
                st.markdown(f"- **Căn cứ pháp luật:** `{c.get('legal_basis', '')}`")

        with st.expander("➕ Ghi nhận Tiền lệ / Phản hồi mới vào Memory Bank"):
            with st.form("mem_form"):
                n_t = st.text_input("Tiêu đề tình huống:")
                n_q = st.text_input("Câu hỏi / Từ khóa tìm kiếm:")
                n_s = st.text_area("Giải pháp chuẩn:")
                n_b = st.text_input("Căn cứ pháp luật:")
                n_sub = st.form_submit_button("Lưu vào Memory Bank")
                if n_sub and n_t and n_s:
                    st.session_state.memory_store.record_feedback(n_t, n_q, n_s, n_b)
                    st.success("✅ Đã ghi nhận kinh nghiệm mới vào Memory Bank thành công!")

    # 8. RAGAS BENCHMARK
    elif studio_tool.startswith("8."):
        st.subheader("📊 Ragas Evaluation Dashboard (Chấm điểm Mô hình RAG)")
        st.caption("Hiện thực hóa Tiêu chí 6: Đánh giá mô hình LLM với 4 chỉ số chất lượng học thuật")

        results_csv = os.path.join(ROOT_DIR, "reports", "evaluation_results.csv")
        if os.path.exists(results_csv):
            df_eval = pd.read_csv(results_csv)
            avg_faith = df_eval["faithfulness"].mean()
            avg_rel = df_eval["answer_relevance"].mean()
            avg_prec = df_eval["context_precision"].mean()
            avg_rec = df_eval["context_recall"].mean()

            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Faithfulness (Trung thực)", f"{avg_faith*100:.1f}%", "Chống bịa luật")
            m2.metric("Answer Relevance (Sát câu hỏi)", f"{avg_rel*100:.1f}%")
            m3.metric("Context Precision (Chính xác)", f"{avg_prec*100:.1f}%")
            m4.metric("Context Recall (Bao phủ)", f"{avg_rec*100:.1f}%")

            st.dataframe(df_eval, width=1200)

            chart_df = pd.DataFrame({
                "Chỉ số": ["Faithfulness", "Answer Relevance", "Context Precision", "Context Recall"],
                "Điểm số": [avg_faith, avg_rel, avg_prec, avg_rec]
            }).set_index("Chỉ số")
            st.bar_chart(chart_df)
        else:
            st.warning("Chưa tìm thấy file kết quả đánh giá. Hãy chạy `python src/evaluation/ragas_evaluator.py`.")
