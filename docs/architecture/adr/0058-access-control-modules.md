# ADR 0058: Modern access control (`pub` / module / `_`)

## Status

**Accepted** (revised 2026-07-23). The public spelling is amended by ADR 0067.
Supersedes Java-style `protected` + mandatory
`module-info` exports.

Companions: ADR 0054 (linker), ADR 0055–0056 (OOP surface),
`docs/architecture/physicist-dx-harmony.md`.

## Decision

### Visibility (Rust / Go / Python style)

| Surface | Meaning | Access |
|---------|---------|--------|
| *(default)* | **module-private** | Same compilation module |
| `pub` | Public API | Cross-module / library boundary |
| leading `_` (or legacy `private`) | Class-private | Defining `class` / same file only |

- **`protected` is Forbidden** — no inheritance; compose + inject parameters.
- **`new` is Forbidden** — construct with `Type(...)`.
- Physicists write blackboard code with **zero modifiers** for local scripts;
  library authors mark exports with a short `pub`.

### Module metadata

`module-info.qpex` remains **optional / advisory**. Missing `exports` does
**not** produce `PACKAGE_NOT_EXPORTED_ERROR`. Multi-file examples (01–10) need
no ceremony.

Illegal `_` member access → `PRIVATE_ACCESS_VIOLATION_ERROR`.
Non-`pub` cross-module use → `MODULE_PRIVATE_ACCESS_ERROR`.

## Verification

- `tests/test_modern_oop_and_visibility.py`
- `tests/test_encapsulation_and_module_info.py`
- `examples/10_topological_physics/` (no `module-info` required)
