# ADR 0154: Reject mixed-unit `+` / `-` (no automatic rescale)

## Status

**Superseded** (2026-07-31) by [ADR 0155](0155-mixed-unit-canonical-promote.md).
Was Accepted under WP-0060 / LISS-0186; reject-for-all-mixed withdrawn for
shared-canonical families.

## Decisions (historical)

1. Track an optional **unit suffix** on `Ty` for unit literals, successful
   `expr to unit`, and Type-First binds that preserve that suffix.
2. For `+`, `-`, and relational ops: if **both** operands have a known unit
   and the suffixes differ → `UNIT_MIXED_ARITHMETIC_ERROR`.
3. Same-unit operands remain allowed; magnitudes stay raw (no silent rescale).
4. Explicit `expr to unit` remains the only conversion path (ADR 0124).
5. **No** automatic rescale / canonical promotion in arithmetic.

## Non-goals

Implicit conversion; inferring units for dimensionless numerics; `*`/`/` unit
algebra beyond existing Dim rules.

## Consequences

- Unit tracking on `Ty` remains (reused by ADR 0155).
- Reject diagnostics now apply only when units lack a shared canonical.
