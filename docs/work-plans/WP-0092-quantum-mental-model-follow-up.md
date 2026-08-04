# WP-0092: Quantum mental model and observation contract follow-up

| Field | Value |
|---|---|
| Status | **open — scientific-alias slice final-review-ready** (2026-08-04) |
| Branch | `codex/adr-quantum-mental-model` |
| Parent | [ADR 0189](../architecture/adr/0189-quantum-mental-model-and-observation-contract.md) |
| Scope | specification design only until a Phase 1 approval |
| Implementation | forbidden in this work plan until the target specifications and tests are reviewed |

## Goal

Turn the accepted ADR 0189 direction into reviewable language and semantic
specifications without changing the compiler, tests, grammar, or official
examples prematurely.

## Work units

1. **Scientific lexicon:** inventory compact Unicode spellings and short ASCII
   aliases such as `psi`/`ψ`, `phi`/`φ`, `rho`/`ρ`, `hbar`/`ℏ`, `dag`/`†`, and
   `tp`/`⊗`; define token classes, declaration contexts, diagnostics, and
   shadowing rules without introducing verbose mandatory names.
2. **Quantum composition surface:** compare `superpose` with at most two
   alternatives; define the distinction between mixture, coherent
   superposition, controlled unitary, and dynamic feed-forward; define the
   compatibility and migration rule for `when`.
3. **Observation contract:** define `Observable<T>`, `Projection<T>`, and
   `Observation<T>` candidates and the collapse/result contract for `expect`,
   `project`, `inspect`, `trace_out`, `measure`, and `tomography`.
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

- **Architecture approval:** ADR 0189 — complete.
- **Specification approval:** required before changing normative grammar,
  type rules, or observation contracts.
- **Phase 1 approval:** required before adding failing conformance tests.
- **Implementation approval:** required before lexer, parser, evaluator, IR,
  or example changes.

## Acceptance criteria

- One canonical scientific lexicon proposal with explicit compatibility rules.
- One selected quantum-composition spelling or a recorded unresolved choice.
- A typed observation matrix separating state-preserving operations,
  measurements, and Host protocols.
- A current-Kernel coverage matrix that distinguishes shipped, deferred, and
  semantically expressible capabilities.
- Conformance scenarios that can be reviewed independently from their future
  implementation.

## Phase 1 result

The proposed acceptance specification is now available at
[`staqex-v1-quantum-mental-model-follow-up.md`](../specs/staqex-v1-quantum-mental-model-follow-up.md).
It contains the first EARS/Gherkin scenarios but no executable tests. This is
intentional: the scientific lexicon, `superpose` spelling, and observation
type-layer are still review questions. Adding Red tests before those choices
are resolved would encode an accidental surface.

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
  unimplemented scientific inventory, `superpose`, observation types, and
  their later conformance work.
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
