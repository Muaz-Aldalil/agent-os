#!/usr/bin/env python3
"""
tests/test_skill_router.py
Unit tests for the Task-to-Skill and Tool Routing Engine.
"""

import unittest
from scripts.skill_router import resolve_task_routing

class TestSkillRouter(unittest.TestCase):
    def test_routes_frontend_ui_task(self):
        res = resolve_task_routing("Build bilingual modal component in Tailwind")
        self.assertIn("FRONTEND_UI", res["domains"])
        self.assertIn("muaz-skill", res["implementation_skills"])
        self.assertIn("rtl-logical-guard", res["completion_guards"])

    def test_routes_laravel_backend_file(self):
        res = resolve_task_routing("app/Http/Controllers/OrderController.php")
        self.assertIn("BACKEND_LARAVEL_PHP", res["domains"])
        self.assertIn("laravel-mastery", res["implementation_skills"])
        self.assertIn("pest-security-guard", res["completion_guards"])

    def test_routes_server_action_file(self):
        res = resolve_task_routing("app/orders/actions.ts")
        self.assertIn("NEXTJS_SERVER_ACTIONS", res["domains"])
        self.assertIn("next-server-action-guard", res["implementation_skills"])
        self.assertIn("next-server-action-guard", res["completion_guards"])

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

if __name__ == "__main__":
    unittest.main()
