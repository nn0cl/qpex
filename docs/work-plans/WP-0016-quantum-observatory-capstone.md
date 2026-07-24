# WP-0016: Quantum Observatory capstone

## Goal

Deliver the highest-priority modular example that demonstrates the complete
shipping QPex surface to students and theoretical physicists, with a CPU-full
story and an honest QPU-compatible subset.

## Scope

- In: LISS-0020, its acceptance specification, `examples/16_quantum_observatory/`,
  coverage tests, catalog docs, and QASM lane.
- Out: LISS-0010…0019 implementation, new language semantics, cloud submit,
  real cryptanalysis, and claims of experimental accuracy.

## Issue Graph

| Issue | Status | Size | Depends on | Phase |
|---|---|---:|---|---|
| LISS-0020 | proposed | XL | LISS-0001…0009; spec review | Architecture → Feature |

## Recommended Order

1. Adjudicator reviews LISS-0020 and the capstone acceptance specification.
2. Phase 1 Red: add failing coverage/catalog/QASM tests only.
3. Review Phase 1 tests and explicitly approve Phase 2 Green.
4. Implement the smallest modular example slices, keeping CPU and QPU lanes
   separate where the backend boundary requires it.
5. Phase 3 Refactor: readability pass with student and physicist review notes.
6. Run full SV, example discovery, CPU seeded runs, and QASM validation.

## Current Next Issue

- Issue: LISS-0020 design/spec review.
- Reason: acceptance scope is broad and must be reviewed before tests or code.
- Adjudicator approval needed: scope, Architecture Path, and then Phase 1 Red.

The initial Green slice and the subsequent continuous-model/diagnostics slice
are complete. Any further expansion must begin with new Phase 1 Red tests for
an explicitly named remaining surface; no deferred LISS feature is implied by
the capstone.

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
