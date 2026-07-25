# LISS-0051: Operator Pauli-atom-call parsing gap

## Metadata

- Local issue ID: LISS-0051
- GitHub issue: none
- Status: proposed
- Phase: phase-0-design
- Type: bug / parser grammar gap
- Priority: P1
- Initial planning size: S
- Current planning size: S
- Reclassification reason: n/a
- Owner/agent: TBD
- Related branch: `bug/liss-0051-operator-pauli-atom-call-parse`

## Summary

`parser.py`'s `_type_first_bind` decides whether an `Operator`-typed bind's
right-hand side is parsed by the dedicated Operator-polynomial grammar
(`_op_expression` → `OpBin`/`OpPauli`/`OpLit`, ...) or by the generic
expression grammar (`_expression` → `BinOp`/`Call`/`Var`, ...). The decision
looks only one token ahead: "identifier immediately followed by `(`" is
treated as an ordinary factory function call (supporting the shipped
`fn make_coin() -> Operator { ... }` / `Operator k = make_coin()` pattern).
This heuristic does not exempt the Operator-DSL's own reserved atom names
(`I`, `X`, `Y`, `Z`, `hop`), so a site-qualified Pauli atom such as `Z(0)` —
or any product/sum built from them, since the whole expression falls to the
generic grammar once the first token is misclassified — is parsed as a
plain function call/`BinOp` instead of `OpPauli`/`OpBin`.

Found 2026-07-25 while investigating LISS-0011's "general operator algebra
remains deferred" scope for Lindblad; this defect is broader than Lindblad
and independent of it — it affects the SV evaluator's `evolve` path and the
QASM/Trotter path equally, since both consume whatever AST node type
`self.operators`/`op_env` actually stores.

## Reproduction

```qpex
package t
pub fn main() -> Unit {
    Operator H = Z(0) * Z(1)
    state a = |+>
    state b = |0>
    state (a, b) = evolve (a, b) under H for 0.1
        using Suzuki(order = 2, steps = 4)
    measure a
}
```

- `python3 -m compiler.qpex check <file>` reports `ok` (expected: `check`
  only lints Forbidden/Retired/Early-Collapse vocabulary).
- `python3 -m compiler.qpex run <file>` exits `1`:
  `RUNTIME_ERROR: cannot compile sparse Pauli for BinOp`.
- `python3 -m compiler.qpex emit-qasm <file>` exits `1`:
  `QASM_TROTTER_UNSUPPORTED_H: cannot compile sparse Pauli for BinOp`.
