# Staqex representative-program plan (rebaseline, 2026-07-31)

| Field | Value |
|---|---|
| Status | **Accepted** (2026-07-31) — P0→P1→P2→S*; **P0/P1 start authorized** 2026-07-31 |
| Supersedes | [`staqex-v1-noether-forge-review-plan.md`](staqex-v1-noether-forge-review-plan.md) (Slice A–D execution record retained historically) |
| Related Issue | [LISS-0120](../issues/LISS-0120-representative-program-language-review-gate.md) — **rejected / deferred** pending prerequisites |
| Successor Issues | Gate P0: [LISS-0119](../issues/LISS-0119-examples-health-inventory.md) / [LISS-0122](../issues/LISS-0122-examples-basics-heal.md) / [LISS-0123](../issues/LISS-0123-examples-applied-heal-defer.md) (**complete**); Gate P1: [LISS-0124](../issues/LISS-0124-language-coverage-ledger.md) (**complete**, [ledger](staqex-v1-language-coverage-ledger.md)). Showcase S* = new ID after P2 (do not reuse LISS-0120) |
| North-star lens | [Physicist × DX harmony](../architecture/physicist-dx-harmony.md); Clean Architecture / DDD in `AGENTS.md` |
| Friction evidence | [physicist-source-friction-ledger.md](../architecture/physicist-source-friction-ledger.md) |

```markdown
[DESIGN CHECK]
- Scope: reformulate the representative-program path so Staqex meets the
  joint professional standard of research physicists and senior DDD/CA
  engineers — including hard prerequisites and rejection of premature
  LISS-0120.
- Not in scope: implementing the showcase, fixing all examples in this
  document, accepting Open Topics by silence.
- Joint standard: blackboard-direct physics reading AND bounded contexts,
  ports, fail-closed diagnostics, no hidden policy in adapters (see
  physicist-dx-harmony).
- Ambiguity: concrete scientific mission theme for the showcase remains
  Adjudicator-chosen after prerequisites; coverage table rows need inventory.
- Verification: docs sync; no .sqx/compiler changes in this docs packet.
```

## 0. Why rebaseline

LISS-0120 assumed a representative sample could review the language once IR
gates opened. Adjudicator review found the opposite prerequisites missing:

1. **Language surface is not “all closed.”** Core Kernel is shipped, but Open
   Topics and honest “in / out of v1 review” boundaries were not locked.
2. **`examples/basics` and `examples/applied` are not reliably exemplary.**
   Many entries run with `compile.ok == False` (often LINEAR), and some fail
   at runtime. A showcase built on that baseline confuses language defects,
   sample debt, and review judgement.
3. **Physicist × DX harmony is not proven by line count or module trees.**
   It is proven when source is scientifically legible and architecturally
   maintainable under the same meaning.

Therefore LISS-0120 is **rejected for continuation as the active review
gate**. Work already shipped (plans, A11 prototype attempts, IR deps) remains
historical evidence, not authorization to proceed.

## 1. North star — Physicist × DX harmony (normative)

Authoritative framing:
[`physicist-dx-harmony.md`](../architecture/physicist-dx-harmony.md).

The representative program exists to make this **joint professional
standard** reviewable:

> Staqex expresses research-grade physical models and experimental intent
> directly, while preserving Clean Architecture / DDD discipline at
> application scale: clear bounded contexts, ubiquitous language shared with
> the physics, ports at the boundary, and fail-closed diagnostics.

Neither audience is secondary. Physics reading is not “DX decoration,” and
software structure is not “enterprise noise on equations.”

### 1.1 Physicist criteria (research reading)

| Signal | Pass means |
|---|---|
| Domain directness | Source reads as model + protocol, not compiler choreography |
| State continuity | Joint / Never Leave the State is obvious in the mission spine |
| Honest capability | Unsupported realization is explicit (no fake QPU success) |
| Publishable intent | Symmetry, quench, observable, exactness obligations are named |
| Scientific ambition | Theme is credible on a quantum-machine research roadmap |

