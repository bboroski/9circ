# 9circ

9circ is a three-runtime code/data processing platform built around C# core services, a Swift memory-mapped I/O layer and a Ruby native-component lifecycle manager.

## Repository layout

- src/9circ.Core — allocation-aware clustering, interpolation, motivation graph, IPC codec, telemetry, PostgreSQL/Qdrant/Redis adapters and corpus interfaces.
- src/9circ.Api — bounded HTTP entry points for clustering, motivation graph management/feedback and health checks.
- modules/buffer-swift — mmap-backed ring buffer and direct POSIX read/write helpers.
- modules/lifecycle-ruby — FFI native module loader, lease-based hot reload and IPC v1 codec.
- tests/9circ.SmokeTests — dependency-light C# smoke tests.
- migrations/postgres — document, artifact-manifest and motivation-event tables.
- docker-compose.yml — local PostgreSQL, Qdrant and Redis services.
- k8s — hardened API Deployment and Service example.
- .github/workflows — multi-language CI and main-branch container publication to GHCR.

## Requirements

- .NET SDK 10.0.100 or a compatible 10.0 feature-band SDK.
- Ruby 3.4 with Bundler.
- Swift 6 toolchain.
- Docker Engine with Compose v2.

## Local development

Copy .env.example to .env and replace the local development credentials, then start dependencies:

    docker compose up -d --wait

Build and run the API:

    dotnet build src/9circ.Api/9circ.Api.csproj -c Release
    dotnet run --project src/9circ.Api/9circ.Api.csproj

Run C# smoke checks:

    dotnet run --project tests/9circ.SmokeTests/9circ.SmokeTests.csproj -c Release

Run Swift tests:

    swift test --package-path modules/buffer-swift

Run Ruby tests:

    cd modules/lifecycle-ruby
    bundle install
    bundle exec ruby -Itest test/test_ninecirc.rb

The API exposes GET /healthz, GET /readyz, POST /api/v1/clusters, GET /api/v1/motivation, POST /api/v1/motivation/nodes, POST /api/v1/motivation/dependencies and POST /api/v1/motivation/feedback. The clustering endpoint accepts a flat row-major float matrix, dimensions, epsilon and minPoints.

## Runtime contracts

The shared IPC header is 32 bytes, little-endian, version 1. Its field layout and synchronization requirements are defined in docs/ipc.md. The metadata codec is implemented in C#, Swift and Ruby. Cross-process locking and crash recovery are not yet implemented by the Swift ring buffer; its current lock protects threads in one process only.

The C# DBSCAN routine accepts caller-owned spans for labels, visited flags, queue and queued flags. It avoids managed allocations in its clustering hot path. The agglomerative centroid engine also uses caller-owned workspace. Both algorithms are CPU-bound; DBSCAN has quadratic worst-case work and API request limits are enforced.

Ruby hot reload initializes a candidate before swapping it into service. Existing leases keep the previous component callable until released. Native shared-library unmapping is controlled by the FFI runtime/GC and is not promised to happen immediately.

## Integration boundaries and non-goals of this foundation

Concrete Tree-sitter grammar bindings for all three languages, a production embedding model adapter, eBPF kernel probes, a sandbox execution service for generated code, a cross-process lock-free queue, OpenTelemetry exporters/collector configuration, signed artifact publication, production secret injection and an operational production cluster are not included yet. Interfaces, schemas, documentation or deployment templates may be present for those follow-up integrations, but they must not be treated as production-complete.

Generated code is never executed or applied automatically. Refactor suggestions are review-only until a disposable sandbox evaluator and approval gate are installed.

## CI/CD

Pull requests and pushes run the .NET, Ruby, Swift, IPC, integration-stack, vulnerability, container and documentation checks. Merges to main publish a multi-architecture API image to ghcr.io/bboroski/9circ-api with commit-addressed and latest tags, plus SBOM/provenance metadata. This publishes an image; it does not deploy to a production Kubernetes cluster. A cluster endpoint and deployment credentials have not been supplied.

## Security

Do not use the development credentials from docker-compose.yml in production. Use a secret manager, enable authentication/TLS for data services, restrict network exposure and deploy signed images by immutable digest. Review docs/security.md and docs/operations.md before deployment.
