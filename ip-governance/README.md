# Repository IP governance

Portable provenance and rights metadata baseline. `manifest.json` records a repository-scoped UOI locator, rights declaration, provenance settings, privacy defaults, and optional artifact digests. `verify.py` validates metadata and file digests with Python's standard library. GitHub Actions runs the check on relevant pushes and pull requests.

Use SPDX expressions only after checking the actual license; otherwise retain `NOASSERTION`. Do not infer authors or rights holders from commit metadata. Add digests only after review. SHA-256 proves byte integrity, not authorship, ownership, originality, or a legally conclusive timestamp. Signed commits and trusted timestamps are supporting evidence, not legal conclusions.

This manifest is metadata, not a replacement for MIT, GPL, Creative Commons, contracts, or applicable law. Blockchain, DAG anchoring, NFTs, and automated payments are optional and require threat-model, key-management, privacy, and legal reviews. Avoid public per-viewer event ledgers and personal identifiers by default. Personalized watermarking must be opt-in. Do not rewrite source text to conceal trademark references: aliases belong only in presentation layers, while criticism and nominative references remain intact. Contribution metrics must not be treated as legal ownership shares.

To register a reviewed artifact, compute its SHA-256 digest and add an entry to `artifacts`:
```sh
python -c "import hashlib,pathlib; p=pathlib.Path('path/to/file'); print(hashlib.sha256(p.read_bytes()).hexdigest())"
python ip-governance/verify.py
```
