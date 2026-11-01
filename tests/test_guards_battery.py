#!/usr/bin/env python3
"""
Comprehensive Guard Verification Battery for Antigravity Agent OS.
Validates detection accuracy of domain-specific guard rules against
adversarial/vulnerable samples and clean/compliant fixtures.
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))
from guard_checker import (
    check_next_server_actions,
    check_pest_php_security,
    check_rtl_logical_css,
    check_clean_code_hygiene,
    check_python_security_and_hygiene,
    check_architectural_boundaries,
    check_modularity_and_reusability,
)

class TestNextServerActionGuard(unittest.TestCase):

    def test_vulnerable_server_action_detected(self):
        vulnerable_code = """
"use server";

export async function deletePostAction({ id, userId, role }) {
    // VULNERABILITY 1: userId & role accepted directly from client payload
    // VULNERABILITY 2: Deleting by id alone (IDOR)
    await prisma.post.delete({
        where: { id }
    });
}

export async function updateSettingsAction(data) {
    try {
        await saveSettings(data);
    } catch (err) {
        // VULNERABILITY 3: Leaking internal error.message to client
        return { success: false, error: err.message };
    }
}
"""
        violations = check_next_server_actions(vulnerable_code)
        rule_ids = [v.rule for v in violations]
        self.assertIn("AUTH_DERIVATION_VIOLATION", rule_ids)
        self.assertIn("ANTI_IDOR_VIOLATION", rule_ids)
        self.assertIn("RAW_ERROR_LEAK", rule_ids)
        self.assertGreaterEqual(len(violations), 3)

    def test_compliant_server_action_passes(self):
        compliant_code = """
"use server";

import { auth } from "@/lib/auth";
import { updatePostSchema } from "@/lib/validations/post";

export async function updatePostAction(rawInput: unknown) {
    const session = await auth();
    if (!session?.user?.id) {
        throw new Error("Unauthorized");
    }

    const parsed = updatePostSchema.safeParse(rawInput);
    if (!parsed.success) {
        return { success: false, errors: parsed.error.flatten() };
    }

    try {
        const updated = await prisma.post.update({
            where: {
                id: parsed.data.id,
                userId: session.user.id // Anti-IDOR scoping
            },
            data: parsed.data
        });
        return { success: true, data: updated };
    } catch (err) {
        console.error("Failed to update post:", err);
        return { success: false, error: "Unable to update post at this time." };
    }
}
"""
        violations = check_next_server_actions(compliant_code)
        self.assertEqual(len(violations), 0)


class TestPestPhpSecurityGuard(unittest.TestCase):

    def test_vulnerable_php_detected(self):
        vulnerable_code = """<?php

class DangerousService {
    public function executeUntrusted($input) {
        eval($input);
        system("rm -f " . $input);
        $obj = unserialize($input);
    }
}
"""
        violations = check_pest_php_security(vulnerable_code, filename="DangerousService.php")
        rule_ids = [v.rule for v in violations]
        self.assertIn("STRICT_TYPES_REQUIRED", rule_ids)
        self.assertIn("DANGEROUS_FUNCTION_FORBIDDEN", rule_ids)
        self.assertGreaterEqual(len(violations), 3)

    def test_compliant_pest_and_php_passes(self):
        compliant_code = """<?php

declare(strict_types=1);

namespace Tests\\Feature;

test('security architectural preset enforced', function () {
    arch()->preset()->security();
});
"""
        violations = check_pest_php_security(compliant_code, filename="SecurityArchitectureTest.php")
        self.assertEqual(len(violations), 0)


class TestRtlLogicalGuard(unittest.TestCase):

    def test_physical_css_and_tailwind_detected(self):
        bad_component = """
export function Card() {
    return (
        <div style={{ marginLeft: 16, textAlign: 'left' }} className="ml-4 pl-2 text-left">
            <span style={{ paddingRight: 8 }}>Badge</span>
        </div>
    );
}
"""
        bad_css = """
.card {
    margin-left: 16px;
    padding-right: 24px;
    text-align: right;
    left: 10px;
}
"""
        violations_component = check_rtl_logical_css(bad_component)
        violations_css = check_rtl_logical_css(bad_css)

        self.assertTrue(any(v.rule == "PHYSICAL_TAILWIND_UTILITY" for v in violations_component))
        self.assertTrue(any(v.rule == "PHYSICAL_CSS_PROPERTY" for v in violations_css))
        self.assertGreaterEqual(len(violations_component) + len(violations_css), 5)

    def test_compliant_logical_css_and_tailwind_passes(self):
        compliant_component = """
export function Card() {
    return (
        <div className="ms-4 ps-2 text-start">
            <span className="pe-2">Badge</span>
        </div>
    );
}
"""
        compliant_css = """
