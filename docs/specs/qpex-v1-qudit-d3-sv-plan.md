# QPex qudit D=3 state-vector MVP plan (LISS-0112)

| Field | Value |
|---|---|
| Status | **Slice B plan ready for review** (2026-07-29) |
| Authority | WP-0025; ADR 0106 D3; LISS-0074 complete; [`qpex-v1-language-north-star.md`](qpex-v1-language-north-star.md) §5.2 |
| Depends on | [LISS-0074](../issues/LISS-0074-qutrit-qudit-finite-local-dimension-types.md) **complete** |
| Last updated | 2026-07-29 |

This companion freezes the **LISS-0112** design intake. Adjudicator plan
approval selects the recommended MVP and authorizes **Slice A Phase 1 Red**
only.

## 1. Goals

1. **Real dim-3 SV** for `State<Qutrit>` / `State<Qudit<3>>` in the shipping
   Python Kernel.
2. **Lift** `UNSUPPORTED_LOCAL_DIMENSION` only on approved MVP entry points
   (measure; Identity evolve / apply(I)).
3. **Fail closed** elsewhere (D≠3 SV, QASM, qubit Pauli silent embed).
4. Preserve LISS-0074 type / label / acting-space contracts.

## 2. Baseline after LISS-0074

| Surface | Today | Gap |
|---|---|---|
| Type / labels / acting-space | ✓ LISS-0074 A–C | — |
| Measure / evolve / apply on qudit | ✓ hard `UNSUPPORTED_LOCAL_DIMENSION` | real D=3 SV |
| QASM / QPU | ✓ hard reject | keep reject in 0112 |

## 3. Architecture boundary

```text
LISS-0074 carriers + UNSUPPORTED_LOCAL_DIMENSION
  → LISS-0112 lifts reject on D=3 measure / Identity paths
  → ket_support + evaluator use local dim 3 (not 2**n)
  → QASM / D≠3 / non-Identity gates remain fail-closed
```

Rules:

- No silent qubit embedding.
- No OpenQASM qudit opcodes in this Issue.
- Multi-site register SV is out of scope.

## 4. MVP (fixed for this Issue)

**In:** single-site `Qutrit` ≅ `Qudit<3>`; ket `|0⟩`…`|2⟩`; measure;
Identity evolve / apply(I).

**Out:** clock/shift gate family; `QutritRegister` SV; `Qudit<D>` for D≠3;
QASM qudit emit; Rust.

## 5. Planned slices

| Slice | Scope | Exit |
|---|---|---|
| **A** | Ket + measure; lift reject on that path; dim-3 `ket_support` | **complete** |
| **B** | Identity evolve / apply(I); dim-3 consistency | **Green+Refactor ready** |
| **C** | Conformance / catalog / closeout; QASM + D≠3 still reject | Red→Green |

### Slice A (complete)

Shipped: measure allow for `Qutrit`/`Qudit<3>`; ket label `2`; `Qudit<D>`
payload; evolve/apply remain rejected until Slice B.

### Slice B (Green ready)

Shipped (pending completion approval): bare Identity `apply(I)` /
`evolve … under I` on `Qutrit`/`Qudit<3>`; runtime no-op preserves levels;
non-Identity and D≠3 remain rejected.

### Recommended next Red batch

**Slice C** — after Adjudicator Slice B completion + Slice C plan approval.

## 6. Non-goals

See Issue non-goals. Do not expand mid-Issue without Adjudicator stop.

## 7. Verification

- Docs-only plan PR; no `compiler/` / `tests/` until Slice A Red.
- After each Green: slice suite + LISS-0074 regression (`test_qudit_slice_*`).

## 8. Adjudicator decisions

See [`LISS-0112`](../issues/LISS-0112-qutrit-qudit-d3-statevector-mvp.md)
Decision Points (plan). Recommended defaults:

1. Issue + slices A–C as tabled.
2. MVP = measure + Identity evolve/apply(I).
3. Slice A Phase 1 Red only after plan approval.
4. QASM hard reject continues.
