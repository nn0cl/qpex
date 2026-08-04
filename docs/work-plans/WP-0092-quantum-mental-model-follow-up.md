# WP-0092: Quantum mental model and observation contract follow-up

| Field | Value |
|---|---|
| Status | **open — observation-type slice shipped; composition taxonomy accepted via ADR 0190; remaining design/implementation slices open** (2026-08-04) |
| Branch | Design: `codex/adr-quantum-mental-model`; implementation: PR #342 (`abaa7cb`) merged |
| Parent | [ADR 0189](../architecture/adr/0189-quantum-mental-model-and-observation-contract.md); composition taxonomy refined by [ADR 0190](../architecture/adr/0190-s02-selection-boundary-and-mix-control.md) |
| Scope | specification design plus explicitly approved implementation slices |
| Implementation | `DiagnosticView<T>` classification shipped (PR #342); `mix` canonical grammar and `when` hard-retirement diagnostic shipped (PR #337, commit `321de3a`, under ADR 0190/WP-0093 Phase 2 approval); remaining grammar, conformance, and surface changes (scientific lexicon, `superpose`/`controlled` grammar) still require their own approval |

## Goal

Turn the accepted ADR 0189 direction into reviewable language and semantic
specifications without changing the compiler, tests, grammar, or official
examples prematurely.

## Work units

1. **Scientific lexicon:** inventory compact Unicode spellings and short ASCII
   aliases such as `psi`/`ψ`, `phi`/`φ`, `rho`/`ρ`, `hbar`/`ℏ`, `dag`/`†`, and
   `tp`/`⊗`; define token classes, declaration contexts, diagnostics, and
   shadowing rules without introducing verbose mandatory names.
2. **Quantum composition surface:** [ADR 0190](../architecture/adr/0190-s02-selection-boundary-and-mix-control.md)
   has already accepted the distinction between mixture (`mix`), coherent
   superposition (`superpose`), coherent controlled operation (`controlled`
   / `Ctl`), and dynamic feed-forward, and has already accepted the migration
   rule for `when` (retired, no compatibility alias, hard diagnostic). That
   taxonomy is restated in this general-language follow-up specification
   (§4.3/§4.4 of the acceptance specification). The `mix` grammar and the
   `when` → `RETIRED_KEYWORD` diagnostic (naming `mix` as the replacement) are
   **already shipped** in the Kernel (PR #337, commit `321de3a`, under the
   ADR 0190/WP-0093 Phase 2 implementation approval) — confirmed live: `state
   c = when(...)` now fails lexing with `RETIRED_KEYWORD: retired \`when\` →
   use \`mix\``, and the full spec-verification suite (including SV-02, the
   `mix`/`when` non-destructive-composition suite) passes 161/161. The
   remaining open work for this unit is only the `superpose` and `controlled`
   grammar, which are reserved names but not yet active syntax.
3. **Observation contract:** define `Observable<T>`, `Projection<T>`, and
   `Observation<T>` candidates and the collapse/result contract for `expect`,
   `project`, `inspect`, `trace_out`, `measure`, and `tomography`. The first
   implementation slice classifies `inspect` as `DiagnosticView<T>` while
   retaining the established terminal `measure` identity-bind behavior.
4. **Semantic IR boundary:** map the current finite Joint and limited density
   implementation to the future Hilbert-space/observable abstraction without
   claiming unsupported operations are shipped.
5. **Conformance plan:** write EARS/Gherkin scenarios for no implicit collapse,
   non-destructive observations, terminal measurement, capability rejection,
   scientific aliases, and `when` migration. Tests are not to be implemented
   until the scenarios receive Phase 1 approval.

## Included context

- ADR 0189 and DEC-0002 / DEC-0003 / DEC-0006.
- `staqex-language-axioms.md`, `adjudicator-language-vision.md`,
  `staqex-language-specification.md`.
- Shipping Kernel state, evaluator, mixed-state, physics IR, and capability
  contracts, only as evidence of current coverage and gaps.

## Omitted context

- Provider SDKs and live QPU integration.
- A premature choice of Hilbert-space storage, Rust data structures, or a
  numerical library.
- Breaking syntax migration and implementation phases.

## Approval gates

- **Architecture approval:** ADR 0189 — complete; ADR 0190 — complete for the
  `mix` / `superpose` / `controlled` / `when`-retirement taxonomy.
- **Specification approval:** required before changing normative grammar,
  type rules, or observation contracts.
- **Phase 1 approval:** required before adding failing conformance tests.
- **Implementation approval:** required before lexer, parser, evaluator, IR,
  or example changes.

## Acceptance criteria

- One canonical scientific lexicon proposal with explicit compatibility rules.
- One selected quantum-composition spelling or a recorded unresolved choice —
  satisfied by ADR 0190's `mix` / `superpose` / `controlled` taxonomy and
  `when`-retirement rule, restated in §4.3/§4.4 of the acceptance
  specification.
- A typed observation matrix separating state-preserving operations,
  measurements, and Host protocols.
- A current-Kernel coverage matrix that distinguishes shipped, deferred, and
  semantically expressible capabilities.
- Conformance scenarios that can be reviewed independently from their future
  implementation.

## Phase 1 result

The proposed acceptance specification is available at
[`staqex-v1-quantum-mental-model-follow-up.md`](../specs/staqex-v1-quantum-mental-model-follow-up.md).
It contains the first EARS/Gherkin scenarios. The observation type boundary
has since been implemented and merged in PR #342. The `mix` / `superpose` /
`controlled` / `when`-retirement composition taxonomy is no longer an open
review question — it was accepted by ADR 0190 (2026-08-04) and is restated in
§4.3/§4.4 of the acceptance specification. The `mix` grammar and `when`
retirement diagnostic from that taxonomy are also already implemented and
merged (PR #337). `superpose`/`controlled` grammar, the scientific lexicon,
public observation surface, and remaining conformance scenarios are still
review questions.

## Verification

Documentation-only verification for this work plan:

```text
git diff --check
```

No runtime or test suite is required until specification or implementation
files are intentionally included in a later phase.

## Phase 3 closeout — scientific-alias slice

- **Scope:** `psi`/`ψ`, `phi`/`φ`, `rho`/`ρ` state-name aliases and `cm(A,B)`
  commutator alias only.
- **Implementation:** parser-side alias registration and runtime binding
  resolution; source spelling and existing Joint axis names remain stable.
- **Review status:** `final-review-ready`; WP-0092 remains open for the
  unimplemented scientific inventory, `superpose`, and later conformance
  work. Observation types are no longer an unimplemented item: the first
  semantic classification slice shipped separately in PR #342.
- **Verification:** `python3 -m pytest tests/ -q` → `1188 passed`; `python3
  tests/spec_verification/run_all.py` → `161/161`, 100%; `git diff --check` →
  pass.
- **Reviewer empathy:** The alias table is isolated in
  `compiler/staqex/scientific_vocabulary.py`; parser registration preserves
  source names, and runtime resolution is used only when the corresponding
  state axis exists. This keeps the change narrow and avoids changing package,
  type-first, or paper-notation identifiers.
- **Remaining review focus:** confirm that preserving source spelling while
  sharing semantic identity is the desired long-term AST/IR contract before
  adding more scientific aliases.

## Implementation closeout — `mix`/`when`-retirement slice (verified pre-existing)

- **Scope:** `mix` as the canonical, non-collapsing probabilistic/classified
  composition keyword; `when` retired from the canonical surface with a hard
  `RETIRED_KEYWORD` diagnostic naming `mix` as the replacement; no
  runtime/parser fallback rewrite.
- **Commit:** `321de3a` (`feat(s02): establish mix and coherent selection
  surface`); PR #337. Landed the same day as ADR 0190 and predates this WP's
  §4.3/§4.4 update — this closeout only records and verifies what already
  shipped; it authorizes no new implementation.
- **Verification (this review):** live parse of `state c = when(coin()) {
  0 -> vacuum, 1 -> vacuum, }` fails lexing with `RETIRED_KEYWORD: retired
  \`when\` → use \`mix\``; `.venv/bin/python3 -m pytest
  tests/test_s02_selection_surface_red.py -q` → `4 passed`; `.venv/bin/python3
  tests/spec_verification/run_all.py` → `161/161`, 100% (includes SV-02
  `mix`/`when` non-destructive-composition suite).
- **Boundary:** `superpose` and `controlled`/`Ctl` grammar remain reserved
  names, not active syntax. This slice covers only `mix` and `when` removal.

## Implementation closeout — observation-type slice

- **Scope:** classify `inspect(state)` as `DiagnosticView<T>` in the compiler
  type layer without adding public surface annotations or changing the
  established `state viewed = inspect(psi); measure viewed` behavior.
- **Commit:** `abaa7cb` (`feat: type non-destructive observation views`); PR
  [#342](https://github.com/nn0cl/staqex/pull/342) merged.
- **Verification:** dedicated observation-type test, HIR slices C/D, effect
  marking, 161/161 specification checks, and `git diff --check` passed.
- **Boundary:** `Observable<T>`, `Projection<T>`, `Observation<T>`, public
  observation syntax, tomography execution, POVMs, and Host DTO conversion
  remain separate future decisions or implementation slices.
