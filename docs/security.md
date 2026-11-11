# Security and native boundary policy

## Native FFI

Treat every native library as untrusted input. Load only absolute paths from an allow-listed directory, verify the SHA-256 digest against the artifact manifest, and validate ABI/version metadata before calling init. Do not load a module from a corpus upload or user-controlled path.

The Ruby manager performs initialize-before-swap and lease-based retirement. It does not provide a hard memory isolation boundary and does not guarantee immediate dlclose. Native modules must be built with stack protection, position-independent code and hardened linker flags appropriate for each target.

## Shared memory

Validate frame magic, protocol version, payload length, sequence and CRC before reading payload bytes. Enforce a maximum segment size and reject integer overflow when computing offsets. Never trust offsets or lengths supplied by another process. Use process-shared synchronization for multi-process writers.

## Generated code

Creative proposals are data, not executable commands. Never evaluate generated source inside the API process. A production evaluator must run in a disposable, unprivileged sandbox with no network, read-only base filesystem, bounded CPU/memory/time, syscall restrictions and an explicit allow-list of dependencies. Require review before applying patches.

## Runtime hardening

Use non-root containers, read-only filesystems, dropped Linux capabilities, seccomp, least-privilege service accounts and secret managers. Do not expose PostgreSQL, Redis or Qdrant administrative endpoints publicly. Rotate credentials and enable TLS/authentication in production.

## Resource control

Motivation scores are scheduling hints only. Hard CPU/memory limits remain with the OS and orchestrator. Never use feedback weights to disable safety checks, starve health probes or bypass tenant quotas.
