# LISS-0068: QPex v1 normative specification rebaseline

## Metadata

- Local issue ID: LISS-0068
- GitHub issue: not created
- Status: **closed — E0 complete** (Adjudicator approved 2026-07-27); promotion PR is next gate
- Phase: phase-0-design (E0 closed)
- Type: architecture / language specification / conformance
- Priority: P0
- Initial planning size: XL
- Current planning size: XL
- Reclassification reason: not applicable
- Owner/agent: unassigned after design review
- Related branch: `docs/liss-0068-normative-rebaseline`

## Summary

Create one coherent, versioned normative QPex v1 specification before any
north-star lexer, parser, IR, or runtime implementation begins.

The current v0.1 specification remains the shipping conformance target until
this Issue is reviewed. It predates many accepted ADRs and contains stale or
contradictory statements about returns, effect syntax, Param/Dynamic status,
QPU IR, and completed lowering slices.

## Acceptance Notes

The Issue is complete only when:

1. every accepted ADR through ADR 0105 is mapped to a normative section,
   grammar production, diagnostic, acceptance scenario, or explicit
   implementation-only note;
2. all existing language behavior is classified as:
   - preserved in v1;
   - additive v1 extension;
   - deliberate breaking migration;
   - implementation bug;
   - documented deferral;
3. v0.1 contradictions have one named authoritative resolution;
4. the v1 grammar and diagnostic catalog have stable versioning rules;
5. formula-to-source, invalid-source, observable-semantics, provenance, and
   backend-profile acceptance envelopes exist;
6. every breaking surface has a source migration and removal contract;
7. no compiler implementation changes are mixed into the Architecture Path
   review.

## Dependencies

- Parent: [WP-0025](../work-plans/WP-0025-qpex-v1-north-star.md)
- Depends on:
  - ~~Adjudicator architecture review of [ADR 0106](../architecture/adr/0106-qpex-v1-north-star-language-and-compiler.md)~~ **Accepted with conditions** (2026-07-27)
  - accepted [ADR 0095](../architecture/adr/0095-design-horizon-ideal-form-first.md)
- Blocks: LISS-0069 through the implementation roadmap in WP-0025
- Related:
  - [current v0.1 specification](../specs/qpex-language-specification.md)
  - [v1 north-star proposal](../specs/qpex-v1-language-north-star.md)
  - [rebaseline register slice 1](../specs/qpex-v1-normative-rebaseline-register.md)
  - [§1–§2 outline slice 2](../specs/qpex-v1-normative-outline-s12.md)
  - [diagnostic catalog slice 3](../specs/qpex-v1-diagnostic-catalog.md)
  - [acceptance envelopes slice 4](../specs/qpex-v1-acceptance-envelopes.md)
  - [migration matrix slice 5](../specs/qpex-v1-migration-matrix.md)
  - [E0 adjudicator completion trace](../collaboration/traces/2026-07-27-liss-0068-e0-adjudicator-completion.md)
  - [compiler blueprint](../architecture/qpex-v1-compiler-blueprint.md)

## Adjudicator Decision Points

- Accept, revise, or reject ADR 0106 as the v1 target.
- Confirm that Unicode Dirac/tensor notation is the canonical v1 source and
  therefore a migration rather than a permanent compatibility alias.
- Confirm the explicit Static Kernel versus `dynamic qpu fn` boundary.
- Confirm that the Python Kernel remains the reference during an incremental
  Rust migration rather than authorizing a big-bang rewrite.
- Approve the exact scope of a later Phase 1 Red conformance slice. This Issue
  does not infer that approval.

## Context

- Included:
  - normative v0.1 specification and grammar outline;
  - QPex axioms and physicist-DX documents;
  - accepted Static/Parametric/Dynamic, Workflow, QPU IR, operator, binder,
    resource, Host submit, and multi-register ADRs;
  - compiler AST, Symbolic IR, QPU IR, pipeline, and Host module boundaries;
  - canonical open-work register and theory-to-QPU plans;
  - official OpenQASM, QIR, Catalyst, CUDA-Q, IBM, AWS, Q#, Silq, Qunity, and
    PennyLane sources listed in the research companion.
- Omitted:
  - provider credentials and private data;
  - generated reports and build artifacts;
  - full implementation-file review unrelated to semantic boundaries;
  - vendor SDK source code;
  - detailed performance benchmarking, which belongs to later technology
    Issues.
- Assumptions:
  - accepted ADRs remain authoritative until explicitly superseded;
  - Python remains the shipping Kernel;
  - Rust remains the recorded long-term implementation target;
  - no provider or external compiler dependency is selected by this Issue.

## AI Planning Records

### AIP-0068-001

- Status: proposed
- Created by:
  - Agent/environment: Codex desktop
  - Model as displayed: GPT-5
  - Reasoning setting as displayed: not exposed
- Created at: 2026-07-27
- Planning size: XL
- Intended execution route: Architecture Path for reconciliation; Feature Path
  only after a reviewed conformance slice exists
- Intended scope: normative inventory, versioning, compatibility matrix,
  grammar/diagnostic alignment, and acceptance envelopes
- Estimated token range: N/A
- Estimated token midpoint: N/A
- Token metric: unavailable in the environment
- Estimation basis: N/A
- Assumptions: listed in Context
- Confidence: high that rebaseline is prerequisite; medium on final migration
  details pending Adjudicator review
- Revises: none
- Revision reason: none
- Superseded by: none

## References

- [OpenQASM 3.1 specification](https://openqasm.com/versions/3.1/)
  (fetch-verified 2026-07-27)
- [QIR overview](https://learn.microsoft.com/en-us/azure/quantum/concepts-qir)
  (fetch-verified 2026-07-27)
- [Catalyst architecture](https://docs.pennylane.ai/projects/catalyst/en/stable/dev/architecture.html)
  (fetch-verified 2026-07-27)
- [Silq paper/project page](https://www.sri.inf.ethz.ch/publications/bichsel2020silq)
  (fetch-verified 2026-07-27)
- [Qunity POPL 2023](https://popl23.sigplan.org/details/POPL-2023-popl-research-papers/32/Qunity-A-Unified-Language-for-Quantum-and-Classical-Computing)
  (fetch-verified 2026-07-27)

## Work Notes

- 2026-07-27: Architecture intake found that the v0.1 specification header
  stops at ADR 0069 even though accepted language decisions now extend through
  ADR 0105.
- 2026-07-27: `qpex-language-axioms.md` still says `return` is rejected while
  ADR 0068 and the normative v0.1 specification require explicit terminal
  `return` in ordinary functions.
- 2026-07-27: the v0.1 specification still labels Parametric/Dynamic lanes as
  proposed/non-conforming despite reviewed implementation boundaries.
- 2026-07-27: architecture status prose includes historical “Phase 1 remains”
  descriptions for features whose Issue/ADR records report Phase 3 review.
- These are specification-state defects to reconcile, not evidence that the
  implemented semantics should be discarded.
- 2026-07-27: slice 5 delivered — [`qpex-v1-migration-matrix.md`](../specs/qpex-v1-migration-matrix.md).
  **LISS-0068 E0 documentation batch complete.**
- 2026-07-27: Adjudicator E0 review **approved with comments**; stale cross-refs
  (F-01–F-05) reconciled. Next: v1 spec promotion PR; then LISS-0069 / LISS-0071
  per matrix §7.

## Verification

- Documentation-only Architecture Path task.
- Planned checks: all referenced paths/IDs, Markdown/link scan,
  `git diff --check`, and confirmation that no source/test file changed.
