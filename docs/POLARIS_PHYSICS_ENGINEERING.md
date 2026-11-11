# Polaris Physics Engineering (PPE)

**Status: specification / planned.** Repository purpose, language and runtime must be established before executable integration. This document defines only the shared PPE boundary; it does not assume a domain or claim implementation.

## Five subsystems
1. **Anti-corpuscular control:** detect incompatible states, duplicate work, resource contention, stale records and dependency cycles. Report conflicts; never silently delete data or cancel valid work.
2. **Corpuscular-wave model:** immutable discrete entities plus versioned events propagated over a bounded graph. Define identity, ordering, deduplication, backpressure and cancellation.
3. **Technical mechanics:** measurable resource budgets, load, queue pressure, latency, contention and state transitions. Use explicit units.
4. **Cardio-thermodynamics:** heartbeat/liveness and thermal/load telemetry are separate signals. Distinguish measured, estimated and unavailable values.
5. **Leaf-flight mechanics:** seeded stochastic scheduling with bounded exploration, fairness and deterministic fallback.

## Safety and data contract
- Events carry ID, source, kind, schema version, monotonic tick and correlation ID.
- Metrics declare unit, sampling interval, source and confidence/status.
- Bound queues, graph depth, retries, memory and execution time.
- Unknown data stays unknown; missing telemetry is never zero.
- No destructive cleanup, remote execution, kernel writes or device mutation is implied.
- APIs are opt-in and backward compatible; experimental modules use feature flags.

## Conformance tests
Deterministic replay; duplicate/out-of-order events; overflow, cancellation and backpressure; state invariants and cycle detection; resource bounds/timeouts; dimensional checks; benchmarks against recorded baselines.

## Delivery gates
`planned` → `partial` → `implemented` only with code, tests and appropriate benchmark/evidence. First inspect and document repository architecture before selecting an executable implementation.
