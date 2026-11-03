# -*- coding: utf-8 -*-
"""
Unit tests for the 4 Breakthrough Legal Tech Modules:
1. UsuryTrapDetector
2. CourtJurisdictionGuide
3. DivorceSettlementCalculator
4. InheritanceDistributionEngine
"""

import unittest
from src.tools.usury_trap_detector import UsuryTrapDetector
from src.tools.court_jurisdiction_guide import CourtJurisdictionGuide
from src.tools.divorce_settlement_calculator import DivorceSettlementCalculator
from src.tools.inheritance_distribution_engine import InheritanceDistributionEngine


class TestBreakthroughModules(unittest.TestCase):
    def test_usury_trap_detector_criminal(self):
        res = UsuryTrapDetector.analyze_loan(
            principal_amount=20_000_000,
            actual_received_amount=16_000_000,
            term_days=50,
            periodic_interest_fee=100_000,
            fee_cycle_days=1,
            hidden_fees=500_000
        )
        self.assertGreater(res["annualized_percent"], 100.0)
        self.assertTrue(res["is_criminal_rate"])
        self.assertGreater(res["excess_interest_amount"], 0)
        self.assertIn("DỪNG NGAY", res["recommendations"][0])

        template = UsuryTrapDetector.generate_criminal_denunciation_template(
            res,
            {"full_name": "Nguyễn Văn Nhựt", "birth_year": "1995", "cccd": "079095xxxxxx", "address": "TP.HCM", "phone": "0901234567"},
            {"name": "Chủ app vay nặng lãi", "contact": "0988888888", "address": "Quận 1", "police_dept": "Công an Quận 1"}
        )
        self.assertIn("ĐƠN TỐ GIÁC TỘI PHẠM", template)
        self.assertIn("Điều 201 Bộ luật Hình sự 2015", template)

    def test_court_jurisdiction_guide_land(self):
        res = CourtJurisdictionGuide.resolve_jurisdiction_and_checklist(
            dispute_type="LAND_DISPUTE",
            province="HỒ CHÍ MINH",
            district="QUẬN 1"
        )
        self.assertIn("Tòa án nhân dân Quận 1", res["target_court_name"])
        self.assertTrue(res["mandatory_pre_litigation"])
        self.assertIn("Hòa giải tại UBND xã/phường", res["pre_litigation_notice"])
        self.assertGreaterEqual(len(res["required_dossier"]), 5)

    def test_divorce_settlement_calculator(self):
        children = [{"name": "Bé Bi", "age_months": 24}]
        res = DivorceSettlementCalculator.calculate_settlement(
            husband_separate_assets=100_000_000,
            wife_separate_assets=50_000_000,
            common_assets_value=2_000_000_000,
            common_debts_value=200_000_000,
            wife_is_homemaker=True,
            children=children,
            non_custodial_parent_income=20_000_000
        )
        self.assertEqual(res["net_common_assets"], 1_800_000_000)
        self.assertEqual(res["wife_share_common"], 900_000_000)
        self.assertEqual(res["husband_share_common"], 900_000_000)
        self.assertEqual(res["custody_analysis"][0]["recommended_custodian"], "Người Mẹ")
        self.assertGreater(res["monthly_child_support_per_child"], 0)

    def test_inheritance_distribution_engine(self):
        res = InheritanceDistributionEngine.calculate_statutory_inheritance(
            total_estate_value=3_000_000_000,
            funeral_expenses=0,
            unpaid_debts=300_000_000,
            has_spouse=True,
            parents_alive_count=1,
            children_count=2,
            minor_children_count=1
        )
        self.assertEqual(res["net_estate_value"], 2_700_000_000)
        self.assertEqual(res["heirs_rank_1_total"], 4)
        self.assertEqual(res["legal_share_per_person"], 675_000_000)
        self.assertEqual(res["mandatory_protection_share_2_thirds"], 450_000_000)


if __name__ == "__main__":
    unittest.main()
