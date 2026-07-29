# LISS-0112: Qutrit / qudit D=3 state-vector MVP

## Metadata

- Local issue ID: LISS-0112
- GitHub issue: not created
- Status: **Slice A Red ready for review** (2026-07-29)
- Phase: slice-a phase-1-red
- Type: Kernel runtime / state-vector / finite local dimension
- Priority: P0
- Initial planning size: L
- Current planning size: L (sliced A–C)
- Owner/agent: —
- Related branch: `feature/liss-0112-slice-a-red`
- Parent: [WP-0025](../work-plans/WP-0025-qpex-v1-north-star.md) E1 / Kernel SV
- Depends on: [LISS-0074](LISS-0074-qutrit-qudit-finite-local-dimension-types.md)
  **complete** (type surface, labels, acting-space, hard reject)
- Related: [LISS-0029](LISS-0029-static-hilbert-kernel-surface.md);
  [ADR 0102](../architecture/adr/0102-acting-space-typing.md);
  [ADR 0106](../architecture/adr/0106-qpex-v1-north-star-language-and-compiler.md) D3;
  [north-star §5.2](../specs/qpex-v1-language-north-star.md);
  [qudit type plan](../specs/qpex-v1-qudit-local-dimension-plan.md)

## Summary

Ship a **real dim-3 state-vector path** in the Python Kernel for
`State<Qutrit>` / `State<Qudit<3>>`, lifting the LISS-0074
`UNSUPPORTED_LOCAL_DIMENSION` hard reject on the approved MVP surfaces only.

LISS-0074 established nominal carriers, label checks, acting-space honesty,
and fail-closed QASM. This Issue supplies the deferred **execution** layer
for D=3 without silently embedding into qubit `2**n` SV.

Plan companion:
[`qpex-v1-qudit-d3-sv-plan.md`](../specs/qpex-v1-qudit-d3-sv-plan.md).

## Acceptance Notes (Issue complete when)

1. `State<Qutrit>` / `State<Qudit<3>>` with `|0⟩` / `|1⟩` / `|2⟩` measure under
   a **dim-3** Kernel SV (not qubit `2**n`).
2. Identity `evolve` / `apply(I)` on the same single-site carriers succeed with
   Hilbert dimension 3 preserved.
3. Unsupported paths remain fail-closed with named diagnostics:
   general Pauli-as-qubit on qudit, `Qudit<D>` SV for `D ≠ 3`, QASM emission.
4. Slices A–C Red/Green land; LISS-0074 type / label / acting-space contracts
   unchanged; conformance note updated.
5. No OpenQASM qudit opcodes, multi-site register SV, or general-D SV in this
   Issue.

## Planned slices

| Slice | Scope | Phase gate |
|---|---|---|
| **A** | Ket `|0..2⟩` + measure on `State<Qutrit>` / `Qudit<3>`; lift
  `UNSUPPORTED_LOCAL_DIMENSION` on that path only; `ket_support` / measure dim | **Red ready for review** |
| **B** | Identity evolve / apply(I) on single qutrit; SV dim=3 consistency | plan → Red → Green → Refactor |
| **C** | Conformance / catalog / docs closeout; keep QASM + D≠3 reject; Issue done | plan → Red → Green → Refactor |

## Non-goals

- General clock/shift (generalized X/Z) gate set.
- `QutritRegister` / multi-site qudit SV.
- OpenQASM qudit opcodes / QPU capability for qudits.
- Generic `Qudit<D>` SV for `D ≠ 3`.
- Continuous / photonic / Physics IR.
- Linear usage (LISS-0075).
- Rust frontend (LISS-0070).

## Adjudicator Decision Points (plan)

- [x] Approve Issue ID **LISS-0112**, acceptance notes, and slices A–C above.
- [x] Confirm MVP fixed to **measure + Identity evolve/apply(I)** (recommended).
- [x] Confirm first Red batch: **Slice A only** after plan approval.
- [x] Confirm QASM remains **hard reject** in this Issue (no qudit emit).

## Adjudicator Decision Points (Slice A Red)

- [ ] Approve Phase 1 Red assertions (`tests/test_qudit_d3_sv_slice_a_red.py`).
- [ ] Authorize Phase 2 Green for D=3 ket + measure only (lift
      `UNSUPPORTED_LOCAL_DIMENSION` on that path; keep D≠4 / QASM reject).

## Work Notes

- 2026-07-29: Plan intake opened after Adjudicator selected D=3 SV follow-up
  (option 2) post LISS-0074 closeout (PR #108).
- 2026-07-29: Plan merged via PR #109 (`2fc6f4e`). Plan **approved** (“承認”).
  Phase 1 Red — `tests/test_qudit_d3_sv_slice_a_red.py`. Expected Red:
  `State<Qutrit>` / `Qudit<3>` measure still emits
  `UNSUPPORTED_LOCAL_DIMENSION` (including `|2⟩`).

## Verification

- Plan: merged PR #109.
- Slice A: Red suite on `feature/liss-0112-slice-a-red`.
