# Engineering Standard

**Standard ID:** PERSONA-ENG-STD · **Version:** 1.0.0  
**Scope:** minimum cross-ecosystem engineering controls; see `.engineering/profile.json` for this product's local overlay.

## 1. Precedence and preservation
This standard does not impose a shared runtime, language, build system, folder layout, API, release cadence, or product roadmap. Preserve this repository's identity, established module boundaries, public contracts, native tooling, licenses, platform assumptions, and documented safety limits. The local profile is authoritative for product-specific constraints; narrower safety limits always win.

## 2. Architecture and integration
- Do not refactor architecture solely to create visual or structural uniformity.
- Do not introduce cross-repository imports, shared process state, privileged access, or dependencies by implication.
- Integrate only through explicit, documented, versioned contracts and adapters.
- Prefer additive and backward-compatible changes. Breaking changes require rationale, migration notes, impact analysis, and independent review.
- Keep experimental, partial, host-tested, target-qualified, and released capabilities distinct.

## 3. Change control
- Use focused topic branches and Pull Requests; keep each change independently reviewable.
- Describe intent, affected modules/contracts, alternatives, compatibility, risk, verification, documentation, and rollback.
- Review the entire diff. Resolve merge conflicts by understanding file semantics; never accept incoming/current wholesale as a substitute for analysis.
- Do not bypass failing checks, required reviews, protected-branch rules, or repository policy.
- Never report a PR as merged, a feature as released, or a deployment as successful until confirmed.

## 4. Verification and evidence
- Run the native checks relevant to the change, using this repository's documented commands and existing workflows.
- Add positive, negative, boundary, and regression tests for behavior changes.
- Test the current PR head and record exact commands and outcomes.
- Host tests, emulators, simulations, static analysis, and diagrams prove only what they actually exercised; none imply physical-target qualification.
- Mark unavailable checks as not run, explain why, and identify residual risk. Never fabricate test output, benchmark data, coverage, or capability claims.

## 5. Security, privacy, and supply chain
- Apply least privilege to workflows and application capabilities; new workflows default to read-only.
- Never commit secrets, private data, credentials, or machine-specific paths.
- Review dependency versions, licenses, provenance, and known vulnerabilities.
- Validate external inputs, manifests, downloaded artifacts, and inter-repository data before use.
- Destructive operations require exact target identification, explicit confirmation, bounded scope, and recovery instructions.
- Do not infer permission to upload, transmit, or collect local data.

## 6. Documentation, release, and operations
- Update docs when behavior, API, config, commands, supported targets, data flow, or operational procedures change.
- Keep examples executable or clearly illustrative; state limitations and non-goals beside claims.
- Record significant design decisions in the repository's established ADR/design location.
- A merge is not a release. Releases require applicable native checks, compatibility disclosure, dependency review, known-issue disclosure, and an appropriate recovery path.
- Maintain independent versioning and release decisions for independent products.

## 7. Required evidence gates
Each material change addresses: profile validation; native project checks; architecture/compatibility review; security/privacy review; documentation review; human review; and target qualification when applicable. “Not applicable” requires a reason.

## 8. Status vocabulary
- **PROPOSED:** suggested, not implemented.
- **PLANNED:** accepted for future work, not implemented.
- **IMPLEMENTED:** code/configuration exists; verification may be pending.
- **TESTED:** named tests ran and passed; test scope is stated.
- **VERIFIED:** stated acceptance criteria have evidence.
- **MERGED:** present in the target branch.
- **RELEASED:** a versioned release was published.
- **BLOCKED:** stopped by an identified dependency, failure, or decision.

Statuses are not interchangeable. A design, open PR, metadata check, or host test is not a product release or hardware qualification.

## 9. Ternary review model
**-1 / reject:** regression, unsafe boundary, failed invariant, or insufficient evidence.  
**0 / hold:** unknown or incomplete; gather evidence.  
**+1 / accept:** acceptance criteria pass and required review is complete.  
This score never overrides mandatory gates or human approval.

## 10. Definition of Done
Implementation, relevant native checks, recorded evidence, security and compatibility review, accurate documentation, complete diff review, and required approvals must be complete. Missing target evidence remains an explicit limitation.

## 11. Enforcement boundary
The `Engineering Standard / profile-validation` workflow validates governance metadata only. Existing project workflows remain responsible for builds and tests. Administrators must make this check and applicable native checks required in branch protection/rulesets for GitHub to block merges. This change does not silently modify branch protection.
