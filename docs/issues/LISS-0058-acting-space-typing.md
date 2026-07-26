# LISS-0058: Acting-space typing — replace max-site-index inference

## Metadata

- Local issue ID: LISS-0058
- GitHub issue: none
- Status: proposed — **design intake only, not scheduled**
- Phase: phase-0-design (no ADR yet; needs its own Architecture Path decision)
- Type: type system / compiler context
- Priority: P2
- Initial planning size: XL
- Current planning size: XL
- Reclassification reason: n/a
- Owner/agent: TBD
- Related branch: none yet

## Summary

QPex currently infers how many qubits an operator acts on by **scanning the
expression for the maximum Pauli site index**
(`runtime/hamiltonian.py`'s `op_n_qubits`, and the equivalent logic in
`backend/qasm/lower.py`). This is structurally fragile: the operator's
acting space is recovered from its syntax rather than carried by its type or
by the compilation context.

[ADR 0096](../architecture/adr/0096-indexed-operator-and-binder-surface.md)
D12 accepted only the *minimal* context-determined path that empty-domain
identities need (LISS-0056), and recorded replacing the inference in general
as a required follow-up. This issue is that follow-up. It needs its own
Architecture Path decision and is **not scheduled**.

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

## Design questions (none decided)

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
- Does the existing dimension/`Dim` machinery (`compiler/qpex/dimensions.py`)
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

- [ ] Whether to schedule this at all, and when. It is deliberately opened
      unscheduled so the weakness is recorded rather than rediscovered.
- [ ] Whether an ADR is required before Phase 1 Red — the author's
      assessment is **yes**: this is a type-system change with several
      genuine alternatives, not a single unambiguous fix.
- [ ] Priority relative to the ADR 0096 deferred list (indexed coefficient
      families, dependent ranges, SI dimensions).

## Context

- Included (for the eventual design): `compiler/qpex/runtime/hamiltonian.py`
  (`op_n_qubits`, `op_space`, `hop_basis_dim`),
  `compiler/qpex/backend/qasm/lower.py`, `compiler/qpex/static_hilbert.py`,
  ADR 0069, LISS-0029.
- Omitted: implementation of any option — no option is favoured by this
  issue.
- Assumption: the eventual answer carries acting space with the value rather
  than re-deriving it, but the mechanism (type parameter vs context vs both)
  is genuinely open.

## Verification

- Architecture review and option selection first; no Phase 1 Red before an
  accepted ADR.
- Once designed: the five symptom rows above become regression cases, and in
  particular a site-free operator in a multi-qubit system must never resolve
  to one qubit.

## Work Notes

- 2026-07-26: Opened from ADR 0096 D12. Identified by the independent design
  review, which correctly recognised that the empty-identity problem is a
  *symptom* of syntax-derived acting space rather than an isolated edge case.
