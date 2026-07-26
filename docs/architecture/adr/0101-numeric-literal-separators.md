# ADR 0101: Underscore separators in numeric literals

## Status

**Proposed design** (2026-07-26). This ADR does not authorize lexer
implementation or a Phase 1 Red test change.

## Context

Resource profiles and scientific examples contain values such as shot counts,
term budgets, register sizes, and tolerances. Long digit strings are easy to
misread when written without grouping:

```qpex
shots = 1000000
```

The language should improve source readability without introducing a new
numeric type, changing the `f64` Kernel boundary, or making separators part of
the numeric value.

## Decisions proposed for review

### D1 — Accept separators between digits

QPex numeric literals may contain `_` only between two digits in the same
numeric component:

```qpex
1_000
1_000_000
1_000.25
1.0e-4
1.0e-04
```

The lexer removes separators before numeric conversion. The source lexeme
remains available for diagnostics and provenance.

### D2 — Apply the rule to integer, fractional, and exponent digits

Separators are allowed within the integer digits, fractional digits, and
exponent digits. They are not allowed next to punctuation or a sign:

```qpex
1_000.25
1.000_25
1.0e1_0
```

The sign in an exponent is a separator boundary, not a digit component.

### D3 — Reject malformed placement explicitly

The following forms are invalid and produce a lexer diagnostic rather than a
different tokenization or a silently repaired value:

```qpex
_100
100_
1__000
1_.0
1._0
1e_4
1e+_4
```

The diagnostic should identify the literal span and explain that separators
must occur between digits. No whitespace, sign, decimal point, or exponent
marker may be silently absorbed.

### D4 — Preserve existing numeric meaning

Separators are lexical sugar only:

```text
1_000 == 1000
1_000.25 == 1000.25
```

They do not alter unit suffix handling, dimension analysis, constant folding,
rounding, tolerance policy, or the existing `f64` conversion boundary defined
by ADR 0076 and ADR 0097.

### D5 — Keep the feature independent of future numeric modes

The rule applies to the current `Int`/`Float` literal surface. A future exact,
symbolic, or arbitrary-precision mode must define its own accepted literal
grammar explicitly and may not silently inherit this rule if doing so changes
its semantics.

## Consequences

- Large scientific values become easier to audit visually.
- Lexer validation becomes stricter at malformed separator positions, which is
  preferable to ambiguous tokenization.
- Parser, type checker, unit suffixes, and runtime numeric storage need no new
  domain type.
- The original lexeme can be retained in diagnostics without making source
  formatting part of runtime equality.

## Open decisions

- Whether hexadecimal, binary, or octal literals will ever be introduced;
  this slice covers only the existing decimal grammar.
- The stable diagnostic code/name for malformed separator placement.
- Whether formatter support is part of this LISS or a later tooling slice.
- Whether source-level numeric provenance must be exposed in QPU IR metadata.

## Non-goals

- No exact arithmetic or numeric tower selection.
- No change to unit suffixes or dimension inference.
- No change to `Param<T>`, `Host<T>`, `State<T>`, or QPU lowering.
- No automatic insertion of separators by the compiler.

## Related documents

- [ADR 0076](0076-numeric-representation-policy.md)
- [ADR 0097](0097-numeric-representation-horizon.md)
- [LISS-0018](../../issues/LISS-0018-numerical-representation.md)
- [LISS-0061](../../issues/LISS-0061-numeric-literal-separators.md)
