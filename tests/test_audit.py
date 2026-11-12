import tempfile
import unittest
from pathlib import Path

from ninecirc.audit import build_triadic_matrix, scan_repository


class AuditTests(unittest.TestCase):
    def test_inventory_detects_signals_and_skips_dependencies(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "README.md").write_text("# Example\n\n" + ("Purpose. " * 30), encoding="utf-8")
            (root / "pyproject.toml").write_text("[project]\nname='example'\n", encoding="utf-8")
            (root / "SECURITY.md").write_text("Security reporting\n", encoding="utf-8")
            (root / "LICENSE").write_text("License marker\n", encoding="utf-8")
            (root / "src").mkdir()
            (root / "src" / "main.py").write_text("print('not executed')\n", encoding="utf-8")
            (root / "tests").mkdir()
            (root / "tests" / "test_main.py").write_text("def test_example(): pass\n", encoding="utf-8")
            (root / ".github" / "workflows").mkdir(parents=True)
            (root / ".github" / "workflows" / "ci.yml").write_text("name: CI\n", encoding="utf-8")
            (root / "node_modules").mkdir()
            (root / "node_modules" / "ignored.js").write_text("ignored\n", encoding="utf-8")
            result = scan_repository(root)
            self.assertEqual(result["source_count"], 1)
            self.assertEqual(result["test_count"], 1)
            self.assertIn("Python", result["languages"])
            self.assertTrue(result["has_security_policy"])
            self.assertTrue(result["has_license"])
            self.assertTrue(result["readme_defined"])
            self.assertFalse(any("node_modules" in item for item in result["sample_paths"]))

    def test_matrix_is_three_by_three(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "README.md").write_text("# Notes\n" + ("Research notes. " * 20), encoding="utf-8")
            matrix = build_triadic_matrix(scan_repository(root))
            self.assertEqual(len(matrix["stages"]), 3)
            self.assertTrue(all(len(stage["axes"]) == 3 for stage in matrix["stages"]))
            self.assertGreaterEqual(matrix["score"], -9)
            self.assertLessEqual(matrix["score"], 9)

    def test_missing_folder_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(ValueError):
                scan_repository(Path(temp) / "missing")


if __name__ == "__main__":
    unittest.main()
