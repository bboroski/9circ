# UTYA-ZHNETS — Project Design Profile

**Version:** 1.0.0  
**Repository:** 9circ  
**Status:** Design specification; runtime adoption must be verified independently  
**Canonical standard:** [Hellduck — UTYA-ZHNETS Machine Design](https://github.com/bboroski/Hellduck/blob/main/docs/UTYA_ZHNETS_MACHINE_DESIGN.md)

## Project profile
Repository scope is not verifiable from the current README, which contains only the project name. Apply only the neutral shell, tokens and documentation baseline until the actual runtime and product purpose are inspected; do not invent capabilities.

## Applied design language

UTYA-ZHNETS is an original industrial field-reclaimer machine identity. Use a low, broad, asymmetric equipment silhouette, a forward sensor cowl, a three-aperture crest, modular side housings, service seams and clearly marked access panels. Materials are matte graphite ceramic, dark polymer, restrained satin alloy and rubberized joints. The duck motif is abstract and functional, not a cartoon face. These are original design directions, not a reference to any existing game or franchise.

The interface language uses dense but legible machine panels, stable navigation, labelled telemetry, tabular measurements, precise dividers and restrained chamfers. Preserve this repository's existing accent color and visual identity; UTYA-ZHNETS adds a semantic machine layer rather than replacing the brand. Use amber for attention, cyan for informational telemetry, green for confirmed success, red for critical failure and neutral gray for unknown states. Always add a text label or icon.

## Operational constraints

- Do not introduce a GUI into a headless library, kernel, firmware or CLI project.
- Do not imply that a visual preview is running software or live telemetry.
- Keep implemented, partial, planned, design-only and not-tested states distinct.
- Do not grant extra device, kernel, firmware, filesystem, process, network or actuator authority through a visual change.
- Honor keyboard focus, platform scaling and reduced-motion settings wherever a GUI exists.

## Copyright and asset provenance

All silhouettes, marks, symbols, labels, diagrams and interface components must be original or separately licensed. Do not reproduce Mass Effect names, logos, factions, characters, ships, weapons, story elements, UI layouts, sounds or recognizable armor silhouettes. Do not trace game screenshots or fan art, and do not imply affiliation or endorsement. Broad industrial science-fiction concepts are acceptable; protected expression is not.

## Machine-readable tokens

[utya-zhnetz.tokens.json](utya-zhnetz.tokens.json) defines the cross-project palette, typography fallbacks, geometry, motion, accessibility and telemetry vocabulary. Existing project tokens remain authoritative for the original brand accent.

## Definition of done

The profile is adopted when its token file parses as JSON, its project-specific use remains faithful to the actual runtime, statuses are not color-only, reduced motion and keyboard focus are preserved in GUI surfaces, and native project checks pass. No production-readiness claim follows from this document alone.
