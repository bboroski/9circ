# 9circ implementation roadmap

## Iteration 1 — Desktop foundation

- Cross-platform Tk desktop shell.
- Local repository registry with independent profiles.
- On-demand read-only host snapshot.
- Bounded repository inventory.
- Three-stage / three-axis matrix.
- Local activity log and JSON export.
- Unit tests and cross-platform CI.

## Iteration 2 — Evidence and proposal quality

Candidate capabilities, not yet implemented:
- Stable finding identifiers, severity, and evidence references.
- Repository-specific acceptance profiles.
- Optional read-only dependency and license metadata parsers.
- Benchmark adapters requiring explicitly selected commands.
- Patch preview and exact-diff approval records.
- Reproducible audit bundles with checksums.

## Iteration 3 — Controlled multi-repository coordination

Candidate capabilities, not yet implemented:
- Explicit repository enrollment and removal.
- Signed, versioned event envelopes.
- Opt-in report exchange with data minimization.
- Per-repository policy adapters and independent release gates.
- Conflict-aware proposal coordination without remote code execution.

## Permanent gates

- No self-modification of privileged policy.
- No autonomous writes to host OS or installed applications.
- No unreviewed source rewrite or merge.
- Unknown evidence is never presented as success.
- No capability is marked VERIFIED without reproducible evidence.
