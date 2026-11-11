# Cross-Substrate Semantic API (CSSA)

**Status:** proposed, reviewable contract; not a claim of BCI, neural decoding, memory transfer, or hardware qualification.

## Purpose

Provide a versioned, platform-neutral contract for exchanging typed digital events, semantic entities, declared intents, and capability metadata across independently implemented modules. The API is an interoperability layer, not a mechanism for connecting to or controlling a biological nervous system.

## Core envelope

```json
{
  "contract": "cssa.event",
  "version": "1.0.0",
  "message_id": "opaque-unique-id",
  "correlation_id": "optional-opaque-id",
  "occurred_at": "RFC3339 timestamp",
  "producer": { "id": "module-id", "version": "semver" },
  "subject": { "type": "domain-qualified-type", "id": "opaque-id" },
  "kind": "event | intent | observation | capability",
  "schema": "urn:cssa:schema:example:1",
  "payload": {},
  "provenance": { "source": "declared-source", "integrity": "unverified" }
}
```

The envelope is transport-neutral. Adapters may map it to JSON/HTTP, message queues, gRPC/Protobuf, local IPC, or embedded C ABI without changing semantic meaning.

## Required operations

Native implementations expose equivalent operations:

- `cssa_validate(envelope, schema_registry)`: validate shape, schema, timestamps, and supported major version.
- `cssa_negotiate(local_capabilities, remote_capabilities)`: compute the explicit intersection of versions, encodings, message kinds, limits, and optional features.
- `cssa_normalize(input, mapping_profile)`: map into a declared vocabulary while retaining source value and provenance; never infer hidden mental states.
- `cssa_authorize(principal, action, resource, policy)`: default-deny authorization for each action.
- `cssa_publish(envelope, delivery_policy)`: publish validated messages and report accepted/rejected/queued status.
- `cssa_migrate(envelope, source_version, target_version)`: deterministic, explicit migration; never silently reinterpret required data.

## Semantic graph

Use stable concept identifiers and typed directed relationships. Nodes and edges carry vocabulary/version, provenance, evidence confidence where applicable, and optional validity intervals. Confidence is metadata, not proof. Preserve unknown optional concepts as opaque extensions.

## Security and privacy

- No raw neural, biometric, health, or memory data is required or assumed.
- Do not use neural or behavioral patterns as sole authentication factors.
- Authenticate software principals cryptographically and authorize each action separately.
- Minimize payloads, encrypt transport/storage where applicable, redact secrets, and define retention.
- Treat external payloads as untrusted; enforce size, depth, rate, and replay limits.
- Never execute an intent directly: map it to an allowlisted action, validate parameters, authorize, and audit.
- Any future sensitive-signal adapter requires explicit consent, revocation, independent review, and remains disabled by default.

## Latency and delivery

Do not promise microsecond end-to-end latency without target measurements. Define per-adapter budgets, monotonic local timing, bounded queues, backpressure, cancellation, and timeout behavior. State delivery guarantees (best-effort, at-most-once, or at-least-once); make retryable consumers idempotent.

## Compatibility

Use semantic versioning. Additive optional fields are minor changes; breaking semantic changes require a major version. Preserve unknown optional fields where practical. Maintain golden fixtures and test old-producer/new-consumer and new-producer/old-consumer combinations.

## Conformance checklist

1. Positive/negative envelope fixtures and unsupported-version tests.
2. Capability intersection and no-common-version behavior.
3. Deterministic normalization with source/provenance preservation.
4. Default-deny authorization, replay rejection, limits, and redaction.
5. Ordering, duplicate delivery, retry, cancellation, and backpressure.
6. Cross-adapter compatibility fixtures.
7. Measured latency percentiles with target and environment identified.

## Implementation boundary

This is the shared contract and acceptance criteria. An operation is implemented only when executable code, tests, and reproducible CI evidence exist. BCI, neural decoding, memory encoding/transfer, and cross-biological-substrate claims require separate qualification and are out of scope here.
