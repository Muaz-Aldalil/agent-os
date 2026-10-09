#!/usr/bin/env python3
"""
tests/test_chaos_guard.py
Unit tests for the Chaos / Adversarial Test Gate engine.
"""

import unittest
from scripts.chaos_guard import analyze_test_content

class TestChaosGuard(unittest.TestCase):
    def test_happy_path_only_fails(self):
        happy_code = """
def test_addition():
    assert add(2, 3) == 5
    self.assertEqual(add(10, 20), 30)
"""
        res = analyze_test_content(happy_code, "test_happy.py")
        self.assertFalse(res["passed"])
        self.assertEqual(res["negative_assertions"], 0)
        self.assertEqual(res["adversarial_ratio"], 0.0)

    def test_negative_exception_passes(self):
        code_with_raises = """
def test_division_by_zero():
    with self.assertRaises(ZeroDivisionError):
        divide(10, 0)
"""
        res = analyze_test_content(code_with_raises, "test_raises.py")
        self.assertTrue(res["passed"])
        self.assertGreater(res["negative_assertions"], 0)

    def test_negative_http_error_code_passes(self):
        code_with_http = """
def test_unauthorized_user():
    res = client.get("/admin")
    assert res.status_code == 403
"""
        res = analyze_test_content(code_with_http, "test_auth.py")
        self.assertTrue(res["passed"])
        self.assertGreater(res["negative_assertions"], 0)

    def test_js_to_throw_passes(self):
        js_code = """
it('throws on invalid email', () => {
    expect(() => validate('bad-email')).toThrow();
});
"""
        res = analyze_test_content(js_code, "auth.test.ts")
        self.assertTrue(res["passed"])
        self.assertGreater(res["negative_assertions"], 0)

if __name__ == "__main__":
    unittest.main()
