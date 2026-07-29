# ADR 0108: Quantum Semantic IR value and region contract

## Status

**Proposed** (2026-07-29). Requires Adjudicator architecture approval.

No implementation, phase transition, or acceptance is implied by this draft.

Companions:

- [LISS-0082](../../issues/LISS-0082-quantum-semantic-ir.md)
- [Quantum Semantic IR contract](../quantum-semantic-ir-contract.md)
- [ADR 0106](0106-staqex-v1-north-star-language-and-compiler.md)
- [ADR 0109](0109-quantum-machine-scale-and-model-envelope.md) (**Proposed**)
- [ADR 0111](0111-current-hardware-first-delivery-horizon.md) (**Proposed**)

## Context

ADR 0106 and the compiler blueprint place a provider-neutral Quantum Semantic
IR between Physics IR and Algorithm Plan IR. The existing plan names finite
acting spaces, transformation regions, control, resources, parameters, and
exactness, but does not yet prevent several semantic leaks:

- mutable qubit references could replace state-valued meaning;
- coherent control, compile-time selection, and measurement feedback could be
  collapsed into one ambiguous control node;
- mid-program measurement could leak into Static Kernel;
- approximation methods and budgets could move upstream from Algorithm Plan;
- lowering could read source AST or provider capabilities directly.

## Dependency adoption evidence

No new runtime or build dependency is proposed. MLIR, QSSA, QIRO, QIR, and
OpenQASM are research inputs only; LISS-0082 does not adopt their libraries or
formats.

## Proposed decision

1. Quantum Semantic IR uses immutable **Joint-state-value semantics**. A
   quantum value identifies the whole Joint-store generation over a finite
   acting space. Factor/resource IDs identify coordinates and ownership inside
   that value; they do not imply separability. No value is a physical qubit,
   pointer, mutable register, or provider handle.
   1a. **The quantum value identity *is* the generation.** `QuantumValueId` /
   `value_id` alone denotes one immutable whole-Joint-state generation. The IR
   carries **no separate generation field** — no integer counter, sequence
   index, version number, or `lineage_id + index` pair. A bare counter would
   assert a total order the IR does not have and cannot verify, and it would
   flatten branching, merging, and hierarchical regions into a running number
   before the region graph exists (see §"Rejected: explicit generation
   numbering"). Ordering between generations, where it is ever needed, is a
   property of the producer/consumer region graph, not of a stored number.
2. The verifier enforces one producer and one consuming path per quantum value
   generation. Fan-out, use-after-consume, and implicit ancilla discard are
   invalid.
3. `Unitary`, `Isometry`, `Channel`, `Measurement`, `CoherentControl`, and
   `DynamicControl` are distinct region contracts with explicit carrier and
   acting-space signatures.
4. Compile-time selection is resolved before Quantum Semantic IR. Coherent
   control remains state-valued. Measurement feedback is valid only in the
   Dynamic QPU lane and remains behaviorally owned by LISS-0077.
5. Static Kernel measurement is terminal and consumes the relevant state.
   It does not create a reusable mid-program classical value.
   Dynamic measurement instead declares a correlated post-measurement Joint
   state and phase-local token pair; neither may escape or be used
   independently, and branch flow must return one merged Joint generation.
6. Semantic exactness is either `Exact` or
   `ApproximationRequired(obligation, reason, provenance)`. Method, tolerance,
   bound, resource estimate, and target choice belong to Algorithm Plan or
   later IR.
7. Lowering consumes a narrow finite-evidence contract over Physics IR. It may
   not inspect raw AST/CompilationUnit, evaluator state, provider capability,
   files, network, or adapter objects.
8. Every semantic node has deterministic identity and closed provenance.
   Invalid modules receive named diagnostics and are never silently repaired.
9. LISS-0082 lowers only source-native or already-reviewed finite evidence.
   General discretization/mapping stage ordering remains an explicit follow-on
   architecture decision; missing evidence is diagnosed, never privately
   selected.

## Consequences

Positive:

- Never Leave the State becomes structurally inspectable.
- Static and adaptive execution cannot be confused by a generic control node.
- Dynamic feedback retains explicit Joint-state continuity and correlation.
- Simulator and QPU paths retain one semantic source of truth.
- Algorithm Plan remains the owner of realization and approximation choices.
- The Python and future Rust implementations can share a versioned contract.

Negative:

- DTOs and verification are more explicit than a compact instruction list.
- Lowering must provide finite carrier and linear evidence instead of reaching
  back into source objects.
- General channels, dynamic feedback, and proof-producing transformations
  remain incomplete until their own Issues land.

## Rejected alternatives

- **Mutable qubit/register references:** lower-level realization identity,
  unsuitable as Staqex semantic identity.
- **One generic transformation/control node:** permits illegal combinations
  and moves language laws into convention.
- **OpenQASM or QIR as Semantic IR:** target/interchange constraints would
  become source semantics.
- **Approximation policy in Semantic IR:** would absorb LISS-0083 and couple
  meaning to a chosen realization.
- **Dynamic feedback in Static Kernel:** violates terminal measurement and
  Never Leave the State.
- **Explicit generation numbering** (a bare integer `generation` field on each
  carrier): rejected. It duplicates `value_id`, which already denotes exactly
  one immutable generation, while asserting a total order the IR neither has
  nor verifies. Nothing in the language requires generations to be comparable,
  and a stored number invites consumers to infer a schedule that Semantic IR
  deliberately leaves to later planning.
- **`lineage_id` plus a per-lineage generation index:** rejected for the same
  reason and one more. Defining "lineage" before the region graph exists would
  force branching, merging, and hierarchical regions into a single running
  number, contradicting the no-eager-flattening law. If ordering evidence ever
  proves necessary, it belongs to the Slice C region graph, where producers and
  consumers have meaning, not to the value DTO.

## Follow-on if accepted

1. Record acceptance date and Adjudicator evidence.
2. Authorize LISS-0082 Slice A Phase 1 Red separately.
3. Keep LISS-0077, LISS-0083, LISS-0084, and target migrations as separate
   review units.
4. Authorize the LISS-0082 gap 3 Phase 1 Red that removes the shipped bare
   integer `generation` field, bringing the Kernel back in line with §1a. The
   field shipped in Slice B before this clarification existed.
