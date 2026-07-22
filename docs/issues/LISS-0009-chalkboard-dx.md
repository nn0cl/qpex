# LISS-0009: Chalkboard DX — cut redundancy, keep formula beauty

## Metadata

- Local issue ID: LISS-0009
- GitHub issue: none
- Status: **proposed**
- Phase: Feature Path (mostly stdlib + examples; thin ADR if new prelude consts)
- Type: chore + DX + docs
- Priority: P2
- Initial planning size: M
- Current planning size: M
- Reclassification reason: n/a
- Owner/agent: TBD
- Related branch: TBD `docs/chalkboard-dx`

## Summary

Audit official examples (and thin Kernel sugar) so physics that is short on the
blackboard is not padded in QPex with magic floats, unused Type-First binds, or
duplicated narrative skins. Keep **Never Leave the State**; prefer prelude
constants and honest operators over comment-synced noise.

## Findings (2026-07-23 audit)

### Already good (keep)

| Area | Why it reads like math |
|------|------------------------|
| Grover `phase(idx, pi, 2)` + `grover_diffuse` | Matches $e^{i\pi}$ mark + diffusion |
| Bell `\|+\>`, `cnot`, `expect(ZZ, …)` | Φ⁺ prep without nested `when` |
| Ising `H = -J*(Z(0)*Z(1)) - h*(X(0)+X(1))` then `evolve under H for t` | Hamiltonian spelling is close to paper |
| Gauge `phase(site, pi)` | U(1) one-liner |
| Prelude `pi` / `Math.pi` (LISS-0007) | Magic π literal gone |

### Redundant / ugly (fix in this issue)

| Smell | Where | Desired |
|-------|--------|---------|
| Magic `0.7071067811865476 * (X+Z)` | 07, 09, 15 Coin | `(X+Z) * inv_sqrt2` or `H` / shared const |
| Magic `1.5707963267948966` | 09 `coin_parameters.theta` | `pi / 2` |
| Unused decorative `Float` binds | 11–15 mains (`modulus`, `hop_id`, …) | Remove or `inspect` with purpose |
| Hand tables + harvested Floats still duplicated pedagogy | 11 modexp `when` | Keep honesty; optional later `modexp` surface (not this issue) |
| Dream skins ≈ 04/09 | 12/14/15 | Already honest in README; optional shared `_lib` (low priority) |

### Language gaps that block beauty (may need ADR)

1. **Classical `sqrt` / `inv_sqrt2` prelude** — so Coin = $(X+Z)/\sqrt{2}$ without decimal soup.
2. Optional: allow `Operator Coin = H` when `H` is the Hadamard gate name in Operator position (today Coin is built from Paulis).

## Acceptance Notes

- [ ] Prelude (or thin ADR 0062 amend): `inv_sqrt2` (and optionally `sqrt2`) as
      classical Float, same rules as `pi` (no State⊕const mix).
- [ ] Replace `0.7071…` / `1.5707…` in official examples with `inv_sqrt2` /
      `pi / 2`.
- [ ] Cull or justify unused Float / enum binds in examples 11–15.
- [ ] Short note in `examples-catalog-conventions.md`: “chalkboard test” —
      prefer paper spelling; ban new magic π/√2 decimals.
- [ ] SV suite green.

## Dependencies

- Related: LISS-0007 / ADR 0062 (`pi`); LISS-0006 catalog honesty
- Does not block: LISS-0008 Trotter

## Adjudicator Decision Points

- [ ] Name: `inv_sqrt2` vs `SQRT1_2` vs `Math.invSqrt2`.
- [ ] Whether Operator-position `H` sugar is in-scope or deferred.

## AI Planning Records

### AIP-0009-001

- Status: proposed
- Created at: 2026-07-23
- Planning size: M
- Intended scope: prelude const + example cleanup; no QFT / Trotter
- Confidence: high

## References

- `examples/07_quantum_walk/dtqw.qpex`, `09_…/walk_operators.qpex`, `15_…/mesh_walk.qpex`
- `examples/09_…/models/coin_parameters.qpex`

## Work Notes

- 2026-07-23: filed from Adjudicator “数式らしい美しさ” review.

## Verification

- Examples compile/run; no remaining `0.7071067811865476` / `1.5707963267948966`
  in `examples/`.
