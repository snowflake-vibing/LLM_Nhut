"""
Dynamic Legal Document Drafter Module - Version 2.1
Soạn thảo Văn bản Pháp lý Đa dạng theo Yêu cầu với Form Thông minh & Placeholder Linh hoạt:
- Tự động điền sẵn 100% căn cứ pháp luật và nội dung tranh tụng chuẩn mực.
- Trường thông tin cá nhân: người dùng nhập thì lấy giá trị, để trống thì AI tự động
  chèn dòng kẻ giữ chỗ (........................) hoặc nhãn [PLACEHOLDER] để tải về ký/điền tay.
- Hỗ trợ xuất file Word (.docx) chuẩn thể thức tư pháp Việt Nam (Nghị định 30/2020/NĐ-CP).
"""

import io
from typing import Dict, Any, Optional
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

from llm_provider.model_factory import ModelFactory


def _val_or_placeholder(val: Optional[str], placeholder_label: str = "........................................................") -> str:
    """Trả về giá trị người dùng nhập, nếu rỗng thì trả về placeholder chuẩn tư pháp."""
    if val and str(val).strip():
        return str(val).strip()
    return placeholder_label


def _setup_docx_page_and_header(doc: Document, document_title: str) -> None:
    """Thiết lập căn lề chuẩn Nghị định 30/2020/NĐ-CP và Quốc hiệu Tiêu ngữ."""
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(0.8)

    # Quốc hiệu - Tiêu ngữ
    p_quoc_hieu = doc.add_paragraph()
    p_quoc_hieu.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_qh1 = p_quoc_hieu.add_run("CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM\n")
    r_qh1.bold = True
    r_qh1.font.size = Pt(13)
    r_qh1.font.name = "Times New Roman"

    r_qh2 = p_quoc_hieu.add_run("Độc lập - Tự do - Hạnh phúc\n")
    r_qh2.bold = True
    r_qh2.font.size = Pt(14)
    r_qh2.font.name = "Times New Roman"

    r_qh3 = p_quoc_hieu.add_run("---------------o0o---------------\n\n")
    r_qh3.font.name = "Times New Roman"

    # Tiêu đề văn bản
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t = p_title.add_run(document_title.upper() + "\n")
    r_t.bold = True
    r_t.font.size = Pt(16)
    r_t.font.name = "Times New Roman"


