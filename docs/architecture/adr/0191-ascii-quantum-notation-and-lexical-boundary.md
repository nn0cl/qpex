# ADR 0191: ASCII quantum notation and lexical boundary

| Field | Value |
|---|---|
| Status | **Accepted — implementation final-review-ready** |
| Date | 2026-08-04 |
| Scope | Ket, bra, tensor notation, and Unicode input policy |
| Related | ADR 0189, ADR 0190, WP-0094 |

## Context

Staqex should retain compact physics-facing notation without requiring a
Unicode-capable keyboard. The ASCII sequence `||` is already the logical OR
operator, so a lexer that treats every single `|` as the start of a ket can
misread expressions such as:

```text
100 || psi > 10
```

The language also currently accepts Unicode mathematical punctuation and
Unicode identifiers. That is inconsistent with the decision that `psi`,
`phi`, and `rho` are the canonical source spellings.

## Proposed decision

1. Canonical source spellings are ASCII:

   ```text
   |psi>       // ket literal
   <psi|       // bra literal
   a *|* b     // tensor product
   ```

2. ASCII aliases remain available for unambiguous and machine-generated
   source:

   ```text
   ket(psi)
   bra(psi)
   tensor(a, b)
   ```

3. Unicode identifiers and Unicode quantum punctuation are not source syntax.
   This includes `ψ`, `φ`, `ρ`, `⟨`, `⟩`, `⊗`, and `†`.
   Full-width Latin letters, full-width ASCII punctuation, and other Unicode
   mathematical symbols are also not alternate source spellings. They must be
   rejected or handled by an explicit source-normalization tool outside the
   lexer; the lexer must not silently normalize them.

4. Lexical precedence is explicit:

   - `||` is recognized before a single `|`.
   - `|identifier>` is a ket only when the complete ASCII delimiter is
     present.
   - `<identifier|` is a bra only in a primary-expression position and only
     when the delimiters are adjacent; `< psi |` remains ordinary comparison /
     operator syntax.
   - `*|*` is a dedicated ASCII tensor operator, recognized as one token before
     `*` is considered independently.

   Tensor-specific rules are also explicit:

   - `*|*` is a binary, left-associative quantum product. Thus
     `a *|* b *|* c` means `(a *|* b) *|* c` and preserves factor order.
   - `tensor(a, b)` is a semantic alias for the same binary operation, not a
     classical array or coefficient-tensor constructor. Three or more factors
     must be written with explicit nesting; variadic folding is not implicit.
   - Mixing tensor product with ordinary arithmetic multiplication or division
     requires parentheses. This prevents a scalar product from silently
     becoming a tensor factor and makes lowering boundaries reviewable.
   - The exact token `*|*` is required. `* | *` is not a tensor operator and
     must not be normalized into one.

6. Tensor operands are checked at the quantum semantic boundary:

   - Operands must be compatible quantum states or quantum operators; a
     classical collection or numeric coefficient is not accepted merely because
     it is passed to `tensor(...)`.
   - The result retains ordered factor identity and product dimensions. No
     silent dimension coercion or factor reordering is permitted.
   - The infix and alias forms must lower to the same AST/IR operation and have
     identical diagnostics and runtime behavior.

7. When an ASCII notation is ambiguous, the compiler emits a diagnostic that
   points to `ket(...)`, `bra(...)`, or `tensor(...)`; it must not guess.

8. Formatter and documentation may render Unicode chalk as presentation, but
   formatted source must remain ASCII-reproducible.

## Consequences

Positive:

- International users can write all quantum expressions with ordinary
  keyboards.
- Conditions such as `100 == a || 10 == b` remain ordinary Boolean syntax.
- Physicist-facing short notation is retained where delimiters make its
  meaning deterministic.

Costs:

- `<psi|` needs a dedicated ASCII bra lexing rule because `<` is also a
  comparison operator.
- Existing Unicode notation tests and grammar productions must be migrated.
- The formatter becomes responsible for any optional Unicode presentation.
- Tensor alias lowering and its arity/grouping boundaries are implemented;
  focused acceptance evidence is recorded in WP-0094. Final review remains
  required before completion status is promoted.

## Non-goals

- Changing the meaning of `mix`, `controlled`, `project`, or `measure`.
- Adding implicit multiplication or a new Boolean expression model.
- Accepting full-width Latin characters as ASCII identifiers.

## Gate

This ADR is accepted as the source-language boundary. Implementation evidence
and the remaining final-review gate are recorded in WP-0094; no compatibility
fallback or alternate Unicode source semantics are implied.
