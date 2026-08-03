# ADR 0185: Kernel `Continuous` value — Proposed ship boundary

## Status

**Proposed** (2026-08-03) — Architecture Path reopen of permanent-out Continuous
row ([LISS-0312](../../issues/LISS-0312-continuous-kernel-architecture.md)).

This document is **not** implementation authorization. Feature Path Red requires
this ADR **Accepted** (or a thinner successor) plus Phase / Issue approval.

## Context

| Layer | Status |
|---|---|
| Design boundary (no Kernel continuous value) | [ADR 0126](0126-continuous-pdf-design-boundary.md) **Accepted** |
| Preferred unseal path: Host/Bridge first | [ADR 0162](0162-continuous-host-bridge-first.md) **Accepted** |
| Host MC → finite inject MVP | [ADR 0163](0163-host-mc-finite-state-inject.md) **shipped** |
| Host consumption seam (labels + 0074 provenance) | [ADR 0164](0164-host-mc-inject-consumption-seam.md) **shipped** |
| Theory continuous_operator → explicit discretization | existing (ADR 0074 lineage / LISS-0111) |

ADR 0162 Decision 4: a Kernel `Continuous` (or additive sugar) requires a
**separate ship ADR after Host/Bridge is specified**. Host inject + seam are
now specified and shipped. Drafting this ADR is therefore in-policy; shipping
is not automatic.

Physicist pressure: blackboard PDFs / continuous observables want a first-class
surface without dropping into Python Host APIs. Counter-pressure: mid-program
`Continuous` is hard to narrow later; NLTS and QPU paths must remain
**finite-only**.

## Dependency Adoption Evidence

Not applicable — no new external SDK. Host MC and discretization stay ports.

## Decision (proposed — Adjudicator must choose a lane)

### Lane A — Finiteize surface only (recommended MVP)

**No mid-program `Continuous` Kernel value.** Add Kernel / language surface that
makes Host finiteization **callable from Staqex notebooks** without inventing a
new Joint carrier:

1. A fail-closed finiteize form (name TBD in Red grammar), e.g. chalk intent:
   ```text
   state psi = finiteize(samples, interval, bins)   // Host-backed MVP
   ```
   or a thin import of Host inject helpers under a documented package, not a
   new type universe.
2. Semantics: equal-width histogram path reuses ADR 0163/0164 ports; result is
   ordinary finite `State` / Joint.
3. Provenance: ADR 0074 `discretization` block required (0164).
4. **Forbidden:** `measure` / QPU emit on non-finiteized continuous bags;
   silent truncation; adaptive/KDE bins in MVP.

**Unseals:** notebook-facing continuous → finite without Python Host demo only.  
**Does not unseal:** `Continuous` as a mid-program type.

### Lane B — Mid-program `Continuous<T>` type (larger ship)

Introduce `Continuous<…>` as a **distinct type world** (ADR 0162 Decision 1):

1. Allowed: prepare / transform continuous descriptions; explicit
   `finiteize(c) → State`.
2. **Hard gates (non-negotiable):**
   - no terminal `measure` on `Continuous`
   - no Joint mix of Continuous × State without finiteize
   - no QASM / QPU path on Continuous
   - no Trace-Out GC / LINEAR rules that pretend Continuous is State
3. MVP operations: explicit list in Feature Red (keep ≤ 3 ops).
4. Host MC remains the sampling backend behind finiteize for histogram MVP.

**Risk:** once mid-program Continuous ships, removing it is breaking (0162 §5).

### Lane C — Keep Host-only (reject reopen)

Maintain ADR 0126/0162; no Kernel Continuous surface. Close LISS-0312 as
**wontfix / repark**.

## Recommended choice

**Lane A** for the first ship ADR acceptance. Reasons:

- Host path is already the honesty story; A elevates it to notebook surface.
- Physicist chalk still writes continuous models at Host/Theory and sees one
  explicit finiteize step (ADR 0162 Decision 2).
- Avoids irreversible mid-program type until notebook finiteize proves demand.
- Lane B remains a **later** additive ADR after A is Runtime complete.

If the Adjudicator wants blackboard `Continuous` spelling **in the same** first
ship, Accept **Lane B with gates** and a hard MVP op list — do not half-ship B.

## Non-goals (all lanes)

- Cloud / HPC Monte Carlo SDK technology selection
- Joint rational masses (ADR 0125)
- CUDA deferred workers
- Silent continuous operators in Theory scopes without discretization
- Replacing NLTS or terminal-measure-only collapse

## Consequences if Accepted (Lane A)

1. Feature Issues: grammar/surface Red → Host wiring Green → example pedagogy.
2. ADR 0126 remains true that mid-program Continuous is absent; amend 0126
   only if Lane B is chosen instead.
3. ADR 0162 Decision 4 is satisfied by this ship ADR family.
4. Agents must not treat Acceptance of Lane A as permission for Lane B ops.

## Consequences if Accepted (Lane B)

1. Amend ADR 0126 Decision 1 (finite-only mid-program) with an explicit
   Continuous type-world exception and gates.
2. Larger HIR/typecheck surface; LINEAR / effect story must stay separate.
3. Examples must never measure Continuous.

## Open questions for Adjudicator

1. **Lane A / B / C?** (recommendation: A)
2. If A: preferred surface spelling — Host-import helper vs new keyword
   `finiteize` vs method form?
3. If B: MVP op list (prepare / map / finiteize only?) and carrier param `T`?
4. Relation to Theory `continuous_operator` + discretization bridge: same
   finiteize vocabulary or keep Theory-only?
5. Does Acceptance of this ADR authorize Feature Path Plan on named Issues
   immediately, or only Architecture of the lane?

## Implementation permission

| Item | This Proposed ADR |
|---|---|
| Architecture approval of a lane | **requested** |
| Technology selection | not required (Host port already chosen) |
| Phase 1 Red | **forbidden** until Accepted + Issue Plan |
| Kernel code | **forbidden** until Feature Path Green authorized |
