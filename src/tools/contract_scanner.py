"""
Contract Vulnerability & Risk Scanner Module
Thẩm định, phát hiện lỗ hổng/cạm bẫy pháp lý và chấm điểm an toàn cho hợp đồng.
Hỗ trợ xuất báo cáo thẩm định Word (.docx) và đề xuất điều khoản thay thế (Clause Redlining).
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
    Bộ phân tích và chấm điểm rủi ro hợp đồng pháp lý Việt Nam.
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
                        "risk_explanation": (
                            f"Luật Thương mại quy định mức phạt vi phạm nghĩa vụ hợp đồng do các bên thỏa thuận "
                            f"nhưng KHÔNG ĐƯỢC QUÁ 8% giá trị phần nghĩa vụ bị vi phạm. Thỏa thuận {rate}% "
                            f"có nguy cơ bị Tòa án hoặc Trọng tài tuyên vô hiệu phần vượt quá."
                        ),
                        "suggested_replacement": (
                            "Bên vi phạm có nghĩa vụ chịu phạt vi phạm hợp đồng với mức phạt bằng 8% "
                            "giá trị phần nghĩa vụ hợp đồng bị vi phạm và bồi thường toàn bộ thiệt hại thực tế phát sinh."
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
                "risk_explanation": (
                    "Khi xảy ra sự kiện khách quan bất khả kháng (hỏa hoạn, thiên tai, dịch bệnh phong tỏa, thay đổi chính sách nhà nước), "
                    "bên gặp khó khăn sẽ không có căn cứ rõ ràng để miễn trừ trách nhiệm bồi thường và hoãn thực hiện nghĩa vụ."
                ),
                "suggested_replacement": (
                    "Điều khoản Bất khả kháng: Sự kiện bất khả kháng là sự kiện xảy ra mang tính khách quan, không thể lường trước được "
                    "và không thể khắc phục được mặc dù đã áp dụng mọi biện pháp cần thiết (thiên tai, dịch bệnh, chiến tranh, quyết định của cơ quan nhà nước). "
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
                        "risk_explanation": (
                            "Khoản 2 Điều 25 BLLĐ 2019 quy định thời gian thử việc không quá 60 ngày đối với công việc có trình độ cao đẳng trở lên. "
                            "Thỏa thuận thử việc dài hơn là vi phạm pháp luật và có thể bị xử phạt vi phạm hành chính."
                        ),
                        "suggested_replacement": (
                            "Thời gian thử việc là 60 ngày kể từ ngày bắt đầu làm việc. Hết thời gian thử việc, "
                            "nếu người lao động đáp ứng yêu cầu công việc thì người sử dụng lao động có trách nhiệm ký kết hợp đồng lao động chính thức."
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
                    "risk_explanation": (
                        "Ghi chung chung dễ dẫn đến tranh chấp kéo dài về thẩm quyền lãnh thổ giữa Tòa án nơi nguyên đơn và bị đơn đặt trụ sở. "
                        "Nên chỉ định rõ Tòa án nhân dân cấp tỉnh/thành phố cụ thể hoặc Trung tâm Trọng tài Quốc tế Việt Nam (VIAC)."
                    ),
                    "suggested_replacement": (
                        "Mọi tranh chấp phát sinh từ hoặc liên quan đến hợp đồng này trước hết được giải quyết thông qua thương lượng hòa giải. "
                        "Nếu không thương lượng được trong vòng 30 ngày, tranh chấp sẽ được đưa ra giải quyết tại Tòa án nhân dân có thẩm quyền tại nơi Bên A đặt trụ sở chính (hoặc tại Trung tâm Trọng tài Quốc tế Việt Nam - VIAC)."
                    )
                })

        return findings

    def scan(self, contract_text: str) -> Dict[str, Any]:
        """
        Thực hiện quét toàn diện: Quy tắc cứng + LLM phân tích sâu & tính điểm an toàn.
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

        # Phân loại trạng thái
        if score >= 85:
            status_label = "🟢 AN TOÀN (Cân bằng quyền lợi tốt)"
        elif score >= 65:
            status_label = "🟡 RỦI RO TRUNG BÌNH (Cần điều chỉnh một số điều khoản)"
        else:
            status_label = "🔴 RỦI RO CAO (Chứa điều khoản vi phạm luật hoặc bẫy pháp lý)"

        # 3. LLM Deep Review
        prompt = (
            f"Bạn là chuyên gia thẩm định hợp đồng pháp lý cao cấp (Senior Legal Counsel).\n"
            f"Dưới đây là nội dung một bản hợp đồng:\n\n"
            f"\"\"\"\n{clean_text[:4000]}\n\"\"\"\n\n"
            f"Các rủi ro sơ bộ đã phát hiện bằng hệ thống quy tắc:\n"
            f"{[f['title'] for f in findings]}\n\n"
            f"Hãy đưa ra:\n"
            f"1. Nhận xét tổng quan về tính cân bằng nghĩa vụ giữa hai bên.\n"
            f"2. Cảnh báo các cạm bẫy bất lợi tiềm ẩn đối với bên yếu thế.\n"
            f"3. Lời khuyên đàm phán quan trọng nhất trước khi đặt bút ký."
        )

        try:
            ai_review = self.factory.generate(
                prompt=prompt,
                system_prompt="Bạn là Trợ lý Thẩm định Hợp đồng Doanh nghiệp và Cá nhân. Phân tích sắc sảo, khách quan, bảo vệ quyền lợi hợp pháp."
            )
        except Exception:
            ai_review = (
                "Hợp đồng cần được rà soát kỹ các điều khoản về nghĩa vụ thanh toán, thời hạn bảo hành "
                "và chế tài bồi thường. Đảm bảo các mốc thời gian và chế tài phải có tính đối ứng, bình đẳng giữa hai bên."
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
        Xuất Báo cáo Thẩm định Rủi ro Hợp đồng chuẩn hóa dưới dạng tệp Word (.docx).
        """
        doc = Document()

        # Quốc hiệu Tiêu ngữ
        p_head = doc.add_paragraph()
        p_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r1 = p_head.add_run("BÁO CÁO THẨM ĐỊNH PHÁP LÝ & QUÉT LỖ HỔNG HỢP ĐỒNG\n")
        r1.bold = True
        r1.font.size = Pt(16)
        r1.font.name = "Times New Roman"

        r2 = p_head.add_run("(Hệ thống AI LegalTech Intelligence - Version 2.0)\n")
        r2.italic = True
        r2.font.size = Pt(11)

        # Thông tin tổng quan
        doc.add_heading("1. KẾT QUẢ ĐÁNH GIÁ TỔNG QUAN", level=1)
        doc.add_paragraph(f"- Điểm An toàn Pháp lý (Legal Risk Score): {scan_result.get('score', 0)} / 100")
        doc.add_paragraph(f"- Mức độ Đánh giá: {scan_result.get('status_label', '')}")
        doc.add_paragraph(f"- Tổng số lỗ hổng & cảnh báo phát hiện: {scan_result.get('findings_count', 0)}")

        # Bảng chi tiết lỗ hổng
        doc.add_heading("2. DANH MỤC LỖ HỔNG & ĐIỀU KHOẢN RỦI RO CHI TIẾT", level=1)
        findings = scan_result.get("findings", [])
        if findings:
            table = doc.add_table(rows=1, cols=5)
            table.alignment = WD_TABLE_ALIGNMENT.CENTER
            table.autofit = True

            hdr = table.rows[0].cells
            titles = ["STT", "Mức độ", "Vấn đề / Điều khoản", "Căn cứ Pháp luật", "Đề xuất Thay thế (Redline)"]
            for i, t in enumerate(titles):
                hdr[i].text = t
                _set_cell_background(hdr[i], "D9E1F2")
                hdr[i].paragraphs[0].runs[0].bold = True

            for idx, f in enumerate(findings, 1):
                row = table.add_row().cells
                row[0].text = str(idx)
                row[1].text = f.get("level", "")
                row[2].text = f.get("title", "") + f"\n[Trích dẫn: {f.get('clause_snippet', '')}]"
                row[3].text = f.get("legal_basis", "")
                row[4].text = f.get("suggested_replacement", "")
        else:
            doc.add_paragraph("Không phát hiện lỗ hổng nghiêm trọng nào theo các quy tắc luật định.")

        # Đánh giá chuyên sâu của AI
        doc.add_heading("3. Ý KIẾN THẨM ĐỊNH & KHUYẾN NGHỊ ĐÀM PHÁN (AI COUNSEL)", level=1)
        doc.add_paragraph(scan_result.get("ai_review", ""))

        buffer = io.BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        return buffer
