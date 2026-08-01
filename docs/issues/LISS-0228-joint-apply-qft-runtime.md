# LISS-0228: Joint `apply(qft/iqft/cqft, …)` runtime

## Metadata

- Local issue ID: LISS-0228
- GitHub issue: (none yet)
- Status: **proposed**
- Phase: (none — intake)
- Type: feature
- Priority: P1
- Initial planning size: M
- Current planning size: M
- Owner/agent: (unassigned)
- Related branch: (none yet)
- Program: [WP-0072](../work-plans/WP-0072-s01-coverage-residuals.md)

## Summary

S01 / B11 today build `Operator F = qft(register)` (and `iqft` / `cqft`) for
**QPU IR provenance**, then evolve under a correlator Pauli H. A shake of
`state … = apply(F, …)` fails (LINEAR / `cannot compile operator node Call`).
Scorecard must not claim Joint QFT application until this lands.

Related shipped surface: ADR 0078 / 0120 (exact QFT family + basic-gate
lowering). This Issue is the **Joint evaluator apply path**, not IR lowering.

## Acceptance Notes

- [ ] Spec (EARS/Gherkin) for `apply(qft(reg), wires…)` / arity / LINEAR move
- [ ] Red: apply QFT into Joint state; `expect` or measure witnesses spectrum story
- [ ] Green without editing tests to pass
- [ ] S01 `main_burst_spectrum.sqx` can drop the “IR only” escape if desired
- [ ] Scorecard Honesty row updated

## Dependencies

- ADR 0078, ADR 0120, LISS-0220 (inference as Operator)
- Related sample: `examples/basics/B11_qft_registers/`, S01 burst lane
- Blocks honest S01 QFT runtime claim

## Verification

- New Red test under `tests/`
- `python3 -m compiler.staqex run` burst (or dedicated) main seed 0
