# Staqex v1 Physics IR plan (LISS-0081)

| Field | Value |
|---|---|
| Status | **complete** — Adjudicator global closeout 2026-07-29 |
| Authority | WP-0025 E2; ADR 0106; compiler blueprint §4.2 |
| Depends on | LISS-0073, LISS-0074, and LISS-0080 — all complete |
| Shipping target | Python package `compiler/staqex` |
| Rust target | Deferred; shared contracts may be mirrored later |

## 1. Boundary

```text
typed HIR
  -> Physics IR builder
  -> Physics IR verifier
  -> later algebra / discretization / Quantum Semantic IR passes
```

Physics IR is the optimization and inspection level for equations and
operator algebra. It preserves mathematical meaning and provenance. It does
not choose a numerical method, expand a binder, map statistics to qubits, or
emit executable target instructions.

The builder is a UseCase-facing domain transformation over immutable DTOs. It
has no file, network, provider, database, RNG, or measurement-sink adapter.

## 2. Proposed DTO vocabulary

Names are design candidates, not implementation authorization.

- `PhysicsSpan` / `SourceOrigin`: source identity, span, and optional parent
  origin for desugaring ancestry.
- `HilbertSpace`: carrier identity, local dimension, and tensor factors.
- `TensorFactor`: stable source-order identity and local carrier metadata.
- `Coefficient`: symbolic expression, unit, dimension, and exact source origin
  — **shipped** in `compiler/staqex/physics_equation.py` (LISS-0116).
- `OperatorNode`: operator family, domain/codomain spaces, operands, and
  statistics metadata where applicable.
- `BinderNode`: binder kind, ordered variables, domain, constraints, body, and
  expansion provenance (without expansion in this Issue).
- `EquationNode`: relation/equation kind, sides or dynamics, coefficients, and
  origin — **shipped** in `physics_equation.py` (LISS-0116); initial conditions
  / measurement intent remain optional later fields.
- `Unit`: symbol plus `(L, M, T)` dimension exponents — **shipped** in
  `physics_equation.py` (LISS-0116).
- `SymmetryNode`: named symmetry or conservation law with operands and origin.
- `PhysicsModule`: immutable root containing nodes, declarations, and source
  provenance.

All nodes require valid ancestry. Domain, unit, and statistics references are
validated by a lightweight verifier before a module is accepted.

## 3. Initial acceptance corpus

The corpus should be represented through existing source/type contracts and
small inspection fixtures, not through a new formula parser:

| Family | Required preserved structure |
|---|---|
| Ising | tensor factors, Pauli operator products, symbolic coefficients, sum binder |
| Heisenberg | component operators, site binder/order, coefficient structure |
| Hubbard | fermion statistics, creation/annihilation order, orbital/site domains |
| Molecular electronic | orbital domain, fermion terms, coefficient provenance |
| Oscillator | continuous coordinate/momentum symbols, units, equation relation |
| Lindblad | density-state/channel structure, jump operators, measurement intent |

The inspection projection must be deterministic and must show source ancestry
for every top-level node. It is not a numerical evaluator.

## 4. Ambiguity boundaries

The following require explicit Adjudicator decisions or a later ADR if they
become necessary:

- whether units are interned symbols or structured dimensional vectors;
- whether non-square operator codomains are enabled in this Issue or remain a
  follow-up to the existing operator-domain boundary;
- the exact canonical ordering policy for fermionic terms beyond preserving
  source order;
- whether continuous domains are represented symbolically only or may carry a
  typed basis descriptor;
- how existing `symbolic_ir.py` projections are bridged without duplicating
  semantics.

No choice is made here for a provider, numerical library, datastore, or exact
arithmetic technology.

## 5. Context ledger

### Included

- LISS-0073, LISS-0074, and LISS-0080 acceptance boundaries;
- WP-0025 LISS-0081 dependency and acceptance summary;
- ADR 0106 and the compiler blueprint §3–§4.2;
- v1 north-star equations, operators, binders, statistics, and Lindblad
  examples;
- existing HIR and symbolic IR module locations.

### Omitted

- unrelated frontend slices and provider/QPU implementation details;
- full runtime/evaluator source;
- Rust implementation and future QPU adapters;
- private data, secrets, and external provider documentation.

