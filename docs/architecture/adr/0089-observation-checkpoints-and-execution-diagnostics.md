# ADR 0089: Observation checkpoints and execution diagnostics

## Status

Accepted for [LISS-0044](../../issues/LISS-0044-observation-checkpoints-and-execution-diagnostics.md) Phase 1 Red.
This acceptance authorizes contract tests only. It does not authorize parser,
runtime, simulator, or provider implementation.

## Context

QPex is intended to let a physicist express a physical model, provide real
world data, and obtain a measured result from a simulator or quantum
computer. That workflow needs intermediate evidence for debugging and
validation. A classical debugger model is not sufficient:

- a simulator can inspect internal state vectors or density matrices;
- a QPU cannot expose its internal quantum state directly;
- an intermediate measurement changes the experiment and may require a
  separate circuit or Job;
- tomography and repeated observations have measurable resource cost.

The existing language law remains unchanged: `measure` is explicit and
terminal in the static Kernel lane. Job results are opaque Host DTOs and do
not expose `Joint`, AST, or simulator state as the normal result.

## Decision proposal

1. Add a future provider-neutral observation/checkpoint contract rather than a
   general-purpose quantum debugger.
2. An observation request names an observable, source location, execution
   stage, and requested result projection. It does not mean that the program
   may read a quantum state as a classical value.
3. Simulator-only diagnostics may optionally include a state-vector or density
   snapshot behind an explicitly simulator-scoped capability. Such snapshots
   must not be presented as QPU-equivalent results.
4. QPU checkpoints lower to explicit observation plans. Depending on the
   target, a checkpoint may produce a separate circuit/Job from the same
   initial preparation rather than a continuation of the original quantum
   state.
5. Every checkpoint and diagnostic result records provenance: source span,
   observable/effect identity, execution lane, Job identity when applicable,
   shots, seed policy, target profile, and approximation/mapping metadata.
6. The Host receives structured observation reports through the Job/JobResult
   boundary. The Kernel does not submit, poll, store, or print provider data.
7. Checkpoints are opt-in. No implicit measurement, tomography, state dump, or
   extra Job may be inserted by the compiler.

## Candidate surface

The exact syntax is intentionally open. A future design may use a declaration
such as:

```qpex
checkpoint after_prepare {
    observe energy(H)
    observe probability(|000>)
}
```

or keep the source surface declarative and attach observation plans from the
Host API. The accepted design must not make a simulator-only `snapshot` appear
portable to a QPU.

## Result boundary

The future provider-neutral report should distinguish at least:

```text
ObservationReport
  - checkpoint identity
  - observable identity and domain
  - probabilities / counts / expectation values
  - simulator-only snapshot reference, if explicitly requested
  - execution lane and target
  - Job identity and shot metadata
  - provenance and diagnostics
```

Raw `State<T>`, `DensityState<T>`, `Joint`, and provider SDK objects remain
outside the normal Host result contract.

## Non-goals

- No hidden mid-circuit measurement in the Static Kernel lane.
- No unrestricted state inspection on a QPU.
- No automatic tomography or automatic insertion of diagnostic Jobs.
- No provider SDK, credential, persistence, or logging implementation.
- No replacement of the Dynamic QPU lane owned by LISS-0028.
- No change to terminal `measure` semantics.

## Open decisions

- Is the first surface a QPex declaration or a Host API plan?
- Which observables are first-class: expectation, probability, counts, energy?
- Should a QPU checkpoint always be a separate Job, or may a dynamic target
  support a continuation form?
- How are checkpoint resource budgets and maximum extra shots declared?
- Is a simulator snapshot returned inline, by reference, or only written to a
  diagnostic sink?
- How do checkpoint reports compose with `WorkflowReport` and `JobResult`?

## Verification proposal

- Phase 1: simulator/QPU capability matrix, terminal-boundary negative tests,
  opaque-result tests, provenance tests, and explicit extra-Job accounting.
- Phase 2: one provider-neutral observation DTO and a local fake/simulator
  adapter; no live provider required.
- Phase 3: compare report readability and ensure no implicit observations were
  introduced.
