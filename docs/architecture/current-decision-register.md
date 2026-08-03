# Current decision register

This is the compressed developer-facing view of accepted architecture. The
numbered ADRs remain the detailed source records where they are still needed;
this page prevents developers from having to read the ADR history to discover
the current rule.

## Language and physicist-facing surface

The current theme-level reading surfaces are:

- [DEC-0002: State-first semantics](decision-themes/dec-0002-state-first-semantics-and-measurement.md)
- [DEC-0003: Language surface and physicist-first DX](decision-themes/dec-0003-language-surface-and-physicist-first-dx.md)
- [DEC-0004: Type-First scientific model](decision-themes/dec-0004-type-first-scientific-model.md)
- [DEC-0005: Quantum operations and runtime](decision-themes/dec-0005-quantum-operations-and-runtime.md)
- [DEC-0006: Host, QPU, and external ports](decision-themes/dec-0006-host-qpu-and-external-ports.md)

These drafts summarize the current reading surface. The source ADRs remain
authoritative until the migration register is accepted.

- **Never Leave the State:** mid-program values remain `State<T>`; classical
  collapse is terminal `measure` only. See
  [`staqex-language-axioms.md`](staqex-language-axioms.md), the language
  specification, and ADR 0095.
- **Physicist first:** ideal blackboard form takes priority over machine-
  convenient syntax. See
  [`adjudicator-language-vision.md`](adjudicator-language-vision.md) and
  [`physicist-dx-harmony.md`](physicist-dx-harmony.md).
- **One language, two generations:** Python `compiler/staqex/` is the shipping
  Kernel; Rust is the long-term VM/simulator target. Rust wording does not
  define a second language semantics.
- **Current surface:** `when`, `state`, `evolve`, `measure`, `fn`, `pub`,
  `namespace`, `enum`, `struct`, `class`, and explicit `State<T>` boundaries.

## Runtime and external boundaries

- Domain semantics do not depend on file systems, networks, providers, or
  framework SDKs.
- External resources enter through ports, including `RngPort`,
  `MeasureSinkPort`, and `SourcePort`.
- QPU providers remain adapters behind provider-neutral ports. A provider SDK,
  credential policy, or live network integration requires its own approval.
- Observation and measurement are explicit; diagnostics must not silently
  collapse a state.

## Documentation source of truth

- Language and architecture decisions belong in ADRs and normative
  specifications.
- Historical Issues, Work Plans, and Traces are indexed recovery records under
  [ADR 0187](adr/0187-documentation-source-record-compaction.md); their source
  files are deleted, while unresolved Issues and current review evidence remain
  full.

## Current implementation source

- Python package: [`compiler/staqex/`](../../compiler/staqex/)
- Language specification: [`../specs/staqex-language-specification.md`](../specs/staqex-language-specification.md)
- Open/deferred work: [`open-work-register.md`](open-work-register.md)
- Detailed accepted decisions: [`adr/`](adr/)

## Reading rule

Start here and follow only the linked canonical page or source record required
by the task. Historical execution prose is not normative unless a current page
explicitly points to it as required evidence.
