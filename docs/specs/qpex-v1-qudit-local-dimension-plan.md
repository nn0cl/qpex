# Staqex qutrit / qudit finite local-dimension plan (LISS-0074)

| Field | Value |
|---|---|
| Status | **complete** (2026-07-29); D=3 SV → [LISS-0112](../issues/LISS-0112-qutrit-qudit-d3-statevector-mvp.md) **complete** |
| Authority | WP-0025 E1; ADR 0106 D3; ADR 0102; [`staqex-v1-language-north-star.md`](staqex-v1-language-north-star.md) §5.2; [`staqex-v1-compiler-blueprint.md`](../architecture/staqex-v1-compiler-blueprint.md) |
| Depends on | LISS-0068 **complete**; LISS-0071 **complete**; LISS-0029 / LISS-0058 **reviewed** |
| Last updated | 2026-07-29 |

This companion freezes the **LISS-0074** design intake. Adjudicator plan
approval selects the recommended direction and authorizes **Slice A Phase 1
Red** only.

## 1. Goals

1. **Nominal finite carriers** — `Qutrit`, `Qudit<D>`, `QutritRegister<N>`,
   `QuditRegister<D, N>` are type-level shapes, not integer arrays.
2. **Label safety** — ket/bra labels are checked against local dimension before
   lowering.
3. **Acting-space honesty** — qudit carriers participate in ADR 0102 rules;
   no silent qubit coercion.
4. **Fail closed on backends** — unsupported QASM/QPU paths reject qudits
   explicitly.
5. **Spec truth** — EBNF / language-spec catch-up with accepted slices.

## 2. Current baseline (evidence)

| Surface | Today | Gap |
|---|---|---|
| `QubitRegister<N>` | ✓ typecheck + SV/QASM paths | — |
| `Qutrit` / `Qudit<D>` | ✓ Slice A type surface | — |
| Ket label vs dimension | ✓ Slice B typecheck on `State<Qutrit>` / `State<Qudit<D>>` | — |
| Acting space | ✓ Slice C typecheck + declared-space for qudit registers | — |
| Runtime SV | ✓ LISS-0074 D hard reject; D=3 measure+Identity → [LISS-0112](../issues/LISS-0112-qutrit-qudit-d3-statevector-mvp.md) **complete** | clock/shift / D≠3 / register SV (later) |
| QASM / QPU | ✓ Slice E hard reject (no silent embed) | OpenQASM qudit opcodes (later) |

Shipping Kernel remains Python. No Rust gate (LISS-0070 deferred).

## 3. Architecture boundary

```text
source TypeRef / State / Operator annotations
  → typecheck (dimension + register shape)
  → ket/bra label check vs local dim
  → acting-space / tensor compatibility
  → runtime elaboration (optional D=3 MVP) OR hard unsupported
  → backend capability reject (QASM/QPU)
```

Rules:

- No hidden encoding of qudits as qubits.
- No Physics IR / continuous engines in this Issue.
- Multi-register naming remains LISS-0067; this Issue adds local-dimension
  carriers into that model without provider routing.

## 4. Recommended type map

| Surface | Meaning |
|---|---|
| `Qubit` | local dim 2 (existing) |
| `Qutrit` | local dim 3 (nominal) |
| `Qudit<D>` | local dim `D` (static positive int) |
| `QubitRegister<N>` | N qubits (existing) |
| `QutritRegister<N>` | N qutrits |
| `QuditRegister<D, N>` | N sites of local dim `D` |

**Recommended:** `Qutrit` and `Qudit<3>` are **dimensionally equivalent** for
label and acting-space checks; both remain **nominal names** (not `Int`
aliases). Exact interchangeability in the type lattice is fixed in Slice A/C
Red assertions.

## 5. Planned slices

| Slice | Scope | Exit |
|---|---|---|
| **A** | Validate type surface + EBNF | Types parse; bad `D`/`N` diagnostics |
| **B** | Ket/Bra label vs local dim | Invalid labels hard-fail |
| **C** | Acting-space / Operator / tensor | No silent qubit coercion |
| **D** | Runtime MVP (`D=3`) or documented deferral | Explicit SV path **or** hard unsupported |
| **E** | Backend reject + conformance goldens | Issue acceptance notes satisfied |

### Recommended first Red batch

**Slice A only** after plan approval (done — Green).

### Slice A plan (complete)

Shipped: `_validate_local_dimension_surface` for `Qutrit` / `Qudit<D>` /
`QutritRegister<N>` / `QuditRegister<D,N>`; `LOCAL_DIMENSION_TYPE_ERROR` hard
code; EBNF type productions; register binds as `Ty("Register", …)`.

### Slice B plan (complete)

**Shipped:** `_local_dim_of_state_carrier` + `_check_ket_bra_local_dimension`
on typed `StateBind`; numeric `k` must satisfy `0 ≤ k < D` (`Qutrit` ≅ 3);
out-of-range → `LOCAL_DIMENSION_TYPE_ERROR`; alone ket without qudit carrier
unchanged.

**Suite:** `tests/test_qudit_slice_b_red.py` PASS.

### Slice C plan (complete)

**Shipped:**
- `operator_declared_space` resolves `QutritRegister<N>` / `QuditRegister<D,N>`
- `_operator_domain_payload`: `QutritRegister<N>` ≅ `QuditRegister<3,N>` via
  `LocalRegister<3,N>`
- `_check_silent_qubit_operator_coercion` rejects `Operator<QubitRegister>` in
  qudit-only register contexts

**Suite:** `tests/test_qudit_slice_c_red.py` PASS.

### Slice D plan (complete)

**Shipped:** hard `UNSUPPORTED_LOCAL_DIMENSION` (pipeline hard code) at
measure / evolve / apply entry for deferred `State<Qutrit|Qudit<…>>` and
`LocalRegister` / `LocalSite` Operator domains. Annotations alone remain
typecheckable (Slice A–C). No D=3 SV.

**Suite:** `tests/test_qudit_slice_d_red.py` PASS.

### Slice E plan (complete)

**Shipped:**
- `run.HARD_CODES` includes `UNSUPPORTED_LOCAL_DIMENSION` /
  `LOCAL_DIMENSION_TYPE_ERROR`
- `qudit_capability_reject` in QASM lower + emit (empty QASM; named reject)
- Conformance `E06-002`; diagnostic catalog entries
- Issue acceptance notes satisfied; real D=3 SV → [LISS-0112](../issues/LISS-0112-qutrit-qudit-d3-statevector-mvp.md)

**Suite:** `tests/test_qudit_slice_e_red.py` PASS.

## 6. Non-goals

- Photonic / continuous / infinite dim
- Full qudit OpenQASM opcode set
- LISS-0075 linear usage
- LISS-0081 Physics IR
- Rust (LISS-0070)

## 7. Verification

- Docs-only plan PR; no `compiler/` / `tests/` until Slice A Red.
- After each Green: standalone slice tests + SV gate when runtime is touched.

## 8. Adjudicator decisions

See [`LISS-0074`](../issues/LISS-0074-qutrit-qudit-finite-local-dimension-types.md)
Decision Points (plan). Recommended defaults:

1. Slices A–E as tabled.
2. `Qutrit` ≅ `Qudit<3>` for dimension checks; both nominal.
3. Slice A Phase 1 Red only after plan approval.
4. Slice D: typecheck-first; `D=3` SV only if small; else hard unsupported.
5. QASM/QPU: named hard reject (no qubit embed).
6. Reuse existing diagnostic families where fit.
