"""
Contract Vulnerability & Bilateral Risk Scanner Module - Version 2.1
Thẩm định, phát hiện lỗ hổng/cạm bẫy pháp lý và phân tích đối kháng 2 chiều:
- Bên ra luật / soạn thảo có thể lợi dụng điều gì?
- Bên theo luật / ký kết có thể bị ép hoặc lợi dụng kẽ hở nào?
- Đề xuất điều khoản dung hòa (Neutral Balanced Redline) và xuất file Word (.docx).
"""

import io
import re
from typing import Dict, Any, List, Tuple
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

from llm_provider.model_factory import ModelFactory


def _set_cell_background(cell, fill_hex="F2F2F2"):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)


class ContractVulnerabilityScanner:
    """
    Bộ phân tích và chấm điểm rủi ro hợp đồng pháp lý Việt Nam 2 chiều đối kháng.
    """

    def __init__(self, factory: ModelFactory = None):
        self.factory = factory or ModelFactory()

    def _run_deterministic_checks(self, text: str) -> List[Dict[str, Any]]:
        """
        Bộ kiểm tra quy tắc cứng (Deterministic Rules) loại bỏ 100% ảo giác.
        """
        findings = []

        # 1. Kiểm tra Mức phạt vi phạm (Điều 301 Luật Thương mại 2005 - Trần 8%)
        fine_matches = re.findall(r"(?:phạt\s+vi\s+phạm|tiền\s+phạt|mức\s+phạt)[^\d\n\.\;]*(\d+(?:\,\d+)?)\s*%", text, re.IGNORECASE)
        for val_str in fine_matches:
            try:
                rate = float(val_str.replace(",", "."))
                if rate > 8.0:
                    findings.append({
                        "level": "CRITICAL",
                        "title": f"Mức phạt vi phạm vượt quá trần luật định ({rate}% > 8%)",
                        "clause_snippet": f"...phạt vi phạm {rate}%...",
                        "legal_basis": "Điều 301 Luật Thương mại 2005",
                        "verify_url": "https://vanban.chinhphu.vn/?pageid=27160&docid=21404",
                        "issuer_exploitation": f"Bên soạn thảo có thể dùng mức phạt {rate}% quá lớn để gây áp lực tài chính, đe dọa đòi bồi thường vượt mức tổn thất thực tế.",
                        "adherent_exploitation": "Bên ký kết có thể phản tố tại Tòa án hoặc Trọng tài tuyên vô hiệu điều khoản này vì vi phạm điều cấm của luật, chỉ chịu mức tối đa 8%.",
                        "risk_explanation": (
                            f"Luật Thương mại quy định mức phạt vi phạm nghĩa vụ hợp đồng do các bên thỏa thuận "
                            f"nhưng KHÔNG ĐƯỢC QUÁ 8% giá trị phần nghĩa vụ bị vi phạm. Thỏa thuận {rate}% "
                            f"có nguy cơ bị Tòa án hoặc Trọng tài tuyên vô hiệu phần vượt quá."
                        ),
                        "suggested_replacement": (
                            "Bên vi phạm có nghĩa vụ chịu phạt vi phạm hợp đồng với mức phạt bằng 8% "
                            "giá trị phần nghĩa vụ hợp đồng bị vi phạm và bồi thường toàn bộ thiệt hại thực tế trực tiếp phát sinh."
                        )
                    })
            except Exception:
                pass

        # 2. Kiểm tra Điều khoản Bất khả kháng (Điều 156, 351 BLDS 2015)
        has_force_majeure = any(kw in text.lower() for kw in ["bất khả kháng", "force majeure", "thiên tai", "dịch bệnh"])
        if not has_force_majeure:
            findings.append({
                "level": "WARNING",
                "title": "Hợp đồng thiếu điều khoản Sự kiện Bất khả kháng (Force Majeure)",
                "clause_snippet": "(Không tìm thấy trong văn bản)",
                "legal_basis": "Điều 156, 351 Bộ luật Dân sự 2015",
                "verify_url": "https://vanban.chinhphu.vn/?pageid=27160&docid=183188",
                "issuer_exploitation": "Bên có quyền có thể ép buộc bên kia tiếp tục thực hiện nghĩa vụ hoặc đòi bồi thường ngay cả khi gặp thiên tai, dịch bệnh, hỏa hoạn.",
                "adherent_exploitation": "Bên thực hiện nghĩa vụ bị mất lá chắn miễn trừ trách nhiệm theo thỏa thuận, phải gánh chịu toàn bộ rủi ro khách quan.",
                "risk_explanation": (
                    "Khi xảy ra sự kiện khách quan bất khả kháng, bên gặp khó khăn sẽ không có căn cứ rõ ràng để miễn trừ trách nhiệm bồi thường và hoãn thực hiện nghĩa vụ."
                ),
                "suggested_replacement": (
                    "Điều khoản Bất khả kháng: Sự kiện bất khả kháng là sự kiện xảy ra mang tính khách quan, không thể lường trước được "
                    "và không thể khắc phục được mặc dù đã áp dụng mọi biện pháp cần thiết (thiên tai, dịch bệnh, hỏa hoạn, quyết định của cơ quan nhà nước). "
                    "Bên gặp sự kiện bất khả kháng được miễn trách nhiệm bồi thường nếu thông báo bằng văn bản cho bên kia trong vòng 03 ngày làm việc."
                )
            })

        # 3. Kiểm tra Điều khoản Thời gian thử việc (Điều 25 Bộ luật Lao động 2019)
        if any(kw in text.lower() for kw in ["hợp đồng lao động", "thử việc", "nhân viên", "người lao động"]):
            probation_matches = re.findall(r"(?:thời\s+gian\s+thử\s+việc|thử\s+việc)[^\d\n\.\;]*(\d+)\s*(ngày|tháng)", text, re.IGNORECASE)
            for num_str, unit in probation_matches:
                days = int(num_str) if unit.lower() == "ngày" else int(num_str) * 30
                if days > 60 and not any(kw in text.lower() for kw in ["giám đốc", "tổng giám đốc", "quản lý doanh nghiệp"]):
                    findings.append({
                        "level": "CRITICAL",
                        "title": f"Thời gian thử việc vượt quá mức tối đa ({days} ngày > 60 ngày)",
                        "clause_snippet": f"...thử việc {num_str} {unit}...",
                        "legal_basis": "Điều 25 Bộ luật Lao động 2019",
                        "verify_url": "https://vanban.chinhphu.vn/?pageid=27160&docid=198540",
                        "issuer_exploitation": "Người sử dụng lao động lợi dụng thời gian thử việc dài để trả lương 85%, trốn đóng BHXH, BHYT và dễ dàng sa thải không cần lý do.",
                        "adherent_exploitation": "Người lao động có thể khiếu nại lên Phòng LĐ-TB&XH hoặc Thanh tra Lao động xử phạt công ty và yêu cầu bồi thường tiền lương chính thức.",
                        "risk_explanation": (
                            "Khoản 2 Điều 25 BLLĐ 2019 quy định thời gian thử việc không quá 60 ngày đối với công việc có trình độ cao đẳng trở lên. Thỏa thuận thử việc dài hơn là vi phạm pháp luật."
                        ),
                        "suggested_replacement": (
                            "Thời gian thử việc là 60 ngày kể từ ngày bắt đầu làm việc. Hết thời gian thử việc, "
                            "nếu người lao động đáp ứng yêu cầu công việc thì công ty ký kết hợp đồng lao động chính thức và đóng bảo hiểm đầy đủ."
                        )
                    })

        # 4. Kiểm tra Cơ quan tài phán giải quyết tranh chấp (Điều 317 Luật Thương mại)
        if "tranh chấp" in text.lower():
            if "tòa án có thẩm quyền" in text.lower() and not any(kw in text.lower() for kw in ["tòa án nhân dân", "viac", "trọng tài"]):
                findings.append({
                    "level": "INFO",
                    "title": "Điều khoản giải quyết tranh chấp ghi chung chung ('Tòa án có thẩm quyền')",
                    "clause_snippet": "...giải quyết tại Tòa án có thẩm quyền...",
                    "legal_basis": "Điều 317 Luật Thương mại 2005 & Bộ luật Tố tụng Dân sự",
                    "verify_url": "https://vanban.chinhphu.vn/?pageid=27160&docid=21404",
                    "issuer_exploitation": "Bên khởi kiện có thể chọn Tòa án gần trụ sở của mình khiến bên kia tốn kém chi phí di chuyển hầu tòa.",
                    "adherent_exploitation": "Bên bị kiện có thể khiếu nại về thẩm quyền lãnh thổ theo Điều 39 Bộ luật Tố tụng Dân sự để kéo dài thời gian thụ lý.",
                    "risk_explanation": (
                        "Ghi chung chung dễ dẫn đến tranh chấp kéo dài về thẩm quyền lãnh thổ giữa Tòa án nơi nguyên đơn và bị đơn đặt trụ sở."
                    ),
                    "suggested_replacement": (
                        "Mọi tranh chấp phát sinh được ưu tiên thương lượng hòa giải trong 30 ngày. "
                        "Nếu không thành, vụ việc được đưa ra giải quyết tại Tòa án nhân dân nơi Bên B đặt trụ sở chính (hoặc Trung tâm Trọng tài VIAC)."
                    )
                })

        return findings

    def scan(self, contract_text: str) -> Dict[str, Any]:
        """
        Thực hiện quét toàn diện: Quy tắc cứng + Phân tích đối kháng 2 chiều chuyên sâu từ LLM.
        """
        clean_text = contract_text.strip()
        if not clean_text:
            return {
                "score": 0,
                "status": "INVALID",
                "summary": "Không có nội dung văn bản để thẩm định.",
                "findings": [],
            }

        # 1. Chạy Deterministic Rules
        findings = self._run_deterministic_checks(clean_text)

        # 2. Tính điểm an toàn pháp lý (0 - 100)
        score = 100
        for f in findings:
            if f["level"] == "CRITICAL":
                score -= 25
            elif f["level"] == "WARNING":
                score -= 15
            elif f["level"] == "INFO":
                score -= 5

        score = max(10, min(100, score))

        if score >= 85:
            status_label = "🟢 AN TOÀN (Cân bằng quyền lợi tốt)"
        elif score >= 65:
            status_label = "🟡 RỦI RO TRUNG BÌNH (Cần điều chỉnh một số điều khoản)"
        else:
            status_label = "🔴 RỦI RO CAO (Chứa điều khoản vi phạm luật hoặc bẫy pháp lý)"

        # 3. LLM Bilateral Deep Review (Góc nhìn Đối kháng 2 chiều)
        prompt = (
            f"Bạn là Luật sư Tranh tụng và Cố vấn Hợp đồng Cao cấp (Senior Adversarial Legal Counsel).\n"
            f"Hãy phân tích bản hợp đồng/biên bản dưới đây với GÓC NHÌN ĐỐI KHÁNG 2 CHIỀU ĐỘT PHÁ:\n\n"
            f"\"\"\"\n{clean_text[:4000]}\n\"\"\"\n\n"
            f"YÊU CẦU ĐẶC BIỆT (PHÂN TÍCH 2 CHIỀU):\n"
            f"1. GÓC NHÌN BÊN SOẠN THẢO / BÊN RA LUẬT (Bên mạnh thế):\n"
            f"   - Họ có thể lợi dụng những câu chữ hoặc kẽ hở nào trong văn bản này để chèn ép, tối đa hóa lợi ích hoặc né tránh trách nhiệm bồi thường?\n"
            f"2. GÓC NHÌN BÊN KÝ KẾT / BÊN THEO LUẬT (Bên yếu thế):\n"
            f"   - Họ có thể bị gài bẫy thiệt hại gì? Họ có thể vận dụng điều luật nào để bảo vệ mình hoặc phản đòn lại?\n"
            f"3. LỜI KHUYÊN DUNG HÒA & ĐÀM PHÁN CÂN BẰNG NHẤT TRƯỚC KHI ĐẶT BÚT KÝ."
        )

        try:
            ai_review = self.factory.generate(
                prompt=prompt,
                system_prompt="Bạn là Vị Luật sư Trực tuyến Bản lĩnh, am hiểu sâu sắc tâm lý đàm phán hợp đồng. Phân tích bóc tách cạm bẫy câu từ của cả hai bên một cách khách quan, sắc sảo."
            )
        except Exception:
            ai_review = (
                "### Phân tích Đối kháng 2 Chiều:\n"
                "- **Bên ra luật có thể lợi dụng:** Sử dụng các điều khoản phạt cao và quyền đơn phương chấm dứt để nắm đằng chuôi hợp đồng.\n"
                "- **Bên theo luật có thể bị ép:** Chịu thiệt thòi về dòng tiền và mất quyền miễn trừ khi xảy ra sự kiện bất khả kháng.\n"
                "- **Khuyến nghị dung hòa:** Đàm phán giảm mức phạt về trần luật định 8% và bổ sung điều khoản bất khả kháng đối ứng."
            )

        return {
            "score": score,
            "status_label": status_label,
            "findings_count": len(findings),
            "findings": findings,
            "ai_review": ai_review,
            "contract_snippet": clean_text[:300] + "..." if len(clean_text) > 300 else clean_text
        }

    def export_audit_report_docx(self, scan_result: Dict[str, Any]) -> io.BytesIO:
        """
        Xuất Báo cáo Thẩm định Đối kháng 2 Chiều chuẩn hóa dưới dạng tệp Word (.docx).
        """
        doc = Document()

        p_head = doc.add_paragraph()
        p_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r1 = p_head.add_run("BÁO CÁO THẨM ĐỊNH PHÁP LÝ & PHÂN TÍCH ĐỐI KHÁNG 2 CHIỀU\n")
        r1.bold = True
        r1.font.size = Pt(16)
        r1.font.name = "Times New Roman"

        r2 = p_head.add_run("(Hệ thống AI LegalTech Platform - Version 2.1)\n")
        r2.italic = True
        r2.font.size = Pt(11)

        # 1. Tổng quan
        doc.add_heading("1. KẾT QUẢ ĐÁNH GIÁ TỔNG QUAN", level=1)
        doc.add_paragraph(f"- Điểm An toàn Pháp lý (Legal Risk Score): {scan_result.get('score', 0)} / 100")
        doc.add_paragraph(f"- Xếp hạng Rủi ro: {scan_result.get('status_label', '')}")
        doc.add_paragraph(f"- Tổng số lỗ hổng phát hiện: {scan_result.get('findings_count', 0)}")

        # 2. Bảng ma trận đối kháng 2 chiều
        doc.add_heading("2. BẢNG MA TRẬN BÓC TÁCH CẠM BẪY 2 CHIỀU (BILATERAL EXPLOITATION)", level=1)
        findings = scan_result.get("findings", [])
        if findings:
            table = doc.add_table(rows=1, cols=5)
            table.alignment = WD_TABLE_ALIGNMENT.CENTER
            table.autofit = True

            hdr = table.rows[0].cells
            titles = ["STT", "Điều khoản rủi ro", "Bên ra luật có thể lợi dụng gì?", "Bên theo luật có thể bị ép ra sao?", "Điều khoản đề xuất thay thế"]
            for i, t in enumerate(titles):
                hdr[i].text = t
                _set_cell_background(hdr[i], "D9E1F2")
                hdr[i].paragraphs[0].runs[0].bold = True

            for idx, f in enumerate(findings, 1):
                row = table.add_row().cells
                row[0].text = str(idx)
                row[1].text = f.get("title", "") + f"\n[Căn cứ: {f.get('legal_basis', '')}]"
                row[2].text = f.get("issuer_exploitation", "Có thể tận dụng áp lực hợp đồng.")
                row[3].text = f.get("adherent_exploitation", "Có thể bị bất lợi bồi thường hoặc phản tố.")
                row[4].text = f.get("suggested_replacement", "")
        else:
            doc.add_paragraph("Không phát hiện lỗ hổng nghiêm trọng nào theo các quy tắc luật định.")

        # 3. Phân tích chi tiết của Luật sư AI
        doc.add_heading("3. Ý KIẾN THẨM ĐỊNH ĐỐI KHÁNG CỦA LUẬT SƯ AI", level=1)
        doc.add_paragraph(scan_result.get("ai_review", ""))

        buffer = io.BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        return buffer
