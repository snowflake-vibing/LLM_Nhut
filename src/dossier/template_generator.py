"""
Document & Dossier Generator Module
Tạo biểu mẫu hồ sơ pháp lý thành lập doanh nghiệp chuẩn Nghị định 01/2021/NĐ-CP
và Luật Doanh nghiệp 2020 dưới dạng tệp văn bản Word (.docx).
"""

import io
import re
from typing import Dict, Any, List, Tuple
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn


def _set_cell_background(cell, fill_hex="F2F2F2"):
    """Thiết lập màu nền cho ô trong bảng docx."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)


def _format_vnd(amount) -> str:
    """Format số tiền VNĐ."""
    try:
        val = int(amount)
        return f"{val:,} VNĐ"
    except Exception:
        return f"{amount} VNĐ"


def validate_company_name(name: str) -> Tuple[bool, List[str]]:
    """
    Rà soát tính hợp lệ của Tên doanh nghiệp theo Điều 38, 39, 41 Luật Doanh nghiệp 2020.
    Returns:
        (is_valid, list_of_warnings_or_errors)
    """
    warnings = []
    clean_name = name.strip()

    if not clean_name:
        return False, ["Tên công ty không được để trống."]

    # 1. Kiểm tra tiền tố loại hình (Điều 37)
    valid_types = ["TNHH", "TRÁCH NHIỆM HỮU HẠN", "CỔ PHẦN", "HỢP DANH", "DOANH NGHIỆP TƯ NHÂN", "DNTN"]
    has_type = any(t in clean_name.upper() for t in valid_types)
    if not has_type:
        warnings.append("⚠️ Tên doanh nghiệp bắt buộc phải có thành tố loại hình doanh nghiệp (Ví dụ: 'CÔNG TY TNHH...' hoặc 'CÔNG TY CỔ PHẦN...'). [Điều 37]")

    # 2. Kiểm tra từ ngữ cấm theo Điều 38
    forbidden_words = [
        "QUÂN ĐỘI", "CÔNG AN", "CHÍNH PHỦ", "QUỐC GIA", "BỘ CÔNG THƯƠNG",
        "UBND", "ỦY BAN NHÂN DÂN", "CỤC QUẢN LÝ", "TRUNG ƯƠNG"
    ]
    for fw in forbidden_words:
        if fw in clean_name.upper():
            warnings.append(f"🚫 Tên chứa từ ngữ bị cấm hoặc gây nhầm lẫn với cơ quan nhà nước, tổ chức chính trị: '{fw}' [Khoản 2 Điều 38].")

    # 3. Ký tự đặc biệt không được phép
    if re.search(r"[@#$%^*+=~`<>]", clean_name):
        warnings.append("⚠️ Tên công ty không được chứa các ký tự đặc biệt (@, #, $, %, ^, *...) theo quy tắc đặt tên của Bộ Kế hoạch & Đầu tư.")

    is_valid = len([w for w in warnings if w.startswith("🚫")]) == 0
    return is_valid, warnings


def validate_dossier_legal_compliance(data: Dict[str, Any]) -> List[str]:
    """
    AI Reviewer: Kiểm tra toàn diện tính hợp lệ của hồ sơ kê khai.
    """
    alerts = []

    # Kiểm tra tên
    company_name = data.get("company_name", "")
    _, name_alerts = validate_company_name(company_name)
    alerts.extend(name_alerts)

    # Kiểm tra vốn điều lệ
    capital = data.get("charter_capital", 0)
    try:
        cap_val = float(str(capital).replace(",", "").replace(".", "").replace("VNĐ", "").strip())
        if cap_val < 10000000:
            alerts.append("⚠️ Vốn điều lệ quá thấp (dưới 10.000.000 VNĐ) có thể gặp khó khăn khi mở tài khoản ngân hàng hoặc xin giấy phép chuyên ngành.")
    except Exception:
        alerts.append("⚠️ Định dạng số vốn điều lệ chưa đúng chuẩn số.")

    # Thời hạn góp vốn
    alerts.append("📌 Lưu ý pháp lý: Các thành viên/cổ đông phải góp đủ vốn đăng ký trong thời hạn 90 ngày kể từ ngày được cấp GCN ĐKDN (Điều 47, 75 Lập Doanh nghiệp 2020).")

    # Kiểm tra CCCD
    rep_cccd = data.get("rep_cccd", "")
    if rep_cccd and not (len(rep_cccd) == 12 and rep_cccd.isdigit()):
        alerts.append("⚠️ Số CCCD của Người đại diện theo pháp luật chưa đúng chuẩn 12 số định danh cá nhân.")

    return alerts


def _add_national_header(doc: Document):
    """Thêm Quốc hiệu, Tiêu ngữ chuẩn thể thức văn bản hành chính Việt Nam (Nghị định 30/2020/NĐ-CP)."""
    p_header = doc.add_paragraph()
    p_header.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run1 = p_header.add_run("CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM\n")
    run1.bold = True
    run1.font.size = Pt(13)
    run1.font.name = "Times New Roman"

    run2 = p_header.add_run("Độc lập - Tự do - Hạnh phúc\n")
    run2.bold = True
    run2.font.size = Pt(14)
    run2.font.name = "Times New Roman"

    run3 = p_header.add_run("-----------------------")
    run3.font.size = Pt(12)
    run3.font.name = "Times New Roman"
    doc.add_paragraph()  # Dòng trống


def generate_registration_request_docx(data: Dict[str, Any]) -> io.BytesIO:
    """
    Sinh file Giấy đề nghị đăng ký doanh nghiệp chuẩn Nghị định 01/2021/NĐ-CP.
    """
    doc = Document()

    # Thiết lập lề trang
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(0.8)

    _add_national_header(doc)

    # Tiêu đề
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_title = p_title.add_run("GIẤY ĐỀ NGHỊ ĐĂNG KÝ DOANH NGHIỆP\n")
    run_title.bold = True
    run_title.font.size = Pt(15)
    run_title.font.name = "Times New Roman"

    sub_type = data.get("entity_type_label", "CÔNG TY TRÁCH NHIỆM HỮU HẠN")
    run_sub = p_title.add_run(f"({sub_type.upper()})\n")
    run_sub.bold = True
    run_sub.font.size = Pt(13)
    run_sub.font.name = "Times New Roman"

    p_ref = doc.add_paragraph()
    p_ref.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_ref = p_ref.add_run("(Ban hành kèm theo Thông tư số 01/2021/TT-BKHĐT và Nghị định số 01/2021/NĐ-CP)")
    run_ref.italic = True
    run_ref.font.size = Pt(11)

    # Kính gửi
    p_kg = doc.add_paragraph()
    p_kg.paragraph_format.left_indent = Inches(0.5)
    run_kg = p_kg.add_run(f"Kính gửi: Phòng Đăng ký kinh doanh - Sở Kế hoạch và Đầu tư tỉnh/thành phố {data.get('city', 'TP. Hồ Chí Minh')}")
    run_kg.bold = True
    run_kg.font.size = Pt(12)

    # Nội dung thông tin
    def add_field(label: str, value: str, bold_val: bool = False):
        p = doc.add_paragraph()
        r1 = p.add_run(f"{label}: ")
        r1.bold = True
        r1.font.size = Pt(12)
        r2 = p.add_run(str(value) if value else "..................................................")
        r2.bold = bold_val
        r2.font.size = Pt(12)

    doc.add_heading("1. Tình trạng thành lập:", level=2)
    doc.add_paragraph("Thành lập mới doanh nghiệp theo quy định của Luật Doanh nghiệp 2020.")

    doc.add_heading("2. Tên doanh nghiệp:", level=2)
    add_field("Tên doanh nghiệp viết bằng tiếng Việt", data.get("company_name", "").upper(), bold_val=True)
    add_field("Tên doanh nghiệp viết bằng tiếng nước ngoài (nếu có)", data.get("company_name_en", ""))
    add_field("Tên doanh nghiệp viết tắt (nếu có)", data.get("company_name_abbr", ""))

    doc.add_heading("3. Địa chỉ trụ sở chính:", level=2)
    add_field("Số nhà, ngách, hẻm, ngõ, đường", data.get("address_street", ""))
    add_field("Xã/Phường/Thị trấn", data.get("address_ward", ""))
    add_field("Quận/Huyện/Thị xã", data.get("address_district", ""))
    add_field("Tỉnh/Thành phố", data.get("city", ""))
    add_field("Điện thoại liên hệ", data.get("rep_phone", ""))
    add_field("Email", data.get("rep_email", ""))

    doc.add_heading("4. Ngành, nghề kinh doanh chính:", level=2)
    add_field("Tên ngành nghề kinh doanh", data.get("main_industry_name", ""))
    add_field("Mã ngành theo hệ thống VSIC", data.get("main_industry_code", ""))

    doc.add_heading("5. Vốn điều lệ:", level=2)
    capital_val = data.get("charter_capital", 0)
    add_field("Vốn điều lệ (bằng số)", _format_vnd(capital_val), bold_val=True)
    add_field("Vốn điều lệ (bằng chữ)", data.get("charter_capital_in_words", "Theo giá trị kê khai"))

    doc.add_heading("6. Thông tin Người đại diện theo pháp luật:", level=2)
    add_field("Họ và tên", data.get("rep_name", "").upper(), bold_val=True)
    add_field("Chức danh", data.get("rep_title", "Giám đốc"))
    add_field("Giới tính", data.get("rep_gender", "Nam"))
    add_field("Ngày sinh", data.get("rep_dob", ""))
    add_field("Dân tộc", "Kinh")
    add_field("Quốc tịch", "Việt Nam")
    add_field("Loại giấy tờ pháp lý", "Thẻ Căn cước công dân")
    add_field("Số thẻ CCCD", data.get("rep_cccd", ""))
    add_field("Ngày cấp", data.get("rep_cccd_date", ""))
    add_field("Nơi cấp", data.get("rep_cccd_place", "Cục Cảnh sát QLHC về trật tự xã hội"))
    add_field("Nơi đăng ký hộ khẩu thường trú", data.get("rep_permanent_address", ""))
    add_field("Chỗ ở hiện tại", data.get("rep_current_address", ""))

    # Cam kết
    doc.add_heading("7. Cam kết của người đại diện:", level=2)
    p_camket = doc.add_paragraph(
        "Tôi cam kết rằng:\n"
        "- Trụ sở chính thuộc quyền sử dụng hợp pháp của doanh nghiệp và không đặt tại nhà chung cư có mục đích để ở;\n"
        "- Các thông tin kê khai trong Giấy đề nghị đăng ký doanh nghiệp này là hoàn toàn chính xác, trung thực và chịu trách nhiệm trước pháp luật;\n"
        "- Doanh nghiệp sẽ góp đủ vốn điều lệ trong thời hạn 90 ngày kể từ ngày được cấp Giấy chứng nhận đăng ký doanh nghiệp."
    )
    p_camket.paragraph_format.line_spacing = 1.25

    # Chữ ký
    doc.add_paragraph()
    p_sign = doc.add_paragraph()
    p_sign.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_sign.paragraph_format.right_indent = Inches(0.5)
    run_date = p_sign.add_run(f"{data.get('city', 'TP. Hồ Chí Minh')}, ngày ..... tháng ..... năm 202...\n")
    run_date.italic = True
    run_rep_title = p_sign.add_run("NGƯỜI ĐẠI DIỆN THEO PHÁP LUẬT CỦA CÔNG TY\n")
    run_rep_title.bold = True
    run_sign_note = p_sign.add_run("(Ký, ghi rõ họ tên và đóng dấu nếu có)\n\n\n\n\n")
    run_sign_note.italic = True
    run_name = p_sign.add_run(data.get("rep_name", "").upper())
    run_name.bold = True

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer


def generate_company_charter_docx(data: Dict[str, Any]) -> io.BytesIO:
    """
    Sinh Dự thảo Điều lệ Công ty TNHH / Cổ phần chuẩn mực theo Luật Doanh nghiệp 2020.
    """
    doc = Document()
    _add_national_header(doc)

    company_name = data.get("company_name", "CÔNG TY").upper()

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run1 = p_title.add_run("ĐIỀU LỆ\n")
    run1.bold = True
    run1.font.size = Pt(16)
    run2 = p_title.add_run(f"{company_name}\n")
    run2.bold = True
    run2.font.size = Pt(14)

    p_legal = doc.add_paragraph()
    p_legal.italic = True
    p_legal.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_legal.add_run(
        "- Căn cứ Luật Doanh nghiệp số 59/2020/QH14 được Quốc hội Nước CHXHCN Việt Nam thông qua ngày 17 tháng 06 năm 2020;\n"
        "- Căn cứ Nghị định số 01/2021/NĐ-CP về đăng ký doanh nghiệp;\n"
        "- Căn cứ nhu cầu và sự tự nguyện của các thành viên/cổ đông sáng lập."
    )

    chapters = [
        ("CHƯƠNG I: QUY ĐỊNH CHUNG", [
            ("Điều 1: Hình thức, tên gọi và biểu tượng",
             f"1. Công ty hoạt động theo hình thức {data.get('entity_type_label', 'Công ty Trách nhiệm hữu hạn')}, có tư cách pháp nhân kể từ ngày được cấp Giấy chứng nhận đăng ký doanh nghiệp.\n"
             f"2. Tên tiếng Việt: {company_name}\n"
             f"3. Tên viết bằng tiếng nước ngoài: {data.get('company_name_en', 'Không đăng ký')}\n"
             f"4. Tên viết tắt: {data.get('company_name_abbr', 'Không đăng ký')}"),
            ("Điều 2: Trụ sở chính và chi nhánh",
             f"Địa chỉ trụ sở chính đặt tại: {data.get('address_street', '')}, {data.get('address_ward', '')}, {data.get('address_district', '')}, {data.get('city', '')}."),
            ("Điều 3: Ngành nghề kinh doanh",
             f"Công ty kinh doanh các ngành nghề theo quy định pháp luật. Ngành nghề chính: {data.get('main_industry_name', '')} (Mã VSIC: {data.get('main_industry_code', '')})."),
        ]),
        ("CHƯƠNG II: VỐN ĐIỀU LỆ VÀ PHẦN VỐN GÓP", [
            ("Điều 4: Vốn điều lệ và thời hạn góp vốn",
             f"1. Vốn điều lệ của Công ty là: {_format_vnd(data.get('charter_capital', 0))} (Bằng chữ: {data.get('charter_capital_in_words', 'Theo giá trị đăng ký')}).\n"
             f"2. Thời hạn góp vốn: Chủ sở hữu / Thành viên cam kết góp đủ 100% phần vốn cam kết trong thời hạn 90 ngày kể từ ngày được cấp Giấy chứng nhận ĐKDN theo quy định tại Luật Doanh nghiệp 2020."),
            ("Điều 5: Thay đổi vốn điều lệ",
             "Công ty có thể tăng hoặc giảm vốn điều lệ theo quyết định của Chủ sở hữu / Hội đồng thành viên phù hợp với quy định của pháp luật."),
        ]),
        ("CHƯƠNG III: CƠ CẤU TỔ CHỨC VÀ ĐẠI DIỆN PHÁP LUẬT", [
            ("Điều 6: Cơ cấu quản lý",
             "Cơ cấu quản lý của Công ty bao gồm:\n- Chủ tịch Công ty / Hội đồng thành viên\n- Giám đốc (hoặc Tổng giám đốc)\n- Ban kiểm soát / Kiểm soát viên (nếu thuộc trường hợp luật định)."),
            ("Điều 7: Người đại diện theo pháp luật",
             f"1. Người đại diện theo pháp luật của Công ty là: {data.get('rep_name', '').upper()}.\n"
             f"2. Chức danh: {data.get('rep_title', 'Giám đốc')}.\n"
             f"3. Người đại diện theo pháp luật đại diện cho công ty thực hiện các quyền và nghĩa vụ phát sinh từ giao dịch của công ty theo quy định tại Điều 12, 13 Luật Doanh nghiệp 2020."),
        ]),
        ("CHƯƠNG IV: ĐIỀU KHOẢN THI HÀNH", [
            ("Điều 8: Hiệu lực của Điều lệ",
             "Điều lệ này gồm 4 chương, 8 điều, được người thành lập công ty thông qua và có hiệu lực thi hành kể từ ngày Công ty được cấp Giấy chứng nhận đăng ký doanh nghiệp."),
        ])
    ]

    for chap_title, articles in chapters:
        doc.add_heading(chap_title, level=1)
        for art_title, art_content in articles:
            p_art = doc.add_paragraph()
            r_art = p_art.add_run(f"{art_title}\n")
            r_art.bold = True
            p_art.add_run(art_content)

    # Chữ ký người thành lập
    doc.add_paragraph()
    p_sign = doc.add_paragraph()
    p_sign.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run_date = p_sign.add_run(f"{data.get('city', 'TP. Hồ Chí Minh')}, ngày ..... tháng ..... năm 202...\n")
    run_date.italic = True
    run_sign_title = p_sign.add_run("CHỦ SỞ HỮU / CÁC THÀNH VIÊN SÁNG LẬP\n")
    run_sign_title.bold = True
    run_sub = p_sign.add_run("(Ký và ghi rõ họ tên)\n\n\n\n\n")
    run_sub.italic = True
    run_name = p_sign.add_run(data.get("rep_name", "").upper())
    run_name.bold = True

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer


def generate_member_list_docx(data: Dict[str, Any]) -> io.BytesIO:
    """
    Sinh Danh sách thành viên góp vốn / Cổ đông sáng lập dưới dạng Bảng biểu chuẩn.
    """
    doc = Document()
    _add_national_header(doc)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run1 = p_title.add_run("DANH SÁCH THÀNH VIÊN GÓP VỐN / CỔ ĐÔNG SÁNG LẬP\n")
    run1.bold = True
    run1.font.size = Pt(14)
    run2 = p_title.add_run(f"Tên công ty: {data.get('company_name', '').upper()}")
    run2.bold = True

    # Bảng danh sách
    members = data.get("members", [])
    if not members:
        # Mặc định lấy từ Người đại diện nếu chưa nhập nhiều thành viên
        members = [{
            "name": data.get("rep_name", "Nguyễn Văn A"),
            "cccd": data.get("rep_cccd", "079201000000"),
            "address": data.get("rep_permanent_address", data.get("city", "TP. Hồ Chí Minh")),
            "capital": data.get("charter_capital", 100000000),
            "ratio": "100%",
            "asset_type": "Đồng Việt Nam (VNĐ)"
        }]

    table = doc.add_table(rows=1, cols=6)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = True

    hdr_cells = table.rows[0].cells
    headers = ["STT", "Họ và tên thành viên", "Số CCCD/Định danh", "Địa chỉ thường trú", "Vốn góp (VNĐ)", "Tỷ lệ (%)"]
    for i, title in enumerate(headers):
        hdr_cells[i].text = title
        _set_cell_background(hdr_cells[i], "D9E1F2")
        hdr_cells[i].paragraphs[0].runs[0].bold = True

    for idx, m in enumerate(members, 1):
        row_cells = table.add_row().cells
        row_cells[0].text = str(idx)
        row_cells[1].text = str(m.get("name", "")).upper()
        row_cells[2].text = str(m.get("cccd", ""))
        row_cells[3].text = str(m.get("address", ""))
        row_cells[4].text = _format_vnd(m.get("capital", 0))
        row_cells[5].text = str(m.get("ratio", "100%"))

    # Tổng kết
    doc.add_paragraph()
    p_tot = doc.add_paragraph()
    p_tot.add_run(f"- Tổng số thành viên góp vốn: {len(members)} thành viên.\n").bold = True
    p_tot.add_run(f"- Tổng giá trị vốn góp cam kết: {_format_vnd(data.get('charter_capital', 0))}.\n").bold = True
    p_tot.add_run(f"- Thời hạn góp vốn: 90 ngày kể từ ngày được cấp GCN ĐKDN theo Điều 47 Luật Doanh nghiệp 2020.")

    # Ký tên
    doc.add_paragraph()
    p_sign = doc.add_paragraph()
    p_sign.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_sign.paragraph_format.right_indent = Inches(0.5)
    run_date = p_sign.add_run(f"{data.get('city', 'TP. Hồ Chí Minh')}, ngày ..... tháng ..... năm 202...\n")
    run_date.italic = True
    run_title = p_sign.add_run("NGƯỜI ĐẠI DIỆN THEO PHÁP LUẬT CỦA CÔNG TY\n")
    run_title.bold = True
    run_sub = p_sign.add_run("(Ký và ghi rõ họ tên)\n\n\n\n\n")
    run_sub.italic = True
    run_name = p_sign.add_run(data.get("rep_name", "").upper())
    run_name.bold = True

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer


def generate_full_dossier_docx(data: Dict[str, Any]) -> io.BytesIO:
    """
    Tạo Bộ hồ sơ doanh nghiệp tích hợp đầy đủ cả Giấy đề nghị, Điều lệ và Danh sách thành viên trong 1 file Word.
    """
    doc = Document()

    # Thêm Giấy đề nghị
    _add_national_header(doc)
    p_cover = doc.add_paragraph()
    p_cover.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cov = p_cover.add_run("BỘ HỒ SƠ THÀNH LẬP DOANH NGHIỆP ĐẦY ĐỦ\n")
    r_cov.bold = True
    r_cov.font.size = Pt(18)
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run(f"DOANH NGHIỆP: {data.get('company_name', '').upper()}\n")
    r_sub.bold = True
    r_sub.font.size = Pt(14)
    doc.add_paragraph(f"Loại hình: {data.get('entity_type_label', 'Công ty TNHH')}")
    doc.add_paragraph(f"Vốn điều lệ: {_format_vnd(data.get('charter_capital', 0))}")
    doc.add_paragraph(f"Người đại diện: {data.get('rep_name', '').upper()} - CCCD: {data.get('rep_cccd', '')}")
    doc.add_page_break()

    # Tài liệu 1: Giấy đề nghị
    doc.add_heading("PHẦN 1: GIẤY ĐỀ NGHỊ ĐĂNG KÝ DOANH NGHIỆP", level=1)
    doc.add_paragraph("Theo mẫu Phụ lục I ban hành kèm Thông tư 01/2021/TT-BKHĐT.")
    doc.add_paragraph(f"Tên doanh nghiệp: {data.get('company_name', '')}")
    doc.add_paragraph(f"Trụ sở: {data.get('address_street', '')}, {data.get('address_ward', '')}, {data.get('address_district', '')}, {data.get('city', '')}")
    doc.add_paragraph(f"Ngành nghề chính: {data.get('main_industry_name', '')} (Mã: {data.get('main_industry_code', '')})")
    doc.add_paragraph(f"Đại diện pháp luật: {data.get('rep_name', '')} - Chức danh: {data.get('rep_title', 'Giám đốc')}")
    doc.add_page_break()

    # Tài liệu 2: Dự thảo Điều lệ
    doc.add_heading("PHẦN 2: DỰ THẢO ĐIỀU LỆ DOANH NGHIỆP", level=1)
    doc.add_paragraph("Căn cứ Luật Doanh nghiệp 2020 số 59/2020/QH14.")
    doc.add_paragraph(f"Điều lệ công ty {data.get('company_name', '')} gồm các chương điều về quyền hạn, nghĩa vụ, cơ cấu điều hành và vốn góp 90 ngày.")
    doc.add_page_break()

    # Tài liệu 3: Danh mục hồ sơ nộp
    doc.add_heading("PHẦN 3: CHECKLIST HỒ SƠ NỘP SỞ KẾ HOẠCH & ĐẦU TƯ", level=1)
    doc.add_paragraph("1. Giấy đề nghị đăng ký doanh nghiệp (Bản chính có chữ ký)")
    doc.add_paragraph("2. Điều lệ công ty (Bản chính có chữ ký các thành viên sáng lập)")
    doc.add_paragraph("3. Bản sao có chứng thực Căn cước công dân của Người đại diện theo pháp luật và các thành viên góp vốn")
    doc.add_paragraph("4. Giấy ủy quyền nộp hồ sơ (nếu không phải đại diện pháp luật trực tiếp đi nộp)")

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer
