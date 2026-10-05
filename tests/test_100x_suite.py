#!/usr/bin/env python3
"""
Unit tests for the 100X Power Suite:
- preflight.py (assumption validation & flight clearance)
- code_graph.py (AST symbol extraction & instant lookup)
- tracer.py (scientific debugging & hypothesis ledger)
- snapshot.py (cognitive memory freeze & resume)
"""

import sys
import os
import unittest
from pathlib import Path
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))
from preflight import run_preflight
from code_graph import extract_python_symbols, find_symbol
from tracer import start_investigation, add_hypothesis, conclude_hypothesis, load_traces
from snapshot import freeze_session, restore_session

class Test100XPowerSuite(unittest.TestCase):

    def test_preflight_scoring(self):
        score, items = run_preflight()
        self.assertGreaterEqual(score, 70)
        self.assertGreater(len(items), 5)

    def test_code_graph_symbol_extraction(self):
        sample_code = """
class DataProcessor:
    def process_item(self, item):
        return item * 2

def standalone_helper(x, y):
    \"\"\"Helper docstring.\"\"\"
    return x + y
"""
        with tempfile.NamedTemporaryFile("w+", suffix=".py", delete=False, encoding="utf-8") as tmp:
            tmp.write(sample_code)
            tmp_path = Path(tmp.name)

        try:
            symbols = extract_python_symbols(tmp_path)
            names = [s.name for s in symbols]
            self.assertIn("DataProcessor", names)
            self.assertIn("DataProcessor.process_item", names)
            self.assertIn("standalone_helper", names)
            helper = next(s for s in symbols if s.name == "standalone_helper")
            self.assertEqual(helper.docstring, "Helper docstring.")
        finally:
            tmp_path.unlink()

    def test_code_graph_find_existing_symbol(self):
        matches = find_symbol("evaluate_command")
        self.assertGreaterEqual(len(matches), 1)
        self.assertEqual(matches[0].name, "evaluate_command")

    def test_tracer_scientific_cycle(self):
        start_investigation("Unit Test Investigation")
        add_hypothesis("Testing tracer cycle", prediction="Cycle will succeed")
        conclude_hypothesis("CONFIRMED", notes="Verified by unit test")
        data = load_traces()
        inv = data.get("current_investigation")
        self.assertIsNotNone(inv)
        self.assertEqual(inv["title"], "Unit Test Investigation")
        self.assertEqual(inv["hypotheses"][-1]["verdict"], "CONFIRMED")

    def test_snapshot_freeze_and_json(self):
        snap = freeze_session("Unit Test Freeze")
        self.assertIn("label", snap)
        self.assertEqual(snap["label"], "Unit Test Freeze")
        self.assertIn("git", snap)

if __name__ == "__main__":
    unittest.main()
