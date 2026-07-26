# LISS-0061: Numeric literal separators

## Metadata

- Local issue ID: LISS-0061
- GitHub issue: none
- Status: proposed
- Phase: phase-0 design intake
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
When a separator occurs at the start/end, twice consecutively, or next to
     a decimal point, exponent marker, or exponent sign
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

- [ ] Accept the proposed separator grammar.
- [ ] Select the malformed-separator diagnostic code.
- [ ] Approve Phase 1 Red lexer tests.
- [ ] Confirm whether formatter support is excluded from this slice.

## Design boundary

This issue is documentation/design only until the decision points above are
accepted. Implementation must not begin from the proposed examples alone.
