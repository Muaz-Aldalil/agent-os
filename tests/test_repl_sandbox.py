#!/usr/bin/env python3
"""
Unit tests for the In-Memory Micro-Sandbox & Hypothesis REPL (scripts/repl_sandbox.py).
Validates isolated execution of Python, SQL, and Regex micro-experiments.
"""

import unittest
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from repl_sandbox import (
    run_python,
    run_sql,
    run_regex,
    format_sql_table
)

class TestReplSandbox(unittest.TestCase):

    def test_python_eval_expression(self):
        res = run_python("sum([1, 2, 3, 4, 5])")
        self.assertEqual(res["status"], "SUCCESS")
        self.assertEqual(res["result"], 15)
        self.assertLess(res["elapsed_ms"], 1000)

    def test_python_multiline_block(self):
        code = """
total = 0
for i in range(10):
    total += i
result = total
"""
        res = run_python(code)
        self.assertEqual(res["status"], "SUCCESS")
        self.assertEqual(res["result"], 45)

    def test_python_runtime_error_handled(self):
        res = run_python("1 / 0")
        self.assertEqual(res["status"], "ERROR")
        self.assertIn("ZeroDivisionError", res["error"])

    def test_sql_in_memory_execution(self):
        sql = """
CREATE TABLE ledger (id INT, amount INT);
INSERT INTO ledger VALUES (1, 1000), (2, 2500);
SELECT sum(amount) FROM ledger;
"""
        res = run_sql(sql)
        self.assertEqual(res["status"], "SUCCESS")
        self.assertEqual(res["queries_executed"], 3)
        select_res = res["results"][2]
        self.assertEqual(select_res["rows"][0][0], 3500)

    def test_regex_match_and_substitute(self):
        res = run_regex(r"(?P<year>\d{4})-(?P<month>\d{2})", "Date: 2026-10-08", "[YEAR-MONTH]")
        self.assertEqual(res["status"], "SUCCESS")
        self.assertEqual(res["match_count"], 1)
        self.assertEqual(res["matches"][0]["groupdict"], {"year": "2026", "month": "10"})
        self.assertEqual(res["replaced_text"], "Date: [YEAR-MONTH]-08")

if __name__ == "__main__":
    unittest.main()
