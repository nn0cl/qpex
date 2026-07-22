# ADR 0060: Joint coordinate preservation under remarginalization

## Status

**Accepted** (2026-07-23). Adjudicator authorized Feature Path via
“ISSUE を消化して進めて” on the LISS-0003 ledger.

Follow-up Issue: [LISS-0004](../../issues/LISS-0004-joint-preservation-classical-env.md).  
Parent: [LISS-0003](../../issues/LISS-0003-examples-driven-kernel-brush-up.md).

## Context

`grover_diffuse` / `diffuse` call `Joint.diffuse_copy`, which rebuilt each
surviving world as `{dest: v}` only. Classical Type-First binds (`Float cfg`)
and sibling wires disappeared from `assign`, so later `inspect(cfg)` raised
`KeyError`. Examples 12/14 worked around this by never inspecting config after
amplify.

`phase` keeps `{**w.assign, …}` (coordinates preserved). Remarginalization was
the inconsistent path. Separately, `phase(..., only)` evaluated `only` with an
empty assign map, and `evolve times N` parsed only integer literals.

## Dependency Adoption Evidence

Not applicable (Kernel semantics; no new dependency).

## Decision

1. **Coordinate preservation:** Any Joint transform that rewrites amplitudes
   for a named coordinate `src`→`dest` **MUST** retain all other keys in each
   world’s `assign` unless the op’s contract explicitly projects them away
   (`project`, `trace_out`, measure collapse).
2. **`diffuse` / `grover_diffuse`:** Implement (1). Diffusion acts on the
   amplitude **marginal** of `src`; within each value bucket, world amplitudes
   are rescaled proportionally so sibling wires / classical coords survive.
3. **Classical resolution for mark/times:** `phase`’s `only` / θ and `evolve`’s
   `times` resolve against evaluator classical env (`scalars` + closed object
   Attr) and world assign — Var lookup falls through to `scalars` when absent
   from assign.
4. **`EvolveExpr.times`:** AST carries an expression. Runtime evaluates to a
   non-negative integer; **Float truncates toward zero** via `int(float(x))`.

## Consequences

Positive:

- Multi-file Grover demos keep domain Floats visible after amplify.
- Domain `n_steps` can drive DTQW loops (09/15).

Negative:

- Slightly larger world maps; coalescing keys must stay correct.
- Parser/AST change for `times` touches compile path.

## Enforcement

Code review should reject:

- Joint helpers that drop unrelated `assign` keys without an explicit project.
- Treating `KeyError` on classical inspect after Grover as “user error.”

## Verification

- Float survives `grover_diffuse`; `phase`/`times` accept classical vars.
- Full SV suite green.
