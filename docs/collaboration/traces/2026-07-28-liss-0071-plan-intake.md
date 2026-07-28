# Trace: LISS-0071 Phase 0 plan intake

| Field | Value |
|---|---|
| Date | 2026-07-28 |
| Issue | LISS-0071 |
| Path | Feature Path — documentation / plan only |
| Phase | phase-0-design |
| Branch | `docs/liss-0071-conformance-plan` |
| Implementation | **forbidden** until plan approval |

## [DESIGN CHECK]

- Scope: Propose versioned conformance plan (taxonomy, slices A–C, Python
  oracle, DR-011 + report drift); no Red.
- Specs inspected: WP-0025; acceptance envelopes E-01–E-14; SV protocol;
  `tests/spec_verification/`; LISS-0071 Issue stub.
- Boundaries: docs only; Rust differential out (LISS-0070 deferred).
- Decisions pending Adjudicator: report-drift policy default
  (`--no-write-report` + CI artifacts).
- Verification: docs PR; no compiler/tests mutations.

## Next safe action

Adjudicator plan approval → Slice A Phase 1 Red.
