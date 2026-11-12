# Nero Spider — flat GUI and visual contract

**Repository:** 9circ  
**Status:** design contract only; this repository currently has no verified GUI runtime.

## Visual foundation
Nero Void `#050505`, Anthracite `#121212`, dividers `#1F1F1F`, text `#F4F4F4`, Mallard Green `#006442` for verified success/trust/protection, critical red `#FF1E1E`. Square geometry, 1 px rules and a 2% coordinate grid. No shadows, gradients, silhouettes, 3D or skeuomorphic effects.

## Motion and graphics
Use 100–220 ms transitions, a maximum 420 ms click ripple and honor `prefers-reduced-motion`. Use abstract geometric line marks for duck references and abstract circles/triangles/typography for anime-inspired motifs; no character likenesses or silhouettes. Audio and custom cursors are disabled by default.

## Operational GUI contract
Any future status view must show branch, commit, build/security state and verified timestamp. Missing telemetry is `UNKNOWN`, never `PASS`. Logs remain ordered and readable; destructive actions require confirmation and audit events. Emergency stop must be keyboard accessible, confirmed and fail-safe.

## README and screenshot policy
Generated `Live Security Status` content may be updated only inside explicit markers and only from verified CI data. Save screenshots in `docs/screenshots/`; call an image a runtime screenshot only if captured from a running application. Do not invent GUI capability or screenshots for this repository.

## Integration gates
Validate token JSON, contrast, keyboard focus, 200% zoom and reduced motion. Preserve repository ownership, language, build system and license. Luci is the canonical token source.

The source manifesto provides ten concrete examples and placeholders for the remaining concepts; this file applies the supplied design direction without claiming that 666 individually specified features or a GUI runtime already exist.
