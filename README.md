# 9circ

**9circ** is an experimental, evidence-aware chronology foundation for unusual historical, geological and cosmic-scale events.

## Initial capabilities

- Interval-based dating that preserves uncertainty instead of inventing exact timestamps.
- Astronomical year numbering for BCE/CE conversion.
- Validation of source references, evidence states and separately declared causal hypotheses.
- Timeline ordering and overlapping-interval inspection without confusing correlation with causation.

The initial layer is intentionally data-empty. The 666-item source text supplied for this work omits large numbered ranges and does not provide primary sources for most examples, so it is not imported as a verified catalogue.

## Development

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
```

See [the event-atlas contract](docs/EVENT_ATLAS.md).
