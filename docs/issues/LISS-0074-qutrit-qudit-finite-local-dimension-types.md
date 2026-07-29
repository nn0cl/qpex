# LISS-0074: Qutrit, qudit, and finite local-dimension types

## Metadata

- Local issue ID: LISS-0074
- GitHub issue: not created
- Status: **Slice C plan ready for review** (2026-07-29)
- Phase: slice-b complete; slice-c phase-0-design
- Type: language type system / static Hilbert surface / acting space
- Priority: P0
- Initial planning size: L
- Current planning size: L (sliced A–E; A–B complete)
- Owner/agent: —
- Related branch: `feature/liss-0074-slice-b-red`
- Parent: [WP-0025](../work-plans/WP-0025-qpex-v1-north-star.md) E1 — Source and frontend
- Depends on: [LISS-0068](LISS-0068-qpex-v1-normative-rebaseline.md) **promoted**;
  [LISS-0071](LISS-0071-versioned-conformance-and-differential-oracle.md) **complete**
- Related: [LISS-0029](LISS-0029-static-hilbert-kernel-surface.md) (`QubitRegister<N>`);
  [LISS-0058](LISS-0058-acting-space-typing.md) / [ADR 0102](../architecture/adr/0102-acting-space-typing.md);
  [LISS-0067](LISS-0067-multi-register-acting-space-and-qpu-mapping.md);
  [ADR 0106](../architecture/adr/0106-qpex-v1-north-star-language-and-compiler.md) D3;
  [north-star §5.2](../specs/qpex-v1-language-north-star.md)

## Summary

Extend the shipping Kernel’s **finite local-dimension** type surface beyond
qubits so that `Qutrit`, `Qudit<D>`, `QutritRegister<N>`, and
`QuditRegister<D, N>` are **nominal carriers** (not integer-array aliases),
with compile-time basis-label checking and acting-space compatibility.

Invalid ket labels and incompatible local dimensions must fail **before**
lowering. QPU / OpenQASM targets that do not advertise qudit support must
fail closed with named diagnostics — never silently map to qubits.

Plan companion:
[`qpex-v1-qudit-local-dimension-plan.md`](../specs/qpex-v1-qudit-local-dimension-plan.md).

## Acceptance Notes (Issue complete when)

1. `Qutrit`, `Qudit<D>`, `QutritRegister<N>`, and `QuditRegister<D, N>` parse
   and typecheck as nominal shapes (positive integer `D`, `N`).
2. Ket / bra labels are checked against the declared local carrier dimension
   (e.g. `|3⟩` rejected on `State<Qutrit>` / `Qudit<3>`).
3. Acting-space / Operator / tensor combinations involving qudit carriers
   follow ADR 0102 / LISS-0058 rules (no silent qubit coercion).
4. Unsupported backend / capability paths reject qudit programs with named
   codes (no silent qubit embedding).
5. Conformance goldens cover valid and invalid cases; no Physics IR / continuous
   / photonic engines in this Issue.
6. EBNF / language-spec catch-up lands with the slices that introduce forms.

## Planned slices

| Slice | Scope | Phase gate |
|---|---|---|
| **A** | Type surface: `Qutrit` / `Qudit<D>` / `QutritRegister<N>` / `QuditRegister<D,N>` validation in typecheck (+ EBNF note) | **complete** |
| **B** | Ket/Bra label cardinality vs declared local dimension | **complete** |
| **C** | Acting-space / `Operator` / tensor compatibility for qudit carriers | **plan ready for review** |
| **D** | Shipping Kernel MVP elaboration for `D = 3` (optional small-D SV path) **or** explicit typecheck-only deferral of runtime | plan → Red → Green → Refactor |
| **E** | Backend / capability hard reject + conformance goldens; Issue closeout | plan → Red → Green → Refactor |

## Non-goals (initial)

- Continuous / photonic / infinite-dimensional carriers.
- Silent mapping of qudits to qubit encodings.
- Full QPU / OpenQASM qudit opcode set.
- Physics IR (LISS-0081).
- Linear usage / uncomputation (LISS-0075).
- Rust frontend (LISS-0070 deferred).
- Changing qubit-only examples unless a minimal golden is required.

## Adjudicator Decision Points (plan)

- [x] Approve planned slices A–E and Issue acceptance notes above.
- [x] Confirm `Qutrit` vs `Qudit<3>`: recommended **both nominal; dimensionally
      equivalent for label/acting-space checks** (not an `Int` alias).
- [x] Confirm first Red batch: **Slice A only** after plan approval.
- [x] Confirm Slice D default: recommended **typecheck + acting-space first;
      `D = 3` SV MVP only if Green stays small**; otherwise document
      typecheck-only runtime deferral with hard “unsupported dim” diagnostics.
- [x] Confirm backend policy: qudit on QASM/QPU → **named hard reject** until a
      later capability Issue (no silent qubit embed).
- [x] Confirm diagnostics: reuse acting-space / static-Hilbert families where
      fit; add named codes only when qudit-specific shape is required.
- [x] Approve Phase 1 Red for **Slice A only** after plan approval.

## Adjudicator Decision Points (Slice A Red)

- [x] Approve Phase 1 Red assertions (`tests/test_qudit_slice_a_red.py`).
- [x] Authorize Phase 2 Green for type-surface validation + EBNF note only.

## Adjudicator Decision Points (Slice A Green / Refactor)

