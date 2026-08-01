# LISS-0226: Nested empty `sum` must not inject undetermined OpIdentity

## Metadata

- Local issue ID: LISS-0226
- GitHub issue: (none yet)
- Status: **complete**
- Phase: Phase 3 complete (Adjudicator authorized with WP-0071 residual)
- Type: bug
- Priority: P0
- Initial planning size: S
- Current planning size: S
- Owner/agent: Cursor agent
- Related branch: `feature/wp-0071-binder-when-enum-gaps`
- Program: [WP-0071](../work-plans/WP-0071-s01-kernel-gaps-from-review.md)

## Summary

```staqex
Operator H = sum (i in Index<0..1>, j in Index<0..1>) where i < j {
    Z[i] * Z[j]
}
```

lowers to `Z[0]*Z[1] + OpIdentity(kind=sum, acting_space=None)` because the
inner empty `sum` (when `i=1`) becomes an additive identity **operator** rather
than a **zero contribution**. Evolve then fails with
`IDENTITY_ACTING_SPACE_UNDETERMINED` unless `QubitRegister<N>` is declared.

Empty **outer** sums still become undetermined identity (LISS-0056) — keep that.
Only nested empty contributions inside a non-empty outer `sum` should omit.

## Acceptance Notes

- [x] Red: `where i < j` two-index sum evolves on two wires without QubitRegister
- [x] Green: lowered AST has no undetermined OpIdentity sibling
- [x] LISS-0056 empty outer sum still rejects without acting space
- [x] S01 `Lattice.damage_hamiltonian` can use the where form again

## Dependencies

- Related: LISS-0056, LISS-0224
- Spec: [staqex-v1-liss-0226-nested-empty-sum-identity.md](../specs/staqex-v1-liss-0226-nested-empty-sum-identity.md)

## Verification

- `python3 tests/test_liss_0226_nested_empty_sum_identity_red.py`
- LISS-0056 empty-domain tests still PASS
