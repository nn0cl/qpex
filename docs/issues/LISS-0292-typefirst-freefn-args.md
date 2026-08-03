# LISS-0292: Type-First object args on classical free functions

## Metadata

- Local issue ID: LISS-0292
- Status: **complete** (2026-08-03)
- Type: Feature Kernel (conformance residual; no new ADR)
- Priority: P1
- Parents: LISS-0277 residual notes; ADR 0174 field units; LISS-0231 classical free-fn
- Branch: `feature/liss-0292-typefirst-freefn-args`

## Problem

`Length r = road_m(qty)` with `qty` a class carrying Type-First fields failed:

```text
unbound coordinate `qty` while binding parameter `q` of `road_m`
```

Methods on the class worked. Pure Float struct free-fn args already worked.
Joint `_bind_user_fun` treated object Vars as state coordinates.

## Fix

1. Route classical Type-First return heads (`Length`, `Mass`, …) through classical free-fn evaluation (not Joint param bind).
2. Execute intermediate binds in free-fn bodies; resolve field units from free-fn locals.

## Exit

- [x] Red/Green tests
- [x] Multi-stmt + unit convert free-fn with class arg
- [x] Regression: Float struct free-fn
