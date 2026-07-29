# Staqex v1 Quantum Semantic IR plan (LISS-0082)

| Field | Value |
|---|---|
| Status | **plan intake** — Slice A Phase 1 Red gated |
| Authority | WP-0025 E2; ADR 0106 D9/D11; compiler blueprint §4.3 |
| Depends on | LISS-0075 complete; LISS-0081 complete |
| Shipping target | Python package `compiler/staqex` |
| Rust target | Deferred; shared contracts may be mirrored later |

## Design check

```markdown
[DESIGN CHECK]
- Scope and expected behavior: additive Quantum Semantic IR DTOs capturing
  finite executable quantum semantics shared by simulator and QPU planning;
  no provider types.
- Specifications and files inspected: WP-0025 LISS-0082 row; ADR 0106 D9/D11;
  compiler blueprint §4.3; LISS-0081 complete boundary; LISS-0080 HIR pattern.
- Component boundaries: new `quantum_semantic_ir.py`; UseCase-facing builder
  over immutable DTOs; no file/network/provider adapters.
- Applicable constraints: Clean Architecture; AT-TDD phase gates; Physics IR
  remains upstream inspection/algebra level.
- Decisions, assumptions, and unresolved ambiguities: Slice A names are
  design candidates until Red; soft compile wire deferred to optional Slice E;
  Dynamic QPU remains LISS-0077.
- Included and omitted AI context: include blueprint §4.3 and Issue body;
  omit provider SDKs, full evaluator, OpenQASM opcode catalogs.
- Task routing: docs/plan intake on capable assistant; Red/Green later on
  Kernel Python; deterministic `py_compile` / direct runners.
- Input/output evidence contract: N/A for docs intake; later Red asserts
  named diagnostics and immutable module shape.
- Verification plan: link check, claim sync, `git diff --check`; no compiler
  source changes in this intake.
```

## 1. Boundary

```text
Physics IR / Kernel contracts
  -> Quantum Semantic IR builder
  -> Quantum Semantic IR verifier
  -> later Algorithm Plan IR (LISS-0083)
  -> Logical QPU IR / simulator plans
```

Quantum Semantic IR is the backend-neutral level for **finite quantum
meaning**. It does not choose encodings, Trotter orders, shot plans, grids,
or providers. Those decisions belong to Algorithm Plan IR.

The builder is a UseCase-facing domain transformation over immutable DTOs. It
has no file, network, provider, database, RNG, or measurement-sink adapter.

## 2. Proposed DTO vocabulary

Names are design candidates, not implementation authorization.

- `SourceOrigin` / span reuse from Physics IR where practical.
- `ActingSpace`: finite carrier identity and dimension metadata.
- `TransformationRegion`: pure/mixed transformation with provenance.
- `UnitaryRegion` / `ChannelRegion` / `MeasurementRegion`: kind-tagged
  regions without opcode expansion.
- `ControlRegion`: static control structure markers (dynamic controller
  lifetime → LISS-0077).
- `ParameterSymbol`: symbolic parameter identity and provenance.
- `ResourceMarker`: linear / ancilla lifetime markers.
- `ExactnessMarker`: `Exact` vs approximate placeholder for later Plan IR.
- `QuantumSemanticModule`: immutable root of regions, markers, and origins.

## 3. Slice A acceptance boundary

- Importable module `compiler/staqex/quantum_semantic_ir.py`.
- Immutable root module DTO with provenance.
- Named verifier diagnostics for missing ancestry / invalid construction
  (non-compile-hard).
- Builder stub callable from tests without wiring `compile_source`.
- No Physics IR DTO edits; no evaluator changes; no QPU adapter changes.

## 4. Out of scope (Issue-wide)

- Numerical solving and simulator execution.
- Gate / matrix expansion and circuit synthesis.
- Jordan–Wigner and other mapping **execution** (LISS-0083).
- Provider SDK / OpenQASM-as-semantics / QIR-as-semantics.
- Equation DTO extension / auto-extraction.
- Algorithm Plan IR (LISS-0083), pass manager (LISS-0087).
- Soft `CompileResult` wire unless Slice E is separately approved.

## 5. Dependency and unlock graph

```text
LISS-0081 complete
LISS-0075 complete
    |
    +--> LISS-0082 (this Issue)
              |
              +--> LISS-0083 Algorithm Plan IR
              +--> LISS-0077 Dynamic QPU (also needs 0076)
              +--> later 0087 / Logical QPU consumers
```

## 6. Next allowed operation

After Adjudicator approval of this plan and the Issue body:

1. Stop — no implementation yet.
2. On separate approval: Slice A Phase 1 Red only
   (`tests/test_quantum_semantic_ir_slice_a_red.py`).
