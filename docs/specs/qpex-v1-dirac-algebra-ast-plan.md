# QPex named Dirac notation and algebra AST plan (LISS-0073)

| Field | Value |
|---|---|
| Status | **Slice G Red ready for review** (2026-07-29) |
| Authority | WP-0025 E1; ADR 0106 D5; ADR 0087 (function-shaped core); [`qpex-v1-compiler-blueprint.md`](../architecture/qpex-v1-compiler-blueprint.md) §3.1–3.2; [`qpex-v1-language-north-star.md`](qpex-v1-language-north-star.md) §3.1 / §6.1 |
| Depends on | LISS-0069 **complete**; LISS-0072 **complete**; LISS-0031 **reviewed** |
| Last updated | 2026-07-29 |

This companion freezes the **LISS-0073** design intake. Adjudicator plan
approval selects the recommended direction and authorizes **Slice A Phase 1
Red** only.

## 1. Goals

1. **Punctuation surface** — parse bras, inner products, matrix elements,
   outer / projector forms, expression-side adjoints, and (if approved)
   commutator / anticommutator brackets.
2. **One typed algebra model** — punctuation lowers to the same contracts as
   LISS-0031 function forms; no macro or string semantics.
3. **Hard errors** — domain mismatches and `|>` / `⟩` / list-brace collisions
   fail closed with named diagnostics.
4. **Dual-accept** — function-shaped forms remain valid (M-P06 deprecate gate
   deferred unless Adjudicator overrides).
5. **Spec truth** — EBNF / language-spec precedence updated with each accepted
   form (or final sync in Slice G).

## 2. Current baseline (evidence)

| Surface | Lex | Parse | Typed today | Gap |
|---|---|---|---|---|
| Ket `\|label⟩` | ✓ | ✓ | `KetLit` | Named labels already lexed post-LISS-0069 |
| Bra `⟨label\|` | ✓ | ✗ | — | `_primary` ignores `BRA` |
| Tensor `⊗` / `*|*` | ✓ | ✓ | `TensorExpr` | State vs operator tensor model open |
| `†` postfix | ✓ | Operator DSL only | `OpCall("adjoint")` | Expression-side asymmetry |
| `adjoint` / `inner` / … | n/a | ✓ `Call` | `typecheck._check_algebra_call` | Semantic core (ADR 0087) |
| `⟨φ\|ψ⟩` / `⟨φ\|A\|ψ⟩` | partial | ✗ | function forms only | Juxtaposition undefined |
| `\|ψ⟩⟨φ\|` | partial | ✗ | `outer` / `projector` calls; `OpHop` site-only | General outer sugar missing |
| `[A,B]` / `{A,B}` | n/a | ✗ | function forms only | Collides with `ListExpr` / braces |

Authoritative deferrals:

- LISS-0069 / unicode-math-source: bra–ket matrix-element desugar → **A.1 / LISS-0073**
- LISS-0072 non-goals: bra / matrix-element desugar out
- ADR 0087: Unicode punctuation deferred; function forms normative until this Issue

## 3. Architecture boundary

```text
source
  → lexer (existing BRA/KET/DAGGER/TENSOR)
  → parser (new juxtaposition / postfix paths)
  → desugar / AST nodes
  → typecheck algebra contracts (LISS-0031)
  → existing Joint / Operator pipeline
```

Rules:

- **No new runtime evaluator** for algebra; reuse existing Call / OpCall /
  State / Operator evaluation paths.
- **No Physics IR** work (LISS-0081).
- Formatter (`qpex format`) may later emit punctuation or function forms;
  Slice G documents emit policy without requiring a full pretty rewrite.
- CST trivia from LISS-0072 remains presentation-only; algebra meaning lives
  in AST + typecheck.

## 4. Recommended formula → core map

| Punctuation (target) | Lowers to (semantic core) |
|---|---|
| `⟨ψ\|` | `BraLit` → typechecks as bra / `adjoint(ket)` contract |
| `⟨φ\|ψ⟩` | `inner(φ, ψ)` |
| `⟨φ\|A\|ψ⟩` | matrix element ≡ `inner(φ, A(ψ))` or approved equivalent typed form |
| `\|ψ⟩⟨φ\|` | `outer(ψ, φ)` |
| `\|ψ⟩⟨ψ\|` | `projector(ψ)` |
| `A†` (expr + Operator DSL) | `adjoint(A)` / `OpCall("adjoint", …)` |
| `ψ ⊗ φ` | existing `TensorExpr` |
| `[A, B]` (if approved) | `commutator(A, B)` |
| `{A, B}` (if approved) | `anticommutator(A, B)` |

Exact matrix-element lowering identity is fixed in Slice C Red assertions
after plan approval (must match typecheck + SV oracles).

## 5. Planned slices

