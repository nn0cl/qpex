# LISS-0331: `FermionOperator`/etc. RHS with a leading scalar coefficient fails to parse

## Metadata

- Local issue ID: LISS-0331
- Status/phase: **proposed** / `phase-0-design` (2026-08-05) — Plan
  approval granted directly by the Adjudicator in response to this
  finding ("パースエラーは言語の不備を見つけたということだと思うので
  修正をして")
- Type: Feature Path (Kernel — `compiler/staqex/parser.py::_type_first_bind`
  only; no AST/typecheck/evaluator change)
- Priority: P2
- Initial planning size: `S`
- Owner / agent: Claude Code
- Program: found during
  [WP-0095](../work-plans/WP-0095-real-hbar-hamiltonian-dynamics.md) work
  unit 2 design intake (`A03_h2_vqe` migration); this Issue fixes an
  unrelated, pre-existing parser bug the migration surfaced, not part of
  WP-0095's own scope
- Depends on: none
- Branch: `feature/liss-0331-second-quantized-leading-coefficient`
- GitHub Issue / PR: none yet

## Intent

`FermionOperator<Orbitals> H = 1.0 * create[0] * annihilate[0]` fails to
parse (`PARSE_ERROR: function result expression must be the final item in
a block`), while `create[0] * annihilate[0] * 1.0` and `create[0] * 1.0 *
annihilate[0]` (coefficient anywhere except first) both parse and compile
cleanly.

Root cause, confirmed by direct code reading:
`parser.py::_type_first_bind` (line ~1886) decides whether a
`FermionOperator`/`BosonOperator`/`SpinOperator`/`QubitOperator` binding's
RHS is parsed via the Operator-DSL grammar (`_op_expression()`, which
understands `create[i]`/`annihilate[i]` second-quantized atoms) or the
ordinary expression grammar (`_expression()`, which does not) based
**only** on whether the very first token is `IDENT` immediately followed
by `[`:

```python
if (
    self._peek().kind == TokenKind.IDENT
    and self._peek_at_kind(1) == TokenKind.LBRACKET
):
    expr = self._op_expression()
else:
    expr = self._expression()
```

A leading scalar coefficient (`1.0 * create[0] * ...`) makes the first
token a `FLOAT`, not `IDENT`, so this check silently routes the whole
fermionic expression through the wrong grammar, producing a confusing,
unrelated-looking parse error instead of a real second-quantized
expression.

## Fix

**Scope widened during design intake**: a named `Float`-variable leading
coefficient (`Float e0 = 1.0` then `FermionOperator<Orbitals> H = e0 *
create[0] * annihilate[0]`) was verified to fail identically
(`e0` is `IDENT` but followed by `STAR`, not `LBRACKET`, so the original
single-token check also misses it) — this is the more realistic pattern
for physically-real, named-scalar coefficients (WP-0095's own migration
need), so the fix generalizes to a small bounded forward scan rather than
only the literal-numeric case:

```python
def _second_quantized_rhs_is_op_dsl(self) -> bool:
    """FermionOperator/BosonOperator/SpinOperator/QubitOperator RHS:
    detect a second-quantized OpDSL expression (`create[i]`/`annihilate[i]`
    atoms) even behind a chain of leading scalar coefficients
    (`1.0 * create[0]...`, `e0 * create[0]...`, `2.0 * e0 * create[0]...`),
    not just when the atom is the very first token."""
    offset = 0
    while offset <= 8:  # bounded: a handful of chained coefficients at most
        kind = self._peek_at_kind(offset)
        next_kind = self._peek_at_kind(offset + 1)
        if kind == TokenKind.IDENT and next_kind == TokenKind.LBRACKET:
            return True
        if kind not in (TokenKind.INT, TokenKind.FLOAT, TokenKind.IDENT):
            return False
        if next_kind != TokenKind.STAR:
            return False
        offset += 2
    return False
```

Used in place of the inline condition at `_type_first_bind`'s
`FermionOperator`/etc. branch. Verified this does not regress the
`QubitOperator<Qubits> H = map(H_fermion, JordanWigner)` binding form
(the second token after `map` is `LPAREN`, not `STAR`/`LBRACKET`, so the
scan correctly falls through to `False` / ordinary `_expression()` on the
very first iteration).

## Explicitly out of scope

- Any change to `_op_expression`/`_op_primary`'s own internal handling of
  multiplication once dispatched correctly — only the FermionOperator/etc.
  binding's up-front grammar-selection heuristic changes.
- Coefficients that are themselves compound expressions (e.g. `(e0 + e1)
  * create[0] * ...`) — not needed for WP-0095's migration use case, not
  covered by the bounded scan above.

## Acceptance reference

```gherkin
Feature: FermionOperator RHS with a leading scalar coefficient

  Scenario: a leading numeric literal coefficient parses via the OpDSL grammar
    Given FermionOperator<Orbitals> H = 1.0 * create[0] * annihilate[0]
    When the program is compiled
    Then it compiles without a PARSE_ERROR

  Scenario: a leading named Float coefficient parses via the OpDSL grammar
    Given Float e0 = 1.0
      And FermionOperator<Orbitals> H = e0 * create[0] * annihilate[0]
    When the program is compiled
    Then it compiles without a PARSE_ERROR

  Scenario: existing non-leading-coefficient forms are unaffected
    Given FermionOperator<Orbitals> H = create[0] * annihilate[0] * 1.0
    When the program is compiled
    Then it compiles without a PARSE_ERROR (regression, already passing)

  Scenario: the QubitOperator map(...) binding form is unaffected
    Given QubitOperator<Qubits> H = map(H_fermion, JordanWigner)
    When the program is compiled
    Then it compiles without a PARSE_ERROR (regression, already passing)
```

## AI planning record (size S)

- Status: proposed, pre-Phase-1
- Authoring environment: Claude Code (Sonnet 5), this session
- Date: 2026-08-05
- Size: `S` — one lookahead condition in one function, one file.
- Route: direct implementation by this session.
- Confidence: high — root cause directly confirmed by reading the exact
  dispatch condition and reproducing the failure/success pattern across
  three coefficient-position variants before drafting this Issue.

## Exit criteria

- [ ] Phase 1 Red: acceptance test for the leading-coefficient scenario
      exists and fails for the documented reason.
- [ ] Phase 2 Green: minimal fix makes it pass without editing the test,
      without changing the two already-working coefficient-position
      forms' behavior.
- [ ] Phase 3 Refactor: no behavior change; reviewer empathy summary.
- [ ] Full regression: `pytest tests/ -q`, `python3
      tests/spec_verification/run_all.py`, `git diff --check`.

## Non-goals

- General multi-term/named-variable coefficient forward-scanning beyond
  the single-leading-numeric-literal case.
