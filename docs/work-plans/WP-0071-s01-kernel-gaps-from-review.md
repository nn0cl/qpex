# WP-0071: S01 review Kernel gaps (binder method return + when enum)

| Field | Value |
|---|---|
| Status | **complete** (2026-08-01) |
| Branch | `feature/wp-0071-binder-when-enum-gaps` |
| Discovery | [LISS-0223](../issues/LISS-0223-s01-language-physicist-review.md) |

## Issues

| ID | Title | Status |
|---|---|---|
| [LISS-0224](../issues/LISS-0224-method-returned-binder-evolve.md) | Method-returned finite binders must lower before evolve | **complete** |
| [LISS-0225](../issues/LISS-0225-when-on-enum.md) | `when` on classical enum control | **complete** |

## Order

1. LISS-0224 (OpBinder path — unblocks S01 Lattice→evolve)
2. LISS-0225 (`when(enum)` — unblocks enum-only scoring)
3. Re-wire S01 shake comments / evolve under lattice H; drop Float twins where
   enum `when` suffices (optional thin follow in same PR if green)

## Verification

```bash
python3 tests/test_liss_0224_method_returned_binder_evolve_red.py
python3 tests/test_liss_0225_when_on_enum_red.py
python3 -m compiler.staqex run examples/showcase/S01_quantum_disaster_response/main_disaster_response.sqx --seed 0
```
