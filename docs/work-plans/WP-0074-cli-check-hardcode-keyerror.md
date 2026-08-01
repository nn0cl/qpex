# WP-0074: CLI check / hard-code gate / partial KeyError (Wave CLI)

| Field | Value |
|---|---|
| Status | **complete** (2026-08-01) |
| Branch | `batch/wp-0074-cli-check-hardcode-keyerror` |
| Batch | [execution-batch-wp-0074.json](../collaboration/reviews/execution-batch-wp-0074.json) |
| Parent | WP-0069; Adjudicator「上から順番に」 |

## Goal

Fix LISS-0199 → LISS-0200 → LISS-0201 in that order (CLI / gate / crash).

## Locked defaults

- `check` gates on the same hard-code judgement as `CompileResult.ok`
- One exported `HARD_CODES` from `pipeline.py`; `run.py` / `cli.py` import it;
  include `CONFIG_HARVEST_COLLISION_ERROR` in that set
- Partial formation with `_` holes must not Trace-Out closed-over caller coords;
  Pipe State binds move linear Vars (so `w |> p` discharges `w`)

## Issues

| ID | Title | Status |
|---|---|---|
| LISS-0199 | `check` false-OK | **complete** |
| LISS-0200 | hard-code set divergence | **complete** |
| LISS-0201 | partial-hole KeyError | **complete** |

## Out

LISS-0204–0207, 0209–0210, 0212–0219 (later in the same top-down sequence).
