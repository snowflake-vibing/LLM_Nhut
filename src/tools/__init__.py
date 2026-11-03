"""
Web Search, External Tools & Contract Scanner Module
Hỗ trợ tìm kiếm mở rộng Internet và thẩm định lỗ hổng hợp đồng (Version 2.0).
"""

from .web_search_tool import search_web_legal, hybrid_industry_search
from .contract_scanner import ContractVulnerabilityScanner
from .social_cases_knowledge import SocialCasesKnowledgeEngine, SOCIAL_CASES_DATA
from .citizen_legal_tools import CitizenLegalTools
from .multimodal_evidence_parser import MultimodalEvidenceParser
from .instant_petition_generator import InstantPetitionGenerator
from .litigation_simulator import LegalLitigationSimulator
from .voice_narrator import VoiceNarrator
from .litigation_dossier_generator import LitigationDossierGenerator
from .citizen_wizard import CitizenDiagnosticFunnel
from .plain_legal_glossary import PlainLegalGlossary
from .deterministic_rules import DeterministicLegalRules
from .chaotic_citizen_tests import ChaoticCitizenTestSuite

__all__ = [
    "search_web_legal",
    "hybrid_industry_search",
    "ContractVulnerabilityScanner",
    "SocialCasesKnowledgeEngine",
    "SOCIAL_CASES_DATA",
    "CitizenLegalTools",
    "MultimodalEvidenceParser",
    "InstantPetitionGenerator",
    "LegalLitigationSimulator",
    "VoiceNarrator",
    "LitigationDossierGenerator",
    "CitizenDiagnosticFunnel",
    "PlainLegalGlossary",
    "DeterministicLegalRules",
    "ChaoticCitizenTestSuite",
]
