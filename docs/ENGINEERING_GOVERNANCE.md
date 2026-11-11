# Engineering Governance

**Scope:** this repository and any application or runtime added in future work.  
**Status:** baseline governance is being established; no application capability is claimed.

## Principles

1. Define product purpose, supported platforms and user needs before choosing architecture.
2. Preserve data, interfaces, history and working behavior when implementation begins.
3. Make changes small, isolated, reviewable and reversible.
4. Use real tests and reproducible evidence; never create a permanently green placeholder check.
5. Keep permissions, dependencies, collected data and telemetry to the minimum required.
6. Document failure states, limitations and unsupported environments honestly.
7. A plan, specification or mock-up is not an implemented feature.

## Change control

- Work from current `main` using short-lived branches.
- Use one coherent objective per PR and describe acceptance criteria, impact, risk and rollback.
- Require actual checks to pass on the PR head before merge.
- Review API, data, security and compatibility implications.
- Do not bypass branch protections or claim rules are active until repository settings have been checked.

## Quality baseline

Before an application is considered ready, define its build/install path, meaningful tests, CI, input validation, error handling, security boundaries, dependency policy and operating requirements. Test success, boundary and failure behavior. Add UI accessibility checks only if a GUI is introduced.

## Documentation and visuals

Keep root `README.md` at or below 5,000 characters. State what exists today and what remains unimplemented. Use current screenshots of the actual application only; if no GUI exists, do not create substitute screenshots. Clearly label diagrams. Keep cross-links limited to genuine dependencies and end the root README with an accurately translated Chinese quotation about love.

## Definition of Done

A change is complete only when its acceptance criteria, tests, applicable CI checks, security/compatibility review and documentation are verified. Unknown behavior stays **not assessed**. No implementation may be labelled production-ready without reproducible evidence.
