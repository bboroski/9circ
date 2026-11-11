# Beelzebub Engine (MVP)

This repository contains a read-only security scanner and the shared Threat Exchange Format schema.

## Run locally

Requires Python 3.10+; the scanner uses only the Python standard library.

```sh
python3 -I tools/beelzebub/scan.py --root . --report beelzebub-report.json --fail-on high
```

Exit codes: 0 = no finding met the blocking threshold; 1 = a finding met it; 2 = invalid invocation or repository root.

The JSON report contains redacted finding metadata, dependency-manifest paths and SHA-256 digests. It does not include matched secret values. Files larger than 2 MiB, symlinks, known build/cache directories, and binary files are skipped.

## Safety boundaries

- Read-only with respect to source files; only the requested report file is written.
- No network access, package installation, code execution, deletion, patching, or automatic quarantine.
- Findings are heuristic indicators, not proof of compromise.
- Review every finding before rotating credentials or changing dependencies.
- Do not commit generated reports if they contain internal repository metadata.

## Threat exchange

`schemas/threat-exchange.schema.json` defines TEF 1.0. Schema validity is not proof of authenticity: production exchange must additionally verify a detached signature over a canonical payload, enforce issuer trust, freshness, replay protection, and transport authorization. Never execute mitigation text received from a peer.

## Current maturity

MVP: local secret-pattern checks, dependency manifest inventory, JSON reporting, and pull-request CI integration. P2P gossip, global consensus, AST/behavioral analysis, artifact signing, federated learning, and automated remediation are not implemented by this MVP.
