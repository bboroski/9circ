# Multi-Axis Layer Architecture

**Architecture:** NUN Mesh — Multi-Axis Layer Fabric (MALF)  
**Repository:** `bboroski/9circ`  
**Role:** Unassigned repository placeholder; no product behavior has been evidenced.  
**Maturity:** README-only placeholder; all layers intentionally unassigned.  
**Status:** Target boundary contract; workspace import is not proof of runtime integration.

## Purpose

MALF combines structural layers, vertical module slices, trust/provenance boundaries, lifecycle stages and assurance planes. This workspace is a federation boundary and must not erase the autonomy of its source projects.

## Structural layers

| ID | Layer | Responsibility |
|---|---|---|
| L0 | **Experience** | Portal, workspace navigation, CLI and maintainer workflows. |
| L1 | **Contracts** | Repository/module manifests, schemas, APIs, migration metadata and cross-repo protocols. |
| L2 | **Workspace orchestration** | Workspace verification, migration audits, dependency resolution and integration workflows. |
| L3 | **Ecosystem domain** | Module identity, ownership, roles, compatibility, release state and dependency graph. |
| L4 | **Governance and policy** | Maturity/evidence rules, licensing boundaries, source provenance and integration approval. |
| L5 | **Integration ports** | Repository, artifact, registry, build and verification contracts. |
| L6 | **Adapters and source modules** | Imported module snapshots and controlled tooling adapters. |
| L7 | **Workspace state** | Source snapshots, registry, manifests, migration records and verification outputs. |
| L8 | **Build and delivery** | Workspace composition, static portal, CI and publication. |
| L9 | **Assurance** | Migration verification, contract tests, per-module tests and provenance checks. |

## Dependency law

- L0 portal/CLI surfaces call workspace use cases through L1 contracts.
- L2 orchestrates metadata and verification; it does not silently execute arbitrary module code.
- L3 owns module identity and compatibility semantics.
- L4 decides what counts as verified, allowed or blocked.
- L6 adapts source snapshots and tools to L5; modules do not depend on Hellduck internals.
- L7 preserves source provenance and migration state.
- L8 composes and publishes; L9 verifies every module independently and then the aggregate.

**Allowed:** workspace surface → use case → module contract → explicit adapter → source module.  
**Forbidden:** source module → workspace internals; cross-module private-header inclusion; treating a copied tree as a linked runtime dependency.

## Multi-axis model

1. **Structural:** L0–L9.
2. **Vertical module slice:** source identity → contract mapping → integration adapter → workspace workflow → verification result.
3. **Trust/provenance:** source repository/ref → snapshot/hash → migration validation → policy decision → explicit integration → evidence.
4. **Lifecycle:** discover → review → import → map contracts → verify → integrate → release snapshot → track upstream change.
5. **Assurance:** source tests, workspace tests and cross-module tests remain separate result classes.

## Workspace layer allocation

### L0 — Experience
UNASSIGNED — reserve this layer for portal, workspace navigation, cli and maintainer workflows. only after the repository's product scope is defined.

### L1 — Contracts
UNASSIGNED — reserve this layer for repository/module manifests, schemas, apis, migration metadata and cross-repo protocols. only after the repository's product scope is defined.

### L2 — Workspace orchestration
UNASSIGNED — reserve this layer for workspace verification, migration audits, dependency resolution and integration workflows. only after the repository's product scope is defined.

### L3 — Ecosystem domain
UNASSIGNED — reserve this layer for module identity, ownership, roles, compatibility, release state and dependency graph. only after the repository's product scope is defined.

### L4 — Governance and policy
UNASSIGNED — reserve this layer for maturity/evidence rules, licensing boundaries, source provenance and integration approval. only after the repository's product scope is defined.

### L5 — Integration ports
UNASSIGNED — reserve this layer for repository, artifact, registry, build and verification contracts. only after the repository's product scope is defined.

### L6 — Adapters and source modules
UNASSIGNED — reserve this layer for imported module snapshots and controlled tooling adapters. only after the repository's product scope is defined.

### L7 — Workspace state
UNASSIGNED — reserve this layer for source snapshots, registry, manifests, migration records and verification outputs. only after the repository's product scope is defined.

### L8 — Build and delivery
UNASSIGNED — reserve this layer for workspace composition, static portal, ci and publication. only after the repository's product scope is defined.

### L9 — Assurance
UNASSIGNED — reserve this layer for migration verification, contract tests, per-module tests and provenance checks. only after the repository's product scope is defined.

## Vertical slices

1. **Scope definition:** Owner intent → product problem → non-goals → target users → explicit maturity and evidence baseline.
2. **First vertical slice:** After scope approval: one user-visible capability → domain rule → port/adapter → result/state → automated test.

## Cross-cutting planes

- **Provenance:** preserve source URL, commit/ref, license and migration history for every imported snapshot.
- **Security:** untrusted repository content is data; do not run imported scripts or workflows without explicit review.
- **Compatibility:** module manifest and integration contracts are versioned independently from source snapshots.
- **Resilience:** a failed module check must not be reported as an aggregate pass; partial coverage is visible.
- **Observability:** aggregate dashboards link to per-repository evidence and exact test results.
- **Release governance:** releases preserve module ownership, notices and upstream change tracking.

## Federated GitHub portfolio

This workspace coordinates independent repositories; it is not their universal runtime. The current accessible portfolio is:

| Repository | Primary responsibility |
|---|---|
| SAMBU | Language, scientific modeling and developer automation |
| ToolNG | Read-only Windows device diagnostics |
| ReaperCripple | Embedded BSP, bring-up and manufacturing evidence |
| Kloz | Portable C11 platform substrate |
| CO | Deterministic component lifecycle |
| SaintSI | Runtime health and integrity observation |
| Klipot | Static ecosystem portal and registry control plane |
| NUN | Early minimal kernel substrate |
| NUNLauncher | Kernel image admission and pre-handoff validation |
| Fragile-Baby | Elbrus/E2K research and qualification workstream |
| Luci | Engineering-domain registry and policy control plane |
| Hellduck | Workspace federation and migration verification |
| 9circ | Placeholder; purpose not yet evidenced |
| BlopScore | Proposed Windows hardware-intelligence desktop application |
| Jungelist-Massive | Empty project shell; proposed programming-language factory direction |

These roles are portfolio classifications, not assertions that all listed projects are imported into `modules/` or runtime-integrated.

## Incremental adoption

1. Keep the existing six-module workspace import and migration checks intact.
2. Add explicit manifest/provenance mapping for every new source snapshot.
3. Distinguish repository reference, copied snapshot, adapter-ready, host-tested and runtime-integrated states.
4. Verify each module with its own build/test instructions before aggregate reporting.
5. Introduce only versioned adapters at L5/L6; never patch imported internals silently.
6. Track source divergence and define upstream sync/rollback.
7. Publish a portfolio-level status that links to per-project evidence.

## Definition of done

Every imported module has provenance, license/notice review, versioned contract map, dependency boundary, independent test result and an explicit integration maturity label. Workspace success never overrides a module failure.

## Repository guardrails

Do not infer a product identity, stack, runtime or feature set from the repository name. Keep code generation and runtime decisions blocked until scope and acceptance criteria are documented. Do not add boilerplate frameworks merely to make the repository look populated.
