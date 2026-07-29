# LISS-0082 architecture design deepening trace

- Date: 2026-07-29
- Branch: `codex/liss-0082-design-deepening`
- Operating path: Architecture Path
- Current phase: Phase 0 design intake / architecture review preparation
- Implementation permission: **none**
- Approved scope: inspect current project documents and source, research public
  primary sources, and update/add LISS-0082 design documents
- Post-review required: Adjudicator architecture approval, followed by a
  separate Slice A Phase 1 Red approval

## Design intake

```markdown
[DESIGN CHECK]
- Scope and expected behavior: deepen the Quantum Semantic IR design across
  compiler stages while preserving Never Leave the State, provider neutrality,
  and Issue/phase ownership.
- Specifications and files inspected: AGENTS.md; architecture quickstart and
  readiness; language axioms; physicist/DX harmony; ADR 0106/0107; compiler
  blueprint; WP-0025; LISS-0080/0081/0082; current HIR, Physics IR, lowering,
  pipeline, and QPU IR code.
- Component boundaries, ports/adapters, and VO/DTO candidates when applicable:
  immutable domain DTOs and pure verifier/lowering; no external-resource
  adapters. Detailed candidates are in the architecture contract.
- Applicable constraints: terminal Static measurement; static shape; linear
  state use; no hidden realization choice; deterministic provenance; one
  language across Python and future Rust.
- Decisions, assumptions, and unresolved ambiguities: ADR 0108 remains
  Proposed. Finite evidence enters through a narrow input; eventual upstream
  storage is unresolved. Dynamic behavior remains LISS-0077.
- Included and omitted AI context: included relevant repository artifacts and
  primary public research; omitted provider SDKs, credentials, unrelated code,
  and opcode catalogs.
- Task routing (model/assistant/tool): architecture synthesis by agent;
  deterministic repository/diff checks; web research limited to primary
  technical sources.
- Input/output evidence contract when AI output is involved: cited artifacts
  in; reviewable proposed design and explicit inferences out; no hidden
  reasoning or generated execution evidence.
- Verification plan: links, terminology/status synchronization, forbidden
  boundary search, and diff checks; no source/test execution.
```

## Repository findings

- Physics IR is immutable and provenance-bearing but currently carries only a
  minimal subset of finite carrier evidence.
- Physics lowering is softly wired into `compile_source`; LISS-0082 must not
  repeat AST-adjacent lowering or modify that wire before its optional final
  slice.
- HIR already exposes linear consume evidence and phase/effect diagnostics.
- Existing QPU IR is source-adjacent. LISS-0082 does not migrate it, but the
  future migration must derive from verified semantic/plan contracts.
- LISS-0082 unlocks LISS-0083 and LISS-0077 and must not absorb their behavior.

## External evidence

Primary sources and the Adopt/Adapt/Reject synthesis are recorded in
[`docs/research/2026-07-29-quantum-semantic-ir-foundations.md`](../../research/2026-07-29-quantum-semantic-ir-foundations.md).

The evidence supports immutable value flow, operation-owned typed regions,
separate terminal/adaptive measurement capabilities, declarative uncompute
obligations, and separation of static shape from linear runtime values. These
are inferences applied under Staqex's accepted axioms, not imported semantics.

## Resulting proposed decisions

1. Whole-Joint-state generations replace mutable qubit/register references;
   factor/resource IDs do not imply separability.
2. Unitary, isometry, channel, measurement, coherent control, and dynamic
   control have distinct signatures.
3. Static Kernel terminal measurement and Dynamic QPU feedback are separate
   lanes; Dynamic feedback preserves a correlated post-measurement Joint state
   and phase-local token until one merged Joint generation.
4. Approximation need is semantic; method, tolerance, bound, and resources are
   Algorithm Plan decisions.
5. Lowering reads a narrow Physics IR + finite-evidence contract, not AST,
   evaluator, provider, or adapter state.
6. Deterministic identity, closed provenance, and no-silent-repair verifier
   behavior are mandatory.
7. General continuous/mapping-dependent lowering remains blocked on a
   follow-on stage-ordering decision; LISS-0082 diagnoses missing finite
   evidence.

## Changed artifacts

- added detailed architecture contract;
- added Proposed ADR 0108;
- added primary-source research note;
- refined LISS-0082 Issue and slice plan;
- synchronized WP-0025, architecture navigation, and open-work register.

## Stop condition

Stop after documentation verification. Do not create tests, implementation,
pipeline wiring, or accepted ADR status. Request Adjudicator architecture
review.
