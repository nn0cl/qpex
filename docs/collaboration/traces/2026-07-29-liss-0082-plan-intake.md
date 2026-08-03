# Trace: LISS-0082 plan intake

| Field | Value |
|---|---|
| Date | 2026-07-29 |
| Issue | LISS-0082 |
| Path | Architecture / Feature Path plan intake |
| Branch | `docs/liss-0082-plan-intake` |
| Prerequisite | LISS-0081 global closeout merged (PR #134) |

## Design note

Additive Quantum Semantic IR on the Python Shipping Kernel per ADR 0106 D9
and compiler blueprint §4.3. Shared simulator/QPU semantic contract; no
provider types. Slice A is root DTOs + verifier + builder stub only.

## Artifacts

- [docs/issues/LISS-0082-quantum-semantic-ir.md](../../architecture/documentation-compression-map.md)
- [docs/specs/staqex-v1-quantum-semantic-ir-plan.md](../../specs/staqex-v1-quantum-semantic-ir-plan.md)
- Claim sync: open-work-register, local-issue-planning, WP-0025 Current next

## Out of scope (locked at intake)

Numerical solving; gate/matrix expansion; Jordan–Wigner execution; Algorithm
Plan IR; provider/OpenQASM-as-semantics; Equation DTO extensions; soft
`compile_source` wire (optional Slice E later).

## Stop condition

Plan intake complete. **No compiler or test files changed.**

Next: Adjudicator authorizes **Slice A Phase 1 Red only**.
