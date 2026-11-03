# -*- coding: utf-8 -*-
"""
Unit tests for CitizenAccountManager and OnboardingTutorial
"""

import unittest
from src.security.citizen_account_manager import CitizenAccountManager
from src.security.onboarding_tutorial import OnboardingTutorial


class TestAccountAndTutorial(unittest.TestCase):
    def test_demo_personas_loaded(self):
        mgr = CitizenAccountManager()
        bac_ba = mgr.get_demo_persona("bac_ba")
        self.assertIsNotNone(bac_ba)
        self.assertEqual(bac_ba["name"], "Bác Ba (Nông dân - Tiền Giang)")
        self.assertIn("initial_prompt", bac_ba)

        chi_lan = mgr.get_demo_persona("chi_lan")
        self.assertIsNotNone(chi_lan)
        self.assertIn("Tín Dụng Đen", chi_lan["category"])

        anh_hoang = mgr.get_demo_persona("anh_hoang")
        self.assertIsNotNone(anh_hoang)
        self.assertIn("Ly Hôn", anh_hoang["category"])

        cu_sau = mgr.get_demo_persona("cu_sau")
        self.assertIsNotNone(cu_sau)
        self.assertIn("Thừa Kế", cu_sau["category"])

    def test_default_guest(self):
        guest = CitizenAccountManager.get_default_guest()
        self.assertEqual(guest["id"], "GUEST_CITIZEN")
        self.assertEqual(guest["name"], "Công Dân Vãng Lai")

    def test_save_account(self):
        mgr = CitizenAccountManager()
        acc = mgr.save_account("TEST_USER_01", "Nguyễn Văn Test", "0909999999", "Ghi chú vụ việc")
        self.assertEqual(acc["name"], "Nguyễn Văn Test")
        self.assertEqual(acc["phone"], "0909999999")

    def test_tutorial_steps(self):
        steps = OnboardingTutorial.get_tutorial_steps()
        self.assertEqual(len(steps), 4)
        self.assertEqual(steps[0]["step"], 1)
        self.assertIn("Demo", steps[0]["title"])


if __name__ == "__main__":
    unittest.main()