- [x] Approve Phase 2 Green + Phase 3 Refactor (`_validate_local_dimension_surface`,
      `LOCAL_DIMENSION_TYPE_ERROR` as hard code, EBNF qutrit/qudit productions).
- [x] Confirm Slice A complete and allow Slice B plan intake (ket/bra label
      cardinality).

## Adjudicator Decision Points (Slice B plan)

- [x] Approve **Slice B** plan for Phase 1 Red only (ket/bra label cardinality
      vs declared local dimension).
- [x] Confirm label policy (recommended): numeric labels `|0⟩`…`|D-1⟩` on
      `State<Qutrit>` / `State<Qudit<D>>` (and matching register element carriers);
      out-of-range → `LOCAL_DIMENSION_TYPE_ERROR` (or dedicated label code if
      clearer). Named non-numeric labels deferred unless already supported for
      qubits.
- [x] Confirm Slice B excludes acting-space (C), SV (D), backend reject (E).
- [x] Approve Phase 1 Red for **Slice B only** after plan approval.

## Adjudicator Decision Points (Slice B Red)

- [x] Approve Phase 1 Red assertions (`tests/test_qudit_slice_b_red.py`).
- [x] Authorize Phase 2 Green for ket/bra label cardinality checks only.

## Adjudicator Decision Points (Slice B Green / Refactor)

- [x] Approve Phase 2 Green + Phase 3 Refactor (`_check_ket_bra_local_dimension`
      on `State<Qutrit>` / `State<Qudit<D>>`; out-of-range →
      `LOCAL_DIMENSION_TYPE_ERROR`).
- [x] Confirm Slice B complete and allow Slice C plan intake (acting-space /
      Operator / tensor for qudit).

## Adjudicator Decision Points (Slice C plan)

- [ ] Approve **Slice C** plan for Phase 1 Red only (acting-space / Operator /
      tensor for qudit carriers; no silent qubit coercion).
- [ ] Confirm recommended policy:
      - Extend `operator_declared_space` / identity acting-space resolution beyond
        `QubitRegister<N>` to `QutritRegister<N>` / `QuditRegister<D,N>` (and
        single-site `Qutrit` / `Qudit<D>` where applicable).
      - Reject `Operator<QubitRegister<…>>` (or qubit identity lowering) in a
        qudit-only program context — no silent qubit annotation.
      - Keep existing `OPERATOR_DOMAIN_ERROR` for
        `Operator<QubitRegister>` ↛ `Operator<QutritRegister>`.
      - Treat `Qutrit` ≅ `Qudit<3>` and `QutritRegister<N>` ≅ `QuditRegister<3,N>`
        as **dimensionally equivalent** for acting-space checks (still nominal).
      - Reuse `OPERATOR_DOMAIN_ERROR` / `ACTING_SPACE_MISMATCH` /
        `IDENTITY_ACTING_SPACE_UNDETERMINED` where fit; new codes only if needed.
- [ ] Confirm Slice C excludes SV/runtime (D), backend reject (E), RegisterSet
      qudit expansion (ADR 0105 follow-up), and Pauli/SV materialization for D≠2.
- [ ] Approve Phase 1 Red for **Slice C only** after plan approval.

## Work Notes

- 2026-07-29: Plan intake opened after LISS-0073 completion (PR #102/#103).
  Dependencies LISS-0068 / LISS-0071 confirmed complete. LISS-0029 remains the
  qubit register baseline.
- 2026-07-29: Plan **approved** (“承認”) with recommended defaults. Phase 1 Red —
  `tests/test_qudit_slice_a_red.py`. Expected Red: `Qudit<0>` / bad arity /
  nonpositive registers currently accepted (no `LOCAL_DIMENSION_TYPE_ERROR`);
  EBNF lacks qutrit/qudit productions.
- 2026-07-29: Slice A Phase 1 Red **approved** (“承認”); Phase 2 Green +
  Phase 3 Refactor. Typecheck validates qutrit/qudit shapes; hard
  `LOCAL_DIMENSION_TYPE_ERROR`; EBNF productions. Suite PASS.
- 2026-07-29: Slice A completion **approved** (“承認”). Slice B plan proposed
  for ket/bra label cardinality vs local dimension.
- 2026-07-29: Slice A merged via PR #104 (`601525c`).
- 2026-07-29: Slice B plan **approved** (“承認”). Phase 1 Red —
  `tests/test_qudit_slice_b_red.py`. Expected Red: `|3⟩` on `State<Qutrit>`
  (and `|4⟩` on `Qudit<4>`) currently accepted without
  `LOCAL_DIMENSION_TYPE_ERROR`.
- 2026-07-29: Slice B Phase 1 Red **approved** (“承認”); Phase 2 Green +
  Phase 3 Refactor. Typecheck checks numeric ket/bra labels against local
  dimension on `State<Qutrit>` / `State<Qudit<D>>`. Suite PASS.
- 2026-07-29: Slice B Green+Refactor **approved** (“承認”). Slice C plan
  proposed for acting-space / Operator / tensor (no silent qubit coercion).

## Verification

- Slice A: merged via PR #104; suite PASS.
- Slice B: `python3 tests/test_qudit_slice_b_red.py` PASS on
  `feature/liss-0074-slice-b-red` (PR pending).
- Slice C: plan only — no Red until Adjudicator approval.
