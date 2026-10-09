#!/usr/bin/env python3
"""
Unit tests for the Antigravity Agent OS Prompt Caching & Intake Engine.
Validates prefix hash stability, deterministic sorting, LF normalization,
and leakage prevention.
"""

import unittest
import sys
from pathlib import Path

# Add scripts directory to path
SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from prompt_cache import (
    normalize_newlines,
    canonical_json,
    PromptIntakeAssembler,
    run_cache_audit,
    run_cache_simulation
)

class TestPromptCachingEngine(unittest.TestCase):

    def test_newline_normalization(self):
        """Verifies CRLF line breaks are stripped to clean LF."""
        windows_str = "line1\r\nline2\r\nline3\r"
        normalized = normalize_newlines(windows_str)
        self.assertEqual(normalized, "line1\nline2\nline3\n")
        self.assertNotIn("\r", normalized)

    def test_canonical_json_sorting(self):
        """Verifies JSON keys are sorted alphabetically and compactly."""
        dict_a = {"zebra": 1, "alpha": 2, "charlie": {"beta": 3, "apple": 4}}
        dict_b = {"alpha": 2, "zebra": 1, "charlie": {"apple": 4, "beta": 3}}
        
        json_a = canonical_json(dict_a)
        json_b = canonical_json(dict_b)
        
        self.assertEqual(json_a, json_b)
        self.assertEqual(json_a, '{"alpha":2,"charlie":{"apple":4,"beta":3},"zebra":1}')

    def test_prefix_hash_invariance_across_turns(self):
        """Verifies static prefix hash remains identical despite changing user requests & metadata."""
        assembler = PromptIntakeAssembler()
        assembler.set_tier_0_base("Immutable Constitution Section 1.1")
        assembler.set_tier_1_tools([{"name": "b_tool"}, {"name": "a_tool"}])
        assembler.set_tier_2_grounding("Workspace ADR records")

        initial_hash = assembler.compute_static_prefix_hash()

        # Turn 1
        assembler.set_tier_4_tail("Turn 1: Fix bug", {"timestamp": "2026-10-08T20:00:00", "id": 101})
        turn_1_hash = assembler.compute_static_prefix_hash()
        self.assertEqual(initial_hash, turn_1_hash)

        # Turn 2 with totally different user query and clock
        assembler.add_tier_3_turn("user", "Turn 1: Fix bug")
        assembler.add_tier_3_turn("assistant", "Fixed bug.")
        assembler.set_tier_4_tail("Turn 2: Run tests", {"timestamp": "2026-10-08T21:30:15", "id": 102})
        turn_2_hash = assembler.compute_static_prefix_hash()
        self.assertEqual(initial_hash, turn_2_hash)

    def test_deterministic_tool_and_skill_sorting(self):
        """Verifies tool and skill orders are alphabetized regardless of input order."""
        assembler1 = PromptIntakeAssembler()
        assembler1.set_tier_1_tools([{"name": "zoom"}, {"name": "alpha"}])
        assembler1.set_tier_1_skills([{"name": "skill_z"}, {"name": "skill_a"}])

        assembler2 = PromptIntakeAssembler()
        assembler2.set_tier_1_tools([{"name": "alpha"}, {"name": "zoom"}])
        assembler2.set_tier_1_skills([{"name": "skill_a"}, {"name": "skill_z"}])

        self.assertEqual(assembler1.build_static_prefix(), assembler2.build_static_prefix())

    def test_cache_leakage_detection(self):
        """Verifies auditor catches timestamps and git telemetry leaked into prefix."""
        assembler = PromptIntakeAssembler()
        
        # Leaking a timestamp into Tier 0
        assembler.set_tier_0_base("Current time: 2026-10-08T21:00:00 - Bad header")
        violations = assembler.audit_cache_leakage()
        self.assertTrue(any("LEAK: Dynamic ISO timestamp" in v for v in violations))

        # Leaking dirty_files into Tier 2
        assembler.set_tier_0_base("Clean base")
        assembler.set_tier_2_grounding("Grounding with dirty_files: ['file1.ts']")
        violations = assembler.audit_cache_leakage()
        self.assertTrue(any("LEAK: Git working tree telemetry" in v for v in violations))

    def test_simulation_run(self):
        """Verifies that running cache simulation executes cleanly without error."""
        exit_code = run_cache_simulation()
        self.assertEqual(exit_code, 0)

if __name__ == "__main__":
    unittest.main()
