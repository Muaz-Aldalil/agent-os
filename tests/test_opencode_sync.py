#!/usr/bin/env python3
"""
Unit & Integration Tests for Tri-Target Parity Synchronization
(D:/Skills/.agents <-> C:/Users/HP/.gemini/config <-> C:/Users/HP/.config/opencode).
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))
from sync_config import (
    discover_all_antigravity_skills,
    parse_skill_frontmatter,
    render_opencode_command_md,
    scan_sync_drift,
    apply_sync,
)


class TestOpenCodeParitySync(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.ws_root = self.root / "ws"
        self.gl_root = self.root / "gemini" / "config"
        self.bi_root = self.root / "gemini" / "builtin" / "skills"
        self.oc_root = self.root / "opencode"

        (self.ws_root / "skills").mkdir(parents=True)
        (self.ws_root / "rules").mkdir(parents=True)
        (self.ws_root / "scripts").mkdir(parents=True)
        (self.gl_root / "skills").mkdir(parents=True)
        (self.gl_root / "plugins").mkdir(parents=True)
        self.bi_root.mkdir(parents=True)
        (self.oc_root / "skills").mkdir(parents=True)
        (self.oc_root / "commands").mkdir(parents=True)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_parse_skill_frontmatter_normalizes_underscores_and_skills_folder(self):
        plugin_skill_dir = self.gl_root / "plugins" / "google_maps_platform" / "skills"
        plugin_skill_dir.mkdir(parents=True)
        skill_md = plugin_skill_dir / "SKILL.md"
        skill_md.write_text(
            "---\nname: google-maps-platform\ndescription: >-\n  Google Maps SDKs and APIs.\n---\n# Body\n",
            encoding="utf-8",
        )
        name, desc = parse_skill_frontmatter(skill_md)
        self.assertEqual(name, "google-maps-platform")
        self.assertEqual(desc, "Google Maps SDKs and APIs.")

    def test_tri_target_sync_creates_opencode_skills_commands_and_preserves_speckit_dots(self):
        # 1. Create a workspace skill
        ew_dir = self.ws_root / "skills" / "engineering-workflow"
        ew_dir.mkdir(parents=True)
        (ew_dir / "SKILL.md").write_text(
            "---\nname: engineering-workflow\ndescription: Autonomous workflow\n---\n# EW\n",
            encoding="utf-8",
        )
        # 2. Create a plugin skill with underscore directory name
        af_dir = self.gl_root / "plugins" / "science" / "skills" / "alphafold_fetch"
        af_dir.mkdir(parents=True)
        (af_dir / "SKILL.md").write_text(
            "---\nname: alphafold-fetch\ndescription: Fetch structures\n---\n# AF\n",
            encoding="utf-8",
        )
        # 3. Create an existing speckit.plan.md in OpenCode commands that must be preserved
        speckit_dot = self.oc_root / "commands" / "speckit.plan.md"
        speckit_dot.write_text("# Custom Speckit Dot Command\n", encoding="utf-8")

        drift = scan_sync_drift(
            include_opencode=True,
            workspace_root=self.ws_root,
            global_root=self.gl_root,
            opencode_root=self.oc_root,
            builtin_root=self.bi_root,
        )
        self.assertGreater(len(drift), 0)

        applied = apply_sync(drift)
        self.assertEqual(applied, len(drift))

        # Verify OpenCode skill folders and command files exist
        self.assertTrue((self.oc_root / "skills" / "engineering-workflow" / "SKILL.md").is_file())
        self.assertTrue((self.oc_root / "skills" / "alphafold-fetch" / "SKILL.md").is_file())
        self.assertTrue((self.oc_root / "commands" / "engineering-workflow.md").is_file())
        self.assertTrue((self.oc_root / "commands" / "alphafold-fetch.md").is_file())

        # Verify speckit.plan.md was preserved untouched
        self.assertEqual(speckit_dot.read_text(encoding="utf-8"), "# Custom Speckit Dot Command\n")

        # Second scan should report 0 drift
        drift_after = scan_sync_drift(
            include_opencode=True,
            workspace_root=self.ws_root,
            global_root=self.gl_root,
            opencode_root=self.oc_root,
            builtin_root=self.bi_root,
        )
        self.assertEqual(drift_after, [])

    def test_live_ecosystem_discovers_all_active_skills_within_context_budget(self):
        catalog = discover_all_antigravity_skills()
        self.assertGreaterEqual(len(catalog), 120)
        self.assertLessEqual(len(catalog), 148)
        self.assertIn("engineering-workflow", catalog)
        self.assertIn("intake", catalog)
        self.assertIn("critique", catalog)
        self.assertIn("agentic-workflows", catalog)
        self.assertIn("plan-daily", catalog)
        self.assertIn("google-maps-platform", catalog)
        self.assertNotIn("skills", catalog)


if __name__ == "__main__":
    unittest.main()
