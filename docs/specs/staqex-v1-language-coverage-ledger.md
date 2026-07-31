# Staqex v1 language coverage ledger (Gate P1)

| Field | Value |
|---|---|
| Status | **Accepted** (2026-07-31) — P1 complete; P2 mission locked; binds S* required rows |
| Authority | [rebaseline](staqex-v1-representative-program-rebaseline.md) Gate P1; [friction ledger](../architecture/physicist-source-friction-ledger.md); agent Open Topics |
| Issue | [LISS-0124](../issues/LISS-0124-language-coverage-ledger.md) |
| Mission | [showcase mission lock](staqex-v1-showcase-mission-lock.md) (P2) |
| Not | implementation approval for Open Topics; not S1 `.sqx` authorization |

```markdown
[DESIGN CHECK]
- Scope: honest in/partial/out rows for showcase prerequisites.
- Seed: F-01…F-10 + shipped Kernel + Open Topics + ports/diagnostics/LINEAR.
- Ambiguity: “In showcase?” means default recommendation for the **locked**
  P2 mission; demotions still need Adjudicator approval.
```

## Legend

| Status | Meaning |
|---|---|
| **shipped** | Accepted + Kernel-usable for teaching / showcase |
| **partial** | Accepted intent with known residuals / soft obligations |
| **open** | Not accepted / not shipped (Open Topic or deferred ADR) |
| **axiomatic** | Intentionally restricted (Class A) — keep |

| In showcase? | Meaning |
|---|---|
| **required** | Future showcase must exercise or explicitly demote with approval |
| **optional** | May appear if mission needs it |
| **out** | Must not pretend shipped; omit or refuse honestly |

---

## 1. Friction-seeded surfaces (F-01…F-10)

| Surface / concern | Status | Where proven today | In showcase? | Follow-up |
|---|---|---|---|---|
| Classical `if` / `&&` / bare loops rejected; use `when` / `evolve` | **axiomatic** | B02; vocabulary Forbidden | required (teach `when`) | keep; pedagogy only |
| Named `Float` / struct field coeffs in `Operator` | **shipped** | ADR 0114; LISS-0121; B08 | required | none (F-02/F-05 closed) |
| Many-body binders `sum`/`product` + `Index<…>` | **shipped** | ADR 0096; LISS-0055 | optional | width/QASM hygiene as sample debt |
| Dirac paper spelling `⟨φ\|ψ⟩` | **partial** | `inner`/`outer` (ADR 0087) | optional | sugar later; function form OK |
| `expect` / `inspect` choreography | **shipped** | B04/B08/A06 | required | teach ≠ measure |
| Typed surface `state x: State<Int>` | **open** | PARSE_ERROR (F-07) | **out** | Open Topic; inference-only until ADR |
| Density / Lindblad general CPTP | **partial** | ADR 0057 numeric + 1q symbolic; A07 toy | optional | schedule or keep out of required rows |
| `evolve until` | **open** | Open Topic | **out** | ADR after `for`/`times` |
| Continuous PDF / Monte Carlo | **open** | Open Topic | **out** | — |
| SI scale beyond (L,M,T) | **open** | Open Topic | **out** | — |
| Exact rational masses | **open** | Open Topic | **out** | f64 policy stays |
| Multi-file `import` / modules | **shipped** | B09; A06; A11 | required | F-09 residuals tracked via P0 green |
| QPU / OpenQASM lanes | **partial** | B10 static; LISS-0097 CH0; dynamic P0 | optional | live provider **out** of showcase |
| Soft `QSEM_*` obligations | **partial** | most green samples | optional | honesty, not failure |

## 2. Shipped language core (required baseline)

| Surface / concern | Status | Where proven today | In showcase? | Follow-up |
|---|---|---|---|---|
| `state` / Never Leave the State + terminal `measure` | **shipped** | B01; axioms | required | — |
| Ket literals + `evolve … under … for/times` | **shipped** | B04; ADR 0037 | required | — |
| Operator algebra + Suzuki | **shipped** | B08 | required | — |
| `namespace` / `enum` / `struct` / `class` / `fn init` / visibility | **shipped** | B07; A06; ADR 0054–0056, 0058 | required | — |
| LINEAR resource discipline (true quantum) | **shipped** | LISS-0114; green samples | required | consume-on-return residuals → LISS-0126+ |
| Ports: RNG / Source / MeasureSink | **shipped** | Kernel runtime | required (architecture) | no provider SDK in showcase |
| Diagnostics fail-closed | **shipped** | LINEAR / TYPE / MODULE codes | required | — |
| Soft Physics / Semantic IR | **partial** | LISS-0082; A11 | optional | honest soft only |

## 3. Open Topics (agent contracts) — in or out

| Topic | In showcase? | Rationale |
|---|---|---|
| ADR 0057 full Lindblad CPTP | **out** (optional toy OK) | Partial ship; do not claim general open-system completeness |
| `evolve until` | **out** | Not accepted |
| `\|>` / currying specs | **out** | Not accepted |
| Trait `impl` / measure-effect on `fun` | **out** | Not accepted |
| SI beyond (L,M,T) | **out** | Not accepted |
| Continuous PDF / Monte Carlo | **out** | Not accepted |
| Exact rational vs f64 | **out** | f64 policy |
| Concrete QPU IR details | **out** | Ports only; no live QPU credentials |
| Typed surface annotations | **out** | F-07; inference-only |

## 4. Known residuals (not showcase blockers if demoted)

| Residual | Status | Follow-up |
|---|---|---|
| Consume-on-return LINEAR on product/apply chains | partial / sample workaround | LISS-0126+ (from 0122/0123) |
| Namespace/`Float` method return runtime bind | partial | LISS-0126+ |
| Soft `MULTI_REGISTER_INDEX_AMBIGUOUS` false positive | partial | LISS-0126+ |
| Classical Type-First ⊕ State arithmetic | open/partial | LISS-0126+ |
| Sample hardcode params beside unused structs | Class E | P0 green reduces; style guard remains |

## 5. Gate implication

- **P0 examples health:** basics (LISS-0122) + applied (LISS-0123) green catalogs.
- **P1:** this ledger — Open Topics are **out** unless scheduled above.
- **P2:** mission lock may only mark **required** rows as showcase obligations.
- Showcase Red/Green remains forbidden until P0+P1 complete **and** P2 locked
  ([rebaseline](staqex-v1-representative-program-rebaseline.md) §5).
