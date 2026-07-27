# QPex v1 normative rebaseline register

| Field | Value |
|---|---|
| Status | Architecture Path draft (LISS-0068 slice 1) |
| Owner | LISS-0068 / WP-0025 E0 |
| Normative target until rebaseline completes | `qpex-language-specification.md` v0.1 |
| Proposed v1 target | ADR 0106 (**Accepted with conditions**, 2026-07-27) + `qpex-v1-language-north-star.md` |
| Last updated | 2026-07-27 |

This register is the working inventory for LISS-0068. It does not supersede
v0.1 conformance or authorize compiler changes.

## 1. Purpose

LISS-0068 must produce one coherent, versioned normative v1 contract before
north-star lexer, parser, IR, or runtime implementation begins. Slice 1 records:

1. authoritative document precedence;
2. known specification drift between v0.1 prose and accepted ADRs;
3. an ADR-to-normative mapping skeleton for ADR 0013–0105;
4. a draft versioning policy;
5. open Adjudicator decisions that block later slices.

## 2. Authoritative stack (precedence)

| Layer | Artifact | Role during rebaseline |
|---|---|---|
| L0 | Accepted ADR 0013–0105 | Highest authority for decided language/process behavior |
| L1 | Companion specs under `docs/specs/` | Normative where cited by an accepted ADR or SV harness |
| L2 | `qpex-language-specification.md` v0.1 | Shipping conformance target; must be reconciled, not silently overridden |
| L3 | `qpex-v1-language-north-star.md` + ADR 0106 | Proposed target; non-normative until Adjudicator accepts ADR 0106 |
| L4 | `docs/architecture/*.md` umbrella notes | Informative unless they cite L0–L2; drift here is a documentation defect |

**Rule:** when L2 contradicts L0, L0 wins and L2 receives a tracked migration
entry in §4. Implementation behavior is evidence, not authority, unless an ADR
explicitly ratifies it.

## 3. Classification legend

Every reconciled item is tagged exactly one of:

| Tag | Meaning |
|---|---|
| `preserve` | v1 keeps current accepted behavior and surface |
| `additive` | v1 adds capability without breaking valid v0.1 programs |
| `breaking` | v1 requires migration; removal contract required |
| `bug` | v0.1 prose or umbrella doc is wrong; implementation + ADR already agree |
| `defer` | intentionally out of v1 normative scope; explicit deferral record |

## 4. Specification drift register

| ID | Drift | Authoritative resolution | Tag | Migration owner |
|---|---|---|---|---|
| DR-001 | `qpex-language-specification.md` decision log stops at ADR 0069 | Extend header/index through ADR 0105 in v1 rebaseline | `bug` | LISS-0068 |
| DR-002 | §1.2 labels Parametric/Dynamic lanes as non-conforming proposals | ADR 0070/0071 Accepted; type/runtime boundaries reviewed (LISS-0027/0028) | `bug` | LISS-0068 |
| DR-003 | `qpex-language-axioms.md` rejects `return`; ADR 0068 requires explicit terminal `return` in ordinary `fn` | ADR 0068 + normative §functions | `bug` | LISS-0068 |
| DR-004 | `docs/architecture/README.md` still lists Parametric/Dynamic and `until` as open despite WP-0027 completion | `open-work-register.md` + LISS-0012/0027 Issue records | `bug` | LISS-0068 |
| DR-005 | Historical “Phase 1 remains” prose for features with Phase 3 reviewed Issues | Issue/ADR status is authoritative; umbrella prose is stale | `bug` | LISS-0068 |
| DR-006 | ASCII `X`/`Y`/`Z` Pauli spellings vs v1 Unicode-first north star | ADR 0106 D4 + LISS-0069 migration | `breaking` | LISS-0069 |
| DR-007 | v0.1 `state` keyword vs north-star `State<T>` Type-First surface | ADR 0106 preserves NLTS law; spelling migration TBD at LISS-0069 | `breaking` | LISS-0069 |
| DR-008 | Scientific phase blocks (`theory`/`experiment`/…) are north-star only | ADR 0106 D1; not in v0.1 conformance | `additive` | LISS-0068+ |
| DR-009 | `dynamic qpu fn` lane not in v0.1 spec | ADR 0071 capability boundary; runtime mid-circuit still deferred | `additive` | LISS-0068 |
| DR-010 | Continuous bridge lowering absent from v0.1 spec body | ADR 0074 + LISS-0111 shipped MVP lowering | `additive` | LISS-0068 |
| DR-011 | SV protocol header lists SV-01–SV-17; harness implements through SV-31 | Extend v1 verification index to match harness | `bug` | LISS-0071 |
| DR-012 | Provider physical routing described as open while logical mapping is complete | ADR 0105 D6; Host/provider scope only | `defer` | post-MVP Host |

