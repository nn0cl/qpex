# Quantum Semantic IR foundations research (2026-07-29)

## Purpose and scope

This note records primary-source evidence used to deepen the LISS-0082 design.
It is not a language specification, an accepted architecture decision, or
implementation authorization. Staqex's accepted axioms and compiler blueprint
remain authoritative when prior art differs.

The research question is narrow:

> Which IR structures help preserve state-valued quantum semantics, explicit
> measurement boundaries, linear ownership, region-local control, provenance,
> and backend independence without turning Staqex into a circuit DSL?

Provider SDK selection, gate-set selection, numerical methods, and target
capability negotiation are intentionally omitted.

## Findings

### 1. Value semantics can make no-cloning and data flow inspectable

QSSA models quantum operations as side-effect-free operations over quantum
values. Ordinary operations consume and produce quantum values, while a
verifier checks no-cloning constraints. The circuit is visible in SSA
definition-use chains rather than hidden behind mutable qubit references.

QIRO further distinguishes an input dialect with memory semantics from an
optimization dialect with value semantics. Its QuantumSSA form consumes and
returns quantum states and uses explicit data dependencies to enable
verification and transformation.

**Staqex inference:** Quantum Semantic IR should use immutable, generation-
bearing **Joint state** values. Factor/resource IDs identify coordinates inside
that Joint value and do not imply separability. The IR should not expose
physical-qubit pointers or mutable register references. This is a structural
consequence of Never Leave the State and the Joint store, not a wholesale
adoption of QSSA or QIRO.

### 2. Regions need locally defined semantics and scope

MLIR operations may own regions, operands, results, properties, and source
locations. Region semantics are defined by the containing operation, and
values are scoped to the region in which they are defined. Traits and
operation verifiers enforce operation-specific invariants.

**Staqex inference:** `unitary`, `isometry`, `channel`, `measurement`, and
control boundaries should be distinct region contracts. A single generic
control or transformation bag would leave the most important laws to
convention. Staqex need not depend on MLIR to adopt this structural lesson.

### 3. Terminal and adaptive measurement are different execution contracts

The QIR Base Profile describes unitary transformations followed by end-of-
program measurements. It forbids using a qubit after an irreversible action
and does not require instructions conditioned on measurement results.

The QIR Adaptive Profile removes that restriction: it permits mid-program
measurement, reading results, conditional forward branches, and subsequent
quantum instructions. This is an explicit target capability boundary.

OpenQASM 3 is an imperative language for communicating quantum programs to
hardware and includes real-time classical computation and feed-forward. Its
role is therefore lower than Staqex's scientific and semantic IRs.

**Staqex inference:** Static Kernel terminal measurement and Dynamic QPU
feedback must not share an ambiguous `ControlRegion`. Static Kernel remains
the default language law. Dynamic measurement control is a separate semantic
lane and capability obligation owned by LISS-0077. QIR and OpenQASM remain
possible target forms, never source semantics.

### 4. Uncomputation intent and synthesis should remain separate

Modular synthesis research on quantum uncomputation separates a declarative
uncomputation specification from the compiler's synthesis of an efficient
implementation. It also makes the safety conditions explicit.

**Staqex inference:** Quantum Semantic IR should carry ancilla lifetime and
uncomputation obligations or witnesses, but should not synthesize inverse
circuits or silently clear resources. Synthesis and optimization belong to
later planning or verified pass work.

### 5. Static shape and linear runtime values are separate concerns

Linear dependent type theory combines linear resources with unrestricted
index-level information. This provides a useful formal precedent for keeping
resource usage linear while dimensions and other shape facts remain static.

**Staqex inference:** finite acting-space shape is immutable semantic metadata.
State values consume and produce generations within that shape. Runtime
measurement/controller values may select behavior in the Dynamic QPU lane but
must not redefine acting-space shape.

## Adopt, adapt, reject

| Prior-art idea | Staqex treatment | Reason |
|---|---|---|
| SSA-like quantum value flow | **Adapt** | Makes whole-Joint-state flow and no-cloning inspectable without implying separable registers |
| Mutable qubit/register references as semantic identity | **Reject** | Conflicts with Never Leave the State and leaks lower-level realization |
| Operation-owned typed regions | **Adapt** | Makes unitary/channel/measurement/control laws locally verifiable |
| MLIR dependency in the Python Shipping Kernel | **Reject for LISS-0082** | Structural ideas are sufficient; dependency and Rust-generation choices are separate |
| Base/adaptive execution profiles | **Adapt as semantic lanes** | Separates terminal measurement from dynamic feedback without importing QIR semantics |
| OpenQASM/QIR as source or Semantic IR | **Reject** | They are target/interchange representations |
| Declarative uncompute obligation | **Adopt** | Preserves intent and safety without prematurely selecting synthesis |
| Gate, mapping, tolerance, or provider choices | **Reject from this IR** | Owned by Algorithm Plan, Logical QPU, Target IR, or adapters |

## Primary sources

- MLIR, [Language Reference](https://mlir.llvm.org/docs/LangRef/).
- S. Peduri et al., [QSSA: An SSA-based IR for Quantum
  Computing](https://arxiv.org/abs/2109.02409).
- A. Ittah et al., [QIRO: A Static Single Assignment-based Quantum Program
  Representation for Optimization](https://spcl.ethz.ch/Publications/.pdf/ittah_qiro.pdf),
  DOI 10.1145/3491247.
- QIR Alliance, [Base
  Profile](https://github.com/qir-alliance/qir-spec/blob/main/specification/profiles/Base_Profile.md).
- QIR Alliance, [Adaptive
  Profile](https://github.com/qir-alliance/qir-spec/blob/main/specification/profiles/Adaptive_Profile.md).
- OpenQASM, [Live specification introduction](https://openqasm.com/intro.html).
- M. Venev et al., [Modular Synthesis of Efficient Quantum
  Uncomputation](https://arxiv.org/abs/2406.14227), DOI 10.1145/3689785.
- M. B. Vákár, [A Framework for Linear Dependent Type
  Theory](https://lmcs.episciences.org/10009).

## Research limits

- The sources show useful IR patterns; they do not decide Staqex semantics.
- No claim is made that the cited IRs share Staqex's state-persistence axiom.
- CPTP, isometry, and unitarity proofs are not solved by this note. LISS-0082
  defines inspectable declarations and verifier obligations, not a theorem
  prover.
- Backend profiles can inform capability boundaries but cannot weaken the
  Static Kernel law.
