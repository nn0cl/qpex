# LISS-0018: Numerical and physical representation follow-ups

## Metadata

- Local issue ID: LISS-0018
- GitHub issue: none
- Status: **Phase 3 reviewed; numeric policy slice complete**
- Phase: `phase-3-refactor`
- Type: architecture + numerical semantics
- Priority: P2
- Initial planning size: L
- Current planning size: TBD
- Reclassification reason: grouped related technology evaluations before implementation.
- Owner/agent: TBD
- Related branch: none yet

## Summary

Resolve the remaining representation questions: SI dimensions beyond `(L, M,
T)`, continuous PDF/Monte Carlo samples, exact rational versus `f64` masses,
and numeric literal versus `dirac` sugar.

## Acceptance Notes

- [ ] Each representation has an explicit scope or is rejected/deferred.
- [ ] Precision, normalization, sampling, and serialization policies are recorded.
- [ ] Dimension expansion does not change existing accepted programs silently.
- [ ] Numeric literal lifting has a normative rule.
- [ ] Separate follow-on Issues are created if the scope cannot remain unified.

## Phase 0 design resolution

- MVP storage remains dependency-free `f64` / complex `f64` pairs through the
  existing `runtime/matrix.py` boundary.
- Exact rational arithmetic is not a Kernel runtime mode; literal provenance
  may be retained without changing evaluation representation.
- Tolerances are contract-specific: PMF `1e-9`; density, Kraus, POVM, and
  Lindblad physical guards `1e-12`.
- Tolerances validate and diagnose; they never authorize silent normalization,
  clipping, or repair.
- Continuous PDFs and Monte Carlo samples remain outside Kernel values and
  enter only through a future port or explicit LISS-0036 discretization.
- Default Host results do not expose raw matrices; numeric provenance may
  identify representation and tolerance policy.

See [ADR 0076](../architecture/adr/0076-numeric-representation-policy.md) and
[WP-0015](../work-plans/WP-0015-numeric-representation-policy.md).

## Phase 1 Red record

- Added [`test_numeric_representation_policy_red.py`](../../tests/test_numeric_representation_policy_red.py).
- The three policy fixtures are Red until the representation constants and
  non-repair validation boundary exist.
- No production implementation was changed in this phase.

## Phase 2 Green record

- Added the dependency-free `runtime/numeric_policy.py` boundary with `f64`
  and `complex-f64` representation names.
- Added separate PMF and physical tolerance constants.
- Added non-repair validation that rejects invalid values without normalize,
  clip, or silent correction.
- Density and Lindblad physical tolerance aliases now use the shared policy.
- The three reviewed policy fixtures pass; continuous PDFs and exact arithmetic
  remain deferred.

## Phase 3 review record

- Representation names and tolerance classes are grouped in
  `MVP_NUMERIC_POLICY`; stable field constants remain available to consumers.
- Reviewer empathy: the distinction between PMF and physical tolerances is
  visible in one policy object without changing existing call sites.
- Verification: all standalone tests pass, Spec Verification is 165/165,
  `py_compile` passes, and `git diff --check` passes.

## Dependencies

- Parent: none
- Depends on: ADR 0014, ADR 0018, ADR 0037
- Blocks: continuous-state or exact-probability implementation
- Related: `qpex-dimensional-types.md`, `qpex-type-system.md`

## Adjudicator Decision Points

- [ ] Which item, if any, is prioritized for the next Kernel generation?
- [ ] Is `f64` retained as MVP storage with exact arithmetic only at the boundary?
- [ ] Are continuous distributions a Kernel capability or a separate port?

## Context

- Included: current PMF/amplitude representation and dimensional typing.
- Omitted: density matrices (LISS-0011) and QPU IR (LISS-0019).
- Assumptions: existing examples remain numerically compatible.

## AI Planning Records

### AIP-0018-001

- Status: proposed
- Created at: 2026-07-23
- Planning size: L
- Intended execution route: Architecture Path research and triage only.
- Intended scope: classify and prioritize representation questions.
- Estimation basis: multiple independent numerical decisions.
- Assumptions: no implementation implied by classification.
- Confidence: medium

## Verification

- Decision matrix and representative numerical fixtures after scope acceptance.
