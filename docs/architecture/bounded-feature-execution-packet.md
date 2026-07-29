# Bounded feature execution packet

## Status

**Proposed process contract for P0/P1 Issue review. Documentation only.**

This contract turns an approved Issue slice into a bounded request suitable
for a code-assistant-class model. It does not authorize a phase or replace the
Issue, accepted specification, tests, or Adjudicator.

## Required packet

Every execution request must name:

1. one Issue and one Slice;
2. exactly one phase: Red, Green, or Refactor;
3. the accepted authority and reviewed acceptance scenarios;
4. unresolved dependencies and whether they are complete or waived;
5. allowed write paths, read-only paths, and forbidden paths;
6. input fixtures and delivery profiles;
7. deterministic commands and expected phase result;
8. explicit stop conditions;
9. implementation and technology-selection permission;
10. the required handoff evidence.

Missing fields make the packet invalid. The agent stops after design intake.

## Phase invariants

- **Red:** change tests or approved test scaffolding only; demonstrate the
  expected failure; do not write implementation.
- **Green:** do not alter reviewed assertions; add the smallest readable
  implementation; stop when the selected tests pass.
- **Refactor:** preserve assertions and behavior; improve responsibility and
  readability; run the selected and regression checks.

No packet authorizes the next phase. One successful Slice does not authorize
another Slice.

## Model routing

A code assistant may execute a packet when requirements are closed, write
paths are narrow, and verification is deterministic. Escalate to a strong
reasoning agent and stop before mutation when:

- accepted documents conflict;
- a new semantic, deployment, security, provider, or dependency boundary is
  required;
- more than the named Issue must change;
- an expected diagnostic or observable result is undefined;
- reviewed tests appear incorrect;
- a target or simulator technology must be selected;
- a second failed implementation attempt changes the planning size.

## Output evidence

The handoff reports:

- Issue, Slice, phase, and approval source;
- files read and changed;
- tests/checks run and their exact status;
- Red, Green, or Refactor result;
- assumptions, deviations, and remaining risks;
- confirmation that forbidden paths and later phases were not touched.

Do not request or expose hidden chain-of-thought. Evidence consists of public
decisions, file references, diagnostics, diffs, and deterministic results.

## P0/P1 profile rule

Each executable Slice names at least one applicable profile:

- current: `CH0_COMMON_PHYSICAL`, `CH1_DIGITAL_RESEARCH`,
  `CH1_ANALOG_RESEARCH`, `SIM0_EXACT`, or `SIM1_MIXED`;
- planned-system: one NH5 profile when scale affects the contract;
- horizon: QP-2 or QS-2 only when compactness or exact resource magnitude is
  under test.

Profiles are downstream fixtures, never language or Semantic IR limits.
