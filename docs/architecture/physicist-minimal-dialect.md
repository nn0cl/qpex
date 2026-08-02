# Physicist minimal dialect (blackboard ~10 lines)

| Field | Value |
|---|---|
| Status | **Accepted** (Adjudicator, 2026-08-02) — **pedagogy / teaching law**; **not** axiom rewrite; **not** Kernel implementation approval; **not** S01 code-edit approval |
| Date | 2026-08-02 |
| Authority | Adjudicator |
| Parents | [Adjudicator language vision](adjudicator-language-vision.md), [axioms](staqex-language-axioms.md), [physicist-dx-harmony](physicist-dx-harmony.md), [ADR 0095](adr/0095-design-horizon-ideal-form-first.md) |
| Critique input | Adjudicator review 2026-08-02 (showcase / surface pedagogy; points 1–13) |
| Next | [S01 redesign sketch](../specs/staqex-v1-s01-redesign-toward-minimal-dialect.md); [destructive simplification sketch](staqex-destructive-simplification-sketch.md) |

```markdown
[DESIGN CHECK]
- Scope: re-fix what “Staqex-looking” source is in ≤10 blackboard lines;
  separate Experiment Kernel dialect from Host/classical modules; give a
  scoring ruler for examples and future S01 work.
- Not in scope: Kernel/syntax changes; ADR acceptance; S01 code edits;
  destructive language cuts (third review step).
- Specs inspected: axioms, vision, physicist-dx-harmony, friction ledger,
  B01/B08, S01 spine patterns, LISS-0243 Host envelope note.
- Ambiguity: exact surface for “trace out others at measure”; whether
  package/FQN noise is Class B sugar or Class E sample debt; Operator
  lane vs circuit lane as one dialect or two named dialects.
- Routing: Architecture Path / documentation only.
- Verification: Adjudicator accept/reject/amend this dialect; then gate
  S01 redesign against it.
```

## 1. Purpose

The axioms are sharp. Showcase and coverage pressure blunt them.

This document defines the **minimal dialect**: the shortest source a research
physicist should recognize as *the* Staqex experiment script — without
enterprise ceremony, inspect floods, LINEAR hand-kills, or “OS-scale”
classical Float theaters.

It is a **pedagogy and design ruler**, not a new axiom set. Where current
Kernel forces extra lines (packages, sibling `|0>`), those lines are classified
as friction — not as the ideal form.

**Accepted scope:** teaching honesty, example scoring, and gates for future
showcase / S01 *design*. It does **not** by itself authorize `.sqx` edits,
Kernel changes, or axiom ADRs.

## 2. Two languages (public honesty)

| Lane | Name | Owns | Does not own |
|---|---|---|---|
| **E** | Experiment Kernel | `state` / `Operator` / `when` / `evolve` / `expect` / terminal `measure` | Graph search, MIP, city ops ledgers, Job DTOs |
| **H** | Host / classical module | Python (or future classical modules), JobResult → ticket, logging, I/O ports | Mid-program collapse; inventing `sample_value` |

**Never Leave the State** applies fully inside **E**. Classical Float bags and
mutable trackers live in **H** (or in non-experiment library modules that are
**not** taught as the blackboard dialect).

Today’s fiction — “everything is Joint, including CommandBoard.phase_tag” —
is what makes S01 look like OOP theater with a 2-wire Suzuki coda. Thin that
fiction in teaching first; language ADR changes come later if needed.

## 3. The ~10-line dialect (ideal notebook)

Ideal reading (virtual sugar allowed in comments; Kernel may still require
`package` / `pub fn` today):

```text
// Experiment: transverse-field Ising, two sites — expect ZZ, sample s0
J, h := 1.0, 0.5
H := -J*(Z[0]*Z[1]) - h*(X[0]+X[1])
s0, s1 := |+>, |+>
(s0, s1) := evolve (s0, s1) under H for 0.7 using Suzuki(order=2, steps=6)
zz := expect(ZZ, s0, s1)          // notebook quantity — not a log flood
measure s0 tracing_out s1         // IDEAL: one observation; others leave honestly
```

Shipping Kernel spelling today (honest, still “dialect-shaped” if kept short):

```text
package com.staqex.examples.basics.minimal_ising   // friction: FQN noise

pub fn main() -> Unit {
    Float J = 1.0
    Float h = 0.5
    Operator H = -J * (Z[0] * Z[1]) - h * (X[0] + X[1])
    state s0 = |+>
    state s1 = |+>
    state (s0, s1) = evolve (s0, s1) under H for 0.7
        using Suzuki(order = 2, steps = 6)
    state zz = expect(ZZ, s0, s1)
    measure s0 tracing_out s1         // ADR 0173 — leftover leaves honestly
}
```

**Count:** ≈10 meaningful physics lines. Package + `main -> Unit` wrapper are
ceremony, not physics.

