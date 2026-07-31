# ADR 0139: Interference prune / support-merge MVP (Hold partial unseal)

## Status

**Accepted** (2026-07-31) — unlocks LISS-0171 under WP-0045.
Amends [ADR 0022](0022-quantum-native-optimizations.md) Hold for Interference
Pruning & Support Merging MVP only. Companion:
[`staqex-compiler-optimizations.md`](../staqex-compiler-optimizations.md) §3.

## Context

ADR 0022 documented support merge + zero prune as a future engine family.
The shipping Kernel already coalesces equal Joint atoms by summing complex
amplitudes on mixture / unitary / `interfer` paths (`_coalesce`). Adjudicator
unseals that family as an explicit MVP contract.

## Decisions

1. **Hold partial unseal.** Deferred Pushforward DAG remains Hold. Interference
   prune is authorized only for the MVP below. Operator Fusion (ADR 0137) and
   Trace-Out GC fn-scope (ADR 0138) stay as previously unsealed.
2. **Support merge.** Worlds with equal assignment (and equal coord-phase keys)
   coalesce by **summing complex amplitudes** (interference monoid on ℂ).
3. **Zero prune.** After merge, drop atoms with Born mass `|amp|² ≤ EPS`
   (existing Joint epsilon). No new `f64` vs rational threshold policy in this
   MVP (see ADR 0125 for exact-rational design boundary).
4. **Surface.** `Joint.merge_support()` is the named MVP entry wrapping the
   Kernel coalesce. Evaluator paths that already coalesce (`when`, unitary
   apply, `interfer`, …) remain authoritative; this ADR does **not** require
   silent coalesce on every `bind_pushforward` (carrier collapse must not
   invent Born mass via naive amp-sum without a follow-on renorm ADR).
5. **≠ `project`.** Merge/prune never apply a predicate subspace or Lüders
   renorm; cancelled atoms simply disappear (vacuum when all cancel).

## Non-goals

IR-level interference pass; forced coalesce-on-every-bind; Deferred
Pushforward scheduling of merge; density-matrix CPTP prune.

## Consequences

- Agents may call / rely on `merge_support` and existing coalescing eval paths.
- Destructive interference to exact zero yields vacuum (empty Joint).
- Agents must not treat this ADR as unsealing Deferred Pushforward.