### 1.2 Software-architecture criteria (DDD / Clean Architecture)

| Signal | Pass means |
|---|---|
| Bounded contexts | Ownership directories match real responsibility, not quota folders |
| Ubiquitous language | Types share physicist vocabulary; no parallel DTO dialect in `.sqx` |
| Composition | `import` + constructors + small functions; every binding serves the mission |
| Ports | RNG / source / sink / future QPU behind ports; no provider SDK in sample |
| Fail-closed | Diagnostics name public rules; LINEAR and type errors are not normalized away |
| Reviewability | One mission spine; file/method size fit for human review |

**Reject criteria for the future showcase:** kitchen-sink syntax tourism;
padding; unlinked ownership trees; `compile.ok == False` treated as normal;
coverage that cannot state which surface is in scope.

## 2. Prerequisite program (must complete before a new showcase Issue)

### Gate P0 — Example health (basics first, then applied)

**Goal:** official examples are trustworthy teaching artifacts.

Minimum exit (Adjudicator may tighten):

1. Inventory every `examples/basics/**` and `examples/applied/**` entry point.
2. Classify each as: **green** (`compile.ok` + deterministic run), **amber**
   (runs but unclean diagnostics — must have Issue), **red** (runtime fail /
   missing modules).
3. Bring **all basics** to **green**, or mark retired with replacement pointer.
4. Bring **applied** to green-or-explicitly-deferred; no silent broken demos in
   the default catalog path (`QUICKSTART` links only to green).
5. Document LINEAR / multi-file / keyword landmines discovered while healing
   examples as language or docs Issues — do not hide them in samples.

Issue family (P0 start authorized; LISS-0119 **complete**):

| ID | Role |
|---|---|
| [LISS-0119](../issues/LISS-0119-examples-health-inventory.md) | Inventory — **complete** |
| [LISS-0122](../issues/LISS-0122-examples-basics-heal.md) | Basics heal — **ready** |
| [LISS-0123](../issues/LISS-0123-examples-applied-heal-defer.md) | Applied heal/defer — **ready** |

### Gate P1 — Language coverage ledger (honest v1 boundary)

**Goal:** lock an honest v1 surface boundary for the showcase (what is in
scope, what is implemented, what is explicitly out).

Issue: [LISS-0124](../issues/LISS-0124-language-coverage-ledger.md)
(**authorized**; not started). Deliverable: a coverage ledger (new spec or ADR
companion). Seed rows from
[`physicist-source-friction-ledger.md`](../architecture/physicist-source-friction-ledger.md)
(F-01…F-10) plus shipped surfaces. Table shape:

| Surface / concern | Status | Where proven today | In showcase? | Follow-up |
|---|---|---|---|---|
| e.g. `when`, `evolve for`, `class`/`init`, static QPU lane, … | shipped / partial / open | Bxx / SV / none | required / optional / out | Issue/ADR |

Rules:

- Open Topics from agent contracts are either **scheduled for implementation**
  before the showcase, or **explicitly out of showcase scope** with physicist-
  readable rationale (not “later maybe”).
- “All syntax” for the showcase means **all rows marked required**, not every
  historical ADR fantasy.
- Programmer rows include ports, diagnostics, module visibility, linear
  resources — not only grammar tokens.

### Gate P2 — Mission selection (only after P0+P1)

Pick one ambitious finite mission that:

- meets research-grade scientific credibility for its domain;
- is structured as a real bounded-context application under Clean
  Architecture / DDD reading;
- can declare simulator vs static-hardware honesty without false success;
- stays finite (no hidden continuous discretization in v1 showcase).

**Default scientific theme (retained, not locked):** finite quantum-matter
discovery (Noether Forge lineage) — quench + symmetry + magnetization /
correlation evidence + provenance dossier — **rewritten as one mission spine**,
not a type museum.

