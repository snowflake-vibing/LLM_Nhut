"""
Multi-Agent Orchestrator & Workflow
Điều phối toàn bộ quy trình làm việc giữa các Agent, tích hợp Lớp bảo mật
Guardrails (PII Masking & Anti-Injection) và Model Switcher.
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


class LegalMultiAgentWorkflow:
    """
    Hệ thống điều phối Đa tác nhân (Multi-Agent System) cho LegalTech SME Assistant.
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

    def process(self, raw_user_query: str) -> Dict[str, Any]:
        """
        Quy trình xử lý hoàn chỉnh từ lúc nhận input đến khi trả lời:
        1. Guardrail 1: Kiểm tra an toàn Prompt Injection & Ý định trái luật.
        2. Guardrail 2: Masking dữ liệu nhạy cảm PII (CCCD, SĐT, Email).
        3. Router Agent: Xác định ý định và Agent chuyên trách.
        4. Specialized Agent: Thực thi tác vụ (RAG hoặc SQL Tool).
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
            }

        # BƯỚC 2: Che giấu thông tin cá nhân (PII Masking)
        masked_query, pii_mapping = self.pii_masker.mask_text(raw_user_query)

        # BƯỚC 3: Router Agent điều hướng
        route_decision = self.router_agent.route(masked_query)
        intent = route_decision.get("intent", "ENTITY_ADVISORY")

        # BƯỚC 4: Gọi Agent chuyên trách
        citations = []
        if intent == "INDUSTRY_LOOKUP":
            agent_result = self.lookup_agent.lookup(masked_query)
            active_agent = "IndustryLookupAgent"
            citations = agent_result.get("citations", [])
        elif intent == "REGISTRATION_STEPS":
            agent_result = self.reviewer_agent.generate_checklist(masked_query)
            active_agent = "DocumentReviewerAgent"
            citations = agent_result.get("citations", [])
        else:
            agent_result = self.advisory_agent.advise(masked_query)
            active_agent = "EntityAdvisoryAgent"
            citations = agent_result.get("citations", [])

        # BƯỚC 5: Khôi phục PII & Kiểm duyệt đầu ra
        raw_response = agent_result["response"]
        unmasked_response = self.pii_masker.unmask_text(raw_response, pii_mapping)
        final_response, is_approved = self.output_moderator.moderate_and_append_disclaimer(unmasked_response)

        return {
            "success": True,
            "intent": intent,
            "active_agent": active_agent,
            "response": final_response,
            "citations": citations,
            "masked_query": masked_query,
            "has_pii": bool(pii_mapping),
        }
