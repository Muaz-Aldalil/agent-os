#!/usr/bin/env python3
"""
Unit tests for skill_indexer.py.
Validates skill indexing, parsing, categorization, and search accuracy.
"""

import sys
import os
import unittest
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))
from skill_indexer import build_index, search_skills, parse_frontmatter

class TestSkillIndexer(unittest.TestCase):

    def test_parse_frontmatter_multi_line_description(self):
        sample_fm = """---
name: sample-guard
description: >-
  This is line one.
  This is line two of the description.
version: 1.0.0
---
# Main Content
"""
        data, body = parse_frontmatter(sample_fm)
        self.assertEqual(data.get("name"), "sample-guard")
        self.assertIn("line one", data.get("description", ""))
        self.assertIn("line two", data.get("description", ""))
        self.assertEqual(data.get("version"), "1.0.0")

    def test_build_index_indexes_all_skills(self):
        index_data = build_index()
        self.assertGreaterEqual(index_data["total_skills"], 40)
        self.assertEqual(len(index_data["skills"]), index_data["total_skills"])

    def test_search_skills_exact_match(self):
        results = search_skills("next-server-action-guard", limit=1)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "next-server-action-guard")

    def test_search_skills_keyword_pest_php(self):
        results = search_skills("pest php laravel", limit=3)
        self.assertGreaterEqual(len(results), 1)
        names = [r["name"] for r in results]
        self.assertIn("pest-security-guard", names)

    def test_search_skills_keyword_rtl(self):
        results = search_skills("rtl arabic", limit=3)
        self.assertGreaterEqual(len(results), 1)
        names = [r["name"] for r in results]
        self.assertIn("rtl-logical-guard", names)

if __name__ == "__main__":
    unittest.main()
