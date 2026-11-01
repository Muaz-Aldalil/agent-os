#!/usr/bin/env python3
"""
Unit tests for Git hooks installation and pre-commit verification logic.
"""

import sys
import os
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))
from install_git_hooks import install_hooks, PRE_COMMIT_SCRIPT


class TestGitHooks(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.hooks_dir = Path(self.temp_dir.name) / ".git" / "hooks"
        self.hooks_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_install_hooks_creates_pre_commit(self):
        result = install_hooks(hooks_dir=self.hooks_dir)
        self.assertTrue(result)
        hook_path = self.hooks_dir / "pre-commit"
        self.assertTrue(hook_path.exists())
        content = hook_path.read_text(encoding="utf-8")
        self.assertIn("Pre-Commit Guard", content)
        self.assertIn("guard_checker.py", content)

    def test_install_hooks_fails_when_hooks_dir_missing(self):
        missing_dir = Path(self.temp_dir.name) / "nonexistent" / ".git" / "hooks"
        result = install_hooks(hooks_dir=missing_dir)
        self.assertFalse(result)

    def test_pre_commit_script_logic(self):
        # Script must check cached diffs, include modern extensions, and fail closed
        self.assertIn("--cached", PRE_COMMIT_SCRIPT)
        self.assertIn("--name-only", PRE_COMMIT_SCRIPT)
        self.assertIn("has_violations", PRE_COMMIT_SCRIPT)
        self.assertIn(".vue", PRE_COMMIT_SCRIPT)
        self.assertIn(".svelte", PRE_COMMIT_SCRIPT)
        self.assertNotIn("return 0\n\n    if not output:", PRE_COMMIT_SCRIPT)


if __name__ == "__main__":
    unittest.main()
