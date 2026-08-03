# LISS-0259: TonightTicket thin ops mapping (honest Host C-layer)

## Metadata

- Local issue ID: LISS-0259
- Status: **complete** (2026-08-02)
- Type: Feature Path (Host / S01 host only)
- Priority: P1
- Program: [WP-0087](../work-plans/WP-0087-s01-expressiveness-brushup.md)
- Parent: [LISS-0243](../architecture/documentation-compression-map.md) (**done** A→B→C envelope)
- Recommended after: [LISS-0256](LISS-0256-s01-spine-causal-domain-joint.md)
- Paths: `host/ticket_dto.py`, README Host section; tests `tests/test_s01_tonight_ticket_export.py`
- Branch: `docs/wp-0087-s01-expressiveness-brushup`

## Problem

LISS-0243 ships structured `TonightTicket` with non-vacuum `plan.sample_value` /
`marginal` and honesty blocks. The sample is still a **bare 2-level outcome**
with no ops vocabulary (corridor bias, hazard pressure, ration story). Readers
may over-read `0` as “plan ID 0” without documentation.

## Goal

Extend ticket **optionally and honestly**:

1. Document what `sample_value` means (basis label of terminal measure wire)
2. Add **optional** `ops_context` (or similar) fields **only** if sourced from
   JobResult metadata / declared Host-side constants / non-invented diagnostics
3. Never invent fairness scores or city optimum from vacuum or stdout scrape

Prefer: after 0256, Host may pass **explicit** context via settings or a small
sidecar produced only from values the spine documents as ticket-facing — not
Joint leakage of full domain graphs.

## Schema sketch (additive; keep schema_version bump policy)

```json
{
  "schema_version": 2,
  "plan": {
    "sample_value": 0,
    "marginal": {"0": 0.9, "1": 0.1},
    "vacuum": false,
    "wire": "plan0",
    "meaning": "Terminal sample of tonight plan wire (not a multi-field dispatch ID)"
  },
  "ops_context": {
    "note": "optional; only fields with documented source",
    "seed": 0
  },
  "honesty": { "live_qpu": false, "optimality_claim": false }
}
```

If additive fields are not yet justifiable, **schema_version 1 + stronger
`meaning` / README** alone can meet a reduced exit (Adjudicator may accept).

## Exit

- [x] Ticket documents measure wire meaning (`plan.wire` / `plan.meaning` + README)
- [x] No invented ops KPIs; thin `ops_context` note only; fail-closed vacuum unchanged
- [x] Tests: `pytest tests/test_s01_tonight_ticket_export.py`
- [x] `honesty.live_qpu == false`, `optimality_claim == false`
- [x] schema_version remains **1** (additive fields only)

## Non-goals

- Live field dispatch system
- Scraping valuemass stdout
- Full morning/day2 ticket chain
- Live QPU

## Verification

```bash
python3 examples/showcase/S01_quantum_disaster_response/host/export_tonight_ticket.py --seed 0 --out /tmp/tonight_ticket.json
# pytest for ticket export if present
```
