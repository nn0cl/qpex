# Staqex showcase S0 specification (docs-only)

| Field | Value |
|---|---|
| Status | **draft Accepted for S0** (2026-07-31) — docs only; no `.sqx` Red yet |
| Issue | [LISS-0127](../issues/LISS-0127-showcase-s0-specification.md) |
| Mission | [mission lock](staqex-v1-showcase-mission-lock.md) (P2) |
| Coverage | [language coverage ledger](staqex-v1-language-coverage-ledger.md) (P1) |
| Implementation permission | **none** for S1+ until Adjudicator authorizes Phase S Red |

## 1. Problem statement (physicist)

Show that Staqex can host a **finite quantum-matter discovery** workflow:
build a lattice/spin Hamiltonian from typed parameters, evolve a prepared
state under that operator for a finite duration, inspect non-destructive
observables (expect / inspect), and only then `measure`, while the source
remains blackboard-legible and refuses classical control shortcuts.

## 2. Context map (programmer)

```text
[Domain] couplings / geometry / Operator H
    ↓
[Application protocol] prepare → evolve → observe intent → measure
    ↓
[Provenance] SIM vs static honesty + soft IR evidence
```

Adapters: only Kernel ports already accepted (RNG, Source, MeasureSink).
No provider SDK. No live QPU.

## 3. Entrypoint and module map (planned)

| Module (planned) | Bounded context | Role |
|---|---|---|
| `main_quantum_matter_discovery.sqx` | Application | Spine entry |
| `domain/` model + params | Domain | `struct`/`enum`/`namespace` packs |
| `physics/` operators / quench | Domain | Operator trees; named coeffs |
| `protocol/` evolve + observe | Application | `evolve` / `expect` / `inspect` |
| `provenance/` honesty notes | Provenance | comments + inspect surfaces; soft IR OK |

Exact filenames may adjust in S1; every file must participate in the spine or
be deleted (rebaseline S2 rule).

**A11 salvage:** may donate patterns/names; must not be copied as a type museum.

## 4. Required coverage subset (from P1 ledger)

| Required row | How S* will prove it |
|---|---|
| `when` | At least one protocol branch uses `when`, never `if` |
| Named Float / field coeffs in Operator | Hamiltonian uses Type-First or struct field coeffs |
| `expect` / `inspect` | Mid-spine observation without collapse |
| Multi-file modules | `run_path` on package entry |
| OOP / visibility with physics reading | domain packs + `pub`/`_` as needed |
| LINEAR honesty | No false discards; leftovers measured or uncomputed |
| Ports / diagnostics | Fail-closed on invalid linear / type misuse fixture |
| Terminal `measure` | Single classical collapse at end of spine |
| `evolve … for/times` | Finite duration quench/drive |

## 5. Joint rubric (extends rebaseline §1)

| Pass | Evidence |
|---|---|
| Physicist | Source readable as the paper narrative; no equation-breaking workarounds taught as style |
| Maintainer / CA | Clear contexts; no hidden policy in adapters; green `compile`/`run` |
| Friction | Language bugs → Issues/ADRs only — never silent Kernel patches in sample |

## 6. Non-goals (S0–S4)

- Provider SDKs / live QPU credentials
- Padding for LOC targets
- Implementing Open Topics
- Reclaiming LISS-0120 ID
- Changing accepted axioms (`when`-not-`if`)

## 7. Next phase gate

- **S1** may be authorized (Option B complete). This S0 document alone does
  **not** authorize writing showcase `.sqx` — need explicit S1 Issue + Phase.
- QPU honesty: [staqex-v1-qpu-capability-honesty.md](staqex-v1-qpu-capability-honesty.md).
