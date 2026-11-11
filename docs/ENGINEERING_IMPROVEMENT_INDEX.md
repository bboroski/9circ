# Engineering Improvement Index

> This is a repository-specific execution map. It records the baseline and required next steps; it does not assert that an application already exists.

**Baseline snapshot:** 2026-11-11  
**Default branch:** `main`  
**Current scope:** repository bootstrap; product definition and implementation are not yet present in the baseline snapshot.

## 1. Observed baseline

- [README](../README.md): the only file in the baseline tree.
- CI: no GitHub Actions workflow was present at baseline. This change adds [documentation validation](../.github/workflows/docs.yml).
- Tests: no application test suite was present at baseline.
- Build manifest and source tree: none detected.
- Screenshots: none detected; no GUI is claimed.
- Governance: [Engineering Governance](ENGINEERING_GOVERNANCE.md) and [Technical Debt Register](TECHNICAL_DEBT_REGISTER.md) are introduced with this change.
- PR review: [Pull request template](../.github/pull_request_template.md) is introduced with this change.

The documentation workflow checks the README character limit, required governance documents and relative Markdown links. It is deliberately not labelled as an application build or application test.

## 2. Engineering sequence

1. Define product purpose, user needs, non-goals, supported platforms and acceptance criteria.
2. Select the smallest appropriate architecture and toolchain; record the decision.
3. Implement one working vertical slice with explicit inputs, outputs and failure behavior.
4. Add tests that exercise real behavior, including boundary and negative cases.
5. Add a CI workflow that installs the actual toolchain, runs tests and builds the real artifact.
6. Add dependency, secret, license and permission controls appropriate to the chosen stack.
7. Document installation, use, compatibility, security, troubleshooting and release procedure.
8. Add current screenshots only after a real GUI exists; otherwise use no screenshot or a clearly labelled architecture diagram.
9. Introduce performance and operational metrics only after there is a measurable application to observe.

## 3. Universal engineering rules

Preserve history and avoid destructive cleanup. Keep modules focused, dependencies minimal, errors explicit, and data/API contracts versioned. Validate untrusted input, authorization and filesystem boundaries. Never commit secrets or personal data. Keep automation least-privileged and make each check fail on a real defect. Do not mark planned, partial or mocked behavior as production-ready.

Use isolated branches and focused PRs. Include intent, scope, evidence, compatibility impact, risk, migration and rollback. Do not merge with failed, missing or pending required checks. Do not bypass protections or fabricate test results.

Keep root README at or below 5,000 characters. Use truthful support claims, real commands and a small number of relevant cross-links. Keep screenshots current and authentic. End the README with a correctly translated Chinese quotation about love.

## 4. Definition of Done

A product change is complete only when its acceptance criteria, implementation, relevant tests, applicable CI checks, security review, compatibility and documentation are all verified. For the current bootstrap state, completion of the first product milestone additionally requires a documented scope, runnable application behavior, a real test suite and an application build pipeline.

**Current status:** repository governance and documentation checks are being established. Product architecture, application behavior, API, data model, runtime security, performance and operational readiness remain **not assessed** until a real product scope and implementation exist.
