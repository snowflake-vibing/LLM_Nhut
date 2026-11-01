"""
Official LangGraph Multi-Agent Orchestrator & Workflow - Version 2.2
Xây dựng dựa trên thư viện chính thức langchain-ai/langgraph (StateGraph, START, END).
Điều phối mạng lưới Đa tác nhân: Guardrails, Router, 6 Chuyên viên Pháp lý, và Output Moderator.
"""

import sys
import os
from typing import Dict, Any, Optional, List, TypedDict

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from langgraph.graph import StateGraph, START, END

from llm_provider.model_factory import ModelFactory
from src.security import PIIMasker, PromptInjectionGuard, OutputModerator
from src.agents.router_agent import RouterAgent
from src.agents.advisory_agent import EntityAdvisoryAgent
from src.agents.lookup_agent import IndustryLookupAgent
from src.agents.reviewer_agent import DocumentReviewerAgent
from src.tools.contract_scanner import ContractVulnerabilityScanner
from src.tools.social_cases_knowledge import SocialCasesKnowledgeEngine, SOCIAL_CASES_DATA
from src.dossier.dynamic_drafter import DynamicLegalDrafter


class LegalAgentState(TypedDict):
    """
    Trạng thái luân chuyển xuyên suốt Đồ thị Tác nhân LangGraph (Stateful Workflow).
    """
    raw_query: str
    masked_query: str
    pii_mapping: Dict[str, str]
    is_safe: bool
    error: Optional[str]
    intent: str
    case_id: Optional[str]
    active_agent: str
    response: str
    citations: List[Dict[str, Any]]
    action_type: Optional[str]
    action_data: Optional[Dict[str, Any]]


