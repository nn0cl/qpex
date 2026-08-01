# LISS-0224: Method-returned finite binders must lower before evolve

## Metadata

- Local issue ID: LISS-0224
- GitHub issue: (none yet)
- Status: **complete** (2026-08-01)
- Phase: Phase 1 Red → Phase 2 Green (Adjudicator authorized 2026-08-01)
- Type: bug
- Priority: P0
- Initial planning size: M
- Current planning size: M
- Owner/agent: Cursor agent
- Related branch: `feature/wp-0071-binder-when-enum-gaps`
- Program: [WP-0071](../work-plans/WP-0071-s01-kernel-gaps-from-review.md)

## Summary

Top-level `Operator H = sum (i in Index<…>) { … }` lowers and runs under
`evolve` (LISS-0052). The same binder returned from a **class method**

```staqex
Operator H = lattice.damage_hamiltonian()  // body: sum (…) { Z[i]*Z[j] }
evolve … under H …
```

stays `OpBinder` in `self.operators` / method `local_ops`, so Joint fails with
`RUNTIME_ERROR: cannot compile sparse Pauli for OpBinder`.

Found by S01 shake ([LISS-0223](LISS-0223-s01-language-physicist-review.md)).

## Acceptance Notes

- [x] Red: failing test for method-returned `sum`/`product` binder under `evolve`
- [x] Green: method-returned binder lowers to Pauli AST; `run` exits 0
- [x] Free-fn `fn … -> Operator` returning a binder also lowers (same path)
- [x] Top-level binder regression (LISS-0052 shape) still green
- [x] S01 tonight spine evolves under method-returned `H_damage` (LISS-0224)

## Dependencies

- Parent: LISS-0223 (discovery)
- Related: LISS-0052 (complete — top-level only), LISS-0139 (Operator method call)
- Spec: [staqex-v1-liss-0224-method-returned-binder-evolve.md](../specs/staqex-v1-liss-0224-method-returned-binder-evolve.md)

## Adjudicator Decision Points

- None for MVP: reuse existing finite-binder lowering; no new ADR.

## Context

- Included: `evaluator._resolve_operator_method_call`, `_resolve_operator_factory_call`,
  `finite_binder._lower_operator_expr`
- Omitted: QASM emit path stretch goals beyond existing top-level behavior
- Assumptions: register size inference from evolve arity remains as today

## AI Planning Records

### AIP-0224-001

- Status: accepted (working)
- Created at: 2026-08-01
- Planning size: M
- Intended execution route: Feature Path Red→Green
- Intended scope: lower OpBinder when materializing Operator from method/fn return

## Work Notes

- Root cause: method Operator binds stored raw `stmt.expr` without
  `_lower_operator_expr`; top-level main binds use `lower_finite_binder_operators`.
- Fix: `Evaluator._lower_operator_value` + apply on method/factory Operator
  materialization; stash `self._unit` for lowering context.
- Residual: `sum … where i < j { Z[i]*Z[j] }` still wants `QubitRegister<N>`
  (`IDENTITY_ACTING_SPACE_UNDETERMINED`) — separate from method-return lowering.

## Verification

- `python3 tests/test_liss_0224_method_returned_binder_evolve_red.py` PASS
- S01 `main_disaster_response.sqx` evolves under `lattice.damage_hamiltonian()`
