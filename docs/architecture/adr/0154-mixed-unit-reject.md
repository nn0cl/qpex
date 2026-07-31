# ADR 0154: Reject mixed-unit `+` / `-` (no automatic rescale)

## Status

**Accepted** (2026-07-31) — unlocks LISS-0186 under WP-0060.
Implements [ADR 0124](0124-si-scale-conversion-explicit.md) Decision 5.

## Decisions

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

- `1.kg + 1.g` and `Mass a=1.kg; Mass b=1.g; a+b` are rejected.
- `(1.kg to g) + 1.g` typechecks.
