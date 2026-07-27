# QPex v1 normative outline — §1 Introduction and §2 Lexical structure

| Field | Value |
|---|---|
| Status | Architecture Path draft (LISS-0068 slice 2) |
| Replaces (when promoted) | `qpex-language-specification.md` §1–§2 |
| Authority | ADR 0013–0105; ADR 0106 **Accepted with conditions** |
| Companion | [`qpex-v1-normative-rebaseline-register.md`](qpex-v1-normative-rebaseline-register.md) |
| Last updated | 2026-07-27 |

This document is the reconciled **outline** for v1 §1–§2. It resolves drift
IDs DR-001–DR-003 and DR-011 partial (header only) from the rebaseline register.
Promotion into the normative specification file awaits slice 3+ review; v0.1
remains the shipping conformance target until explicit version bump.

---

## Specification header (v1 target)

| Field | Value |
|---|---|
| Status | **Normative v1.0** (target; not yet promoted) |
| Conformance target | Reimplementable compiler / interpreter + SV harness |
| Decision log | ADR 0013–0105 in `docs/architecture/adr/` |
| North-star architecture | ADR 0106 (Accepted with conditions, 2026-07-27) |
| Formal grammar | `grammar/qpex.ebnf` (sync in slice 3+) |
| Verification | `docs/testing/qpex-spec-verification-protocol.md` (SV-01–SV-31) |

**Conformance:** unchanged law — accept Valid programs, reject Invalid with stated
diagnostics, match semantic rules (§5+ in full v1 spec).

---

## §1 Introduction

### §1.1 Purpose and design thesis (Normative)

QPex is a quantum–probabilistic programming language for physicists. Source
programs describe **joint state evolution**; classical collapse occurs only at
a terminal **`measure`** in the Static Kernel lane.

Three non-negotiable constraints (preserve v0.1):

1. **Never Leave the State** — mid-program quantum values are `State<T>` or
   `DensityState<T>` in a joint store; they do not become ordinary classical
   scalars except via lift boundaries or terminal measurement.
2. **Kotlin-like DX** — `package` / `fn` / `when` / `class` without classical
   `if` / `while` / exceptions / threads in the Static Kernel.
3. **Blackboard surface** — Type-First quantities, dimensional algebra, Dirac
   kets, Hamiltonian `evolve`, non-destructive `expect` / `inspect`.

**Informative north-star sentence** (ADR 0106 D1): QPex is an executable
notation for a physical theory, an experiment over that theory, and an explicit
plan for realizing the experiment on a simulator or quantum computer. Five-phase
`theory` / `experiment` / `workflow` / `execution` / `report` blocks are an
**additive** v1 extension; v0.1-valid programs need not use them (DR-008).

### §1.2 Execution model (Normative summary)

| Topic | v1 rule | ADR / Issue | Drift resolved |
|---|---|---|---|
| **Joint store** | Finite-support Joint; Born weight $\|c\|^2$ | 0013, 0014 | — |
| **Pure statements** | $\mathsf{Joint}\to\mathsf{Joint}$ transformers | 0013 | — |
| **Nondeterminism** | Terminal `measure` only (Static Kernel) | 0017, 0027 | — |
| **Evaluation order** | Left-to-right; args left-to-right | 0013 | — |
| **Concurrency** | No object-language threads | 0028, 0032 | — |
| **Explicit `return`** | Ordinary `fn` may end with terminal `return` as a **pure value boundary**; not observation | 0068 | DR-003 |
| **`main`** | `pub fn main() -> Unit`; results via terminal `measure` + Host envelope | 0064, 0027 | — |
| **Host execution** | Lifecycle outside the language; Job/JobResult contract is **Accepted** Host boundary | 0065 | DR-001 (header) |
| **Static QPU lane** | No ordinary classical control; static `forEach` elaboration; `QubitRegister<N>` normative | 0069 | DR-002 (partial) |
| **Parametric lane** | `Param<T>` symbolic parameters; QPU IR/OpenQASM preservation; Host binding validation **shipped** | 0070, LISS-0027 | DR-002 |
| **Dynamic QPU lane** | Separate `dynamic qpu fn`; capability rejection **shipped**; mid-circuit **execution deferred** | 0071, LISS-0028 | DR-002, DR-009 |
| **`evolve … until`** | Bounded pure repetition in Joint evaluator; QPU emission unsupported | 0079, LISS-0012 | DR-002 (README drift) |
| **Discretization bridges** | Explicit contract + MVP lowering (`Position`/`UniformGrid`/periodic FD) | 0074, LISS-0111 | DR-010 |
| **Multi-register mapping** | Named registers, `RegisterSet`, logical QPU identity; physical routing deferred | 0105 | DR-012 |
| **Reference implementation** | Python `compiler/qpex/` until Rust passes same conformance corpus | 0106 D12 | — |

**Removed v0.1 text:** “Parametric / Dynamic lanes are proposed extensions and
not part of this normative conformance target.”

**Replacement:** Parametric and Dynamic are **reviewed language lanes** with
documented conformance subsets. Static Kernel remains the default conformance
baseline; Parametric adds symbolic-parameter QPU programs; Dynamic adds only
the capability/rejection boundary until execution Issues land.

