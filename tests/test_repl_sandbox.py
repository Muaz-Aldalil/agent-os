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

    def test_sandbox_blocks_open_and_filesystem_access(self):
        res_open = run_python("open('.env').read()")
        self.assertEqual(res_open["status"], "ERROR")
        self.assertIn("SecurityViolation", res_open["error"])

        res_path = run_python("Path('.').resolve()")
        self.assertEqual(res_path["status"], "ERROR")
        self.assertIn("SecurityViolation", res_path["error"])

    def test_sandbox_blocks_imports_and_dunder_escape(self):
        res_imp = run_python("__import__('os').system('echo pwned')")
        self.assertEqual(res_imp["status"], "ERROR")
        self.assertIn("SecurityViolation", res_imp["error"])

        res_stmt = run_python("import os\nresult = os.getcwd()")
        self.assertEqual(res_stmt["status"], "ERROR")
        self.assertIn("SecurityViolation", res_stmt["error"])

        res_dunder = run_python("().__class__.__base__.__subclasses__()")
        self.assertEqual(res_dunder["status"], "ERROR")
        self.assertIn("SecurityViolation", res_dunder["error"])

    def test_sandbox_enforces_execution_timeout(self):
        res = run_python("while True:\n    pass", timeout_seconds=0.2)
        self.assertEqual(res["status"], "ERROR")
        self.assertIn("TimeoutError", res["error"])

    def test_sandbox_blocks_single_line_cpu_and_memory_bombs(self):
        # Single-line comprehension loop must be interrupted by opcode-level trace timeout
        res_comp = run_python("sum(i * i for i in range(9_000_000))", timeout_seconds=0.05)
        self.assertEqual(res_comp["status"], "ERROR")
        self.assertIn("TimeoutError", res_comp["error"])

        # Astronomical exponentiation or huge range allocation blocked at AST level
        res_pow = run_python("10 ** 100000")
        self.assertEqual(res_pow["status"], "ERROR")
        self.assertIn("SecurityViolation", res_pow["error"])

        res_range = run_python("len(list(range(100_000_000)))")
        self.assertEqual(res_range["status"], "ERROR")
        self.assertIn("SecurityViolation", res_range["error"])

    def test_sql_blocks_attach_database_disk_write(self):
        res = run_sql("ATTACH DATABASE 'pwned_disk.db' AS pwn;")
        self.assertEqual(res["status"], "ERROR")
        self.assertFalse(Path("pwned_disk.db").exists())


if __name__ == "__main__":
    unittest.main()
