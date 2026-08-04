# LISS-0238: Multi-hole Partial pipe must move the lhs

## Metadata

- Local issue ID: LISS-0238
- Status: **complete**
- Phase: phase-3-refactor
- Type: bug
- Priority: P1
- Planning size: S
- Program: [WP-0085](../work-plans/WP-0085-deferred-kernel-gaps.md)
- Design ADR: [0149](../architecture/decision-themes/dec-0004-type-first-scientific-model.md) (**Accepted**)
- Recorded on: [LISS-0233](LISS-0233-green-floor-residual-suites.md) deferred Kernel

## Intent

`state q = x |> p` where `p` still has \(n>1\) holes must **move** linear
`x` (no `LINEAR_IMPLICIT_DISCARD`).

## Exit

- [x] `x |> p` (2+ holes remaining) compiles without `LINEAR_IMPLICIT_DISCARD`
- [x] Stepwise `p = f(_,_); q = x |> p; r = y |> q` evaluates correctly
- [x] One-hole pipe / Call fill regressions still green
- [x] Full `pytest tests/` green

## Non-goals

Changing fill order; fusing multi-hole stages (ADR 0143 stays one-hole).