## 6. Routing and evidence contract

- Design and architecture boundaries: stronger reasoning review by the human
  Adjudicator.
- DTO/test conversion: code assistant after Slice A Red approval.
- Formatting, test execution, and import checks: deterministic tools.
- No external AI/model output is consumed as runtime data in this Issue.

If AI assistance is used for fixtures or projections, output must be structured
as source fixture → expected IR shape → source-origin evidence → verification
status. Unverified generated formulas must not become acceptance data.

## 7. Slice B plan intake

Slice B consumes the existing `OpBinder`, second-quantized operator families,
and symbolic provenance contracts. It introduces no source syntax and does not
call the finite binder expander or Jordan–Wigner mapper.

### Required retained structure

| Input | Physics IR evidence |
|---|---|
| `sum` / `product` | binder kind, ordered variables, domain, constraints, body, origin |
| nested binder | nested node identity and source order, without expansion |
| fermion/boson/spin/qubit family | family, domain, statistics, atoms, source order, origin |
| non-canonical fermion order | original order plus explicit canonical metadata |

### Slice B phase gate

The next allowed operation is Phase 1 Red tests only. Green implementation
requires review of those tests; mapping, expansion, evaluator changes, and
Phase 3 cleanup remain separately gated.

## 8. Slice C plan intake

Slice C preserves mixed-state/channel, measurement-intent, initial-condition,
and symmetry/conservation structure from existing typed contracts. It is an
inspection and semantic-boundary slice, not an execution or numerical-validity
slice.

Expected nodes are `ChannelNode`, `MeasurementIntent`, `InitialCondition`, and
`SymmetryNode`, each with source origin and domain references. The verifier will
reject missing origin/domain references with named diagnostics. Existing
`mixed_state.py`, `measurement.py`, observation contracts, and Lindblad source
forms are input evidence; their runtime behavior remains unchanged.

The next allowed operation is Slice C Phase 1 Red only after review of this
plan. No runtime, provider, numerical integration, hidden measurement, or
simulator changes are authorized by this intake.

## 9. Slice D plan intake

Slice D defines the deterministic inspection boundary for the six required
formula families: Ising, Heisenberg, Hubbard, molecular electronic,
oscillator, and Lindblad. It should consume Physics IR DTO fixtures or a later
HIR builder output; it must not introduce a formula parser.

The proposed `PhysicsInspection` contains ordered `InspectionRecord` values
with family, stable node identity, recognizable structure summary, and source
provenance. Repeated inspection of the same immutable module must be byte/value
deterministic. Missing family markers or provenance are named verifier errors.

This slice is inspection-only: no gate expansion, numerical evaluation,
discretization, mapping, provider selection, or simulator execution.

The next allowed operation is Slice D Phase 1 Red only after this plan and its
golden corpus boundary are approved.

## 10. Slice E plan intake

Slice E is a docs-only closeout boundary for the current Python DTO and
inspection slice. It will create a stable six-family golden catalog, document
the four `PHYSICS_IR_*` verifier diagnostics, and synchronize Issue/plan/trace
status. The catalog must distinguish fixture evidence from a promoted public
runtime oracle, following the conformance plan's oracle rule.

Slice E does not claim that HIR-to-Physics-IR lowering, full Equation/Unit DTOs,
or numerical execution are complete. Those remain explicit follow-up work if
the Adjudicator does not expand this Issue's accepted scope.

The next allowed operation is Slice E Phase 1 documentation/fixture preparation
after review of this closeout plan.

## 11. Slice E completion evidence

- Golden catalog: `docs/specs/staqex-v1-physics-ir-golden-catalog.md`.
- Diagnostic catalog: Appendix K.13, four non-compile-hard verifier codes.
- Follow-ups LISS-0115–0117 completed under WP-0028 (now closed).
- No HIR builder, Equation/Unit implementation, runtime, or backend change was
  made in Slice E itself.

## 12. Global closeout (2026-07-29)

Adjudicator closed LISS-0081 as **complete**. Structural Physics IR (A–D),
Slice E fixture/diagnostic docs, and follow-ups 0115–0117 satisfy the Issue.
Deferred beyond 0081: full six-family public oracle, equation auto-extraction
in `compile_source`, and Quantum Semantic IR (LISS-0082).