.card {
    margin-inline-start: 16px;
    padding-inline-end: 24px;
    text-align: start;
    inset-inline-start: 10px;
}
"""
        self.assertEqual(len(check_rtl_logical_css(compliant_component)), 0)
        self.assertEqual(len(check_rtl_logical_css(compliant_css)), 0)


class TestCleanCodeGuard(unittest.TestCase):

    def test_swallowed_exceptions_detected(self):
        swallowed_python = "def fetch_data():\n    try:\n        connect()\n    except" + " Exception:\n        " + "pass\n"
        swallowed_js = "function processOrder() {\n    try {\n        chargeCard();\n    } catch (e) {" + "}\n}"
        violations_py = check_clean_code_hygiene(swallowed_python)
        violations_js = check_clean_code_hygiene(swallowed_js)

        self.assertEqual(len(violations_py), 1)
        self.assertEqual(violations_py[0].rule, "SWALLOWED_EXCEPTION")

        self.assertEqual(len(violations_js), 1)
        self.assertEqual(violations_js[0].rule, "SWALLOWED_EXCEPTION")

    def test_clean_error_handling_passes(self):
        clean_python = """
def fetch_data():
    try:
        connect()
    except Exception as e:
        logger.error("Database connection failed", exc_info=e)
        raise
"""
        clean_js = """
function processOrder() {
    try {
        chargeCard();
    } catch (error) {
        logger.error("Payment failed", error);
        throw new PaymentError("Payment processing failed");
    }
}
"""
        self.assertEqual(len(check_clean_code_hygiene(clean_python)), 0)
        self.assertEqual(len(check_clean_code_hygiene(clean_js)), 0)


class TestPythonSecurityAndHygieneGuard(unittest.TestCase):

    def test_mutable_default_argument_detected(self):
        code = "def process_queue(items=[]):\n    pass\n"
        violations = check_python_security_and_hygiene(code, "queue.py")
        self.assertEqual(len(violations), 1)
        self.assertEqual(violations[0].rule, "MUTABLE_DEFAULT_ARGUMENT")

    def test_insecure_os_system_detected(self):
        code = "import os\ndef deploy():\n    os.system('rm -rf /tmp/cache')\n"
        violations = check_python_security_and_hygiene(code, "deploy.py")
        self.assertEqual(len(violations), 1)
        self.assertEqual(violations[0].rule, "INSECURE_OS_SYSTEM")

    def test_hardcoded_secret_detected(self):
        code = 'def get_client():\n    api_key = "sk_live_1234567890abcdef"\n    return Client(api_key)\n'
        violations = check_python_security_and_hygiene(code, "client.py")
        self.assertEqual(len(violations), 1)
        self.assertEqual(violations[0].rule, "HARDCODED_SECRET_LITERAL")

    def test_clean_python_code_passes(self):
        code = 'import os\ndef process_items(items=None):\n    if items is None:\n        items = []\n    api_key = os.getenv("API_KEY")\n    return len(items)\n'
        violations = check_python_security_and_hygiene(code, "clean.py")
        self.assertEqual(len(violations), 0)


class TestArchitecturalBoundariesGuard(unittest.TestCase):

    def test_client_server_boundary_leak_detected(self):
        leaky_client = """
"use client";
import { prisma } from "@/lib/prisma";
import { userRepo } from "@/domains/identity/repositories/user.repo";

export function ProfileWidget({ id }: { id: string }) {
    const user = prisma.user.findUnique({ where: { id } });
    return <div>{String(user)}</div>;
}
"""
        violations = check_architectural_boundaries(leaky_client, "src/components/ProfileWidget.tsx")
        rule_ids = [v.rule for v in violations]
        self.assertIn("CLIENT_SERVER_BOUNDARY_LEAK", rule_ids)
        self.assertGreaterEqual(len(violations), 2)

    def test_controller_layer_skipping_detected(self):
        leaky_controller = """<?php
declare(strict_types=1);

namespace App\\Http\\Controllers;

use App\\Repositories\\OrderRepository;
use Illuminate\\Support\\Facades\\DB;

class OrderController {
    public function store(OrderRepository $orderRepo) {
        DB::beginTransaction();
        $rows = DB::select("SELECT * FROM orders WHERE status = 'pending'");
        return $orderRepo->create([]);
    }
}
"""
        violations = check_architectural_boundaries(leaky_controller, "app/Http/Controllers/OrderController.php")
        rule_ids = [v.rule for v in violations]
        self.assertIn("LAYER_SKIPPING_CONTROLLER_BYPASS", rule_ids)
        self.assertGreaterEqual(len(violations), 3)

    def test_public_admin_shell_leak_detected(self):
        leaky_public_page = """
import { AdminSidebar } from "@/components/admin/AdminSidebar";

export default function PublicLandingPage() {
    return (
        <div>
            <AdminSidebar />
        </div>
    );
}
"""
        leaky_admin_page = """
import { PublicNavbar } from "@/components/public/Navbar";

export default function AdminDashboardPage() {
    return (
        <div>
            <PublicNavbar />
        </div>
    );
}
"""
        v_pub = check_architectural_boundaries(leaky_public_page, "src/app/[locale]/(public)/page.tsx")
        v_adm = check_architectural_boundaries(leaky_admin_page, "src/app/[locale]/admin/page.tsx")
        self.assertTrue(any(v.rule == "PUBLIC_ADMIN_SHELL_LEAK" for v in v_pub))
        self.assertTrue(any(v.rule == "PUBLIC_ADMIN_SHELL_LEAK" for v in v_adm))

    def test_cross_domain_repository_leak_detected(self):
        leaky_domain_service = """<?php
