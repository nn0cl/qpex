# Language design re-review (2026-08-03)

| Field | Value |
|---|---|
| Status | **Design review** — findings for Adjudicator; P0 samples+docs batch authorized 2026-08-03 (LISS-0303) |
| Authority | Architecture Path intake |
| Motive | Adjudicator「言語的なデザインを見直して。モダンな言語デザインに寄せる形になればなお良い。運用方針は守る。改善点を提示」 |
| Parents | [vision](adjudicator-language-vision.md), [ADR 0095](adr/0095-design-horizon-ideal-form-first.md), [minimal dialect](physicist-minimal-dialect.md), [surface modernization north star](surface-modernization-north-star.md), [friction ledger](physicist-source-friction-ledger.md), WP-0088/0089 + LISS-0290–0302 |

```markdown
[DESIGN CHECK]
- Scope: re-score Staqex surface against physicist-first + modern-language
  aesthetics after WP-0089 adoption residuals; list improvement candidates.
- Not in scope: Kernel/sample edits; ADR acceptance; technology selection.
- Binding: NLTS / when-not-if / terminal measure; ideal form first; no
  gate-DSL-first; no Kernel async/try; AT-TDD / ADR gates.
- “Modern” here means: short chalk, records for data, explicit effects,
  module edges without enterprise FQN theater — **not** mainstream app-language
  fashion (async, exceptions, inheritance, GC-as-default story).
- Routing: Architecture Path / documentation only.
- Verification: Adjudicator rank / reject / authorize Issues or WP.
```

---

## 1. Policy preserved (non-negotiable)

Any modernization **must not**:

| Forbidden “modernization” | Why |
|---|---|
| Kernel `if` / `while` / bare `for` as Joint control | Axioms 3–4 |
| Mid-program collapse / Result-unwrap quantum | Never Leave the State |
| Gate-DSL-first rewrite of Hamiltonians | Vision §4 industry anti-pattern |
| Silent capability success | writeable ≠ executable honesty |
| Second semantics for “Rust only” | One language, two generations |
| Skip ADR for language surface ship | AT-TDD / approval model |

**Physicist mental model primary; programmer DX secondary but required.**

---

## 2. What is already strong (do not re-litigate)

### 2.1 Physics-facing core

- Ket / Operator algebra / `evolve under H` / `expect` / terminal `measure`
- `when` mixtures; LINEAR honesty; `tracing_out` leftover policy (ADR 0173)
- Type-First dimensions + SI `to` / mixed promote (ADR lineage)
- Dirac paper sugar `⟨φ|ψ⟩` (ADR 0165/0169)

### 2.2 Surface modernization already shipped (WP-0088/0089 + residuals)

| Lever | Status | Evidence |
|---|---|---|
| Default experiment profile (no package/`main` on singles) | **shipped** | B01, B08 |
| Local type inference | **shipped** | B08 `J = 1.0`, `H_chain = …` |
| Named struct construction | **shipped** | `Type { a: e }` |
| Selective + relative import | **shipped** | S01, applied, QMD |
| Classical Call in expr | **shipped** | ADR 0179 |
| struct + free-fn scores / Operator factories | **shipped** | S01 domain, B07, QMD |
| Nested free-fn + bare-pipe transitive link | **shipped** | LISS-0294–0295/0299 |
| Operator free-fn struct field coeffs | **shipped** | LISS-0297 |
| Trait surface examples parked (no ship) | **complete** | LISS-0196 採択 |

### 2.3 First-screen comparison

| Face | Today (honest) |
|---|---|
| **B01** | 2 lines — matches ideal dialect |
| **B08** | ~12 lines chalk — near north-star |
| **S01 spine** | multi-file + long classical prelude → Joint coda |
| **QMD** | better than pre-0298; still inspect museum + main ceremony |

**Judgement:** the **teaching spine (B01–B08)** is now modern-enough *as chalk*.
The residual enterprise feel is concentrated in **multi-file showcases** and a
few **dual-keyword / dual-constructor** seams — not in axioms.

---

## 3. What “modern language design” means here

Borrow *aesthetics* from modern languages without importing their physics sins:

| From modern langs | Staqex reading |
|---|---|
| Python notebook / Julia REPL | Experiment profile: short script, math first |
| Rust modules + `use` | selective import / relative `import .` / `use Enum.*` |
| Swift/Kotlin data records | `struct` default; `class` only for true systems |
| Swift named args / Rust struct init | `Type { field: expr }` |
| Explicit effect systems (research) | fixed `effects {…}` — already shipped core |
| Zig/Rust “no hidden control” | `when` / `evolve` honesty |

**Not** targets: Java beans, Spring FQNs, Qiskit gate soup, TypeScript `any`,
async Kernel, try/catch Joint control.

---

## 4. Improvement findings (ranked)

### P0 — highest leverage for “modern chalk” feel

#### P0-1. Multi-file still forces `package` + `pub fn main() -> Unit`

