"""
Multi-Agent Orchestrator & Workflow - Version 2.0
Điều phối toàn bộ quy trình làm việc giữa các Agent, tích hợp Lớp bảo mật Guardrails,
Thẩm định Hợp đồng, Soạn thảo Hồ sơ và In-Chat Generative Actions.
"""

import sys
import os
from typing import Dict, Any, Optional

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from llm_provider.model_factory import ModelFactory
from src.security import PIIMasker, PromptInjectionGuard, OutputModerator
from src.agents.router_agent import RouterAgent
from src.agents.advisory_agent import EntityAdvisoryAgent
from src.agents.lookup_agent import IndustryLookupAgent
from src.agents.reviewer_agent import DocumentReviewerAgent
from src.tools.contract_scanner import ContractVulnerabilityScanner
from src.tools.social_cases_knowledge import SocialCasesKnowledgeEngine, SOCIAL_CASES_DATA
from src.dossier.dynamic_drafter import DynamicLegalDrafter


class LegalMultiAgentWorkflow:
    """
    Hệ thống điều phối Đa tác nhân (Multi-Agent System) cho LegalTech Platform - Version 2.1.
    """

    def __init__(self, factory: Optional[ModelFactory] = None):
        self.factory = factory or ModelFactory()
        self.pii_masker = PIIMasker()
        self.injection_guard = PromptInjectionGuard()
        self.output_moderator = OutputModerator()

        self.router_agent = RouterAgent(self.factory)
        self.advisory_agent = EntityAdvisoryAgent(self.factory)
        self.lookup_agent = IndustryLookupAgent(self.factory)
        self.reviewer_agent = DocumentReviewerAgent(self.factory)
        self.contract_scanner = ContractVulnerabilityScanner(self.factory)
        self.dynamic_drafter = DynamicLegalDrafter(self.factory)

    def process(self, raw_user_query: str) -> Dict[str, Any]:
        """
        Quy trình xử lý hoàn chỉnh từ lúc nhận input đến khi trả lời:
        1. Guardrail 1: Kiểm tra an toàn Prompt Injection & Ý định trái luật.
        2. Guardrail 2: Masking dữ liệu nhạy cảm PII (CCCD, SĐT, Email).
        3. Router Agent: Xác định ý định và Agent chuyên trách.
        4. Specialized Agent: Thực thi tác vụ (RAG, SQL, Contract Scanner, Social Cases, Dynamic Drafter).
        5. Guardrail 3: Unmasking dữ liệu và kiểm duyệt phản hồi + gắn Disclaimer.
        """
        # BƯỚC 1: Kiểm tra an toàn đầu vào
        is_safe, violation_msg = self.injection_guard.check_safety(raw_user_query)
        if not is_safe:
            return {
                "success": False,
                "error": "SECURITY_VIOLATION",
                "response": violation_msg,
                "active_agent": "SecurityGuardrail",
                "citations": [],
                "action_type": None,
            }

        # BƯỚC 2: Che giấu thông tin cá nhân (PII Masking)
        masked_query, pii_mapping = self.pii_masker.mask_text(raw_user_query)

        # BƯỚC 3: Router Agent điều hướng
        route_decision = self.router_agent.route(masked_query)
        intent = route_decision.get("intent", "ENTITY_ADVISORY")

        # BƯỚC 4: Gọi Agent chuyên trách
        citations = []
        action_type = None
        action_data = None

        if intent == "SOCIAL_CASE_ADVISORY":
            active_agent = "SocialCasesAdvisoryAgent"
            case_id = route_decision.get("case_id", "DEBT_COLLECTION")
            raw_response = SocialCasesKnowledgeEngine.generate_advisory_text(case_id)
            action_type = "DYNAMIC_DRAFT_ACTION"
            action_data = {"case_id": case_id}

            case_info = SOCIAL_CASES_DATA.get(case_id, {})
            for law_str in case_info.get("key_laws", []):
                citations.append({
                    "law_title": law_str.split(":")[0] if ":" in law_str else law_str,
                    "article": law_str,
                    "header": case_info.get("title", "Tình huống pháp lý xã hội"),
                    "verify_url": "https://vanban.chinhphu.vn/",
                    "text_snippet": law_str,
                    "full_text": case_info.get("core_doctrine", "")
                })

        elif intent == "DYNAMIC_DRAFT":
            active_agent = "DynamicDocumentDrafter"
            case_id = route_decision.get("case_id", "CUSTOM")
            action_type = "DYNAMIC_DRAFT_ACTION"
            action_data = {"case_id": case_id}
            raw_response = (
                "### 📝 Biểu mẫu Soạn thảo Văn bản Pháp lý Thông minh (In-Chat Smart Form):\n"
                "Tôi đã kích hoạt biểu mẫu điền sẵn 100% căn cứ pháp luật và nội dung tranh tụng chuẩn mực ngay bên dưới. "
                "Bạn chỉ cần điền thông tin cá nhân (nếu có), trường nào chưa biết có thể để trống — hệ thống sẽ tự động chèn dòng kẻ giữ chỗ "
                "để bạn tải ngay file Word (.docx) dùng ngay!"
            )
            citations = [
                {
                    "law_title": "Bộ luật Dân sự & Nghị định 30/2020/NĐ-CP",
                    "article": "Quy chuẩn thể thức văn bản tư pháp",
                    "header": "Biểu mẫu pháp lý chuẩn mực",
                    "verify_url": "https://vanban.chinhphu.vn/?pageid=27160&docid=199514",
                    "text_snippet": "Thể thức trình bày văn bản hành chính và văn bản tố tụng tư pháp chuẩn quốc gia.",
                    "full_text": "Quy định về căn lề, Quốc hiệu, Tiêu ngữ, số hiệu và chữ ký theo Nghị định 30/2020/NĐ-CP."
                }
            ]

        elif intent == "CONTRACT_AUDIT":
            active_agent = "ContractVulnerabilityScanner"
            scan_res = self.contract_scanner.scan(masked_query)
            action_type = "CONTRACT_AUDIT_ACTION"
            action_data = scan_res

            # Rút trích citations từ findings
            for f in scan_res.get("findings", []):
                citations.append({
                    "law_title": f.get("legal_basis", "Quy định pháp luật"),
                    "article": f.get("title", ""),
                    "header": f.get("title", ""),
                    "verify_url": f.get("verify_url", "https://vanban.chinhphu.vn/"),
                    "text_snippet": f.get("risk_explanation", "")[:200],
                    "full_text": f.get("suggested_replacement", "")
                })

            resp_parts = [
                f"### 🛡️ Kết quả Thẩm định Rủi ro Hợp đồng (Legal Risk Audit):\n",
                f"- **Điểm An toàn Pháp lý:** `{scan_res['score']} / 100` ({scan_res['status_label']})\n",
                f"- **Số lượng vấn đề phát hiện:** `{scan_res['findings_count']}`\n\n",
                f"**Ý kiến chuyên gia thẩm định (Phân tích đối kháng 2 chiều):**\n{scan_res['ai_review']}\n\n",
                f"👉 *Bạn có thể tải Báo cáo Thẩm định (.docx) hoặc chỉnh sửa trực tiếp qua công cụ bên dưới!*"
            ]
            raw_response = "".join(resp_parts)

        elif intent == "DOSSIER_CREATION":
            active_agent = "DossierDraftingAgent"
            action_type = "DOSSIER_CREATION_ACTION"
            raw_response = (
                "### 📝 Bộ Soạn thảo Hồ sơ Doanh nghiệp Tự động (In-Chat Canvas):\n"
                "Tôi đã kích hoạt biểu mẫu tạo lập hồ sơ pháp lý chuẩn theo Nghị định 01/2021/NĐ-CP ngay bên dưới. "
                "Bạn có thể điền thông tin và bấm nút xuất trọn bộ file Word (.docx) dùng ngay!"
            )
            citations = [
                {
                    "law_title": "Nghị định 01/2021/NĐ-CP về đăng ký doanh nghiệp",
                    "article": "Phụ lục I-2, I-3",
                    "header": "Biểu mẫu Giấy đề nghị đăng ký doanh nghiệp",
                    "verify_url": "https://vanban.chinhphu.vn/?pageid=27160&docid=202613",
                    "text_snippet": "Biểu mẫu quy chuẩn áp dụng toàn quốc khi đăng ký thành lập doanh nghiệp.",
                    "full_text": "Phụ lục ban hành kèm theo Thông tư 01/2021/TT-BKHĐT và Nghị định 01/2021/NĐ-CP..."
                }
            ]

        elif intent == "INDUSTRY_LOOKUP":
            agent_result = self.lookup_agent.lookup(masked_query)
            active_agent = "IndustryLookupAgent"
            raw_response = agent_result["response"]
            citations = agent_result.get("citations", [])

        elif intent == "REGISTRATION_STEPS":
            agent_result = self.reviewer_agent.generate_checklist(masked_query)
            active_agent = "DocumentReviewerAgent"
            raw_response = agent_result["response"]
            citations = agent_result.get("citations", [])

        else:
            agent_result = self.advisory_agent.advise(masked_query)
            active_agent = "EntityAdvisoryAgent"
            raw_response = agent_result["response"]
            citations = agent_result.get("citations", [])

        # BƯỚC 5: Khôi phục PII & Kiểm duyệt đầu ra
        unmasked_response = self.pii_masker.unmask_text(raw_response, pii_mapping)
        final_response, is_approved = self.output_moderator.moderate_and_append_disclaimer(unmasked_response)

        return {
            "success": True,
            "intent": intent,
            "active_agent": active_agent,
            "response": final_response,
            "citations": citations,
            "action_type": action_type,
            "action_data": action_data,
            "masked_query": masked_query,
            "has_pii": bool(pii_mapping),
        }