declare(strict_types=1);

namespace App\\Domains\\Billing\\Services;

use App\\Domains\\Identity\\Repositories\\UserRepository;

class InvoiceService {
    public function issue(UserRepository $users) {}
}
"""
        violations = check_architectural_boundaries(leaky_domain_service, "app/Domains/Billing/Services/InvoiceService.php")
        self.assertEqual(len(violations), 1)
        self.assertEqual(violations[0].rule, "CROSS_DOMAIN_REPOSITORY_LEAK")

    def test_upward_abstraction_leak_detected(self):
        leaky_service = """<?php
declare(strict_types=1);

namespace App\\Domains\\Catalog\\Services;

use Illuminate\\Database\\Eloquent\\Builder;

class CourseService {
    public function queryPublishedCourses(): Builder {
        return Course::query();
    }
}
"""
        violations = check_architectural_boundaries(leaky_service, "app/Domains/Catalog/Services/CourseService.php")
        self.assertEqual(len(violations), 1)
        self.assertEqual(violations[0].rule, "UPWARD_ABSTRACTION_LEAK")

    def test_compliant_layered_architecture_passes(self):
        clean_controller = """<?php
declare(strict_types=1);

namespace App\\Http\\Controllers;

use App\\Domains\\Billing\\Actions\\IssueInvoiceAction;

class InvoiceController {
    public function store(IssueInvoiceAction $issueInvoice) {
        return $issueInvoice->execute();
    }
}
"""
        clean_public_page = """
import { PublicNavbar } from "@/components/public/Navbar";

export default function PublicCoursesPage() {
    return <PublicNavbar />;
}
"""
        self.assertEqual(len(check_architectural_boundaries(clean_controller, "app/Http/Controllers/InvoiceController.php")), 0)
        self.assertEqual(len(check_architectural_boundaries(clean_public_page, "src/app/[locale]/(public)/courses/page.tsx")), 0)


class TestModularityAndRootGovernanceGuard(unittest.TestCase):

    def test_monolith_entry_file_detected(self):
        monolith_app = """
function Header() {
    return <header>Nav</header>;
}
function HeroSection() {
    return <section>Hero</section>;
}
function Footer() {
    return <footer>Footer</footer>;
}
export default function App() {
    return (
        <div>
            <Header />
            <HeroSection />
            <Footer />
        </div>
    );
}
"""
        violations = check_modularity_and_reusability(monolith_app, "src/App.jsx")
        rule_ids = [v.rule for v in violations]
        self.assertIn("MONOLITH_COMPONENT_FILE", rule_ids)

    def test_missing_component_header_doc_detected_and_compliant_passes(self):
        undocumented_card = """
export function Card({ title, children }) {
    return <div className="rounded-xl p-6">{title}{children}</div>;
}
"""
        documented_card = """/**
 * Purpose: Reusable surface card container for metrics and feature blocks.
 * Reused In: Public Landing Page (Features) & Admin Dashboard (Metrics Grid).
 * Key Props: title (string), children (ReactNode).
 */
export function Card({ title, children }) {
    return <div className="rounded-xl p-6">{title}{children}</div>;
}
"""
        v_missing = check_modularity_and_reusability(undocumented_card, "src/components/ui/Card.tsx")
        v_clean = check_modularity_and_reusability(documented_card, "src/components/ui/Card.tsx")
        self.assertEqual(len(v_missing), 1)
        self.assertEqual(v_missing[0].rule, "MISSING_COMPONENT_HEADER_DOC")
        self.assertEqual(len(v_clean), 0)

    def test_root_governance_scaffolding_and_tiered_security(self):
        import tempfile
        from pathlib import Path
        from precode_engine import init_root_governance, audit_root_governance, detect_security_tier

        self.assertEqual(detect_security_tier("Promo Landing Page", "landing"), 1)
        self.assertEqual(detect_security_tier("Academy LMS Portal", "lms"), 3)
        self.assertEqual(detect_security_tier("Al-Noor SMS System", "sms"), 3)
        self.assertEqual(detect_security_tier("Acme SaaS Dashboard", "saas"), 2)

        with tempfile.TemporaryDirectory() as tmp:
            root_path = Path(tmp)
            res = init_root_governance(root_path, "Academy LMS", project_type="lms")
            self.assertEqual(res["security_tier"], 3)
            self.assertTrue((root_path / "MASTER.md").is_file())
            self.assertTrue((root_path / "DESIGN.md").is_file())
            self.assertTrue((root_path / "SECURITY.md").is_file())
            sec_text = (root_path / "SECURITY.md").read_text(encoding="utf-8")
            self.assertIn("Tier 3", sec_text)

            audit_res = audit_root_governance(root_path)
            self.assertTrue(audit_res["passed"])
            self.assertEqual(audit_res["score"], 100.0)


if __name__ == "__main__":
    unittest.main()
