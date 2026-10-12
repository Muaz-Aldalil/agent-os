#!/usr/bin/env python3
"""
tests/test_bandwidth_guard.py
Unit tests for the Data-Saver & Bandwidth Optimization Engine.
"""

import unittest
import tempfile
import shutil
import json
from pathlib import Path
from scripts.bandwidth_guard import BandwidthGuard, DATA_SAVER_PROFILE

class TestBandwidthGuard(unittest.TestCase):

    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.settings_file = self.test_dir / "settings.json"

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_detects_unoptimized_settings(self):
        self.settings_file.write_text("{}", encoding="utf-8")
        guard = BandwidthGuard(self.settings_file)
        status = guard.get_status()

        self.assertFalse(status["editor.inlineSuggest.enabled"]["active"])
        self.assertFalse(status["git.autofetch"]["active"])
        self.assertFalse(status["telemetry.telemetryLevel"]["active"])

    def test_applies_data_saver_profile_and_creates_backup(self):
        self.settings_file.write_text(json.dumps({"editor.tabSize": 2}), encoding="utf-8")
        guard = BandwidthGuard(self.settings_file)

        success, count = guard.apply_profile()
        self.assertTrue(success)
        self.assertGreater(count, 0)

        # Verify backup exists
        backup_file = self.settings_file.with_suffix(".json.backup")
        self.assertTrue(backup_file.exists())
        self.assertIn("editor.tabSize", backup_file.read_text(encoding="utf-8"))

        # Verify all settings applied
        status = guard.get_status()
        for k, v in status.items():
            self.assertTrue(v["active"], f"Setting {k} should be active")

    def test_restores_from_backup(self):
        self.settings_file.write_text(json.dumps({"original": True}), encoding="utf-8")
        guard = BandwidthGuard(self.settings_file)
        guard.apply_profile()

        self.assertIn("telemetry.telemetryLevel", guard.read_settings())

        restored = guard.restore_backup()
        self.assertTrue(restored)
        data = guard.read_settings()
        self.assertTrue(data.get("original"))
        self.assertNotIn("telemetry.telemetryLevel", data)

if __name__ == "__main__":
    unittest.main()
