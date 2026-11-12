# 9circ architecture

## Runtime boundaries

9circ is a single repository with three language-owned modules:

- C# owns clustering, feature-space normalization, dependency scoring, storage clients, API contracts and telemetry instruments.
- Swift owns the file-backed mmap ring buffer and direct POSIX stream adapters.
- Ruby owns native component lifecycle, safe hot-swap coordination and the shared IPC header codec.

The shared-memory contract is documented in ipc.md. Payload data is not serialized through JSON between language runtimes. The 32-byte metadata header is little-endian and payload bytes remain in the mapped region.

## Data plane

Raw input enters the Swift ring buffer. The C# worker consumes a validated frame and performs DBSCAN over a contiguous row-major float matrix using caller-owned workspace spans. Documents are persisted with PostgreSQL; vectors are written to Qdrant through its HTTP API. Redis is the distributed cache and in-memory caches are intended for short-lived local entries.

## Control plane

The Ruby component manager loads a replacement native module before publication, atomically swaps the active slot under a mutex and lets in-flight leases finish on the old component. This is a logical hot swap: the manager does not promise that the operating system unmaps a shared library immediately after the last lease is released.

The motivation graph converts measured throughput, latency, errors and resource pressure into bounded priority hints. It is not an operating-system scheduler and does not grant CPU time or bypass cgroups/Kubernetes quotas.

## Creative code evolution

Tree-sitter adapters implement ITreeSitterParser for C#, Ruby and Swift. The current C# planner compares normalized AST declaration bodies and emits reviewable refactoring proposals. Native grammar bindings, patch application and isolated execution are separate adapters and must be added before generated changes are allowed to run. Proposals are not automatically applied.

## Reliability principles

- Every shared-memory frame has a version, length, sequence and CRC field.
- Buffer operations are bounded and report partial writes/reads rather than silently dropping data.
- API requests have point-count and dimensionality limits.
- Native modules are loaded before becoming active; failed initialization leaves the active slot unchanged.
- Production secrets are injected by the deployment environment and are never committed.
- Cluster weights are advisory and constrained to bounded numeric ranges.

## Current implementation status

This commit adds the project foundation, DBSCAN core, matrix interpolation, motivation graph, shared IPC header, PostgreSQL/Qdrant/Redis adapters, Swift mmap buffer, Ruby FFI lifecycle manager, API scaffold, migration, local service stack and CI pipeline. Production-grade eBPF probes, concrete Tree-sitter grammar bindings for all languages, full corpus ingestion workers, artifact registry/rollback orchestration, OTLP exporters, distributed locking and production deployment credentials remain follow-up work.