| Slice | Scope | Exit |
|---|---|---|
| **A** | Wire `BRA` in `_primary`; introduce `BraLit` (recommended); EBNF `primary` includes `bra_lit`; alone-bra typechecks | Bra parses; no juxtaposition yet |
| **B** | `⟨φ\|ψ⟩` → `inner`; pipeline / close-bracket collision tests | Inner punctuation round-trips to algebra contracts |
| **C** | `⟨φ\|A\|ψ⟩` matrix element; domain mismatch hard errors | Matrix element goldens + diagnostics |
| **D** | `\|ψ⟩⟨φ\|` / `\|ψ⟩⟨ψ\|` → `outer` / `projector`; document `OpHop` | Outer / projector sugar |
| **E** | Expression-side `†` parity with Operator DSL | Asymmetry closed |
| **F** | `[A,B]` / `{A,B}` **only after** Adjudicator ambiguity decision | Bracket sugar or explicit deferral note |
| **G** | Freeze typed algebra model + formula table; EBNF/spec sync; optional formatter emit note | Issue acceptance notes satisfied |

### Recommended first Red batch

**Slice A only** after initial plan approval (done). Later slices each need
their own plan / Red gate.

### Slice B plan (complete)

Shipped: single-bar `⟨φ|ψ⟩` → `Call(inner, [BraLit, KetLit])` via lexer ket
half + `_bra_or_inner`; EBNF `bra_ket_inner`; alone bra preserved.

### Slice C plan (complete)

Shipped: `⟨φ|A|ψ⟩` → `Call(inner, [BraLit, Call(A, [KetLit])])`; State middle
→ `OPERATOR_ALGEBRA_TYPE_ERROR`; EBNF `bra_op_ket`.

### Slice D plan (complete)

Shipped: `|ψ⟩⟨φ|` → `Call(outer, [KetLit, BraLit])`; matching labels →
`Call(projector, [KetLit])`; `Operator` bind KET/BRA → `_expression`;
EBNF `ket_bra_outer` + OpHop note. Merged PR #99.

### Slice E plan (complete)

Shipped: expression postfix `†` in `_call` → `Call(adjoint, [expr])`;
EBNF `dagger_suffix`; OpDSL `_op_postfix` unchanged; dual-accept with
`adjoint(…)`.

### Slice F plan (complete)

Shipped: Operator-context `[A, B]` → `Call(commutator, …)`; `{A, B}` →
`Call(anticommutator, …)` (expr + Operator bind + OpDSL primary); expression
`[…]` remains `ListExpr`; EBNF `bracket_commutator` / `brace_anticommutator`.

### Slice G plan (proposed)

**Scope:** Close LISS-0073 by freezing the typed algebra model and proving the
§4 formula→AST table against the shipping Kernel. No new punctuation.

**Recommended deliverables:**
1. Update §4 table rows for `[A,B]` / `{A,B}` to shipped rules (Operator-context
   commutator; braces → anticommutator; expr `[…]` stays `ListExpr`).
2. Proof suite `tests/test_dirac_slice_g_red.py` — one assertion family per
   table row (AST shape + dual-accept with function form where applicable);
   may import/call A–F helpers or inline minimal sources.
3. Formatter emit policy paragraph: M-P06 dual-accept retained; format/migrator
   emit of punctuation vs function form is **policy-only** (no full pretty
   rewrite in this Issue).
4. On Green: mark Issue acceptance notes satisfied; status → **complete**.

**Out of Slice G:** new sugar; Physics IR; NFC; deprecating function forms.

**Red suite:** `tests/test_dirac_slice_g_red.py` — expected Red until formula
table / proof harness / emit-policy docs land in Green.

### Slice F default recommendation (historical)

Historical deferral note: bracket sugar waited until A–E green. Superseded by
the complete Slice F section above.

## 6. Non-goals

- LISS-0081 Physics IR
- NFC on-read, M-P01, M-P05
- Deprecating function-shaped forms inside this Issue (unless overridden)
- Non-square operator codomains
- Rust frontend

## 7. ADR / supersession note

ADR 0087 remains authoritative for **typed contracts**. This Issue **extends**
the deferred Unicode / punctuation sugar clause; it does not replace the
function-shaped core. If first-class algebra nodes replace `Call` wrappers,
they must preserve Span provenance and identical typecheck results — capture
as an ADR amendment only if the Adjudicator requires it during Slice G.

## 8. Verification

- Docs-only plan PR; no `compiler/` / `tests/` until Slice A Red.
- After each Green: standalone slice tests + SV gate.
- Formula map in §4 must match Red assertions exactly.

## 9. Adjudicator decisions (copy of Issue)

See [`LISS-0073`](../issues/LISS-0073-named-dirac-notation-and-algebra-ast.md)
Decision Points (plan). Recommended defaults:

1. Slices A–G as tabled; F deferred until A–E green.
2. First-class `BraLit` + typecheck lowering.
3. Juxtaposition matrix-element parse (no composite token).
4. Expression-side `†` in Slice E.
5. M-P06 dual-accept retained.
6. Reuse `OPERATOR_ALGEBRA_TYPE_ERROR` where applicable.
7. Authorize **Slice A Phase 1 Red** only after plan approval.
