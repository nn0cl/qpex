# ADR 0060: Joint coordinate preservation under remarginalization

## Status

**Proposed** (2026-07-23). Does **not** authorize implementation until Accepted.

Follow-up Issue: [LISS-0004](../../issues/LISS-0004-joint-preservation-classical-env.md).  
Parent: [LISS-0003](../../issues/LISS-0003-examples-driven-kernel-brush-up.md).

## Context

`grover_diffuse` / `diffuse` call `Joint.diffuse_copy`, which rebuilds each
surviving world as `{dest: v}` only. Classical Type-First binds (`Float cfg`)
and sibling wires disappear from `assign`, so later `inspect(cfg)` raises
`KeyError`. Examples 12/14 work around this by never inspecting config after
amplify.

`phase` keeps `{**w.assign, …}` (coordinates preserved). `evolve` / `cnot`
likewise. Remarginalization is the inconsistent path.

Separately, `phase(..., only)` evaluates `only` with an empty assign map, and
`evolve times N` parses only integer literals — classical domain structs cannot
drive oracles or step counts.

## Dependency Adoption Evidence

Not applicable (Kernel semantics; no new dependency).

## Decision

*(Proposed — pending Adjudicator Accept)*

1. **Coordinate preservation:** Any Joint transform that rewrites amplitudes
   for a named coordinate `src`→`dest` **MUST** retain all other keys in each
   world’s `assign` unless the op’s contract explicitly projects them away
   (`project`, `trace_out`, measure collapse).
2. **`diffuse` / `grover_diffuse`:** Implement (1). Dest may replace `src` or
   be a fresh name; unrelated classical and quantum coordinates survive.
3. **Classical resolution for mark/times:** `phase`’s `only` (and preferably
   θ) and `evolve`’s `times` expression resolve against evaluator classical
   env (`scalars` + closed object Attr) and, when needed, the current world’s
   assign — documented in the evaluator contract.
4. **`EvolveExpr.times`:** AST carries an expression (literal or closed
   classical); runtime evaluates to a non-negative integer (Float truncate
   policy: Adjudicator choice at Accept).

## Consequences

Positive:

- Multi-file Grover demos can keep domain Floats visible after amplify.
- Domain `n_steps` can drive DTQW loops (09/15).
- Matches physicist expectation: diffusion is about amplitudes, not erasing
  classical labels on the joint.

Negative:

- Slightly larger world maps; coalescing keys must stay correct.
- Parser/AST change for `times` touches compile path.

## Enforcement

Code review should reject:

- Joint helpers that drop unrelated `assign` keys without an explicit project.
- New examples that reintroduce “do not inspect Float after diffuse” as a
  permanent language limitation once this ADR is Accepted and implemented.
- Treating `KeyError` on classical inspect after Grover as “user error.”

## Verification (when Accepted + implemented)

- Unit / SV: Float survives `grover_diffuse`.
- `phase(idx, pi, target)` with `Float target` (or Attr) marks correctly.
- `evolve times n_steps` with classical Int.
- Full SV suite green.
