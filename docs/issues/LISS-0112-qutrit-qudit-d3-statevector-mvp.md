# LISS-0112: Qutrit / qudit D=3 state-vector MVP

## Metadata

- Local issue ID: LISS-0112
- GitHub issue: not created
- Status: **complete** (2026-07-29)
- Phase: complete
- Type: Kernel runtime / state-vector / finite local dimension
- Priority: P0
- Initial planning size: L
- Current planning size: L (sliced A–C; all complete)
- Owner/agent: —
- Related branch: `feature/liss-0112-slice-c-red` (closeout)
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

1. [x] `State<Qutrit>` / `State<Qudit<3>>` with `|0⟩` / `|1⟩` / `|2⟩` measure under
   a **dim-3** Kernel SV (not qubit `2**n`).
2. [x] Identity `evolve` / `apply(I)` on the same single-site carriers succeed with
   Hilbert dimension 3 preserved.
3. [x] Unsupported paths remain fail-closed with named diagnostics:
   general Pauli-as-qubit on qudit, `Qudit<D>` SV for `D ≠ 3`, QASM emission.
4. [x] Slices A–C Red/Green land; LISS-0074 type / label / acting-space contracts
   unchanged; conformance note updated.
5. [x] No OpenQASM qudit opcodes, multi-site register SV, or general-D SV in this
   Issue.

## Planned slices

| Slice | Scope | Phase gate |
|---|---|---|
| **A** | Ket `|0..2⟩` + measure on `State<Qutrit>` / `Qudit<3>`; lift
  `UNSUPPORTED_LOCAL_DIMENSION` on that path only; `ket_support` / measure dim | **complete** |
| **B** | Identity evolve / apply(I) on single qutrit; SV dim=3 consistency | **complete** |
| **C** | Conformance / catalog / docs closeout; keep QASM + D≠3 reject; Issue done | **complete** |

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

- [x] Approve **Slice B** plan for Phase 1 Red only (Identity evolve /
      apply(I) on single-site `Qutrit` / `Qudit<3>`; dim-3 preserved).
- [x] Confirm policy: lift `UNSUPPORTED_LOCAL_DIMENSION` for Identity-only
      evolve/apply on MVP D=3 states; non-Identity operators (X/H/…) and
      `Qudit<D≠3>` remain rejected; QASM reject unchanged.
- [x] Approve Phase 1 Red for **Slice B only** after plan approval.

## Adjudicator Decision Points (Slice B Red)

- [x] Approve Phase 1 Red assertions (`tests/test_qudit_d3_sv_slice_b_red.py`).
- [x] Authorize Phase 2 Green for Identity-only evolve/apply on MVP D=3
      (keep non-Identity / D≠3 / QASM reject).

## Adjudicator Decision Points (Slice B Green / Refactor)

- [x] Approve Phase 2 Green + Phase 3 Refactor (Identity no-op runtime;
      typecheck Identity-only `allow_mvp_d3` on apply/evolve).
- [x] Confirm Slice B complete and allow Slice C plan (conformance/closeout).

## Adjudicator Decision Points (Slice C plan)

- [x] Approve **Slice C** plan for Phase 1 Red only (conformance catalog
      entry for D=3 SV MVP; diagnostic catalog notes LISS-0112 lift surfaces;
      QASM + `Qudit<D≠3>` reject regression; Issue closeout).
- [x] Confirm policy: **no** new runtime gates; **no** OpenQASM qudit emit;
      Kernel measure + Identity remain the only lifted SV paths.
- [x] Approve Phase 1 Red for **Slice C only** after plan approval.

## Adjudicator Decision Points (Slice C Red)

- [x] Approve Phase 1 Red assertions (`tests/test_qudit_d3_sv_slice_c_red.py`).
- [x] Authorize Phase 2 Green for catalog / Issue closeout only (no new
      runtime gates; QASM + D≠3 reject unchanged).

## Adjudicator Decision Points (Slice C Green / Issue complete)

- [ ] Approve Phase 2 Green + Phase 3 Refactor (E06-003; diagnostic LISS-0112
      notes; Issue **complete**).
- [ ] Confirm LISS-0112 Issue complete (PR merge).

## Work Notes

- 2026-07-29: Plan intake opened after Adjudicator selected D=3 SV follow-up
  (option 2) post LISS-0074 closeout (PR #108).
- 2026-07-29: Plan merged via PR #109 (`2fc6f4e`). Plan **approved** (“承認”).
  Phase 1 Red — `tests/test_qudit_d3_sv_slice_a_red.py`.
- 2026-07-29: Slice A Phase 1 Red **approved** (“承認”); Phase 2 Green +
  Phase 3 Refactor. Measure of `Qutrit`/`Qudit<3>` on dim-3 ket support.
- 2026-07-29: Slice A merged via PR #110 (`a50d569`).
- 2026-07-29: Slice B plan **approved** (“承認”); Red then Green Identity
  evolve/apply; merged via PR #111 (`74e6ecf`).
- 2026-07-29: Slice C plan **approved** (“承認”); Phase 1 Red then Phase 2
  Green — E06-003, diagnostic LISS-0112 notes, Issue **complete**.

## Verification

- Plan: PR #109. Slice A: PR #110. Slice B: PR #111.
- Slice C: `python3 tests/test_qudit_d3_sv_slice_c_red.py` PASS;
  A/B + LISS-0074 `test_qudit_slice_*` PASS.
