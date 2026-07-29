# Agent sync addendum: project / interfer / System

Date: 2026-07-22. Append to `agent-sync-staqex-baseline.md` read order.
Full baseline still applies; this file records the **stdlib naming lock**.

## Normative spellings (ADR 0021)

| Role | Name | Not |
|------|------|-----|
| Pushforward | `map` | — |
| Subspace proj. + renorm | `project` | `filter`, `given` (retired) |
| Combine states | `interfer` | `fold` (retired as normative) |
| Domain trait | `System` | `QSystem`, `Evolvable` |
| Terminal collapse | `measure` | PPL `observe` |

## Semantics

- §Project / §Interfer in `docs/specs/staqex-formal-semantics-sketch.md`
- Density form $\rho' = \Pi\rho\Pi / \mathrm{Tr}(\Pi\rho\Pi)$ is the lift
  narrative; MVP is the PMF shadow.

## AST

- Expr nodes: `Map`, `Project`, `Interfer`
- Decls: `TraitDef`, `SystemDef` (`: System`)

## Docs

- `staqex-stdlib-combinators.md`
- ADR 0021 (supersedes ADR 0020 naming)

## Hold

No harness / stdlib / typechecker implementation until Adjudicator unseals.
