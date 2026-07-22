# ADR 0052: Extended static unitarity checks

## Status

Accepted (2026-07-23).

Companions: ADR 0045. Verification: **SV-30**.

## Context

ADR 0045 caught `project` / constant `map` / collapsing `when` on strict
quantum lineages, non-unitary `apply` matrices, and non-Hermitian `evolve`.
After `capply` / Fock / grid HO, several dishonest patterns still compiled:

- `apply(N+½, qubit)` / `apply(Xx, …)` — Schrödinger $H$ misused as a gate
- `map(psi, x -> x * 0)` — bit support collapse not flagged as “constant λ”
- `capply` / non-Hermitian `evolve` lacked dedicated verification cases

## Decision

Extend **`NON_UNITARY_TRANSFORM_ERROR`** with:

| Pattern | Rationale |
|---------|-----------|
| `apply`/`capply`/`ocapply` of Fock or grid `Operator` | Not a qubit gate unitary; use `evolve under H` |
| `map` λ with $f(0)=f(1)$ on strict quantum | Non-injective on bit support |
| (retain) non-unitary gate `Operator`, non-Hermitian $H$ | ADR 0045 |

**Still Deferred:** exhaustive proof of every pushforward; Float-grid
injectivity of arbitrary `map`; open BC continuum.

**Still allowed:** classical `coin` `project`; gauge `phase`+`project` pedagogy.

## Consequences

Positive: Fock/grid / sneaky `map` lies fail at compile time.
Negative: completeness still intentional MVP.

## Verification

SV-30 — reject/accept cases above; SV-23 + gauge example remain green.
