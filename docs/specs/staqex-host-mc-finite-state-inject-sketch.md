# Host Monte Carlo → finite State injection (design sketch)

| Field | Value |
|---|---|
| Status | **design sketch** — Adjudicator review requested |
| Issue | [LISS-0195](../issues/LISS-0195-host-mc-finite-state-design.md) |
| Strategy | [ADR 0162](../architecture/adr/0162-continuous-host-bridge-first.md) (**Accepted**) |
| Boundary | [ADR 0126](../architecture/adr/0126-continuous-pdf-design-boundary.md) maintained |
| Discretization family | [ADR 0074](../architecture/adr/0074-explicit-discretization-contract.md) |
| Implementation | **forbidden** until a separate **ship ADR** + Feature Path approval |

## 1. Type gate (non-negotiable)

```text
Continuous world          Finiteization (explicit)         Kernel world
─────────────────         ────────────────────────         ────────────
PDF / sample bag    →     Host adapter + provenance   →    State / Joint
continuous equation       (programmer invokes)             measure / QPU-bound
Host Monte Carlo                                           finite-support only
```

- **In:** continuous description or raw sample stream (Host-owned).
- **Out:** finite-support Kernel `State` (or Joint atoms with classical labels).
- **Forbidden:** Kernel mid-program `Continuous` value; silent grid choice;
  theory-lane truncation without provenance; QPU submit of continuous carriers.

## 2. Recommended MVP finiteization mode

**Weighted histogram (equal-width bins)** as the first inject mode.

| Choice | Why |
|---|---|
| Histogram bins | Matches ADR 0014 finite PMF; easy denotation checks |
| Equal-width on a declared interval | Forces programmer to name domain + resolution |
| Weights = normalized counts (or importance weights) | Born mass on Joint is `|amp|²`; classical inject uses real masses → amplitudes `√p` at bind |

**Deferred (not MVP):** kernel density estimates, adaptive bins, particle bags
kept as continuous objects, streaming online MC inside Kernel.

## 3. Host port sketch (provider-neutral)

Illustrative Python Host DTOs (not shipped; names may change in ship ADR):

```text
MonteCarloSpec
  domain_label: str              # e.g. "x" / "energy"
  interval: (float, float)       # [lo, hi)
  n_bins: int                    # resolution ≥ 1
  n_samples: int
  seed: int | None
  approximation: str             # e.g. "EqualWidthHistogram"
  provenance: mapping            # source PDF id, code hash, notes

FiniteStateInject
  coordinate: str                # Kernel State bind name
  atoms: list[(label, mass)]     # finite support; masses ≥ 0, Σ mass = 1 ± ε
  provenance: mapping            # must include MonteCarloSpec digest

HostMonteCarloPort (Protocol)
  sample_to_finite(spec: MonteCarloSpec, rng: RngPort) -> FiniteStateInject
```

- Entropy for **sampling** uses Host `RngPort` (or injected `random.Random`);
  this is **not** Kernel terminal `measure` entropy.
- Missing interval / `n_bins` / approximation tag → **fail closed** (no default grid).

## 4. Kernel intake (no Continuous syntax)

MVP intake stays **Host-side construction + existing Kernel finite binds**, e.g.:

1. Host runs `sample_to_finite`.
2. Host emits a finite Staqex fragment or API bind equivalent to
   `state s = …` over a **finite** support (explicit atoms / lattice labels).
3. Kernel typechecks `s` as ordinary `State<…>`; measure / evolve / QPU paths
   see only finite carriers.

**Not in MVP Kernel surface:** `Continuous`, `monte_carlo(…)`, or auto-inject
from PDF literals.

Optional later Bridge sugar (separate ship ADR), analogous to ADR 0074
`use Contract for Theory.Op as alias`:

```text
# ILLUSTRATIVE ONLY — not accepted syntax
use HistogramInject(spec=…) for Host.Samples as psi_finite
```

## 5. Provenance / approximation obligation

Every inject must carry (mirroring ADR 0074 spirit):

- domain + interval + resolution (`n_bins`)
- approximation method tag
- sample count + seed (or RNG digest)
- statement that support is **finite approximation**, not the continuous PDF

Compiler / Host validator rejects injects lacking these fields.

## 6. Relationship to existing mechanisms

| Mechanism | Role |
|---|---|
| ADR 0074 discretization | Continuous **operators** / grids → finite Ops |
| This sketch (LISS-0195) | Continuous **distributions** / MC → finite **State** |
| ADR 0051 position grid | Already-finite lattice wavefunctions in Kernel |
| ADR 0119 Host tensors | Precedent for Host→Kernel finite numeric inject |
| ADR 0126 / 0162 | Boundary + Host/Bridge-first strategy |

## 7. Ship ADR checklist (before any Red)

A future ship ADR must name at least:

1. Frozen DTO / port names and fail-closed diagnostics codes  
2. Exact mass→amplitude convention for inject  
3. Allowed label types (Int bin index vs Float bin center)  
4. Test plan: denotation under fixed Host RNG; reject missing provenance  
5. Explicit **non-goals:** Kernel `Continuous`; cloud MC SDK; QPU of raw samples  

**ADR 0162 alone does not authorize Red.**

## 8. Open questions for Adjudicator

1. Bin label: integer bin index vs representative float center (recommend **index**
   for MVP; centers as Host metadata)?
2. First Host API: library-only vs thin `host("…")` wiring like coefficient tensors?
3. Should ship ADR live as ADR 0163, or wait until WP-0062…0066 land to avoid
   number races?

## 9. Recommendation

Accept this sketch as the LISS-0195 design baseline: **Host histogram inject →
finite `State`**, programmer-supplied interval/resolution/provenance, no Kernel
`Continuous`. Defer ship ADR numbering until Adjudicator answers §8.
