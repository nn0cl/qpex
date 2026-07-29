# Trace: LISS-0068 normative rebaseline slice 3

- Date: 2026-07-27
- Task: Diagnostic catalog merge (Kernel vs Host appendix split)
- Agent: Cursor (Auto)
- Phase: Architecture Path / LISS-0068 slice 3

## Delivered

- `docs/specs/staqex-v1-diagnostic-catalog.md`
  - Appendix K: Kernel compile-hard (`pipeline._HARD_CODES`) + runtime/warnings
  - Appendix B: Backend emission (QASM/QPU)
  - Appendix H: Host (parametric binding, scientific input, resource, observation, QPU result)
  - Appendix V: Harness-only (SV meta-assertions)
  - Gap register vs v0.1 Appendix B

## Verification

- Documentation-only; codes sourced from shipping `compiler/staqex/`.
- `FUNCTION_ARITY_ERROR`, `ACTING_SPACE_MISMATCH`, `BINDER_GUARD_UNSUPPORTED`,
  `CONFIG_HARVEST_COLLISION_ERROR` documented as shipping compile diagnostics
  pending `_HARD_CODES` audit in LISS-0071.

## Next safe action

- LISS-0068 slice 4 — EARS/Gherkin acceptance envelopes per major capability.
