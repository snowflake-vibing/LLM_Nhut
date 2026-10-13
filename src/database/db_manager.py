"""
Database Manager Module
Quản lý kết nối, truy vấn dữ liệu từ SQLite Database sme_legal.db.
"""

import os
import sqlite3
from typing import List, Dict, Any, Optional

DEFAULT_DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "data", "database", "sme_legal.db"
)


class DatabaseManager:
    """
    Quản lý kết nối và thực thi các câu lệnh truy vấn CSDL pháp lý doanh nghiệp.
    """

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or DEFAULT_DB_PATH

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def query(self, sql: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Thực thi câu truy vấn SELECT và trả về danh sách dict."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def search_industry(self, keyword: str) -> List[Dict[str, Any]]:
        """
        Tìm kiếm mã ngành kinh tế VSIC theo mã số hoặc tên ngành nghề.
        """
        sql = """
        SELECT code, name, is_conditional, regulatory_authority, license_required, description
        FROM industry_codes
        WHERE code LIKE ? OR name LIKE ? OR description LIKE ?
        ORDER BY is_conditional DESC, code ASC
        """
        like_kw = f"%{keyword}%"
        return self.query(sql, (like_kw, like_kw, like_kw))

    def get_license_info(self, keyword: str) -> List[Dict[str, Any]]:
        """
        Tra cứu điều kiện và thủ tục cấp giấy phép con theo tên giấy phép hoặc cơ quan cấp.
        """
        sql = """
        SELECT license_name, issuing_body, standard_duration_days, estimated_fee, legal_basis, required_dossier
        FROM license_requirements
        WHERE license_name LIKE ? OR legal_basis LIKE ?
        """
        like_kw = f"%{keyword}%"
        return self.query(sql, (like_kw, like_kw))

    def get_checklist(self, entity_type: str) -> List[Dict[str, Any]]:
        """
        Lấy các bước thực hiện thủ tục đăng ký theo loại hình doanh nghiệp.
        entity_type: 'HO_KINH_DOANH', 'TNHH_1TV', 'CO_PHAN'...
        """
        clean_type = entity_type.upper().strip()
        sql = """
        SELECT step_number, step_name, action_details, target_authority, output_document
        FROM registration_checklist
        WHERE entity_type = ?
        ORDER BY step_number ASC
        """
        return self.query(sql, (clean_type,))

    def execute_safe_sql(self, sql: str) -> List[Dict[str, Any]]:
        """
        Thực thi câu truy vấn SQL tùy biến do LLM sinh ra (chỉ cho phép SELECT để đảm bảo bảo mật).
        """
        clean_sql = sql.strip()
        if not clean_sql.upper().startswith("SELECT"):
            raise PermissionError("Chỉ cho phép thực thi câu lệnh truy vấn dữ liệu (SELECT)!")

        # Chặn các từ khóa phá hoại
        forbidden = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE"]
        for word in forbidden:
            if word in clean_sql.upper().split():
                raise PermissionError(f"Từ khóa '{word}' không được phép sử dụng vì lý do an toàn!")

        return self.query(clean_sql)
