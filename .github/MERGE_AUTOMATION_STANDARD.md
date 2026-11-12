# GitHub Merge Automation Standard

**Scope:** this repository and its project-specific architecture. This standard governs integration and release safety; it does not impose a shared application architecture, language, directory layout, or build system.

## 1. Source of truth
- Discover the repository's default branch from GitHub metadata. Use that configured branch, not an assumed name, as the integration target.
- Product, CI, security, and documentation changes go through topic branches and pull requests.
- The default branch is canonical current state; the PR head is the incoming change set.
- Never force-push or use an administrative bypass to make a PR appear mergeable.

## 2. Branch and PR discovery
Before changing or merging, inventory the default-branch head SHA, open/draft/closed/merged PRs, head/base refs and SHAs, changed paths, patch size, reviews, required checks, mergeability, and overlapping PRs. Do not infer duplication from titles or branch names alone. Cross-repository changes must be checked against each project's own code, tests, and release contract.

## 3. Safe conflict resolution
Resolve conflicts per file and semantic unit, never by blindly selecting all current-side or all incoming-side changes.
1. Re-read base and incoming versions, surrounding code, tests, and project invariants.
2. Preserve valid behavior from both sides when compatible.
3. Keep established base contracts unless the PR explicitly and safely changes them.
4. Regenerate lockfiles and generated artifacts only with the repository's declared toolchain.
5. Rerun focused tests and complete required CI after conflict resolution.
6. When intended behavior cannot be established, leave the conflict unresolved and request a human decision.
A conflict-free textual merge is not proof of a correct semantic merge.

## 4. Merge-readiness gate
A PR is eligible only when it is open, non-draft, mergeable, its latest head SHA is unchanged since inspection, every required check passes on that head, required reviews are satisfied, no active changes-requested review remains, review threads are resolved, security scans and project-specific build/test/package/release gates pass, and the merge method is permitted. Pending, skipped, cancelled, missing, or unknown checks do not pass. Never require a status before it has emitted successfully on a PR in this repository.

## 5. Merge execution
Prefer the repository's permitted linear-history method (squash or rebase where configured). Enable auto-merge only after all gates are configured and verified. Re-check the current head SHA immediately before merge and use an expected-head-SHA guard where supported. Never bypass failed checks with admin privileges. Preserve release tags, published artifacts, migrations, and compatibility guarantees unless the PR explicitly owns those changes.

## 6. Old-PR rehabilitation
Classify each open PR as ready, needs-rebase, conflict, checks-failing, review-blocked, draft/incomplete, duplicate, superseded, or stale-but-valuable. Merge only unique reviewed changes that pass the gate. Rebase only after confirming the new base cannot erase project work. Close duplicates/superseded PRs only after identifying a replacement and confirming no unique commits or review decisions are lost. Never close or delete branches merely due to age.

## 7. CI and security
Use least-privilege workflow permissions and concurrency groups. Analyze languages actually present; select CodeQL build modes per language and actual project build system. Use none for supported languages when buildless analysis is adequate, autobuild only when reliably detectable, and manual only with verified repository-specific commands. Run secret scanning on PRs, default-branch pushes, and a schedule. Keep Actions dependencies under Dependabot. Do not claim a scan or GitHub setting is enabled until its run or setting is verified.

## 8. Architecture preservation
This policy is shared; implementation is not. Each repository retains its own languages, targets, CI matrix, packaging, release process, and module boundaries. Shared automation adapts to existing project contracts rather than rewriting them.
