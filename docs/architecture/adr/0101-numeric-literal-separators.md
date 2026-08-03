# ADR 0101: Underscore separators in numeric literals

## Status

**Accepted / Phase 3 Refactor complete** (2026-07-27). The separator placement
rule and lexer implementation are accepted; formatter support and QPU
provenance remain deferred.

## Context

Resource profiles and scientific examples contain values such as shot counts,
term budgets, register sizes, and tolerances. Long digit strings are easy to
misread when written without grouping:

```staqex
shots = 1000000
```

The language should improve source readability without introducing a new
numeric type, changing the `f64` Kernel boundary, or making separators part of
the numeric value.

## Decisions

### D1 — Use Java-compatible placement for decimal literals

Staqex follows Java's placement rule: `_` is allowed only between two digits in
the same numeric component. This is not a fixed three-digit grouping rule.
The first slice applies to the existing decimal `Int` and `Float` forms:

```staqex
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

```staqex
1_000.25
1.000_25
1.0e1_0
```

The sign in an exponent is a separator boundary, not a digit component.

### D3 — Reject malformed placement explicitly

The following digit-started forms are invalid and produce a lexer diagnostic
rather than a different tokenization or a silently repaired value:

```staqex
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

### D6 — Do not import Java's non-decimal literal surface

Java also permits separators in hexadecimal, binary, and octal literals. Staqex
does not currently have those literal forms, so this ADR does not introduce
them. Any future non-decimal form requires an explicit grammar decision.

### D7 — Preserve the existing private-identifier boundary

An underscore at the beginning of a lexeme remains part of the existing
private-identifier syntax. Therefore `_100` is lexed as an identifier, not as
a malformed numeric literal. Numeric separator diagnostics apply only after a
digit has established a numeric literal.

## Deferred decisions

- Formatter support as a later tooling slice.
- Whether source-level numeric provenance must be exposed in QPU IR metadata.

The malformed-placement diagnostic for this slice is fixed as
`NUMERIC_LITERAL_SEPARATOR_ERROR`.

## Non-goals

- No exact arithmetic or numeric tower selection.
- No change to unit suffixes or dimension inference.
- No change to `Param<T>`, `Host<T>`, `State<T>`, or QPU lowering.
- No automatic insertion of separators by the compiler.

## Related documents

- [ADR 0076](0076-numeric-representation-policy.md)
- [ADR 0097](0097-numeric-representation-horizon.md)
- [LISS-0018](../documentation-compression-map.md)
- [LISS-0061](../documentation-compression-map.md)
