# Staqex v1 HIR-to-Physics IR lowering plan (LISS-0115)

| Field | Value |
|---|---|
| Status | **complete** (Slices A–D; Phase 3 Refactor done) |
| Authority | ADR 0106; compiler blueprint §§3–4.2; LISS-0080 HIR plan |
| Depends on | LISS-0080 complete; LISS-0081 Physics IR boundary |
| Target | Python Shipping Kernel `compiler/staqex` |

## Design check

The additive builder consumes an immutable `HirModule` and an optional
`CompilationUnit` source index. It emits an immutable `PhysicsModule` while
preserving declaration identity, typed references, source ancestry, operator
atom order, binder structure, and channel domains. Slice D wires lowering into
`compile_source` as a soft artifact on `CompileResult` without making
`PHYSICS_IR_*` diagnostics hard-fail.

Included context is `hir.py`, `physics_ir.py`, `physics_ir_lower.py`, the
LISS-0080 and LISS-0081 plans, and the LISS-0116 Equation/Unit DTO contract.
Runtime, provider, numerical, parser, and backend details are intentionally
omitted.

No new port, adapter, dependency, or ADR is introduced. `SourceOrigin` is the
provenance value object and the existing Physics IR DTOs remain the boundary.
Verification is deterministic direct test execution plus `py_compile` and
`git diff --check`.

## Slice A–B acceptance boundary

- Slice A: HIR input produces an immutable Physics IR root with stable node
  identity, source provenance, and no evaluator rewiring.
- Slice B: typed operator atoms, unexpanded binders, and channel domains are
  retained without execution, gate expansion, or unit inference.
- Slice C: Equation/Coefficient/Unit records are consumed without rewriting
  DTOs or changing source order (complete on `main`).
- Slice D: `compile_source` exposes `CompileResult.physics_ir` via
  `lower_hir_to_physics_ir` without equations by default; soft
  `PHYSICS_IR_*` diagnostics only.

## Slice D verification

- Pipeline: `compiler/staqex/pipeline.py` (`CompileResult.physics_ir`).
- Lowering API: `compiler/staqex/physics_ir_lower.py`.
- Acceptance tests: `tests/test_physics_ir_lower_d_red.py`.
- Soft diagnostics only; equations still require explicit caller input.
- Verification: Slice D + C runners, `py_compile`, `git diff --check`.
