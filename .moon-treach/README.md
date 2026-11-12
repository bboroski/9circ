# MoonTreach

MoonTreach runs repository-native checks through a shared composite GitHub Action.

- Changed paths select matching suites; unknown Git history or edits to MoonTreach itself trigger every configured suite.
- Selected suites run as independent GitHub Actions matrix jobs.
- Suite commands are explicit argument arrays, time-bounded and executed without shell interpolation.
- Manual workflow dispatch supports `force_all=true`.
- No configured suite means **unverified**, not tested.

Edit `.moon-treach/config.json` to maintain the project-specific test map. The shared engine is pinned to an immutable revision of `bboroski/SAMBU`.

MoonTreach never merges PRs, changes permissions, rewrites branches, resolves conflicts automatically or bypasses branch protection. Its merge-evidence report is advisory; GitHub required checks and human review remain authoritative.

Host-side tests do not imply physical-device or target-hardware qualification.
