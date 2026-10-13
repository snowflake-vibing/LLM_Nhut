"""
Few-Shot Prompting Templates
Bộ ví dụ mẫu (Few-shot learning) giúp LLM trích xuất chính xác ý định,
thông tin kinh doanh và ánh xạ sang mã ngành / loại hình.
"""

FEW_SHOT_ROUTER_EXAMPLES = """
Sau đây là một số ví dụ mẫu phân loại ý định người dùng:

Ví dụ 1:
Người dùng: "Tôi và bạn thân muốn cùng nhau mở quán trà sữa và đồ ăn vặt khoảng 200 triệu thì nên chọn loại hình công ty nào?"
Phân loại:
{
  "intent": "ENTITY_ADVISORY",
  "entities": ["mở quán trà sữa", "2 người cùng mở", "vốn 200 triệu"],
  "reasoning": "Người dùng đang phân vân giữa các loại hình công ty có nhiều thành viên góp vốn."
}

Ví dụ 2:
Người dùng: "Kinh doanh tiệm cắt tóc gội đầu và spa mini thì thuộc mã ngành nào? Có cần giấy phép an toàn thực phẩm hay PCCC không?"
Phân loại:
{
  "intent": "INDUSTRY_LOOKUP",
  "entities": ["cắt tóc gội đầu", "spa mini", "mã ngành", "PCCC"],
  "reasoning": "Người dùng hỏi trực tiếp về mã ngành VSIC và điều kiện cấp phép con."
}

Ví dụ 3:
Người dùng: "Quy trình nộp hồ sơ thành lập công ty TNHH 1 thành viên gồm những bước nào và nộp ở đâu?"
Phân loại:
{
  "intent": "REGISTRATION_STEPS",
  "entities": ["công ty TNHH 1 thành viên", "hồ sơ", "nơi nộp"],
  "reasoning": "Người dùng muốn biết checklist các bước nộp và cơ quan tiếp nhận hồ sơ."
}
"""

FEW_SHOT_ENTITY_EXTRACTION_EXAMPLES = """
Ví dụ mẫu trích xuất thông tin kế hoạch kinh doanh:

User Input: "Mình tên Nhựt, định mở công ty phần mềm chuyên làm web và app cho khách hàng nước ngoài, một mình mình làm chủ với vốn ban đầu 50 triệu."
Output JSON:
{
  "founder_name": "Nhựt",
  "business_idea": "Công ty phần mềm chuyên làm web và app xuất khẩu",
  "num_founders": 1,
  "capital_vnd": 50000000,
  "industry_keywords": ["lập trình phần mềm", "thiết kế website", "SaaS"],
  "suggested_type": "TNHH_1TV"
}
"""
