# WP-0031: Hamiltonian library surface

| Field | Value |
|---|---|
| Status | **planning** — 2026-07-31; docs/Issues; Kernel Red not authorized |
| Program | [hamiltonian-library-surface-plan](../specs/staqex-v1-hamiltonian-library-surface-plan.md) |
| Parent reading | [physicist-dx-harmony](../architecture/physicist-dx-harmony.md) |
| Prerequisite | LISS-0136 (PR #180) |
| Created | 2026-07-31 |

## Issue rows

| ID | Topic | Priority | Status |
|---|---|---|---|
| LISS-0137 | Classical Float binding + parametrized Operator factory | P0 | **ready** (expanded) |
| LISS-0139 | Operator RHS method Call parse + return | P0 | **ready** |
| (follow-up) | Showcase `tfim(J,h)` / `hamiltonian()` | P1 | after 0137+0139 Green |
| LISS-0138 | `when` ket prepare arms | — | **out of program** |

## Current next

Adjudicator Plan authorize for **LISS-0137** (or batch WP-0031
`approved_for_execution`). Then 0139. Do not start Red without that gate.

## Invalidating triggers

- ADR change that classical coefficients are quantum LINEAR resources again
- Decision that `class` must not return `Operator` (then demote 0139)
