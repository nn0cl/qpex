# LISS-0232: S01 Index lattice beyond 2-wire toy

## Metadata

- Local issue ID: LISS-0232
- GitHub issue: (none yet)
- Status: **proposed**
- Phase: (none — intake)
- Type: chore
- Priority: P2
- Initial planning size: S
- Current planning size: S
- Owner/agent: (unassigned)
- Related branch: (none yet)
- Program: [WP-0072](../work-plans/WP-0072-s01-coverage-residuals.md)

## Summary

`grid/block_costs.sqx` uses `Index<0..1>` so binders match the tonight
**two-wire** evolve spine (LISS-0224/0226). That is honest for MVP green, but
the disaster lattice story (`n_blocks = 4.0`, K-ku envelope) still reads as a
2-site toy. Re-check asked to grow Index width without silently breaking evolve.

## Acceptance Notes

- [ ] Binder domains reflect a narrative block count > 2 (or document why not)
- [ ] Evolve / register arity stays consistent (no undetermined identity regress)
- [ ] Scorecard notes real Index width + wire count
- [ ] If Kernel limits force a satellite main, cite it explicitly

## Dependencies

- LISS-0224 / 0226 / 0227 complete on main
- May need multi-register / `QubitRegister<N>` acting-space rules

## Verification

- Lattice + tonight (or satellite) main seed 0 green
- Red test if a Kernel gap surfaces (then split Kernel Issue)
