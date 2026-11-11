# Swift 6+ Modular-Monolith Adoption Contract

**Status:** architecture baseline; implementation is incremental and must be proven by repository CI.
**Language mode:** Swift 6 (pin the exact Swift toolchain in CI).

## Objective

Use a high-performance in-process Swift core where this repository's runtime, deployment model, and target platform support it. Keep module boundaries explicit with SwiftPM targets and typed APIs. Do not convert an independent repository or hardware/OS boundary into an in-process dependency merely to satisfy a monolith slogan.

## Mandatory engineering rules

1. Enable Swift 6 language mode and complete strict-concurrency checking per target. Resolve diagnostics rather than blanket-suppressing them.
2. Model shared mutable state with actor isolation or narrowly scoped synchronization. Treat every `@unchecked Sendable`, unsafe pointer, C/C++ bridge, and global mutable as a reviewed safety boundary with tests and an owner.
3. Use `Sendable` only where values genuinely cross isolation domains. Non-Sendable values remain within their owning actor/task; do not claim they are physically unable to leave a module.
4. Use value semantics by default. Introduce `~Copyable`, `borrowing`, and `consuming` only where the pinned compiler supports the required feature and a measured resource-lifetime benefit exists.
5. Organize Swift code into SwiftPM targets (Domain, Application, Infrastructure, Adapters, Tests) with dependency direction toward Domain. Avoid cyclic package dependencies and global singleton service locators.
6. Keep network, process, device, privilege, and machine boundaries where they provide fault containment, security, portability, or independent lifecycle. Replace only unnecessary *in-process* HTTP/JSON hops with typed calls.
7. Preserve existing public APIs, ABI, file formats, boot contracts, and cross-language interfaces. Any ABI/schema change requires an explicit version, compatibility tests, and migration notes.
8. Persistence remains durable: use transactions, WAL/checkpoint policy, crash-recovery tests, and explicit backup/restore. Embedded SQLite is an option for a single-node local store, not a universal replacement for shared/distributed storage.
9. Shutdown must stop accepting work, cancel owned task groups, drain/close owned transports, flush durable state, and report incomplete cleanup. Do not assume cancelling a task group terminates unrelated actor work.
10. Benchmark before and after. Record compiler/toolchain, target hardware, workload, p50/p95/p99 latency, throughput, allocations, and memory. Do not publish theoretical call-latency ratios as measured results.
11. Enable cross-module optimization/LTO only in supported release configurations after correctness and reproducibility checks. Do not impose one linker flag across unsupported platforms/toolchains.
12. CI must build and test every supported target, run Swift 6 strict-concurrency checks, test native/FFI boundaries, and publish artifacts with reproducible toolchain metadata.

## Adoption sequence

- **A. Inventory:** map languages, deployables, module graph, public interfaces, persistence, unsafe code, and platform constraints.
- **B. Core boundary:** identify the smallest stable Swift domain API; define versioned DTOs only at genuine process/network boundaries.
- **C. Concurrency:** migrate target-by-target to Swift 6; eliminate unreviewed unsafe sendability and data races.
- **D. Native interop:** isolate C/C++ behind Clang modules or a narrow C ABI where direct C++ interop is unavailable or unsuitable; test ownership and error propagation.
- **E. Storage and lifecycle:** choose embedded versus external persistence from durability and multi-writer requirements; implement orderly startup/shutdown.
- **F. Optimization:** profile, benchmark, then selectively enable LTO/CMO.
- **G. Release gate:** merge only after all required CI checks, ABI compatibility checks, and review pass.

## Repository-specific scope

9circ is a multi-language verification and orchestration project (C#, Ruby, Swift). Adopt Swift as a native core only for components with demonstrated value; retain C# and Ruby adapters and versioned cross-language contracts. Do not declare a single Swift executable until interop and deployment tests prove it.



This document is an adoption contract, not a claim that Swift code or a SwiftPM package already exists. The implementation plan must respect this repository's existing product and target role. Where Swift cannot run (for example, a bare-metal kernel target), keep the native kernel implementation and use Swift only in supported host-side tools, validation, or orchestration.

## Acceptance criteria

- A checked-in toolchain pin and reproducible SwiftPM build for each Swift target.
- Complete strict-concurrency checking with no unexplained suppressions.
- Tests for actor isolation, cancellation, persistence recovery, and native boundary ownership where applicable.
- Documented module/deployment graph and versioned external contracts.
- Benchmarks and CI evidence attached to the implementation PR; no unsupported performance or absolute race-freedom claims.
