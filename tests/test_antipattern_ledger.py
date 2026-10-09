#!/usr/bin/env python3
"""
tests/test_antipattern_ledger.py
Unit tests for the Anti-Pattern and Post-Mortem Ledger engine.
"""

import unittest
from scripts.antipattern_ledger import load_ledger, scan_text, scan_diff

class TestAntipatternLedger(unittest.TestCase):
    def test_load_ledger_contains_defaults(self):
        ledger = load_ledger()
        self.assertGreaterEqual(len(ledger), 3)
        ids = [item["id"] for item in ledger]
        self.assertIn("AP-001", ids)

    def test_scan_text_flags_raw_sql_concatenation(self):
        bad_code = """
def get_user(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    db.raw(query)
"""
        violations = scan_text(bad_code, "test_file.py")
        self.assertGreater(len(violations), 0)
        self.assertTrue(any(v["id"] == "AP-001" for v in violations))

    def test_scan_diff_flags_mutable_default(self):
        diff = """diff --git a/service.py b/service.py
--- a/service.py
+++ b/service.py
@@ -1,3 +1,4 @@
+def append_record(record, storage=[]):
"""
        violations = scan_diff(diff)
        self.assertGreater(len(violations), 0)
        self.assertTrue(any(v["id"] == "AP-003" for v in violations))

    def test_clean_code_passes_scan(self):
        clean_code = """
def append_record(record, storage=None):
    if storage is None:
        storage = []
    storage.append(record)
    return storage
"""
        violations = scan_text(clean_code, "clean.py")
        self.assertEqual(len(violations), 0)

if __name__ == "__main__":
    unittest.main()
