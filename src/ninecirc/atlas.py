"""Interval-based chronology for Earth and cosmic-scale events.

All bounds use astronomical year numbering: 1 CE is 1 and 1 BCE is 0.
Intervals preserve dating uncertainty rather than inventing a precise instant.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from math import isfinite
from typing import Sequence

SCALES = {"historical", "geological", "cosmic"}
PRECISIONS = {"exact", "year", "range", "estimate", "unknown"}
EVIDENCE_STATES = {"unverified", "single-source", "corroborated", "disputed", "corrected"}


@dataclass(frozen=True)
class NineCircEvent:
    event_id: str
    earliest_year: float
    latest_year: float
    time_scale: str
    time_precision: str
    summary: str
    evidence_state: str
    confidence: float
    source_ids: tuple[str, ...] = field(default_factory=tuple)
    related_ids: tuple[str, ...] = field(default_factory=tuple)
    causal_hypotheses: tuple[str, ...] = field(default_factory=tuple)


def astronomical_year(era_year: int, era: str) -> int:
    """Convert BCE/CE input to astronomical year numbering (BCE 1 -> year 0)."""
    if isinstance(era_year, bool) or not isinstance(era_year, int) or era_year < 1:
        raise ValueError("era_year must be a positive integer")
    normalized = era.upper()
    if normalized == "CE":
        return era_year
    if normalized == "BCE":
        return 1 - era_year
    raise ValueError("era must be BCE or CE")


def validate_atlas(events: Sequence[NineCircEvent]) -> list[str]:
    errors: list[str] = []
    by_id: dict[str, NineCircEvent] = {}
    for index, event in enumerate(events):
        if not isinstance(event, NineCircEvent):
            errors.append(f"events[{index}] must be a NineCircEvent")
            continue
        if not event.event_id or event.event_id in by_id:
            errors.append(f"missing or duplicate event_id: {event.event_id!r}")
        else:
            by_id[event.event_id] = event
        if not all(isfinite(value) for value in (event.earliest_year, event.latest_year)):
            errors.append(f"{event.event_id}: date bounds must be finite")
        elif event.earliest_year > event.latest_year:
            errors.append(f"{event.event_id}: earliest_year must not exceed latest_year")
        if event.time_scale not in SCALES:
            errors.append(f"{event.event_id}: unsupported time_scale")
        if event.time_precision not in PRECISIONS:
            errors.append(f"{event.event_id}: unsupported time_precision")
        if not event.summary.strip():
            errors.append(f"{event.event_id}: summary is required")
        if event.evidence_state not in EVIDENCE_STATES:
            errors.append(f"{event.event_id}: unsupported evidence_state")
        if not isfinite(event.confidence) or not 0 <= event.confidence <= 1:
            errors.append(f"{event.event_id}: confidence must be within 0..1")
        if not event.source_ids or any(not value.strip() for value in event.source_ids):
            errors.append(f"{event.event_id}: at least one non-empty source_id is required")
        if len(set(event.source_ids)) != len(event.source_ids):
            errors.append(f"{event.event_id}: duplicate source_id")
    for event in by_id.values():
        for field_name, refs in (("related_ids", event.related_ids),
                                 ("causal_hypotheses", event.causal_hypotheses)):
            for reference in refs:
                if reference == event.event_id:
                    errors.append(f"{event.event_id}: self-reference in {field_name}")
                elif reference not in by_id:
                    errors.append(f"{event.event_id}: unresolved {field_name} reference {reference}")
    errors.extend(_cycle_errors(by_id))
    return errors


def _cycle_errors(events: dict[str, NineCircEvent]) -> list[str]:
    state: dict[str, int] = {}
    errors: list[str] = []

    def visit(key: str, trail: list[str]) -> None:
        if state.get(key) == 2:
            return
        if state.get(key) == 1:
            errors.append("causal-hypothesis cycle: " + " -> ".join(trail + [key]))
            return
        state[key] = 1
        for parent in events[key].causal_hypotheses:
            if parent in events:
                visit(parent, trail + [key])
        state[key] = 2

    for key in events:
        if state.get(key, 0) == 0:
            visit(key, [])
    return errors


def chronological_atlas(events: Sequence[NineCircEvent]) -> list[NineCircEvent]:
    errors = validate_atlas(events)
    if errors:
        raise ValueError("; ".join(errors))
    return sorted(events, key=lambda item: (item.earliest_year, item.latest_year, item.event_id))


def overlapping_intervals(
    events: Sequence[NineCircEvent]
) -> list[tuple[str, str, float]]:
    """Return intervals that intersect; overlap is not evidence of common cause."""
    ordered = chronological_atlas(events)
    result: list[tuple[str, str, float]] = []
    for index, left in enumerate(ordered):
        for right in ordered[index + 1:]:
            if right.earliest_year > left.latest_year:
                break
            overlap = min(left.latest_year, right.latest_year) - max(
                left.earliest_year, right.earliest_year
            )
            if overlap >= 0:
                result.append((left.event_id, right.event_id, overlap))
    return result
