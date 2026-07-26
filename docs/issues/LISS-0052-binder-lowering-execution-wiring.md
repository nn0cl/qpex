# LISS-0052: Binder lowering execution wiring

## Metadata

- Local issue ID: LISS-0052
- GitHub issue: none
- Status: proposed
- Phase: phase-0-design complete (ADR 0096 D7 accepted); awaiting Phase 1 Red approval
- Type: bug / spec-implementation divergence
- Priority: P1
- Initial planning size: M
- Current planning size: M
- Reclassification reason: n/a
- Owner/agent: TBD
- Related branch: none yet

## Summary

`ADR 0088` Decision 3 promises that finite-binder lowering produces "a
concrete Pauli `Operator` tree suitable for the existing Hamiltonian/Suzuki
path". The implementation does not do this: it produces a JSON-shaped `dict`
under `qpu_ir["binder_lowering"]` for inspection, while the AST bound to the
operator name stays `OpBinder`, which no execution path can consume.

This is a **bug against an accepted specification**, not a design gap. It is
the first step of ADR 0096's implementation order (D7), and it is what makes
every other binder capability observable at all.

## Reproduction

```qpex
package t
pub fn main() -> Unit {
    QubitRegister<4> register = system()
    Operator H = sum (i in Index<0..2>) {
        1.0 * Z[i] * Z[next(i)]
    }
    state a = |+>
    state b = |0>
    state c = |0>
    state d = |0>
    state (a, b, c, d) = evolve (a, b, c, d) under H for 0.1
        using Suzuki(order = 2, steps = 4)
    measure a
}
```

- `check` reports `ok`, and `compiled.qpu_ir["binder_lowering"]["H"]`
  contains the correct 3-term expansion.
- `run` exits 1: `RUNTIME_ERROR: cannot compile sparse Pauli for OpBinder`.
- `emit-qasm` exits 1: `QASM_TROTTER_UNSUPPORTED_H: cannot compile sparse
  Pauli for OpBinder`.

Neither failure is silent, so this is not the LISS-0049/LISS-0050 class of
defect — but the promised capability does not exist.

## Root cause

- `compiler/qpex/finite_binder.py`'s `_lower_expr` builds plain `dict`
  nodes (`{"kind": "Pauli", ...}`), and `_operator_metadata` returns them as
  `operator_tree` inside an inspection payload.
- Nothing writes an `OpExpr` back into the environment that
  `runtime/evaluator.py` (`self.operators`) and
  `backend/qasm/lower.py` (`op_env`) consume.
- `runtime/sparse_pauli.py`'s `compile_sparse_pauli` has no handler for
  `OpBinder`, and none for `OpIndexed` either — so even a hand-written
  `Z[0]` outside a binder fails at runtime.

## Acceptance notes

- [ ] Finite-binder lowering produces a real operator AST (`OpBin`/`OpPauli`
      tree), not only an inspection `dict`, following the shape
      [ADR 0093](../architecture/adr/0093-jordan-wigner-numerical-mapping.md)
      established for Jordan-Wigner: the executable value goes into the same
      environment a hand-written operator uses.
- [ ] `compile_sparse_pauli` resolves `OpIndexed` over a Pauli base, so
      `Z[0]` works wherever `Z(0)` works.
- [ ] The reproduction program above **runs** on the SV simulator **and**
      **emits QASM** — both required, matching the acceptance bar set for
      LISS-0032.
- [ ] Numerical equivalence: the lowered 3-term chain behaves identically to
      the hand-written `Z(0)*Z(1) + Z(1)*Z(2) + Z(2)*Z(3)` equivalent,
      verified by measurement marginals rather than by asserting internal
      representation.
- [ ] `binder_lowering` provenance (source span, binder variable, domain,
      expanded term count, resource check) is retained unchanged — provenance
      stays provenance and is never the executable value.
- [ ] No new surface syntax is introduced by this issue.

## Non-goals

- No change to what the binder body may contain (LISS-0055).
- No notation unification (LISS-0054).
- No `product`, empty-domain, or `where` semantics (LISS-0053, LISS-0056).
- No performance work on expansion.

## Dependencies

- Parent: none
- Depends on: [ADR 0096](../architecture/adr/0096-indexed-operator-and-binder-surface.md) D7 (accepted)
- Related: ADR 0088 (the spec this issue makes true), LISS-0043 (the slice
  that recorded the promise), LISS-0032 (same fix shape, already shipped)
- Blocks: LISS-0053, LISS-0055, LISS-0056 — none of their behaviour is
  observable end-to-end until lowering reaches an execution path

## Adjudicator Decision Points

- [ ] Approve Phase 1 Red.
- [ ] Confirm no ADR is needed: ADR 0096 D7 already decided this, and the
      work is making an accepted spec true rather than choosing among
      alternatives.

## Context

- Included: `compiler/qpex/finite_binder.py`,
  `compiler/qpex/runtime/sparse_pauli.py`,
  `compiler/qpex/runtime/evaluator.py`, `compiler/qpex/backend/qasm/lower.py`,
  ADR 0088, ADR 0093 (fix precedent).
- Omitted: parser and typechecker — this issue adds no syntax.
- Assumption: the correct executable form is the same `OpExpr` shape the
  parser already produces for hand-written operators, so no execution path
  needs a binder-specific branch.

## Verification

- Phase 1 Red: the reproduction program fails `run` and `emit-qasm` for the
  stated reason; `Z[0]` outside a binder fails at runtime.
- Phase 2 Green: both succeed, and match the hand-written equivalent
  numerically.
- Full regression sweep and `python3 tests/spec_verification/run_all.py`
  must stay green.

## Work Notes

- 2026-07-26: Opened from ADR 0096's accepted implementation order, after
  the evidence classification (ADR 0095 Decision 6) established this is a
  spec-implementation divergence rather than a design gap.
