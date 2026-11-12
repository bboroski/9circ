# 9circ desktop architecture

## Product role

9circ is a local-first desktop studio for repository inventory, evidence evaluation, and human-reviewed improvement planning. It remains an independent research and extension environment; registering multiple repositories does not impose a common stack, build system, or release policy.

## Runtime

- UI: Python Tkinter / ttk.
- Runtime baseline: Python 3.11+.
- Runtime dependencies: Python standard library only.
- Entry points: run_9circ.py, python -m ninecirc, or the installed 9circ command.
- Persistence: the current user's application data directory.
- Network: no network client is included in the desktop runtime.

## Module boundaries

| Module | Responsibility | Boundary |
|---|---|---|
| app.py | Navigation, repository selection, matrix display, report export | UI only |
| audit.py | Bounded local inventory and triadic evaluation | Read-only; no source parsing or code execution |
| system.py | Point-in-time host information | Read-only; no continuous monitoring |
| store.py | Repository registry and local activity log | User-level data directory only |

## Three-stage triadic matrix

Each stage has three independent axes. States use ternary values:

- READY (+1): a check has concrete local evidence.
- REVIEW (0): evidence is absent, incomplete, or needs a human decision.
- BLOCKED (-1): a hard safety or correctness gate prevents progression.

### Stage 1 — Observe

Collect file names, counts, likely languages, manifests, tests, docs, CI markers, security policy markers, and license markers. Skip common dependency/build directories, avoid symlinks, and cap scan depth and file count.

### Stage 2 — Evaluate

Compare inventory signals with the repository's declared purpose. Review project entry points, tests, README, CI, and governance. A missing marker is a prompt for review, not proof that a repository is defective.

### Stage 3 — Propose

Produce findings for human review. The stage does not apply patches, write files into a repository, or change OS settings. Any future change engine must bind approval to an exact diff and validation result.

## Repository uniqueness

A registry entry stores a local path, display name, and independent profile label. It does not copy sibling repository dependencies, release rules, or architecture. Cross-repository coordination must use explicit, versioned contracts and remain opt-in.

## Future extension gates

Potential follow-on capabilities include isolated test execution, patch previews, SBOM generation, dependency analysis, benchmark collection, and signed report exchange. They require separate platform scope, threat models, tests, and opt-in boundaries. They are not enabled by this MVP.
