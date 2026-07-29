# Trace: LISS-0075 Issue completion closeout

| Field | Value |
|---|---|
| Date | 2026-07-29 |
| Issue | LISS-0075 |
| Path | Feature Path — Issue completion |
| Phase | done (Slices A–D) |
| Branch | `feature/liss-0075-linear-quantum-usage` |
| Approval | Adjudicator「承認」(completion) |

## Closeout

- One-time C/D approval earlier same day; risks accumulate policy honored.
- Slices A–D Red → Green → Refactor complete.
- Completion approval does **not** auto-close R1–R10.

## Delivered surface

| Code / artifact | Role |
|---|---|
| `HirLinearVerifier` | per-fun linear use analysis |
| `LINEAR_DUPLICATE_USE` | alias / duplicate consume |
| `LINEAR_IMPLICIT_DISCARD` | unconsumed State at block exit |
| `UNCOMPUTE_WITNESS_MISSING` | declared Uncompute without witness |
| static `|0>` / `vacuum` rebind | provisional Uncompute witness (R9) |
| `HirModule.linear_diagnostics` | Slice D wiring via `build_hir` |

## Register / WP

- open-work-register: LISS-0075 **complete**; residuals → LISS-0114 (triage)
- WP-0025: LISS-0075 marked complete; current next → **LISS-0114**

## Self-check

- Red failed for missing diagnostics / fields before Green (A–D).
- Green did not edit tests to force pass.
- Refactor did not change assertions.
- A/B/C/D + LISS-0080 HIR D suite PASS after C/D.
- Parked risks triaged to LISS-0114 (R10 closed-accepted).

## Next safe action

1. Commit + PR when Adjudicator requests (working tree may still be dirty).
2. **LISS-0114 plan intake** (Slice A: pipeline hard-fail + Gherkin).
