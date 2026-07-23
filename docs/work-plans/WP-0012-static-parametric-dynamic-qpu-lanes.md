# WP-0012: Static, parametric, and dynamic QPU lanes

## [DESIGN CHECK]

- Scope and expected behavior: revise ADR 0069 around a type-level static
  Hilbert shape and split Parametric and Dynamic QPU concerns into ADR 0070/0071.
- Specifications and files inspected: ADR 0036/0059/0065/0069, LISS-0016,
  LISS-0019, LISS-0026, QPU backend docs, and official OpenQASM/IBM/Braket
  documentation summarized in the research note.
- Component boundaries: `QubitRegister<N>` and static elaboration belong to
  the Kernel/QPU lowering boundary; `Param<T>` is symbolic circuit data;
  Host binding and dynamic capability negotiation belong to Host/QPU adapters.
- Applicable constraints: terminal `measure`, `State<T>` pre-measurement
  ontology, no provider SDK in the Kernel, no hidden Host fallback.
- Assumptions and ambiguities: `QubitRegister<N>` is the preferred surface;
  declaration syntax, resource profile ownership, parameter syntax, and
  dynamic effects remain review decisions.
- Included context: local ADR/spec/LISS artifacts and primary public
  OpenQASM/IBM/Braket documentation. Omitted: credentials, private provider
  data, SDK implementation details, and unrelated language features.
- Routing: strong reasoning for architecture; deterministic tools for links
  and document checks; later code assistant only after issue/phase approval.
- Verification plan: Markdown/path checks now; Phase 1 conformance tests per
  LISS-0027/0028/0029 later.

## Planned phases

1. Architecture review of revised ADR 0069 and ADR 0070/0071: complete.
2. Separate Phase 1 Red approvals for LISS-0027, LISS-0028, and LISS-0029.
3. Implement one lane at a time; do not mix provider selection with Kernel
   semantics.

## Current status

Architecture review: accepted by the Adjudicator on 2026-07-23.

Design documents are accepted. No implementation authorization is included;
the next gate is separate Phase 1 Red approval for LISS-0027, LISS-0028, and
LISS-0029.

Phase 1 Red tests are now staged in
`tests/test_static_parametric_dynamic_boundaries_red.py`; no production code
was changed.

Phase 2 Green: complete for the bounded type/diagnostic boundary. Static
register migration, symbolic QPU binding, and dynamic execution remain
separate follow-up slices. Phase 3 Refactor approval is required before further
cleanup or examples.

Phase 3 Refactor: complete for the bounded boundaries. Added
`docs/examples/qpu-lane-boundaries.md`, refreshed physicist-DX documentation,
and synchronized the three LISS records. Provider binding, resource profiles,
and dynamic execution remain explicitly open.
