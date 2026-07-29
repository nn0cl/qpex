# QPex phase-resolved typed HIR plan (LISS-0080)

| Field | Value |
|---|---|
| Status | **Slice B plan ready for review** (2026-07-29) |
| Authority | WP-0025 E2; ADR 0106 D9; [`qpex-v1-compiler-blueprint.md`](../architecture/qpex-v1-compiler-blueprint.md) §4.1 |
| Depends on | [LISS-0071](../issues/LISS-0071-versioned-conformance-and-differential-oracle.md) **complete**; [LISS-0072](../issues/LISS-0072-lossless-cst-formatter-and-source-versioning.md) **complete** |
| Does not depend on | LISS-0070 (Rust deferred) |
| Unlocks | LISS-0075; LISS-0081 / LISS-0082 |
| Last updated | 2026-07-29 |

This companion freezes the **LISS-0080** design intake. Slice A shipped the
immutable HIR DTO; Slice B adds declaration phase.

## 1. Goals

1. Ship an **immutable phase-resolved typed HIR** on the Python Shipping Kernel.
2. Extract additively from [`typecheck.py`](../../compiler/qpex/typecheck.py)
   (`Ty`, `typed`, `fun_effects`) — **no big-bang IR rewrite**.
3. Record resolved symbols, declaration phase, typed expressions, effects /
   capabilities, and provenance per blueprint §4.1.
4. Keep frontend diagnostics at/before HIR; leave Physics IR and linear
   analysis to later Issues.

## 2. Baseline (after Slice A)

| Surface | Today | Gap |
|---|---|---|
| CST / formatter | ✓ LISS-0072 | — |
| Immutable HIR symbols + typed | ✓ LISS-0080 A (`hir.py`) | — |
| Scientific-scope phase contracts | ✓ LISS-0034 (sealed) | decl phase on HIR |
| Effects on HIR | typecheck `fun_effects` only | Slice C |
| Provenance / verifier | spans exist on AST | Slice D |
| Linear usage | not shipped | LISS-0075 |

## 3. Architecture boundary

```text
Source/CST (LISS-0072)
  -> AST + TypeChecker (shipping)
  -> immutable HIR view (LISS-0080)   ← this Issue
  -> Physics IR (LISS-0081)          ← out
  -> Quantum Semantic IR (LISS-0082) ← out
```

Rules:

- Additive module (`compiler/qpex/hir.py`); typecheck remains authoritative.
- Slice A: API / DTO only — evaluator unwired (**complete**).
- Rust HIR mirrors later under LISS-0070.

## 4. MVP (fixed for this Issue)

**In:** immutable HIR DTO; build from TypeChecker; decl phase; effects /
capabilities lift; provenance + construction verifier.

**Out:** Physics IR; Quantum Semantic IR; proof-driven uncomputation;
body-level phase typing (LISS-0076); Rust; big-bang pipeline rewrite.

## 5. Planned slices

| Slice | Scope | Exit |
|---|---|---|
| **A** | Immutable HIR DTO + build API (symbols / `Ty` map); evaluator unwired | **complete** |
| **B** | Declaration phase on HIR decls (existing scope contracts; not 0076) | **plan ready** |
| **C** | Effects / capabilities explicit on HIR (`fun_effects` lift) | Red→Green |
| **D** | Provenance + verifier + closeout; linear analysis → LISS-0075 | Red→Green |

### Slice A (complete)

Shipped: `HirModule` + `build_hir(TypeChecker)` with `MappingProxyType`
symbols / typed; evaluator unwired.

### Slice B plan (proposed)

**Scope:** Record declaration **phase** on HIR decls from LISS-0034
scientific-scope `kind` (`theory` / `experiment` / `workflow` / `execution` /
`report`) via sealed `scope_contracts` / scope decls.

**Policy:**
- Phase tags come from existing sealed contracts — not body-level typing.
- Programs without scientific scopes use documented default (`kernel` /
  unscoped).
- `build_hir` may accept optional `scope_contracts` / unit decls additively;
  Slice A call shape remains valid when omitted (empty/default phases).

**Out of Slice B:** effects (C), provenance (D), LISS-0076, evaluator rewire.

**Red suite (after plan approval):** `tests/test_hir_slice_b_red.py`

### Recommended next Red batch

**Slice B only** — after Adjudicator plan approval.

## 6. Non-goals

See Issue non-goals. Do not expand mid-Issue without Adjudicator stop.

## 7. Verification

- After Slice B Green: A + B suites; typecheck regression if `hir.py` touched.

## 8. Adjudicator decisions

See [`LISS-0080`](../issues/LISS-0080-phase-resolved-typed-hir.md)
Decision Points (plan + Slice B). Recommended defaults:

1. Slice B = decl phase from LISS-0034 scope kinds only.
2. Default phase for unscoped Kernel programs.
3. Additive `build_hir` inputs; no big-bang pipeline rewrite.
4. Slice B Phase 1 Red only after plan approval.
