# WP-0093: S02 language expressiveness and selection surface

| Field | Value |
|---|---|
| Status | **Work unit A complete; work unit B complete ([LISS-0321](../issues/LISS-0321-s02-host-domain-and-finite-boundary.md), PR #349 merged); work unit C's ADR ([ADR 0192](../architecture/adr/0192-s02-projector-selection-semantics.md)) Accepted and Kernel slice final-review-ready ([LISS-0322](../issues/LISS-0322-s02-projector-region-semantics.md), not yet merged); work units D, E open** |
| Scope | S02 drug-discovery benchmark and the language boundaries it exposes |
| Parent direction | [State-transformer language review](../architecture/staqex-state-transformer-language-review.md) |
| Related plan | [WP-0092](WP-0092-quantum-mental-model-follow-up.md) |
| Target design | [S02 benchmark design](../specs/staqex-v1-drug-discovery-benchmark-design.md) |
| Acceptance specification | [S02 benchmark specification](../specs/staqex-v1-s02-drug-discovery-benchmark.md) |
| Implementation | Work unit A (`mix`/`controlled`/`when` language surface) shipped (PR #337). Work unit B (Host domain records + finite boundary) implemented, Host-side only, Phase 3 complete on LISS-0321 (final-review-ready). Full S02 domain fixture (classical baselines, resource/provenance report, Kernel-side selection state) remains deferred to work units C–E |

## Goal

Use S02 to improve Staqex's physicist-facing expressiveness without turning
the benchmark into a chemistry framework or a vendor-specific optimizer.
S02 must make the following distinction readable:

```text
classical candidate data
  → explicit finite encoding
  → quantum selection State
  → feasible-subspace restriction
  → objective evolution
  → terminal Outcome
```

## Decisions to preserve

- Existing S01 disaster-response showcase remains unchanged.
- Static Kernel has no classical `if`, `while`, or bare `for` control.
- `State<T>` is never implicitly collapsed.
- Terminal `measure` is the classical result boundary.
- Host owns fixtures, classical baselines, resource reports, and provider
  orchestration.
- S02 starts with an 8–16 candidate synthetic fixture and selection size 2–4.

## Work units

### A — `mix` / `controlled` semantic review

1. Promote `mix` as the canonical probabilistic / classified state
   transformation in the Static Kernel.
2. Specify that `mix` is not coherent quantum control and does not perform
   terminal measurement.
3. Compare the current nested-branch restriction with compositional
   mixture semantics. Do not remove the restriction until flattening,
   exhaustiveness, and diagnostic behavior are specified.
4. Keep coherent control as a separate candidate surface (`controlled` or
   typed `Ctl` operation), never as a reinterpretation of `mix`.
5. Keep post-measurement feed-forward in the named Dynamic QPU lane.

Deliverable: an amended semantic table and breaking migration note under
WP-0092. No compiler change in this unit.

#### Keyword candidates

| Candidate | Appropriate meaning | Assessment |
|---|---|---|
| `when` | State-valued classification / arm mapping | Retire; v1 compatibility is not a constraint |
| `mix` | Incoherent probabilistic mixture | Physically honest for the current MVP denotation; less expressive as a general quantum word |
| `superpose` | Coherent linear combination of alternatives | Good physicist-facing word, but incorrect if it merely denotes the current convex mixture |
| `controlled` | Apply an operation coherently under a quantum control | Best for coherent control; not a direct replacement for classification |
| `span` | Mathematical span / historical Staqex spelling | Already retired; do not restore without a migration decision |

**Working recommendation:** do not overload one keyword with both mixture and
coherent superposition. Replace `when` with `mix` for the current
convex-mixture meaning and use `controlled` (or typed `Ctl`) for coherent
operation control. Reserve `superpose` for a semantics that preserves coherent
relative phase. The migration may be breaking: `when` is removed from the
canonical v2 surface rather than retained as an alias. Existing source must be
rewritten by an explicit migration tool or rejected with a fix-it diagnostic;
the compiler must not silently reinterpret it.

### B — S02 domain and finite boundary — **complete** ([LISS-0321](../issues/LISS-0321-s02-host-domain-and-finite-boundary.md))

1. Define `CandidateId`, `Candidate`, `TargetProfile`, `Constraint`, `Score`,
   and `SelectionProblem` as benchmark/domain records.
2. Define `FiniteDomain<T,N>` or an equivalent explicit finiteization witness.
3. Separate Host input hygiene from quantum selection constraints.
4. Reject missing, duplicate, non-finite, oversized, or unproven finite input.

Deliverable: S02 target specification with schema and fail-closed scenarios.
The schema/scenarios deliverable was already satisfied by the accepted S02
spec (same commit as ADR 0190). Item 1's records, item 2's witness
(`FiniteManifestWitness`, distinct from the Kernel's general `finiteize`
op), and items 3–4's fail-closed Host input hygiene are now implemented,
Host-side only, in `examples/showcase/S02_drug_discovery/host/domain.py`
and `.../finite_boundary.py`. Status: **final-review-ready** (Phase 3
complete; no PR/merge yet) — see LISS-0321 for verification evidence and
the reviewer empathy summary.

### C — Constraint and objective semantics

1. Define hard selection constraints as a feasible-subspace / projector
   contract.
2. Define soft preferences as named, normalized weighted objective terms.
3. Retain penalty Hamiltonian as a later comparison profile, not the only
   meaning of a constraint.
4. Record which constraints were host-validated, projected, or penalized in
   `BenchmarkResult`.

Deliverable: ADR proposal covering `Projector<Selection>` semantics,
constraint lowering, objective normalization, and violation handling.
**ADR complete:** [ADR 0192](../architecture/adr/0192-s02-projector-selection-semantics.md)
**Accepted** (2026-08-05). **Kernel slice complete:**
[LISS-0322](../issues/LISS-0322-s02-projector-region-semantics.md)
implements ADR 0192 Decisions 1–2 in
`_append_selection_projector_region` — `constraint_ref` is now derived
from the actual recognized predicate names, and an unrecognized predicate
fails closed with `S02_UNKNOWN_CONSTRAINT_PREDICATE`. Status:
**final-review-ready** (Phase 3 complete; no PR/merge yet). The Host-side
`BenchmarkResult` disposition fields (ADR 0192 Follow-up item 2) remain a
separate, unstarted Issue, likely folded into work unit E.

### D — Quantum state and observation contract

1. Use `State<Selection<CandidateId>>` as the conceptual quantum carrier.
2. Keep `expect` non-destructive and separate from `measure`.
3. Treat an empty or unverifiable terminal selection as a failed result, not a
   fabricated score.
4. Add resource and provenance metadata at the Host boundary, not as hidden
   Kernel side effects.

Deliverable: observation matrix aligned with WP-0092's `Observable`,
`Projection`, `Observation`, and `Outcome` candidates.

### E — Conformance and implementation gates

1. Write EARS/Gherkin acceptance scenarios only after A–D receive review.
2. Phase 1 Red tests cover encoding, state ownership, no implicit collapse,
   projector feasibility, seeded replay, and target rejection.
3. Phase 2 Green implements the smallest simulator-backed slice.
4. Phase 3 refines source readability and the resource/provenance report.

No `.sqx`, compiler, grammar, or normative language specification changes are
authorized by this work plan alone.

## Candidate language improvements

| Candidate | Priority | Decision posture |
|---|---:|---|
| Explicit finiteization witness | P0 | Required for S02 design |
| `Selection<CandidateId>` library carrier | P0 | Required domain concept; syntax TBD |
| Projector / feasible-subspace type | P1 | Architecture decision required |
| Named normalized objective terms | P1 | Domain library first; avoid new arithmetic syntax |
| Resource/capability witness | P1 | Host DTO and diagnostics |
| Separate coherent-control surface | P1 | Coordinate with WP-0092; no `when` reinterpretation |
| Alternative encodings | P2 | Later profile comparison |
| Lexicographic / Pareto objective | P2 | Later benchmark chapter |

## Approval gates

- **Architecture review:** confirm S02 mission boundary and `mix` /
  `controlled` taxonomy.
- **Specification approval:** accept the finite-domain, projector, objective,
  and observation contracts.
- **Phase 1 approval:** authorize failing conformance tests.
- **Implementation approval:** authorize compiler, grammar, IR, or example
  changes for named Issues only.

## Phase 2 implementation evidence

- `mix` is the canonical state-valued mixture surface; `when` is a hard
  `RETIRED_KEYWORD` diagnostic with no fallback.
- `controlled` is classified as coherent control and is not lowered to
  `Mixture`.
- `project … onto feasible(...)` retains an explicit `ProjectorRegion` witness
  in the quantum semantic boundary.
- `measure` remains the terminal classical result boundary.
- Active examples and affected fixtures were migrated from `when` to `mix`;
  Python verification-harness method names remain unchanged.

## Verification for this planning phase

```text
git diff --check
```

The full S02 domain fixture, host data boundary, objective lowering, and QPU
execution profiles remain outside this implementation batch. The affected
language-surface fixtures were migrated only to keep the deliberate breaking
`when` removal coherent.
