# ADR 0055: Namespace, enum, and dotted scope resolution

## Status

**Accepted** (2026-07-23). Implemented in Kernel (with enum).

Companions: ADR 0054 (linker), ADR 0056 (struct/class/`this`).

## Decision

1. `namespace A.B { … }` (nested allowed); flatten to `namespace` lists on decls.
2. `enum Name { V0, V1, … }` → `EnumDecl`; values `Name.V0` / `A.B.Name.V0`.
3. Enum ↔ Int/Float literals → `ENUM_TYPE_MISMATCH` (no implicit conversion).
4. Dotted types/constructors: `Topology.ChainLattice`, `Physics.Parameters.SSHParams(…)`.

## Verification

`tests/test_oop_namespace_enum_struct.py`, `tests/test_namespace_and_class_methods.py`,
SV-09 example `10_topological_physics`.
