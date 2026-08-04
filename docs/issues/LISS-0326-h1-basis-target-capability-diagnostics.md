# LISS-0326: real `BASIS_MISMATCH_ERROR` / `TARGET_CAPABILITY_REJECT` for H1 theories

## Metadata

- Local issue ID: LISS-0326
- Status/phase: **design intake only — Plan approval withheld** (2026-08-05)
- Type: Feature Path (Kernel — `compiler/staqex/parser.py`,
  `compiler/staqex/ast_nodes.py`, `compiler/staqex/h1_authoring.py`; likely
  touches `compiler/staqex/target_capability.py`)
- Priority: P2 (test-suite-only blast radius; no shipped example uses
  `theory`/`experiment`)
- Initial planning size: `L` (larger than first assumed — see below)
- Owner / agent: Claude Code
- Program: [WP-0092](../work-plans/WP-0092-quantum-mental-model-follow-up.md)
  work unit 6
- Related: [LISS-0325](LISS-0325-h1-non-hermitian-operator-diagnostic.md)
  (the third H1 diagnostic gap found in the same investigation; split out
  because it needs no grammar change and LISS-0326 does — see below)
- Depends on: none technically, but shares `h1_authoring.py` with LISS-0325;
  sequence LISS-0325 first to avoid two Issues editing the same function in
  parallel
- Branch: none yet — design intake happened on
  `docs/wp-0092-h1-theory-diagnostic-honesty`, no implementation branch
  created
- GitHub Issue / PR: none yet

## Why this is not a same-size fix as LISS-0325

Initial assumption (rejected during design intake, recorded per the AI
failure/recovery pattern in
[`ai-failure-recovery.md`](../collaboration/ai-failure-recovery.md)): all
three `h1_authoring.py` diagnostics were assumed to be same-size, source-text
heuristics fixable by switching to structured AST fields that already exist.
That held for `NON_HERMITIAN_OPERATOR_ERROR` (LISS-0325) but not for the two
diagnostics here — direct source reading found no AST field to switch to,
because the source constructs these diagnostics claim to check are not
parsed into any AST node at all:

- `compiler/staqex/parser.py::_parse_h1_theory_members` (line 513) only
  recognizes `parameter` and `operator` tokens inside a `theory { ... }`
  body. Every other token — including `basis position_grid = UniformGrid(-1.0,
  1.0, 8)` and `coordinate site: Lattice<128>` from the existing Red test
  fixtures — falls through to the loop's unconditional `index += 1` (line
  573) and is silently discarded.
- `compiler/staqex/parser.py::_parse_h1_experiment_body` (line 590)
  classifies each source line by lexeme membership
  (`"mix" in lexemes`, `"evolve" in lexemes`, etc.). No branch matches
  `realize`, so a `realize qpu:CH0_STATIC_V1` line is silently dropped from
  the returned statement list — same discard pattern.

So `TheoryDecl` has no `basis`/`coordinate` field to consult, and
`ExperimentDecl.body` has no node carrying the `realize` target name,
because the parser never captured them. `BASIS_MISMATCH_ERROR` and
`TARGET_CAPABILITY_REJECT` are currently the *only* way this information
reaches a diagnostic — via raw substring matching on `source` — precisely
because there is nothing else to check against yet.

## What already exists and can be reused

`compiler/staqex/target_capability.py` has a real, structured capability
registry (`TargetCapabilityProfile`, `verify_capability_profile()`) — not a
stub. Its fixture profiles (`_FIXTURE_QUBITS`, line 17):

| profile_id | qubits |
|---|---:|
| `CH0_COMMON_PHYSICAL` | 2 |
| `CH1_DIGITAL_RESEARCH` | 4 |
| `NH5_REFERENCE` | 8 |

**`CH0_STATIC_V1`, the name the existing Red test uses
(`tests/test_h1_hamiltonian_authoring_red.py`), is not in this registry.**
A real `TARGET_CAPABILITY_REJECT` check needs a real target name to look up.

## Open design questions (Hard Stop — presenting for decision, not deciding unilaterally)

### Q1: Where do `basis`/`coordinate` live in the AST?

- **Option A (recommended):** add two optional fields directly to
  `TheoryDecl` — `basis: H1BasisDecl | None = None`,
  `coordinate: H1CoordinateDecl | None = None` — each a small dataclass
  (`name: str`, a captured expression or `TypeRef`, `span`). Matches both
  existing test fixtures exactly (each theory declares at most one of
  either). No speculative multi-basis/multi-coordinate support, consistent
  with not designing for a requirement nothing has asked for yet.
- **Option B:** a general `list[H1DomainDecl]` on `TheoryDecl` covering any
  future theory-body declaration kind. More extensible, but speculative —
  nothing today needs more than one basis or one coordinate per theory.

### Q2: How does a `state` become "bound to" a theory's basis/coordinate, for `BASIS_MISMATCH_ERROR`?

The mismatch test fixture is: `state spin = |+>` (a bare ket literal, no
theory linkage at all) then `spin |> evolve under PositionModel.H for 0.7`.
The non-mismatch case (not yet covered by any test, but implied) would be a
state actually prepared "over" the theory's declared basis/coordinate, e.g.
`state psi = prepare plus over LargeModel.site` (used verbatim in the
`TARGET_CAPABILITY_REJECT` fixture, for a different purpose).

