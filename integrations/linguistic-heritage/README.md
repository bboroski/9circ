# Linguistic Heritage Engine integration

This repository is enrolled in the cross-repository Linguistic Heritage Engine initiative.

- Canonical research core: [bboroski/SAMBU](https://github.com/bboroski/SAMBU), package path `linguistic_heritage/`.
- Data contract: `schemas/linguistic-heritage-letter.schema.json` in the canonical repository.
- Initial case study: Cyrillic Ы / ы.
- Evidence states: `established`, `qualified`, `hypothesis`, `unsupported`.

This PR adds a declarative manifest only. It does not modify application runtime, dependencies, build scripts, secrets, or existing workflows. A project-specific adapter requires prior review of the repository's language, entry points, and test framework.

Do not promote hypotheses to facts without traceable sources. Keep grapheme history distinct from phoneme history. Do not infer borrowing from sound similarity alone.

All changes are proposed on `feature/linguistic-heritage-engine`; the default branch is not modified directly.
