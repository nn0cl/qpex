# Research: theory-to-QPU feature roadmap

Status: **proposed roadmap — design only; no implementation authorization**

This note reconciles the requested theory-physicist notation coverage with the
shipping Kernel, the Static/Parametric/Dynamic QPU lanes, and the existing open
LISS register. It is a planning artifact, not a language specification.

## 1. Decision boundary

QPex should preserve two properties at the same time:

1. Mathematical expressions remain close to the notation used by theoretical
   physicists.
2. Theory, experiment, workflow, and execution concerns cannot silently mix.

The proposed solution is not to expose a general-purpose `Int` or a general
purpose classical builder inside the Kernel. Mathematical binders and typed
finite domains may be introduced in expression scopes; execution values remain
in the host/execution boundary. The final QPU target still receives a lowered
finite representation, not the source notation.

```text
theory expression
  -> symbolic operator/state IR
  -> resolved finite Hilbert representation
  -> QPU IR / simulator plan
  -> Job/Task execution boundary
```

The existing `State<T>` and terminal `measure` law remain authoritative. A new
notation feature must not introduce an implicit mid-program collapse.

## 2. Capability inventory

| Capability requested in the study | Current QPex position | Tracking |
|---|---|---|
| Static register and parameter lanes | Bounded slice implemented; final/resource work open | LISS-0026/0029, ADR 0069; LISS-0027, ADR 0070 |
| Dynamic circuits and feed-forward | Explicit boundary/rejection slice; execution semantics open | LISS-0028, ADR 0071 |
| Real QFT / IQFT | Deliberately deferred; no fake QFT | LISS-0010 |
| Density matrices, CPTP, Lindblad | Open architecture | LISS-0011, ADR 0057 |
| `evolve ... until` | Open | LISS-0012 |
| Pipeline, currying, trait implementation, effects | Open | LISS-0013–0015 |
| Host submission and Job result lifecycle | Kernel boundary/host adapter work | LISS-0016, LISS-0022 |
| Higher-order Suzuki and error bounds | Deferred | LISS-0017 |
| Numerical representation and continuous PDFs | Open research | LISS-0018 |
| Concrete QPU IR and backend lowering | Open | LISS-0019 |
| Mathematical finite sums, products, indices, and domains | Not yet a language surface | LISS-0030 |
| Bra-ket, adjoint, inner/outer products, commutators | Not yet a general operator algebra | LISS-0031 |
| Typed fermion/boson/spin operators and mappings | Not yet a surface or semantic boundary | LISS-0032 |
| Expression-preserving symbolic IR and provenance | Only specialized operator paths exist | LISS-0033 |
| Theory/experiment/workflow/execution separation | Architectural intent exists; no phase/resolver contract | LISS-0034 |
| VQE/QAOA and hybrid feedback workflow | Host Job exists as a boundary; workflow language is open | LISS-0035 |
| Continuous operators, integrals, derivatives, discretization | Finite-grid approximations only | LISS-0036 |
| POVM and general measurement/channel contracts | Not covered completely by the current pure-state surface | LISS-0037; dependency LISS-0011 |
| Semantic discrete carriers and phase-local types | `Int` roles are not yet fully separated | LISS-0038 |

The prior list's resource limits, target capability checks, mapping, Trotter
policy, and approximation reporting are not duplicated here. They are already
tracked by LISS-0017, LISS-0019, LISS-0022, LISS-0029, and the host/QPU ADRs.

## 3. New LISS slices

### LISS-0030 — Mathematical binders, finite domains, and indexed expressions

Define a pure expression surface for `sum`, `product`, finite domains, indexed
operators, boundary conditions, and binder scope. A binder is a mathematical
construction, not an imperative loop and cannot perform I/O, mutation, or
measurement. The design must distinguish meta-level dimensions/counts from
quantum-state carriers and must preserve the symbolic binder until resolution.

### LISS-0031 — General operator algebra and Dirac notation

Define the minimum algebra needed to write common quantum expressions directly:
bra/ket, adjoint, inner and outer products, expectation, projector,
commutator, anticommutator, tensor product, and operator domains/codomains.
The issue must state which constructs are surface notation, which are typed
operators, and which lower to existing Kernel primitives.

### LISS-0032 — Typed second-quantized operator families

