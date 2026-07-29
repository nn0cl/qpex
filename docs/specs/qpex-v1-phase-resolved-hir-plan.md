# QPex phase-resolved typed HIR plan (LISS-0080)

| Field | Value |
|---|---|
| Status | **Slice A Phase 1 Red** (2026-07-29) |
| Authority | WP-0025 E2; ADR 0106 D9; [`qpex-v1-compiler-blueprint.md`](../architecture/qpex-v1-compiler-blueprint.md) §4.1 |
| Depends on | [LISS-0071](../issues/LISS-0071-versioned-conformance-and-differential-oracle.md) **complete**; [LISS-0072](../issues/LISS-0072-lossless-cst-formatter-and-source-versioning.md) **complete** |
| Does not depend on | LISS-0070 (Rust deferred) |
| Unlocks | LISS-0075; LISS-0081 / LISS-0082 |
| Last updated | 2026-07-29 |

This companion freezes the **LISS-0080** design intake. Adjudicator plan
approval selects the dependency rewrite and authorizes **Slice A Phase 1 Red**
only.

## 1. Goals

1. Ship an **immutable phase-resolved typed HIR** on the Python Shipping Kernel.
2. Extract additively from [`typecheck.py`](../../compiler/qpex/typecheck.py)
   (`Ty`, `typed`, `fun_effects`) — **no big-bang IR rewrite**.
3. Record resolved symbols, declaration phase, typed expressions, effects /
   capabilities, and provenance per blueprint §4.1.
4. Keep frontend diagnostics at/before HIR; leave Physics IR and linear
   analysis to later Issues.

## 2. Baseline (today)

| Surface | Today | Gap |
|---|---|---|
| CST / formatter | ✓ LISS-0072 | — |
| Typecheck `Ty` / `typed` / effects | ✓ monolithic in typecheck | immutable HIR view |
| Scientific-scope phase contracts | ✓ LISS-0034 (sealed); body-level open | decl phase on HIR |
| Physics / Quantum IR | not shipped | LISS-0081 / 0082 |
| Linear usage | not shipped | LISS-0075 (after HIR) |

## 3. Architecture boundary

```text
Source/CST (LISS-0072)
  -> AST + TypeChecker (shipping)
  -> immutable HIR view (LISS-0080)   ← this Issue
  -> Physics IR (LISS-0081)          ← out
  -> Quantum Semantic IR (LISS-0082) ← out
```

Rules:

- Additive module (`compiler/qpex/hir.py` or `hir/`); typecheck remains
  authoritative for diagnostics during extraction.
- Slice A: **API / DTO only** — do not rewire evaluator or change program
  semantics.
- Rust HIR mirrors later under LISS-0070; same contracts, not a second
  language.

## 4. MVP (fixed for this Issue)

**In:** immutable HIR DTO; build from TypeChecker; decl phase; effects /
capabilities lift; provenance + construction verifier.

**Out:** Physics IR; Quantum Semantic IR; proof-driven uncomputation;
body-level phase typing (LISS-0076); Rust; big-bang pipeline rewrite.

## 5. Planned slices

| Slice | Scope | Exit |
|---|---|---|
| **A** | Immutable HIR DTO + build API (symbols / `Ty` map); evaluator unwired | **Phase 1 Red** |
| **B** | Declaration phase on HIR decls (existing scope contracts; not 0076) | Red→Green |
| **C** | Effects / capabilities explicit on HIR (`fun_effects` lift) | Red→Green |
| **D** | Provenance + verifier + closeout; linear analysis → LISS-0075 | Red→Green |

### Recommended first Red batch

**Slice A only** — `tests/test_hir_slice_a_red.py`.

Expected Red: missing `compiler.qpex.hir` (or documented build API) so import /
construction assertions fail.

## 6. Non-goals

See Issue non-goals. Do not expand mid-Issue without Adjudicator stop.

## 7. Verification

- Docs-only plan PR; no `compiler/` / `tests/` until Slice A Red.
- After each Green: slice suite + existing typecheck / SV regression when
  typecheck is touched.

## 8. Adjudicator decisions

See [`LISS-0080`](../issues/LISS-0080-phase-resolved-typed-hir.md) Decision
Points (plan). Recommended defaults:

1. Issue + slices A–D as tabled.
2. Depends = LISS-0071 + LISS-0072 only (**drop LISS-0070**).
3. Additive extraction; no big-bang rewrite.
4. Slice A Phase 1 Red only after plan approval; evaluator unwired in A.
