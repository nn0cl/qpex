# LISS-0057: Periodic boundary accessor `wrap(i)`

## Metadata

- Local issue ID: LISS-0057
- GitHub issue: none
- Status: proposed
- Phase: phase-0-design complete (ADR 0096 D4 accepted); awaiting Phase 1 Red approval
- Type: language surface (additive)
- Priority: P2
- Initial planning size: M
- Current planning size: M
- Reclassification reason: n/a
- Owner/agent: TBD
- Related branch: `codex/liss-0057-periodic-boundary-red`

## Summary

Add `wrap(i)` as the explicit periodic-boundary index accessor, per
[ADR 0096](../architecture/adr/0096-indexed-operator-and-binder-surface.md)
D4:

```qpex
sum (i in Index<0..N-1>) { -J * Z[i] * Z[wrap(i)] }
```

Periodic rings are standard objects of study — closed spin chains, lattices
with periodic boundary conditions — and are currently inexpressible.

`next(i)` keeps its meaning unchanged: open boundary, hard
`BINDER_INDEX_OUT_OF_BOUNDS` when it leaves the domain.

## Why an accessor rather than a domain or register property

Boundary policy is placed at the **point of use**, not on the domain type or
the register, so that a reader of the formula sees which boundary is in
effect without consulting a declaration elsewhere. This also matches
`next(i)`, which is already an accessor, and keeps the feature strictly
additive: no existing `Index<a..b>` syntax changes, which is why ADR 0096
could classify periodic support as a legitimate deferral rather than a
breaking decision.

## Acceptance notes

- [ ] `wrap(i)` resolves to $(i + 1) \bmod |D|$ over the binder's own
      domain $D$, and never silently falls outside the containing static
      register.
- [ ] A periodic ring Hamiltonian
      ($-J\sum_{i=0}^{N-1} Z_i Z_{(i+1)\bmod N}$) lowers, runs, and emits
      QASM, with the wrapped term present — verified by expanded term count
      **and** by numerical comparison against the hand-written equivalent
      including the closing bond.
- [ ] `next(i)` behaviour is unchanged: the open-chain example still fails
      at the boundary with `BINDER_INDEX_OUT_OF_BOUNDS`.
- [ ] `wrap(i)` whose wrapped target would leave the containing static
      register (a domain larger than the register) is a hard diagnostic, not
      a silent wrap into a nonexistent site.
- [ ] Provenance records which accessor was used, so the emitted circuit can
      be traced back to open vs periodic boundary.

## Non-goals

- Wrapping by an arbitrary stride (`wrap(i, k)`) — additive, deferred.
- Multi-dimensional lattice topology (2D/3D periodic) — needs its own
  domain design; deferred.
- Making boundary policy a property of the register or domain — explicitly
  rejected by D4.

## Dependencies

- Parent: none
- Depends on: **LISS-0052** (execution wiring). **LISS-0055** preferred
  first so `wrap` lands against the final body grammar.
- Related: ADR 0096 D4, ADR 0088 (which deferred periodic boundaries),
  LISS-0043 (`next(i)` open-boundary validation this mirrors)
- Blocks: nothing

## Adjudicator Decision Points

- [x] Approve Phase 1 Red.
- [x] Confirm the accessor name `wrap` (alternatives considered: `cyclic`,
      `mod_next`). `wrap` is proposed as the shortest name that reads as
      "wrap around" without implying a modulus argument.
- [x] Confirm `wrap(i)` wraps over the **binder domain**, not over the
      register, when the two differ — this issue proposes the domain, and a
      mismatch with the register is a diagnostic rather than a silent
      reinterpretation.

## Context

- Included: `compiler/qpex/parser.py` (`OpCall` accessor names),
  `compiler/qpex/finite_binder.py` (`_resolve_index`, which currently
  handles `next` only), `compiler/qpex/typecheck.py` (accessor validation).
- Omitted: multi-dimensional topology, arbitrary strides.
- Assumption: `wrap` composes with `where` guards and nested binders without
  special-casing, since it resolves during the same index-resolution step as
  `next`.

## Verification

- Phase 1 Red: `wrap(i)` is unrecognised today; the periodic ring
  Hamiltonian cannot be written.
- Phase 2 Green: acceptance notes pass, including the numerical check that
  the closing bond is actually present rather than merely counted.
- Full regression sweep and spec verification stay green.

## Work Notes

- 2026-07-27: Adjudicator approved Phase 1 Red. The acceptance tests require
  explicit `wrap(i)` domain resolution, a retained closing bond, execution and
  QASM coverage, and a hard diagnostic when the wrapped target exceeds the
  containing static register. No production implementation is included in
  this phase.

- 2026-07-26: Opened from ADR 0096 D4. Reclassified during that ADR's design
  from "potentially breaking" (if boundary policy had been placed on the
  domain type) to "additive" (accessor at the point of use) — the design
  choice is what made the deferral legitimate.