Alternates only by Adjudicator scope approval (e.g. mission-observatory-scale
networking physics, open-system sensor with honest mixed-state boundary if P1
marks that surface in-scope).

## 3. Showcase construction plan (after P0–P2)

Call this **Phase S** (showcase). New Issue ID after reclaim policy is set.

### S0 — Showcase specification (docs-only)

- Mission problem statement in one paragraph (physicist) + context map
  (programmer).
- Coverage ledger subset: which required rows the showcase must exercise.
- Module map by bounded context; entrypoint naming (`main_<mission>.sqx`).
- Joint rubric (extend §1) with evidence artifacts (source citations, IR
  traces, example-green dependency).
- Non-goals: provider SDKs, live QPU credentials, padding, silent Kernel fixes
  inside the sample.

### S1 — Vertical thin slice (integrated Red→Green→Refactor)

One path: prepare → evolve → observe intent → terminal measure, **using**
domain/physics/application types for real values (duration, couplings, model),
`compile.ok`, multi-file `run_path`, no unused catalogs.

### S2 — Full mission scale

Grow coherently to the agreed size band (revisit 1k–3k only after P0 removes
pressure to pad). Every module participates in the mission spine or is deleted.

### S3 — Coverage completion + IR evidence

Close remaining **required** ledger rows inside the showcase or demote them
with Adjudicator approval. Keep soft Semantic / Physics IR evidence honest.

### S4 — Joint human review (Adjudicator)

Separate passes:

1. Physicist pass — §1.1  
2. Maintainer / CA pass — §1.2  
3. Friction ledger → Issues/ADRs only (no silent sample patches for language
   bugs)

## 4. Relationship to prior LISS-0120 artifacts

| Artifact | Fate |
|---|---|
| LISS-0120 Issue | **Rejected / deferred** as active gate; keep file for history + pointers |
| Noether Forge Slice A plan | Historical; superseded by this rebaseline |
| A11 tree / NF-E01 attempts | Optional salvage after P0; not authoritative until rewritten under S* |
| ADR 0108–0111, LISS-0082 | Remain prerequisites for IR honesty when S3 runs |

## 5. Execution order (summary)

```text
P0 example health  ──┐
                     ├──► P2 mission lock ──► S0 spec ──► S1..S4 joint review
P1 coverage ledger ──┘
```

No showcase Red/Green until **P0 and P1 are Adjudicator-accepted complete**
and **P2 mission is locked**.

## 6. Adjudicator decision points

- [x] Accept this rebaseline plan (Physicist × DX harmony; P0→P1→P2→S*).
      Accepted 2026-07-31.
- [x] Confirm LISS-0120 status **rejected / deferred** (not quietly continued).
- [x] Accept [ADR 0114](../architecture/adr/0114-classical-coefficient-elaboration-vs-linear.md)
      (classical coefficient elaboration vs LINEAR; fold-invariant) —
      [LISS-0121](../issues/LISS-0121-classical-coefficient-elaboration-vs-linear.md)
      Phase 3 complete (2026-07-31).
- [x] Authorize starting **P0** (examples conformance) as the next
      implementation program — Issues filed:
      [LISS-0119](../issues/LISS-0119-examples-health-inventory.md) (**complete**),
      [LISS-0122](../issues/LISS-0122-examples-basics-heal.md) (**ready**),
      [LISS-0123](../issues/LISS-0123-examples-applied-heal-defer.md) (**ready**).
      Authorized 2026-07-31. Inventory done; heal next.
      Named-coeff LINEAR no longer blocks B08; other residuals may remain.
- [x] Authorize starting **P1** coverage ledger (docs; may parallel after
      LISS-0119 exists) — Issue filed:
      [LISS-0124](../issues/LISS-0124-language-coverage-ledger.md).
      Authorized 2026-07-31.
- [x] Defer mission finalization (P2) until P0+P1 exit.
