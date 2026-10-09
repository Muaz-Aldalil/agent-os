#!/usr/bin/env python3
"""
tests/test_context_telemetry.py
Unit tests for context window and token budget telemetry.
"""

import unittest
from scripts.context_telemetry import (
    reset_telemetry,
    record_turn,
    evaluate_health,
    get_telemetry
)

class TestContextTelemetry(unittest.TestCase):
    def setUp(self):
        reset_telemetry()

    def tearDown(self):
        reset_telemetry()

    def test_record_turn_increments_count_and_tokens(self):
        data = record_turn(fresh_tokens=1000, cached_tokens=25000)
        self.assertEqual(data["turn_count"], 1)
        self.assertEqual(data["total_input_tokens"], 26000)
        self.assertEqual(data["cached_input_tokens"], 25000)

    def test_evaluate_health_thresholds(self):
        # 0 turns -> HEALTHY
        h0 = evaluate_health()
        self.assertEqual(h0["status"], "HEALTHY")

        # Simulate 42 turns -> WARNING
        for _ in range(42):
            record_turn(100, 1000)
        h42 = evaluate_health()
        self.assertEqual(h42["status"], "WARNING")

        # Simulate up to 65 turns -> CRITICAL
        for _ in range(23):
            record_turn(100, 1000)
        h65 = evaluate_health()
        self.assertEqual(h65["status"], "CRITICAL")

if __name__ == "__main__":
    unittest.main()
