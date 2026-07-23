# LISS-0036: Continuous operators and discretization boundary

- Status: **proposed** (Architecture Path; design only)
- Depends on: LISS-0018, LISS-0033, ADR 0069
- Blocks: direct source coverage for continuous-space models

## Summary

Investigate integrals, derivatives, wavefunctions, boundary conditions, and
continuous-domain notation. Decide whether these belong to QPex source,
symbolic front-end ports, or an external preprocessing boundary.

## Acceptance questions

- What finite representation is required before simulator/QPU execution?
- How are basis, resolution, boundary conditions, and approximation error
  represented?
- Can continuous notation coexist with the finite Hilbert type boundary?
- Which exact/numeric choices belong to LISS-0018?

## Non-goals

This LISS does not claim infinite-dimensional QPU execution or silently hide
discretization.
