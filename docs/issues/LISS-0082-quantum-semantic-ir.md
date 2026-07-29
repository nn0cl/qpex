# LISS-0082: Quantum Semantic IR

## Metadata

- Local issue ID: LISS-0082
- GitHub issue: not created
- Status: **review** — Slice A complete; Slice B **not complete**: follow-up 1
  closed gaps 1, 2, and 5, gap 4 is decided with no code change, and gap 3
  remains open pending an Architecture Path update; Slice C gated
- Phase: Slice B `phase-3-refactor` done for the approved scope; a Slice B
  follow-up Red is required before Slice B may be called complete;
  Slices C–F remain unauthorized
- Type: semantic IR / quantum domain
- Priority: P0
- Initial planning size: XL
- Current planning size: XL
- Owner/agent: unassigned
- Parent: [WP-0025](../work-plans/WP-0025-staqex-v1-north-star.md) E2 — Semantic IR
- Depends on: [LISS-0075](LISS-0075-linear-quantum-usage.md) **complete**;
  [LISS-0081](LISS-0081-physics-ir-equations-and-operator-algebra.md) **complete**
- Unlocks: [LISS-0083](../work-plans/WP-0025-staqex-v1-north-star.md) Algorithm
  Plan IR; [LISS-0077](../work-plans/WP-0025-staqex-v1-north-star.md) Dynamic QPU
  (also needs 0076 **complete**)
