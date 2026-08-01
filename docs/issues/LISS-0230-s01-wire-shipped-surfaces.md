# LISS-0230: S01 wire Basis / Trace-Out / Algebraic Fusion / Rankine·troy

## Metadata

- Local issue ID: LISS-0230
- GitHub issue: (none yet)
- Status: **proposed**
- Phase: (none — intake)
- Type: chore
- Priority: P2
- Initial planning size: M
- Current planning size: M
- Owner/agent: (unassigned)
- Related branch: (none yet)
- Program: [WP-0072](../work-plans/WP-0072-s01-coverage-residuals.md)

## Summary

These Kernel surfaces are **already shipped** (WP-0035 / 0044–0048 / 0047 /
0050 / 0057 family) but S01 does not exercise them. Re-check asked for
showcase wiring without inventing new Kernel:

| Surface | Shipped cue | S01 gap |
|---|---|---|
| `Basis<N>` binders | ADR 0118 / LISS-0148 | no `sum (i in Basis<…>)` |
| Trace-Out GC | ADR 0138 / 0142 / … | manual `\|0>` discharge only |
| Algebraic / poly≥2 Operator Fusion | ADR 0141 / 0157 | compose is arithmetic pipe only |
| Rankine `.R` / troy `.oz_t` | ADR 0144–0151 | SI + lb/oz/t only |

## Acceptance Notes

- [ ] Each row has a narrative-true S01 call site (not a dead inspect tag)
- [ ] Scorecard B rows cite paths + runnable phase
- [ ] No new Kernel behavior unless a shake finds a real bug (then split Issue)

## Dependencies

- S01 mission lock / locked scenario — reality wins over syntax museum
- Kernel ADRs above stay authoritative

## Verification

- Affected S01 mains / domain files seed 0 green
- Scorecard evidence paths filled
