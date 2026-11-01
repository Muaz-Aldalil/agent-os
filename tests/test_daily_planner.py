#!/usr/bin/env python3
"""
tests/test_daily_planner.py
Unit tests for scripts/daily_planner.py (Autonomous Session Triage & Skill/Tool Evolution Factory).
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT / "scripts"))

from daily_planner import (
    detect_project_stack,
    extract_Candidate_tasks,
    build_daily_plan,
    format_daily_plan_report,
)


class TestDailyPlanner(unittest.TestCase):

    def test_detects_agent_os_stack(self):
        stack = detect_project_stack(WORKSPACE_ROOT)
        self.assertTrue(any("Agent OS" in s for s in stack["stacks"]))
        self.assertIn("engineering-workflow", stack["guards"])
        self.assertIn("python scripts/agent_os.py test", stack["quality_gates"])

    def test_detects_nextjs_and_laravel_fullstack_in_temp_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "package.json").write_text('{"name": "web"}', encoding="utf-8")
            (root / "composer.json").write_text('{"name": "laravel/laravel"}', encoding="utf-8")

            stack = detect_project_stack(root)
            self.assertIn("Next.js / React / TypeScript Frontend", stack["stacks"])
            self.assertIn("Laravel / PHP Backend", stack["stacks"])
            self.assertIn("next-server-action-guard", stack["guards"])
            self.assertIn("pest-security-guard", stack["guards"])
            self.assertIn("rtl-logical-guard", stack["guards"])

    def test_extracts_tasks_and_enforces_one_primary_focus(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "PROGRESS.md").write_text(
                "# Progress\n\n## Immediate Next Executable Actions\n"
                "- [ ] Implement checkout idempotency guard\n"
                "- [ ] Add RTL table truncation in admin orders\n"
                "- [ ] Write Pest security tests for webhook\n",
                encoding="utf-8",
            )
            docs_dir = root / "docs"
            docs_dir.mkdir()
            (docs_dir / "release-tracker.md").write_text(
                "# Release Tracker\n- [ ] Verify production env keys\n",
                encoding="utf-8",
            )

            tasks, trackers = extract_Candidate_tasks(root)
            self.assertEqual(len(tasks), 4)
            self.assertIn("PROGRESS.md", trackers)
            self.assertIn("docs/release-tracker.md", trackers)

            plan = build_daily_plan(root)
            self.assertEqual(plan["primary_focus"]["task"], "Implement checkout idempotency guard")
            self.assertEqual(len(plan["up_next"]), 3)

            report = format_daily_plan_report(plan)
            self.assertIn("[1] PRIMARY FOCUS FOR THIS SESSION", report)
            self.assertIn("Implement checkout idempotency guard", report)
            self.assertIn("NEVER auto-commit, auto-push, or auto-merge", report)

    def test_focus_hint_prioritizes_matching_task(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "tasks.md").write_text(
                "- [ ] Build public landing hero\n"
                "- [ ] Fix authentication token refresh race condition\n",
                encoding="utf-8",
            )
            plan = build_daily_plan(root, focus_hint="authentication")
            self.assertEqual(
                plan["primary_focus"]["task"],
                "Fix authentication token refresh race condition",
            )

    def test_skill_evolution_factory_mode(self):
        plan = build_daily_plan(
            WORKSPACE_ROOT,
            focus_hint="Layer and domain boundary leak guard",
            skill_mode="clean-code-guard",
        )
        self.assertEqual(plan["primary_focus"]["source"], "Skill & Tool Evolution Factory")
        self.assertIn("clean-code-guard", plan["primary_focus"]["task"])
        self.assertEqual(len(plan["execution_steps"]), 5)
        report = format_daily_plan_report(plan)
        self.assertIn("Skill & Tool Evolution Factory", report)
        self.assertIn("python scripts/agent_os.py sync --apply", report)


if __name__ == "__main__":
    unittest.main()
