# QPex qudit D=3 state-vector MVP plan (LISS-0112)

| Field | Value |
|---|---|
| Status | **Slice C Phase 1 Red** (2026-07-29) |
| Authority | WP-0025; ADR 0106 D3; LISS-0074 complete; [`qpex-v1-language-north-star.md`](qpex-v1-language-north-star.md) §5.2 |
| Depends on | [LISS-0074](../issues/LISS-0074-qutrit-qudit-finite-local-dimension-types.md) **complete** |
| Last updated | 2026-07-29 |

This companion freezes the **LISS-0112** design intake. Adjudicator plan
approval selected the recommended MVP; Slices A–B shipped Kernel D=3
measure + Identity paths.

## 1. Goals

1. **Real dim-3 SV** for `State<Qutrit>` / `State<Qudit<3>>` in the shipping
   Python Kernel.
2. **Lift** `UNSUPPORTED_LOCAL_DIMENSION` only on approved MVP entry points
   (measure; Identity evolve / apply(I)).
3. **Fail closed** elsewhere (D≠3 SV, QASM, qubit Pauli silent embed).
4. Preserve LISS-0074 type / label / acting-space contracts.

## 2. Baseline after LISS-0074

| Surface | Today (after A–B) | Gap |
|---|---|---|
| Type / labels / acting-space | ✓ LISS-0074 A–C | — |
| Measure on D=3 | ✓ LISS-0112 A | — |
| Identity evolve / apply(I) on D=3 | ✓ LISS-0112 B | — |
| Non-Identity / D≠3 / QASM | ✓ hard reject | Slice C catalog note |

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
| **B** | Identity evolve / apply(I); dim-3 consistency | **complete** |
| **C** | Conformance / catalog / closeout; QASM + D≠3 still reject | **Phase 1 Red** |

### Slice A (complete)

Shipped: measure allow for `Qutrit`/`Qudit<3>`; ket label `2`; `Qudit<D>`
payload.

### Slice B (complete)

Shipped: bare Identity `apply(I)` / `evolve … under I` on D=3; runtime
no-op preserves levels; non-Identity and D≠3 remain rejected.

### Slice C plan (proposed)

**Scope:** Issue closeout only — no new Kernel SV behavior.

1. Conformance catalog entry for D=3 SV MVP (measure + Identity; cite
   `tests/test_qudit_d3_sv_slice_{a,b}_red.py`).
2. Diagnostic catalog: note LISS-0112 lifts measure + Identity; retain
   `UNSUPPORTED_LOCAL_DIMENSION` for QASM / D≠3 / non-Identity.
3. Regression Red: QASM emit still rejects `State<Qutrit>`; `Qudit<4>`
   measure/apply still unsupported; A/B suites still PASS.
4. Mark Issue / register / WP complete; point LISS-0074 follow-up as done.

**Out of Slice C:** clock/shift gates; register multi-site SV; OpenQASM
qudit opcodes; bound `Operator = I` expansion beyond bare atom (deferred).

**Red suite (after plan approval):** `tests/test_qudit_d3_sv_slice_c_red.py`

### Recommended next Red batch

**Slice C only** — after Adjudicator plan approval.

## 6. Non-goals

See Issue non-goals. Do not expand mid-Issue without Adjudicator stop.

## 7. Verification

- After Slice C Green: A/B/C suites + LISS-0074 `test_qudit_slice_*` +
  QASM reject regression.

## 8. Adjudicator decisions

See [`LISS-0112`](../issues/LISS-0112-qutrit-qudit-d3-statevector-mvp.md)
Decision Points (plan + Slice C). Recommended defaults:

1. Issue + slices A–C as tabled.
2. MVP = measure + Identity evolve/apply(I) (A–B shipped).
3. Slice C = catalog / conformance / closeout only.
4. QASM hard reject continues.
