# Adjudicator review request: WP-0089 sugar ADRs 0180–0183

| Field | Value |
|---|---|
| Date | 2026-08-03 |
| Requested approval | **Architecture Accept** (per ADR, independent) |
| Not requested | Kernel Red/Green; batch execution; axiom change |
| Program | [WP-0089](../../architecture/documentation-compression-map.md) |
| Drafts | [ADR 0180](../../architecture/adr/0180-local-type-inference.md), [0181](../../architecture/adr/0181-named-struct-construction.md), [0182](../../architecture/adr/0182-default-experiment-profile.md), [0183](../../architecture/adr/0183-module-relative-import.md) |

## Also in this continuation

S01 chapter selective import adoption (morning / day2 / lattice / route) —
examples only; no Kernel change.

## Ask

1. Accept / amend / reject each of ADR 0180–0183?
2. Freeze open choices listed in each ADR checklist (e.g. named-struct syntax,
   relative import package- vs directory-relative, default-profile trigger)?

## After Accept

Kernel Issues LISS-0282 / 0284 / 0286 / 0288 in that Accept order; then
LISS-0289 face re-sync.