### §1.3 Terminology (Normative + extensions)

| Term | Meaning |
|---|---|
| **Static Kernel** | Default lane: NLTS, terminal `measure`, no classical control flow |
| **Parametric lane** | `Param<T>` gate parameters; Host binding before submit |
| **Dynamic lane** | `dynamic qpu fn`; `Controller<T>`; finite `match` only |
| **Value (quantum)** | `State<T>` or `DensityState<T>` in the joint store |
| **Joint** | Finite map: coordinate assignments → complex amplitude |
| **Vacuum** | Empty support; norm $0$ |
| **Lit-Lift** | Literals lift to Dirac `State` |
| **measure** | Terminal collapse (Static Kernel) |
| **Type-First** | `Type name = expr` (quantity heads the line) |
| **Dimension** | Exponent vector $\mathbf{d}=(L,M,T)$ |
| **Controller\<T\>** | Phase-local classical outcome of mid-circuit measurement (Dynamic lane only) |

### §1.4 Valid / Invalid (unchanged examples)

v0.1 §1.4 examples remain authoritative until promotion. Additional invalid
patterns are defined in companion lane specs and slice 3 diagnostic catalog.

---

## §2 Lexical structure

Normative companions: `docs/architecture/qpex-token-specification.md` (ADR 0035);
full productions in `grammar/qpex.ebnf` (grammar sync deferred to slice 3).

### §2.1 Character set, normalization, and identifiers

| Rule | v0.1 shipping | v1 target | Migration |
|---|---|---|---|
| Encoding | UTF-8 | UTF-8, **NFC-normalized** on read | LISS-0069 |
| Identifiers | ASCII `letter (letter \| digit)*` | + restricted UAX #31 Unicode profile | LISS-0069 additive |
| Case | Case-sensitive (`state` ≠ `State`) | Preserve | — |
| Confusables | — | Public identifiers: confusable diagnostics | LISS-0069 |

**During transition:** ASCII identifiers and ASCII Pauli atoms remain valid
(DR-006 staged removal).

### §2.2 Comments and whitespace

Unchanged from v0.1 §2.2.

### §2.3 Literals

| Form | v1 notes | ADR |
|---|---|---|
| Integer / Float | Underscore separators allowed (`1_000`, `0.5_0`) | 0101 |
| Unit suffix | Unchanged | 0037 |
| Ket (ASCII) | `\|0>`, `\|+>`, … remain valid | 0038 |
| Ket (Unicode) | `\|ψ⟩`, `\|0⟩` canonical **target** spelling | 0106 D5, LISS-0069 |
| Bra / adjoint / tensor | ASCII lowering paths until LISS-0069; Unicode canonical target | 0106 D5 |

### §2.4 Keyword triage

| Class | v1 additions / clarifications |
|---|---|
| **Active** | `theory`, `discretization`, `use` (bridge), scientific scope keywords per companion specs |
| **Contextual** | `until` inside `evolve … until … max N` (ADR 0079) |
| **Forbidden** | Unchanged (`if`, `while`, `throw`, …) |
| **Retired** | Unchanged (`observe`→`measure`, …) |
| **Lane markers** | `dynamic qpu fn` introduces Dynamic lane body (ADR 0071) |

Bare C-style `for (` remains ungrammatical. Lexeme `for` is contextual inside
`evolve … for …` and `forEach` only.

### §2.5 Pipeline vs Dirac tokens

- Pipeline: `|>` (left-associative, precedence level 1).
- Ket close delimiter `⟩` (U+27E9) is tokenized separately from `|>` so pipeline
  and Dirac syntax do not collide (ADR 0106 D5).

### §2.6 Valid / Invalid

v0.1 §2.5 examples remain valid. Slice 3 adds diagnostics for Unicode
confusables and illegal Dynamic/Static leakage at lexer/parser boundary.

---

## Drift resolution map (slice 2 scope)

| ID | Resolution in this outline |
|---|---|
| DR-001 | Header decision log → ADR 0013–0105; SV → SV-31 |
| DR-002 | §1.2 lane table replaces “proposed extensions” prose |
| DR-003 | §1.2 `return` row; axioms patch (companion file) |
| DR-006 | §2.3 staged ASCII/Unicode; removal in LISS-0069 |
| DR-007 | §2.1 notes `state` sugar remains until separate migration Issue |
| DR-008 | §1.1 informative five-phase note; additive only |
| DR-009 | §1.2 Dynamic row; §2.4 lane marker |
| DR-010 | §1.2 discretization row |
| DR-011 | Header SV-31; full protocol sync in LISS-0071 |

---

## Promotion checklist (before replacing v0.1 §1–§2)

- [ ] Adjudicator review of this outline.
- [ ] Slice 3 diagnostic catalog merge.
- [ ] EBNF diff for `until`, separators, scientific scope keywords.
- [ ] SV header/doc cross-links updated in same promotion PR.
- [ ] No `breaking` Unicode/Pauli removal until LISS-0069 migrator + corpus.

## Next slice

**Slice 4** — EARS/Gherkin acceptance envelopes per major capability.
