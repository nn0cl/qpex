# AI work trace — LISS-0250 Phase 2 Green

| Field | Value |
|---|---|
| Date | 2026-08-02 |
| Branch | `feature/liss-0250-measure-tracing-out` |
| Path | Feature Path — Phase 2 Green |
| Issue | LISS-0250 |
| ADR | 0173 **Accepted** |
| Approval | Adjudicator「承認」(Phase 2 Green) |

## Change

- `Measure.tracing_out` AST + parser clause after optional `with` / `to`
- HIR: leftovers consumed at measure; builtin `trace_out` always consumes args
- Evaluator: Born `joint.trace_out` leftovers then measure; deferred cone seeds

## Verification

`tests/test_liss0250_measure_tracing_out_red.py` → 7 passed (no test edits).

## Next safe action

Adjudicator Phase 3 Refactor approval (optional cleanup) then completion /
S01 spine follow-on.
