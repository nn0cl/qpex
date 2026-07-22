# ADR 0016: Stance (a) — Discrete PMF MVP with amplitude lift path

## Status

Accepted

Adjudicator technology-selection approval: 2026-07-22.
Related: ADR 0013, ADR 0014, `docs/architecture/qpex-positioning.md`,
`docs/specs/qpex-formal-semantics-sketch.md`.

## Context

QPex aims at QPU-native compilation eventually, but starting amplitude-native
from day one would delay the Kernel PoC track and blur the probabilistic
executable story. The Adjudicator chose stance (a): PMF foundation now,
amplitude lift later, with interfaces that do not block the lift.

## Dependency Adoption Evidence

Not applicable.

## Decision

1. MVP runtime representation is Discrete PMF over finite `i64` product
   supports (joint distributions), as in ADR 0014 and the formal semantics
   sketch.
2. Interpret MVP PMF mass $\mu(s)$ as the special case of a quantum-like state
   with **phase 0** on every atom (classical probability shadow).
3. Domain and UseCase APIs must be expressed in terms of **state on a finite
   product support** (joints, pushforwards, terminal collapse), not as
   “independent scalar bags,” so a future amplitude IR
   ($\alpha(s) \in \mathbb{C}$, $|\alpha(s)|^2 = \mu(s)$) can lift without
   rewriting Language Law.
4. Amplitude-native evaluation, interference, and QPU IR backends require a
   later ADR before production implementation.
5. Feature Path Phase 1 Red remains HOLD until Kernel PoC A/B fixtures pass;
   this ADR does not by itself unseal Phase 1.

## Consequences

Positive:

- Clear near-term simulator story.
- Honest marketing: PMF ≠ full QM, with a named lift path.

Negative:

- Early demos will not show interference.
- Lift may force IR redesign if joints are implemented too narrowly.

## Enforcement

Code review should reject:

- Hard-wiring “probability only forever” into public IR names without an
  escape hatch for amplitudes.
- Implementing complex amplitudes in MVP without a superseding ADR.
- Treating MVP as quantum-complete in docs or README claims.
