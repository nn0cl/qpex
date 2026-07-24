# ADR 0088: Inclusive finite-range binder lowering

## Status

Accepted for LISS-0043 Phase 1 Red. This is the follow-up lowering slice for
the accepted symbolic binder boundary in LISS-0030.

## Context

LISS-0030 already parses and type-checks symbolic `sum`/`product` binders, but
does not expand them into executable Pauli operators. An open finite chain
needs a domain that excludes its final site when the body refers to
`next(i)`.

## Decision

1. `Index<start..end>` is an **inclusive** finite range.

   ```qpex
   Index<0..N-2>
   ```

   denotes `0, …, N-2`. The notation is intentionally mathematical rather than
   Rust-style half-open range syntax.

2. The first boundary policy is fixed `Open`. `next(i)` is valid only when its
   resolved target is within the containing static register/domain. An
   out-of-range access is a hard `BINDER_INDEX_OUT_OF_BOUNDS` diagnostic.

3. The first lowering body is restricted to a finite Pauli nearest-neighbor
   term:

   ```qpex
   sum (i in Index<0..N-2>) {
       coefficient * Pauli[i] * Pauli[next(i)]
   }
   ```

   The resolved result is a concrete Pauli `Operator` tree suitable for the
   existing Hamiltonian/Suzuki path.

4. Lowering must retain a provenance record containing the source span, binder
   variable, resolved domain, expanded term count, and resource-check result.
   The symbolic source form remains available as provenance; it is not the
   executable operator value.

5. Range endpoints must be statically resolvable. Numeric endpoints are
   supported in the first slice. `N-2` is supported only when `N` resolves from
   a static Hilbert shape; runtime `Int`, `Param`, `ShotCount`, and Host values
   cannot determine a binder range.

6. Empty, reversed, negative, or out-of-register ranges are hard domain
   errors. Expansion beyond the existing resource budget is a hard
   `BINDER_RESOURCE_ERROR`; truncation and symbolic fallback are forbidden in
   this executable slice.

## Deferred

`Periodic` boundaries, `product`, `Basis<N>` domains, indexed coefficient
arrays, arbitrary functions, non-Pauli operators, and direct provider/QPU
lowering remain deferred.

## Verification contract

- Inclusive range syntax parses into a range-bearing binder domain.
- Open-chain nearest-neighbor sums resolve to the expected finite Pauli term
  count.
- `next(last)` produces `BINDER_INDEX_OUT_OF_BOUNDS`.
- Invalid/empty ranges produce `BINDER_DOMAIN_ERROR`.
- Oversized ranges produce `BINDER_RESOURCE_ERROR`.
- Provenance identifies the source binder and expanded term count.
