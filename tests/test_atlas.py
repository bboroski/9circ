import unittest

from ninecirc.atlas import (
    NineCircEvent, astronomical_year, chronological_atlas,
    overlapping_intervals, validate_atlas,
)


class NineCircAtlasTests(unittest.TestCase):
    def event(self, key, start, end, **kwargs):
        return NineCircEvent(
            key, start, end, kwargs.get("scale", "historical"),
            kwargs.get("precision", "range"), key,
            kwargs.get("state", "single-source"), 0.7,
            source_ids=("source-" + key,),
            causal_hypotheses=kwargs.get("hypotheses", ()),
        )

    def test_bce_conversion_avoids_a_fake_year_zero_gap(self):
        self.assertEqual(astronomical_year(1, "BCE"), 0)
        self.assertEqual(astronomical_year(1, "CE"), 1)
        self.assertEqual(astronomical_year(44, "BCE"), -43)

    def test_uncertain_intervals_are_kept_and_sorted(self):
        old = self.event("old", -1000, -900, scale="geological")
        new = self.event("new", 1500, 1501)
        self.assertEqual([x.event_id for x in chronological_atlas([new, old])],
                         ["old", "new"])

    def test_interval_overlap_is_not_causal_inference(self):
        a = self.event("a", 100, 110)
        b = self.event("b", 108, 120)
        self.assertEqual(overlapping_intervals([a, b]), [("a", "b", 2)])

    def test_invalid_intervals_and_hypothesis_cycles_are_rejected(self):
        a = self.event("a", 10, 5, hypotheses=("b",))
        b = self.event("b", 0, 1, hypotheses=("a",))
        errors = validate_atlas([a, b])
        self.assertTrue(any("earliest_year" in x for x in errors))
        self.assertTrue(any("cycle" in x for x in errors))


if __name__ == "__main__":
    unittest.main()
