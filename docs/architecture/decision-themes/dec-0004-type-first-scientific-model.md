# DEC-0004: Type-First scientific model

## Status

**Draft — source review required**

## Current rules

- Scientific quantities are Type-First: dimensions and units are part of the
  type/semantic contract, not comments attached after evaluation.
- Dimensionally invalid arithmetic is rejected before execution.
- Product carriers expose their component types and preserve correlation;
  tracing out is explicit.
- Numeric precision, continuous-domain discretization, rational literals, and
  unit conversion remain explicit boundaries rather than implicit coercions.
- Linear obligations follow the carrier type and transforming calls, not a
  cosmetic binding keyword.

See [type system](../staqex-type-system.md),
[dimensional types](../staqex-dimensional-types.md), and the
[language specification](../../specs/staqex-language-specification.md).

## Source boundary

- Source tag: `docs/pre-canonicalization-2026-08-03`
- Source commit: `8663ba72295964069ac275b93c350e762a0844d8`
- Source ADRs: ADR 0037, ADR 0074, ADR 0076, ADR 0090, ADR 0097, ADR 0101, ADR 0116, ADR 0118, ADR 0121, ADR 0124, ADR 0125, ADR 0128, ADR 0129, ADR 0130, ADR 0131, ADR 0132, ADR 0133, ADR 0134, ADR 0135, ADR 0136, ADR 0144, ADR 0145, ADR 0146, ADR 0147, ADR 0148, ADR 0149, ADR 0150, ADR 0151, ADR 0152, ADR 0153, ADR 0154, ADR 0155, ADR 0156, ADR 0160, ADR 0174, ADR 0180, ADR 0181, ADR 0185, ADR 0186
- Recovery command: `git show <source_tag>:<source_path>`

## Acceptance gate

The source set must be reviewed for duplicate, superseded, unique, and unresolved decisions before this document is promoted to the current normative reading surface. Existing ADRs remain authoritative until that review is accepted.
