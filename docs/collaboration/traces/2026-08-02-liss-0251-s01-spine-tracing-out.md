# AI work trace — LISS-0251 S01 spine tracing_out

| Field | Value |
|---|---|
| Date | 2026-08-02 |
| Branch | `feature/liss-0250-measure-tracing-out` |
| Issue | LISS-0251 |
| Approval | Adjudicator「spine 移行」 |

## Change

- Tonight spine `main_disaster_response.sqx`: replace `|0>` hand-kills with
  `measure plan0 tracing_out plan1, ration, …`.
- Scorecard / README / dialect sync; chapters/satellites unchanged.

## Verification

`python3 -m compiler.staqex run …/main_disaster_response.sqx --seed 0` → `0`.
Compile hard LINEAR/PARSE empty. LISS-0250 Red + tonight ticket tests green.
