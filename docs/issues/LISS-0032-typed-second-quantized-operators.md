# LISS-0032: Typed second-quantized operators

- Status: **Complete** (Jordan-Wigner numerical mapping slice) — Adjudicator
  final review approved 2026-07-25. Bravyi-Kitaev, Boson, and Spin mapping
  remain a possible future follow-up, not scheduled and not part of this
  closure.
- Depends on: LISS-0030, LISS-0031, LISS-0033, LISS-0019
- Architecture decision: [ADR 0093](../architecture/adr/0093-jordan-wigner-numerical-mapping.md)
  (2026-07-25) — Jordan-Wigner mapping for `FermionOperator`, one-body and
  two-body terms in scope, no hard limit or scope cut for performance
  reasons.
- Blocks: quantum chemistry and many-body Hamiltonian source coverage
- Acceptance draft: [`staqex-second-quantized-operators.md`](../specs/staqex-second-quantized-operators.md)
- AT-TDD Phase 1 Red (typed boundary): [`test_second_quantized_operators_red.py`](../../tests/test_second_quantized_operators_red.py)
- AT-TDD Phase 1 Red (numerical mapping): [`test_jordan_wigner_mapping_red.py`](../../tests/test_jordan_wigner_mapping_red.py)

## Summary

Define distinct fermion, boson, spin, and qubit operator families. Include
creation/annihilation operators, statistics, canonical ordering, and an
explicit mapping boundary such as fermion-to-qubit lowering.

## Acceptance questions

- Are `FermionOperator`, `BosonOperator`, `SpinOperator`, and `QubitOperator`
  distinct types rather than aliases of `Operator`?
- How are canonical ordering and exchange relations represented and diagnosed?
- Which mappings are language semantics, compiler passes, or external ports?
- How are mapping choice, qubit count, and approximation provenance retained?

## Non-goals

This LISS does not select OpenFermion, Qiskit Nature, PennyLane, or a provider
SDK, and does not authorize implementation of a chemistry solver.

## Phase 2 Green record

- Added typed family boundaries for `FermionOperator`, `BosonOperator`,
  `SpinOperator`, and `QubitOperator`.
- Added symbolic `create`, `annihilate`, `spin_raise`, and `spin_lower`
  operator atoms.
- Mixed second-quantized families produce
  `SECOND_QUANTIZATION_TYPE_ERROR`.
- Mapping is explicit through the function-shaped `map(operator, mapping)`
  boundary; automatic mapping/provider selection is not performed.
- Early `measure` remains rejected in second-quantized expressions.
- Regression checks: all standalone `tests/test_*.py` scripts passed;
  specification verification passed 165/165 (100%).

## Phase 3 review record

- Symbolic IR records family statistics (`fermionic`, `bosonic`, `spin`,
  `qubit`).
- Creation/annihilation atoms receive deterministic canonical ordering.
- Fermion permutations record an exchange sign; Boson ordering does not invent
  a fermion sign.
- Explicit mapping names are recorded in the resolved-link metadata surface.
- Full exchange-law normalization, output-domain validation, and numerical
  mapping remain deferred.

Phase 3 acceptance evidence: second-quantized operator tests pass, all
standalone tests pass, and specification verification passes 165/165 (100%).

## Phase 2 Green record (Jordan-Wigner numerical mapping, 2026-07-25)

Architecture approved per ADR 0093: one-body and two-body fermionic terms in
scope; correctness prioritized over Pauli-string count/performance; Bravyi-
Kitaev, Boson, and Spin mappings remain deferred.

- New module `compiler/staqex/second_quantization.py`: expands a
  `FermionOperator` symbolic expression into an `OpExpr` Pauli-sum AST (the
  same shape the parser already produces for a hand-written `Operator`
  expression), by direct term-by-term Jordan-Wigner substitution
  (`a_p = (X_p+iY_p)/2`, `a_p^dagger = (X_p-iY_p)/2`, with a `Z`-string
  parity prefix for `k<p`), Pauli-algebra multiplication with phase tracking,
  grouping by Pauli-string, and a final real-coefficient assertion (raises
  `SECOND_QUANTIZATION_MAPPING_UNSUPPORTED` if a genuinely non-Hermitian
  residual survives grouping — the mapping's own representational limit, not
  a new Hermiticity-checking mechanism; `unitarity_check.py` and
  `backend/qasm/trotter.py` already own that check per ADR 0093 point 7).
