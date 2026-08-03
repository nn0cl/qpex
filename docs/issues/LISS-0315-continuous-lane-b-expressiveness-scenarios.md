# LISS-0315: Continuous Lane B expressiveness scenarios (docs seats)

## Metadata

- Local issue ID: LISS-0315
- Status: **complete** (2026-08-03) — documentation seats + inventory only
- Type: Architecture Path / expressiveness (no Kernel)
- Priority: P3 Lane B preparation
- Depends: ADR 0185 Lane A shipped; proper-demand analysis (session)
- Branch: `docs/liss-0315-continuous-lane-b-expressiveness`
- Spec: [staqex-v1-continuous-lane-b-expressiveness-scenarios.md](../specs/staqex-v1-continuous-lane-b-expressiveness-scenarios.md)

## Intent

Add **proper mid-program Continuous demand** as locked expressiveness seats
(same checking style as S01 A+B / constellation): Ideal form, hard gates,
today’s Lane A/Host substitute, Class, action. Enables language-design review
without shipping Lane B.

## Seats

| ID | Name |
|---|---|
| CH-field-compose | Multi-step continuous field → one finiteize |
| CH-field-fork | Shared continuous → dual finiteize |
| CH-field-theory | Theory continuous vocabulary aligned with notebook |

## Exit

- [x] Spec inventory + Ideal chalk + verification checklist
- [x] S01 locked scenario §Field continuous
- [x] Scorecard + S01 README pointers
- [x] ADR 0185 / re-review cross-links
- [x] No Kernel Continuous; no city-wide continuous QC claim

## Non-goals

Ship ADR for Continuous type; Feature Red; tonight-spine Continuous.
