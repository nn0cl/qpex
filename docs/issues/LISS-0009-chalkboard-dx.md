# LISS-0009: Chalkboard DX — cut redundancy, keep formula beauty

## Metadata

- Local issue ID: LISS-0009
- GitHub issue: none
- Status: **done**
- Phase: Feature Path — Green
- Type: chore + DX + docs
- Priority: P2
- Initial planning size: M
- Current planning size: M
- Reclassification reason: n/a
- Owner/agent: Cursor agent
- Related branch: `docs/language-axioms-mvp-spec`

## Summary

Audit official examples (and thin Kernel sugar) so physics that is short on the
blackboard is not padded in Staqex with magic floats, unused Type-First binds, or
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

### Fixed in this issue

| Smell | Fix |
|-------|-----|
| Magic `0.7071… * (X+Z)` | `(X + Z) * inv_sqrt2` (07, 09, 15) |
| Magic `1.5707…` | `pi / 2.0` (09 coin θ, ket evolve) |
| Grid wavepacket σ decimal | `inv_sqrt2` |
| Decorative unused Float / enum in 11–15 mains | Removed; inspect domain fields directly |

### Deferred

| Item | Note |
|------|------|
| Operator-position bare `H` | ADR 0062 §7 — later |
| Shared `_lib` for dream skins | Low priority; Honesty READMEs already OK |

## Acceptance Notes

- [x] Prelude (ADR 0062 amend): `inv_sqrt2` + `sqrt2` classical Floats; `Math.*` aliases.
- [x] Replace `0.7071…` / `1.5707…` in official examples.
- [x] Cull unused Float / enum binds in examples 11–15.
- [x] Chalkboard test note in `examples-catalog-conventions.md`.
- [x] SV suite green.

## Dependencies

- Related: LISS-0007 / ADR 0062 (`pi`); LISS-0006 catalog honesty

## Adjudicator Decision Points

- [x] Name: **`inv_sqrt2`** (+ `sqrt2`); `Math.inv_sqrt2` alias (same as `Math.pi`).
- [x] Operator-position `H` sugar **deferred**.

## AI Planning Records

### AIP-0009-001

- Status: done
- Created at: 2026-07-23
- Planning size: M
- Intended scope: prelude const + example cleanup; no QFT / Trotter
- Confidence: high

## References

- ADR 0062 (amended), `examples/07_quantum_walk/dtqw.staqex`, walk / mesh Coin ops

## Work Notes

- 2026-07-23: filed from Adjudicator “数式らしい美しさ” review; shipped same day.

## Verification

```bash
python3 tests/test_prelude_pi.py
rg '0\.7071067811865476|1\.5707963267948966' examples/   # expect empty
python3 tests/spec_verification/run_all.py
```
