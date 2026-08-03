# Staqex qudit D=3 state-vector MVP plan (LISS-0112)

| Field | Value |
|---|---|
| Status | **complete** (2026-07-29) |
| Authority | WP-0025; ADR 0106 D3; LISS-0074 complete; [`staqex-v1-language-north-star.md`](staqex-v1-language-north-star.md) §5.2 |
| Depends on | [LISS-0074](../architecture/documentation-compression-map.md) **complete** |
| Last updated | 2026-07-29 |

This companion freezes the **LISS-0112** design intake. Slices A–C shipped
Kernel D=3 measure + Identity paths and conformance closeout.

## 1. Goals

1. **Real dim-3 SV** for `State<Qutrit>` / `State<Qudit<3>>` in the shipping
   Python Kernel.
2. **Lift** `UNSUPPORTED_LOCAL_DIMENSION` only on approved MVP entry points
   (measure; Identity evolve / apply(I)).
3. **Fail closed** elsewhere (D≠3 SV, QASM, qubit Pauli silent embed).
4. Preserve LISS-0074 type / label / acting-space contracts.

## 2. Baseline (shipped)

| Surface | Status |
|---|---|
| Type / labels / acting-space | ✓ LISS-0074 A–C |
| Measure on D=3 | ✓ LISS-0112 A |
| Identity evolve / apply(I) on D=3 | ✓ LISS-0112 B |
| Non-Identity / D≠3 / QASM | ✓ hard reject; catalog E06-003 |

## 3. Architecture boundary

```text
LISS-0074 carriers + UNSUPPORTED_LOCAL_DIMENSION
  → LISS-0112 lifts reject on D=3 measure / Identity paths
  → ket_support + evaluator use local dim 3 (not 2**n)
  → QASM / D≠3 / non-Identity gates remain fail-closed
```

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
| **C** | Conformance / catalog / closeout; QASM + D≠3 still reject | **complete** |

### Slice C (complete)

- Conformance `E06-003` (A/B oracles)
- Diagnostic catalog notes LISS-0112 lift surfaces
- Issue / register / WP marked complete

## 6. Non-goals

See Issue non-goals.

## 7. Verification

- `tests/test_qudit_d3_sv_slice_{a,b,c}_red.py` PASS
- `tests/test_qudit_slice_{a,b,c,d,e}_red.py` PASS

## 8. Adjudicator decisions

All plan / slice decisions recorded on
[`LISS-0112`](../architecture/documentation-compression-map.md).
