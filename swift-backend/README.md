# 9circ Server-Side Swift backend

A Swift 6 / Vapor service boundary for 9circ. The service is a separate deployable process; it does not replace the existing .NET host, Ruby FFI adapter, or Swift native IPC components.

## Local build

```sh
cd swift-backend
swift test
swift run ninecirc-server
```

Endpoints:
- `GET /health` — liveness response.
- `GET /ready` — process readiness only. It does not claim PostgreSQL, Redis, Qdrant, or external dependencies are healthy.
- `GET /v1/health` — versioned liveness response.

Configuration: `HOST`, `PORT`, and `SERVICE_VERSION`. Defaults are `0.0.0.0`, `8080`, and `0.1.0`.

## Concurrency and safety

The package compiles in Swift 6 language mode. DTOs and configuration are immutable `Sendable` value types. Blocking database or filesystem work must not run on SwiftNIO event-loop threads. Add database clients only with bounded pools, explicit timeouts, migrations, and integration tests.

## Production qualification still required

The current readiness endpoint checks process availability only. PostgreSQL/Redis health probes, authentication, TLS termination, OpenTelemetry export, Prometheus metrics, load tests, deployment manifests, and production secrets integration are not represented as complete. Configure these against actual infrastructure before production promotion.
