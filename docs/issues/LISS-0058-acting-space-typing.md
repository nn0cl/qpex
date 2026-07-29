# LISS-0058: Acting-space typing — replace max-site-index inference

## Metadata

- Local issue ID: LISS-0058
- GitHub issue: none
- Status: **Complete**
- Phase: Feature Path — Phase 1 Red → Phase 2 Green → Phase 3 Refactor complete
- Type: type system / compiler context
- Priority: P2
- Initial planning size: XL
- Current planning size: XL
- Reclassification reason: n/a
- Owner/agent: Codex
- Related branch: `codex/liss-0058-refactor`

## Summary

Staqex currently infers how many qubits an operator acts on by **scanning the
expression for the maximum Pauli site index**
(`runtime/hamiltonian.py`'s `op_n_qubits`, and the equivalent logic in
`backend/qasm/lower.py`). This is structurally fragile: the operator's
acting space is recovered from its syntax rather than carried by its type or
by the compilation context.

[ADR 0096](../architecture/adr/0096-indexed-operator-and-binder-surface.md)
D12 accepted only the *minimal* context-determined path that empty-domain
identities need (LISS-0056), and recorded replacing the inference in general
as a required follow-up. This issue is that follow-up. Its Architecture Path
is now recorded in [ADR 0102](../architecture/adr/0102-acting-space-typing.md);
Phase 1 Red and Phase 2 Green are now complete; Phase 3 Refactor remains
separately gated.

## Known symptoms of the current approach

Each of these is the same root cause, not separate bugs:

| Case | Current behaviour |
|---|---|
| Expression with no site indices (empty binder identity) | falls back to **1 qubit**, silently wrong in a larger system — the trigger for ADR 0096 D9/D12 |
| Expression containing only identity operators (`I`) | same fallback; no site to infer from |
| System with **unused** high qubits | inferred size is the highest *used* site, not the declared system size |
| System with **several registers** | a single integer qubit count cannot express which register a site belongs to |
| Operator passed across a function boundary | acting space must be re-derived at each use site rather than travelling with the value |

Only the first is addressed by LISS-0056's minimal mechanism.

## Design questions (resolved by ADR 0102 unless explicitly deferred)

- Does the acting space belong to the **operator's type**
  (e.g. `Operator<Register>` / `Operator<4>`), to the **compilation
  context**, or to both?
- How does it interact with the already-normative `QubitRegister<N>` static
  Hilbert surface (ADR 0069 / LISS-0029), which declares system shape today?
- Multi-register systems: how is a site's owning register named, and is that
  surface syntax or inference?
- How much of this is a **breaking** change to existing operator-typed
  programs? Under ADR 0095 Decision 2 this is the question that decides
  whether the work can be deferred at all: if adopting acting-space typing
  later would force a re-spelling of operator declarations, it should be
  decided sooner rather than later.
- Does the existing dimension/`Dim` machinery (`compiler/staqex/dimensions.py`)
  interact, or is acting space an orthogonal axis?

## Non-goals

- Anything LISS-0056 already covers (the minimal empty-identity path).
- SI dimension extension — a separate axis, tracked in ADR 0096's deferred
  list.

## Dependencies

- Parent: none
- Depends on: **LISS-0056** (its minimal mechanism is the first concrete
  data point about what context-determined acting space needs)
- Related: ADR 0096 D12 (which recorded this follow-up), ADR 0069 /
  LISS-0029 (`QubitRegister<N>` static Hilbert surface), LISS-0027
  (`Param<T>` typing precedent)
- Blocks: nothing currently scheduled

## Adjudicator Decision Points

- [x] Schedule this as the next acting-space architecture slice.
- [x] An ADR is required before Phase 1 Red: [ADR 0102](../architecture/adr/0102-acting-space-typing.md)
      fixes the semantic boundary while leaving the final multi-register
      surface deferred.
- [x] Prioritise acting-space typing ahead of indexed coefficient families,
      dependent ranges, and SI-dimension extensions because it is a shared
      correctness boundary for execution.

## Context

- Included (for the eventual design): `compiler/staqex/runtime/hamiltonian.py`
  (`op_n_qubits`, `op_space`, `hop_basis_dim`),
  `compiler/staqex/backend/qasm/lower.py`, `compiler/staqex/static_hilbert.py`,
  ADR 0069, LISS-0029.
- Omitted: provider mapping, and the final
  multi-register surface.
- Decision captured in ADR 0102: acting space is carried by the operator
  value, with an enclosing register/context as the secondary resolution
  source; no execution path may use syntax-derived or one-qubit fallback.

## Verification

- Architecture review and option selection completed through ADR 0102.
- Phase 1 Red acceptance tests cover the declared single-register shape,
  identity-only operators, unused high qubits, function boundaries,
  context-free rejection, and the deferred multi-register boundary.
- Phase 2 Green uses the declared `Operator<QubitRegister<N>>` shape during
  Hamiltonian evolution and rejects an untyped site-free identity instead of
  applying a one-qubit fallback.
- Phase 3 Refactor centralizes operator-shape extraction so the finite-binder
  validation and simulator consume one acting-space interpretation; the
  acceptance assertions remain unchanged.

## Work Notes

- 2026-07-26: Opened from ADR 0096 D12. Identified by the independent design
  review, which correctly recognised that the empty-identity problem is a
  *symptom* of syntax-derived acting space rather than an isolated edge case.
- 2026-07-27: Architecture Path review accepted ADR 0102.
- 2026-07-27: Phase 1 Red added the acting-space acceptance boundary.
- 2026-07-27: Phase 2 Green records declared single-register shapes on
  operator values, uses them during Hamiltonian evolution, and emits an
  explicit diagnostic for context-free site-free identities. The
  multi-register surface remains an intentional parse-level rejection.
- 2026-07-27: Phase 3 Refactor centralized the shared operator-shape helper,
  refreshed the acceptance-test documentation, and synchronized this issue with the
  reviewed completion state. Multi-register/provider mapping remains deferred.
