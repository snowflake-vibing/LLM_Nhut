"""
LegalTech SME Assistant - Streamlit Application
Giao diện người dùng đa chức năng đáp ứng trọn vẹn 7 tiêu chí đồ án AI Engineer.
"""

import os
import sys
import json
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

# Cấu hình giao diện Streamlit
st.set_page_config(
    page_title="LegalTech SME Assistant",
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
                "👋 **Xin chào! Tôi là Trợ lý AI Tư vấn Pháp lý Khởi nghiệp (LegalTech SME Assistant).**\n\n"
                "Tôi có thể hỗ trợ bạn:\n"
                "- 🏢 Tư vấn lựa chọn mô hình: *Hộ kinh doanh cá thể, Công ty TNHH 1TV, 2TV hay Cổ phần*.\n"
                "- 🔍 Tra cứu mã ngành kinh tế (VSIC 2018) và các điều kiện giấy phép con (*ATVSTP, PCCC...*).\n"
                "- 📋 Lên lộ trình từng bước và checklist hồ sơ thành lập doanh nghiệp.\n\n"
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

# --- SIDEBAR: CẤU HÌNH & MODEL SWITCHER ---
with st.sidebar:
    st.title("⚖️ Cấu hình Hệ thống")
    st.markdown("---")

    st.subheader("⚡ Chế độ Mô hình (Model Mode)")
    current_mode = st.session_state.factory.current_provider_type.value
    selected_mode = st.radio(
        "Chọn môi trường LLM:",
        options=["cloud", "local"],
        format_func=lambda x: "☁️ Cloud Model (Google Gemini API)" if x == "cloud" else "💻 Local Model (Ollama / Llama 3)",
        index=0 if current_mode == "cloud" else 1
    )

    if selected_mode != current_mode:
        st.session_state.factory.set_provider(selected_mode)
        st.success(f"Đã chuyển sang chế độ: **{selected_mode.upper()}**")

    # Kiểm tra trạng thái kết nối
    st.markdown("---")
    st.subheader("📡 Trạng thái Kết nối (Health Check)")
    health = st.session_state.factory.check_health()

    c1, c2 = st.columns(2)
    with c1:
        if health["cloud"]["available"]:
            st.markdown("🟢 **Cloud:** Sẵn sàng")
        else:
            st.markdown("🟡 **Cloud:** Chưa có API Key")
    with c2:
        if health["local"]["available"]:
            st.markdown("🟢 **Local:** Online")
        else:
            st.markdown("🔴 **Local:** Offline")

    st.caption(f"Model Cloud: `{health['cloud']['model']}`")
    st.caption(f"Model Local: `{health['local']['model']}`")

    st.markdown("---")
    st.info(
        "🛡️ **Lớp Bảo mật (Guardrails):**\n"
        "- Tự động ẩn danh CCCD, SĐT, Email (PII Masking)\n"
        "- Chống bẻ khóa Jailbreak & Prompt Injection\n"
        "- Tuân thủ Điều 16 Luật Doanh nghiệp 2020"
    )

# --- KHU VỰC NỘI DUNG CHÍNH: 4 TABS ---
tab_chat, tab_db, tab_security, tab_eval = st.tabs([
    "💬 Trò chuyện Trợ lý Pháp lý",
    "📚 Tra cứu Mã ngành & Giấy phép (Database)",
    "🛡️ Giám sát Bảo mật & Model Switcher",
    "📊 Đánh giá Benchmark (Ragas Evaluation)"
])

# ==================== TAB 1: CHATBOT ====================
with tab_chat:
    st.header("💬 Trò chuyện cùng Trợ lý Pháp lý SME")
    st.caption("Ứng dụng Multi-Agent Orchestration + RAG Luật Doanh nghiệp 2020 + CSDL VSIC 2018")

    # Hiển thị lịch sử chat
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("citations"):
                with st.expander("📖 Căn cứ pháp luật trích dẫn (Citations)"):
                    for c in msg["citations"]:
                        st.markdown(f"- `{c}`")
            if msg.get("agent") and msg["role"] == "assistant":
                st.caption(f"🤖 Xử lý bởi Agent: **{msg['agent']}**")

    # Input từ người dùng
    user_input = st.chat_input("Nhập câu hỏi hoặc ý tưởng kinh doanh của bạn...")
    if user_input:
        # Lưu câu hỏi người dùng
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Xử lý qua Multi-Agent Workflow
        with st.chat_message("assistant"):
            with st.spinner("AI Agents đang phân tích và tra cứu căn cứ pháp lý..."):
                result = st.session_state.workflow.process(user_input)

            resp_text = result["response"]
            st.markdown(resp_text)

            if result.get("citations"):
                with st.expander("📖 Căn cứ pháp luật trích dẫn (Citations)"):
                    for c in result["citations"]:
                        st.markdown(f"- `{c}`")

            st.caption(f"🤖 Xử lý bởi Agent: **{result['active_agent']}**")

            # Lưu vào session
            st.session_state.messages.append({
                "role": "assistant",
                "content": resp_text,
                "agent": result["active_agent"],
                "citations": result.get("citations", [])
            })

# ==================== TAB 2: TRA CỨU CSDL ====================
with tab_db:
    st.header("📚 Tra cứu CSDL Mã ngành Kinh tế & Điều kiện Giấy phép")
    st.caption("Dữ liệu đọc trực tiếp từ SQLite Database (`sme_legal.db`)")

    search_kw = st.text_input("Nhập từ khóa ngành nghề cần tra cứu (VD: cà phê, ăn uống, phần mềm, mỹ phẩm...):", value="cà phê")
    if search_kw:
        industries = st.session_state.db_manager.search_industry(search_kw)
        st.subheader(f"Kết quả tra cứu mã ngành cho: '{search_kw}' ({len(industries)} kết quả)")
        if industries:
            df_ind = pd.DataFrame(industries)
            st.dataframe(df_ind, use_container_width=True)
        else:
            st.warning("Không tìm thấy mã ngành phù hợp.")

        st.markdown("---")
        licenses = st.session_state.db_manager.get_license_info(search_kw)
        st.subheader("Điều kiện Giấy phép con & Căn cứ Pháp lý liên quan:")
        if licenses:
            for lic in licenses:
                with st.expander(f"📜 {lic['license_name']} - Cơ quan cấp: {lic['issuing_body']}"):
                    st.markdown(f"- **Thời gian xử lý chuẩn:** {lic['standard_duration_days']} ngày làm việc")
                    st.markdown(f"- **Lệ phí nhà nước:** {lic['estimated_fee']:,} VNĐ")
                    st.markdown(f"- **Căn cứ pháp lý:** {lic['legal_basis']}")
                    st.markdown(f"- **Thành phần hồ sơ:** {lic['required_dossier']}")
        else:
            st.info("Không có yêu cầu giấy phép con đặc thù cho từ khóa này (hoặc ngành nghề kinh doanh tự do).")

# ==================== TAB 3: BẢO MẬT & MODEL SWITCHER ====================
with tab_security:
    st.header("🛡️ Giám sát Bảo mật (Security & Guardrails Monitor)")
    st.caption("Hiện thực hóa Tiêu chí 7: Bảo mật LLM & Che giấu thông tin PII")

    st.subheader("1. Thử nghiệm Lọc Thông tin Định danh Cá nhân (PII Masking)")
    sample_pii = st.text_area(
        "Nhập đoạn văn bản có chứa CCCD, SĐT, Email để kiểm tra:",
        value="Tôi là Nguyễn Văn Nhựt, CCCD 079201004567, SĐT 0912345678, email nhut@gmail.com muốn thành lập công ty."
    )
    if st.button("Chạy thử nghiệm PII Masking"):
        masker = PIIMasker()
        masked, mapping = masker.mask_text(sample_pii)
        st.success("✅ Đã xử lý che giấu thông tin!")
        st.markdown(f"**Văn bản sau khi Mask (gửi đến LLM):**\n`{masked}`")
        st.json(mapping)

    st.markdown("---")
    st.subheader("2. Thử nghiệm Chống Tấn công Jailbreak & Ý định Trái luật")
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

# ==================== TAB 4: ĐÁNH GIÁ MÔ HÌNH ====================
with tab_eval:
    st.header("📊 Bảng điều khiển Đánh giá Mô hình (Ragas Evaluation Dashboard)")
    st.caption("Hiện thực hóa Tiêu chí 6: Đánh giá mô hình LLM với 4 chỉ số cốt lõi")

    results_csv_path = os.path.join(ROOT_DIR, "reports", "evaluation_results.csv")
    if os.path.exists(results_csv_path):
        df_eval = pd.read_csv(results_csv_path)

        # Tính toán metric trung bình
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
        st.dataframe(df_eval, use_container_width=True)

        st.subheader("Biểu đồ so sánh 4 chỉ số chất lượng RAG:")
        chart_data = pd.DataFrame({
            "Chỉ số": ["Faithfulness", "Answer Relevance", "Context Precision", "Context Recall"],
            "Điểm số": [avg_faith, avg_rel, avg_prec, avg_rec]
        }).set_index("Chỉ số")
        st.bar_chart(chart_data)
    else:
        st.warning("Chưa tìm thấy file kết quả đánh giá. Hãy chạy script `python src/evaluation/ragas_evaluator.py` để sinh kết quả.")
