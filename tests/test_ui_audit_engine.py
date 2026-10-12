#!/usr/bin/env python3
"""
tests/test_ui_audit_engine.py
Unit tests for the 100X Frontend UI Audit & Implementation Prompt Engine.
"""

import unittest
import tempfile
import shutil
from pathlib import Path
from scripts.ui_audit_engine import (
    UIAuditEngine,
    FrontendTopology,
    CRITICAL,
    HIGH,
    MEDIUM,
    LOW
)

class TestUIAuditEngine(unittest.TestCase):

    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_framework_discovery_nextjs_tailwind(self):
        pkg_json = self.test_dir / "package.json"
        pkg_json.write_text("""{
            "dependencies": {
                "next": "15.1.0",
                "react": "19.0.0",
                "tailwindcss": "^4.0.0",
                "next-intl": "^3.0.0",
                "@radix-ui/react-slot": "^1.0.0"
            },
            "scripts": {
                "lint": "next lint",
                "test": "vitest"
            }
        }""", encoding="utf-8")

        topology = FrontendTopology(self.test_dir)
        topology.discover()

        self.assertIn("Next.js", topology.framework)
        self.assertEqual(topology.styling_system, "Tailwind CSS")
        self.assertTrue(topology.has_rtl)
        self.assertIn("npm run lint", topology.test_diagnostics)
        self.assertIn("npm run test", topology.test_diagnostics)

    def test_detects_fixed_width_responsive_overflow(self):
        comp = self.test_dir / "Card.tsx"
        comp.write_text("""
        export function Card() {
            return <div className="w-[600px] p-4">Overflow card</div>;
        }
        """, encoding="utf-8")

        engine = UIAuditEngine(self.test_dir)
        engine.analyze()

        overflow_findings = [f for f in engine.findings if f.category == "Responsive Behavior"]
        self.assertGreaterEqual(len(overflow_findings), 1)
        self.assertEqual(overflow_findings[0].severity, HIGH)
        self.assertIn("Fixed Container Width", overflow_findings[0].title)

    def test_detects_accessibility_violations(self):
        comp = self.test_dir / "Navigation.tsx"
        comp.write_text("""
        export function Nav() {
            return (
                <nav>
                    <div onClick={() => alert('clicked')} className="cursor-pointer">Click Me</div>
                    <button className="outline-none">Action</button>
                    <img src="/logo.png" />
                </nav>
            );
        }
        """, encoding="utf-8")

        engine = UIAuditEngine(self.test_dir)
        engine.analyze()

        a11y = [f for f in engine.findings if f.category == "Accessibility"]
        titles = [f.title for f in a11y]

        self.assertTrue(any("Non-Semantic Interactive Element" in t for t in titles))
        self.assertTrue(any("Focus Outline Suppressed" in t for t in titles))
        self.assertTrue(any("Image Tag Missing Required 'alt'" in t for t in titles))

    def test_detects_physical_css_properties_breaking_rtl(self):
        comp = self.test_dir / "Sidebar.tsx"
        comp.write_text("""
        export function Sidebar() {
            return <div className="pl-6 mr-4 text-left">Content</div>;
        }
        """, encoding="utf-8")

        engine = UIAuditEngine(self.test_dir)
        engine.analyze()

        rtl_findings = [f for f in engine.findings if f.category == "Localization & RTL"]
        self.assertGreaterEqual(len(rtl_findings), 1)
        self.assertIn("Physical CSS Property", rtl_findings[0].title)
        self.assertIn("ps- (padding-inline-start)", rtl_findings[0].expected_behavior)

    def test_generates_complete_report_and_prompts(self):
        comp = self.test_dir / "Button.tsx"
        comp.write_text("""
        export function ActionButton() {
            return <div onClick={() => {}} className="bg-[#ff0000] p-[15px] outline-none">Click</div>;
        }
        """, encoding="utf-8")

        engine = UIAuditEngine(self.test_dir)
        engine.analyze()

        out_dir = self.test_dir / "docs" / "ui-audits" / "2026-10-12-test"
        res = engine.generate_report_artifacts(out_dir)

        self.assertTrue((out_dir / "report.md").exists())
        self.assertTrue((out_dir / "manual-browser-checklist.md").exists())
        self.assertGreaterEqual(res["prompts_count"], 1)

        # Inspect generated prompt schema
        prompts = list((out_dir / "prompts").glob("*.md"))
        self.assertTrue(len(prompts) > 0)
        first_prompt = prompts[0].read_text(encoding="utf-8")

        # Must contain all 10 mandatory sections A through J
        self.assertIn("## A. Role", first_prompt)
        self.assertIn("## B. Task & Objective", first_prompt)
        self.assertIn("## C. Context & Evidence", first_prompt)
        self.assertIn("## D. Exact Location & Affected Scope", first_prompt)
        self.assertIn("## E. Recommended Solution & Invariants", first_prompt)
        self.assertIn("## F. Implementation Task Checklist", first_prompt)
        self.assertIn("## G. Tools, Skills, and MCP Capabilities", first_prompt)
        self.assertIn("## H. Acceptance Criteria", first_prompt)
        self.assertIn("## I. Verification Plan", first_prompt)
        self.assertIn("## J. Implementation Boundaries", first_prompt)

    def test_generates_diff_preview_for_deterministic_findings(self):
        comp = self.test_dir / "RtlComponent.tsx"
        comp.write_text("""
        export function RtlComponent() {
            return <div className="pl-4 mr-2">RTL Test</div>;
        }
        """, encoding="utf-8")

        engine = UIAuditEngine(self.test_dir)
        engine.analyze()

        out_dir = self.test_dir / "docs" / "ui-audits" / "2026-10-12-diff-test"
        engine.generate_report_artifacts(out_dir)

        prompts = list((out_dir / "prompts").glob("*.md"))
        self.assertTrue(len(prompts) > 0)
        content = prompts[0].read_text(encoding="utf-8")

        self.assertIn("Suggested Code Replacement (Unified Diff Preview)", content)
        self.assertIn("- return <div className=\"pl-4 mr-2\">RTL Test</div>;", content)
        self.assertIn("+ return <div className=\"ps-4 me-2\">RTL Test</div>;", content)

    def test_json_and_strict_evaluation(self):
        comp = self.test_dir / "HeavyView.tsx"
        comp.write_text("""
        export function Heavy() {
            return <div className="w-[800px]"><button>No type</button></div>;
        }
        """, encoding="utf-8")

        engine = UIAuditEngine(self.test_dir)
        engine.analyze()

        data = [f.to_dict() for f in engine.findings]
        self.assertGreaterEqual(len(data), 1)
        first = data[0]
        for key in ["id", "title", "category", "severity", "confidence", "file", "line", "snippet", "current_behavior", "expected_behavior", "user_impact"]:
            self.assertIn(key, first)

        has_crit_high = any(f.severity in [CRITICAL, HIGH] for f in engine.findings)
        self.assertTrue(has_crit_high)

if __name__ == "__main__":
    unittest.main()

