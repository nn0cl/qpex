# LISS-0112: Qutrit / qudit D=3 state-vector MVP

## Metadata

- Local issue ID: LISS-0112
- GitHub issue: not created
- Status: **Slice B plan ready for review** (2026-07-29)
- Phase: slice-a complete; slice-b phase-0-design
- Type: Kernel runtime / state-vector / finite local dimension
- Priority: P0
- Initial planning size: L
- Current planning size: L (sliced A–C; A complete)
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
  `UNSUPPORTED_LOCAL_DIMENSION` on that path only; `ket_support` / measure dim | **complete** |
| **B** | Identity evolve / apply(I) on single qutrit; SV dim=3 consistency | **plan ready for review** |
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

- [x] Approve Phase 1 Red assertions (`tests/test_qudit_d3_sv_slice_a_red.py`).
- [x] Authorize Phase 2 Green for D=3 ket + measure only (lift
      `UNSUPPORTED_LOCAL_DIMENSION` on that path; keep D≠4 / QASM reject).

## Adjudicator Decision Points (Slice A Green / Refactor)

- [x] Approve Phase 2 Green + Phase 3 Refactor (MVP D=3 measure path;
      `Qudit<D>` payload; ket `2`; evolve/apply still unsupported).
- [x] Confirm Slice A complete and allow Slice B plan/Red (Identity evolve /
      apply(I)).

## Adjudicator Decision Points (Slice B plan)

- [ ] Approve **Slice B** plan for Phase 1 Red only (Identity evolve /
      apply(I) on single-site `Qutrit` / `Qudit<3>`; dim-3 preserved).
- [ ] Confirm policy: lift `UNSUPPORTED_LOCAL_DIMENSION` for Identity-only
      evolve/apply on MVP D=3 states; non-Identity operators (X/H/…) and
      `Qudit<D≠3>` remain rejected; QASM reject unchanged.
- [ ] Approve Phase 1 Red for **Slice B only** after plan approval.

## Work Notes

- 2026-07-29: Plan intake opened after Adjudicator selected D=3 SV follow-up
  (option 2) post LISS-0074 closeout (PR #108).
- 2026-07-29: Plan merged via PR #109 (`2fc6f4e`). Plan **approved** (“承認”).
  Phase 1 Red — `tests/test_qudit_d3_sv_slice_a_red.py`. Expected Red:
  `State<Qutrit>` / `Qudit<3>` measure still emits
  `UNSUPPORTED_LOCAL_DIMENSION` (including `|2⟩`).
- 2026-07-29: Slice A Phase 1 Red **approved** (“承認”); Phase 2 Green +
  Phase 3 Refactor. Measure of `Qutrit`/`Qudit<3>` runs on dim-3 ket support;
  evolve/apply remain rejected. Suite PASS.
- 2026-07-29: Slice A Green+Refactor **approved** (“承認”). Slice B plan
  proposed for Identity evolve / apply(I). Probe: both still
  `UNSUPPORTED_LOCAL_DIMENSION`.

## Verification

- Plan: merged PR #109.
- Slice A: suite PASS on `feature/liss-0112-slice-a-red` (PR pending).
- Slice B: plan only — no Red until Adjudicator approval.