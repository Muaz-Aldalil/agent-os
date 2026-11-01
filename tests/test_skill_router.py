#!/usr/bin/env python3
"""
tests/test_skill_router.py
Unit tests for the Dynamic Full-Catalog & 4-Phase Conflict-Free Routing Engine.
"""

import unittest
from scripts.skill_router import resolve_task_routing


class TestSkillRouter(unittest.TestCase):
    def test_routes_frontend_ui_task(self):
        res = resolve_task_routing("Build bilingual modal component in Tailwind")
        self.assertIn("FRONTEND_UI", res["domains"])
        self.assertIn("muaz-skill", res["implementation_skills"])
        self.assertIn("rtl-logical-guard", res["completion_guards"])

    def test_routes_laravel_backend_file_without_nextjs_or_wp_conflict(self):
        res = resolve_task_routing("app/Http/Controllers/OrderController.php")
        self.assertIn("BACKEND_LARAVEL_PHP", res["domains"])
        self.assertIn("laravel-mastery", res["implementation_skills"])
        self.assertIn("pest-security-guard", res["completion_guards"])
        self.assertNotIn("nextjs-fullstack", res["implementation_skills"])
        self.assertNotIn("wp-guard", res["implementation_skills"])

    def test_routes_server_action_file_without_laravel_or_wp_conflict(self):
        res = resolve_task_routing("app/orders/actions.ts")
        self.assertIn("NEXTJS_SERVER_ACTIONS", res["domains"])
        self.assertIn("next-server-action-guard", res["implementation_skills"])
        self.assertIn("next-server-action-guard", res["completion_guards"])
        self.assertNotIn("laravel-mastery", res["implementation_skills"])
        self.assertNotIn("wp-guard", res["implementation_skills"])

    def test_routes_wordpress_woocommerce_without_laravel_or_nextjs_conflict(self):
        res = resolve_task_routing("Build HPOS WooCommerce checkout extension in wp-content/plugins")
        self.assertIn("WORDPRESS_WOOCOMMERCE", res["domains"])
        self.assertIn("wp-guard", res["implementation_skills"])
        self.assertIn("woo-guard", res["implementation_skills"])
        self.assertNotIn("nextjs-fullstack", res["implementation_skills"])
        self.assertNotIn("laravel-mastery", res["implementation_skills"])

    def test_routes_database_task(self):
        res = resolve_task_routing("Create order items table migration with foreign key")
        self.assertIn("DATABASE_PERSISTENCE", res["domains"])
        self.assertIn("database", res["implementation_skills"])
        self.assertTrue(any("AP-001" in g for g in res["completion_guards"]))

    def test_routes_stripe_payments_task(self):
        res = resolve_task_routing("Configure stripe webhook for customer subscription")
        self.assertIn("PAYMENTS_BILLING", res["domains"])
        self.assertTrue(any("stripe MCP" in t for t in res["in_flight_tools"]))
        self.assertTrue(any("Danger Zone 1" in g for g in res["completion_guards"]))

    def test_routes_devops_netlify_and_github_task(self):
        res = resolve_task_routing("Trigger netlify preview deploy and open PR on github")
        self.assertIn("DEVOPS_DEPLOYMENT", res["domains"])
        self.assertTrue(any("netlify MCP" in t for t in res["in_flight_tools"]))
        self.assertTrue(any("github MCP" in t for t in res["in_flight_tools"]))

    def test_routes_stitch_and_devtools_ui_task(self):
        res = resolve_task_routing("Generate screen design using Stitch and verify layout")
        self.assertIn("FRONTEND_UI", res["domains"])
        self.assertTrue(any("StitchMCP" in t for t in res["in_flight_tools"]))
        self.assertTrue(any("chrome-devtools-mcp" in t for t in res["in_flight_tools"]))
        self.assertTrue(any("lighthouse_audit" in g for g in res["completion_guards"]))

    def test_task_sizing_levels(self):
        r1 = resolve_task_routing("fix typo in button label")
        self.assertIn("Level 1", r1["task_level"])
        self.assertIn("Zero ceremony", r1["ceremony"])

        r2 = resolve_task_routing("fix crash error when user clicks submit")
        self.assertIn("Level 2", r2["task_level"])

        r4 = resolve_task_routing("architectural overhaul and greenfield precode specs")
        self.assertIn("Level 4", r4["task_level"])

    def test_delegation_guidance(self):
        r_fs = resolve_task_routing("modify firestore.rules for user security")
        self.assertIn("firestore-rules-author", r_fs["delegation"])

        r_std = resolve_task_routing("write unit tests for order service")
        self.assertIn("DIRECT EXECUTION LOCK", r_std["delegation"])

    def test_fallbacks_and_continuity_domain(self):
        r_cont = resolve_task_routing("resume session from PROGRESS.md and check memory")
        self.assertIn("CROSS_SESSION_CONTINUITY", r_cont["domains"])
        self.assertIn("memory MCP", r_cont["fallbacks"])

    def test_routes_webmcp_browser_tools(self):
        r_webmcp = resolve_task_routing("register in-browser WebMCP tool using document.modelContext")
        self.assertIn("WEBMCP", r_webmcp["domains"])
        self.assertIn("webmcp", r_webmcp["implementation_skills"])
        self.assertTrue(any("chrome-devtools-mcp" in t for t in r_webmcp["in_flight_tools"]))

    def test_routes_ui_audit_task(self):
        r_audit = resolve_task_routing("run comprehensive frontend UI audit across routes and components")
        self.assertIn("FRONTEND_UI", r_audit["domains"])
        self.assertIn("ui-audit", r_audit["implementation_skills"])

    def test_routes_gemini_ai_and_performance_and_ponytail(self):
        r_ai = resolve_task_routing("Integrate gemini live api multimodal streaming")
        self.assertIn("AI_GEMINI_INTEGRATION", r_ai["domains"])
        self.assertIn("gemini-live-api-dev", r_ai["implementation_skills"])

        r_perf = resolve_task_routing("Debug slow LCP and memory leak in heapsnapshot")
        self.assertIn("PERFORMANCE_A11Y_DEBUG", r_perf["domains"])
        self.assertIn("debug-optimize-lcp", r_perf["implementation_skills"])
        self.assertIn("memory-leak-debugging", r_perf["implementation_skills"])

        r_pony = resolve_task_routing("Run /ponytail-review to cut over-engineering bloat")
        self.assertIn("PONYTAIL_SIMPLICITY", r_pony["domains"])
        self.assertIn("ponytail-review", r_pony["implementation_skills"])

    def test_four_phase_loadout_and_authority_winners_present(self):
        res = resolve_task_routing("Build bilingual Next.js checkout page with Stripe")
        loadout = res.get("phase_loadout", {})
        self.assertIn("1_THINK", loadout)
        self.assertIn("2_PLAN", loadout)
        self.assertIn("3_BUILD", loadout)
        self.assertIn("4_VERIFY", loadout)
        self.assertIn("design_tokens_and_layout", res.get("authority_winners", {}))


if __name__ == "__main__":
    unittest.main()