- **Option A (recommended):** treat `H1Prepare` as needing the same
  structural fix as `basis`/`coordinate` — capture the `over <Theory>.<name>`
  target (if present) and the bound state variable's name, instead of just a
  `source_tokens` tuple. Then `BASIS_MISMATCH_ERROR` becomes a real,
  checkable AST correlation: find the `H1Evolve` statement's theory, find
  the `H1Prepare` that introduced the evolved state variable, and compare
  its declared `over` target against the theory's `basis`/`coordinate` name.
  No `state` origin found, or an origin that doesn't match → mismatch.
- **Option B:** narrow the check to only fire when a state carrier's
  *literal kind* (ket literal vs. `prepare ... over` call) disagrees with
  the theory's declared basis kind (discrete/qubit vs. continuous grid),
  without full provenance tracking. Smaller, but weaker — would not catch a
  `prepare ... over` call that names the *wrong* theory.

Option A is the more honest fix but is real new correlation logic, not a
one-line change. This is the single biggest reason this Issue is `L`, not
`S`/`M`.

### Q3: What does `TARGET_CAPABILITY_REJECT` actually compare?

- **Option A (recommended):** `coordinate site: Lattice<N>`'s `N` versus the
  named `realize qpu:<target>`'s `max_logical_qubits` from
  `target_capability.py`, via the same `verify_capability_profile()`
  function real (non-H1) target lowering already uses elsewhere — reuse, not
  reinvent.
- **Option B:** a new, H1-specific capability comparison, decoupled from
  `target_capability.py`. Rejected as a default — would duplicate logic that
  already exists and is real.

### Q4: The fixture references `CH0_STATIC_V1`, which is not a real profile. Fix the test or the registry?

- **Option A (recommended):** rewrite the existing Red test
  (`tests/test_h1_hamiltonian_authoring_red.py`) to `realize
  qpu:NH5_REFERENCE` (real, max 8) instead of the fictional
  `CH0_STATIC_V1`. `Lattice<128>` exceeds all three real fixtures, so the
  scenario's intent (128-site model rejected by a small real target) is
  preserved without inventing hardware. Consistent with this whole
  investigation's finding that the diagnostic's realism, not the test's
  exact wording, is what matters.
- **Option B:** add `CH0_STATIC_V1` as a new fixture profile to
  `_FIXTURE_QUBITS`, to avoid touching the existing test's source text. Adds
  a fixture whose only reason to exist is this one test.

## Explicitly out of scope (regardless of which options are chosen)

- `NON_HERMITIAN_OPERATOR_ERROR` — LISS-0325, independent, no grammar
  change.
- Any real physical carrier-kind taxonomy (discrete qubit vs. continuous
  grid vs. lattice site as first-class Kernel types). Q2's Option A is a
  provenance/naming correlation, not a physics-aware type system.
- Live QPU capability discovery — `target_capability.py`'s fixture profiles
  stay fake/local, per existing project boundary.
- Any change to `mix`/`superpose`/`controlled`/S02 surfaces (WP-0093).

## Recommendation

Q1-A, Q2-A, Q3-A, Q4-A — reuse existing patterns (`target_capability.py`,
optional-field-on-decl) everywhere a reuse option exists, and accept that
Q2's provenance correlation is genuinely new logic. Estimated shape: new
`H1BasisDecl`/`H1CoordinateDecl` dataclasses, `TheoryDecl.basis` /
`.coordinate` fields, `H1Prepare` extended with an optional `bound_to:
tuple[str, str] | None` (theory name, basis/coordinate name) and `state_name:
str | None`, a new `H1Realize` statement node capturing the target name, and
a correlation pass in `h1_authoring.py` replacing both substring checks.

## Verification plan (once Plan-approved)

Phase 1 Red keeps both existing scenarios from
`tests/test_h1_hamiltonian_authoring_red.py`
(`test_h1_basis_mismatch_is_a_physics_diagnostic`,
`test_h1_invalid_target_rejects_without_rewriting_the_model`) as the
acceptance baseline, plus new negative-control scenarios proving the fix is
not a renamed substring check:

```gherkin
Feature: H1 basis and target-capability diagnostic honesty

  Scenario: renaming the mismatched identifiers still fires the diagnostic
    Given a state prepared with no theory linkage, evolved under a theory
      with a declared basis, using different identifier spellings than the
      original fixture
    When the program is compiled
    Then BASIS_MISMATCH_ERROR still fires

  Scenario: an unrelated co-occurrence of the same words does not fire
    Given a source file containing an unrelated theory with a
      position-grid-named basis and an unrelated state literally named
      spin, with no dependency between them
    When the program is compiled
    Then BASIS_MISMATCH_ERROR does not fire

  Scenario: a correctly bound state does not fire
    Given a state prepared via `prepare ... over` the same theory's declared
      basis or coordinate, then evolved under that theory's operator
    When the program is compiled
    Then BASIS_MISMATCH_ERROR does not fire

  Scenario: a small declared coordinate size does not reject a real target
    Given coordinate site: Lattice<4> realized against qpu:NH5_REFERENCE
    When the program is compiled
    Then TARGET_CAPABILITY_REJECT does not fire
```

## Exit criteria

- [ ] Adjudicator decision on Q1-Q4 (or an alternative not listed here).
- [ ] Plan approval, after the decision.
- [ ] Phase 1 Red / Phase 2 Green / Phase 3 Refactor per the decided design.
- [ ] Full regression: `pytest tests/ -q`; `python3
      tests/spec_verification/run_all.py` → 161/161; `git diff --check`.
- [ ] WP-0092 work unit 6 row and the kernel stub registry's
      `BASIS_MISMATCH_ERROR`/`TARGET_CAPABILITY_REJECT` entries updated.

## Non-goals

- Physical carrier-kind type system.
- Live QPU capability discovery.
- Any WP-0093/S02 change.
