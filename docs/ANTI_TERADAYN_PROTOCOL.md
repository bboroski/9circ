# Anti-Teradayn Protocol — 9circ

**Status:** baseline governance document; implementation profile is not yet verified from the repository's current README.  
**Scope:** 9circ only. This document deliberately avoids asserting an unverified language stack, runtime, kernel boundary, or production capability.

## Purpose

Establish evidence-first engineering rules before expanding the project: bounded modules, explicit contracts, reproducible builds, minimal necessary dependencies, and honest capability reporting. “Typified steaming” means typed, bounded, reviewable changes—not a new runtime or a claim of zero entropy.

## Seven-phase protocol

1. **Dependency discipline.** Inventory source files, build manifests, direct/transitive dependencies, and runtime entry points before removing anything. Preserve required interfaces and replace dependencies only with tested alternatives.
2. **Corpuscular transparency.** Document module responsibilities, data flow, ownership, error handling, and public interfaces. Choose low-level languages or assembly only when the verified target and measured requirements justify them. Swift is optional, not a universal bridge.
3. **Driver and hardware boundaries.** Do not introduce kernel drivers or privileged operations without a concrete hardware target, documented ABI, threat model, and target test plan. Ruby is not a kernel-driver ABI.
4. **Applicable validation matrix.** First identify the actual product surfaces. Then define unit, integration, static, build, stress, emulator, and hardware checks that apply. GUI, Lua, rendering, interrupt, and device tests are conditional, not assumed.
5. **Hardened integration.** Apply least privilege, input validation, bounded timeouts/resources, explicit secrets handling, and documented cache/retention. Google services and external APIs are optional.
6. **SAMBU relationship.** Integrate SAMBU only if the codebase has a concrete scientific/statistical modeling need, using a versioned data contract. Do not add a dependency merely to satisfy ecosystem branding.
7. **Resource allocation.** Define memory, CPU, concurrency, storage, and latency budgets in measurable units. Select C/C++/C#/Swift/Ruby/Python based on verified project constraints, not a fixed language mandate or “six-molecule” metaphor.

## Typed-steaming rules

- **Never boil:** no speculative full rewrite or broad refactor without a scoped behavior change and regression coverage.
- **Never over-boil:** keep responsibilities bounded and interfaces small.
- **Never cook:** avoid hidden global state, unbounded queues, implicit network calls, and unnecessary runtime work.
- Preserve public contracts unless a versioned migration is provided.
- Make no performance or readiness claim without reproducible evidence.
- Mark unknown capabilities as **not verified**, not implemented.

## Repository-specific application

The current root README contains only the project name. Therefore the language stack, build system, architecture, runtime, tests, hardware targets, and feature maturity are **not verified by the available repository documentation**. The first engineering task is a source/build inventory; this protocol does not presume a C/C++/C#/Swift/Ruby/Python implementation or a neural-network capability.

## Acceptance checklist

- [ ] Source tree and build entry points are inventoried.
- [ ] Supported platforms, dependencies, and runtime are documented from evidence.
- [ ] Public interfaces, ownership, failure modes, and resource limits are explicit.
- [ ] Tests are mapped to real product behavior; missing target evidence is marked pending.
- [ ] README and docs describe implemented behavior only.
- [ ] Cross-repository integrations use versioned contracts and do not execute foreign code implicitly.

## Ecosystem boundary

9circ remains independently buildable and retains its own API and release lifecycle. Federation with other bboroski repositories means documented, versioned contracts—not a forced monolith or shared runtime.

---

*Make every claim testable, every boundary explicit, and every optimization measurable.*
