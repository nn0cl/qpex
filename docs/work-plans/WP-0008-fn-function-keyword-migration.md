# WP-0008: `fn` function keyword migration

## [DESIGN CHECK]

- Scope and expected behavior: replace canonical Staqex callable keyword `fun` with `fn` without backward compatibility.
- Specifications and files inspected: ADR-0024/0026/0035/0056/0066, LISS-0021, Staqex grammar, token specification, all official examples.
- Component boundaries, ports/adapters, and VO/DTO candidates: lexer token spelling, parser declarations, no runtime or host DTO change.
- Applicable constraints: one Staqex semantics across Python Kernel and future Rust VM; no Rust ownership semantics introduced.
- Decisions, assumptions, unresolved ambiguities: `fun` becomes retired; exact diagnostic code reuses `RETIRED_KEYWORD` unless the implementation review chooses a dedicated code.
- Included and omitted AI context: included language surface and examples; omitted provider SDKs, cloud adapters, and unrelated deferred LISS implementations.
- Task routing: strong reasoning for surface/ADR consistency; deterministic tools for inventory and tests; code assistant for mechanical migration after Green approval.
- Verification plan: Phase 1 Red tests, Phase 2 token/parser migration, full SV/QASM and source inventory.

## Execution status

- Phase 1 Red: complete.
- Phase 2 Green: complete; `fn` is active, `fun` is retired, and SV passes
  164/164 with QASM verification green.
- Phase 3 Refactor: complete; current documentation uses `fn`, while historical
  records and the negative test retain `fun` only to explain its retirement.
