#!/usr/bin/env python3
"""
Unit tests for doctor.py diagnostic and self-healing engine.
"""

import sys
import os
import unittest
from pathlib import Path
import tempfile
import shutil

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))
from doctor import (
    check_stale_git_locks,
    check_nested_git_submodules,
    check_runtime_binaries,
    check_required_artifacts,
    run_diagnostics
)

class TestDoctorDiagnostics(unittest.TestCase):

    def test_runtime_binaries_pass(self):
        checks = check_runtime_binaries()
        self.assertGreaterEqual(len(checks), 2)
        py_check = next(c for c in checks if c.name == "Python Runtime")
        git_check = next(c for c in checks if c.name == "Git CLI")
        self.assertTrue(py_check.passed)
        self.assertTrue(git_check.passed)

    def test_required_artifacts_all_present(self):
        checks = check_required_artifacts()
        self.assertEqual(len(checks), 7)
        for c in checks:
            self.assertTrue(c.passed, f"Artifact failed check: {c.name} - {c.message}")

    def test_clean_workspace_no_nested_git(self):
        check = check_nested_git_submodules(fix=False)
        self.assertTrue(check.passed)
        self.assertIn("No detached nested .git", check.message)

    def test_stale_git_lock_detection_and_fix(self):
        # Create a mock lock file in .git
        lock_file = Path("D:/Skills/.agents/.git/index.lock")
        if lock_file.exists():
            lock_file.unlink()

        try:
            # Simulate stale lock creation
            lock_file.write_text("dummy lock content", encoding="utf-8")

            # 1. Detection without fix
            detect_check = check_stale_git_locks(fix=False)
            self.assertFalse(detect_check.passed)
            self.assertTrue(detect_check.fixable)
            self.assertIn("STALE LOCK FOUND", detect_check.message)

            # 2. Repair with fix
            fix_check = check_stale_git_locks(fix=True)
            self.assertTrue(fix_check.passed)
            self.assertIn("REPAIRED", fix_check.message)
            self.assertFalse(lock_file.exists())
        finally:
            if lock_file.exists():
                lock_file.unlink()

if __name__ == "__main__":
    unittest.main()
