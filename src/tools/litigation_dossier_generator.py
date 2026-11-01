# -*- coding: utf-8 -*-
"""
Module Đóng Gói Bộ Hồ Sơ Tố Tụng Hoàn Chỉnh (Litigation Dossier Generator)
Phiên bản 5.1 - Trọn gói hồ sơ tư pháp chuyên nghiệp nộp thẳng đến Tòa án Nhân dân.
Tích hợp: Đơn khởi kiện Mẫu 23-DS + Bảng tạm tính Án phí + Chiến lược Bàn cờ 2 Chiều + Danh mục chứng cứ.
"""

import io
from typing import Optional, Dict, Any
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT


class LitigationDossierGenerator:
    """Động cơ đóng gói bộ hồ sơ khởi kiện trọn gói cho công dân."""

    @staticmethod
    def generate_dossier_docx(
        court_name: str,
        plaintiff_name: str,
        plaintiff_year: str,
        plaintiff_id: str,
        plaintiff_address: str,
        plaintiff_phone: str,
        defendant_name: str,
        defendant_address: str,
        claim_amount: float,
        dispute_summary: str,
        evidence_list: Optional[list] = None,
        court_fee_details: Optional[Dict[str, Any]] = None,
        simulation_data: Optional[Dict[str, Any]] = None
    ) -> io.BytesIO:
        """Sinh file Word (.docx) Bộ Hồ Sơ Khởi Kiện Dân Sự Toàn Diện."""
        doc = Document()

        # Định dạng trang A4
        sections = doc.sections
        for section in sections:
            section.top_margin = Inches(0.8)
            section.bottom_margin = Inches(0.8)
            section.left_margin = Inches(1.0)
            section.right_margin = Inches(0.8)

        # Trang Bìa / Quốc hiệu
        p_qh = doc.add_paragraph()
        p_qh.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_qh = p_qh.add_run("CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM\nĐộc lập - Tự do - Hạnh phúc")
        run_qh.font.name = "Times New Roman"
        run_qh.font.size = Pt(13)
        run_qh.bold = True

        p_line = doc.add_paragraph()
        p_line.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_line = p_line.add_run("-----------------------")
        run_line.bold = True

        # Tiêu đề tập hồ sơ
        p_title = doc.add_paragraph()
        p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_title = p_title.add_run("BỘ HỒ SƠ KHỞI KIỆN VÀ TÀI LIỆU TRANH TỤNG DÂN SỰ\n(BẢN CHÍNH THỨC NỘP TÒA ÁN NHÂN DÂN)")
        run_title.font.name = "Times New Roman"
        run_title.font.size = Pt(16)
        run_title.bold = True
        run_title.font.color.rgb = RGBColor(0, 51, 102)

        # Thông tin gửi Tòa
        p_to = doc.add_paragraph()
        p_to.paragraph_format.space_before = Pt(14)
        run_to = p_to.add_run(f"Kính gửi: TÒA ÁN NHÂN DÂN {court_name.upper()}")
        run_to.bold = True
        run_to.font.size = Pt(13)

        # MỤC LỤC BỘ HỒ SƠ
        p_toc = doc.add_paragraph()
        p_toc.paragraph_format.space_before = Pt(10)
        p_toc.add_run("DANH MỤC CÁC PHẦN TRONG BỘ HỒ SƠ:\n").bold = True
        p_toc.add_run("1. PHẦN I: ĐƠN KHỞI KIỆN (MẪU SỐ 23-DS CỦA TAND TỐI CAO)\n")
        p_toc.add_run("2. PHẦN II: BẢNG GIẢI TRÌNH & DỰ TRÙ ÁN PHÍ DÂN SỰ TẠM ỨNG (NQ 326/2016)\n")
        p_toc.add_run("3. PHẦN III: BÁO CÁO CHIẾN LƯỢC BÀN CỜ TỐ TỤNG & BIỆN PHÁP KHẨN CẤP TẠM THỜI\n")
        p_toc.add_run("4. PHẦN IV: DANH MỤC TÀI LIỆU, CHỨNG CỨ KÈM THEO VÀ HƯỚNG DẪN NỘP TÒA\n")

        doc.add_page_break()

        # ==========================================
        # PHẦN I: ĐƠN KHỞI KIỆN (MẪU 23-DS)
        # ==========================================
        h1 = doc.add_heading("PHẦN I: ĐƠN KHỞI KIỆN DÂN SỰ", level=1)
        h1.paragraph_format.space_before = Pt(10)

        p_sub = doc.add_paragraph()
        p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_sub.add_run("(Ban hành kèm theo Nghị quyết số 01/2017/NQ-HĐTP ngày 13/01/2017 của Hội đồng Thẩm phán TANDTC)").italic = True

        p_info = doc.add_paragraph()
        p_info.add_run("1. Người khởi kiện: ").bold = True
        p_info.add_run(f"{plaintiff_name.upper()}  (Sinh năm: {plaintiff_year})\n")
        p_info.add_run(f"- CCCD/CMND số: {plaintiff_id}\n")
        p_info.add_run(f"- Nơi cư trú: {plaintiff_address}\n")
        p_info.add_run(f"- Số điện thoại liên hệ: {plaintiff_phone}\n\n")

        p_info.add_run("2. Người bị kiện: ").bold = True
        p_info.add_run(f"{defendant_name.upper()}\n")
        p_info.add_run(f"- Nơi cư trú hiện nay: {defendant_address}\n\n")

        p_info.add_run("3. Nội dung sự việc và căn cứ khởi kiện:\n").bold = True
        p_info.add_run(f"{dispute_summary}\n\n")

        p_info.add_run("4. Yêu cầu Tòa án giải quyết những vấn đề sau:\n").bold = True
        p_info.add_run(f"- Buộc {defendant_name} phải thanh toán trả cho tôi toàn bộ số tiền nợ gốc là: {claim_amount:,.0f} VNĐ.\n")
        p_info.add_run(f"- Buộc {defendant_name} thanh toán khoản tiền lãi chậm trả theo quy định tại Khoản 2 Điều 468 Bộ luật Dân sự 2015 tính từ ngày quá hạn đến ngày thực tế thi hành án xong.\n")
        p_info.add_run(f"- Buộc bên bị kiện phải chịu toàn bộ án phí dân sự sơ thẩm theo quy định pháp luật.\n")

        # ==========================================
        # PHẦN II: BẢNG TẠM TÍNH ÁN PHÍ NQ 326/2016
        # ==========================================
        doc.add_heading("PHẦN II: BẢNG GIẢI TRÌNH & DỰ TRÙ ÁN PHÍ DÂN SỰ SƠ THẨM", level=1)
        p_fee_intro = doc.add_paragraph()
        p_fee_intro.add_run("Căn cứ Nghị quyết số 326/2016/UBTVQH14 của Ủy ban Thường vụ Quốc hội quy định về mức thu, miễn, giảm, thu, nộp, quản lý và sử dụng án phí và lệ phí Tòa án:")

        fee_table = doc.add_table(rows=4, cols=2)
        fee_table.style = "Table Grid"
        fee_table.alignment = WD_TABLE_ALIGNMENT.CENTER

        est_fee = court_fee_details.get("court_fee", claim_amount * 0.05) if court_fee_details else claim_amount * 0.05
        est_advance = court_fee_details.get("advance_payment", est_fee * 0.5) if court_fee_details else est_fee * 0.5

        data = [
            ("Giá trị tranh chấp (Giá ngạch)", f"{claim_amount:,.0f} VNĐ"),
            ("Án phí dân sự sơ thẩm dự kiến", f"{est_fee:,.0f} VNĐ"),
            ("Mức Tạm ứng án phí phải nộp (50%)", f"{est_advance:,.0f} VNĐ"),
            ("Cơ quan thu tiền tạm ứng án phí", f"Chi cục Thi hành án dân sự {court_name}")
        ]

        for i, (k, v) in enumerate(data):
            row = fee_table.rows[i]
            row.cells[0].paragraphs[0].add_run(k).bold = True
            row.cells[1].paragraphs[0].add_run(v)

        doc.add_paragraph().paragraph_format.space_after = Pt(12)

        # ==========================================
        # PHẦN III: BÁO CÁO BÀN CỜ TỐ TỤNG 2 CHIỀU
        # ==========================================
        doc.add_heading("PHẦN III: BÁO CÁO CHIẾN LƯỢC BÀN CỜ TỐ TỤNG 2 CHIỀU & BẢO TOÀN TÀI SẢN", level=1)
        p_sim = doc.add_paragraph()
        win_rate = simulation_data.get("win_rate_percent", 80) if simulation_data else 80
        p_sim.add_run(f"★ ĐÁNH GIÁ TỶ LỆ THẮNG KIỆN KHÁCH QUAN: {win_rate}%\n").bold = True

        p_atk = doc.add_paragraph()
        p_atk.add_run("1. Mũi tấn công pháp lý của Nguyên đơn:\n").bold = True
        p_atk.add_run("- Xác lập quan hệ hợp đồng vay tài sản hợp pháp căn cứ Điều 463 BLDS 2015.\n")
        p_atk.add_run("- Nghĩa vụ trả nợ đến hạn của bên vay căn cứ Điều 466 BLDS 2015.\n")
        p_atk.add_run("- Bằng chứng chứng minh việc giao nhận tiền rõ ràng, không bị cưỡng ép.\n\n")

        p_def = doc.add_paragraph()
        p_def.add_run("2. Các chiêu bài phản đòn Bị đơn thường áp dụng tại Tòa:\n").bold = True
        p_def.add_run("- Chối bỏ chữ ký hoặc viện cớ ký trong tình trạng không minh mẫn để yêu cầu giám định kéo dài thời gian.\n")
        p_def.add_run("- Nại lý do đây là tiền góp vốn hợp tác đầu tư bị thua lỗ chứ không phải khoản vay có hoàn lại.\n")
        p_def.add_run("- Tìm cách tẩu tán tài sản (chuyển nhượng nhà đất, rút tiền ngân hàng) trước khi Tòa tuyên án.\n\n")

        p_strat = doc.add_paragraph()
        p_strat.add_run("3. Kế sách phòng thủ & hóa giải tuyệt đối:\n").bold = True
        p_strat.add_run("★ NỘP NGAY ĐƠN YÊU CẦU ÁP DỤNG BIỆN PHÁP KHẨN CẤP TẠM THỜI (Điều 111, 120 BLTTDS 2015):\n")
        p_strat.add_run("  + Đề nghị Tòa án ra Quyết định phong tỏa tài khoản ngân hàng của bị đơn.\n")
        p_strat.add_run("  + Kê biên tài sản hoặc cấm chuyển dịch tài sản đang có tranh chấp.\n")
        p_strat.add_run("★ Xuất trình bản chính chứng cứ để đối chiếu; lập Vi bằng Thừa phát lại toàn bộ tin nhắn Zalo/SMS xác nhận nợ.\n")

        # ==========================================
        # PHẦN IV: DANH MỤC CHỨNG CỨ & KÝ TÊN
        # ==========================================
        doc.add_heading("PHẦN IV: DANH MỤC TÀI LIỆU CHỨNG CỨ NỘP KÈM & CHỮ KÝ", level=1)
        p_docs = doc.add_paragraph()
        p_docs.add_run("Danh mục chứng cứ gửi kèm theo đơn khởi kiện:\n").bold = True

        if not evidence_list:
            evidence_list = [
                "1. Bản sao chứng thực Căn cước công dân của người khởi kiện.",
                "2. Bản gốc Giấy nhận nợ / Giấy vay tiền có chữ ký của bên vay.",
                "3. Bản in sao kê tài khoản ngân hàng thể hiện giao dịch chuyển tiền.",
                "4. Vi bằng / Biên bản ghi nhận tin nhắn Zalo, SMS trao đổi hứa hẹn trả nợ.",
                "5. Giấy xác nhận thông tin cư trú của bên bị kiện."
            ]

        for item in evidence_list:
            p_docs.add_run(f"- {item}\n")

        p_sign = doc.add_paragraph()
        p_sign.paragraph_format.space_before = Pt(20)
        p_sign.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_sign.add_run("NGƯỜI KHỞI KIỆN\n(Ký và ghi rõ họ tên)\n\n\n\n").bold = True
        p_sign.add_run(f"{plaintiff_name.upper()}\n").bold = True

        # Lưu vào luồng nhớ
        output_stream = io.BytesIO()
        doc.save(output_stream)
        output_stream.seek(0)
        return output_stream
