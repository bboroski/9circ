# Satan — Distributed Repository Sanitation

Satan is a lightweight, repository-local review assistant. Each repository runs the same baseline policy while retaining its own language, architecture, and engineering conventions.

## Purpose
Reduce avoidable information noise and surface maintainability risks without suppressing disagreement, legitimate technical debate, creativity, or justified complexity.

## Modules
- **Linguistic Noise Reducer:** flags obvious placeholders and low-information residue in changed lines.
- **Over-Engineering Review:** highlights unusually large change sets for human decomposition review; it does not infer that abstraction is inherently bad.
- **Legacy Fallacy Shield:** flags appeals to tradition when used instead of evidence.
- **Temporary Workaround Watch:** asks for ownership, rationale, and a removal condition.
- **Auditability:** findings are GitHub Actions annotations tied to changed files and lines.

## Safety contract
1. Advisory by default; never rewrites or deletes source files.
2. Never blocks a merge based on tone, disagreement, writing style, or subjective complexity.
3. A finding is a review prompt, not proof of a defect.
4. Suppressions and exceptions must be documented by maintainers.
5. Workflow uses read-only repository permissions.
6. Skips common binary, generated, vendor, and lock artifacts.
7. Strict mode is opt-in through `SATAN_STRICT=true` after repository-specific validation.

## Integration
Workflow: `.github/workflows/satan-sanitizer.yml`. Runs on pull requests, pushes to `main`, and manual dispatch. Compares PR base to head and emits GitHub warning annotations.

## Review vocabulary
- **Bazar:** repeated, irrelevant, or placeholder content obscuring an engineering decision.
- **Azar / Azhur:** complexity or polish lacking measurable value or tests.
- **Tuzhur:** retaining an obsolete pattern solely from nostalgia.
- **Babu fallacy:** treating historical habit as sufficient technical evidence.

These are review metaphors, not labels for people. Criticism targets artifacts and claims, never contributors.

## Rollout
Start in advisory mode. Review false positives for at least two development cycles before considering strict mode. Language-specific analyzers, commit-message checks, chat integrations, central policy distribution, and cross-repository memory belong in later, separately reviewed increments.

**Nothing is rejected without a reason. Nothing is modified without an audit trail.**
