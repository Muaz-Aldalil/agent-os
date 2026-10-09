#!/usr/bin/env python3
"""
tests/test_runtime_observer.py
Unit tests for runtime log ingestion and server health probe.
"""

import unittest
import tempfile
from pathlib import Path
from scripts.runtime_observer import tail_log, probe_endpoint

class TestRuntimeObserver(unittest.TestCase):
    def test_tail_log_detects_stack_traces(self):
        with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".log") as tf:
            tf.write("2026-10-08 10:00:00 [INFO] Request started\n")
            tf.write("2026-10-08 10:00:01 [ERROR] Database connection lost\n")
            tf.write("Traceback (most recent call last):\n")
            tf.write("  File \"server.py\", line 42, in connect\n")
            tf.write("ConnectionRefusedError: [Errno 111] Connection refused\n")
            log_path = Path(tf.name)

        try:
            res = tail_log(log_path, lines_count=10)
            self.assertEqual(res["total_file_lines"], 5)
            self.assertGreater(res["errors_detected"], 0)
            self.assertTrue(any("ERROR" in s or "Traceback" in s for s in res["error_snippets"]))
        finally:
            if log_path.exists():
                log_path.unlink()

    def test_probe_endpoint_handles_unreachable_gracefully(self):
        # Port 59999 is almost certainly closed locally
        res = probe_endpoint("http://127.0.0.1:59999", timeout=0.5)
        self.assertFalse(res["reachable"])
        self.assertEqual(res["status_code"], 0)
        self.assertTrue(len(res["error"]) > 0)

if __name__ == "__main__":
    unittest.main()
