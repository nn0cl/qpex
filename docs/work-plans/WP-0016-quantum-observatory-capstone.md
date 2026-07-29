# WP-0016: Quantum Observatory capstone

## Goal

Deliver the highest-priority modular example that demonstrates the complete
shipping Staqex surface to students and theoretical physicists, with a CPU-full
story and an honest QPU-compatible subset.

## Scope

- In: LISS-0020, its acceptance specification, `examples/16_quantum_observatory/`,
  coverage tests, catalog docs, and QASM lane.
- Out: LISS-0010…0019 implementation, new language semantics, cloud submit,
  real cryptanalysis, and claims of experimental accuracy.

## Issue Graph

| Issue | Status | Size | Depends on | Phase |
|---|---|---:|---|---|
| LISS-0020 | Complete (Adjudicator approved 2026-07-27) | XL | LISS-0001…0009; accepted slice review | Feature → Phase 3 → closed |

## Recommended Order

1. Adjudicator reviews LISS-0020 and the capstone acceptance specification.
2. Phase 1 Red: add failing coverage/catalog/QASM tests only.
3. Review Phase 1 tests and explicitly approve Phase 2 Green.
4. Implement the smallest modular example slices, keeping CPU and QPU lanes
   separate where the backend boundary requires it.
5. Phase 3 Refactor: readability pass with student and physicist review notes.
6. Run full SV, example discovery, CPU seeded runs, and QASM validation.

## Current Next Issue

- Issue: start the next independent language issue after this closeout.
- Reason: LISS-0020's example, acceptance specification, and verification are
  synchronized; further language work must not be hidden inside the capstone.
- Adjudicator approval: final review/merge completed; a separate LISS and
  phase approval is required for subsequent language work.

The initial Green slice, continuous-model/diagnostics slice, and expanded
Kitchen Sink slice are complete. No deferred LISS feature is implied by the
capstone.

## Risks

- “All use cases” can become an untestable promise; the coverage matrix makes
  the observable meaning explicit.
- A single narrative can become repetitive; modules must earn their existence
  by demonstrating a distinct shipped surface.
- Hardware claims can exceed OpenQASM support; the QPU lane is deliberately
  small and portable.

## Verification Plan

- `git diff --check` for documentation.
- Phase 1 accepted tests and coverage matrix review.
- `python3 tests/spec_verification/run_all.py` plus capstone tests.
- CPU seeded runs, `check`, `inspect`, `snapshot`, and QASM emission.

## Phase 3 review record

- LISS-0020 expanded the main narrative with accepted trait/pipeline, static
  register/QFT, Suzuki S2, workflow parameter, and numeric Lindblad slices.
- README and acceptance specification now distinguish CPU/simulator, QPU IR,
  and provider-host boundaries.
- Verification: capstone tests, focused accepted-slice tests, `compileall`,
  `git diff --check`, CPU/QPU checks, and Spec Verification 165/165.
