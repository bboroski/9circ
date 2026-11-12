# 9circ

**9circ is a polyglot platform for bounded data processing and controlled improvement.** Its native foundation combines a .NET core, Swift memory-mapped I/O, and Ruby FFI lifecycle management. A separate Swift 6 service provides an independently deployable HTTP boundary.

Each runtime has an explicit responsibility and test boundary. No single language, build system, or release process is imposed on every module.

## Capabilities

- **C# / .NET:** allocation-aware DBSCAN and hierarchical clustering, feature interpolation, motivation graph and diagnostics, bounded event dispatch, buffer leases, and storage adapters.
- **Swift 6:** file-backed mmap ring buffer, IPC header codec, and POSIX read/write adapters.
- **Ruby:** FFI component loading, ABI validation, initialize-before-swap hot reload, and lease-based retirement.
- **Services and storage:** .NET API, separate Swift/Vapor health service, PostgreSQL, Qdrant, Redis, and in-memory cache adapters.
- **Delivery:** multi-language CI, container build, Compose stack, Kubernetes examples, and release workflow.

Adapters and deployment templates do not mean external services are production-configured. See [known limitations](#safety-and-known-limitations).

## Architecture

| Area | Path | Responsibility |
|---|---|---|
| Core | `src/9circ.Core` | Clustering, motivation, IPC, corpus, storage, telemetry |
| .NET API | `src/9circ.Api` | Bounded HTTP endpoints |
| Swift I/O | `modules/buffer-swift` | mmap ring buffer and POSIX adapters |
| Ruby lifecycle | `modules/lifecycle-ruby` | FFI loading, ABI checks, component replacement |
| Swift service | `swift-backend/` | Separate Swift 6 / Vapor health API |
| Tests | `tests/`, module test folders | Smoke, contract, language-specific tests |
| Operations | `docs/`, `migrations/`, `k8s/` | IPC, security, operations, schema, deployment examples |

IPC v1 uses a 32-byte little-endian header with CRC-32; see [docs/ipc.md](docs/ipc.md). The Swift ring-buffer lock protects threads within one process, not inter-process synchronization or crash recovery.

## Requirements

- .NET SDK **10.0.100** (or compatible 10.0 feature-band SDK)
- Ruby **3.4** with Bundler
- Swift **6**
- Docker Engine and Docker Compose v2 for the local service stack

## Quick start

1. Copy `.env.example` to `.env` and replace the development credentials.
2. Start local dependencies:

   ```sh
   docker compose up -d --wait
   ```

3. Build and run the .NET API:

   ```sh
   dotnet build src/9circ.Api/9circ.Api.csproj -c Release
   dotnet run --project src/9circ.Api/9circ.Api.csproj
   ```

4. Run language checks:

   ```sh
   dotnet run --project tests/9circ.SmokeTests/9circ.SmokeTests.csproj -c Release
   swift test --package-path modules/buffer-swift
   cd modules/lifecycle-ruby
   bundle install
   bundle exec ruby -Itest test/test_ninecirc.rb
   ```

The .NET API exposes `GET /healthz`, `GET /readyz`, `POST /api/v1/clusters`, and motivation graph/feedback endpoints under `/api/v1/motivation`. Clustering accepts a flat row-major float matrix, dimensions, epsilon, and `minPoints`.

The separate Swift service exposes `GET /health`, `GET /ready`, and `GET /v1/health`. Its readiness endpoint currently reports process readiness only.

## CI and delivery

CI covers .NET, Ruby, Swift, IPC, integration-stack, vulnerability, container, and documentation checks. The latest reported implementation-foundation .NET and Swift-service workflow runs succeeded; check the current PR head and required checks before merging.

The release workflow can publish a container image to GHCR. This is **not** a production Kubernetes deployment; no production cluster or credentials are assumed.

## Safety and known limitations

- Imported/generated source is never executed or automatically applied. Refactor suggestions remain review-only.
- No autonomous source rewriting, privileged OS changes, or automatic production merge is enabled.
- Authentication, production TLS, secret-manager integration, dependency health probes, and production observability need deployment-specific work.
- Cross-process ring-buffer locking and abandoned-lease recovery are not implemented.
- Concrete Tree-sitter grammars, production embedding providers, eBPF probes, generated-code sandboxing, signed artifact promotion, and production-cluster operations are not complete.
- Compose credentials are local-development only; never reuse them in production.

Review [docs/security.md](docs/security.md), [docs/operations.md](docs/operations.md), and [docs/architecture.md](docs/architecture.md) before deployment.

## Project status

Foundation development is ongoing. A capability is implemented only when code, tests, workflow evidence, and its operational boundary support that claim. A green workflow validates only the jobs it ran; it is not production qualification.

## License

No license is declared yet. Add an explicit license before distributing the software or granting third parties reuse rights.
