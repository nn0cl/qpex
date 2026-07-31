# LISS-0195: Host Monte Carlo → finite State injection (design)

## Metadata

- Local issue ID: LISS-0195
- Status: **open** (design only — no Kernel Red)
- ADR boundary: [0126](../architecture/adr/0126-continuous-pdf-design-boundary.md) **maintained**
- Strategy: [ADR 0162](../architecture/adr/0162-continuous-host-bridge-first.md) **Accepted**
  (Host/Bridge first; Kernel `Continuous` deferred)
- Program: backlog ship plan (docs sync)

## Intent

Design the Host Monte Carlo → **finite** `State` / Joint injection path under
ADR 0162: continuous and finite are different type worlds; the programmer (or
Host adapter they call) must write explicit finiteization before Kernel
execution. No Kernel `Continuous` mid-program value in this Issue.

## Design questions (Architecture Path)

1. Host Monte Carlo sampler contract: inputs, RNG port, sample count, seed.
2. How samples lower to a **finite** `State` / Joint support for Kernel inject
   (histogram / weighted atoms / lattice bins — choose explicitly).
3. Explicit approximation obligation / discretization provenance (ADR 0074
   family; no silent continuous→discrete truncation in theory lane).
4. Port shapes vs any Bridge sugar; keep Kernel surface free of `Continuous`
   values until a later ship ADR.
5. Ship ADR checklist before any Host adapter Red (still required; ADR 0162
   alone is not Red authorization).

## Non-goals (this Issue)

- Kernel `Continuous` value type
- Kernel implementation, tests, or status promotion to Feature Path Red
- Replacing ADR 0126 or weakening ADR 0162
- Technology selection of an HPC / cloud MC SDK

## Exit (design)

- [ ] Written Host→finite-State injection sketch reviewed by Adjudicator
- [ ] Sketch states type gate: continuous in → finite `State` out
- [ ] Ship ADR proposed only after surface + ports are concrete
- [ ] ADR 0126 / 0162 remain authoritative until that ship ADR