- `typecheck.py`: `map(op, mapping)` now validates that `op`'s family is
  `FermionOperator` and `mapping` is `JordanWigner`; anything else produces
  `SECOND_QUANTIZATION_MAPPING_UNSUPPORTED` at compile time (added to
  `pipeline.py`'s hard-diagnostic set), so Boson/Spin mapping attempts fail
  with a specific, honest diagnostic instead of the generic `RUNTIME_ERROR`
  every unmapped construct previously produced.
- `runtime/evaluator.py`: `FermionOperator`/`BosonOperator`/`SpinOperator`
  locals are kept symbolic (`self.second_quantized_operators`); a
  `QubitOperator` bind that is `map(H, JordanWigner)` resolves through the
  new module and is stored in `self.operators` exactly like a hand-written
  `Operator` bind, so `evolve`/`apply` need no special-casing.
- `backend/qasm/lower.py`: the same resolution feeds `op_env`, so the
  existing Trotter/QASM lowering path consumes the mapped result unchanged.
- `symbolic_ir.py`: mapping provenance records now include `qubit_count`
  (previously only `operator`/`mapping`); the one pre-existing test asserting
  the old two-key shape was updated to the three-key shape in the same
  commit.

Verification performed:

- All 11 Phase 1 Red assertions in `test_jordan_wigner_mapping_red.py` pass:
  a mapped diagonal number operator, an adjacent hopping term, a
  non-adjacent hopping term (parity `Z`-string), and a two-body
  density-density interaction each **run** on the SV simulator (numerically
  matching a hand-written Pauli-operator equivalent via measurement
  marginals) **and** emit QASM — both required, neither alone accepted, per
  the Adjudicator's 2026-07-25 acceptance criterion. Mapping provenance
  records `qubit_count`. A `BosonOperator` mapping attempt is rejected with
  `SECOND_QUANTIZATION_MAPPING_UNSUPPORTED`, not a generic crash.
- Full manual regression sweep across all `tests/*.py` (255 test functions
  passing after this change, up from 244): no new failures beyond the same
  5 pre-existing, unrelated failures already present on `main`.
- `python3 tests/spec_verification/run_all.py`: 165/165 (100%).

Phase 3 Refactor and Adjudicator final review remain open. A separate,
independent defect (silent Trotter step-count clamping in
`backend/qasm/trotter.py`, found while verifying the QASM path could accept
a mapped Hamiltonian) was split out per explicit Adjudicator instruction to
[LISS-0050](LISS-0050-trotter-step-silent-clamp.md) rather than folded into
this Issue.

## Phase 3 Refactor record (Jordan-Wigner numerical mapping, 2026-07-25)

- Extracted `resolve_mapping_expr(expr, source_env)` in
  `second_quantization.py`, shared by `runtime/evaluator.py`'s
  `_bind_second_quantized` and `backend/qasm/lower.py`'s bind loop, removing
  the duplicated "is this `map(op, JordanWigner)` referencing a known
  `FermionOperator` source" check that both call sites had inlined
  separately during Phase 2 Green.
- No behavior change: all 11 Phase 1 Red assertions still pass, full manual
  regression sweep still shows 255 passing test functions with the same 5
  pre-existing unrelated failures, and specification verification still
  passes 165/165 (100%).

Phase 3 complete; Adjudicator final review of the merged result is the only
remaining item.

## Closure (2026-07-25)

Adjudicator final review approved ("クローズして"). Issue closed as
**Complete** for the Jordan-Wigner numerical-mapping scope (one-body and
two-body `FermionOperator` terms). Bravyi-Kitaev, Boson, and Spin mapping
remain possible future follow-ups — not scheduled, and opening any of them
would need a new LISS with its own Architecture Path review, not a
reopening of this one.
