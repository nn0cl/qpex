# ADR 0044: Typed product carriers State<(A, B)>

## Status

Accepted (2026-07-23).

Companions: ADR 0041 (`*|*` / `trace_out`). Verification: **SV-22**.

## Context

Runtime product spaces existed as named joint coordinates, but the type
system still treated `*|*` as `State<Any>`. Physicists need
$\mathcal{H}_A\otimes\mathcal{H}_B$ written as `State<(Coin, Position)>`.

## Decision

### A. Type syntax

1. Product carriers: `(T1, T2, …)` inside `State<…>` or as bare TypeRef.
2. Type-First multi-bind: `State<(Qubit, Position)> (c, x) = left *|* right`.
3. Discrete labels `Qubit`, `Coin`, `Position` are dimensionless carriers
   (Int-compatible at MVP).

### B. Checking

1. `*|*` infers `State<(Tl, Tr)>`; tuple bind splits component types into env.
2. Single-name product declaration → **`PRODUCT_BIND_ERROR`**.
3. Arity mismatch → **`PRODUCT_ARITY_ERROR`**.
4. Incompatible component payloads → **`PRODUCT_TYPE_MISMATCH`**.

### C. Subsystems

Coordinate names remain the subsystem ids for `trace_out(coord)` (ADR 0041).

## Consequences

Positive: DTQW / Bell prep can declare product Hilbert space types.
Negative: nested products beyond flat `(A,B,…)` and class-packaged tensors deferred.

## Verification

SV-22 — typed bind, arity/payload errors, `trace_out`, typed `dtqw.staqex`.
