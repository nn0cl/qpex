# WP-0031: Hamiltonian library surface

| Field | Value |
|---|---|
| Status | **complete** — 2026-07-31; Kernel Red/Green on feature branch (PR pending) |
| Program | [hamiltonian-library-surface-plan](../specs/staqex-v1-hamiltonian-library-surface-plan.md) |
| Parent reading | [physicist-dx-harmony](../architecture/physicist-dx-harmony.md) |
| Prerequisite | LISS-0136 (**complete**, #180) |
| Created | 2026-07-31 |

## Issue rows

| ID | Topic | Priority | Status |
|---|---|---|---|
| LISS-0137 | Classical Float binding + parametrized Operator factory | P0 | **complete** (PR pending) |
| LISS-0139 | Operator RHS method Call parse + return | P0 | **complete** (PR pending) |
| (follow-up) | Showcase `tfim(J,h)` / `hamiltonian()` | P1 | **done** on same branch |
| LISS-0138 | `when` ket prepare arms | — | **out of program** |

## Current next

PR merge review for `feature/liss-0137-0139-hamiltonian-library-surface`.
Then Showcase S2 or LISS-0138 as separate authorize.

## Invalidating triggers

- ADR change that classical coefficients are quantum LINEAR resources again
- Decision that `class` must not return `Operator` (then demote 0139)
