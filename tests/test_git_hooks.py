#!/usr/bin/env python3
"""
Unit tests for Git hooks installation and pre-commit verification logic.
"""

import sys
import os
import unittest
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))
from install_git_hooks import install_hooks, PRE_COMMIT_SCRIPT, HOOKS_DIR

class TestGitHooks(unittest.TestCase):

    def test_install_hooks_creates_pre_commit(self):
        result = install_hooks()
        self.assertTrue(result)
        hook_path = HOOKS_DIR / "pre-commit"
        self.assertTrue(hook_path.exists())
        content = hook_path.read_text(encoding="utf-8")
        self.assertIn("Pre-Commit Guard", content)
        self.assertIn("guard_checker.py", content)

    def test_pre_commit_script_logic(self):
        # Script must check cached diffs and block on violations
        self.assertIn("--cached", PRE_COMMIT_SCRIPT)
        self.assertIn("--name-only", PRE_COMMIT_SCRIPT)
        self.assertIn("has_violations", PRE_COMMIT_SCRIPT)

if __name__ == "__main__":
    unittest.main()
