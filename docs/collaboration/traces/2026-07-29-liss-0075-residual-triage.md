# Trace: LISS-0075 residual risk triage → LISS-0114

| Field | Value |
|---|---|
| Date | 2026-07-29 |
| Path | Architecture Path — docs only |
| Source Issue | LISS-0075 (**complete**) |
| Follow-up Issue | **LISS-0114** (proposed) |
| Implementation | **none** |

## Problem corrected

LISS-0075 / register / WP text treated **LISS-0077** as “full linear type
system” successor. WP-0025 defines LISS-0077 as **Dynamic QPU controller**.
Residuals must not mix into 0077.

## Delivered

- [`docs/issues/LISS-0114-linear-verifier-hardening.md`](../../architecture/documentation-compression-map.md)
  — disposition matrix R1–R10; slices A–F; R5 hard-fail + R2 strict-alias defaults
- [`docs/issues/LISS-0075-linear-quantum-usage.md`](../../architecture/documentation-compression-map.md)
  — Unlocks → 0114; out-of-scope retargeted; R10 **closed-accepted**; Gherkin
  sketch rebaselined to shipped surface
- [`docs/architecture/open-work-register.md`](../../architecture/open-work-register.md)
  — 0075 note fixed; 0114 row added
- [`docs/work-plans/WP-0025-staqex-v1-north-star.md`](../../work-plans/WP-0025-staqex-v1-north-star.md)
  — 0114 section; quantum-safety track 0075→0114→0077; current next = 0114

## Disposition summary

| Action | Risks |
|---|---|
| Slice A (first) | R5, R8 |
| Slice B | R1, R3 |
| Slice C (design gate) | R2 |
| Slice D | R4 |
| Slice E | R6 |
| Slice F | R7, R9 (runtime) |
| Closed-accepted on 0075 | R10 |
| MVP provisional until F | R9 static surface |

## Explicitly not done

- No `hir.py` / `pipeline.py` code changes in this triage
- No LISS-0114 Phase 1 Red (awaits plan intake / Adjudicator approval)

## Next safe action

Adjudicator **plan intake** for LISS-0114 Slice A (pipeline hard-fail + Gherkin),
then create `feature/liss-0114-*` and Phase 1 Red.
