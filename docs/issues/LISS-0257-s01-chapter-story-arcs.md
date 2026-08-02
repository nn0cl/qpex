# LISS-0257: S01 constellation chapters — story arcs brush-up

## Metadata

- Local issue ID: LISS-0257
- Status: **complete** (2026-08-02)
- Type: Feature Path
- Priority: P1
- Program: [WP-0087](../work-plans/WP-0087-s01-expressiveness-brushup.md)
- Parent seats: [LISS-0247](LISS-0247-s01-e1-locked-scenario-seats.md) (**complete**)
- Prior align: [LISS-0248](LISS-0248-s01-r3-chapter-align.md) (**complete**)
- Recommended after: [LISS-0256](LISS-0256-s01-spine-causal-domain-joint.md)
- Paths: chapter `main_*.sqx` headers + README constellation table
- Branch: `docs/wp-0087-s01-expressiveness-brushup`

## Problem

E1 gave each chapter a **locked-scenario seat**. R3 labeled CH-* and thinned
inspect floods. Several chapters remain **surface existence proofs** (especially
fuel, burst, fidelity) rather than a readable one-arc story: setup → evolve/apply
→ expect/measure → what the sample means for that seat.

## Goal

For each constellation chapter, ensure:

1. Header cites **CH-id**, lane, Non-placeable if any, locked-scenario anchor
2. **One-sentence arc** in header or README row (who / what changes / what is measured)
3. Code path matches that arc (no dead setup larger than the experiment)
4. Scorecard evidence path still valid

## Per-chapter minimum (checklist)

| Chapter | Path | Minimum arc improvement |
|---|---|---|
| CH-morning | `main_morning_collect.sqx` | Morning fields → status sample; missing stays missing (comment + structure) |
| CH-day2 | `main_day2_recovery.sqx` | Recovery H / S4 named as day-2 policy |
| CH-comms | `main_comms_channel.sqx` | Noisy channel → observed order priority (Lindblad toy honesty) |
| CH-burst | `main_burst_spectrum.sqx` | Burst spectrum → correlation peek → measure; circuit lane labeled |
| CH-tri | `main_tri_register.sqx` | Rescue×logistics×fire coupling readable in names + measure |
| CH-route | `main_route_interference.sqx` | Competing corridors → interference → sample |
| CH-lattice | `main_lattice_four.sqx` | Zone damage field → evolve → sample |
| CH-fidelity | `main_fidelity_inner_check.sqx` | Prior vs proposal `inner`/`outer` before commit narrative |
| CH-fuel | `main_fuel_search.sqx` | Keep minimal; strengthen Non-placeable + “search until budget” comments only if code stays thin |

## Exit

- [x] Each chapter header has arc sentence + CH seat reference
- [x] README constellation table includes one-line arc per CH
- [x] No chapter grows an inspect museum (headers/docs only)
- [x] Smoke: morning / fuel / route seed 0 OK; others header-only
- [x] No A+B row deleted
- [x] Non-placeable labels preserved (fuel)

## Non-goals

- Spine causal rewrite (0256)
- Host ticket schema (0259)
- Kernel changes
- Merging all chapters into one main

## Verification

```bash
for m in main_morning_collect main_day2_recovery main_comms_channel \
  main_burst_spectrum main_tri_register main_route_interference \
  main_lattice_four main_fidelity_inner_check main_fuel_search; do
  python3 -m compiler.staqex run examples/showcase/S01_quantum_disaster_response/${m}.sqx --seed 0
done
```
