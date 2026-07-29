# WP-0013: Theory-to-QPU feature roadmap

## Goal

Register and sequence the missing capabilities needed to write common
theoretical-physics expressions naturally while preserving Staqex's state law,
phase boundaries, and honest QPU lowering.

## Scope

- In: roadmap research, LISS-0030 through LISS-0037, and cross-references to
  existing open LISS/ADR/spec documents.
- Out: parser/runtime implementation, provider SDKs, credentials, cloud
  submission, and acceptance of any proposed syntax.

## Issue graph

| Issue | Status | Depends on | First evidence |
|---|---|---|---|
| LISS-0038 semantic carriers/phases | Phase 3 reviewed | ADR 0018, ADR 0069, LISS-0018 | type/phase matrix + representation mismatch cases; indexed syntax remains LISS-0030 |
| LISS-0030 binders/domains | Phase 3 reviewed | LISS-0038, ADR 0069 | finite sum formula + negative scope cases; runtime lowering remains deferred |
| LISS-0043 finite binder lowering | Phase 3 reviewed | LISS-0030, LISS-0038, LISS-0029, ADR 0088 | inclusive Open range → concrete Pauli Operator with diagnostics, resource guard, and provenance |
| LISS-0031 operator algebra | Phase 3 reviewed | LISS-0030, ADR 0087 | typed function-shaped algebra; punctuation sugar deferred |
| LISS-0032 second quantization | Complete (Jordan-Wigner scope) | 0030/0031/0033/0019 | typed family/statistics boundary and explicit mapping metadata; Jordan-Wigner numerical mapping for one-body/two-body FermionOperator terms shipped (ADR 0093); Bravyi-Kitaev/Boson/Spin mapping remain a possible future follow-up, not scheduled |
| LISS-0033 symbolic IR/provenance | Phase 3 reviewed | 0030/0031, 0017–0019 | source-preserving Symbolic/Resolved inspection boundary; executable lowering records deferred |
| LISS-0034 scientific scopes | Phase 3 reviewed (sealed scope contracts implemented; body-level refinement remains open) | 0069–0071, 0014/0015 | import/visibility matrix |
| LISS-0035 hybrid workflow | Phase 4 reviewed | 0022, 0016, 0034 | Immutable provider-neutral Workflow/Job DTO contract with declarative surface and named Host update callback |
| LISS-0036 continuous/discretization | Phase 3 reviewed (numerical lowering deferred) | 0018/0033 | explicit discretization record and Theory-to-Kernel Bridge |
| LISS-0037 POVM/channels | Phase 3 reviewed; terminal computational-basis POVM slice complete | 0011/0057, 0028 | terminal/dynamic measurement matrix |

## Recommended design order

Every Issue named below has reached Phase 3/4 review as of 2026-07-25 (see
the table above and `open-work-register.md`) — this ordering is historical
and complete, kept for record. Each Issue's "remains deferred" sub-scope is
still open; selecting one for Feature Path Phase 1 Red is a fresh
Adjudicator scope decision, not a continuation of this design order.

1. ~~LISS-0038: establish semantic carriers and phase visibility first.~~ Done.
2. ~~LISS-0030: smallest notation slice and prerequisite for lattice
   formulas.~~ Done.
3. ~~LISS-0043: resolve the approved finite Open-range slice before
   executable indexed formulas feed the algebra and evolution paths.~~ Done.
4. ~~LISS-0031 and LISS-0033: algebra plus expression-preserving IR.~~ Done.
5. ~~LISS-0034: enforce phase separation before exposing workflow syntax.~~
   Done (body-level refinement remains deferred).
6. ~~LISS-0032 and LISS-0036: broaden physical domains after the symbolic
   boundary is stable.~~ Done (LISS-0032's Jordan-Wigner numerical mapping
   for one-body/two-body FermionOperator terms shipped, ADR 0093;
   Bravyi-Kitaev/Boson/Spin mapping and LISS-0036's continuous/discretization
   numerical lowering remain deferred).
7. ~~LISS-0037 and LISS-0035: integrate mixed measurement and host workflow
   after their existing boundary decisions are accepted.~~ Done.

## Process gate

This plan creates design inventory only. Each Issue needs a reviewed
acceptance specification/ADR, explicit phase approval, and implementation
approval before source or tests are changed. Existing deferred work remains
deferred.

## Verification

- Check every new LISS is linked from the canonical open-work register.
- Check all dependency IDs resolve to an existing ADR or LISS.
- Run `git diff --check`.
- No runtime test is expected for this documentation-only batch.
