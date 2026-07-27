# LISS-0061: Numeric literal separators

## Metadata

- Local issue ID: LISS-0061
- GitHub issue: none
- Status: Phase 3 Refactor complete
- Phase: phase-3 refactor complete
- Type: lexer surface
- Priority: P2
- Initial planning size: S
- Current planning size: TBD
- Owner/agent: TBD
- Related branch: `codex/liss-0061-numeric-literal-separators`

## Summary

Allow digit separators in existing decimal integer and floating-point
literals so scientific and operational values remain readable without
introducing a new numeric type or changing runtime numeric semantics.

## Acceptance scenarios

### Accepted forms

```gherkin
Given the decimal numeric literal grammar
When the source contains 1_000, 1_000.25, or 1.0e1_0
Then the lexer emits the existing INT or FLOAT token
And numeric conversion observes the separator-free value
And the original lexeme remains available for diagnostics/provenance
```

### Rejected forms

```gherkin
Given the decimal numeric literal grammar
When a separator occurs at the end, twice consecutively, or next to a decimal
     point, exponent marker, or exponent sign in a digit-started literal
Then lexing fails with an explicit malformed-separator diagnostic
And the compiler does not repair or reinterpret the literal
```

## Scope

- Lexer validation and token payload handling for decimal `Int`/`Float` forms.
- Existing parser, type checker, unit suffix, and numeric conversion paths.
- Diagnostics and source-span preservation.

## Non-goals

- Hexadecimal, binary, or octal literals.
- Exact, symbolic, or arbitrary-precision arithmetic.
- Formatter insertion of separators.
- Changes to `f64` rounding, tolerances, dimensions, or QPU lowering.

## Dependencies

- [ADR 0076](../architecture/adr/0076-numeric-representation-policy.md)
- [ADR 0097](../architecture/adr/0097-numeric-representation-horizon.md)
- [ADR 0101](../architecture/adr/0101-numeric-literal-separators.md)

## Adjudicator decision points

- [x] Accept the proposed separator grammar using Java-compatible placement:
  separators are allowed only between digits in the same decimal component.
- [x] Select `NUMERIC_LITERAL_SEPARATOR_ERROR` for malformed placement.
- [x] Approve Phase 1 Red lexer tests.
- [x] Confirm formatter support is excluded from this slice.
- [x] Preserve leading-underscore private identifiers; `_100` is not a
  numeric-separator diagnostic.

## Design boundary

The separator placement and diagnostic decisions are accepted. The lexer now
implements the accepted decimal separator contract while preserving the
existing leading-underscore private-identifier boundary.

## Phase 1 Red record

- Added lexer tests for valid decimal integer, fraction, and exponent
  separators, including lexeme preservation.
- Added negative tests for separator placement at boundaries, punctuation,
  signs, and repeated separators.

## Phase 2 Green record

- The lexer consumes separators within integer, fraction, and exponent digit
  components while preserving the source lexeme.
- Numeric conversion removes separators only for the runtime numeric payload.
- Malformed digit-started placements emit
  `NUMERIC_LITERAL_SEPARATOR_ERROR` without silent repair.

## Phase 3 Refactor record

- Consolidated separator diagnostics in the lexer and clarified numeric
  component state names without changing tokenization or diagnostics.
- Reviewer empathy: numeric scanning now separates component parsing,
  malformed-separator reporting, and numeric conversion responsibilities.