**Observation:** Experiment profile removes ceremony for **single-file** only.
S01 / QMD / A06 still open with package + main + long import blocks before any
ket appears.

**Modern gap:** first screen is still “module system demo,” not experiment.

**Directions (Architecture Path options — pick later):**

| Option | Idea | Risk |
|---|---|---|
| A | Multi-file **experiment entry** may omit `main` when file is marked entry | Design: entry discovery |
| B | **Import block demotion** in teaching: one “desk” import re-export file | Sample-only, no Kernel |
| C | Keep package/main for multi-file honesty; accept as module lesson | Zero Kernel cost |

**Recommendation:** B (sample composition) first; A only with ADR if still noisy.

#### P0-2. Dual bind spellings remain (`state x =` vs `Float x =` vs bare `x =`)

**Observation:** Inference allows bare `J = 1.0` and `H = …` in experiment
profile, but samples still mix `state s0 = |+>`, typed `Float t = …`, and bare
binds. Spec/docs still explain dual vocabulary (state keyword vs `State<T>`).

**Modern gap:** Swift/Rust-like languages have one primary bind story; we have
three pedagogies.

**Directions:**

| Option | Idea |
|---|---|
| A | **Teaching law only:** experiment profile always bare-or-state; Type-First heads only when unit matters |
| B | Sugar ADR: `let` / `:=` unified binder (maps to state vs classical by RHS) — high design cost |
| C | Keep dual; document decision tree in one page (status quo + docs) |

**Recommendation:** A + C now; B only if Adjudicator wants one keyword forever.

#### P0-3. Showcase inspect museums (QMD still, S01 partially sparse)

**Observation:** Minimal dialect and destructive sketch say **demote inspect
floods**. QMD still binds many `viewed_* = inspect(...)` before evolve.

**Modern gap:** notebook should have 0–1 peeks; Host owns logs.

**Recommendation:** sample-only Issues to strip QMD (and any remaining spine)
inspect seats to ≤1 sparse peek; no Kernel.

---

### P1 — language surface sugars worth Architecture Path (ideal form)

#### P1-1. Multi-bind sugar for classical tuples

Ideal dialect shows `J, h = 1.0, 0.5` and `s0, s1 = |+>, |+>`.
Today: parallel `state (s0,s1) =` exists for evolve results; classical multi
bind is uneven.

**Ship candidate:** classical / mixed multi-bind under experiment profile.
**Gate:** ADR; Red tests; no Joint hole for classical bags.

#### P1-2. Operator free-fn + method symmetry is almost done

LISS-0297 closed struct-field coeffs on free-fns. Remaining edge cases (ledger):
class receivers without intermediate Float; multi-level Attr; nested OpAttr.

**Recommendation:** small Kernel residual Issue only if sample friction returns;
not a fashion ADR.

#### P1-3. `use` ergonomics incomplete vs modern modules

Have: `use OpsPhase.*` for when arms.
Missing vs Rust/Swift feel: `use path::{A as B}`, re-export `pub use`, import
aliases for free-fns.

**Recommendation:** ADR only if S01 import lists stay painful after P0-1B.

#### P1-4. Enum / pattern when still slightly ceremonial

`when (board.phase) { Tonight -> …, else -> … }` is good.
Gap: exhaustive when without `else` when enum is closed; pattern bind on
struct fields (modern match).

**Recommendation:** exhaustive closed-enum `when` is high physicist value;
struct patterns lower priority.

#### P1-5. Effect surface is correct but invisible in samples

Fixed `effects { Inspect, Host }` is modern (explicit capabilities). Official
samples almost never show it; physicists only see LINEAR / soft QSEM.

**Recommendation:** one basics or B-tier sample that **declares** effects on a
helper — pedagogy, not new vocabulary. LISS-0196 parked expansion stands.

---

### P2 — polish / consistency / honesty

#### P2-1. Constructor duality: `Type(…)` vs `Type { … }`

Both legal (positional vs named). Modern languages usually prefer one default.

**Recommendation:** style guide — **named for ≥3 fields / units**; positional for
2-scalar chalk packs. Docs + sample lint later; no Kernel ban.

#### P2-2. Free-fn vs method for pure scores — settled, enforce in reviews

Policy is clear (struct + free-fn). Remaining intentional `class`: interface
impl (S01 squads), mutable clocks (A06/A10/QMD), harvest (B09).

**Recommendation:** PR checklist bullet; no new Issue unless violations return.

#### P2-3. Package root `examples.…` is good; depth still long

`examples.showcase.s01_disaster.day2_lane` reads as product path, not physics.

**Recommendation:** optional shorter package aliases for showcase lanes (docs +
convention); ADR only if path resolution needs change.

#### P2-4. Soft `QSEM_*` on “green” runs

Modern tools: either silent success or hard fail. Soft IR obligations still
appear on successful demos → feels unfinished.

**Recommendation:** product decision — suppress soft on seed-0 teaching path,
or teach “soft ≠ fail” once in QUICKSTART (docs). Not a surface sugar ADR.

