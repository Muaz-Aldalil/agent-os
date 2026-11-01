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
import tracer
import snapshot
from preflight import run_preflight
from code_graph import extract_python_symbols, find_symbol
from tracer import start_investigation, add_hypothesis, conclude_hypothesis, load_traces
from snapshot import freeze_session, restore_session


class Test100XPowerSuite(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self.temp_dir.name)
        self._orig_trace = tracer.TRACE_FILE
        self._orig_snap_json = snapshot.SNAPSHOT_JSON
        self._orig_snap_md = snapshot.SNAPSHOT_MD

        tracer.TRACE_FILE = self.tmp_path / ".agent_trace.json"
        snapshot.SNAPSHOT_JSON = self.tmp_path / ".agent_snapshot.json"
        snapshot.SNAPSHOT_MD = self.tmp_path / "SESSION_SNAPSHOT.md"

        if "scripts.tracer" in sys.modules:
            sys.modules["scripts.tracer"].TRACE_FILE = tracer.TRACE_FILE
        if "scripts.snapshot" in sys.modules:
            sys.modules["scripts.snapshot"].SNAPSHOT_JSON = snapshot.SNAPSHOT_JSON
            sys.modules["scripts.snapshot"].SNAPSHOT_MD = snapshot.SNAPSHOT_MD

    def tearDown(self):
        tracer.TRACE_FILE = self._orig_trace
        snapshot.SNAPSHOT_JSON = self._orig_snap_json
        snapshot.SNAPSHOT_MD = self._orig_snap_md
        if "scripts.tracer" in sys.modules:
            sys.modules["scripts.tracer"].TRACE_FILE = self._orig_trace
        if "scripts.snapshot" in sys.modules:
            sys.modules["scripts.snapshot"].SNAPSHOT_JSON = self._orig_snap_json
            sys.modules["scripts.snapshot"].SNAPSHOT_MD = self._orig_snap_md
        self.temp_dir.cleanup()

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
        tmp_file = self.tmp_path / "sample_mod.py"
        tmp_file.write_text(sample_code, encoding="utf-8")
        symbols = extract_python_symbols(tmp_file)
        names = [s.name for s in symbols]
        self.assertIn("DataProcessor", names)
        self.assertIn("DataProcessor.process_item", names)
        self.assertIn("standalone_helper", names)
        helper = next(s for s in symbols if s.name == "standalone_helper")
        self.assertEqual(helper.docstring, "Helper docstring.")

    def test_code_graph_find_existing_symbol(self):
        matches = find_symbol("evaluate_command")
        self.assertGreaterEqual(len(matches), 1)
        self.assertEqual(matches[0].name, "evaluate_command")

    def test_code_graph_invalid_syntax_returns_empty(self):
        bad_file = self.tmp_path / "broken_syntax.py"
        bad_file.write_text("def broken_func(:\n    pass\n", encoding="utf-8")
        symbols = extract_python_symbols(bad_file)
        self.assertEqual(symbols, [])
        self.assertFalse(bool(symbols))

    def test_tracer_scientific_cycle(self):
        start_investigation("Unit Test Investigation")
        add_hypothesis("Testing tracer cycle", prediction="Cycle will succeed")
        conclude_hypothesis("CONFIRMED", notes="Verified by unit test")
        data = load_traces()
        inv = data.get("current_investigation")
        self.assertIsNotNone(inv)
        self.assertEqual(inv["title"], "Unit Test Investigation")
        self.assertEqual(inv["hypotheses"][-1]["verdict"], "CONFIRMED")

    def test_tracer_rejects_invalid_verdict(self):
        start_investigation("Negative Test Investigation")
        add_hypothesis("Invalid verdict check")
        conclude_hypothesis("MAYBE_LATER", notes="Should be rejected")
        data = load_traces()
        inv = data.get("current_investigation")
        self.assertIsNone(inv["hypotheses"][-1]["verdict"])
        self.assertNotEqual(inv["hypotheses"][-1]["status"], "CONCLUDED")

    def test_snapshot_restore_when_missing_returns_empty(self):
        restored = restore_session()
        self.assertEqual(restored, {})
        self.assertFalse(bool(restored))

    def test_snapshot_freeze_and_json(self):
        snap = freeze_session("Unit Test Freeze")
        self.assertIn("label", snap)
        self.assertEqual(snap["label"], "Unit Test Freeze")
        self.assertIn("git", snap)
        self.assertIn("handover", snap)

    def test_snapshot_handover_fields(self):
        snap = freeze_session(
            label="Handover Test",
            objective="Verify 60-70% context handover",
            decisions=["Keep all 76 skills"],
            rejected=["Delete speckit skills"],
            next_step="Run test suite -> verify: exit code 0",
        )
        handover = snap["handover"]
        self.assertEqual(handover["objective"], "Verify 60-70% context handover")
        self.assertEqual(handover["decisions"], ["Keep all 76 skills"])
        self.assertEqual(handover["rejected"], ["Delete speckit skills"])
        self.assertIn("transcript_kb", handover)
        self.assertIn("transcript_steps", handover)
        restored = restore_session()
        self.assertEqual(restored["handover"]["objective"], "Verify 60-70% context handover")


if __name__ == "__main__":
    unittest.main()