## 5. ADR inventory (0013–0105)

Status abbreviations: **A** Accepted, **P3** Phase 3 reviewed, **Pr** Proposed.

### 5.1 Core language semantics

| ADR | Status | Normative home (target) | Tag |
|---|---|---|---|
| 0013 | A | §semantics / axioms | preserve |
| 0014 | A | §representation (Discrete PMF) | preserve |
| 0016 | A | §amplitude lift | preserve |
| 0017 | A | §surface vocabulary | preserve |
| 0018 | A | §State/classical boundary | preserve |
| 0025 | A | §errors (no exceptions) | preserve |
| 0027 | A | §entry `main` + terminal `measure` | preserve |
| 0028 | A | §concurrency law | preserve |
| 0032 | A | §runtime model (DAG) | preserve |
| 0037 | A | §Type-First + dimensions + `evolve` times/for | preserve |
| 0038 | A | §Dirac / evolve / expect | preserve |
| 0039 | A | §`when` nesting ban | preserve |
| 0040 | A | §physical axiom typecheck | preserve |
| 0064 | A | §`main -> Unit` | preserve |
| 0068 | A | §`return` + lexical scope | preserve |
| 0079 | P3 | §`evolve until` | preserve |
| 0080 | P3 | §pipeline/currying surface | additive |
| 0081 | P3 | §effect marking | additive |
| 0095 | A | §design horizon (meta) | preserve |

### 5.2 Operators, evolution, and scientific notation

| ADR | Status | Normative home (target) | Tag |
|---|---|---|---|
| 0041 | A | §Hamiltonian / tensor / trace | preserve |
| 0045 | A | §unitarity diagnostics | preserve |
| 0049 | A | §Fock/grid quadrature | preserve |
| 0053 | A | §physicist surface | preserve |
| 0057 | P3 | §density / Lindblad boundary | additive |
| 0074 | P3 | §discretization contract | preserve |
| 0075 | P3 | §POVM / measurement contract | additive |
| 0087 | P3 | §operator algebra / Dirac | preserve |
| 0088 | P3 | §finite binder lowering | preserve |
| 0093 | P3 | §Jordan–Wigner mapping | additive |
| 0096 | P3 | §indexed binder surface | additive |
| 0098 | P3 | §binder constraint boundary | preserve |
| 0102 | P3 | §acting-space typing | preserve |

### 5.3 Modules, OOP, and visibility

| ADR | Status | Normative home (target) | Tag |
|---|---|---|---|
| 0024 | A | §packages / `when` / class | preserve |
| 0054 | A | §module import | preserve |
| 0055 | A | §namespace / enum | preserve |
| 0056 | A | §struct / class / `this` | preserve |
| 0058 | A | §`pub` / `_` visibility | preserve |
| 0061 | A | §config harvest | preserve |
| 0066 | A | §`fn` keyword alignment | breaking |
| 0067 | A | §`pub`-only visibility | breaking |
| 0082 | P3 | §interface / `system` | additive |

### 5.4 QPU lanes, IR, and backends

| ADR | Status | Normative home (target) | Tag |
|---|---|---|---|
| 0069 | A | §static QPU classical boundary | preserve |
| 0070 | P3 | §Parametric lane | additive |
| 0071 | P3 | §Dynamic lane capability | additive |
| 0077 | P3 | §QPU IR boundary | preserve |
| 0083 | P3 | §Host submit port | defer (Host) |
| 0085 | P3 | §QPU opcode vocabulary | preserve |
| 0086 | P3 | §QFT gate lowering | preserve |
| 0094 | P3 | §Trotter step policy | preserve |
| 0105 | P3 | §multi-register mapping | preserve |