class DynamicLegalDrafter:
    """
    Engine soạn thảo văn bản pháp lý đa dạng và linh hoạt theo biểu mẫu chuẩn.
    """

    def __init__(self, factory: Optional[ModelFactory] = None):
        self.factory = factory or ModelFactory()

    # 1. ĐƠN KHỞI KIỆN ĐÒI NỢ
    def draft_debt_lawsuit(self, data: Dict[str, Any]) -> io.BytesIO:
        doc = Document()
        _setup_docx_page_and_header(doc, "ĐƠN KHỞI KIỆN VỀ VIỆC TRANH CHẤP HỢP ĐỒNG VAY TÀI SẢN")

        toan = _val_or_placeholder(data.get("court_name"), "Tòa án nhân dân huyện/quận .....................................................")
        p_kinh_gui = doc.add_paragraph()
        p_kinh_gui.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_kg = p_kinh_gui.add_run(f"Kính gửi: {toan}\n")
        r_kg.bold = True
        r_kg.font.name = "Times New Roman"
        r_kg.font.size = Pt(13)

        pl_name = _val_or_placeholder(data.get("plaintiff_name"), "....................................................................................")
        pl_cccd = _val_or_placeholder(data.get("plaintiff_cccd"), ".................................. cấp ngày ...../...../......... tại ..................................")
        pl_addr = _val_or_placeholder(data.get("plaintiff_address"), "....................................................................................")
        pl_phone = _val_or_placeholder(data.get("plaintiff_phone"), "........................................")

        df_name = _val_or_placeholder(data.get("defendant_name"), "....................................................................................")
        df_cccd = _val_or_placeholder(data.get("defendant_cccd"), ".................................. cấp ngày ...../...../......... tại ..................................")
        df_addr = _val_or_placeholder(data.get("defendant_address"), "....................................................................................")
        df_last_seen = _val_or_placeholder(data.get("defendant_last_seen"), "....................................................................................")

        principal = _val_or_placeholder(data.get("principal_amount"), "................................................ VNĐ")
        interest = _val_or_placeholder(data.get("interest_amount"), "................................................ VNĐ")
        total = _val_or_placeholder(data.get("total_amount"), "................................................ VNĐ")
        loan_date = _val_or_placeholder(data.get("loan_date"), "ngày ..... tháng ..... năm 20.....")
        due_date = _val_or_placeholder(data.get("due_date"), "ngày ..... tháng ..... năm 20.....")

        body_text = (
            f"I. THÔNG TIN CÁC BÊN ĐƯƠNG SỰ:\n"
            f"1. Người khởi kiện (Nguyên đơn): Ông/Bà {pl_name}\n"
            f"   - CCCD số: {pl_cccd}\n"
            f"   - Nơi cư trú hiện tại: {pl_addr}\n"
            f"   - Số điện thoại liên hệ: {pl_phone}\n\n"
            f"2. Người bị kiện (Bị đơn): Ông/Bà {df_name}\n"
            f"   - CCCD số: {df_cccd}\n"
            f"   - Nơi cư trú cuối cùng trước khi bỏ trốn/vắng mặt: {df_addr}\n"
            f"   - Tình trạng cư trú hiện nay: {df_last_seen}\n\n"
            f"II. CĂN CỨ VÀ NỘI DUNG VỤ VIỆC:\n"
            f"- Căn cứ Hợp đồng vay/Giấy mượn tiền xác lập vào {loan_date}, Nguyên đơn có cho Bị đơn vay số tiền gốc là {principal}.\n"
            f"- Theo thỏa thuận, thời hạn hoàn trả là vào {due_date}. Tuy nhiên, đến hạn thanh toán, Bị đơn đã không hoàn trả, cố tình trốn tránh, cắt đứt liên lạc và rời khỏi nơi cư trú.\n"
            f"- Căn cứ Điều 463 và Điều 466 Bộ luật Dân sự 2015, bên vay có nghĩa vụ trả đủ tiền khi đến hạn. Hành vi trốn tránh của Bị đơn đã xâm phạm trực tiếp đến quyền và lợi ích hợp pháp của Nguyên đơn.\n"
            f"- Căn cứ Điều 39 và Điều 40 Bộ luật Tố tụng Dân sự 2015, Tòa án nhân dân nơi Bị đơn cư trú hoặc làm việc cuối cùng có thẩm quyền thụ lý và giải quyết theo quy định.\n\n"
            f"III. YÊU CẦU TÒA ÁN GIẢI QUYẾT:\n"
            f"1. Buộc Bị đơn là Ông/Bà {df_name} phải thanh toán toàn bộ số tiền nợ gốc: {principal}.\n"
            f"2. Buộc Bị đơn thanh toán số tiền lãi chậm trả theo quy định pháp luật: {interest}.\n"
            f"   ==> TỔNG CỘNG SỐ TIỀN YÊU CẦU THANH TOÁN: {total}.\n"
            f"3. Đề nghị Tòa án áp dụng biện pháp khẩn cấp tạm thời phong tỏa tài sản hoặc niêm yết xét xử vắng mặt nếu Bị đơn cố tình không có mặt theo giấy triệu tập.\n\n"
            f"IV. DANH MỤC TÀI LIỆU, CHỨNG CỨ KÈM THEO:\n"
            f"1. Bản sao Giấy mượn tiền / Hợp đồng vay tiền / Giấy nhận tiền.\n"
            f"2. Sao kê tài khoản ngân hàng chuyển tiền (nếu có).\n"
            f"3. Bản sao CCCD của Nguyên đơn.\n"
            f"4. Văn bản xác nhận tình trạng cư trú của Bị đơn tại địa phương."
        )

        for p_line in body_text.split("\n\n"):
            p = doc.add_paragraph(p_line)
            p.paragraph_format.line_spacing = 1.2
            for run in p.runs:
                run.font.name = "Times New Roman"
                run.font.size = Pt(13)

        # Chữ ký
        p_sign = doc.add_paragraph("\n......, ngày ..... tháng ..... năm 20.....\nNGƯỜI KHỞI KIỆN\n(Ký và ghi rõ họ tên)\n\n\n\n")
        p_sign.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        for run in p_sign.runs:
            run.font.name = "Times New Roman"
            run.font.size = Pt(13)

        buf = io.BytesIO()
        doc.save(buf)
        buf.seek(0)
        return buf

    # 2. ĐƠN YÊU CẦU HÒA GIẢI TRANH CHẤP ĐẤT ĐAI
    def draft_land_dispute(self, data: Dict[str, Any]) -> io.BytesIO:
        doc = Document()
        _setup_docx_page_and_header(doc, "ĐƠN YÊU CẦU HÒA GIẢI TRANH CHẤP RANH GIỚI ĐẤT ĐAI")

        ubnd = _val_or_placeholder(data.get("ubnd_name"), "Ủy ban nhân dân xã/phường .....................................................")
        p_kinh_gui = doc.add_paragraph()
        p_kinh_gui.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_kg = p_kinh_gui.add_run(f"Kính gửi: {ubnd}\n")
        r_kg.bold = True
        r_kg.font.name = "Times New Roman"
        r_kg.font.size = Pt(13)

        applicant = _val_or_placeholder(data.get("applicant_name"), "....................................................................................")
        app_cccd = _val_or_placeholder(data.get("applicant_cccd"), "........................................................")
        app_addr = _val_or_placeholder(data.get("applicant_address"), "....................................................................................")

        neighbor = _val_or_placeholder(data.get("neighbor_name"), "....................................................................................")
        neighbor_addr = _val_or_placeholder(data.get("neighbor_address"), "....................................................................................")

        parcel_info = _val_or_placeholder(data.get("parcel_info"), "Thửa đất số ......., Tờ bản đồ số ....... tại ....................................................")
        gcn_info = _val_or_placeholder(data.get("gcn_info"), "GCN QSDĐ số ................. do UBND ................. cấp ngày ...../...../.........")
        encroach_desc = _val_or_placeholder(data.get("encroachment_desc"), "Hành vi xây dựng tường rào / cắm cọc / công trình lấn sang ranh giới đất khoảng ..... mét vuông.")

        body_text = (
            f"I. THÔNG TIN NGƯỜI LÀM ĐƠN VÀ BÊN LIÊN QUAN:\n"
            f"1. Người yêu cầu hòa giải: Ông/Bà {applicant}\n"
            f"   - CCCD: {app_cccd} - Địa chỉ: {app_addr}\n"
            f"   - Là chủ sử dụng hợp pháp đối với {parcel_info} theo {gcn_info}.\n\n"
            f"2. Bên có tranh chấp (Hộ liền kề): Ông/Bà {neighbor}\n"
            f"   - Địa chỉ thửa đất liền kề: {neighbor_addr}\n\n"
            f"II. NỘI DUNG SỰ VIỆC TRANH CHẤP:\n"
            f"- Gia đình tôi là chủ sử dụng đất hợp pháp, đã được cấp Giấy chứng nhận quyền sử dụng đất và quản lý sử dụng ổn định từ trước đến nay.\n"
            f"- Vừa qua, hộ gia đình liền kề của Ông/Bà {neighbor} đã có hành vi: {encroach_desc}, làm thay đổi mốc giới hiện trạng và xâm phạm trực tiếp đến diện tích đất đã được cấp giấy của gia đình tôi.\n"
            f"- Hai bên đã tự thương lượng nhiều lần nhưng không đạt được thỏa thuận.\n\n"
            f"III. CĂN CỨ PHÁP LÝ:\n"
            f"- Căn cứ Điều 175, 176 Bộ luật Dân sự 2015 về ranh giới và mốc giới ngăn cách bất động sản liền kề.\n"
            f"- Căn cứ Điều 202 Luật Đất đai quy định: Tranh chấp đất đai mà các bên không tự hòa giải được thì gửi đơn đến UBND cấp xã nơi có đất tranh chấp để hòa giải.\n\n"
            f"IV. NỘI DUNG YÊU CẦU GIẢI QUYẾT:\n"
            f"1. Kính đề nghị UBND xã/phường tổ chức đoàn cán bộ địa chính xuống đo đạc, kiểm tra hiện trạng mốc giới thửa đất giữa hai gia đình.\n"
            f"2. Tổ chức phiên họp hòa giải theo đúng trình tự luật định và lập Biên bản hòa giải theo quy định tại Khoản 4 Điều 202 Luật Đất đai.\n"
            f"3. Yêu cầu bên lấn chiếm chấm dứt hành vi xây dựng và hoàn trả lại nguyên trạng ranh giới đất theo Sổ đỏ."
        )

        for p_line in body_text.split("\n\n"):
            p = doc.add_paragraph(p_line)
            p.paragraph_format.line_spacing = 1.2
            for run in p.runs:
                run.font.name = "Times New Roman"
                run.font.size = Pt(13)

        p_sign = doc.add_paragraph("\n......, ngày ..... tháng ..... năm 20.....\nNGƯỜI LÀM ĐƠN\n(Ký và ghi rõ họ tên)\n\n\n\n")
        p_sign.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        buf = io.BytesIO()
        doc.save(buf)
        buf.seek(0)
        return buf

    # 3. ĐƠN KHIẾU NẠI / TỐ CÁO BẠO LỰC HỌC ĐƯỜNG
    def draft_school_violence_complaint(self, data: Dict[str, Any]) -> io.BytesIO:
        doc = Document()
        _setup_docx_page_and_header(doc, "ĐƠN YÊU CẦU GIẢI QUYẾT VỤ VIỆC BẠO LỰC HỌC ĐƯỜNG & YÊU CẦU BỒI THƯỜNG THIỆT HẠI")

        school_name = _val_or_placeholder(data.get("school_name"), "Trường .....................................................................")
        dept_name = _val_or_placeholder(data.get("education_department"), "Phòng / Sở Giáo dục và Đào tạo ..........................................")
        police_name = _val_or_placeholder(data.get("police_station"), "Công an xã/phường ...........................................................")

        p_kinh_gui = doc.add_paragraph()
        p_kinh_gui.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_kg = p_kinh_gui.add_run(f"Kính gửi: \n- Ban Giám hiệu {school_name}\n- {dept_name}\n- {police_name}\n")
        r_kg.bold = True
        r_kg.font.name = "Times New Roman"
        r_kg.font.size = Pt(12)

        parent = _val_or_placeholder(data.get("parent_name"), "....................................................................................")
        parent_cccd = _val_or_placeholder(data.get("parent_cccd"), "........................................................")
        parent_phone = _val_or_placeholder(data.get("parent_phone"), "........................................")
        student = _val_or_placeholder(data.get("student_name"), "....................................................................................")
        student_class = _val_or_placeholder(data.get("student_class"), "Lớp ........... niên khóa ....................")

        incident_time = _val_or_placeholder(data.get("incident_time"), "vào khoảng ..... giờ ..... ngày ...../...../20.....")
        incident_place = _val_or_placeholder(data.get("incident_place"), "tại khuôn viên / lớp học Trường ...................................")
        injury_desc = _val_or_placeholder(data.get("injury_desc"), "thương tích vùng mặt/đầu/thân thể, sang chấn tâm lý, phải điều trị y tế tại bệnh viện...")
        medical_cost = _val_or_placeholder(data.get("medical_cost"), "................................................ VNĐ")

        body_text = (
            f"I. THÔNG TIN NGƯỜI ĐỨNG ĐƠN:\n"
            f"Tôi là: {parent}, CCCD số: {parent_cccd}, SĐT: {parent_phone}.\n"
            f"Là cha/mẹ (người đại diện theo pháp luật) của cháu: {student}, học sinh {student_class} tại {school_name}.\n\n"
            f"II. NỘI DUNG VỤ VIỆC BẠO LỰC:\n"
            f"- Vào thời điểm: {incident_time}, {incident_place}, con tôi trong giờ học / giờ ra chơi thuộc thời gian nhà trường trực tiếp quản lý đã bị các bạn học sinh khác có hành vi hành hung, bạo lực nghiêm trọng.\n"
            f"- Hậu quả xảy ra: Cháu bị tổn hại sức khỏe: {injury_desc}.\n"
            f"- Tuy nhiên, sau khi sự việc xảy ra, nhà trường có biểu hiện né tránh, đùn đẩy trách nhiệm và chưa có biện pháp xử lý thỏa đáng nhằm bảo vệ học sinh bị bạo lực.\n\n"
            f"III. CĂN CỨ PHÁP LUẬT VỀ TRÁCH NHIỆM CỦA NHÀ TRƯỜNG:\n"
            f"- Khoản 1 Điều 599 Bộ luật Dân sự 2015 quy định rõ: Người dưới mười lăm tuổi trong thời gian trường học trực tiếp quản lý mà gây thiệt hại thì TRƯỜNG HỌC PHẢI BỒI THƯỜNG THIỆT HẠI PHÁT SINH.\n"
            f"- Điều 584 và Điều 590 Bộ luật Dân sự 2015 quy định về bồi thường chi phí cứu chữa, phục hồi sức khỏe và bù đắp tổn thất tinh thần do sức khỏe bị xâm phạm.\n"
            f"- Nghị định số 80/2017/NĐ-CP của Chính phủ về bảo đảm môi trường giáo dục an toàn, phòng chống bạo lực học đường.\n\n"
            f"IV. YÊU CẦU ĐỀ NGHỊ GIẢI QUYẾT:\n"
            f"1. Yêu cầu Ban Giám hiệu nhà trường lập biên bản vụ việc, trích xuất hình ảnh camera an ninh tại thời điểm xảy ra sự việc.\n"
            f"2. Yêu cầu nhà trường và gia đình học sinh vi phạm bồi thường toàn bộ chi phí khám chữa bệnh, viện phí thực tế: {medical_cost} và bồi thường tổn thất tinh thần cho cháu.\n"
            f"3. Có biện pháp kỷ luật, răn đe các học sinh có hành vi bạo lực và bảo đảm tuyệt đối môi trường an toàn để con tôi tiếp tục đến trường."
        )

        for p_line in body_text.split("\n\n"):
            p = doc.add_paragraph(p_line)
            p.paragraph_format.line_spacing = 1.2
            for run in p.runs:
                run.font.name = "Times New Roman"
                run.font.size = Pt(13)

        p_sign = doc.add_paragraph("\n......, ngày ..... tháng ..... năm 20.....\nNGƯỜI ĐỨNG ĐƠN\n(Ký và ghi rõ họ tên)\n\n\n\n")
        p_sign.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        buf = io.BytesIO()
        doc.save(buf)
        buf.seek(0)
        return buf

    # 4. ĐƠN THUẬN TÌNH LY HÔN & PHÂN CHIA QUYỀN NUÔI CON
    def draft_divorce_petition(self, data: Dict[str, Any]) -> io.BytesIO:
        doc = Document()
        _setup_docx_page_and_header(doc, "ĐƠN YÊU CẦU CÔNG NHẬN THUẬN TÌNH LY HÔN, THỎA THUẬN NUÔI CON VÀ CHIA TÀI SẢN")

        court = _val_or_placeholder(data.get("court_name"), "Tòa án nhân dân quận/huyện .....................................................")
        p_kinh_gui = doc.add_paragraph()
        p_kinh_gui.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_kg = p_kinh_gui.add_run(f"Kính gửi: {court}\n")
        r_kg.bold = True
        r_kg.font.name = "Times New Roman"
        r_kg.font.size = Pt(13)

        husband = _val_or_placeholder(data.get("husband_name"), "....................................................................................")
        h_cccd = _val_or_placeholder(data.get("husband_cccd"), "........................................................")
        h_addr = _val_or_placeholder(data.get("husband_address"), "....................................................................................")

        wife = _val_or_placeholder(data.get("wife_name"), "....................................................................................")
        w_cccd = _val_or_placeholder(data.get("wife_cccd"), "........................................................")
        w_addr = _val_or_placeholder(data.get("wife_address"), "....................................................................................")

        m_date = _val_or_placeholder(data.get("marriage_date"), "ngày ...../...../20..... tại UBND ....................................................")
        custody = _val_or_placeholder(data.get("custody_agreement"), "Thỏa thuận giao con chung là cháu ........................ (sinh ngày ...../...../.........) cho Người mẹ / Người cha trực tiếp nuôi dưỡng; Bên còn lại có nghĩa vụ cấp dưỡng ........................ VNĐ/tháng.")
        property_div = _val_or_placeholder(data.get("property_division"), "Hai bên tự thỏa thuận phân chia hoặc không yêu cầu Tòa án giải quyết.")
        debts = _val_or_placeholder(data.get("debt_division"), "Hai bên cam kết không có nợ chung và không yêu cầu Tòa án giải quyết.")

        body_text = (
            f"I. THÔNG TIN NGƯỜI YÊU CẦU:\n"
            f"1. Người chồng: Ông {husband} - CCCD: {h_cccd}\n"
            f"   Địa chỉ: {h_addr}\n"
            f"2. Người vợ: Bà {wife} - CCCD: {w_cccd}\n"
            f"   Địa chỉ: {w_addr}\n\n"
            f"II. TÌNH TRẠNG HÔN NHÂN:\n"
            f"- Hai chúng tôi tự nguyện kết hôn và đã đăng ký kết hôn vào {m_date}.\n"
            f"- Trong quá trình chung sống, do bất đồng quan điểm sống và tính tình không hòa hợp dẫn đến mục đích hôn nhân không đạt được, đời sống chung không thể kéo dài. Nay hai chúng tôi cùng tự nguyện làm đơn này yêu cầu Tòa án công nhận thuận tình ly hôn theo Điều 55 Luật Hôn nhân và Gia đình 2014.\n\n"
            f"III. THỎA THUẬN VỀ CON CHUNG VÀ NGHĨA VỤ CẤP DƯỠNG (Điều 81, 82 Luật HNGĐ 2014):\n"
            f"- {custody}\n\n"
            f"IV. THỎA THUẬN VỀ TÀI SẢN CHUNG VÀ NỢ CHUNG (Điều 59 Luật HNGĐ 2014):\n"
            f"- Về tài sản chung: {property_div}\n"
            f"- Về nợ chung: {debts}\n\n"
            f"Kính mong Quý Tòa xem xét, thụ lý giải quyết theo quy định pháp luật."
        )

        for p_line in body_text.split("\n\n"):
            p = doc.add_paragraph(p_line)
            p.paragraph_format.line_spacing = 1.2
            for run in p.runs:
                run.font.name = "Times New Roman"
                run.font.size = Pt(13)

        table = doc.add_table(rows=1, cols=2)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        c1, c2 = table.rows[0].cells
        c1.text = "NGƯỜI CHỒNG\n(Ký và ghi rõ họ tên)\n\n\n\n"
        c2.text = "NGƯỜI VỢ\n(Ký và ghi rõ họ tên)\n\n\n\n"
        c1.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        c2.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

        buf = io.BytesIO()
        doc.save(buf)
        buf.seek(0)
        return buf

    # 5. HỢP ĐỒNG DỊCH VỤ SONG PHƯƠNG CÂN BẰNG
    def draft_service_contract(self, data: Dict[str, Any]) -> io.BytesIO:
        doc = Document()
        _setup_docx_page_and_header(doc, "HỢP ĐỒNG CUNG ỨNG DỊCH VỤ THƯƠNG MẠI")

        p_a = _val_or_placeholder(data.get("party_a_name"), "CÔNG TY / ÔNG BÀ ................................................................")
        p_a_rep = _val_or_placeholder(data.get("party_a_representative"), "Ông/Bà .................................... - Chức vụ: ....................................")
        p_a_addr = _val_or_placeholder(data.get("party_a_address"), "....................................................................................")

        p_b = _val_or_placeholder(data.get("party_b_name"), "CÔNG TY / ÔNG BÀ ................................................................")
        p_b_rep = _val_or_placeholder(data.get("party_b_representative"), "Ông/Bà .................................... - Chức vụ: ....................................")
        p_b_addr = _val_or_placeholder(data.get("party_b_address"), "....................................................................................")

        scope = _val_or_placeholder(data.get("service_scope"), "Cung ứng dịch vụ theo yêu cầu kỹ thuật và tiến độ thỏa thuận tại Phụ lục.")
        price = _val_or_placeholder(data.get("contract_value"), "................................................ VNĐ")

        body_text = (
            f"- Căn cứ Bộ luật Dân sự 2015;\n"
            f"- Căn cứ Luật Thương mại 2005;\n"
            f"- Căn cứ nhu cầu và khả năng của hai bên;\n\n"
            f"BÊN A (Bên Thuê Dịch Vụ): {p_a}\n"
            f"- Đại diện: {p_a_rep} - Địa chỉ: {p_a_addr}\n\n"
            f"BÊN B (Bên Cung Ứng Dịch Vụ): {p_b}\n"
            f"- Đại diện: {p_b_rep} - Địa chỉ: {p_b_addr}\n\n"
            f"Hai bên đồng ý ký kết hợp đồng với các điều khoản cân bằng và bình đẳng sau:\n\n"
            f"Điều 1: Nội dung và Phạm vi Dịch vụ\n"
            f"Bên B cung ứng cho Bên A dịch vụ: {scope}.\n\n"
            f"Điều 2: Giá trị Hợp đồng và Phương thức Thanh toán\n"
            f"Tổng giá trị hợp đồng là: {price}. Thanh toán theo tiến độ nghiệm thu qua tài khoản ngân hàng.\n\n"
            f"Điều 3: Phạt vi phạm và Bồi thường thiệt hại (Chuẩn mực Điều 301 Luật Thương mại)\n"
            f"Bên vi phạm chịu mức phạt vi phạm tối đa 8% giá trị phần nghĩa vụ bị vi phạm và bồi thường thiệt hại thực tế phát sinh trực tiếp.\n\n"
            f"Điều 4: Sự kiện Bất khả kháng (Force Majeure - Điều 156, 351 BLDS 2015)\n"
            f"Sự kiện khách quan (thiên tai, dịch bệnh, quyết định của cơ quan nhà nước) khiến một bên không thể thực hiện nghĩa vụ được miễn trách nhiệm bồi thường nếu thông báo bằng văn bản kịp thời trong 03 ngày làm việc.\n\n"
            f"Điều 5: Cơ quan Giải quyết Tranh chấp\n"
            f"Mọi tranh chấp trước hết thương lượng giải quyết trong 30 ngày. Nếu không thành, vụ việc được đưa ra Tòa án nhân dân có thẩm quyền để phân xử."
        )

        for p_line in body_text.split("\n\n"):
            p = doc.add_paragraph(p_line)
            p.paragraph_format.line_spacing = 1.2
            for run in p.runs:
                run.font.name = "Times New Roman"
                run.font.size = Pt(13)

        table = doc.add_table(rows=1, cols=2)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        c1, c2 = table.rows[0].cells
        c1.text = "ĐẠI DIỆN BÊN A\n(Ký và đóng dấu)\n\n\n\n"
        c2.text = "ĐẠI DIỆN BÊN B\n(Ký và đóng dấu)\n\n\n\n"
        c1.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        c2.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

        buf = io.BytesIO()
        doc.save(buf)
        buf.seek(0)
        return buf

    # 6. SOẠN THẢO VĂN BẢN TÙY CHỌN BẤT KỲ QUA LLM (ON-DEMAND ARBITRARY DRAFTING)
    def draft_custom_document(self, user_prompt: str, personal_info: Dict[str, Any] = None) -> io.BytesIO:
        personal_info = personal_info or {}
        prompt = (
            f"Bạn là Chuyên viên Pháp lý Soạn thảo Văn bản (Senior Legal Drafter). "
            f"Hãy soạn thảo toàn bộ văn bản pháp lý hoàn chỉnh theo yêu cầu sau:\n"
            f"\"\"\"{user_prompt}\"\"\"\n\n"
            f"QUY CHUẨN SOẠN THẢO:\n"
            f"1. Văn bản phải tuân theo thể thức hành chính Việt Nam (Quốc hiệu, Tiêu ngữ, Tên loại đơn/văn bản, Căn cứ pháp luật, Nội dung vụ việc, Đề nghị giải quyết, Chữ ký).\n"
            f"2. ĐIỀN SẴN 100% CÁC CĂN CỨ PHÁP LUẬT VÀ NỘI DUNG MẪU.\n"
            f"3. Các thông tin nhân thân nếu chưa có hãy dùng dòng kẻ giữ chỗ dạng '........................................................' hoặc '[HỌ VÀ TÊN]' để người dùng có thể tải về điền tay."
        )

        try:
            content = self.factory.generate(
                prompt=prompt,
                system_prompt="Bạn là Luật sư Soạn thảo văn bản chuyên nghiệp. Chỉ xuất văn bản pháp lý hoàn chỉnh, trang trọng, không viết lời phi lộ."
            )
        except Exception:
            content = f"VĂN BẢN PHÁP LÝ THEO YÊU CẦU\n\nCộng hòa Xã hội Chủ nghĩa Việt Nam\nĐộc lập - Tự do - Hạnh phúc\n\nNội dung: {user_prompt}\n..."

        doc = Document()
        for section in doc.sections:
            section.top_margin = Inches(0.8)
            section.bottom_margin = Inches(0.8)
            section.left_margin = Inches(1.0)
            section.right_margin = Inches(0.8)

        for line in content.split("\n"):
            p = doc.add_paragraph(line)
            p.paragraph_format.line_spacing = 1.2
            for run in p.runs:
                run.font.name = "Times New Roman"
                run.font.size = Pt(13)

        buf = io.BytesIO()
        doc.save(buf)
        buf.seek(0)
        return buf
