# Staqex v1 Physics IR golden catalog (LISS-0081 Slice E / LISS-0117)

| Field | Value |
|---|---|
| Status | **Fixture evidence — not a promoted runtime oracle** |
| Issue | LISS-0081; follow-up [LISS-0117](../architecture/documentation-compression-map.md) |
| Boundary | Python Shipping Kernel Physics IR DTO/inspection + golden loader |
| Last updated | 2026-07-29 |

This catalog records stable inspection expectations for the current Physics IR
boundary. Most families remain fixture-only. Oscillator has accepted
**lowered-IR evidence** via LISS-0117 Slices B–C (`verify_golden_against_lowered`
+ Equation/Unit checks). That is **not** a full six-family public runtime
oracle.

## Golden families

| Golden ID | Family | Required structure | Provenance | Status |
|---|---|---|---|---|
| `PIR-G-ISING-001` | Ising | tensor factors, Pauli products, symbolic coefficients, binder | required on each top-level record | fixture |
| `PIR-G-HEISENBERG-001` | Heisenberg | component operators, site order, binder, coefficients | required on each top-level record | fixture |
| `PIR-G-HUBBARD-001` | Hubbard | orbital/site domains, fermion statistics, atom order | required on each top-level record | fixture |
| `PIR-G-MOLECULAR-001` | Molecular electronic | orbital domain, fermion terms, coefficient ancestry | required on each top-level record | fixture |
| `PIR-G-OSCILLATOR-001` | Oscillator | continuous domain, symbolic units/coefficients, equation relation | required on each top-level record | **lowered-IR evidence** (LISS-0117 B/C) |
| `PIR-G-LINDBLAD-001` | Lindblad | density state, channel/jump references, evolution, measurement intent | required on each top-level record | fixture |

## Inspection contract

The current inspection API is:

```text
PhysicsModule -> inspect_physics_ir -> PhysicsInspection
```

Golden harness (LISS-0117):

```text
fixtures/*.json -> load_physics_ir_goldens
lower_hir_to_physics_ir + EquationNode -> verify_golden_against_lowered
```

Inspection is deterministic, immutable, and read-only. A record without a
recognized family or source origin fails verification with a named diagnostic.
Inspection does not expand gates, execute channels, insert measurements, solve
equations, discretize continuous domains, or select a provider.

## Promotion rule

These fixtures become a **full** public conformance oracle only after an
Adjudicator accepts lowered-IR evidence for all six families (or an explicit
subset policy ADR). Until then:

- global status remains **not a promoted runtime oracle**;
- oscillator may cite **lowered-IR evidence** from LISS-0117 B/C without
  promoting the other five families.

## Remaining work

LISS-0081 **complete** (Adjudicator closeout 2026-07-29). Deferred beyond
0081 (new Issues LISS-0119+ as needed):

- expand golden matcher / catalog promotion to the other five families for
  full public-oracle semantics (beyond LISS-0117 oscillator evidence);
- Equation auto-extraction inside `compile_source` (pipeline still lowers
  without equations; callers may pass `EquationNode`s explicitly via
  [LISS-0115](../architecture/documentation-compression-map.md));
- later numerical/discretization and Quantum Semantic IR (LISS-0082+) passes.

Shipped under LISS-0081 + WP-0028:

- Physics IR structural DTOs / verifier / inspection (0081 A–D + E catalog);
- HIR-to-Physics-IR lowering + soft compile wire —
  [LISS-0115](../architecture/documentation-compression-map.md) **complete**;
- Equation/Unit DTO module — [LISS-0116](../architecture/documentation-compression-map.md)
  **complete**;
- source-backed goldens — [LISS-0117](../architecture/documentation-compression-map.md)
  **A–C** (loader + oscillator lowered-IR evidence).
