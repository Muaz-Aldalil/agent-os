#!/usr/bin/env python3
"""
tests/test_scope_guard.py
Unit tests for the Scope Bounding and Blast-Radius Contract engine.
"""

import unittest
from pathlib import Path
from scripts.scope_guard import (
    set_scope,
    get_scope,
    clear_scope,
    check_scope,
    SCOPE_FILE
)

class TestScopeGuard(unittest.TestCase):
    def setUp(self):
        clear_scope()

    def tearDown(self):
        clear_scope()

    def test_set_and_get_scope(self):
        res = set_scope("Fix Auth", ["src/auth.ts", "tests/test_auth.ts"], max_lines=50)
        self.assertEqual(res["task"], "Fix Auth")
        self.assertEqual(res["max_lines"], 50)
        self.assertTrue(SCOPE_FILE.is_file())

        loaded = get_scope()
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded["task"], "Fix Auth")

    def test_check_scope_passes_within_permitted(self):
        set_scope("Fix Auth", ["src/auth.ts", "tests/test_auth.ts"], max_lines=100)
        diff = """diff --git a/src/auth.ts b/src/auth.ts
--- a/src/auth.ts
+++ b/src/auth.ts
@@ -1,3 +1,4 @@
+const token = '123';
"""
        res = check_scope(diff)
        self.assertTrue(res["active"])
        self.assertTrue(res["in_scope"])
        self.assertEqual(len(res["violations"]), 0)
        self.assertEqual(res["total_lines"], 1)

    def test_check_scope_flags_unauthorized_file(self):
        set_scope("Fix Auth", ["src/auth.ts"], max_lines=100)
        diff = """diff --git a/src/auth.ts b/src/auth.ts
--- a/src/auth.ts
+++ b/src/auth.ts
@@ -1,3 +1,4 @@
+const token = '123';
diff --git a/src/billing.ts b/src/billing.ts
--- a/src/billing.ts
+++ b/src/billing.ts
@@ -1,3 +1,4 @@
+const price = 99;
"""
        res = check_scope(diff)
        self.assertTrue(res["active"])
        self.assertFalse(res["in_scope"])
        self.assertIn("src/billing.ts", res["violations"])

    def test_check_scope_flags_line_budget_exceeded(self):
        set_scope("Fix Auth", ["src/auth.ts"], max_lines=2)
        diff = """diff --git a/src/auth.ts b/src/auth.ts
--- a/src/auth.ts
+++ b/src/auth.ts
@@ -1,3 +1,6 @@
+line 1
+line 2
+line 3
"""
        res = check_scope(diff)
        self.assertTrue(res["active"])
        self.assertFalse(res["in_scope"])
        self.assertTrue(res["line_limit_exceeded"])

if __name__ == "__main__":
    unittest.main()
