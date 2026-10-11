#!/usr/bin/env python3
"""
tests/test_adr_enforcer.py
Unit tests for Architecture-as-Code and ADR enforcement engine.
"""

import unittest
from scripts.adr_enforcer import parse_adrs_from_decisions, audit_all_adrs, EXECUTABLE_ADR_MAP

class TestADREnforcer(unittest.TestCase):
    def test_parse_adrs_finds_ratified_records(self):
        adrs = parse_adrs_from_decisions()
        self.assertGreater(len(adrs), 10)
        ids = [a["id"] for a in adrs]
        self.assertIn("ADR-001", ids)
        self.assertIn("ADR-023", ids)
        self.assertIn("ADR-024", ids)
        self.assertIn("ADR-029", ids)

    def test_audit_all_adrs_passes_active_invariants(self):
        res = audit_all_adrs()
        self.assertGreater(res["total_adrs"], 0)
        self.assertGreater(res["enforced_adrs"], 5)
        self.assertEqual(res["failed_enforcements"], 0, "No executable ADR assertions should fail")
        self.assertTrue(res["coverage_percent"] > 0)

    def test_individual_adr_checkers(self):
        for adr_id, checker in EXECUTABLE_ADR_MAP.items():
            check_res = checker()
            self.assertTrue(check_res["passed"], f"Assertion for {adr_id} failed: {check_res.get('message')}")

if __name__ == "__main__":
    unittest.main()