- Related branch: `feature/liss-0082-slice-a-red` (Slice A, merged PR #138);
  `feature/liss-0082-slice-b-red` (Slice B, in progress)
- Authority: [ADR 0106](../architecture/adr/0106-staqex-v1-north-star-language-and-compiler.md)
  D9 / D11; [compiler blueprint §4.3](../architecture/staqex-v1-compiler-blueprint.md);
  [v1 language north star](../specs/staqex-v1-language-north-star.md)
- Plan companion:
  [`staqex-v1-quantum-semantic-ir-plan.md`](../specs/staqex-v1-quantum-semantic-ir-plan.md)
- Detailed contract:
  [`quantum-semantic-ir-contract.md`](../architecture/quantum-semantic-ir-contract.md)
- Proposed architecture decision:
  [ADR 0108](../architecture/adr/0108-quantum-semantic-ir-value-region-contract.md)
- Proposed scale/model decision:
  [ADR 0109](../architecture/adr/0109-quantum-machine-scale-and-model-envelope.md)
- Proposed capacity-horizon decision:
  [ADR 0110](../architecture/adr/0110-optimistic-quantum-capacity-horizon.md)
- Proposed delivery-horizon decision:
  [ADR 0111](../architecture/adr/0111-current-hardware-first-delivery-horizon.md)
- Research evidence:
  [`2026-07-29-quantum-semantic-ir-foundations.md`](../research/2026-07-29-quantum-semantic-ir-foundations.md)

## Summary

Introduce a provider-neutral **Quantum Semantic IR** on the Python Shipping
Kernel. This IR captures **executable finite quantum semantics** after Physics
IR: immutable whole-Joint-state generations over finite acting spaces, explicit
unitary/isometry/channel/measurement region signatures, separated coherent and
dynamic control domains, parameter symbols, linear/ancilla obligations, and
exact-versus-approximation-required markers.

Simulator planning and QPU planning must consume the **same** semantic contract.
No target/provider types appear in this IR. The first implementation is
additive: a new module adjacent to Physics IR, not a big-bang rewrite of the
evaluator or pipeline.

## Acceptance scenarios

1. **Given** a reviewed Physics IR plus finite-carrier evidence, **when** it is
   lowered through `QuantumSemanticInput`, **then** the IR records an ordered
   finite acting space with closed source/upstream provenance and does not
   inspect raw AST, expand gates, or choose a provider.
2. **Given** pure or density Joint-state carriers, **when** transformations are
   represented, **then** each immutable whole-store generation has one producer
   and one consuming path, factor IDs do not imply separability, and
   purity/mixedness remains explicit.
3. **Given** unitary, isometry, channel, or measurement regions, **when** they
   are represented, **then** region kind boundaries remain distinct without
   collapsing into OpenQASM opcodes.
4. **Given** coherent quantum control, compile-time selection, or dynamic
   measurement feedback, **when** lowering runs, **then** coherent control
   remains state-valued, compile-time selection is resolved, and dynamic
   feedback is a dynamic-lane marker rejected from Static Kernel; the marker
   pairs a post-measurement Joint generation with a phase-local token and
   requires one branch merge without defining controller execution.
5. **Given** terminal Static Kernel measurement, **when** it is represented,
   **then** it consumes the relevant final state and produces no reusable
   mid-program classical value or post-measure state use.
6. **Given** linear resource / ancilla obligations, **when** the verifier runs,
   **then** fan-out, use-after-consume, missing discharge, missing provenance,
   or invalid region contracts emit named diagnostics and do not silently
   repair.
7. **Given** a non-exact semantic operation, **when** it is represented,
   **then** it carries `ApproximationRequired` with reason and provenance;
   numerical method, tolerance, bound, resource estimate, and mapping choice
   remain LISS-0083.
8. **Given** simulator and QPU planning consumers, **when** they derive plans,
   **then** neither embeds provider SDK types; unsupported targets fail later
   at ports, not by forking semantics.
9. **Given** a locally attached Personal Quantum Appliance or a modular
   utility-scale target, **when** it consumes the same semantic module,
   **then** region hierarchy remains available, no cloud/deployment assumption
   changes meaning, and bounded target expansion occurs only downstream.
10. **Given** synthetic QP-2 or QS-2 capacity profiles, **when** the semantic
    module is verified, **then** work remains proportional to compact region
    structure and symbolic multiplicity rather than allocating per
    `10^15–10^20` expanded operation.
11. **Given** CH0 or NH5 target profiles, **when** the same semantic module is
    consumed downstream, **then** no current or announced hardware count,
    provider, topology, or error model appears in Semantic IR.

## Non-goals

- no numerical equation solving, state-vector execution, or simulator engines;
- no gate or matrix expansion / circuit synthesis;
- no Jordan–Wigner or other encoding **execution** (decision ledger → LISS-0083);
- no Algorithm Plan IR, verified pass manager, or Logical QPU IR;
- no provider SDK, credentials, network, OpenQASM-as-semantics, or QIR-as-semantics;
- no Equation DTO extensions or auto-extraction (LISS-0116 minimal form stands;
  further work → LISS-0119+);
- no Dynamic QPU controller surface (`dynamic qpu fn` → LISS-0077);
- no existing QPU IR migration;
- no compile-hard diagnostic promotion;
- no private discretization/mapping selection for Physics IR lacking reviewed
  finite evidence; general stage ordering requires follow-on architecture
  review;
- no `compile_source` soft wire unless a separately approved Slice F;
- no Rust mirror (LISS-0070 deferred).
- no local/cloud/facility deployment, power, QEC, decoder, or computation-model
  profile fields in Quantum Semantic IR.

## Proposed slices

| Slice | Scope | Gate |
|---|---|---|
| **A** | Immutable hierarchy-capable semantic IDs, closed provenance, schema-versioned root/region-root references, deterministic root verifier | Phase 1 Red after architecture + phase approval |
| **B** | Finite acting spaces; pure/density Joint-state values; generation-use verifier; no separable-register implication | Separate Red approval |
| **C** | Unitary/isometry/channel signatures and validity obligations | Separate Red approval |
| **D** | Coherent/dynamic control separation; terminal measurement; parameters; ancilla/uncompute obligations | Separate Red approval |
| **E** | Semantic exactness obligations; narrow Physics IR + finite-evidence lowering | Separate Red approval |
| **F** (optional) | Soft `CompileResult` wire | Explicit Adjudicator approval |

Each slice remains additive and provider-neutral. Phase 2 may implement only
reviewed Red assertions; Phase 3 is behavior-preserving cleanup.

## Slice progress

| Slice | Red | Green | Refactor | Evidence |
|---|---|---|---|---|
| **A** | done | done | done | PR #138; [Red trace](../collaboration/traces/2026-07-30-liss-0082-slice-a-red.md), [Green trace](../collaboration/traces/2026-07-30-liss-0082-slice-a-green.md) |
| **B** (approved Red scope) | done | done | done | [Red trace](../collaboration/traces/2026-07-30-liss-0082-slice-b-red.md), [Green/Refactor trace](../collaboration/traces/2026-07-30-liss-0082-slice-b-green.md); `tests/test_quantum_semantic_ir_slice_b_red.py` |
| **B** (contract) | **not complete** — gap 3 open | — | — | [Adjudicator re-review](../collaboration/traces/2026-07-30-liss-0082-slice-b-review.md) |
| **B follow-up 1** (gaps 1, 2, 5) | done | done | done | [Red trace](../collaboration/traces/2026-07-30-liss-0082-slice-b-followup-red.md), [Green/Refactor trace](../collaboration/traces/2026-07-30-liss-0082-slice-b-followup-green.md); `tests/test_quantum_semantic_ir_slice_b_followup_red.py` |
| **B follow-up 2** (gap 3) | blocked on Architecture Path | — | — | approved as option (a), deferred |
| **C**–**F** | not authorized | — | — | — |

Slice B is **not** complete, but only one gap is left. The Adjudicator
re-review of 2026-07-30 opened five gaps
([record](../collaboration/traces/2026-07-30-liss-0082-slice-b-review.md)); of
those, follow-up 1 closed gaps 1, 2, and 5 through Red/Green/Refactor, and
gap 4 was decided with no code change (no ordering field; cycle detection
delegated to the Slice C region graph).

**Gap 3 is the only open item**: removing the bare integer `generation` field,
approved as option (a) but deferred to an Architecture Path update aligning
ADR 0108, the detailed contract, and the Issue/plan, with its own reviewed Red.
On 2026-07-30 the Adjudicator **opened the PR and merge gate** for the
follow-up 1 branch while gap 3 is still open, so the reviewed Slices A/B work
lands on `main` rather than waiting. Gap 3 still gates **calling Slice B
complete** and **starting Slice C**; `generation` remains an unverified field
on `main` until its Architecture Path update and separate Red land.

## Slice B accepted design decisions (2026-07-30)

Adjudicator-approved before Phase 2 Green. These bind the Slice B API surface
already fixed by the reviewed Red assertions.

1. **Provenance** — Slice B DTOs hold `SemanticOrigin` directly instead of
   introducing the contract's `OriginId`. Preserving the Slice A API is the
   priority; migrating to `OriginId` belongs to a later Slice or a follow-up
   Issue.
2. **Root extension** — `QuantumSemanticModule` gains exactly
   `acting_spaces`, `values`, and `value_uses`. No `regions` field and no
   lowering field is added in Slice B.
3. **Producer reference** — `producer_id: SemanticId` is an opaque reference.
   Whether the producer is a well-formed region is Slice C's responsibility.
4. **Diagnostic codes** — Slice B reports only `QSEM_ACTING_SPACE_INVALID`
   (unknown `space_id`, resource/factor arity mismatch, non-positive or
   inconsistent dimension) and `QSEM_VALUE_USE_INVALID` (unknown value,
   missing producer, fan-out, independent factor consumption).

Standing condition: ADR 0108–0111 remain **Proposed**; Slice B proceeds inside
the existing P0 approval boundary, as Slice A did. Region, measurement,
control, lowering, pipeline, and provider work stays out of Slice B.

## Bounded execution readiness

Each approved Slice must be issued as one
[bounded feature execution packet](../architecture/bounded-feature-execution-packet.md).
The packet names the phase, accepted scenarios, exact test paths, allowed
writes, applicable profiles, expected result, and stop conditions. An
architecture ambiguity, required cross-Issue edit, or second failed attempt
stops the code assistant before further mutation.

## Exclusive write paths (initial)

| Path | Role |
|---|---|
| `compiler/staqex/quantum_semantic_ir.py` | **new** — immutable DTOs and verifier; lowering begins in Slice E |
| `tests/test_quantum_semantic_ir_*.py` | Red/Green for this Issue |

**Read-only by default:** `physics_ir.py`, `physics_equation.py`,
`physics_ir_lower.py`, evaluator, QPU adapters.

**Forbidden until Slice F approval:** routine `pipeline.py` edits.

## Adjudicator Decision Points

- [x] Approve Issue body / plan intake (this document + companion plan)
- [x] Authorize Slice A Phase 1 Red only (separate message)
- [x] Confirm out-of-scope list (numerical / gate / JW / QPU / Equation
      extension / 0083 / 0077 behavior / 0084 execution / QPU migration /
      soft wire)
- [x] Confirm module name `quantum_semantic_ir.py` adjacent to Physics IR
- [x] Authorize Slice B Phase 1 Red only (2026-07-30)
- [x] Approve the four Slice B design decisions recorded above (2026-07-30)
- [x] Authorize Slice B Phase 2 Green and Phase 3 Refactor (2026-07-30)
- [x] Re-review Slice B and record the five verification gaps (2026-07-30)
- [x] Decide gap 4 — no ordering field; cycles delegated to Slice C (2026-07-30)
- [x] Decide gap 3 — option (a), remove only the bare `generation` field,
      deferred to Architecture Path (2026-07-30)
- [x] Authorize Slice B follow-up 1 Phase 1 Red only (2026-07-30)
- [x] Approve follow-up 1 Phase 2 Green and Phase 3 Refactor (2026-07-30)
- [x] Review and approve the follow-up 1 Green/Refactor result (2026-07-30)
- [x] Authorize push, PR, and merge of the follow-up 1 branch with gap 3 still
      open (2026-07-30)
- [ ] Architecture Path update for gap 3 (ADR 0108 + detailed contract +
      Issue/plan) with its own reviewed Red
- [ ] Authorize Slice C Phase 1 Red (transformation region signatures)
- [ ] Architecture approval for proposed ADR 0108 and detailed contract
- [ ] Architecture approval for proposed ADR 0109 and machine scale/model
      envelope
- [ ] Architecture approval for proposed ADR 0110 and optimistic capacity
      stress envelope
- [ ] Architecture approval for proposed ADR 0111 and current/NH5 delivery
      envelope
- [ ] Approve later Slices C–F individually

## Design decisions requested (plan intake)

1. Accept blueprint §4.3 as the authoritative vocabulary boundary for this
   Issue.
2. Keep diagnostics non-compile-hard until a later Issue promotes selected
   codes (mirror Physics IR policy).
3. Use immutable whole-Joint-state generations rather than mutable
   qubit/register references; factor IDs do not imply separability.
4. Keep coherent control, resolved compile-time selection, and dynamic
   measurement feedback as distinct semantic domains.
5. Preserve terminal Static Kernel measurement; keep Dynamic QPU behavior in
   LISS-0077.
6. Defer all encoding / approximation **choices** to LISS-0083 even when
   obligations exist on Quantum Semantic IR.
7. Lower only from a narrow Physics IR + reviewed finite-evidence input; never
   fall back to raw AST/`CompilationUnit` or target capability inspection.
8. Keep general discretization/mapping ordering unresolved and fail missing
   finite evidence explicitly rather than selecting a hidden plan.
9. Preserve structured regions/symbolic repetition without eager flattening;
   keep local-to-utility deployment and computation-model profiles downstream.
10. Measure routine verifier complexity against compact structure; never
    require one object, identity, provenance record, or diagnostic per
    expanded operation.

## AI planning record

### AIP-0082-001

- Status: proposed
- Created by: Codex desktop architecture review
- Model/reasoning setting: N/A — exact displayed setting is not exposed in the
  repository artifact
- Created at: 2026-07-30
- Planning size: XL
- Intended route: strong reasoning for architecture; code assistant only for
  one approved bounded Slice and phase
- Intended scope: Slices A–F as independently gated above
- Token estimate/metric: N/A — execution packets are estimated separately
- Confidence: high for boundaries; medium for finite-evidence stage ordering
- Revises/supersedes: none
