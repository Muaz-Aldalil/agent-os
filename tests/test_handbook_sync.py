import json
import re
import unittest
from pathlib import Path
import sys

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT / "scripts"))

import sync_handbook
import guard_checker


class TestHandbookSyncAndPlatform(unittest.TestCase):
    def test_truncate_words_enforces_short_table_cell_limit(self):
        sample = "All-in-one master command to start a brand new project from zero"
        truncated = sync_handbook.truncate_words(sample, max_words=3)
        self.assertEqual(truncated, "All-in-one master command...")
        self.assertLessEqual(len(truncated.split()), 3)

    def test_sanitize_copy_strips_ai_buzzwords(self):
        raw = "This cutting-edge tool will supercharge and empower your seamless workflow."
        cleaned = sync_handbook.sanitize_copy(raw)
        self.assertNotIn("cutting-edge", cleaned.lower())
        self.assertNotIn("supercharge", cleaned.lower())
        self.assertNotIn("empower", cleaned.lower())
        self.assertNotIn("seamless", cleaned.lower())

    def test_sync_registry_produces_all_60_skills_and_bilingual_fields(self):
        payload = sync_handbook.sync_registry()
        self.assertGreaterEqual(payload["totalSkills"], 85)
        self.assertGreaterEqual(payload["totalCliTools"], 28)
        self.assertGreaterEqual(payload["totalMcpServers"], 18)
        self.assertTrue(sync_handbook.REGISTRY_OUT_PATH.exists())

        loaded = json.loads(sync_handbook.REGISTRY_OUT_PATH.read_text(encoding="utf-8"))
        self.assertEqual(len(loaded["skills"]), payload["totalSkills"])
        self.assertEqual(len(loaded["cliTools"]), payload["totalCliTools"])
        for skill in loaded["skills"]:
            for key in (
                "name",
                "command",
                "categoryEn",
                "categoryAr",
                "domainEn",
                "domainAr",
                "domainShortEn",
                "domainShortAr",
                "shortEn",
                "shortAr",
                "descriptionEn",
                "descriptionAr",
                "samplePromptEn",
                "samplePromptAr",
            ):
                self.assertIn(key, skill, f"Missing {key} in skill {skill.get('name')}")
                self.assertTrue(skill[key], f"Empty {key} in skill {skill.get('name')}")
        for tool in loaded["cliTools"]:
            for key in (
                "name",
                "command",
                "domainEn",
                "domainAr",
                "domainShortEn",
                "domainShortAr",
                "descriptionEn",
                "descriptionAr",
                "samplePromptEn",
                "samplePromptAr",
            ):
                self.assertIn(key, tool, f"Missing {key} in CLI tool {tool.get('name')}")
                self.assertTrue(tool[key], f"Empty {key} in CLI tool {tool.get('name')}")

    def test_astro_platform_files_and_synced_handbook_pass_rtl_and_mobile_rules(self):
        index_astro = WORKSPACE_ROOT / "learning-platform" / "src" / "pages" / "index.astro"
        layout_astro = WORKSPACE_ROOT / "learning-platform" / "src" / "layouts" / "W3Layout.astro"
        handbook_html = WORKSPACE_ROOT / "handbook.html"

        for target in (index_astro, layout_astro, handbook_html):
            self.assertTrue(target.exists(), f"Missing expected file: {target}")
            content = target.read_text(encoding="utf-8")
            violations = guard_checker.check_rtl_logical_css(content)
            self.assertEqual(violations, [], f"RTL logical guard failed on {target.name}: {violations}")

        html_text = handbook_html.read_text(encoding="utf-8")
        # Verify W3Schools signature elements & mobile-first containers
        self.assertIn('id="subtopnav"', html_text)
        self.assertIn("overflow-x-auto", html_text)
        self.assertIn("flex-1 min-w-0", html_text)
        self.assertIn("max-w-xs truncate", html_text)
        self.assertIn('id="details-modal-domain"', html_text)
        self.assertIn('id="details-modal-prompt"', html_text)
        self.assertIn("data-open-cli-modal=", html_text)
        # Verify all 11 Situation Combos + /plan-daily are present
        for cmd in (
            "/start-project",
            "/plan-daily",
            "/smart-feature",
            "/feature-full",
            "/feature-febe",
            "/feature-fe",
            "/feature-wp",
            "/fix-ui",
            "/fix-backend",
            "/check-all",
            "/save-data",
            "/doc-project",
        ):
            self.assertIn(cmd, html_text, f"Missing situation combo {cmd} in compiled handbook.html")

    def test_compiled_css_resets_and_dark_mode_contrast_prevent_invisible_text(self):
        handbook_html = WORKSPACE_ROOT / "handbook.html"
        html_text = handbook_html.read_text(encoding="utf-8")
        style_match = re.search(r"<style>([\s\S]*?)</style>", html_text)
        self.assertIsNotNone(style_match, "Missing embedded <style> block in handbook.html")
        css_text = style_match.group(1)

        # 1. Button preflight reset prevents default browser #F0F0F0 buttonface background hiding light text
        self.assertIn("background-color: transparent;", css_text)
        self.assertIn("-webkit-appearance: button;", css_text)

        # 2. List reset prevents default bullet discs on sidebar <ul>
        self.assertIn("ol, ul, menu { list-style: none; margin: 0; padding: 0; }", css_text)

        # 3. Static --w3-ink (#18181B) is never inverted to white so .bg-w3-yellow.text-w3-ink stays readable in dark mode
        self.assertIn("--w3-ink: #18181B;", css_text)
        self.assertNotIn("--w3-ink: #F4F4F5;", css_text)

        # 4. Explicit html.dark .dark:* utility rules exist for dark mode surfaces and text
        for dark_selector in (
            r"html\.dark \.dark\\:bg-w3-slate",
            r"html\.dark \.dark\\:bg-w3-slateDeep",
            r"html\.dark \.dark\\:text-w3-canvas",
            r"html\.dark \.dark\\:text-zinc-100",
            r"html\.dark \.dark\\:text-zinc-200",
            r"html\.dark \.dark\\:text-zinc-300",
            r"html\.dark \.dark\\:text-w3-mint",
            r"html\.dark \.dark\\:border-zinc-700",
        ):
            self.assertRegex(css_text, dark_selector)


if __name__ == "__main__":
    unittest.main()
