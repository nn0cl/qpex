# LISS-0074: Qutrit, qudit, and finite local-dimension types

## Metadata

- Local issue ID: LISS-0074
- GitHub issue: not created
- Status: **plan ready for review** (2026-07-29)
- Phase: phase-0-design
- Type: language type system / static Hilbert surface / acting space
- Priority: P0
- Initial planning size: L
- Current planning size: L (sliced A–E)
- Owner/agent: —
- Related branch: `docs/liss-0074-plan-intake`
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
| **A** | Type surface: `Qutrit` / `Qudit<D>` / `QutritRegister<N>` / `QuditRegister<D,N>` validation in typecheck (+ EBNF note) | plan → Red → Green → Refactor |
| **B** | Ket/Bra label cardinality vs declared local dimension | plan → Red → Green → Refactor |
| **C** | Acting-space / `Operator` / tensor compatibility for qudit carriers | plan → Red → Green → Refactor |
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

- [ ] Approve planned slices A–E and Issue acceptance notes above.
- [ ] Confirm `Qutrit` vs `Qudit<3>`: recommended **both nominal; dimensionally
      equivalent for label/acting-space checks** (not an `Int` alias).
- [ ] Confirm first Red batch: **Slice A only** after plan approval.
- [ ] Confirm Slice D default: recommended **typecheck + acting-space first;
      `D = 3` SV MVP only if Green stays small**; otherwise document
      typecheck-only runtime deferral with hard “unsupported dim” diagnostics.
- [ ] Confirm backend policy: qudit on QASM/QPU → **named hard reject** until a
      later capability Issue (no silent qubit embed).
- [ ] Confirm diagnostics: reuse acting-space / static-Hilbert families where
      fit; add named codes only when qudit-specific shape is required.
- [ ] Approve Phase 1 Red for **Slice A only** after plan approval.

## Work Notes

- 2026-07-29: Plan intake opened after LISS-0073 completion (PR #102/#103).
  Dependencies LISS-0068 / LISS-0071 confirmed complete. LISS-0029 remains the
  qubit register baseline.

## Verification

- Docs-only plan PR until plan approval.
- Post-approval: each slice Red → Green → Refactor; SV gate after each Green
  that touches runtime.