- Neither failure is silent (both are non-zero exit with a diagnostic), so
  this is not the LISS-0049/LISS-0050 class of defect — but the message
  leaks an internal Python type name (`BinOp`) instead of explaining the
  actual problem, and the underlying constraint ("write a leading numeric
  coefficient or the Operator parses generically and breaks") is not
  documented anywhere a physicist would find it.
- Confirmed independently via direct AST inspection:

  | Source | Parses as |
  |---|---|
  | `Operator H = Z(0) * Z(1)` | `BinOp` (generic — **wrong**) |
  | `Operator H = Z(0)` | `Call` (generic — **wrong**) |
  | `Operator H = hop(0, 1)` | `Call` (generic — **wrong**) |
  | `Operator H = 1.0 * (Z(0) * Z(1))` | `OpBin` (Operator DSL — correct, by accident of the leading literal) |
  | `Operator H = Z` | `OpPauli` (Operator DSL — correct; no `(`, so the ambiguity does not trigger) |

## Root cause and fix

In `compiler/qpex/parser.py`'s `_type_first_bind`:

```python
if ty.name == "Operator":
    ...
    if (
        self._peek().kind == TokenKind.IDENT
        and self._peek().lexeme not in {"sum", "product"}
        and self._peek_at_kind(1) == TokenKind.LPAREN
    ):
        expr = self._expression()
    else:
        expr = self._op_expression()
```

The one-token-lookahead heuristic ("`IDENT` then `(`" → ordinary call) does
not exclude the Operator-DSL's own reserved atom names. `_op_primary`
(the dedicated parser) already knows how to parse `I`/`X`/`Y`/`Z` with an
optional parenthesized site and `hop(i, j)` — but the caller never reaches
it for these names because the factory-call branch wins first.

Fix: exclude the reserved Operator-DSL atom names from the factory-call
heuristic, alongside the existing `sum`/`product` exclusion:

```python
_OPERATOR_DSL_RESERVED_ATOMS = {"I", "X", "Y", "Z", "hop"}

if (
    self._peek().kind == TokenKind.IDENT
    and self._peek().lexeme not in {"sum", "product"}
    and self._peek().lexeme not in _OPERATOR_DSL_RESERVED_ATOMS
    and self._peek_at_kind(1) == TokenKind.LPAREN
):
    expr = self._expression()
else:
    expr = self._op_expression()
```

This is the same shape of fix as the existing `{"sum", "product"}`
exclusion already in the code — it is not a new mechanism, just a more
complete list of names the Operator-DSL parser itself already reserves.

## Acceptance notes

- [ ] `Operator H = Z(0) * Z(1)` parses to `OpBin(op='*', lhs=OpPauli('Z',
      0), rhs=OpPauli('Z', 1))`, not a generic `BinOp`.
- [ ] `Operator H = Z(0)` parses to `OpPauli(kind='Z', site=0)`, not a
      generic `Call`.
- [ ] `Operator H = hop(0, 1)` parses to `OpHop(i=0, j=1)`, not a generic
      `Call`.
- [ ] The reproduction program above runs on the SV simulator and emits
      QASM successfully (no `RUNTIME_ERROR`/`QASM_TROTTER_UNSUPPORTED_H`).
- [ ] `Operator k = make_coin()` (an existing shipped factory-call pattern,
      name not in the reserved-atom set) continues to parse and run exactly
      as today — no regression to the factory-call feature this heuristic
      exists for.
- [ ] No other Operator-DSL reserved name (`N`, `Q`, `P`, `sum`, `product`)
      needs adding to the exclusion set: `N`/`Q`/`P` never consume a
      parenthesized argument list in `_op_primary`, so they cannot trigger
      this specific ambiguity; `sum`/`product` are already excluded.

## Dependencies

- Parent: none
- Depends on: none
- Related: [LISS-0011](LISS-0011-density-matrix-lindblad.md) (found during
  its Architecture Path review — independent defect, not blocking or
  blocked by LISS-0011's own remaining scope), LISS-0048 (same "found during
  unrelated review, split out, no ADR needed for a single clear fix"
  pattern)
- Blocks: nothing known; affects any program writing a bare (no leading
  coefficient) product/sum of site-qualified Pauli atoms or `hop(i, j)`,
  in both the SV and QASM paths

## Adjudicator Decision Points

- [ ] Approve the fix (exclude `{"I", "X", "Y", "Z", "hop"}` from the
      factory-call heuristic) before Phase 1 Red.
- [ ] Confirm no ADR is needed — this is a single, unambiguous grammar fix
      restoring the parser's own stated intent ("literal Hamiltonian
      expressions retain the dedicated operator parser"), not a design
      choice among alternatives.

## Context

- Included: `compiler/qpex/parser.py` (`_type_first_bind`, `_op_primary`),
  `compiler/qpex/runtime/hamiltonian.py` (crash site, for understanding
  only), `compiler/qpex/backend/qasm/trotter.py` (crash site, for
  understanding only).
- Omitted: LISS-0011's own remaining scope (Lindblad's hardcoded
  `n_qubits=1` in `_resolve_lindblad_hamiltonian`/`_compile_one_qubit_operator`,
  which is a separate, narrower limitation on top of this one — fixing this
  parser gap is a prerequisite for meaningfully testing that limitation with
  a real multi-qubit Hamiltonian, but is not itself LISS-0011's scope).
- Assumption: the correct fix is parser-level (exclude reserved atom names
  from the factory-call heuristic), not a typecheck-time or runtime
  workaround — the AST should be structurally correct (`OpBin`/`OpPauli`)
  as soon as it is parsed, matching every other Operator expression.

## Verification

- Phase 1 Red: tests reproducing today's mis-parse (via direct AST
  inspection of `compile_source(...).unit`) and the resulting `run`/
  `emit-qasm` failures for the reproduction program.
- Phase 2 Green: the same tests assert the correct `OpBin`/`OpPauli`/`OpHop`
  AST shape and that `run`/`emit-qasm` succeed.
- Existing SV/QASM/Trotter/Suzuki regressions, the `make_coin()`-style
  factory-call tests, and full spec verification (165/165) must remain
  green.

## Work Notes

- 2026-07-25: Issue opened during LISS-0011 Architecture Path
  investigation. Root cause read and reproduced via direct AST inspection
  and CLI probes (`run`/`emit-qasm` both fail honestly, non-silently, but
  with an internal-type-leaking message). No code changed.
