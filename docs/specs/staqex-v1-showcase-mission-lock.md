# Staqex showcase mission lock (Gate P2)

| Field | Value |
|---|---|
| Status | **Locked** (2026-07-31) — Adjudicator 「承認」 |
| Issue | [LISS-0126](../issues/LISS-0126-showcase-mission-lock.md) |
| Prerequisites | P0 complete (LISS-0119/0122/0123); P1 complete (LISS-0124) |
| Authority | [rebaseline](staqex-v1-representative-program-rebaseline.md) Gate P2 |
| Next | [S0 showcase specification](staqex-v1-showcase-s0-specification.md) ([LISS-0127](../issues/LISS-0127-showcase-s0-specification.md)) |

## Locked mission

**Theme:** finite **quantum-matter discovery** (Noether Forge lineage).

**One-sentence physicist brief:** Prepare a finite spin/lattice model, quench or
drive it under an explicit Hamiltonian, read symmetry-aware observables
(magnetization / correlation / spectroscopic intent) without mid-protocol
collapse, then terminal-`measure` with a provenance dossier that states
simulator vs static-hardware honesty.

**Not locked (rejected for v1 showcase):**
- mission-observatory-scale networking physics as the primary spine;
- open-system / Lindblad-first showcase (P1 marks general CPTP **out** / optional toy only);
- live QPU credentials or provider SDKs;
- continuous discretization hidden inside the sample.

**Salvage policy:** `examples/applied/A11_noether_forge/` is **optional salvage
input** only — not authoritative until rewritten under S* as one mission spine
(rebaseline §4).

## Bounded contexts (DDD / CA reading)

| Context | Responsibility | Ports |
|---|---|---|
| Domain / physics model | Couplings, geometry, Hamiltonian operators, durations | none external |
| Application / protocol | Prepare → evolve → observe intent → terminal measure | uses Kernel semantics only |
| Provenance / honesty | Lane declaration (SIM vs static CH*), soft IR evidence | MeasureSink / diagnostics |
| Catalog teaching | Official basics/applied remain separate green demos | — |

Forbidden: hidden business policy in adapters; silent Kernel patches inside
the showcase; padding modules unused by the spine.

## Coverage ledger binding

Required rows from
[`staqex-v1-language-coverage-ledger.md`](staqex-v1-language-coverage-ledger.md)
**must** appear in the S* showcase (or be demoted with explicit Adjudicator
approval):

- `when` (not `if`) pedagogy;
- named coefficient / Operator composition (ADR 0114);
- `expect` / `inspect` ≠ measure;
- multi-file modules;
- `namespace`/`enum`/`struct`/`class` with physics reading;
- LINEAR honesty for true quantum resources;
- ports + fail-closed diagnostics;
- Never Leave the State + terminal `measure`;
- ket + `evolve … for/times`.

Open Topics: **Option B** pauses S1 until selected topics are finalized
([program](staqex-v1-open-topics-before-s1-program.md)). P1 ledger rows stay
provisional until that program exits.

## Size / honesty band

- Finite discrete model only (no hidden continuous grid as “magic”).
- Soft `QSEM_*` / Physics IR evidence allowed; must not be treated as failure.
- Target scale: coherent mission spine; revisit 1k–3k LOC only after padding
  pressure is gone (P0 green catalogs).

## Exit of P2

- [x] Theme locked (default Noether Forge / quantum-matter discovery)
- [x] Alternates explicitly rejected for this lock
- [x] Coverage binding stated
- [x] Successor S0 Issue named (LISS-0127)
