#!/usr/bin/env python3
"""
tests/test_sentinel.py
Unit tests for the Proactive Architectural Sentinel & Scalability Guard (scripts/sentinel.py).
"""

import unittest
from pathlib import Path
import sys

# Ensure scripts directory is on path
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT / "scripts"))

from sentinel import ArchitecturalSentinel, P0, P1, P2

class TestArchitecturalSentinel(unittest.TestCase):
    def setUp(self):
        self.sentinel = ArchitecturalSentinel(WORKSPACE_ROOT)

    def test_unbounded_query_detection(self):
        vulnerable_sql = "SELECT id, email, created_at FROM users WHERE status = 'active';"
        findings = self.sentinel.audit_scalability(vulnerable_sql, "src/controllers/user.py")
        self.assertTrue(any(f.severity == P1 and "unbounded query" in f.message.lower() for f in findings))

    def test_bounded_query_passes(self):
        safe_sql = "SELECT id, email FROM users WHERE status = 'active' LIMIT 50;"
        findings = self.sentinel.audit_scalability(safe_sql, "src/controllers/user.py")
        self.assertEqual(len(findings), 0)

    def test_orm_bulk_fetch_detection(self):
        orm_code = "users = User::all();"
        findings = self.sentinel.audit_scalability(orm_code, "app/Http/Controllers/UserController.php")
        self.assertTrue(any(f.severity == P1 and "bulk fetch" in f.message.lower() for f in findings))

    def test_n_plus_one_detection(self):
        n_plus_one_code = """
        for user_id in user_ids:
            profile = db.findById(user_id)
            print(profile)
        """
        findings = self.sentinel.audit_scalability(n_plus_one_code, "src/services/billing.ts")
        self.assertTrue(any(f.severity == P0 and "n+1" in f.message.lower() for f in findings))

    def test_missing_index_in_migration_detection(self):
        migration_code = "$table->foreignId('organization_id');\n$table->timestamp('expires_at');"
        findings = self.sentinel.audit_scalability(migration_code, "database/migrations/create_tokens_table.php")
        self.assertTrue(len(findings) >= 1)
        self.assertTrue(any("index" in f.message.lower() for f in findings))

    def test_parsimony_single_method_class_detection(self):
        bloated_code = """
class PriceFormatter:
    def format_price(self, amount):
        return f"${amount:.2f}"
"""
        findings = self.sentinel.audit_parsimony(bloated_code, "src/utils/formatter.py")
        self.assertTrue(any(f.severity == P2 and "single-method" in f.message.lower() for f in findings))

    def test_parsimony_multi_method_class_passes(self):
        clean_code = """
class CurrencyExchange:
    def convert(self, amount, rate):
        return amount * rate
    def validate_rate(self, rate):
        return rate > 0
"""
        findings = self.sentinel.audit_parsimony(clean_code, "src/utils/exchange.py")
        self.assertEqual(len(findings), 0)

    def test_hostile_error_leak_detection(self):
        bad_response = "res.status(500).json({ error: 'Internal Server Error', stack: err.stack });"
        findings = self.sentinel.audit_product_empathy(bad_response, "src/api/routes.ts")
        self.assertTrue(any(f.severity == P1 and "leak" in f.message.lower() for f in findings))

    def test_inaccessible_button_detection(self):
        bad_button = "<button className='btn'>Click here</button>"
        findings = self.sentinel.audit_product_empathy(bad_button, "src/components/Nav.tsx")
        self.assertTrue(any(f.severity == P2 and "aria-label" in f.message.lower() for f in findings))

    def test_accessible_button_passes(self):
        good_button = "<button aria-label='Proceed to checkout' className='btn'>Click here</button>"
        findings = self.sentinel.audit_product_empathy(good_button, "src/components/Nav.tsx")
        self.assertEqual(len(findings), 0)

    def test_full_clean_scan_report(self):
        self.sentinel.clear()
        report = self.sentinel.format_report()
        self.assertIn("[PASS] Zero architectural or scalability regressions detected", report)

if __name__ == "__main__":
    unittest.main()
