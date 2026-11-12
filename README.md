# 9circ — Local Optimization Studio

9circ is a cross-platform desktop workspace for evidence-based repository improvement. It gives each local repository its own profile, runs a bounded read-only inventory, evaluates the result through a three-stage triadic matrix, and turns findings into reviewable improvement plans.

Each repository keeps its own purpose, language, build system, and release policy. The registry is opt-in: only folders selected by the user are inspected.

## Desktop capabilities

- **Repository registry:** add/remove local folders; preserve a separate profile for each repository.
- **Stage 1 — Observe:** inventory file names, likely languages, build manifests, tests, documentation, CI, security policy, and license markers.
- **Stage 2 — Evaluate:** assess evidence, quality signals, traceability, and reproducibility.
- **Stage 3 — Propose:** create an evidence-based improvement plan with human-review gates.
- **System profile:** on-demand snapshot of OS, architecture, CPU count, memory, and free disk space.
- **Activity:** local event history and JSON report export.

## Triadic matrix

Each stage evaluates three axes. States are ternary:

| State | Value | Meaning |
|---|---:|---|
| READY | +1 | Verifiable supporting evidence exists |
| REVIEW | 0 | Evidence is incomplete or a human decision is needed |
| BLOCKED | -1 | A safety/correctness gate prevents progression |

The matrix is an evidence tracker, not a self-authorizing agent. A score never authorizes a code or system change.

## Safety and privacy

- Repository inspection is local and read-only.
- The scanner inventories names and metadata; it does not read application source contents.
- No shell commands, build scripts, package lifecycle hooks, or repository-defined code are executed.
- No source file is edited automatically.
- No OS registry, kernel, driver, firmware, service, or installed application is modified.
- No background polling, remote synchronization, or network telemetry is enabled.
- System information is collected only when the user opens or refreshes the System Profile.
- Local registry and activity history are stored in the current user's application data directory.

## Requirements

Python 3.11+ with Tk support. Runtime dependencies: Python standard library only. Supported desktop targets: Windows 10/11, macOS, and Linux.

## Run

~~~bash
python run_9circ.py
~~~

Or install:

~~~bash
python -m pip install .
9circ
~~~

## Test

~~~bash
python -m unittest discover -s tests -v
python -m compileall -q src tests
~~~

## Build a standalone executable

Build on the target operating system:

~~~bash
python -m pip install pyinstaller
pyinstaller --noconfirm --clean --onefile --windowed --name 9circ run_9circ.py
~~~

## Layout

~~~text
src/ninecirc/
  app.py       Desktop interface
  audit.py     Bounded read-only inventory and triadic evaluation
  store.py     Local repository registry and activity log
  system.py    On-demand host snapshot
tests/         Standard-library unit tests
docs/          Architecture, security model, roadmap
.github/       Cross-platform CI
~~~

## Implementation status

This is the first runnable desktop foundation. It does not claim autonomous OS optimization, driver generation, continuous self-modification, AI training, or production deployment. Any future change engine must be separately designed, tested, and explicitly approved.

## License

No license has been selected. Choose and add the intended license before redistributing the application or granting third parties reuse rights.