class LegalMultiAgentWorkflow:
    """
    Hệ thống điều phối Đa tác nhân (Multi-Agent System) - Chuẩn LangGraph Version 2.2.
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

        # Xây dựng và biên dịch LangGraph StateGraph
        self.graph = self._build_langgraph()

    def _build_langgraph(self):
        """Khởi tạo và kết nối các Nodes & Edges trong đồ thị LangGraph."""
        builder = StateGraph(LegalAgentState)

        # 1. Đăng ký các Nodes
        builder.add_node("guardrail_node", self._node_guardrail)
        builder.add_node("router_node", self._node_router)
        builder.add_node("social_case_node", self._node_social_case)
        builder.add_node("dynamic_draft_node", self._node_dynamic_draft)
        builder.add_node("contract_audit_node", self._node_contract_audit)
        builder.add_node("dossier_node", self._node_dossier)
        builder.add_node("industry_lookup_node", self._node_industry_lookup)
        builder.add_node("registration_steps_node", self._node_registration_steps)
        builder.add_node("entity_advisory_node", self._node_entity_advisory)
        builder.add_node("moderator_node", self._node_moderator)

        # 2. Kết nối luồng cơ sở
        builder.add_edge(START, "guardrail_node")
        builder.add_edge("guardrail_node", "router_node")

        # 3. Rẽ nhánh điều kiện từ Router tới các Agent chuyên môn
        builder.add_conditional_edges(
            "router_node",
            self._route_decision_edge,
            {
                "SOCIAL_CASE_ADVISORY": "social_case_node",
                "DYNAMIC_DRAFT": "dynamic_draft_node",
                "CONTRACT_AUDIT": "contract_audit_node",
                "DOSSIER_CREATION": "dossier_node",
                "INDUSTRY_LOOKUP": "industry_lookup_node",
                "REGISTRATION_STEPS": "registration_steps_node",
                "ENTITY_ADVISORY": "entity_advisory_node",
                "UNSAFE": "moderator_node",
            }
        )

        # 4. Tất cả các Node chuyên môn hội tụ về Moderator Node để kiểm duyệt và khôi phục PII
        for node_name in [
            "social_case_node",
            "dynamic_draft_node",
            "contract_audit_node",
            "dossier_node",
            "industry_lookup_node",
            "registration_steps_node",
            "entity_advisory_node",
        ]:
            builder.add_edge(node_name, "moderator_node")

        builder.add_edge("moderator_node", END)
        return builder.compile()

    # ------------------ CÁC NODE XỬ LÝ (LANGGRAPH NODES) ------------------

    def _node_guardrail(self, state: LegalAgentState) -> Dict[str, Any]:
        """Node 1: Kiểm tra an toàn Prompt Injection và Masking PII."""
        raw_query = state.get("raw_query", "")
        is_safe, violation_msg = self.injection_guard.check_safety(raw_query)

        if not is_safe:
            return {
                "is_safe": False,
                "error": "SECURITY_VIOLATION",
                "response": violation_msg,
                "active_agent": "SecurityGuardrail",
                "citations": [],
                "action_type": None,
                "action_data": None,
            }

        masked_text, mapping = self.pii_masker.mask_text(raw_query)
        return {
            "is_safe": True,
            "error": None,
            "masked_query": masked_text,
            "pii_mapping": mapping,
        }

    def _node_router(self, state: LegalAgentState) -> Dict[str, Any]:
        """Node 2: Router Agent phân loại ý định người dùng."""
        if not state.get("is_safe", True):
            return {"intent": "UNSAFE"}

        masked_query = state.get("masked_query", state.get("raw_query", ""))
        route_decision = self.router_agent.route(masked_query)
        return {
            "intent": route_decision.get("intent", "ENTITY_ADVISORY"),
            "case_id": route_decision.get("case_id"),
        }

    def _route_decision_edge(self, state: LegalAgentState) -> str:
        """Hàm điều kiện rẽ nhánh (Conditional Routing Edge)."""
        if not state.get("is_safe", True):
            return "UNSAFE"
        intent = state.get("intent", "ENTITY_ADVISORY")
        valid_intents = {
            "SOCIAL_CASE_ADVISORY",
            "DYNAMIC_DRAFT",
            "CONTRACT_AUDIT",
            "DOSSIER_CREATION",
            "INDUSTRY_LOOKUP",
            "REGISTRATION_STEPS",
            "ENTITY_ADVISORY",
        }
        return intent if intent in valid_intents else "ENTITY_ADVISORY"

    def _node_social_case(self, state: LegalAgentState) -> Dict[str, Any]:
        """Node 3A: Xử lý 4 vụ việc thực tế (Social Cases Agent)."""
        case_id = state.get("case_id") or "DEBT_COLLECTION"
        raw_response = SocialCasesKnowledgeEngine.generate_advisory_text(case_id)
        citations = []
        case_info = SOCIAL_CASES_DATA.get(case_id, {})
        for law_str in case_info.get("key_laws", []):
            citations.append({
                "law_title": law_str.split(":")[0] if ":" in law_str else law_str,
                "article": law_str,
                "header": case_info.get("title", "Tình huống pháp lý đời sống"),
                "verify_url": "https://vanban.chinhphu.vn/",
                "text_snippet": law_str,
                "full_text": case_info.get("core_doctrine", "")
            })

        return {
            "active_agent": "SocialCasesAdvisoryAgent (LangGraph)",
            "response": raw_response,
            "citations": citations,
            "action_type": "DYNAMIC_DRAFT_ACTION",
            "action_data": {"case_id": case_id},
        }

    def _node_dynamic_draft(self, state: LegalAgentState) -> Dict[str, Any]:
        """Node 3B: Kích hoạt Dynamic Smart Drafter với placeholder linh hoạt."""
        case_id = state.get("case_id") or "CUSTOM"
        raw_response = (
            "### 📝 Biểu mẫu Soạn thảo Văn bản Pháp lý Thông minh (LangGraph Smart Form):\n"
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
        return {
            "active_agent": "DynamicDocumentDrafter (LangGraph)",
            "response": raw_response,
            "citations": citations,
            "action_type": "DYNAMIC_DRAFT_ACTION",
            "action_data": {"case_id": case_id},
        }

    def _node_contract_audit(self, state: LegalAgentState) -> Dict[str, Any]:
        """Node 3C: Thẩm định hợp đồng đối kháng 2 chiều (Contract Vulnerability Scanner)."""
        masked_query = state.get("masked_query", state.get("raw_query", ""))
        scan_res = self.contract_scanner.scan(masked_query)
        citations = []
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
            "### 🛡️ Kết quả Thẩm định Rủi ro Hợp đồng (LangGraph Bilateral Audit):\n",
            f"- **Điểm An toàn Pháp lý:** `{scan_res['score']} / 100` ({scan_res['status_label']})\n",
            f"- **Số lượng vấn đề phát hiện:** `{scan_res['findings_count']}`\n\n",
            f"**Ý kiến chuyên gia thẩm định (Phân tích đối kháng 2 chiều):**\n{scan_res['ai_review']}\n\n",
            "👉 *Bạn có thể tải Báo cáo Thẩm định (.docx) hoặc chỉnh sửa trực tiếp qua công cụ bên dưới!*"
        ]
        return {
            "active_agent": "ContractVulnerabilityScanner (LangGraph)",
            "response": "".join(resp_parts),
            "citations": citations,
            "action_type": "CONTRACT_AUDIT_ACTION",
            "action_data": scan_res,
        }

    def _node_dossier(self, state: LegalAgentState) -> Dict[str, Any]:
        """Node 3D: Soạn thảo hồ sơ doanh nghiệp theo Nghị định 01/2021/NĐ-CP."""
        raw_response = (
            "### 📝 Bộ Soạn thảo Hồ sơ Doanh nghiệp Tự động (LangGraph In-Chat Canvas):\n"
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
        return {
            "active_agent": "DossierDraftingAgent (LangGraph)",
            "response": raw_response,
            "citations": citations,
            "action_type": "DOSSIER_CREATION_ACTION",
            "action_data": None,
        }

    def _node_industry_lookup(self, state: LegalAgentState) -> Dict[str, Any]:
        """Node 3E: Tra cứu ngành nghề kinh doanh và điều kiện gia nhập thị trường."""
        masked_query = state.get("masked_query", state.get("raw_query", ""))
        agent_result = self.lookup_agent.lookup(masked_query)
        return {
            "active_agent": "IndustryLookupAgent (LangGraph)",
            "response": agent_result["response"],
            "citations": agent_result.get("citations", []),
            "action_type": None,
            "action_data": None,
        }

    def _node_registration_steps(self, state: LegalAgentState) -> Dict[str, Any]:
        """Node 3F: Quy trình và danh mục hồ sơ thủ tục hành chính."""
        masked_query = state.get("masked_query", state.get("raw_query", ""))
        agent_result = self.reviewer_agent.generate_checklist(masked_query)
        return {
            "active_agent": "DocumentReviewerAgent (LangGraph)",
            "response": agent_result["response"],
            "citations": agent_result.get("citations", []),
            "action_type": None,
            "action_data": None,
        }

    def _node_entity_advisory(self, state: LegalAgentState) -> Dict[str, Any]:
        """Node 3G: RAG & Cố vấn pháp lý toàn diện."""
        masked_query = state.get("masked_query", state.get("raw_query", ""))
        agent_result = self.advisory_agent.advise(masked_query)
        return {
            "active_agent": "EntityAdvisoryAgent (LangGraph)",
            "response": agent_result["response"],
            "citations": agent_result.get("citations", []),
            "action_type": None,
            "action_data": None,
        }

    def _node_moderator(self, state: LegalAgentState) -> Dict[str, Any]:
        """Node 4: Khôi phục PII, kiểm duyệt ngôn từ và thêm Disclaimer pháp lý."""
        if not state.get("is_safe", True):
            return {
                "response": state.get("response", "Yêu cầu vi phạm chính sách bảo mật.")
            }

        intermediate_resp = state.get("response", "")
        pii_mapping = state.get("pii_mapping", {})
        unmasked_resp = self.pii_masker.unmask_text(intermediate_resp, pii_mapping)
        final_resp, _ = self.output_moderator.moderate_and_append_disclaimer(unmasked_resp)
        return {"response": final_resp}

    # ------------------ PHƯƠNG THỨC THỰC THI CHÍNH ------------------

    def process(self, raw_user_query: str) -> Dict[str, Any]:
        """
        Thực thi quy trình xử lý thông qua LangGraph StateGraph.
        """
        initial_state: LegalAgentState = {
            "raw_query": raw_user_query,
            "masked_query": "",
            "pii_mapping": {},
            "is_safe": True,
            "error": None,
            "intent": "ENTITY_ADVISORY",
            "case_id": None,
            "active_agent": "Initializing",
            "response": "",
            "citations": [],
            "action_type": None,
            "action_data": None,
        }

        final_state = self.graph.invoke(initial_state)

        return {
            "success": final_state.get("is_safe", True),
            "error": final_state.get("error"),
            "intent": final_state.get("intent"),
            "active_agent": final_state.get("active_agent"),
            "response": final_state.get("response"),
            "citations": final_state.get("citations", []),
            "action_type": final_state.get("action_type"),
            "action_data": final_state.get("action_data"),
            "masked_query": final_state.get("masked_query", ""),
            "has_pii": bool(final_state.get("pii_mapping")),
        }

    def get_mermaid_diagram(self) -> str:
        """
        Trích xuất sơ đồ cấu trúc mạng lưới đa tác nhân LangGraph định dạng Mermaid.
        """
        try:
            return self.graph.get_graph().draw_mermaid()
        except Exception:
            # Fallback nếu môi trường không render được trực tiếp
            return """graph TD
    __start__([Bắt đầu]) --> guardrail_node[🛡️ Guardrail Node: PII & Anti-Injection]
    guardrail_node --> router_node{🧭 Router Node: Phân loại Ý định}
    router_node -->|Bạo lực học đường / Đất đai / Đòi nợ / Ly hôn| social_case_node[⚖️ Social Cases Agent]
    router_node -->|Soạn thảo theo yêu cầu| dynamic_draft_node[📝 Dynamic Smart Drafter]
    router_node -->|Thẩm định hợp đồng| contract_audit_node[🛡️ Bilateral Contract Auditor]
    router_node -->|Hồ sơ thành lập DN| dossier_node[📂 Dossier Generator NĐ 01/2021]
    router_node -->|Tra cứu ngành nghề| industry_lookup_node[🔍 Industry & SQL Lookup Agent]
    router_node -->|Thủ tục hành chính| registration_steps_node[📋 Registration Steps Agent]
    router_node -->|Tư vấn chung| entity_advisory_node[📚 General Legal RAG Advisor]
    router_node -->|Vi phạm an toàn| moderator_node[⚖️ Output Moderator & Disclaimer]
    social_case_node --> moderator_node
    dynamic_draft_node --> moderator_node
    contract_audit_node --> moderator_node
    dossier_node --> moderator_node
    industry_lookup_node --> moderator_node
    registration_steps_node --> moderator_node
    entity_advisory_node --> moderator_node
    moderator_node --> __end__([Kết thúc])
"""
