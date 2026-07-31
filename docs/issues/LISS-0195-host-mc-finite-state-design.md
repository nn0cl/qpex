# LISS-0195: Host Monte Carlo → finite State injection (design)

## Metadata

- Local issue ID: LISS-0195
- Status: **open** (design only — no Kernel Red)
- ADR boundary: [0126](../architecture/adr/0126-continuous-pdf-design-boundary.md) **maintained**
- Program: backlog ship plan (docs sync)

## Intent

Record the next design gate for continuous / Monte Carlo models without
shipping a Kernel `Continuous` type (NLTS / finite-support conflict).

## Design questions (Architecture Path)

1. Host Monte Carlo sampler contract: inputs, RNG port, sample count, seed.
2. How samples lower to a **finite** `State` / Joint support for Kernel inject.
3. Explicit approximation obligation / discretization provenance (no silent
   continuous→discrete truncation in theory lane).
4. Whether a follow-on **ship ADR** is required before any Host adapter Red.

## Non-goals (this Issue)

- Kernel `Continuous` value type
- Kernel implementation, tests, or status promotion to Feature Path Red
- Replacing ADR 0126

## Exit (design)

- [ ] Written Host→finite-State injection sketch reviewed by Adjudicator
- [ ] Ship ADR proposed only after surface + ports are concrete
- [ ] ADR 0126 boundary text remains authoritative until that ship ADR
