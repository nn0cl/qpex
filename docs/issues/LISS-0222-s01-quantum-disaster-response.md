# LISS-0222: S01 Quantum Disaster Response OS

## Metadata

- Local issue ID: LISS-0222
- Status: **complete** (2026-08-01)
- Type: Feature Path (showcase language benchmark)
- Priority: P0
- ADR / lock: [mission lock](../specs/staqex-v1-showcase-mission-lock.md) superseded 2026-08-01
- Spec: [S0 disaster](../specs/staqex-v1-showcase-s0-disaster-response.md)
- Locked scenario: [staqex-v1-s01-locked-scenario.md](../specs/staqex-v1-s01-locked-scenario.md)
- Scorecard: [coverage scorecard](../specs/staqex-v1-s01-coverage-scorecard.md)
- Program: [WP-0070](../work-plans/WP-0070-s01-quantum-disaster-response.md)
- Path: `examples/showcase/S01_quantum_disaster_response/`
- Branch: `feature/wp-0069-s01-disaster-response` (WP-0070 content; 0069 id already taken)

## Goal

Ship a reality-first disaster command OS showcase that exercises **all shipped**
language surfaces (scorecard A+B), multi-day operational cycle, near-real-time
rolling replan story, and honest out-of-scope boundaries.

## Exit

- [x] Mission lock + S0 + scorecard on branch
- [x] Architecture / ship approval recorded
- [x] S01 tree green (`compile`/`run` for runnable mains, including fidelity)
- [x] Scorecard evidence paths filled
- [x] Host companions for MC / credentials / job
- [x] Living docs / CLAUDE Open Topics pointer updated

## Honesty notes

- `inner`/`outer`: **Joint-runnable** via `main_fidelity_inner_check.sqx`
  (LISS-0229).
- `evolve … until`: Joint green; static QPU IR reports soft unsupported.
- Soft QSEM diagnostics remain non-hard.
- Tri-register satellite uses `state (c, t) = cnot(c, t)` so both wires stay
  live under linear discipline (aligned 2026-08-02).

## Non-goals

Kernel Continuous; Joint rational; trait specialization; live QPU SDK; CUDA.
