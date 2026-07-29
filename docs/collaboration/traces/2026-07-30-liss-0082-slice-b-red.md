# LISS-0082 Slice B Phase 1 Red

- Date: 2026-07-30
- Branch: `feature/liss-0082-slice-b-red`
- Operating path: Feature Path
- Issue: LISS-0082
- Slice/phase: Slice B / Phase 1 Red
- Approval: Adjudicator message naming "LISS-0082 Slice B Phase 1 Red",
  recorded after Slice A Red/Green/Refactor completed (PR #138)
- Implementation permission: **none**
- Technology selection permission: **none**
- Post-review required: Adjudicator review before Phase 2 Green

## Scope

Added only `tests/test_quantum_semantic_ir_slice_b_red.py`, covering the Slice B
acceptance boundary:

- ordered finite `ActingSpace` with positive local dimensions and a total
  dimension consistent with its factors;
- `PureJointStateValue` / `DensityJointStateValue` whole-Joint-store carriers
  with explicit purity and no amplitude or density-matrix payload;
- generation-based one-producer / at-most-one-consuming-path verification via
  `QSEM_VALUE_USE_INVALID`;
- factor IDs as coordinates inside one Joint value, rejected when consumed as
  an independent state value.

Region kinds (Slice C), control/measurement lanes (Slice D), Physics lowering
(Slice E), pipeline wiring (Slice F), encodings, and qubit allocation remain out
of scope. No file under `compiler/` was changed.

## Red evidence

- `python3 tests/test_quantum_semantic_ir_slice_b_red.py`
  **fails as expected** with
  `ImportError: cannot import name 'ActingFactor' from
  'compiler.staqex.quantum_semantic_ir'`.
  The expected Red is the missing Slice B API, not an assertion workaround.
- `python3 -m py_compile tests/test_quantum_semantic_ir_slice_b_red.py` — passed.
- `python3 tests/test_quantum_semantic_ir_slice_a_red.py` — still passes; the
  Slice A root contract is unchanged.
- pytest is not installed in this workspace, so the direct test entry point is
  the deterministic check, matching the Slice A trace.

## Design decisions — approved 2026-07-30

Raised as assumptions at Red and **approved by the Adjudicator** in the same
session. They are recorded in the Issue and in plan §4.1.

1. Slice B DTOs embed `SemanticOrigin` directly rather than introducing the
   contract's `OriginId`, because Slice A shipped without an origin identity.
   Migration to `OriginId` belongs to a later Slice or a follow-up Issue.
2. `QuantumSemanticModule` gains exactly `acting_spaces`, `values`, and
   `value_uses`. No `regions` field and no lowering field is added in Slice B.
3. `producer_id` is an opaque `SemanticId` reference. Whether the producer is a
   well-formed region is Slice C's responsibility.
4. Slice B emits only `QSEM_ACTING_SPACE_INVALID` (unknown `space_id`,
   resource/factor arity mismatch, non-positive or inconsistent dimension) and
   `QSEM_VALUE_USE_INVALID` (unknown value, missing producer, fan-out,
   independent factor consumption).

Standing condition: ADR 0108–0111 remain **Proposed**; Slice B proceeds inside
the existing P0 approval boundary, as Slice A did.

## Documentation synchronized in this reviewable unit

- `docs/issues/LISS-0082-quantum-semantic-ir.md` — status/phase, branch,
  Slice progress table, approved Slice B decisions, decision-point checkboxes.
- `docs/specs/staqex-v1-quantum-semantic-ir-plan.md` — status, new §4.1 Slice B
  acceptance boundary, §8 next allowed operation.
- `docs/architecture/open-work-register.md` — Quantum Semantic IR row.
- `docs/collaboration/local-issue-planning.md` — LISS-0082 ID-claim row (also
  clearing drift left by PR #138).
- `docs/work-plans/WP-0025-staqex-v1-north-star.md` — LISS-0082 status and
  `Current next issue` phase/approval lines.

## Stop condition

Stop after Red evidence. Do not modify `compiler/`, do not edit the reviewed
assertions to make them pass, and do not begin Phase 2 Green, Slice C, lowering,
or pipeline work without separate approval.