**Reference cores that already match this spirit:** B01 (Dirac → measure),
B08 (H + evolve + expect), A03 (Fermion → JW map). Keep those as north-star
samples; do not dilute them with Float-tag festivals.

## 4. Dialect IN / OUT

### IN (teach as normal)

- Ket / Dirac preparation
- `Operator` algebra and `evolve … under H for t` (Suzuki ok when named)
- `when` for mixtures (not classical `if`)
- Sparse `expect` (notebook observables)
- Single terminal `measure` per `main`
- Honest soft diagnostics when writeable ≠ placeable (**not** buried in a
  “city OS” main without a lane label)

### OUT of the minimal dialect (allowed elsewhere, not “the” notebook)

- `inspect` chains / `viewed_*` floods (Host logs instead)
- Hand `|0>` sibling kills as the taught uncompute story
- Identity / empty-body `evolve times N { (wires) }` for coverage
- Domain OOP parameter bags presented as the experiment
- Type-First demos that die at `Float` fields (call them demos, or fix types)
- Circuit-register `forEach` / QFT **in the same pedagogical main** as
  Hamiltonian evolve without an explicit “circuit lane” heading
- Soft-only `evolve … until` on a showcase **spine** without lane annotation
- Disaster-OS / MIP / graph algorithms inside `.sqx` experiment scripts

## 5. Scoring rule for official examples

An official example **passes the dialect test** iff:

1. A physicist can state the experiment in one sentence matching the source.
2. Physics lines dominate ceremony lines (target: ceremony ≤ wrapper).
3. At most a **small** number of `expect` / no `inspect` flood.
4. Terminal `measure` is the result boundary; Host may structure the envelope
   (vacuum success is **not** an accepted teaching outcome).
5. Coverage of extra surfaces lives in **basics satellites**, not by stuffing
   the narrative spine.

Fails the test → Class **E** (sample debt) until fixed or demoted from
“showcase of the language.”

## 6. Fatal anti-patterns (from critique 1–13)

Keep these named so agents do not reintroduce them:

1. **LINEAR tax kill** — `state sibling = |0>` before measure as ritual.
2. **inspect / Float-tag flood** — printf quantum; Host should own logs.
3. **Granularity lie** — 2-wire Suzuki + coverage satellites called an “OS.”
4. **Operator overload fog** — same `+` across Float / State / Operator without
   local typing clarity (teach lanes; later, surface clarity ADRs).
5. **Writeable-as-production** — soft QPU failures on the narrative spine
   without an explicit non-placeable lane.

## 7. Decisions (Adjudicator 2026-08-02)

Accepted with the document defaults:

| ID | Decision | Notes |
|---|---|---|
| D1 | **Accept** two languages (E vs H) as **teaching law** | Axioms text unchanged until a dedicated ADR |
| D2 | **Track** `measure … tracing_out …` as Class B surface candidate | Samples stay honest about the gap; no silent invention in S01 |
| D3 | **Class E** for showcases: shorten package / FQN where legal | Module system remains; pedagogy minimizes noise |
| D4 | **One** Experiment Kernel with **two named sub-lanes** (Hamiltonian vs circuit) | Document headings; do not mix unmarked in one teaching main |
| D5 | Type-First sell **restored** (fields carry units) | [ADR 0174](adr/0174-type-first-field-units.md) **Accepted**; Kernel Green + S01 `quantities.sqx` heal under [LISS-0254](../issues/LISS-0254-type-first-field-units-red.md) (2026-08-02) — demotion lifted |

## 8. Explicit non-goals (this document)

- No Kernel implementation
- No axiom rewrite in this file
- No S01 file edits here (see companion sketch)
- Language-feature cuts → [destructive simplification sketch](staqex-destructive-simplification-sketch.md)

## 9. Acceptance record

- [x] Dialect §3 accepted as the pedagogy north star
- [x] Two-language table (§2) accepted as teaching honesty
- [x] Scoring rule (§5) may gate future example / showcase PRs
- [x] Open decisions D1–D5 resolved as in §7
- [x] Next doc work authorized: S01 redesign sketch + destructive simplification sketch
- [ ] S01 `.sqx` implementation — **not** authorized by this acceptance
- [x] `tracing_out` / LINEAR sugar ADR
  [ADR 0173](adr/0173-measure-tracing-out-leftover-policy.md) (**Accepted**);
  Kernel [LISS-0250](../issues/LISS-0250-measure-tracing-out-red.md) + tonight
  spine [LISS-0251](../issues/LISS-0251-s01-spine-tracing-out.md) **complete**
- [x] Type-First field units ADR + sample heal
  [ADR 0174](adr/0174-type-first-field-units.md) (**Accepted**);
  Kernel Green + S01 [`quantities.sqx`](../../examples/showcase/S01_quantum_disaster_response/domain/quantities.sqx)
  under [LISS-0254](../issues/LISS-0254-type-first-field-units-red.md) — dialect D5 demotion **lifted**
