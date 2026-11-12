# 9circ — interval-based event atlas

This repository now contains the first reusable chronology layer for unusual historical, geological and cosmic-scale events.

- Time is represented as an interval, not an invented exact date.
- Bounds use astronomical year numbering (1 CE = 1; 1 BCE = 0).
- Historical, geological and cosmic scales share a numeric coordinate without pretending their evidence quality is equal.
- Overlapping dates are reported as temporal overlap only; cause remains a separately declared hypothesis.
- Every event requires source identifiers, an explicit evidence state and a confidence assessment.

No events are preloaded from the supplied 666-item text: most numbered ranges were omitted, and unsourced anecdotes must not become canonical data by repetition.

Run `PYTHONPATH=src python -m unittest discover -s tests -v`.
