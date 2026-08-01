# ADR 0076: Numeric representation and precision policy

## Status

**Accepted** (2026-08-01) — WP-0077 / LISS-0213. Shipped slice matches
[LISS-0018](../../issues/LISS-0018-numerical-representation.md) numeric policy
for the current Kernel (`f64` path). Horizon / permanence questions remain
under [ADR 0097](0097-numeric-representation-horizon.md). This acceptance does
**not** authorize a new exact-rational Kernel mode or a new dependency.


## Decision proposal

1. MVP runtime storage remains dependency-free binary floating point: `f64` for
   real scalars/probabilities and complex pairs of `f64` for amplitudes and
   finite matrices. The existing `runtime/matrix.py` remains the implementation
   boundary; NumPy/SciPy are not required dependencies.
2. Exact rational arithmetic is not a Kernel runtime mode. Literal spelling may
   be retained for diagnostics/provenance, but numeric evaluation uses the
   declared floating representation.
3. Tolerances are contract-specific, not one global epsilon:

   | Contract | MVP tolerance |
   |---|---:|
   | PMF normalization / ordinary probability assertions | `1e-9` |
   | Density trace and positivity | `1e-12` |
   | Kraus completeness | `1e-12` |
   | POVM completeness | `1e-12` |
   | Lindblad trace guard | `1e-12` |

   A tolerance validates and diagnoses; it never authorizes silent
   normalization, clipping, or repair.
4. Numeric literals use the existing literal-lifting rule and are interpreted
   as finite floating values in numeric execution. `dirac(x)` remains an
   explicit state constructor and is not a precision or distribution marker.
5. Continuous PDFs, unbounded domains, and Monte Carlo sample sources are not
   Kernel values in this MVP. They belong behind a future port or an explicit
   LISS-0036 discretization contract before entering the Kernel.
6. Raw matrix serialization is not part of the default Host result. Numeric
   provenance may record representation kind, precision policy, tolerance
   class, and source identity without exposing simulator storage.

## Compatibility boundary

Existing accepted programs retain their current PMF tolerance behavior. The
physical tolerances apply only to DensityState/Channel/POVM/Lindblad contracts
and do not silently change ordinary Joint arithmetic.

## Deferred follow-ons

Arbitrary precision, continuous PDF ports, sparse/accelerated storage,
user-configurable tolerances, and error-bound propagation remain separate
follow-on decisions.

## Implementation record

The current policy boundary is implemented by
`compiler/staqex/runtime/numeric_policy.py`. Density and Lindblad physical
tolerance aliases use its shared `PHYSICAL_TOLERANCE`; no external numeric
dependency or implicit repair path was introduced.
