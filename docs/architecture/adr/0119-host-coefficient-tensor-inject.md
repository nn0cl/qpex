# ADR 0119: Host coefficient tensor inject (in-memory)

## Status

**Accepted** (2026-07-31) — unlocks LISS-0150 under WP-0036.
Amends open Decision 7 of [ADR 0090](0090-scientific-input-and-parameter-binding.md)
for coefficient tensors only (geometry remains deferred).

Companions: ADR 0090; [ADR 0096](0096-indexed-operator-and-binder-surface.md);
[ADR 0118](0118-basis-binder-and-partial-float.md).

## Context

Kernel ND `Float[N][M]…` literals (LISS-0144) and classical partial binds
(LISS-0149) are shipped. ADR 0090 still deferred Host `CoefficientTensor`
contracts. Research programs need Host-owned coefficient matrices without
embedding Python/JSON/file paths in Kernel source.

## Decisions

### D1 — Host DTO

`CoefficientTensor` is an immutable Host-side value object:

- `name: str` (non-empty binding key)
- `shape: tuple[int, …]` (rank ≥ 1, each dim > 0)
- `values`: nested finite real floats matching `shape`
- `provenance: InputProvenance` (required)

Element count `∏ shape` must be ≤ `1_000_000` (same Kernel budget). Bool is
rejected. Non-finite floats are rejected.

### D2 — Kernel surface

Placeholder bind (no list literal):

```staqex
Float[N][M] h = host("h")
```

- `host("…")` is a Kernel **boundary marker**, not a `Host<T>` type value.
- The string is the Host binding key (may differ from the local name).
- Binder use remains full-rank for scalar coefficients: `h[p][q] * …`.

### D3 — Merge rules

At binder lowering, Host tensors overlay `_collect_float_arrays`:

1. Unknown Host key for a placeholder → hard `HOST_COEFFICIENT_MISSING`.
2. Shape mismatch (declaration vs Host) → `HOST_COEFFICIENT_SHAPE_ERROR`.
3. Same name supplied as **both** list literal and Host overlay → hard
   `HOST_COEFFICIENT_CONFLICT`.
4. Extra Host keys not referenced by any placeholder → hard
   `HOST_COEFFICIENT_UNKNOWN` (fail closed).

### D4 — Lane separation

Coefficient tensors are **classical Host data**, not `Param<T>` gate
parameters and not Kernel `Host<T>` types (`HOST_TYPE_IN_KERNEL_ERROR`
unchanged).

### D5 — Non-goals

File/CSV/HDF5 adapters; geometry; uncertainty flags; dynamic length;
`Param` tensors; provider SDKs; Kernel JSON/file syntax.

## Consequences

- `scientific_input.py` grows `CoefficientTensor` + validators.
- `Float[…] = host("…")` is accepted in typecheck (shape only).
- `lower_finite_binder_operators(unit, host_arrays=…)` (or equivalent Host
  bind helper) merges overlays before lookup.
- ADR 0090 Decision 7’s coefficient-tensor deferral is closed for this
  in-memory slice; geometry remains open.

## Deferred

Geometry Host contracts; file adapters; non-literal classical partial
indices into Host tensors beyond existing Kernel partial-bind rules.
