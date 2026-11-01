"""
Mô Phỏng Trực Quan Tố Tụng & Bàn Cờ Đối Kháng Pháp Lý 2 Chiều - Version 5.0
Công cụ mô phỏng chiến lược tố tụng dành cho người dân:
1. Dự báo tỷ lệ thắng kiện (0 - 100%) dựa trên chứng cứ thực tế.
2. Bàn cờ đối kháng 2 chiều:
   - Bên khởi kiện (Người dân) tấn công bằng luận điểm gì?
   - Bên bị kiện (Đối phương/Con nợ) sẽ phản đòn bằng chiêu bài gì? (Ví dụ: Chối nợ, nói bị ép ký, nại lý do bất khả kháng, yêu cầu đình chỉ vì hết thời hiệu).
3. Đòn phản công & Kế sách hóa giải dành riêng cho người dân.
"""

from typing import Dict, Any, List, Optional
from llm_provider.model_factory import ModelFactory


class LegalLitigationSimulator:
    """
    Công cụ mô phỏng giả lập phiên Tòa và bàn cờ tranh chấp 2 chiều.
    """

    def __init__(self, factory: Optional[ModelFactory] = None):
        self.factory = factory or ModelFactory()

    def simulate_case(self, case_type: str, facts: str, evidence_type: str) -> Dict[str, Any]:
        """
        Mô phỏng bàn cờ tố tụng đối kháng dựa trên tình tiết và dạng chứng cứ.
        """
        c_upper = case_type.upper()
        
        # 1. Đánh giá tỷ lệ thắng sơ bộ
        base_win_rate = 65
        if "CÔNG CHỨNG" in evidence_type.upper() or "VI BẰNG" in evidence_type.upper():
            base_win_rate = 90
        elif "GIẤY VIẾT TAY" in evidence_type.upper():
            base_win_rate = 75
        elif "TIN NHẮN ZALO" in evidence_type.upper():
            base_win_rate = 60
        else:
            base_win_rate = 45

        # 2. Xây dựng bàn cờ đối kháng chuyên biệt
        if "NỢ" in c_upper or "DEBT" in c_upper:
            plaintiff_attack = [
                "Luận điểm 1: Hợp đồng vay tài sản đã xác lập nghĩa vụ hoàn trả theo Điều 463 BLDS 2015.",
                "Luận điểm 2: Sao kê ngân hàng và chữ ký xác nhận số tiền nợ gốc đã thực nhận.",
                "Luận điểm 3: Bên vay chậm thanh toán phải chịu tiền lãi quá hạn theo Điều 468 BLDS 2015."
            ]
            defendant_counter = [
                "Chiêu phản đòn 1: Chối bỏ chữ ký, yêu cầu giám định chữ ký/chữ viết tay để kéo dài vụ án.",
                "Chiêu phản đòn 2: Khai rằng đã trả một phần bằng tiền mặt không có biên nhận để giảm nợ gốc.",
                "Chiêu phản đòn 3: Yêu cầu Tòa án đình chỉ giải quyết vì cho rằng đã 'hết thời hiệu khởi kiện 03 năm'."
            ]
            winning_tactics = [
                "Kế sách 1: Nộp ngay bản chính giấy vay tiền và sao kê tài khoản ngân hàng để Tòa trưng cầu giám định chữ ký (Bên thua phải chịu chi phí giám định).",
                "Kế sách 2: Lập 'Vi bằng Thừa phát lại' toàn bộ tin nhắn Zalo nơi đối phương từng thừa nhận còn nợ tiền.",
                "Kế sách 3: Làm 'Đơn yêu cầu Áp dụng biện pháp khẩn cấp tạm thời' (Điều 111, 114 BLTTDS) phong tỏa tài khoản ngân hàng hoặc kê biên bất động sản của con nợ ngay khi Tòa thụ lý đơn."
            ]
            court_forecast = "Khả năng Tòa tuyên buộc con nợ phải trả nợ gốc + lãi suất 10%/năm là rất cao nếu nguyên đơn giữ được bản chính giấy vay hoặc sao kê ngân hàng đối chiếu."

        elif "ĐẤT" in c_upper or "LAND" in c_upper:
            plaintiff_attack = [
                "Luận điểm 1: Thửa đất đã được cấp Giấy chứng nhận QSDĐ (Sổ đỏ) có tọa độ ranh giới hợp pháp.",
                "Luận điểm 2: Hành vi xây dựng tường rào lấn sang là hành vi xâm phạm quyền sử dụng đất hợp pháp (Điều 12, 166 Luật Đất đai).",
                "Luận điểm 3: Đã hoàn tất thủ tục hòa giải cơ sở tại UBND cấp xã nhưng hòa giải không thành (Điều 202 Luật Đất đai)."
            ]
            defendant_counter = [
                "Chiêu phản đòn 1: Nại rằng ranh giới đất cũ do ông cha để lại từ xưa, bản đồ địa chính cấp sổ đỏ cho nguyên đơn bị sai lệch diện tích.",
                "Chiêu phản đòn 2: Yêu cầu hủy Giấy chứng nhận quyền sử dụng đất của nguyên đơn với lý do cấp không đúng quy trình.",
                "Chiêu phản đòn 3: Kéo dài thời gian hòa giải tại xã để tiếp tục thi công hoàn thiện công trình kiên cố."
            ]
            winning_tactics = [
                "Kế sách 1: Nộp đơn khẩn cấp đến UBND cấp xã yêu cầu lập Biên bản vi phạm trật tự xây dựng và ban hành Quyết định đình chỉ thi công công trình lấn chiếm ngay lập tức.",
                "Kế sách 2: Yêu cầu Chi nhánh Văn phòng Đăng ký đất đai xuống đo đạc hiện trạng ranh giới thực tế đối chiếu với hồ sơ kỹ thuật thửa đất lưu trữ tại Sở TN&MT.",
                "Kế sách 3: Khởi kiện ra Tòa án yêu cầu: Buộc tháo dỡ phần công trình xây dựng lấn chiếm, khôi phục lại tình trạng ban đầu của đất."
            ]
            court_forecast = "Tòa án sẽ căn cứ vào Hồ sơ địa chính gốc và mốc ranh giới tọa độ VN-2000. Nếu Sổ đỏ của nguyên đơn đúng quy hoạch, Tòa buộc bên lấn chiếm phải tự tháo dỡ công trình."

        elif "LY HÔN" in c_upper or "DIVORCE" in c_upper:
            plaintiff_attack = [
                "Luận điểm 1: Đời sống hôn nhân mâu thuẫn trầm trọng, mục đích hôn nhân không đạt được (Điều 56 Luật HNGĐ 2014).",
                "Luận điểm 2: Con dưới 36 tháng tuổi được giao cho mẹ trực tiếp nuôi dưỡng (Điều 81 Luật HNGĐ).",
                "Luận điểm 3: Tài sản hình thành trong thời kỳ hôn nhân chia đôi nhưng có tính đến công sức đóng góp của mỗi bên (Điều 59 Luật HNGĐ)."
            ]
            defendant_counter = [
                "Chiêu phản đòn 1: Khai rằng nguyên đơn không có việc làm hoặc thu nhập bấp bênh để đòi quyền nuôi toàn bộ các con.",
                "Chiêu phản đòn 2: Tẩu tán nhà đất, ô tô bằng cách lập hợp đồng chuyển nhượng giả tạo cho người thân trước khi nộp đơn.",
                "Chiêu phản đòn 3: Nại ra các khoản nợ ảo để yêu cầu nguyên đơn phải gánh vác chia đôi nghĩa vụ trả nợ."
            ]
            winning_tactics = [
                "Kế sách 1: Chuẩn bị bảng lương, hợp đồng lao động và minh chứng về môi trường sống (chỗ ở ổn định, gần trường học) để bảo vệ quyền nuôi con.",
                "Kế sách 2: Yêu cầu Tòa án gửi công văn sang Văn phòng đăng ký đất đai và các Ngân hàng để tạm ngừng mọi giao dịch chuyển dịch tài sản của vợ/chồng.",
                "Kế sách 3: Yêu cầu người nại ra khoản nợ phải chứng minh số tiền đó được dùng vào nhu cầu thiết yếu của gia đình (Điều 37 Luật HNGĐ), nếu không đó là nợ riêng."
            ]
            court_forecast = "Tòa án luôn ưu tiên bảo vệ lợi ích của phụ nữ và trẻ em. Quyền nuôi con dưới 36 tháng gần như chắc chắn thuộc về mẹ nếu mẹ có thu nhập tối thiểu đảm bảo nuôi dưỡng."

        else:
            plaintiff_attack = [
                "Luận điểm 1: Quyền và lợi ích hợp pháp bị xâm phạm trực tiếp theo quy định của pháp luật dân sự.",
                "Luận điểm 2: Có tài liệu, chứng cứ khách quan chứng minh hành vi vi phạm nghĩa vụ."
            ]
            defendant_counter = [
                "Chiêu phản đòn 1: Bác bỏ toàn bộ trách nhiệm bồi thường.",
                "Chiêu phản đòn 2: Nại các lý do bất khả kháng hoặc lỗi hoàn toàn do nguyên đơn."
            ]
            winning_tactics = [
                "Kế sách 1: Thu thập đầy đủ chuỗi bằng chứng theo trình tự thời gian.",
                "Kế sách 2: Yêu cầu chính quyền hoặc cơ quan có thẩm quyền lập biên bản ghi nhận hiện trường."
            ]
            court_forecast = "Kết quả phụ thuộc vào tính xác thực và tính hợp pháp của tài liệu chứng cứ giao nộp cho Tòa án."

        return {
            "case_type": case_type,
            "win_rate": base_win_rate,
            "plaintiff_attack": plaintiff_attack,
            "defendant_counter": defendant_counter,
            "winning_tactics": winning_tactics,
            "court_forecast": court_forecast
        }