### 5.5 Host workflow, observation, and resources

| ADR | Status | Normative home (target) | Tag |
|---|---|---|---|
| 0065 | A | §Job lifecycle (Host) | defer (Host) |
| 0072 | P3 | §hybrid workflow Host contract | defer (Host) |
| 0073 | P3 | §declarative workflow surface | defer (Host) |
| 0089 | P3 | §observation checkpoints | defer (Host) |
| 0090 | P3 | §scientific input binding | defer (Host) |
| 0091 | P3 | §JobResult observations | defer (Host) |
| 0092 | P3 | §local observation execution | defer (Host) |
| 0100 | P3 | §resource budget policy | defer (Host) |
| 0103 | P3 | §Host QPU orchestration | defer (Host) |
| 0104 | P3 | §QPU observation integration | defer (Host) |

### 5.6 Numeric policy and literals

| ADR | Status | Normative home (target) | Tag |
|---|---|---|---|
| 0076 | P3 | §numeric representation policy | preserve |
| 0097 | Pr | §numeric horizon (meta) | defer |
| 0101 | P3 | §numeric literal separators | additive |

### 5.7 v1 north star (proposed)

| ADR | Status | Normative home (target) | Tag |
|---|---|---|---|
| 0106 | Pr | v1 umbrella + migration boundary | — (requires Adjudicator acceptance) |

Rows marked `defer (Host)` remain out of Kernel conformance but need v1
appendix stubs so Host adapters do not fork semantics silently.

## 6. Companion specification map

| Spec | ADR anchor | Rebaseline action |
|---|---|---|
| `qpex-language-specification.md` | 0013–0069 baseline | Primary rewrite target |
| `grammar/qpex.ebnf` | 0035, 0068, 0079, 0101 | Sync after spec reconciliation |
| `qpex-kernel-classical-boundary.md` | 0069 | Mark reviewed complete |
| `qpex-parametric-circuit.md` | 0070 | Mark reviewed complete |
| `qpex-dynamic-qpu-lane.md` | 0071 | Capability vs runtime split |
| `qpex-continuous-discretization.md` | 0074, LISS-0111 | Add lowering MVP section |
| `qpex-multi-register-acting-space.md` | 0105 | Logical mapping complete; routing deferred |
| `qpex-v1-language-north-star.md` | 0106 | Becomes normative only after ADR 0106 Accepted |

## 7. Draft versioning policy

1. **Spec identity:** `qpex-spec` major.minor (e.g. `1.0.0` at rebaseline acceptance).
2. **Source markers:** programs may declare `qpex_version = "1.0"` in package metadata
   once LISS-0072 lands; until then, implicit v0.1 remains default.
3. **Diagnostic stability:** public diagnostic codes are immutable within a minor
   version; new codes may be added additively.
4. **SV coupling:** each spec minor bump updates the SV gate index; generated
   reports are not conformance oracles.
5. **Migration windows:** every `breaking` row in §4 requires a named LISS, a
   migrator contract (LISS-0069+), and a removal commit window before major bump.

## 8. LISS-0068 remaining slices

| Slice | Deliverable | Blocked by |
|---|---|---|
| 1 (this doc) | Drift register + ADR inventory + versioning draft | — |
| 2 | Reconciled v1 spec outline replacing v0.1 §1–§2 contradictions | — **complete** 2026-07-27 → [`qpex-v1-normative-outline-s12.md`](qpex-v1-normative-outline-s12.md) |
| 3 | Diagnostic catalog merge (language + Host appendix split) | — |
| 4 | EARS/Gherkin acceptance envelopes per major capability | Slice 2–3 |
| 5 | Migration/removal matrix for all `breaking` rows | ADR 0106 + LISS-0069 scope |

## 9. Verification (slice 1)

- Documentation-only; no `compiler/` or `tests/` changes.
- Local checks: path/link scan, `git diff --check`.
- Drift IDs DR-001–DR-012 are stable handles for later PRs.
