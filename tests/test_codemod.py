#!/usr/bin/env python3
"""
Unit tests for codemod.py batch refactoring engine.
"""

import sys
import os
import unittest
from pathlib import Path
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))
from codemod import (
    transform_php_strict_types,
    transform_css_logical,
    transform_tailwind_logical,
    run_codemod
)

class TestCodemodEngine(unittest.TestCase):

    def test_php_strict_types_insertion(self):
        sample_php = "<?php\n\nclass OrderService {\n}\n"
        transformed, changed = transform_php_strict_types(sample_php)
        self.assertTrue(changed)
        self.assertIn("declare(strict_types=1);", transformed)
        self.assertTrue(transformed.startswith("<?php\n\ndeclare(strict_types=1);"))

    def test_php_strict_types_already_present(self):
        sample_php = "<?php\n\ndeclare(strict_types=1);\n\nclass OrderService {}\n"
        transformed, changed = transform_php_strict_types(sample_php)
        self.assertFalse(changed)
        self.assertEqual(transformed, sample_php)

    def test_css_logical_transformation(self):
        sample_css = """
.card {
    margin-left: 16px;
    padding-right: 20px;
    text-align: left;
}
"""
        transformed, changed = transform_css_logical(sample_css)
        self.assertTrue(changed)
        self.assertIn("margin-inline-start: 16px;", transformed)
        self.assertIn("padding-inline-end: 20px;", transformed)
        self.assertIn("text-align: start;", transformed)

    def test_tailwind_logical_transformation(self):
        sample_tsx = '<div className="ml-4 mr-2 pl-6 pr-8 text-left">Hello</div>'
        transformed, changed = transform_tailwind_logical(sample_tsx)
        self.assertTrue(changed)
        self.assertIn("ms-4", transformed)
        self.assertIn("me-2", transformed)
        self.assertIn("ps-6", transformed)
        self.assertIn("pe-8", transformed)
        self.assertIn("text-start", transformed)

    def test_run_codemod_file_apply(self):
        with tempfile.NamedTemporaryFile("w+", suffix=".css", delete=False, encoding="utf-8") as tmp:
            tmp.write(".box { margin-left: 8px; }")
            tmp_path = Path(tmp.name)

        try:
            modified = run_codemod("rtl-css", str(tmp_path), apply=True)
            self.assertEqual(len(modified), 1)
            content = tmp_path.read_text(encoding="utf-8")
            self.assertIn("margin-inline-start: 8px;", content)
        finally:
            tmp_path.unlink()

if __name__ == "__main__":
    unittest.main()
