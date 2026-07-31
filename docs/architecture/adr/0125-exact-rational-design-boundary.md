# ADR 0125: Exact rational masses — design boundary (no Kernel mode yet)

## Status

**Accepted as design boundary** (2026-07-31) — LISS-0157 docs.
Does **not** authorize a Kernel rational runtime.

Companions: ADR 0076; ADR 0097; permanent-out reopen.

## Decision

1. Reopen permits Architecture Path design of optional rational **literals /
   provenance**, not a silent change of Joint/PMF masses to `fractions.Fraction`.
2. Any future rational mode must be **explicit, additive**, and lower or coerce
   to `f64` at the execution boundary unless a later ADR replaces 0076 Decision 2.
3. $1/\sqrt{2}$-class amplitudes remain outside exact rationals (ADR 0097).

## Non-goals (this ADR)

Kernel Joint masses as Rational; generic coefficient type parameters.

Classical-only rational literals are unsealed by
[ADR 0160](0160-classical-rational-literals.md); Joint rational mode remains
out.
