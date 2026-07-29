# Staqex v1 Physics IR golden catalog (LISS-0081 Slice E)

| Field | Value |
|---|---|
| Status | **Fixture evidence — not a promoted runtime oracle** |
| Issue | LISS-0081 |
| Boundary | Python Shipping Kernel Physics IR DTO/inspection slices A–D |
| Last updated | 2026-07-29 |

This catalog records stable inspection expectations for the current Physics IR
boundary. The fixtures describe recognizable structure and provenance; they do
not claim that HIR-to-Physics-IR lowering, numerical execution, or Equation/Unit
DTOs are complete.

## Golden families

| Golden ID | Family | Required structure | Provenance | Status |
|---|---|---|---|---|
| `PIR-G-ISING-001` | Ising | tensor factors, Pauli products, symbolic coefficients, binder | required on each top-level record | fixture |
| `PIR-G-HEISENBERG-001` | Heisenberg | component operators, site order, binder, coefficients | required on each top-level record | fixture |
| `PIR-G-HUBBARD-001` | Hubbard | orbital/site domains, fermion statistics, atom order | required on each top-level record | fixture |
| `PIR-G-MOLECULAR-001` | Molecular electronic | orbital domain, fermion terms, coefficient ancestry | required on each top-level record | fixture |
| `PIR-G-OSCILLATOR-001` | Oscillator | continuous domain, symbolic units/coefficients, equation relation | required on each top-level record | fixture |
| `PIR-G-LINDBLAD-001` | Lindblad | density state, channel/jump references, evolution, measurement intent | required on each top-level record | fixture |

## Inspection contract

The current inspection API is:

```text
PhysicsModule -> inspect_physics_ir -> PhysicsInspection
```

Inspection is deterministic, immutable, and read-only. A record without a
recognized family or source origin fails verification with a named diagnostic.
Inspection does not expand gates, execute channels, insert measurements, solve
equations, discretize continuous domains, or select a provider.

## Promotion rule

These fixtures become a public conformance oracle only after an Adjudicator
accepts a stable HIR-to-Physics-IR builder contract and the corresponding
Equation/Unit DTO boundary. Until then, they are review evidence for the
additive DTO/inspection implementation only.

## Remaining work

Tracked as parallel follow-ups
([WP-0028](../work-plans/WP-0028-physics-ir-followup-parallelism.md)):

- HIR-to-Physics-IR builder and typed source extraction — [LISS-0115](../issues/LISS-0115-hir-physics-ir-lowering.md);
- full `EquationNode`, `Coefficient`, `Unit`, and dimensional algebra DTOs —
  [LISS-0116](../issues/LISS-0116-equation-unit-dto.md);
- source-backed golden loading rather than synthetic DTO fixtures —
  [LISS-0117](../issues/LISS-0117-source-backed-physics-ir-goldens.md);
- later numerical/discretization and Quantum Semantic IR passes.
