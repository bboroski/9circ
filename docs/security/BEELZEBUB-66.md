# Beelzebub 66 — repository security contract

**Policy version:** 1.0.0 | **Scope:** source, dependencies, build pipeline, releases and security events.
**Model:** local-first, least privilege, evidence before enforcement.

A policy requirement is not proof that a runtime sensor, OS agent, signing service or central exchange is deployed. The local scanner is read-only except for its JSON report. Findings are evidence for review, not authority for destructive remediation.

## I. Reconnaissance and detection (01–11)
1. **Asset inventory** — enumerate source, executable, configuration, dependency and generated-artifact paths.
2. **Integrity measurement** — hash critical files and compare with a trusted baseline.
3. **Malware indicators** — detect known signatures and suspicious code combinations; report evidence and confidence.
4. **Secret discovery** — find private keys, tokens, passwords and credential-like assignments; redact values.
5. **Dependency analysis** — inventory manifests and lockfiles; check trusted vulnerability advisories when configured.
6. **Supply-chain provenance** — record package source, version, checksum and publisher metadata.
7. **Obfuscation detection** — flag suspicious encoded payloads, dynamic loading and concealed execution.
8. **Change intelligence** — compare pull-request changes with history and identify high-risk deviations.
9. **Configuration audit** — inspect security settings, exposed services, permissions and unsafe defaults.
10. **Binary inspection** — inventory unknown executable artifacts and compare hashes.
11. **Event correlation** — correlate independent signals without treating one weak signal as proof.

## II. Interception and containment (12–22)
12. **Least privilege** — grant jobs/processes only required permissions; CI tokens default read-only.
13. **Process isolation** — run untrusted builds/tests in disposable restricted runners or containers.
14. **System-call policy** — use supported seccomp, AppArmor or sandbox profiles where available.
15. **Filesystem protection** — protect source, policy, signing keys and release paths.
16. **System configuration protection** — monitor registry/equivalent OS settings only where applicable.
17. **Network egress control** — restrict outbound destinations for build/test jobs.
18. **IPC protection** — constrain inter-process channels according to platform capabilities.
19. **Memory safety controls** — enable compiler/OS mitigations; never corrupt pointers or other processes' memory.
20. **Persistence detection** — audit startup entries, scheduled tasks and services where applicable.
21. **Build isolation** — separate untrusted pull-request jobs from deployment credentials.
22. **Safe quarantine** — preserve originals and evidence; move suspect artifacts only under explicit reversible policy.

## III. Source-code protection (23–33)
23. **Pre-merge validation** — scan changed files and run relevant security tests.
24. **Independent review** — require review for authentication, cryptography, permissions and release logic.
25. **Protected default branch** — require pull requests, checks and approvals.
26. **History integrity** — audit force-pushes and unexpected protected-ref changes.
27. **Source substitution detection** — verify generated, vendored and critical files against provenance/digests.
28. **Unsafe API review** — flag dangerous deserialization, shell execution, dynamic evaluation and weak crypto APIs.
29. **Input validation** — validate untrusted input and test malformed/adversarial values.
30. **Serialization safety** — use safe parsers, bounded inputs and explicit schemas.
31. **Cryptographic correctness** — use maintained libraries and secure random generation.
32. **Authorization checks** — test server-side permission boundaries and deny-by-default decisions.
33. **Dynamic-code controls** — restrict plugin loading, runtime compilation and generated-code execution.

## IV. Build and release integrity (34–44)
34. **Pre-build gate** — validate policy, secrets, dependencies and source state.
35. **Ephemeral workers** — use disposable workers without unnecessary persistent credentials.
36. **Pinned dependencies** — pin direct dependencies and use supported lockfiles.
37. **Lockfile verification** — detect unexpected lockfile drift.
38. **Toolchain integrity** — pin compilers, package managers, images and CI actions.
39. **Environment validation** — allowlist build variables and protect privileged commands.
40. **CI secret isolation** — expose deployment secrets only to trusted release jobs.
41. **Artifact scanning** — inspect outputs for embedded credentials and unexpected executables.
42. **SBOM generation** — produce a machine-readable component inventory.
43. **Artifact signing** — sign releases when managed keys and verification are configured.
44. **Provenance/reproducibility** — retain build metadata, checksums and provenance attestations.

## V. Resilience and recovery (45–55)
45. **Continuous integrity** — re-check critical files and release artifacts.
46. **Repeat-attack detection** — correlate recurring indicators and preserve timelines.
47. **Ransomware indicators** — detect rapid mass rewrites and suspicious encryption behavior where monitored.
48. **Backup tamper detection** — monitor backup deletion/modification and isolate backups from build runners.
49. **Critical-change approval** — review changes to policies, workflows, keys and recovery.
50. **Trusted checkpoints** — retain immutable verified source and release checkpoints.
51. **Trusted-state recovery** — restore only verified commits/artifacts while preserving evidence.
52. **Recovery testing** — test restoration and verify hashes and application health.
53. **Incident analysis** — record timeline, scope, evidence, containment and follow-up.
54. **False-positive handling** — require owner, rationale, scope and expiry for suppressions.
55. **Rule evolution** — update versioned detection rules through reviewed changes and regression tests.

## VI. Cross-repository coordination (56–66)
56. **Repository registry** — inventory enrolled repositories and default branches.
57. **Local project profile** — detect languages/build systems/release surfaces; keep exceptions local.
58. **Policy versioning** — pin policy versions and report drift.
59. **Autonomous local agent** — keep local scanning/reporting available without the coordinator.
60. **Signed threat exchange** — exchange minimal signed indicators only over a verified trust channel.
61. **Update authenticity** — verify signatures, schema, freshness and replay protection.
62. **Repository discovery** — propose new repositories for enrollment; do not silently grant permissions.
63. **Component discovery** — detect new files, manifests and build components.
64. **Incident correlation** — correlate indicators across repositories while preserving local evidence.
65. **Audit/reporting** — produce per-repository and cross-repository evidence reports.
66. **Self-health verification** — test scanner, policy, workflow, reports and update verification.

## Enforcement and safety
**Active baseline where scanner/workflow exists:** read-only secret-pattern scan, dependency-manifest inventory, JSON report and CI execution.
**Policy controls:** branch protection, review, CI permissions, dependency pinning and artifact handling require repository settings/workflow support.
**Platform-dependent:** OS process/network/filesystem monitoring, syscall restrictions, runtime memory protections and ransomware behavior detection require a separate platform-specific agent.
**Future federation:** signed threat exchange and central orchestration remain inactive until identity, key management, privacy and replay protection are deployed and tested.

Never autonomously delete source, kill processes, rewrite history, force-push, replace dependencies or alter production. Emit evidence and proposed remediation; require explicit policy and auditable approval for enforcement.

## Repository-specific adapter
Complete the adapter from the repository's actual language/build/release inventory. Do not assume capabilities from its name.

### Local adapter: bboroski/9circ

Project-specific profile: discover actual language, build and release surfaces before enabling language-specific checks. Keep the adapter report-only until test coverage validates enforcement.

**Enrollment status:** committed to the foundation branch; default-branch enforcement requires merge and successful CI validation.
