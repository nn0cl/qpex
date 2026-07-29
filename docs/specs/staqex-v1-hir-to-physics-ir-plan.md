# Staqex v1 HIR-to-Physics IR lowering plan (LISS-0115)

| Field | Value |
|---|---|
| Status | **Slice A–B acceptance implemented; review pending** |
| Authority | ADR 0106; compiler blueprint §§3–4.2; LISS-0080 HIR plan |
| Depends on | LISS-0080 complete; LISS-0081 Physics IR boundary |
| Target | Python Shipping Kernel `compiler/staqex` |

## Design check

The additive builder consumes an immutable `HirModule` and an optional
`CompilationUnit` source index. It emits an immutable `PhysicsModule` while
preserving declaration identity, typed references, source ancestry, operator
atom order, binder structure, and channel domains. The evaluator and
`compile_source` pipeline remain unwired.

Included context is `hir.py`, `physics_ir.py`, the LISS-0080 and LISS-0081
plans, and the typed AST contracts needed for operator, binder, and channel
fixtures. Runtime, provider, numerical, parser, Equation/Unit, and backend
details are intentionally omitted.

No new port, adapter, dependency, or ADR is introduced. `SourceOrigin` is the
provenance value object and the existing Physics IR DTOs remain the boundary.
Verification is deterministic direct test execution plus `py_compile` and
`git diff --check`.

## Slice A–B acceptance boundary

- Slice A: HIR input produces an immutable Physics IR root with stable node
  identity, source provenance, and no evaluator rewiring.
- Slice B: typed operator atoms, unexpanded binders, and channel domains are
  retained without execution, gate expansion, or unit inference.
- Equation/Unit DTOs, measurement/symmetry extraction, invalid-input
  diagnostics, and golden loading remain follow-up slices.