#### P2-5. Dirac / blackboard Unicode still partial

`⟨φ|ψ⟩` shipped; full notebook Unicode for evolve/measure still not the default
teaching spelling (ASCII keywords remain primary — good for tooling).

**Recommendation:** keep ASCII primary; optional Unicode sugar only where
already Accepted.

#### P2-6. Pipeline `|>` is powerful and under-taught as chalk

Modern FP languages lead with pipe. Staqex has fusion/holes; S01 uses it in
compose; basics barely show it.

**Recommendation:** one B-tier pipe example after B08, not more Kernel.

---

### P3 — parked / do not open without explicit Architecture

| Topic | Status |
|---|---|
| Trait specialization / effect rows | **Parked** LISS-0196 採択 — no ship ADR |
| Continuous Kernel value | design boundary ADR 0126 |
| Display-unit restore | LISS-0197 deferred |
| Live QPU SDK | ADR 0127 + technology selection |
| Interface default method bodies | optional future ship ADR only |
| Unified `let`/`:=` binder | high cost; not required for modern chalk |

---

## 5. Additional findings (beyond the main ranked list)

These are real but secondary; listed so the review is not incomplete:

1. **Comment / causal-map walls** on S01 spine (honest for operators, heavy for
   first physicist glance) — sample editing / Host README split.
2. **Scorecard constellation vs one-tree coverage** — policy already retire-
   candidate for “one tree all surfaces”; still cultural pressure in reviews.
3. **Host / E lane boundary** in showcases still easy to misread as “all is
   Joint including Float boards” — teaching law exists; spine length fights it.
4. **LINEAR uncompute pedagogy** — hand `|0>` rebound still appears in some
   applied; prefer `tracing_out` / vacuum rules where legal.
5. **Experiment vs circuit lane markers** — `// staqex-lane:` is good; not all
   multi-file entries use it consistently.
6. **Config harvest class (B09)** — modern languages use modules/const; harvest
   class is a Kernel-era pattern; leave unless ADR 0061 revisited.
7. **Error vocabulary** — world-line vs Job vs capability (ADR 0175) is modern
   honesty; still under-exposed in basics.
8. **Agent Open Topics** — just synced (LISS-0196); still long “already shipped”
   lists invite skimming past open rows (docs UX, not language surface).
9. **Two implementation generations** (Python Kernel / Rust VM) — risk of
   wording drift in old ADRs; policy already says one semantics.
10. **No formatter / style linter for .sqx** — modern langs have rustfmt/gofmt;
    optional tooling Issue, not language semantics.

---

## 6. Recommended program shape (if Adjudicator wants a follow-on)

**Not** a second multi-wave sugar WP unless P0/P1 demand Kernel.

| Order | Work | Path |
|---|---|---|
| 1 | QMD inspect demotion to ≤1 peek | **done** LISS-0303 |
| 2 | S01 desk causal map → README; denser import header | **done** LISS-0303 |
| 3 | Teaching page: bind decision tree | **done** [bind-decision-tree](bind-decision-tree.md) |
| 4 | Classical multi-bind `J, h = …` | **done** ADR 0184 / LISS-0305 |
| 5 | Exhaustive closed-enum `when` | **done** LISS-0304 (`WHEN_NONEXHAUSTIVE`) |
| 6 | Soft QSEM teaching | **done** LISS-0304 (QUICKSTART) |
| — | Trait defaults / Continuous / display-unit / QPU SDK | **only** explicit reopen |

---

## 7. Scorecard (re-review summary)

| Criterion (north star) | Score | Note |
|---|---|---|
| Blackboard H / ket / evolve short | **A−** | B08 excellent; multi-file lag |
| Enterprise markers decreasing | **B+** | singles healed; showcase main/import remain |
| struct default / class rare | **A−** | intentional seats only |
| Lane honesty E vs H | **B** | law clear; S01 length still blurs |
| Fail-closed capability | **A** | policy intact |
| Modern module ergonomics | **B** | selective/relative good; re-export/alias thin |
| Effect / purity story visible | **B−** | shipped, under-taught |
| Overall vs 2026-08-02 re-review | **↑** | WP-0089 adoption closed the “lever shipped, face old” gap |

**One-line judgement:** Staqex is now a **modern physics language at the
notebook core**; remaining modernization is **showcase composition and a few
targeted sugars**, not another enterprise-erasure wave or axiom rewrite.

---

## 8. Explicit asks for the Adjudicator

1. Accept / amend this ranking (P0–P3)?
2. Authorize a **docs+samples** batch (P0 inspect demotion + import theater)
   without Kernel?
3. Authorize Architecture Path for **at most one** of: multi-bind sugar,
   exhaustive enum `when`, multi-file entry sugar?
4. Confirm trait / Continuous / display-unit / QPU remain **out** of the next
   surface batch?

Implementation starts only after explicit phase / batch approval.
