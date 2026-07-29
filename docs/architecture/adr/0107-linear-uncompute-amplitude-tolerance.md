# ADR 0107: Linear uncompute amplitude tolerance

## Status

**Accepted** (2026-07-29). Adjudicator architecture approval after LISS-0114
Slice F shipped on `main` (PR #120).

Records the numeric tolerance for runtime simulator-equivalence uncompute
witnesses. Implementation already ships via LISS-0114 Slice F; this Accept
locks the tolerance class as architecture policy.

Companions:

- [LISS-0114](../../issues/LISS-0114-linear-verifier-hardening.md) (**complete**)
- [ADR 0076](0076-numeric-representation-policy.md) (physical tolerance class)
- [ADR 0097](0097-numeric-representation-horizon.md) (`f64` provisional)

## Context

LISS-0075 / LISS-0114 ship a static HIR uncompute witness (`|0>` / `vacuum`
rebind). Full uncomputation may also arise from unitary round-trips that only
the evaluator can validate. The project needs an explicit amplitude tolerance
so runtime checks neither invent a private epsilon nor silently “repair”
states.

## Dependency Adoption Evidence

Not applicable (no new dependency).

## Decision

1. Runtime uncompute equivalence uses the **physical tolerance** class already
   recorded in ADR 0076: **`1e-12`**.
2. Authoritative export:
   `compiler.staqex.runtime.uncompute.LINEAR_UNCOMPUTE_AMPLITUDE_TOL`
   (aliased from `PHYSICAL_TOLERANCE`; also re-exported on
   `compiler.staqex.hir`).
3. A coordinate `name` is ≈ computational `|0⟩` when the Born mass of all
   non-zero values of `name` is ≤ tolerance relative to the joint norm
   (`is_computational_basis_zero`).
4. Violations raise a named diagnostic /
   `UNCOMPUTE_RUNTIME_MISMATCH` — **no** silent renormalization or clipping.
5. Static HIR `|0>` / `vacuum` witnesses remain valid; runtime checks defend
   simulator-equivalence for Uncompute-marked returns and `|0>`/vacuum rebinds.

## Consequences

Positive:

- Same numeric class as density / Kraus / POVM physical checks.
- Testable without a second epsilon zoo.

Negative:

- Computed uncompute that is not statically `|0>`/`vacuum` still does not
  clear HIR discard by itself (HIR consume-set unchanged).

## Follow-on

- Optional: extend HIR consume-set when runtime-proven near-zero patterns are
  specified (separate Issue).
