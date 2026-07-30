# Trace: ADR 0108–0111 Accepted + LISS-0082 Slice F Phase 1 Red

| Field | Value |
|---|---|
| Date | 2026-07-30 |
| Path | Architecture acceptance + Feature Path Phase 1 Red |
| Branch | `feature/liss-0082-slice-f-adr-batch` |
| Approval | Adjudicator batch: ADR 0108–0111 Architecture Accepted (conditional);
  Slice F Architecture contract; Slice F Phase 1 Red; stop before Green |

## Investigation summary

- Prior research: Quantum Semantic IR foundations; machine-scale / capacity /
  current-hardware envelopes; ADR 0106 D9/D11; blueprint §4.3.
- Prior decisions: LISS-0082 A–E complete (PR #145); ADR 0108 §1a scoped only;
  0109–0111 Proposed; Slice F optional after A–E.
- Doc drift confirmed: open-work-register / plan / ADR follow-ons still said
  Proposed / PR pending after Issue completion sync.

## Decisions recorded

1. ADR 0108–0111 → **Accepted** with explicit non-authorizations (no language
   maxima, no implicit fallback, no Core credentials, no live provider start
   from ADR alone, no treating envelope numbers as delivery).
2. Slice F Architecture contract locked in plan §9:
   `CompileResult.quantum_semantic_ir`; empty finite evidence soft lower;
   `QSEM_*` soft diagnostics; minimal `pipeline.py`.
3. Slice F Phase 1 Red authored; Green not started.

## Artifacts

- ADRs 0108–0111 status + follow-on updates
- Claim sync: open-work-register, architecture README, local-issue-planning,
  WP-0025 LISS-0082 row, Issue/plan
- `tests/test_quantum_semantic_ir_slice_f_red.py`

## Verification

- Expected Red: `CompileResult` lacks `quantum_semantic_ir`
- No `pipeline.py` / Green implementation in this unit

## Stop

Await Slice F Phase 2 Green approval.