Define distinct semantic families for fermion, boson, spin, and qubit
operators, including creation/annihilation operators, statistics, canonical
ordering, and an explicit fermion-to-qubit mapping boundary. A generic
`Operator` must not erase the algebra or Hilbert-space domain. Mapping choice
and introduced approximation/provenance must remain visible to later lowering.

### LISS-0033 — Symbolic expression IR and lowering provenance

Define a stable symbolic IR between source expressions and executable QPU IR.
It must retain sums, domains, operator products, mappings, discretization,
Trotter/Suzuki choices, and source provenance long enough for type checking,
optimization, diagnostics, and honest error reporting. This issue complements
LISS-0019; it does not select a backend or provider SDK.

### LISS-0034 — Phase-separated scientific program scopes

Define module/scope boundaries for `theory`, `experiment`, `workflow`,
`execution`, and result/report concerns. Source declaration order may be
deferred, but dependency direction must be strict:

```text
execution -> workflow -> experiment -> theory
report -> execution result
```

The issue must decide whether the surface uses named blocks, module kinds, or a
different mechanism. A builder/resolver may collect declarations, but the
mathematical expression body must remain formula-like and must not expose
backend, shots, retry, filesystem, or logging capabilities.

### LISS-0035 — Hybrid scientific workflow and feedback contract

Define VQE/QAOA-like workflows as an explicit host/workflow layer around a
closed experiment specification. The contract must cover parameter binding,
measurement result DTOs, optimizer iteration, convergence, cancellation,
reproducibility, and Job/Task composition without moving provider policy into
the Kernel. This extends LISS-0022 and LISS-0016; it does not authorize cloud
SDK integration.

### LISS-0036 — Continuous operator notation and discretization boundary

Investigate integrals, derivatives, wavefunctions, boundary conditions, and
continuous-domain notation. The issue must first decide whether these are a
QPex source-language capability, a symbolic front-end port, or an external
preprocessing boundary. Any discretization must be explicit and carry domain,
resolution, boundary, and approximation metadata.

### LISS-0037 — POVM, measurement, and channel contracts

Define general measurement effects, POVMs, projectors, classical result
carriers, and their relationship to density matrices/CPTP maps. Terminal
`measure` remains the default language boundary; mid-circuit measurement is
owned by the Dynamic QPU lane and cannot be added as an implicit shortcut.
This issue depends on the representation decisions in LISS-0011.

## 4. Dependency order

```text
LISS-0038 semantic carriers/phases
        |
        +--> LISS-0030 finite binders/domains
        |
        +--> LISS-0031 operator algebra
        |          |
        |          +--> LISS-0032 second quantization
        |          |
        |          +--> LISS-0033 symbolic IR/lowering provenance
        |
        +--> LISS-0034 scientific scopes/resolution
                         |
                         +--> LISS-0035 hybrid workflow

LISS-0011 density/CPTP ----> LISS-0037 POVM/channels
LISS-0018 numerical model -> LISS-0036 continuous/discretization
LISS-0019 QPU IR ----------> LISS-0033, LISS-0035
LISS-0022 Job boundary ----> LISS-0035
```

Recommended first design slice: LISS-0038, because indexed finite sums are
unsafe to specify while dimensions, indices, shot counts, and physical
discrete values still share an overloaded `Int` story. Its acceptance draft is
[`qpex-semantic-discrete-carriers.md`](../specs/qpex-semantic-discrete-carriers.md).
LISS-0030 follows after that carrier boundary is accepted.

## 5. Non-goals and honesty rules

- This roadmap does not claim that any new syntax is implemented.
- It does not reclassify the existing deferred QFT, Lindblad, Suzuki, host
  submit, or provider SDK work as complete.
- It does not add a general classical runtime to the QPU lane.
- It does not require QPex to replace OpenFermion, Qiskit Nature, PennyLane,
  symbolic algebra systems, or provider SDKs; adapters/ports remain a later
  technology choice.
- Every future example must label whether it is Kernel-executable, simulator
  only, QASM-emittable, or a source-level design fixture.

## 6. Acceptance evidence for later implementation

Each LISS needs its own reviewed acceptance specification and AT-TDD phase.
The minimum evidence should include:

1. A formula-to-QPex pair showing notation preservation.
2. A negative case proving that execution/host values cannot enter a theory
   expression.
3. A typed-domain or Hilbert-space mismatch diagnostic.
4. A lowering/provenance record when an approximation or mapping is introduced.
5. A boundary test proving that no implicit measurement occurs before the
   declared terminal boundary.
