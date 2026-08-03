# ADR 0185: Finiteize surface (Lane A) — no mid-program `Continuous`

## Status

**Accepted** (2026-08-03) — Adjudicator「A」on Architecture Path review
([LISS-0312](../documentation-compression-map.md);
[review](../../collaboration/reviews/2026-08-03-continuous-kernel-architecture.md)).

**Architecture approval only** for Lane A. Feature Path Red requires a named
Issue Plan (start: [LISS-0313](../documentation-compression-map.md))
and explicit Plan / Phase permission. This ADR is **not** Implementation
approval.

Companions:

- [ADR 0126](0126-continuous-pdf-design-boundary.md) — mid-program Continuous
  still **out** (Decision 1 maintained)
- [ADR 0162](0162-continuous-host-bridge-first.md) — Host/Bridge first;
  Decision 4 satisfied by this ship ADR for **finiteize surface**, not a
  Continuous type
- [ADR 0163](0163-host-mc-finite-state-inject.md) / [0164](0164-host-mc-inject-consumption-seam.md)
  — Host histogram inject + seam (shipped)
- [ADR 0074](0074-explicit-discretization-contract.md) — discretization provenance

## Context

Host Monte Carlo → finite inject is Runtime complete. Physicists still leave
the notebook for Python Host demos to finiteize continuous draws. Lane A
elevates that explicit finiteization step to a **Kernel-callable surface**
without introducing a mid-program `Continuous` type world (Lane B deferred).

## Dependency Adoption Evidence

Not applicable — reuses existing Host Monte Carlo ports; no new provider SDK.

## Decision

### 1. Lane A only

- **Ship:** notebook-facing **finiteize** that produces ordinary finite
  `State` / Joint.
- **Do not ship:** mid-program `Continuous<T>` (Lane B). That requires a
  **future** additive ADR after Lane A is Runtime complete and demand is clear.
- **Do not repark** Host-only forever (Lane C rejected).

### 2. Surface (MVP spelling)

Authorize a fail-closed Call form (exact grammar fixed in Feature Red):

```text
state psi = finiteize(/* Host-backed continuous → finite args */)
```

Normative intent:

1. Result type is finite `State` (or multi-name bind of finite States) — same
   Joint world as today.
2. Backend for MVP histogram path is ADR 0163/0164
   (`EqualWidthHistogramMonteCarlo` / `finite_inject_to_joint` lineage).
3. Required continuous → finite parameters remain Host-declared: interval,
   bin count, sample count / continuous draw, optional label mode (0164).
4. Provenance must carry ADR 0074 `discretization` block (0164).
5. Exact argument shape (positional vs named struct vs host profile id) is
   fixed in LISS-0313 Red against this ADR — do not invent a second continuous
   type universe while debating args.

Rejected for MVP: method form only; silent Host import without a notebook
token; mid-program `Continuous` values.

### 3. Semantics and gates

1. Finiteize is **explicit programmer-written finiteization** (0162 Decision 2).
2. After finiteize, NLTS / `when` / terminal `measure` rules are ordinary
   finite State rules.
3. **Forbidden:** measure / QPU emit on non-finite bags; silent truncation;
   adaptive/KDE bins; cloud MC SDK inside Kernel.
4. Soft/hard diagnostics for invalid interval / bins / empty support reuse or
   wrap Host `MonteCarloInjectError` codes — fail closed.
5. Effect story: finiteize may be marked Host-effecting if Red needs effect
   rows; it must not pretend to be pure unitary circuit.

### 4. Relation to Theory discretization

Theory `continuous_operator` + explicit discretization bridges (0074 / LISS-0111)
remain a **separate** path. Lane A does not merge Theory bridges into
`finiteize` MVP; a later ADR may unify vocabulary after both are taught.

### 5. What ADR 0126 still means

ADR 0126 Decision 1 stands: Kernel mid-program values are not continuous PDFs.
Lane A does **not** amend 0126 to add a Continuous type. It unseals a
**finiteize Call** whose inputs are Host continuous description / samples and
whose output is finite State.

## Non-goals

- Lane B mid-program `Continuous` (**expressiveness seats only** — see
  [continuous Lane B scenarios](../../specs/staqex-v1-continuous-lane-b-expressiveness-scenarios.md)
  / [LISS-0315](../documentation-compression-map.md);
  ship still requires a future ADR)
- Joint rational masses (0125)
- Live QPU continuous paths
- CUDA deferred workers
- Replacing Host Python APIs entirely (they remain valid Host adapters)

## Consequences

1. LISS-0312 Architecture investigation is complete.
2. Feature Path may be **planned** under LISS-0313; Red only after Plan
   approval (Grok) / Issue autonomy rules (Claude).
3. Agents must not implement Lane B ops under this ADR.
4. Official examples may teach `finiteize` once Green; Host demo remains valid.

## Implementation permission

| Item | Status after Accept |
|---|---|
| Architecture (Lane A) | **granted** 2026-08-03 |
| Technology selection | not required |
| Feature Plan (LISS-0313) | **requested separately** |
| Phase 1 Red / Kernel code | **forbidden** until Feature Plan + phase rules |

## Decision history

| Date | Event |
|---|---|
| 2026-08-03 | Proposed with Lanes A/B/C (recommend A) |
| 2026-08-03 | Adjudicator **A** → Accepted Lane A |
