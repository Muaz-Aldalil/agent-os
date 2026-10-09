#!/usr/bin/env python3
"""
Unit tests for the Local Adversarial Diff Reviewer (scripts/diff_reviewer.py).
Validates diff parsing, P0/P1/P2 severity triage, and report generation.
"""

import unittest
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from diff_reviewer import (
    parse_diff_files,
    map_guard_to_severity,
    generate_report,
    Finding,
    GuardViolation
)

class TestDiffReviewer(unittest.TestCase):

    def test_parse_diff_files(self):
        sample_diff = """diff --git a/src/actions.ts b/src/actions.ts
index abc..def 100644
--- a/src/actions.ts
+++ b/src/actions.ts
@@ -10,3 +10,4 @@ function existing() {
 }
+export async function newAction() {
+    return true;
+}
"""
        parsed = parse_diff_files(sample_diff)
        self.assertIn("src/actions.ts", parsed)
        added_lines = parsed["src/actions.ts"]
        self.assertEqual(len(added_lines), 3)
        self.assertEqual(added_lines[0][0], 11)
        self.assertEqual(added_lines[0][1], "export async function newAction() {")

    def test_severity_mapping(self):
        v_p0 = GuardViolation("next-server-action-guard", "AUTH_DERIVATION_VIOLATION", 10, "msg")
        v_p1 = GuardViolation("pest-security-guard", "DANGEROUS_FUNCTION_FORBIDDEN", 20, "msg")
        v_p2 = GuardViolation("clean-code-guard", "MUTABLE_DEFAULT_ARGUMENT", 30, "msg")

        self.assertEqual(map_guard_to_severity(v_p0), "P0")
        self.assertEqual(map_guard_to_severity(v_p1), "P1")
        self.assertEqual(map_guard_to_severity(v_p2), "P2")

    def test_report_generation_with_findings(self):
        findings = [
            Finding("P0", "src/auth.ts", 15, "AUTH_DERIVATION_VIOLATION", "Payload ID accepted", "export async func"),
            Finding("P1", "src/legacy.php", 1, "STRICT_TYPES_REQUIRED", "Missing declare strict")
        ]
        report = generate_report(findings)
        self.assertIn("P0 (Blocking): 1", report)
        self.assertIn("P1 (Severe): 1", report)
        self.assertIn("VERDICT: [CAUTION]", report)

    def test_clean_report_generation(self):
        report = generate_report([])
        self.assertIn("Zero adversarial findings detected", report)
        self.assertIn("Working tree is clean", report)

if __name__ == "__main__":
    unittest.main()
