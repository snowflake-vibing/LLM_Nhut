"""
Database Initializer & Seed Script
Khởi tạo bảng và nạp dữ liệu mẫu Hệ thống ngành kinh tế Việt Nam (VSIC),
danh mục giấy phép con và quy trình thành lập doanh nghiệp.
"""

import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "database", "sme_legal.db")


def init_database():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Tạo bảng
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS industry_codes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        is_conditional BOOLEAN DEFAULT 0,
        regulatory_authority TEXT,
        license_required TEXT,
        description TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS license_requirements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        license_name TEXT NOT NULL,
        issuing_body TEXT NOT NULL,
        standard_duration_days INTEGER,
        estimated_fee INTEGER,
        legal_basis TEXT,
        required_dossier TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS registration_checklist (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        entity_type TEXT NOT NULL,
        step_number INTEGER NOT NULL,
        step_name TEXT NOT NULL,
        action_details TEXT NOT NULL,
        target_authority TEXT NOT NULL,
        output_document TEXT NOT NULL
    );
    """)

    # 2. Xóa dữ liệu cũ nếu có
    cursor.execute("DELETE FROM industry_codes")
    cursor.execute("DELETE FROM license_requirements")
    cursor.execute("DELETE FROM registration_checklist")

    # 3. Nạp dữ liệu Mã ngành kinh tế Việt Nam (VSIC 2018)
    industries = [
        ("5610", "Dịch vụ nhà hàng và các dịch vụ ăn uống phục vụ lưu động", 1, "Bộ Y tế / Chi cục ATVSTP", "Giấy chứng nhận cơ sở đủ điều kiện An toàn thực phẩm", "Kinh doanh quán ăn, nhà hàng, quán phở, buffet phục vụ tại chỗ"),
        ("5630", "Dịch vụ phục vụ đồ uống", 1, "Bộ Y tế / UBND Quận/Huyện", "Giấy chứng nhận An toàn thực phẩm (nếu chế biến tại chỗ)", "Kinh doanh quán cà phê, trà sữa, quán nước giải khát, quán bar"),
        ("6201", "Lập trình máy vi tính", 0, "Sở Thông tin và Truyền thông", "Không yêu cầu giấy phép con", "Viết phần mềm, ứng dụng di động, thiết kế website, lập trình hệ thống"),
        ("6202", "Tư vấn máy vi tính và quản trị hệ thống máy vi tính", 0, "Sở Thông tin và Truyền thông", "Không yêu cầu giấy phép con", "Tư vấn kiến trúc CNTT, bảo mật, quản trị mạng và hạ tầng đám mây"),
        ("6311", "Xử lý dữ liệu, cho thuê lưu trữ và các hoạt động liên quan", 0, "Bộ Thông tin và Truyền thông", "Không yêu cầu (trừ trung tâm dữ liệu chuyên dụng)", "Dịch vụ SaaS, Cloud Hosting, xử lý cơ sở dữ liệu và AI backend"),
        ("4791", "Bán lẻ theo hình thức đặt hàng qua bưu điện hoặc qua Internet", 1, "Bộ Công Thương", "Thông báo/Đăng ký website thương mại điện tử với Bộ Công Thương", "Bán hàng online qua website, sàn TMĐT Shopee/Lazada/TikTok Shop"),
        ("4711", "Bán lẻ lương thực, thực phẩm, đồ uống chiếm tỷ trọng lớn trong siêu thị, cửa hàng tiện lợi", 1, "Sở Công Thương / Chi cục ATVSTP", "Giấy phép ATVSTP, Giấy phép bán lẻ rượu/thuốc lá (nếu có)", "Cửa hàng tạp hóa, siêu thị mini, bách hóa tiện lợi"),
        ("4933", "Vận tải hàng hóa bằng đường bộ", 1, "Sở Giao thông Vận tải", "Giấy phép kinh doanh vận tải bằng xe ô tô, Phù hiệu xe", "Dịch vụ giao nhận vận chuyển hàng hóa, chuyển phát nhanh nội địa"),
        ("8559", "Giáo dục khác chưa được phân vào đâu", 1, "Sở Giáo dục và Đào tạo", "Giấy phép hoạt động trung tâm đào tạo ngắn hạn / ngoại ngữ / tin học", "Trung tâm dạy thêm, dạy kỹ năng mềm, đào tạo lập trình, ngoại ngữ"),
        ("9602", "Cắt tóc, làm đầu, gội đầu, dịch vụ chăm sóc sắc đẹp", 1, "UBND Quận/Huyện / Sở Y tế (nếu xâm lấn)", "Chứng chỉ hành nghề, Giấy phép hoạt động phòng khám chuyên khoa phẫu thuật thẩm mỹ (nếu có phẫu thuật)", "Tiệm làm tóc, spa chăm sóc da, nối mi, làm móng (nail)"),
        ("6820", "Tư vấn, môi giới, đấu giá bất động sản, đấu giá quyền sử dụng đất", 1, "Sở Xây dựng", "Chứng chỉ hành nghề môi giới bất động sản", "Văn phòng môi giới nhà đất, sàn giao dịch bất động sản"),
        ("4772", "Bán lẻ thuốc, dụng cụ y tế, mỹ phẩm và vật phẩm vệ sinh trong các cửa hàng chuyên doanh", 1, "Sở Y tế", "Giấy chứng nhận đủ điều kiện kinh doanh dược (GPP đối với nhà thuốc)", "Nhà thuốc tây, cửa hàng bán lẻ mỹ phẩm, thực phẩm chức năng"),
    ]

    cursor.executemany("""
    INSERT INTO industry_codes (code, name, is_conditional, regulatory_authority, license_required, description)
    VALUES (?, ?, ?, ?, ?, ?)
    """, industries)

    # 4. Nạp dữ liệu Danh mục Giấy phép con & Điều kiện
    licenses = [
        ("Giấy chứng nhận An toàn thực phẩm (ATVSTP)", "Chi cục An toàn vệ sinh thực phẩm / Phòng Y tế", 15, 700000, "Luật An toàn thực phẩm 2010, Nghị định 15/2018/NĐ-CP", "Đơn đề nghị cấp Giấy chứng nhận, Bản thuyết minh cơ sở vật chất, Giấy khám sức khỏe chủ cơ sở và nhân viên, Giấy xác nhận tập huấn kiến thức ATVSTP"),
        ("Giấy chứng nhận thẩm duyệt thiết kế PCCC", "Cục Cảnh sát PCCC & CNCH / Phòng Cảnh sát PCCC", 10, 500000, "Luật Phòng cháy chữa cháy, Nghị định 136/2020/NĐ-CP", "Bản vẽ thiết kế hệ thống PCCC, Văn bản đề nghị thẩm duyệt, Bản sao Giấy phép kinh doanh, Phương án chữa cháy cơ sở"),
        ("Giấy phép kinh doanh bán lẻ rượu", "Phòng Kinh tế / Kinh tế và Hạ tầng cấp Quận/Huyện", 10, 200000, "Nghị định 105/2017/NĐ-CP, Nghị định 17/2020/NĐ-CP", "Đơn đề nghị, Bản sao Giấy phép kinh doanh, Hợp đồng thuê mặt bằng, Hợp đồng nguyên tắc với nhà phân phối rượu có phép"),
        ("Thông báo website TMĐT bán hàng", "Cục Thương mại điện tử và Kinh tế số - Bộ Công Thương", 3, 0, "Nghị định 52/2013/NĐ-CP, Nghị định 85/2021/NĐ-CP", "Đăng ký tài khoản tại online.gov.vn, Cung cấp giấy phép kinh doanh, Chính sách bảo mật, Chính sách đổi trả và vận chuyển trên web"),
        ("Giấy phép kinh doanh vận tải bằng xe ô tô", "Sở Giao thông Vận tải cấp tỉnh/thành", 5, 200000, "Nghị định 10/2020/NĐ-CP", "Giấy đề nghị, Bản sao giấy phép kinh doanh, Phương án kinh doanh vận tải, Giấy tờ phương tiện và lắp đặt giám sát hành trình"),
    ]

    cursor.executemany("""
    INSERT INTO license_requirements (license_name, issuing_body, standard_duration_days, estimated_fee, legal_basis, required_dossier)
    VALUES (?, ?, ?, ?, ?, ?)
    """, licenses)

    # 5. Nạp dữ liệu Quy trình từng bước (Checklist hồ sơ)
    checklists = [
        # Hộ kinh doanh cá thể
        ("HO_KINH_DOANH", 1, "Soạn thảo giấy đề nghị đăng ký hộ kinh doanh", "Chuẩn bị tên hộ kinh doanh, địa điểm đặt quán/cửa hàng, ngành nghề kinh doanh và số vốn", "Bộ phận Một cửa UBND Quận/Huyện", "Giấy đề nghị và Hợp đồng thuê địa điểm"),
        ("HO_KINH_DOANH", 2, "Nộp hồ sơ và nhận kết quả", "Nộp hồ sơ trực tiếp hoặc online qua cổng dịch vụ công cấp huyện. Thời gian giải quyết: 3 ngày làm việc", "Phòng Tài chính - Kế hoạch UBND Quận/Huyện", "Giấy chứng nhận đăng ký hộ kinh doanh"),
        ("HO_KINH_DOANH", 3, "Đăng ký mã số thuế và kê khai thuế ban đầu", "Liên hệ Chi cục Thuế Quận/Huyện để kê khai phương pháp tính thuế khoán hoặc kê khai", "Chi cục Thuế cơ sở", "Thông báo Mã số thuế và mức thuế khoán"),
        ("HO_KINH_DOANH", 4, "Xin giấy phép con chuyên ngành (nếu có)", "Nộp hồ sơ xin giấy ATVSTP hoặc PCCC trước khi khai trương hoạt động chính thức", "Cơ quan chuyên ngành (Y tế / Công an)", "Giấy phép con đủ điều kiện hoạt động"),

        # Công ty TNHH 1 Thành viên
        ("TNHH_1TV", 1, "Chuẩn bị thông tin doanh nghiệp", "Xác định tên công ty (không trùng lặp), địa chỉ trụ sở (không được là chung cư nhà ở), vốn điều lệ, thông tin chủ sở hữu", "Nội bộ công ty", "Dự thảo Điều lệ công ty"),
        ("TNHH_1TV", 2, "Nộp hồ sơ thành lập doanh nghiệp trực tuyến", "Nộp hồ sơ qua Cổng thông tin quốc gia về đăng ký doanh nghiệp (dangkykinhdoanh.gov.vn)", "Phòng Đăng ký kinh doanh - Sở Kế hoạch và Đầu tư", "Giấy chứng nhận đăng ký doanh nghiệp (kèm MST)"),
        ("TNHH_1TV", 3, "Khắc con dấu và mở tài khoản ngân hàng", "Khắc con dấu pháp nhân công ty và ra ngân hàng thương mại mở tài khoản công ty", "Cơ sở khắc dấu & Ngân hàng thương mại", "Con dấu công ty & Số tài khoản doanh nghiệp"),
        ("TNHH_1TV", 4, "Mua chữ ký số (Token) và Hóa đơn điện tử", "Đăng ký mua thiết bị chữ ký số điện tử để ký nộp thuế và phát hành hóa đơn VAT điện tử", "Nhà cung cấp dịch vụ số (VNPT, Viettel, FPT, MISA)", "Chữ ký số Token & Hệ thống Hóa đơn điện tử"),
        ("TNHH_1TV", 5, "Nộp hồ sơ khai thuế ban đầu và treo bảng hiệu", "Nộp tờ khai lệ phí môn bài và treo biển hiệu công ty tại đúng địa chỉ trụ sở đăng ký", "Chi cục Thuế quản lý", "Thông báo chấp thuận kê khai thuế"),

        # Công ty Cổ phần
        ("CO_PHAN", 1, "Chuẩn bị cổ đông sáng lập & danh sách cổ đông", "Yêu cầu tối thiểu 3 cổ đông sáng lập. Lập danh sách cổ đông sáng lập, dự thảo Điều lệ công ty", "Nội bộ các cổ đông", "Biên bản họp và Danh sách cổ đông sáng lập"),
        ("CO_PHAN", 2, "Nộp hồ sơ thành lập tại Sở Kế hoạch và Đầu tư", "Nộp online tại dangkykinhdoanh.gov.vn kèm bản sao CCCD của tất cả cổ đông", "Sở Kế hoạch và Đầu tư tỉnh/thành", "Giấy chứng nhận đăng ký doanh nghiệp"),
        ("CO_PHAN", 3, "Mở tài khoản, chữ ký số, hóa đơn và góp vốn trong 90 ngày", "Các cổ đông góp đủ số vốn cam kết trong thời hạn 90 ngày kể từ ngày cấp phép", "Ngân hàng & Chi cục Thuế", "Giấy xác nhận góp vốn và Sổ cổ đông"),
    ]

    cursor.executemany("""
    INSERT INTO registration_checklist (entity_type, step_number, step_name, action_details, target_authority, output_document)
    VALUES (?, ?, ?, ?, ?, ?)
    """, checklists)

    conn.commit()
    conn.close()
    print(f"[OK] Khoi tao va nap du lieu thanh cong cho: {DB_PATH}")


if __name__ == "__main__":
    init_database()
