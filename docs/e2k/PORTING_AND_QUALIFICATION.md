# Elbrus E2K portability and qualification profile

**Repository:** bboroski/9circ  
**Status:** engineering plan; implementation and target qualification are not implied.

## Project-specific adaptation
Federation and adapter-contract integration project

Keep adapters contract-first and non-executing by default. Add E2K metadata only where relevant; validate schema compatibility and artifact identity without importing or executing remote repository code.

## Engineering rules
- Record CPU/stepping, board, OS/kernel, ABI, LCC version, sysroot, linker/libc, flags and source revision. Probe flags; do not assume GCC options or semantics are supported by LCC.
- Separate host build, cross-build, emulator and physical E2K execution. Host success is not target evidence.
- Optimize measured hot paths only; inspect emitted assembly/VLIW bundles and record repeatable target timing/PMU data. No unmeasured performance claims.
- Apply restrict only with a real non-aliasing contract; derive alignment from target documentation. Do not assume 128-byte cache lines, fixed VLIW width, APB, register names or protected mode without exact manuals/toolchain evidence.
- Static/monolithic linking is optional. Preserve dynamic libraries, IPC, process isolation and OS services when required for security, plugins, licensing, reliability or independent updates.
- Keep portable reference paths, differential/bounds/overflow tests and capability gates. Fast-math, unrolling and branchless transforms require semantic validation.
- Real-time claims need WCET methodology and scheduler/interrupt/contention assumptions. Security claims need a threat model and evidence for the exact CPU/OS/compiler mode.

## Qualification gates
| Gate | Evidence |
|---|---|
| Inventory | Component map, language/runtime, dependencies, applicability |
| Baseline | Reproducible host build, tests and workload metadata |
| Toolchain | Exact LCC/sysroot/ABI manifest and compile/link smoke test |
| Native slice | Portable hot path, reference implementation and E2K differential tests |
| Optimization | Assembly inspection and repeatable target measurements |
| Integration | Optional backend, versioned adapter and fallback |
| Hardware | Target identity, logs, hashes, correctness and performance evidence |

Benchmark records include hardware, OS/kernel, compiler/linker, flags, commit, artifact SHA-256, input hash, repetitions, timing distribution, correctness and execution class. CI marks unavailable E2K execution **not run**, never pass.

## Claims boundary
This document does not claim current native implementation, a requirement to merge all code into one binary, or measured performance/security gains. Flags such as -O4, -march=native, -mtune=native, -flto and -fwhole-program require toolchain probes. APB, predication, vector widths, register windows and protected-pointer modes require exact target confirmation. Documentation-only work is **planned/specification**, not **implemented**.

## Definition of done
Tie implementation claims to source, reproducible builds, tests, generated-code inspection where relevant, portable fallback and evidence appropriate to maturity.