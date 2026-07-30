# Staqex v1 Exact Circuit Synthesis and Optimization Contract

## Purpose and authority

This specification defines the provider-neutral exact optimization boundary
for LISS-0089. The LISS-0089 Issue is authoritative for scope, acceptance
scenarios, status, and approval state. ADR 0022 remains the semantic baseline
for denotation preservation and Never Leave the State. LISS-0087 owns verified
pass orchestration; LISS-0082 owns Semantic IR invariants; LISS-0092 and later
Issues own target routing and scheduling.

LISS-0089 is one implementation unit. Cancellation, rotation merging,
commutation, controlled/adjoint specialization, ancilla evidence, and
differential verification are internal review dimensions, not separate Issues,
branches, Red/Green/Refactor cycles, or approval gates.

## Architecture boundary

The pass consumes an immutable provider-neutral operation graph whose inputs
have already passed the Semantic/Plan/verified-pass boundaries. It returns an
immutable operation graph plus an explicit proof witness. It does not emit
provider gates, choose a topology, estimate noisy hardware cost, call a
simulator service, or perform runtime-adaptive selection.

```text
verified Algorithm Plan / operation graph
                 |
                 v
       exact optimization pass
          |              |
          v              v
  transformed graph   proof witness
                 |
                 v
       differential exact oracle / later target projection
```

Candidate implementation files are limited to:

- `compiler/staqex/exact_optimization.py`
- `tests/test_exact_optimization_integrated_red.py`
- synchronized Issue, this specification, WP-0025 references, and a dated
  trace

The existing Kernel PoC remains eager and correct without this pass. Enabling
this track does not add a runtime optimization flag, provider dependency, or
new source-language meaning.

## Immutable contract candidates

Names are provisional until Phase 1 Red review.

| Record | Required meaning |
|---|---|
| `OperationNode` | operation identity, kind, ordered operands, symbolic parameters, and source/Physics/Semantic provenance |
| `OperationGraph` | immutable ordered nodes, roots, repetitions, and schema version; no eager expansion of symbolic repetition |
| `OptimizationCandidate` | transformation family, selected input IDs, proposed output IDs, side conditions, and policy identity |
| `ProofWitness` | law, input/output identities, side-condition evidence, provenance, and exact equivalence claim |
| `OptimizationResult` | transformed graph, witnesses, rejected candidates, diagnostics, and stable before/after evidence |

The pass may reject a candidate without changing the graph. A rejected or
unsupported transformation retains the original provenance and names the
missing proof or prerequisite.

## Exact transformation boundary

The integrated P1 contract covers:

- inverse cancellation only when the adjacent operations and operands are
  exact inverses;
- rotation merging only for the same axis/operand and an algebraically exact
  parameter relation;
- commutation only with a declared exact commutation witness;
- controlled/adjoint specialization only when operand polarity, acting space,
  and adjoint law are explicit; and
- ancilla reuse only after linear lifetime and discharge evidence is closed.

The following are forbidden in this Issue:

- approximate rewrites, tolerance-based equivalence, or numeric near-zero
  cancellation;
- unproved reordering, global commutation guesses, or source-order changes
  without a witness;
- target topology, native gate, calibration, routing, provider SDK, or noisy
  cost selection; and
- silent repair, fallback to an unoptimized graph after a claimed proof, or
  mutation of the source graph.

## Verifier laws and diagnostics

The integrated verifier must reject:

1. a transformed node with missing or changed provenance;
2. a cancellation without exact inverse and operand identity evidence;
3. a rotation merge with mismatched axis, acting space, or symbolic parameter
   law;
4. a commutation or reordering without a closed witness;
5. controlled/adjoint specialization with incomplete polarity or adjoint
   evidence;
6. ancilla reuse before discharge or with a second live consumer;
7. approximate or provider-specific policy presented as exact; and
8. a differential mismatch between bounded exact before/after witnesses.

Diagnostic codes and detail keys are part of the reviewed surface. Red must
name the codes and deterministic ordering before Green.

## Differential evidence and profiles

The first evidence matrix uses provider-neutral deterministic doubles:

| Profile | Role |
|---|---|
| `SIM0_EXACT` | bounded exact before/after equivalence oracle |
| `CH1_DIGITAL_RESEARCH` | compact target-independent digital witness |
| `NH5_NISQ_MODULAR` | symbolic resource and repetition compactness stress |

The differential oracle compares exact observable semantics and retains the
operation/provenance witness. It is not a numerical tolerance oracle and does
not become a provider adapter. `CH1_ANALOG_RESEARCH`, `NH5_FT_GIGA`, and
`NH5_NATIVE_LARGE` are later target/profile work.

## Integrated test contract

One Red suite must cover:

- exact inverse cancellation accepted and witnessed;
- exact same-axis rotation merge accepted and witnessed;
- legal commutation accepted only with a witness;
- controlled/adjoint specialization and ancilla discharge evidence;
- mismatched operands, axes, acting spaces, missing witnesses, live ancilla,
  approximate policy, and provider/routing leakage rejected;
- source order retained when no legal proof exists;
- bounded exact differential equivalence before/after; and
- compact symbolic repetition and deterministic diagnostics/serialization.

Fixtures use repository-local immutable literals and deterministic exact
doubles. No live provider, network, random source, or numerical optimizer is
part of Red or Green.

## Approval and execution

Because ADR 0022 currently holds optimizer implementation, the next approval is
Architecture approval for this narrow exact-pass boundary plus Phase 1 Red.
After approval, the Issue follows one integrated cycle:

1. Architecture + Phase 1 Red;
2. Phase 2 Green minimum exact pass;
3. Phase 3 Refactor and documentation synchronization; and
4. final review, completion packet, CI, and merge.

Any change to denotational semantics, approximation policy, runtime scheduling,
provider selection, or target routing invalidates this contract and requires a
new Architecture Path decision.
