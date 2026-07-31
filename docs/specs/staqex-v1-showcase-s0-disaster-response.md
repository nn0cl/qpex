# Staqex showcase S0 — Quantum Disaster Response OS

| Field | Value |
|---|---|
| Status | **Accepted** (2026-08-01) — Architecture + ship authorize via plan implement |
| Issue | [LISS-0222](../issues/LISS-0222-s01-quantum-disaster-response.md) |
| Mission | [mission lock](staqex-v1-showcase-mission-lock.md) |
| **Locked scenario** | [staqex-v1-s01-locked-scenario.md](staqex-v1-s01-locked-scenario.md) |
| Coverage scorecard | [staqex-v1-s01-coverage-scorecard.md](staqex-v1-s01-coverage-scorecard.md) |
| Tree | `examples/showcase/S01_quantum_disaster_response/` |
| Host companions | `examples/showcase/S01_quantum_disaster_response/host/` |

## 1. Problem statement (public)

**This showcase was written as a language-specification benchmark** (express
shipped Staqex on a command-room product story). It is not a claim that an
urban disaster was optimally solved.

The authoritative narrative — stage, trigger, field problems, decisions,
realtime honesty, tonight / morning / day-2 social outputs, secondary hazards
(aftershock / fire / firestorm), and reality checklist — lives in the
**[locked scenario](staqex-v1-s01-locked-scenario.md)**. Sections below are the
engineering S0 map; do not treat this file as a substitute for that story.

After **K-ku** (K区) faces a capital-region mainshock with **liquefaction**,
**zero-meter inundation**, **wooden dense-area fire / firestorm risk**,
outages, jammed channels, and **aftershocks**, the ward HQ must decide who
goes where, which shelters fill, what supplies move, and which messages get
bandwidth — tonight, then again from morning measurements into next-day
recovery — without pretending Kernel Continuous, Joint rationals, trait
specialization, live QPU SDKs, or CUDA.

Secondary hazards are first-class ops inputs (road blocks, shelter surge,
firefighting demand), not a separate CFD chapter. **首都圏（1都3県）** deploy
uses **80** K-ku-class grid cells (see locked scenario), not one mega-QPU.

### Secondary hazards (locked in) — K-ku

| Hazard | Ops effect in S01 |
|---|---|
| Liquefaction | Corridor / foundation failure; remapped reachability |
| Zero-meter inundation | Shelter surge; closed lowland routes |
| Aftershock | New collapse / road re-block / fresh entrapment demand |
| Wooden dense-area fire / firestorm risk | Firefighting + evacuation; corridor closure; replan priority |
| Comms / power loss | Bandwidth priority; Host batch inject |

Do **not** implement combustion CFD or continuous seismic waveforms. Public
copy uses **K-ku** only (do not expand the design-archetype ward name).

## 2. Context map

```text
[Domain] districts / units / shelters / depots / SI stocks
    ↓
[Physics] constraint H, binders, evolve for/until, expect/inner, Lindblad toy, QFT hint
    ↓
[Protocol] tonight window → rolling replan → morning collect → day-2 replan
    ↓
[Host] MC demand inject, CredentialPort, Job + resource profile, workers
    ↓
[Provenance] honesty + soft IR + static QPU lane declaration
```

## 3. Module map

| Path | Context |
|---|---|
| `main_disaster_response.sqx` | Application spine |
| `domain/` | Ops types, SI, Fraction rations, hazards (aftershock/fire/firestorm), interfaces/`impl` |
| `grid/` | Indexed block costs (`sum`/`product`) |
| `physics/` | Operators, Suzuki, phase, multi-register |
| `comms/` | Lindblad toy + QFT burst hint |
| `protocol/` | Windows, `when`, pipe/Partial plan compose, evolve until |
| `provenance/` | Honesty, soft IR notes, static lane tags |
| `host/` | Python: MC inject, credentials, job runner |

## 4. Operational cycle outputs

Authoritative tables (tonight / morning / day-2 / intentional non-outputs):
[locked scenario § Social outputs](staqex-v1-s01-locked-scenario.md).

Unmet demand and missing morning fields must remain visible.

## 5. Language review rubric

| Pass | Evidence |
|---|---|
| Reality | Roles, resources, failures, multi-day cycle readable |
| Expressiveness | Scorecard A+B rows each cite file/phase |
| Honesty | Out rows not faked; SIM / future-target declared |
| Maintainability | No unused padding modules; fail-closed diagnostics |

## 6. Non-goals

Kernel Continuous; Joint rational; trait specialization Red; live QPU SDK;
CUDA; city-wide optimality proof; publishing victim PII.
