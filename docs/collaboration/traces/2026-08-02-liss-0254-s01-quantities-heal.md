# AI work trace — LISS-0254 S01 quantities heal + D5 lift

| Field | Value |
|---|---|
| Date | 2026-08-02 |
| Branch | `feature/liss-0254-type-first-field-units` |
| Issue | LISS-0254 |
| ADR | 0174 **Accepted** |
| Authorization | Adjudicator「修復もして」(sample heal after Phase 2 Green) |

## Done

- S01 `domain/quantities.sqx`: Float stocks → dimful
  `Length`/`Mass`/`Time`/`Current`/`Temperature` fields; methods use
  `this.* to unit` (no literal-only theater for stocks).
- Tonight spine ctor: `12.0.km`, `800.0.kg`, `900.0.s`, `40.0.A`, `291.0.K`.
- `scale_tag` → dimensionless `1.0` (unlike dims not summed into Float).
- Dialect D5 demotion lifted; scorecard / sketch / ADR follow-up synced.

## Verification

- `.venv/bin/pytest tests/test_liss0254_type_first_field_units_red.py
  tests/test_mixed_unit_canonical_promote_red.py -q` → **9 passed**
- `python3 -m compiler.staqex …/main_disaster_response.sqx --seed 0` → `0`

## Still open

- Phase 3 Refactor + reviewer empathy (needs Adjudicator「承認」)
- PR #267 merge after Phase 3 / Adjudicator merge approval
