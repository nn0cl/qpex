# LISS-0015: Effect marking for pure and measure-capable functions

## Metadata

- Local issue ID: LISS-0015
- GitHub issue: none
- Status: **Phase 3 reviewed**
- Phase: Feature Path complete for the fixed effect-marking MVP
- Type: language architecture + type system
- Priority: P1
- Initial planning size: L
- Current planning size: TBD
- Reclassification reason: n/a
- Owner/agent: TBD
- Related branch: none yet

## Summary

Define effect marking for `measure`-capable and host-effectful functions while
keeping ordinary `fn`, interface defaults, and class methods pure.

## Acceptance Notes

- [ ] Effect vocabulary and annotation syntax are specified.
- [ ] `measure`, `snapshot`, `inspect`, and host ports have explicit rules.
- [ ] Effect propagation through calls, generics, and modules is specified.
- [ ] Pure-function rejection diagnostics are testable.
- [ ] Terminal-collapse and port boundaries remain intact.

## Dependencies

- Parent: none
- Depends on: ADR 0018, ADR 0029, ADR 0030
- Blocks: effect-aware `until` and Trait method implementation
- Related: LISS-0012, LISS-0014, `io-reasoning-contracts.md`

## Adjudicator Decision Points

- [ ] Use a fixed effect set or extensible effect rows?
- [ ] Is `inspect` pure in language terms but host-effectful in delivery?
- [ ] Can effectful functions return State values?

## Context

- Included: purity, measurement, host sinks, module boundaries.
- Omitted: external provider implementation and secret storage.
- Assumptions: RNG remains behind `RngPort`.

## AI Planning Records

### AIP-0015-001

- Status: proposed
- Created at: 2026-07-23
- Planning size: L
- Intended execution route: Architecture Path only.
- Intended scope: effect contract and diagnostics.
- Estimation basis: typechecker, linker, and port boundary impact.
- Assumptions: no implementation until acceptance.
- Confidence: medium

## Verification

- Future purity/effect conformance suite after the design is accepted.

## Phase 1 Red record

- Added [`test_effect_marking_red.py`](../../tests/test_effect_marking_red.py).
- The Red contract covers the accepted annotation surface candidate
  `effects { Inspect }`, transitive purity violations, prohibition on returning
  a `State<T>` from a `Measure` function, and effect-aware pipeline stages.
- The suite is intentionally Red because the parser and typechecker do not yet
  implement effect annotations or propagation. No production code was changed.

## Phase 2 Green record

- Added `effects { ... }` to `FunDecl` and the function declaration parser.
- Implemented the fixed effect vocabulary `Measure`, `Snapshot`, `Inspect`,
  and `Host` with declaration validation.
- Added transitive call checks for declared function effects and the built-in
  `inspect` effect. `main` is the host-controlled terminal boundary and may
  invoke declared effects.
- Added hard diagnostics `EFFECT_DECLARATION_ERROR`,
  `EFFECT_VIOLATION_ERROR`, and `EFFECT_MEASURE_RETURN_ERROR`.
- Pipeline stages reject effectful calls with `PIPE_EFFECT_ERROR`; no runtime
  Job/provider behavior or extensible effect rows were added.

Verification: effect tests, all standalone tests, spec verification (165/165),
bytecode compilation, and `git diff --check` pass.

## Phase 3 Refactor record

- Extracted parsing of the optional effect clause into `_effects_clause` and
  centralized function effect-context selection in the type checker.
- Preserved the accepted fixed vocabulary, diagnostics, terminal measurement
  boundary, and pipeline behavior.

Reviewer empathy summary: the parser now has one named boundary for effect
syntax, while function checking makes the distinction between `main`'s host
boundary and ordinary function capabilities explicit without duplicating the
conditional in the body checker.

Verification: all standalone `tests/test_*.py` scripts, the effect contract,
spec verification (165/165), bytecode compilation, and `git diff --check` pass.

## Design Note

- Target behavior: make purity and host-observable operations explicit at
  function boundaries without allowing `measure` to become an ordinary
  `State` value or weakening the terminal-collapse law.
- Phase to execute next: Architecture review and ADR acceptance; Phase 1 Red
  is intentionally not started.
- Context included: ADR 0029 (Host I/O boundary), ADR 0030 (`inspect`),
  `staqex-mvp-discrete-pmf-arith-measure.md`, `staqex-job-based-host-execution.md`,
  the existing `FunDecl`/typechecker behavior, LISS-0012, and LISS-0013.
- Context omitted: provider SDKs, credentials, dynamic QPU semantics, and
  implementation of new syntax.
- VO/DTO candidates: a fixed `EffectSet` attached to function declarations and
  a propagated `EffectSummary` used only by type checking; no runtime Job or
  measurement-result value is introduced.
- Ports/adapters: `RngPort`, `MeasureSinkPort`, and future host ports remain
  adapter capabilities; the Kernel receives effect metadata but no concrete
  adapter.
- Suggested task routing: strong reasoning review for the architecture
  boundary, deterministic parser/typechecker checks after acceptance.
- Ambiguities requiring Adjudicator decision: effect annotation spelling,
  fixed effect vocabulary versus extensible rows, whether `inspect` is a
  language-visible host effect or a pure identity with delivery metadata, and
  whether effectful functions may return `State<T>`.

## Proposed architecture direction

1. Ordinary `fn` remains pure by default. Calling a function whose declared
   effects are not permitted in the current scope is a hard diagnostic.
2. Use a small fixed vocabulary for the first slice: `Measure`, `Snapshot`,
   `Inspect`, and `Host`. `Measure` is terminal-only; `Snapshot` and `Inspect`
   do not collapse the state; `Host` covers port-backed preparation/output.
3. Effects propagate transitively through calls and module exports. A caller
   cannot hide an effect by wrapping it in a pure-looking helper or pipeline
   stage.
4. `measure` remains a terminal statement and never produces an object-language
   classical return value. An effectful function may return `State<T>` only if
   its effect does not collapse or expose a sampled value; this point remains
   open for review.

## Architecture decision record

[ADR 0081](../architecture/adr/0081-effect-marking-and-propagation.md) is
Accepted (2026-07-24). Phase 1 must choose and test the exact annotation
spelling without changing the accepted effect boundary.
