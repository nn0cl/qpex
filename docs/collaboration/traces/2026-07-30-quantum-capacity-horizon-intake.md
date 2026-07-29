# Optimistic quantum capacity horizon intake

- Date: 2026-07-30
- Branch: `codex/liss-0082-design-deepening`
- Operating path: Architecture Path
- Current phase: Phase 0 design intake
- Approved scope: project an optimistic facility-computer-to-household growth
  curve onto a household quantum-computer horizon, then derive a same-world
  quantum-supercomputer tier
- Implementation permission: **none**
- Post-review required: ADR 0110 architecture approval; every implementation
  phase remains separately gated

## Design result

- Start the scenario clock at `BQ-0`, a reproducible useful-computing and
  manufacturability breakthrough, not a roadmap date or first facility
  machine.
- Define QP-1 at `BQ+3–5` years as an early personal quantum workstation
  stress profile.
- Define QP-2 at `BQ+7–10` years as a mature household quantum computer
  stress profile.
- Derive QS-2 as the supercomputer tier in the QP-2 world rather than as an
  unrelated machine class.
- Apply a bounded 12–18-month doubling golden window after `BQ-0` to both
  capacity axes as an intentionally aggressive stress assumption, without
  equating classical FLOPS to logical qubits.
- Do not reuse ENIAC's 35-year social-adoption delay; assume the modern
  recognition, capital, manufacturing, and software-distribution ecosystem.
- Require compact hierarchical representation, exact/symbolic resource
  magnitudes, compositional failure evidence, and bounded materialization.

## Deterministic projection evidence

Reference arithmetic:

```text
RTX headline rate / ENIAC operation rate
  = 318e12 / 5_000
  = 6.36e10 over 79 years

equivalent annual factor ≈ 1.37
equivalent doubling interval ≈ 2.2 years

LineShine HPL / RTX headline rate ≈ 6.9e3
LineShine power / RTX board power ≈ 7.3e4

Golden-window capacity multiplier
  BQ+3 years: 4x–8x
  BQ+5 years: 10x–32x
  BQ+7 years: 25x–128x
  BQ+10 years: 102x–1,024x
```

The benchmark classes differ, so the facility/household comparison is retained
only as the broad `10^4–10^5` system-gap stress factor documented in the
scenario envelope. The 2.2-year result is retained as long-run historical
context, not the adopted post-breakthrough rate.

## Changed design ownership

- LISS-0082: compact hierarchy; no per-expanded-operation objects or
  diagnostics.
- LISS-0083: exact/symbolic multiplicity and resource magnitudes beyond
  unsigned 64-bit range.
- LISS-0087: pass complexity and materialization budgets against compact plan
  size.
- LISS-0091: compositional failure evidence and exact large resource counts.
- LISS-0099: synthetic QP-1/QP-2/QS-2 capability profiles.
- LISS-0120: exercise one representative source meaning against QP-2 and QS-2
  without expanded fixtures.

## Evidence boundary

Primary public records provide historical and roadmap seed values. Classical
and quantum operations are not equated. Dates and magnitudes are optimistic
architecture loads, not forecasts, product commitments, or language limits.

Detailed result:
[`docs/architecture/quantum-capacity-horizon-scenarios.md`](../../architecture/quantum-capacity-horizon-scenarios.md).

Proposed decision:
[`ADR 0110`](../../architecture/adr/0110-optimistic-quantum-capacity-horizon.md).

## Stop condition

Stop after documentation verification. Do not add compiler code, runtime code,
tests, provider dependencies, target adapters, or representative sample source.
