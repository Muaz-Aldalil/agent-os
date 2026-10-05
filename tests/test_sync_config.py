#!/usr/bin/env python3
"""
Unit tests for sync_config.py dual config synchronization engine.
"""

import sys
import os
import unittest
from pathlib import Path
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))
from sync_config import file_hash, scan_sync_drift, apply_sync

class TestSyncConfig(unittest.TestCase):

    def test_file_hash_deterministic(self):
        with tempfile.NamedTemporaryFile("w+", delete=False, encoding="utf-8") as tmp:
            tmp.write("antigravity-agent-os")
            tmp_path = Path(tmp.name)

        try:
            h1 = file_hash(tmp_path)
            h2 = file_hash(tmp_path)
            self.assertEqual(h1, h2)
            self.assertEqual(len(h1), 64)
        finally:
            tmp_path.unlink()

    def test_scan_sync_drift_runs_cleanly(self):
        drift = scan_sync_drift()
        self.assertIsInstance(drift, list)

    def test_apply_sync_copies_file(self):
        with tempfile.TemporaryDirectory() as src_dir, tempfile.TemporaryDirectory() as tgt_dir:
            src_file = Path(src_dir) / "test.txt"
            tgt_file = Path(tgt_dir) / "test.txt"
            src_file.write_text("sync-test-content", encoding="utf-8")

            item = {
                "rel_path": "test.txt",
                "status": "MISSING_IN_GLOBAL",
                "source": src_file,
                "target": tgt_file
            }
            applied = apply_sync([item])
            self.assertEqual(applied, 1)
            self.assertTrue(tgt_file.exists())
            self.assertEqual(tgt_file.read_text(encoding="utf-8"), "sync-test-content")

if __name__ == "__main__":
    unittest.main()
