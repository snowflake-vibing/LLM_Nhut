"""
Instant Petition & Legal Document Generator Engine - Version 4.1
Tự động sinh các mẫu Đơn khởi kiện, Đơn tố giác, Đơn khiếu nại chuẩn mẫu Hội đồng Thẩm phán TANDTC:
- Mẫu số 23-DS (Nghị quyết số 01/2017/NQ-HĐTP): Đơn khởi kiện dân sự.
- Đơn tố giác tội phạm lừa đảo chiếm đoạt tài sản (Điều 144, 145 BLTTHS 2015).
- Đơn yêu cầu hòa giải tranh chấp đất đai (Điều 202 Luật Đất đai).
- Đơn thuận tình / đơn phương ly hôn (Luật HNGĐ 2014).
Xuất trực tiếp file Word (.docx) điền sẵn căn cứ pháp luật và thông tin vụ việc của người dân.
"""

import io
import datetime
from typing import Dict, Any, Optional
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH


class InstantPetitionGenerator:
    """
    Máy phát sinh đơn từ pháp lý tức thì đạt chuẩn hình thức tư pháp Việt Nam.
    """

    @staticmethod
    def generate_lawsuit_petition_docx(data: Dict[str, Any]) -> io.BytesIO:
        """
        Sinh Đơn khởi kiện dân sự theo Mẫu số 23-DS (Nghị quyết 01/2017/NQ-HĐTP).
        """
        doc = docx.Document()
        
        # Thiết lập lề trang A4 chuẩn văn thư
        sections = doc.sections
        for s in sections:
            s.top_margin = Inches(0.8)
            s.bottom_margin = Inches(0.8)
            s.left_margin = Inches(1.0)
            s.right_margin = Inches(0.8)

        # Quốc hiệu & Tiêu ngữ
        p_qh = doc.add_paragraph()
        p_qh.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_qh1 = p_qh.add_run("CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM\n")
        r_qh1.bold = True
        r_qh1.font.size = Pt(12)
        r_qh2 = p_qh.add_run("Độc lập - Tự do - Hạnh phúc\n")
        r_qh2.bold = True
        r_qh2.font.size = Pt(13)
        r_line = p_qh.add_run("-----------------------")
        r_line.font.size = Pt(10)

        # Ngày tháng
        today = datetime.date.today()
        p_date = doc.add_paragraph()
        p_date.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r_d = p_date.add_run(f"..., ngày {today.day} tháng {today.month} năm {today.year}")
        r_d.italic = True
        r_d.font.size = Pt(11)

        # Tiêu đề đơn
        p_title = doc.add_paragraph()
        p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_t = p_title.add_run("\nĐƠN KHỞI KIỆN\n")
        r_t.bold = True
        r_t.font.size = Pt(16)
        r_sub = p_title.add_run(f"(V/v: {data.get('dispute_title', 'Tranh chấp hợp đồng vay tài sản')})\n")
        r_sub.italic = True
        r_sub.font.size = Pt(11)

        # Kính gửi
        court_name = data.get("court_name", "Tòa án nhân dân ......................................................")
        p_kg = doc.add_paragraph()
        p_kg.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_kg = p_kg.add_run(f"Kính gửi: {court_name}")
        r_kg.bold = True
        r_kg.font.size = Pt(12)

        # Thông tin Người khởi kiện
        doc.add_paragraph(
            f"1. Người khởi kiện: {data.get('plaintiff_name', '....................................................................................')}\n"
            f"   - Sinh năm: {data.get('plaintiff_dob', '....................')}    CCCD/CMND số: {data.get('plaintiff_cccd', '........................................')}\n"
            f"   - Nơi cư trú: {data.get('plaintiff_address', '................................................................................................................')}\n"
            f"   - Số điện thoại liên hệ: {data.get('plaintiff_phone', '........................................')}"
        )

        # Thông tin Người bị kiện
        doc.add_paragraph(
            f"2. Người bị kiện: {data.get('defendant_name', '....................................................................................')}\n"
            f"   - Nơi cư trú cuối cùng: {data.get('defendant_address', '................................................................................................')}\n"
            f"   - Số điện thoại (nếu có): {data.get('defendant_phone', '........................................')}"
        )

        # Nội dung vụ việc
        h_nd = doc.add_paragraph()
        r_hnd = h_nd.add_run("3. Nội dung sự việc:")
        r_hnd.bold = True
        
        incident_summary = data.get("incident_summary", (
            "Vào ngày ..../..../........, Bên bị kiện có vay của tôi số tiền là: .................................... VNĐ. "
            "Hai bên có thỏa thuận thời hạn trả nợ vào ngày ..../..../........ Tuy nhiên, đến hạn thanh toán, bên bị kiện "
            "không thực hiện nghĩa vụ trả nợ, cố tình trốn tránh, cắt liên lạc mặc dù tôi đã nhiều lần đôn đốc nhắc nhở."
        ))
        doc.add_paragraph(incident_summary)

        # Yêu cầu Tòa án giải quyết
        h_yc = doc.add_paragraph()
        r_hyc = h_yc.add_run("4. Những vấn đề cụ thể yêu cầu Tòa án nhân dân giải quyết:")
        r_hyc.bold = True
        
        petitions = data.get("petitions", [
            f"- Buộc bên bị kiện phải hoàn trả ngay cho tôi toàn bộ số tiền nợ gốc là: {data.get('claim_amount', '............................ VNĐ')}.",
            f"- Buộc bên bị kiện phải trả khoản tiền lãi phát sinh theo quy định tại Điều 468 Bộ luật Dân sự 2015 tính từ ngày quá hạn đến ngày thanh toán dứt điểm.",
            f"- Yêu cầu Tòa án áp dụng biện pháp khẩn cấp tạm thời (kê biên, phong tỏa tài khoản) nếu bên bị kiện có dấu hiệu tẩu tán tài sản."
        ])
        for pet in petitions:
            doc.add_paragraph(pet)

        # Danh mục chứng cứ kèm theo đơn
        h_cc = doc.add_paragraph()
        r_hcc = h_cc.add_run("5. Danh mục tài liệu, chứng cứ nộp kèm theo đơn khởi kiện:")
        r_hcc.bold = True
        
        evidence_list = data.get("evidence_list", [
            "1. Bản sao Căn cước công dân của Người khởi kiện (Có chứng thực).",
            "2. Hợp đồng vay tiền / Giấy biên nhận tiền viết tay (Bản chính/Bản sao).",
            "3. Vi bằng sao kê tài khoản ngân hàng và nhật ký tin nhắn Zalo/SMS chứng minh việc vay mượn.",
            "4. Văn bản xác nhận nơi cư trú của Bên bị kiện."
        ])
        for ev in evidence_list:
            doc.add_paragraph(f"   {ev}")

        # Lời cam đoan & Chữ ký
        doc.add_paragraph(
            "\nTôi cam đoan những lời khai trong đơn này là hoàn toàn đúng sự thật. "
            "Nếu có điều gì gian dối, tôi xin chịu hoàn toàn trách nhiệm trước pháp luật.\n"
        )

        p_sign = doc.add_paragraph()
        p_sign.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r_spos = p_sign.add_run("NGƯỜI KHỞI KIỆN\n")
        r_spos.bold = True
        r_note = p_sign.add_run("(Ký và ghi rõ họ tên)\n\n\n\n")
        r_note.italic = True
        r_name = p_sign.add_run(data.get("plaintiff_name", "........................................"))
        r_name.bold = True

        buf = io.BytesIO()
        doc.save(buf)
        buf.seek(0)
        return buf

    @staticmethod
    def generate_denunciation_petition_docx(data: Dict[str, Any]) -> io.BytesIO:
        """
        Sinh Đơn tố giác tội phạm lừa đảo / lạm dụng tín nhiệm chiếm đoạt tài sản.
        """
        doc = docx.Document()
        sections = doc.sections
        for s in sections:
            s.top_margin = Inches(0.8)
            s.bottom_margin = Inches(0.8)
            s.left_margin = Inches(1.0)
            s.right_margin = Inches(0.8)

        p_qh = doc.add_paragraph()
        p_qh.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_qh.add_run("CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM\nĐộc lập - Tự do - Hạnh phúc\n-----------------------").bold = True

        today = datetime.date.today()
        p_date = doc.add_paragraph()
        p_date.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_date.add_run(f"..., ngày {today.day} tháng {today.month} năm {today.year}").italic = True

        p_title = doc.add_paragraph()
        p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_title.add_run("\nĐƠN TỐ GIÁC TỘI PHẠM\n").bold = True
        p_title.add_run("(V/v: Hành vi có dấu hiệu 'Lừa đảo chiếm đoạt tài sản' theo Điều 174 BLHS)").italic = True

        police_agency = data.get("police_agency", "Cơ quan Cảnh sát điều tra Công an ......................................................")
        p_kg = doc.add_paragraph()
        p_kg.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_kg.add_run(f"Kính gửi:\n- {police_agency}\n- Viện kiểm sát nhân dân cùng cấp").bold = True

        doc.add_paragraph(
            f"Tôi là: {data.get('applicant_name', '....................................................................................')}\n"
            f"CCCD số: {data.get('applicant_cccd', '........................................')}  Cấp ngày: .................... Tại: ....................\n"
            f"Địa chỉ cư trú: {data.get('applicant_address', '................................................................................................')}\n"
            f"Số điện thoại: {data.get('applicant_phone', '........................................')}"
        )

        doc.add_paragraph(
            f"Tố giác đối tượng: {data.get('suspect_name', '....................................................................................')}\n"
            f"Nơi cư trú hoặc tài khoản ngân hàng liên quan: {data.get('suspect_info', '................................................................')}"
        )

        h_nd = doc.add_paragraph()
        h_nd.add_run("NỘI DUNG TỐ GIÁC:").bold = True
        doc.add_paragraph(data.get("crime_summary", (
            "Bằng các thủ đoạn gian dối qua mạng / trực tiếp, đối tượng đã đưa ra các thông tin sai sự thật để tôi tin tưởng "
            "và chuyển cho đối tượng số tiền là: .................................... VNĐ. Sau khi nhận được tiền, đối tượng đã ngay lập tức "
            "chặn liên lạc, khóa tài khoản nhằm mục đích chiếm đoạt toàn bộ số tiền trên."
        )))

        h_yc = doc.add_paragraph()
        h_yc.add_run("YÊU CẦU CƠ QUAN ĐIỀU TRA:").bold = True
        doc.add_paragraph(
            "1. Tiếp nhận nguồn tin tố giác tội phạm theo Điều 144, 145 Bộ luật Tố tụng Hình sự 2015.\n"
            "2. Khẩn cấp phong tỏa tài khoản ngân hàng của đối tượng nhận tiền để ngăn chặn hành vi tẩu tán.\n"
            "3. Khởi tố vụ án hình sự để điều tra, xử lý nghiêm minh theo quy định của pháp luật và thu hồi tài sản trả lại cho tôi."
        )

        p_sign = doc.add_paragraph()
        p_sign.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_sign.add_run("NGƯỜI TỐ GIÁC\n(Ký và ghi rõ họ tên)\n\n\n\n").bold = True
        p_sign.add_run(data.get("applicant_name", "........................................")).bold = True

        buf = io.BytesIO()
        doc.save(buf)
        buf.seek(0)
        return buf
