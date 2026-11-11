# Motion & GUI system — 9circ

**Version:** 1.0  
**Adoption type:** repository-scoped presentation contract  
**Status:** documentation baseline only; this repository currently exposes no verified application runtime or GUI implementation.

## Scope

This contract covers animation, motion design, dynamic visualization, rendering, GUI, visual interface, application shell, control panel, workspace, screen environment, navigation and interaction surfaces. It defines how a future implementation should be assessed; it does not claim that these capabilities exist today.

## Architectural rules

- Keep domain state separate from presentation state and rendering.
- Animation is presentation only; it cannot imply that work, validation, security checks or user actions have succeeded.
- Any future GUI must define keyboard, focus, semantic labels, high contrast, scaling and responsive behavior.
- Honor reduced-motion preferences. Web implementations must support `prefers-reduced-motion: reduce`; native applications must follow the host accessibility setting when available.
- Provide a static equivalent for every essential animated state. Persistent motion must be avoidable.
- Do not introduce a framework, runtime, graphics dependency or build tool until the product surface and supported platform are documented.

## Motion defaults for future UI

| Token | Default | Intended use |
|---|---:|---|
| `motion-none` | `0 ms` | Static/reduced-motion mode |
| `motion-fast` | `110 ms` | Press and focus feedback |
| `motion-standard` | `180 ms` | Selection and small transitions |
| `motion-slow` | `240 ms` | Panel and view changes |
| `motion-max` | `320 ms` | Upper bound for ordinary UI motion |

Prefer opacity and transform, bounded interpolation and cancellable callbacks. Avoid perpetual motion, parallax and large spatial movement by default.

## Acceptance gate

Before claiming an animated GUI is implemented, add a real product surface and tests proving:
1. core tasks work with motion disabled;
2. keyboard-only operation and visible focus work;
3. reduced-motion mode removes decorative motion without hiding information;
4. state and progress represent real work, not an animated guess;
5. timers/callbacks are cancelled on teardown;
6. build and relevant tests pass.

Until those artifacts exist, classify GUI/animation as **not implemented / not evidenced**. Do not create mock screenshots or infer capabilities from this contract.
