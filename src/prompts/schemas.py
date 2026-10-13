"""
Pydantic Schemas for Structured Output
Định nghĩa cấu trúc dữ liệu JSON đầu ra chuẩn hóa cho hồ sơ thành lập và tư vấn SME.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class BusinessEntityRecommendation(BaseModel):
    """Đề xuất mô hình tổ chức doanh nghiệp tối ưu."""
    recommended_type: str = Field(
        ...,
        description="Loại hình doanh nghiệp đề xuất: 'Hộ kinh doanh cá thể', 'Công ty TNHH 1 TV', 'Công ty TNHH 2 TV trở lên', hoặc 'Công ty Cổ phần'"
    )
    suitability_score: float = Field(
        ...,
        description="Điểm độ phù hợp từ 0.0 đến 1.0"
    )
    key_reasons: List[str] = Field(
        ...,
        description="Danh sách lý do tại sao loại hình này phù hợp với mục tiêu và quy mô"
    )
    capital_liability: str = Field(
        ...,
        description="Chế độ trách nhiệm tài sản (Vô hạn hay Hữu hạn trong phạm vi vốn góp)"
    )
    tax_advantages: str = Field(
        ...,
        description="Đặc điểm nghĩa vụ thuế (Thuế khoán/kê khai vs Thuế TNDN)"
    )


class IndustryLicenseDetail(BaseModel):
    """Thông tin mã ngành và giấy phép con."""
    code: str = Field(..., description="Mã ngành VSIC cấp 4")
    name: str = Field(..., description="Tên ngành nghề kinh doanh")
    is_conditional: bool = Field(..., description="Ngành nghề có điều kiện hay không")
    license_required: Optional[str] = Field(None, description="Tên giấy phép con hoặc chứng chỉ hành nghề")
    issuing_authority: Optional[str] = Field(None, description="Cơ quan có thẩm quyền cấp phép")


class LegalDossierChecklist(BaseModel):
    """Hồ sơ pháp lý hoàn chỉnh cần chuẩn bị."""
    entity_type: str = Field(..., description="Loại hình doanh nghiệp đã chọn")
    company_name_candidates: List[str] = Field(..., description="Các phương án tên dự kiến không trùng lặp")
    industry_codes: List[IndustryLicenseDetail] = Field(..., description="Danh mục mã ngành đăng ký")
    required_documents: List[str] = Field(..., description="Danh mục giấy tờ cần nộp (Giấy đề nghị, Điều lệ, CCCD...)")
    estimated_timeline_days: int = Field(..., description="Tổng thời gian thực hiện ước tính (ngày làm việc)")
    estimated_total_cost_vnd: int = Field(..., description="Tổng chi phí nhà nước ước tính (VNĐ)")
    legal_citations: List[str] = Field(..., description="Căn cứ pháp luật trích dẫn (Điều, Khoản của Luật)")
