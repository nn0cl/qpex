# LISS-0056: Empty-domain identity elements and acting-space determination

## Metadata

- Local issue ID: LISS-0056
- GitHub issue: none
- Status: Phase 3 complete
- Phase: Phase 3 reviewed (implemented and merged in PR #37)
- Type: language semantics + typed symbolic value
- Priority: P2
- Initial planning size: L
- Current planning size: L
- Reclassification reason: n/a
- Owner/agent: TBD
- Related branch: `codex/liss-0056-empty-domain-red`

## Summary

Give empty binders a defined meaning — the identity element of the fold —
rather than an error, per
[ADR 0096](../architecture/adr/0096-indexed-operator-and-binder-surface.md)
D9, and add the minimal acting-space determination that makes this safe
(D12).

The subtlety, and the reason this is its own issue: an identity is
well-defined once its *algebra* is fixed, but its concrete matrix dimension
is not. Materialising it eagerly would hit the current qubit-count
inference, which scans an expression for the maximum Pauli site index —
an empty expression has no sites, so the existing fallback silently yields
**one qubit**. In a 4-qubit system that is a silently wrong operator, which
is precisely what ADR 0095 forbids. The design therefore keeps the identity
**symbolic** until the acting space is known.

## Scope

- `Index<a..b>` with $a > b$ denotes an **empty domain**, never reverse
  iteration.
- Empty `sum` yields the **additive identity**; empty `product` yields the
  **multiplicative identity**.
- The identity is a **typed symbolic** `Zero` / `Identity` value, not an
  immediately materialised matrix.
- It materialises when the acting space is determined from the expected type
  or the surrounding system/register declaration.
- Reaching matrix construction, simulation, or OpenQASM emission with the
  acting space still undetermined is a **hard diagnostic**. A one-qubit
  fallback is forbidden.
- A statically detectable $a > b$ range emits a **non-hard lint diagnostic**
  (likely typo), not a compile error. Hard `BINDER_DOMAIN_ERROR` is retained
  for genuinely malformed ranges.
- The body is **name-resolved and type-checked even when the domain is
  empty**, so a later constant change cannot suddenly surface a latent error
  in a body that was never checked.
- A `where` guard that excludes every tuple yields the same identity as an
  empty range — one case, not two (D5).

## Acceptance notes

- [x] `sum (i in Index<3..1>) { Z[i] }` yields an additive identity, and
      `product (i in Index<3..1>) { Z[i] }` a multiplicative identity, both
      without a hard diagnostic.
- [x] Both are **symbolic** immediately after lowering — a test asserts the
      value is not yet a fixed-dimension matrix.
- [x] Given a surrounding `QubitRegister<4>`, the identity materialises at
      4 qubits, not 1. A test asserts the dimension explicitly, because the
      pre-existing failure mode was a silent single qubit.
- [x] With the acting space undeterminable, `run` and `emit-qasm` each
      produce a hard, **actionable** diagnostic naming what to specify
      (e.g. "cannot determine the space this identity acts on; specify the
      register or system size").
- [x] A literal empty range yields a **warning** and still compiles
      (`compiled.ok is True`), distinguishable from a malformed range which
      remains a hard error.
- [ ] An empty binder whose body contains an undefined name or a type error
      still reports that error. **Follow-up gap: body diagnostics are not yet
      preserved for an empty executable binder.**
- [ ] A `where` guard excluding everything behaves identically to an empty
      range. **Follow-up gap: the current guard path does not emit the empty
      domain warning.**
- [x] Adding a symbolic identity to a concrete operator (`Zero + Z[0]`)
      behaves as the algebraic identity requires.

## Non-goals

- **Replacing qubit-count inference in general** — LISS-0058. This issue
  adds only the minimal context-determined path D9 needs.
- Dependent/computed ranges (deferred by ADR 0096, together with the
  endpoint integer and overflow question).
- Body expressiveness (LISS-0055).

## Dependencies

- Parent: none
- Depends on: **LISS-0052** (execution wiring), **LISS-0053** (recursive
  lowering pass). **LISS-0055** is preferred first so the identity
  interacts with the final body grammar rather than the narrow one.
- Related: ADR 0096 D9/D11/D12, ADR 0095 (no silent wrong results),
  **LISS-0058** (the general acting-space follow-up this issue's minimal
  form anticipates)
- Blocks: nothing scheduled

## Adjudicator Decision Points

- [x] Approve the diagnostic code names:
      `IDENTITY_ACTING_SPACE_UNDETERMINED` is hard;
      `EMPTY_BINDER_DOMAIN_WARNING` is non-hard.
- [x] Keep the symbolic identity internal (a compiler/IR value). This issue
      introduces no user-writable `Zero` or `Identity` literal.

### Adjudicator decision record (2026-07-27)

The compiler must not apply an implicit acting-space or one-qubit fallback.
An empty range may continue with a non-hard warning because its mathematical
identity is well-defined, but materialisation, simulation, and OpenQASM
emission must stop with `IDENTITY_ACTING_SPACE_UNDETERMINED` until the acting
space is explicit. The identity remains an internal symbolic IR value; no
surface `Zero` or `Identity` constructor is added.

## Context

- Included: `compiler/staqex/finite_binder.py`,
  `compiler/staqex/ast_nodes.py` (a typed symbolic identity node),
  `compiler/staqex/runtime/hamiltonian.py` (`op_n_qubits`, the inference whose
  fallback causes the silent single qubit),
  `compiler/staqex/runtime/sparse_pauli.py`, `compiler/staqex/pipeline.py`
  (hard vs non-hard diagnostic registration — `_HARD_CODES`).
- Omitted: the general acting-space redesign (LISS-0058).
- Assumption: a non-hard diagnostic channel is sufficient for the lint
  warning. Verified: `pipeline.py` computes `ok` as "no diagnostic in
  `_HARD_CODES`", so a code omitted from that set is a warning.
- Assumption: expected type or an enclosing register/system declaration is
  always available in the cases this issue must serve. If a legitimate case
  has neither, the hard diagnostic is the correct outcome rather than a
  guess.

## Verification

- Phase 1 Red → Phase 2 Green → Phase 3 reviewed: the implemented slice is
  covered by `tests/test_liss0056_empty_domain_identity_red.py` and merged in
  PR #37 (`aada5e4`).
- The two unchecked acceptance notes above remain explicit follow-up gaps;
  they are not silently reclassified as complete.
- Full regression sweep and spec verification were green for the merged
  implementation.

## Work Notes

- 2026-07-26: Opened from ADR 0096 D9/D12. The symbolic-until-known design
  came from the independent design review, which correctly identified that
  requiring a dimension up front (the author's original proposal) was
  stronger than the mathematics needs: the identity has meaning once its
  algebra is fixed, and only materialisation needs the space.
- 2026-07-27: Synchronized the issue with the already merged implementation
  (PR #37). The general acting-space redesign remains LISS-0058; the two
  unchecked acceptance notes are recorded as follow-up gaps rather than
  expanded into this completed slice.
