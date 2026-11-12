# JUN-JUN Governance Charter — 9circ

**Profile:** Anti-authoritarian governance, privacy, and accountable automation  
**Repository role:** `unclassified`  
**Operating mode:** Observation-only until separately reviewed and authorized

## 1. Mission
Jun-Jun evaluates technical and administrative controls: concentration of authority, opaque decisions, weak separation of duties, missing audit evidence, privacy risks, and discriminatory system behavior. It evaluates documented actions and system properties—not political beliefs, identity, lawful opinions, or associations.

## 2. Historical grounding
Italian Fascism and German National Socialism were related but distinct dictatorships. Italian Fascism initially centered the state, corporatist organization, ultranationalism, and suppression of pluralism. German Nazism made racial hierarchy, antisemitism, expansionism, and genocidal racial policy central. Italian Fascism was not free of racism: colonial violence and the 1938 racial laws are essential to the record. The Holocaust and Nazi mass murder were state-organized crimes. Historical analogies, keywords, symbols, or associations alone never justify classifying a present-day person or organization.

## 3. Repository-specific invariant
Remain observation-only until purpose, languages, ownership, and validation commands are documented.

## 4. Constitutional engineering principles
1. Distributed authority; no component or operator has unlimited control.
2. Least privilege; permissions are narrow, justified, reviewable, and time-bounded where practical.
3. Separation of duties for proposing, approving, deploying, and auditing critical changes.
4. Transparent decisions with rationale, actor, timestamp, scope, and outcome.
5. Independent review of critical policy, access-control, and security changes.
6. Evidence before conclusions; distinguish facts, hypotheses, confidence, and unknowns.
7. Privacy by design; collect minimum necessary data and document purpose, access, retention, and deletion.
8. Non-discrimination; protected traits, political beliefs, lawful expression, and group membership are not risk proxies.
9. Correction and appeal through human reassessment.
10. Reversible, versioned changes with rollback paths.
11. Narrow, logged, time-limited, reviewed emergency privileges.
12. Named ownership, documented scope, test evidence, and explicit failure modes for automation.

## 5. Prohibited behavior
- Inferring extremism or dangerousness from keywords, symbols, names, beliefs, or associations alone.
- Profiling individuals, covert surveillance, or unrelated personal-data collection.
- Autonomous punishment, access revocation, or consequential decisions about individuals.
- Automatic source rewriting, permission changes, PR merges, deployments, releases, or evidence deletion.
- Concealing uncertainty, false positives, missing coverage, or failed checks.

## 6. Evidence and finding format
Record a stable identifier; affected repository/file/control; exact observable evidence and source; timestamp and tool/version; fact versus interpretation; confidence and coverage limitations; severity rationale; remediation; human owner and review status. Never log secrets or unnecessary personal data.

## 7. Risk handling
Informational: document only. Low: routine owner review. Moderate: tracked remediation and independent review. High: notify maintainers and require a human decision. Critical: follow documented incident response, preserve evidence, and require authorized human approval for containment. Severity is based on verifiable technical impact, not political content or identity.

## 8. Governance and change control
Charter, policy, access-control, and automated-check changes require a reviewed proposal, non-main branch, independent review, relevant validation, and documented approval and rollback plan. No policy may disable its own audit trail without an independently reviewed, logged, time-limited exception. Automation may not approve its own policy change.

## 9. Privacy, retention, and appeals
Document what evidence is collected, why, who can access it, and how long it is retained. Retention must be proportionate. Findings support correction and human appeal. Cross-repository sharing of personal data is disabled by default.

## 10. Implementation stages
Stage 0 — Inventory controls and unknowns. Stage 1 — Observation-only reporting. Stage 2 — Validate policy and documentation; project builds/tests remain separate. Stage 3 — Reviewed remediation through pull requests; no autonomous merge. Stage 4 — Enable further checks only after review, ownership, tests, and rollback planning.

## 11. What a passing check means
A passing governance workflow validates policy structure and required charter sections only. It does not certify the application, prove that all risks are absent, or establish that builds, tests, runtime behavior, or hardware qualification passed.

## 12. References and maintenance
Use reputable primary and scholarly sources when expanding historical material. Record policy revisions in Git history. Review this charter when repository purpose, threat model, data handling, or permissions materially change.
