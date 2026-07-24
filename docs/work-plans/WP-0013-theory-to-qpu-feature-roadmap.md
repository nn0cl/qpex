# WP-0013: Theory-to-QPU feature roadmap

## Goal

Register and sequence the missing capabilities needed to write common
theoretical-physics expressions naturally while preserving QPex's state law,
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
| LISS-0032 second quantization | proposed | 0030/0031/0033/0019 | fermion-to-qubit contract |
| LISS-0033 symbolic IR/provenance | proposed | 0030/0031, 0017–0019 | formula-to-lowered trace |
| LISS-0034 scientific scopes | proposed | 0069–0071, 0014/0015 | import/visibility matrix |
| LISS-0035 hybrid workflow | Phase 4 Green | 0022, 0016, 0034 | Immutable provider-neutral Workflow/Job DTO contract with declarative surface and named Host update callback |
| LISS-0036 continuous/discretization | Phase 3 Green | 0018/0033 | explicit discretization record and Theory-to-Kernel Bridge |
| LISS-0037 POVM/channels | proposed | 0011/0057, 0028 | terminal/dynamic measurement matrix |

## Recommended design order

1. LISS-0038: establish semantic carriers and phase visibility first.
2. LISS-0030: smallest notation slice and prerequisite for lattice formulas.
3. LISS-0043: resolve the approved finite Open-range slice before executable
   indexed formulas feed the algebra and evolution paths.
4. LISS-0031 and LISS-0033: algebra plus expression-preserving IR.
4. LISS-0034: enforce phase separation before exposing workflow syntax.
5. LISS-0032 and LISS-0036: broaden physical domains after the symbolic
   boundary is stable.
6. LISS-0037 and LISS-0035: integrate mixed measurement and host workflow
   after their existing boundary decisions are accepted.

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
