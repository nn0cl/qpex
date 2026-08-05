# LISS-0327: `HostInputPort` foundation (ADR 0194, Follow-up item 1)

## Metadata

- Local issue ID: LISS-0327
- Status/phase: **proposed** / `phase-0-design` (2026-08-05) — awaiting
  Plan approval before Phase 1 Red
- Type: Feature Path (Kernel — new `compiler/staqex/host_input_port.py`
  and `compiler/staqex/host_input_binding.py`; `Evaluator.__init__` gains a
  constructor parameter; `host.py`'s `submit_source`/`_submit_compiled`
  gain a `settings["inputs"]` passthrough. No grammar/parser/AST change.)
- Priority: P2
- Initial planning size: `S`
- Owner / agent: Claude Code
- Program: [ADR 0194](../architecture/adr/0194-host-input-port-and-selection-predicate-semantics.md)
  Follow-up item 1
- Depends on: [ADR 0194](../architecture/adr/0194-host-input-port-and-selection-predicate-semantics.md)
  (Accepted — this Issue implements Decisions 1–2 only, the port and its
  validation, not the predicate logic)
- Blocks: [LISS-0328](LISS-0328-selection-projector-predicate-execution.md)
  (real `project ... onto feasible(...)` execution, ADR 0194 Follow-up item
  2 — depends on this port existing)
- Branch: `feature/liss-0327-host-input-port`
- GitHub Issue / PR: none yet

## Intent

Implement ADR 0194 Decisions 1–2, the port foundation only — no predicate
logic (that is LISS-0328's scope):

1. **`HostInputPort`** (`compiler/staqex/host_input_port.py`): a `Protocol`
   with `get(name: str) -> Any | None`, plus `MappingHostInputAdapter`
   (wraps a plain `dict`), matching `MeasureSinkPort`/
   `TextIOMeasureSinkAdapter`'s existing shape exactly
   (`compiler/staqex/measure_sink_port.py`).
2. **`Evaluator` constructor injection**: `Evaluator.__init__` gains
   `host_input: HostInputPort | None = None`, stored as `self.host_input`.
   Matches the existing `measure_sink`/`rng_port` injection pattern
   (`runtime/evaluator.py:195-221`) — no behavior change for any program
   that doesn't reference it.
3. **`host.py` passthrough**: `submit_source`/`_submit_compiled` read an
   optional `settings["inputs"]: dict[str, Any]`, wrap it in
   `MappingHostInputAdapter` when present, and pass it to `Evaluator(...)`
   as `host_input=`. When `settings` has no `"inputs"` key, `host_input`
   stays `None` — fully backward compatible with every existing caller.
4. **`compiler/staqex/host_input_binding.py`** (mirroring
   `parametric_binding.py`'s shape): two new diagnostic codes,
   `HOST_INPUT_BINDING_MISSING` and `HOST_INPUT_BINDING_VALUE_ERROR`, and a
   `validate_matrix_binding(name, value, n, *, dtype, symmetric=True) ->
   list[Diagnostic]` function checking: the value is present (not `None`);
   it is an `n×n` sequence-of-sequences; every element matches `dtype`
   (`bool`, or finite non-negative `float`/`int`); and `value[i][j] ==
   value[j][i]` for every pair when `symmetric=True`. Diagonal entries are
   never validated (never read by any consumer).

## Explicitly out of scope

- Any `feasible(...)` predicate logic, or any change to the `project`
  runtime op's dispatch — that is LISS-0328's scope entirely. This Issue
  adds a port and a validator that nothing calls yet.
- Any change to `Param<T>`/`parametric_binding.py` — confirmed unrelated
  (QPU-circuit-parameter-specific, never reaches the local evaluator).
- Adding `HostInputPort` to `CLAUDE.md`'s "External Resources Must Be
  Ports" list — ADR 0194 Follow-up item 3, a separate documentation-only
  change requiring its own stated reason and AI work trace.
- Any S02-specific naming or hardcoded matrix content (Class E discipline)
  — this port is general-purpose, like `RngPort`/`MeasureSinkPort`.

## Acceptance reference

New Phase 1 scenarios (no existing spec section covers this yet — this
Issue's own Red test is the acceptance evidence, per the established
pattern for infrastructure-only Issues):

```gherkin
Feature: HostInputPort foundation

  Scenario: an injected host input is readable by name
    Given an Evaluator constructed with host_input bound to {"m": <value>}
    When code queries self.host_input.get("m")
    Then it returns <value>

  Scenario: no host_input injected behaves exactly as today
    Given an Evaluator constructed without host_input
    When any existing program runs
    Then behavior is unchanged (self.host_input is None)

  Scenario: a valid n×n symmetric boolean matrix passes validation
    Given a 3×3 symmetric Bool matrix
    When validate_matrix_binding is called with dtype=bool, n=3
    Then no diagnostics are returned

  Scenario: a missing binding fails closed
    When validate_matrix_binding is called with value=None
    Then HOST_INPUT_BINDING_MISSING is returned

  Scenario: a non-square or asymmetric matrix fails closed
    When validate_matrix_binding is called with a 3×2 matrix, or a 3×3
      matrix where value[0][1] != value[1][0]
    Then HOST_INPUT_BINDING_VALUE_ERROR is returned naming the violation

  Scenario: settings["inputs"] passes through host.run_source unchanged
    Given settings={"target": "local", "seed": 0, "inputs": {"m": [[True]]}}
    When run_source is called
    Then the Evaluator constructed internally has host_input.get("m") == [[True]]
```

## AI planning record (size S)

- Status: proposed, pre-Phase-1
- Authoring environment: Claude Code (Sonnet 5), this session
- Date: 2026-08-05
- Size: `S` — two small new modules following an exact existing pattern
  (`measure_sink_port.py`), one constructor parameter, one settings-key
  passthrough. No grammar, no typecheck rule, no new AST.
- Route: direct implementation by this session.
- Assumptions: `n` (matrix width) is supplied by the caller at validation
  time (LISS-0328 will read it from the actual bound selection pattern's
  tuple length at runtime) — this Issue's validator takes `n` as a plain
  parameter and does not itself discover it.
- Confidence: high — the port shape is a direct structural copy of
  `MeasureSinkPort`, verified by direct reading before drafting this Issue.
- Revision links: none yet.

## Exit criteria

- [ ] Phase 1 Red: acceptance tests for the six scenarios above exist and
      fail for a documented reason (`HostInputPort`/`host_input_binding`
      do not exist yet; `Evaluator`/`host.py` don't accept `host_input`/
      `inputs` yet).
- [ ] Phase 2 Green: minimal implementation makes those tests pass without
      editing them, without touching `Param<T>`/`parametric_binding.py`,
      and without changing any existing test's behavior.
- [ ] Phase 3 Refactor: no behavior change; reviewer empathy summary.
- [ ] Full regression: `pytest tests/ -q`, `python3
      tests/spec_verification/run_all.py`, `git diff --check`.
- [ ] ADR 0194's Follow-up item 1 checked off.

## Non-goals

- `feasible(...)` predicate execution (LISS-0328).
- `CLAUDE.md` port-list documentation update (ADR 0194 Follow-up item 3).
