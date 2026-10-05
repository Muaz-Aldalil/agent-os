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
    check_clean_code_hygiene
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
        swallowed_python = """
def fetch_data():
    try:
        connect()
    except Exception:
        pass
"""
        swallowed_js = """
function processOrder() {
    try {
        chargeCard();
    } catch (e) {}
}
"""
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


if __name__ == "__main__":
    unittest.main()
