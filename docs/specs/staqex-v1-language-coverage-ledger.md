# Staqex v1 language coverage ledger (Gate P1)

| Field | Value |
|---|---|
| Status | **Accepted** (2026-07-31) — **under revision**: Option B Open Topics-before-s1 ([program](staqex-v1-open-topics-before-s1-program.md)); S1 blocked |
| Authority | [rebaseline](staqex-v1-representative-program-rebaseline.md) Gate P1; [friction ledger](../architecture/physicist-source-friction-ledger.md) |
| Issue | [LISS-0124](../issues/LISS-0124-language-coverage-ledger.md) |
| Mission | [showcase mission lock](staqex-v1-showcase-mission-lock.md) (P2) |
| Option B | [open-topics-before-s1-program](staqex-v1-open-topics-before-s1-program.md) |
| Not | S1 authorization; silent ship of permanent-out topics |

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
| Typed surface `state x: State<Int>` | **open** | PARSE_ERROR (F-07) | **required after LISS-0129** | Scheduled ship (Option B) |
| Density / Lindblad general CPTP | **partial** | ADR 0057 numeric + 1q symbolic; A07 toy | optional | LISS-0131 boundary doc; no full-CPTP claim |
| `evolve until` | **shipped** | ADR 0079; LISS-0012; axioms | optional | Ledger reconciled (LISS-0130) |
| Continuous PDF / Monte Carlo | **open** | permanent-out pre-S1 | **out** | [permanent-out](staqex-v1-open-topics-permanent-out.md) |
| SI scale beyond (L,M,T) | **open** | permanent-out pre-S1 | **out** | same |
| Exact rational masses | **open** | permanent-out pre-S1 | **out** | f64 policy |
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

## 3. Open Topics — finalized for Option B (2026-07-31)

Authority: [permanent-out note](staqex-v1-open-topics-permanent-out.md);
[program](staqex-v1-open-topics-before-s1-program.md).

| Topic | In showcase? | Status note |
|---|---|---|
| Typed surface annotations | **required after LISS-0129** | Still **open** (F-07); scheduled ship |
| `evolve … until` | **optional** | **shipped** (ADR 0079 / LISS-0012); ledger reconciled |
| ADR 0057 density / Lindblad | **optional** (toy OK) | Runtime complete; **boundary doc** via LISS-0131 — no full-CPTP claim |
| Further `\|>` / currying | **out** | Minimal shipped; further expansion permanent-out pre-S1 |
| Further trait `impl` / effect rows | **out** | Core shipped; further expansion permanent-out pre-S1 |
| SI beyond (L,M,T) | **out** | permanent-out pre-S1 |
| Continuous PDF / Monte Carlo | **out** | permanent-out pre-S1 |
| Exact rational vs f64 | **out** | permanent-out pre-S1; f64 policy |
| Concrete live QPU IR | **out** | permanent-out pre-S1; ports only |

## 4. Known residuals (not showcase blockers if demoted)

| Residual | Status | Follow-up |
|---|---|---|
| Consume-on-return LINEAR on product/apply chains | partial / sample workaround | LISS-0126+ (from 0122/0123) |
| Namespace/`Float` method return runtime bind | partial | LISS-0126+ |
| Soft `MULTI_REGISTER_INDEX_AMBIGUOUS` false positive | partial | LISS-0126+ |
| Classical Type-First ⊕ State arithmetic | open/partial | LISS-0126+ |
| Sample hardcode params beside unused structs | Class E | P0 green reduces; style guard remains |

## 5. Gate implication

- **P0 examples health:** complete.
- **P1:** Option B in progress — permanent-out **Accepted**
  ([LISS-0132](../issues/LISS-0132-open-topics-permanent-out.md));
  remaining: LISS-0129 ship, LISS-0130 docs exit, LISS-0131 boundary.
  See [program](staqex-v1-open-topics-before-s1-program.md).
- **P2:** mission locked.
- **S1:** blocked until Option B program exit + Adjudicator S1 authorize.
