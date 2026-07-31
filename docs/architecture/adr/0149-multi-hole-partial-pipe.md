# ADR 0149: Multi-hole Partial pipe fill

## Status

**Accepted** (2026-07-31) — unlocks LISS-0181 under WP-0055.
Extends [ADR 0131](0131-stepwise-partial-fill.md) and
[ADR 0123](0123-function-partial-holes.md).
Companions: [ADR 0143](0143-call-partial-pipe-fusion-mvp.md) (Fusion stays
one-hole).

## Context

ADR 0131 Decision 5 required bare pipe Partial stages to have **exactly one**
remaining hole. Stepwise Call fill (`p(x)` → smaller Partial) already worked.
Adjudicator unseals thin MVP: bare `|>` into a multi-hole Partial fills one
hole left-to-right — same denotation as calling the Partial with one argument.

## Decisions

1. **Bare Partial pipe.** `payload |> p` where `p` is a bound Partial with
   \(n \ge 1\) remaining holes fills the **leftmost** hole with `payload`.
2. **Result.** If \(n = 1\), the result is the completed `fn` value (State /
   Unit as today). If \(n > 1\), the result is a new Partial with \(n-1\)
   holes (same payload shape `fun#n-1` as ADR 0131).
3. **Inline Call stages.** `x |> f(a, _, _)` continues to fill the leftmost
   `_` via `_piped_call`; remaining holes yield a Partial bind (unchanged
   Call typing).
4. **Fusion.** [ADR 0143](0143-call-partial-pipe-fusion-mvp.md) eligibility is
   unchanged: only **one-hole** Call/Partial stages fuse. Multi-hole mid-chain
   stages fall back to sequential eval.
5. **Malformed payloads** (`#` missing / non-positive hole count) →
   `FUNCTION_ARITY_ERROR`.

## Non-goals

Multi-hole simultaneous fill in one fused stage; `p(_, x)` re-introduction;
method Partials; polynomial≥2 Fusion.

## Consequences

- `p = add3(1,_,_); q = x |> p; r = y |> q` typechecks and evaluates.
- ADR 0131 Decision 5 is superseded by this ADR for bare Partial pipes.
- Agents must not treat this as permission to fuse multi-hole stages.
