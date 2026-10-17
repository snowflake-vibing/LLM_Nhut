"""
Dossier Module
Quản lý tạo lập, thẩm định và xuất biểu mẫu hồ sơ pháp lý doanh nghiệp (.docx).
"""

from .template_generator import (
    generate_registration_request_docx,
    generate_company_charter_docx,
    generate_member_list_docx,
    generate_full_dossier_docx,
    validate_company_name,
    validate_dossier_legal_compliance,
)
from .dynamic_drafter import DynamicLegalDrafter

__all__ = [
    "generate_registration_request_docx",
    "generate_company_charter_docx",
    "generate_member_list_docx",
    "generate_full_dossier_docx",
    "validate_company_name",
    "validate_dossier_legal_compliance",
    "DynamicLegalDrafter",
]
