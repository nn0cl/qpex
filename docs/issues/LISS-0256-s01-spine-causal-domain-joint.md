# LISS-0256: S01 spine — causal domain → Joint (expressiveness P0)

## Metadata

- Local issue ID: LISS-0256
- Status: **complete** (2026-08-02)
- Type: Feature Path
- Priority: **P0** (expressiveness)
- Program: [WP-0087](../work-plans/WP-0087-s01-expressiveness-brushup.md)
- Path: `examples/showcase/S01_quantum_disaster_response/main_disaster_response.sqx` + related `domain/` / `physics/` / `grid/`
- Depends on: dialect spine (LISS-0246); `tracing_out` (LISS-0251); field units (LISS-0254)
- Soft: [LISS-0255](LISS-0255-s01-docs-hygiene-post-0254.md) docs sync
- Branch: `docs/wp-0087-s01-expressiveness-brushup`

## Problem

Tonight spine builds a rich classical domain (shelters, roads, requests, hazards,
quantities, …) then runs a **2-wire** `when` / named-`H` / `evolve` / `expect` /
`measure … tracing_out` experiment. Most constructed values **do not feed**
plan arms, Hamiltonian coeffs, or terminal meaning.

Re-review one-liner: seats and dialect are good; **causal expressiveness** is not.

## Goal

Make the spine an honest **small** Joint experiment **driven by** a minimal set of
ops quantities that appear in the locked scenario CH-tonight-spine seat — without
restoring inspect museum, identity `evolve times`, or scorecard dump on one main.

## Design constraints

- Minimal dialect spine rules remain binding.
- Prefer **fewer domain objects that affect H/when** over many decorative boards.
- Coeffs / pressures should come from named physics or domain methods with a
  physics or ops reading (not anonymous magic numbers only) where practical.
- Do **not** invent MIP/city optimality; keep 2-wire (or documented small width).
- Keep `measure … tracing_out …` (no ritual `|0>` discharge).
- Scorecard A+B evidence for surfaces that leave the spine must still exist on
  constellation chapters (do not drop rows).

## Candidate causal hooks (implementer chooses minimal set; document mapping)

| Domain signal | Possible Joint use |
|---|---|
| `OpsPhase` / shelter status | existing `when` arms (keep; ensure not dead) |
| corridor open / blocked scores | weight `H_corridor` or evolve duration scale |
| hazard secondary pressure | weight `H_damage` / fire-related drive |
| fairness / ration | Classical⊕State ration already; tie to plan branch if honest |
| request urgency proxy | bias plan preparation or expect observable choice |
| Type-First window / stock | scale `PlanWindow.t` or constraint coeffs |

**Exit requires a short mapping table** in file header or README spine section:

```text
domain field/method → H_* / when / expect / measure story
```

## Exit

- [x] Mapping table present and accurate (file header causal map)
- [x] At least **three** independent domain-derived signals affect Joint evolution
      or preparation (blockage→H_drive, fair/ready/people→H_drive, hazard→t_damage,
      open_score→t_corridor, when phase/shelter)
- [x] Decorative-only boards removed from spine (theatre_scale, honesty dossier,
      interference tags, inspect flood already gone)
- [x] `python3 -m compiler.staqex run …/main_disaster_response.sqx --seed 0` succeeds
- [x] Host `export_tonight_ticket.py --seed 0` still non-vacuum fail-closed
- [x] No scorecard A+B row deleted; no Kernel change
- [x] Note: classical free-function Call cannot appear as BinOp operand — bind first

## Non-goals

- Full disaster MIP / multi-hundred request Joint
- Live QPU
- Chapter arc depth (LISS-0257)
- Ticket ops vocabulary (LISS-0259)
- Package FQN rename (LISS-0260)

## Verification

```bash
python3 -m compiler.staqex run examples/showcase/S01_quantum_disaster_response/main_disaster_response.sqx --seed 0
python3 examples/showcase/S01_quantum_disaster_response/host/export_tonight_ticket.py --seed 0 --out /tmp/tonight_ticket.json
# Review: mapping table + causal hooks
```

## Stop conditions

- Requires new language surface → ADR Issue, stop Feature
- Adjudicator rejects shrinking unused domain from spine without chapter home
