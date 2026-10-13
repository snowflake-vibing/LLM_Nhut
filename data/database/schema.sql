# ==============================================================
# HỆ THỐNG CƠ SỞ DỮ LIỆU PHÁP LÝ DOANH NGHIỆP (SME LEGAL DB)
# Bao gồm bảng mã ngành kinh tế Việt Nam (VSIC) và điều kiện cấp phép
# ==============================================================

CREATE TABLE IF NOT EXISTS industry_codes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,               -- Mã ngành VSIC (Cấp 4 hoặc Cấp 5)
    name TEXT NOT NULL,                      -- Tên ngành nghề kinh doanh
    is_conditional BOOLEAN DEFAULT 0,        -- Ngành nghề có điều kiện (1: có, 0: không)
    regulatory_authority TEXT,               -- Cơ quan quản lý chuyên ngành
    license_required TEXT,                   -- Giấy phép con yêu cầu (nếu có)
    description TEXT                         -- Chi tiết phạm vi hoạt động
);

CREATE TABLE IF NOT EXISTS license_requirements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    license_name TEXT NOT NULL,              -- Tên giấy phép con / chứng chỉ
    issuing_body TEXT NOT NULL,              -- Cơ quan cấp (Sở Y tế, Công an PCCC...)
    standard_duration_days INTEGER,          -- Thời gian xử lý tiêu chuẩn (ngày làm việc)
    estimated_fee INTEGER,                   -- Lệ phí nhà nước ước tính (VNĐ)
    legal_basis TEXT,                        -- Căn cứ pháp lý
    required_dossier TEXT                    -- Thành phần hồ sơ yêu cầu
);

CREATE TABLE IF NOT EXISTS registration_checklist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_type TEXT NOT NULL,               -- 'TNHH_1TV', 'TNHH_2TV', 'CO_PHAN', 'HO_KINH_DOANH'
    step_number INTEGER NOT NULL,            -- Thứ tự bước thực hiện
    step_name TEXT NOT NULL,                 -- Tên bước
    action_details TEXT NOT NULL,            -- Hướng dẫn chi tiết
    target_authority TEXT NOT NULL,          -- Cơ quan tiếp nhận
    output_document TEXT NOT NULL            -- Kết quả nhận được
);
