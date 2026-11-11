import json
import unittest
from pathlib import Path

RECORD = Path(__file__).resolve().parents[1] / "data" / "linguistic-heritage" / "cyrillic-letter-y.json"

class LinguisticHeritageContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record = json.loads(RECORD.read_text(encoding="utf-8"))

    def test_identity(self):
        self.assertEqual(self.record["schema_version"], "linguistic-heritage.letter.v1")
        self.assertEqual((self.record["grapheme"], self.record["lowercase"]), ("Ы", "ы"))

    def test_distinct_historical_layers(self):
        self.assertTrue({"historical_graphics", "historical_phonology", "phoneme_profile"}.issubset(self.record))

    def test_interpretation_is_labelled(self):
        self.assertEqual(self.record["interpretive_layer"]["status"], "cultural_interpretation_not_historical_evidence")
        self.assertTrue(self.record["claims_policy"]["label_hypotheses_and_metaphors"])

    def test_comparison_is_qualified(self):
        self.assertIn("not identical", self.record["comparative_slavic"]["polish_y"])
        self.assertIn("not an exact equivalent", self.record["comparative_slavic"]["ukrainian_y"])

    def test_sources(self):
        self.assertTrue(all(x["url"].startswith("https://") for x in self.record["references"]))

if __name__ == "__main__":
    unittest.main()
