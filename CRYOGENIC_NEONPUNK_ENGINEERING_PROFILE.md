# Cryogenic Neonpunk Engineering Profile

> Repository: `9circ`  
> System role: Experimental research and physics engineering

## Purpose

This profile translates the Cryogenic Neonpunk / Egyptian Cyber Duck concept into practical engineering constraints. The visual language is cold, precise, modular, resilient, and deliberately playful; production behavior remains conventional, observable, secure, and testable.

Own research-grade models, experimental computational methods, reproducible numerical work, and explicitly labeled exploratory capabilities. Separate hypotheses from validated results; record assumptions, units, tolerances, provenance, and limits of applicability.

## Engineering principles

1. **Cold-start clarity** — every subsystem documents inputs, outputs, lifecycle, failure modes, assumptions, and ownership.
2. **Small, bounded units** — prefer cohesive modules, explicit contracts, bounded queues and allocations, and predictable resource limits.
3. **Deterministic core** — isolate nondeterminism, make state transitions explicit, and test repeatability where applicable.
4. **Safe automation** — automation is policy-controlled, idempotent where possible, auditable, and reversible. Never silently delete, overwrite, or mutate user data.
5. **Scientific integrity** — distinguish measured data, simulated output, estimates, hypotheses, and illustrative fixtures. Preserve units, uncertainty, provenance, and reproducible parameters.
6. **Measured optimization** — establish a baseline, profile real workloads, and retain changes only when tests and measurements support them.
7. **Compatibility first** — preserve public APIs, data formats, migration paths, and supported platforms unless a separately reviewed breaking change is approved.
8. **Readable implementation** — consistent naming, narrow functions, meaningful errors, minimal dependencies, and comments that explain decisions.

## Cryogenic implementation profile

- **Neonpunk** is the presentation vocabulary for developer-facing surfaces: high-contrast accents, clear state indicators, and restrained visual effects.
- **Cryogenic** means explicit resource budgets, bounded work, predictable shutdown, leak detection, and reproducible builds.
- **Cybernetic** means observable interfaces, health signals, structured logs, traceable operations, and well-defined component boundaries.
- **Egyptian Duck** is an optional identity motif for examples, demo fixtures, and non-critical UI details. It must never enter scientific semantics, protocol names, or security decisions.
- **Multiplicative scale** means composability and repeatable reuse—not claims of infinite capacity, unbounded recursion, or unchecked replication.

## Required change workflow

- Make changes in focused, reviewable commits and isolated pull requests targeting `main`.
- Add tests for behavior changed; cover edge cases, failure paths, numerical invariants, and compatibility.
- Run the repository's real formatter, linter, type checks, tests, and build. Do not invent passing results or placeholder checks.
- Document configuration, units, assumptions, reproducibility steps, operational limits, and known limitations.
- Do not add dependencies, generated binaries, secrets, fake screenshots, or destructive cleanup without a concrete need and review.
- Merge only after required status checks pass and the diff has been reviewed. Preserve branch protection.

## Acceptance checklist

- [ ] Scope is limited to this repository's research responsibility.
- [ ] Scientific claims are reproducible and appropriately qualified.
- [ ] Units, uncertainty, assumptions, and provenance are explicit where relevant.
- [ ] Tests exercise real behavior; no mock-only success claims.
- [ ] Security, privacy, and data-retention implications are reviewed.
- [ ] Documentation matches the implementation.
- [ ] CI is green and the PR is mergeable under repository policy.

## Non-goals

This profile does not authorize speculative claims, hidden background processes, recursive self-modification, uncontrolled code generation, automatic data deletion, or bypassing repository protections. Implementation decisions require evidence from the actual codebase.

---
*Engineering motto: precise as ice, adaptable as water, and harmlessly duck-shaped.*
