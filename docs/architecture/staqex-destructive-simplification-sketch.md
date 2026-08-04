# Destructive simplification sketch — what to cut or demote

| Field | Value |
|---|---|
| Status | **Accepted** (Adjudicator, 2026-08-02) — cut/demote **policy sketch**; ADR 0173 shipped; [ADR 0174](decision-themes/dec-0004-type-first-scientific-model.md) Type-First fields **Accepted** + Kernel Green + S01 quantities heal (D5 lifted); failure glossary still outstanding |
| Date | 2026-08-02 |
| Authority | Adjudicator |
| Parents | Minimal dialect; [axioms](staqex-language-axioms.md); [vision](adjudicator-language-vision.md); [ADR 0095](decision-themes/dec-0003-language-surface-and-physicist-first-dx.md) |

```markdown
[DESIGN CHECK]
- Scope: name surfaces and teaching claims to cut, demote, or split so the
  dialect stays sharp; classify keep / demote / retire-candidate / ADR-needed.
- Not in scope: deleting Kernel features in this turn; editing examples;
  accepting ADRs.
- Constraint: machine convenience still must not reshape chalk (ADR 0095);
  cuts target *pedagogy lies* and *optional ceremony*, not physicist spelling.
```

## 1. Principle

Cut or demote what **blunts** the Accepted dialect. Do not cut blackboard
spelling to make the compiler happier.

| Bucket | Meaning |
|---|---|
| **Keep** | Core E-lane or honest H-lane |
| **Demote** | Allowed, not taught as “the” language; basics-only or lane-labeled |
| **Retire-candidate** | Consider removing from surface or forbidding in official samples |
| **ADR-needed** | Desire is real; needs Architecture Path before ship or kill |

## 2. Inventory

| Item | Bucket | Rationale |
|---|---|---|
| Ket / Dirac / `when` / `evolve under H` / `expect` / terminal `measure` | **Keep** | Dialect core |
| Operator algebra + Suzuki | **Keep** | B08 north star |
| Host Job / MeasurementEnvelope / ticket mapping | **Keep** (H) | Result contract; vacuum success not OK |
| `inspect` in official spines / showcases | **Demote** → retire from spines | Printf pedagogy; Host owns logs |
| Hand `|0>` sibling kill as taught uncompute | **Demote** teaching; **ADR-needed** for `tracing_out` / scope GC | Fatal critique #1 |
| Identity / empty `evolve times` | **Retire-candidate** in samples; keep syntax only if real physics uses it | Coverage lie |
| Soft-only constructs on unmarked spines (`until`, etc.) | **Demote** — lane banner required | writeable ≠ placeable honesty |
| Circuit `forEach` / QFT lane | **Keep** as **named sub-lane**; never unmarked mix with H-spine | Dialect D4 |
| `class` as Float DTO / Tracker | **Demote** from “physical system” teaching | Harmony table vs reality; classical H-lane or library |
| `class` as setup + evolving state (true physical system) | **Keep** when it matches the reading | Do not delete OOP wholesale |
| Type-First field units | [ADR 0174](decision-themes/dec-0004-type-first-scientific-model.md) (**Accepted**): **fix** retention; Kernel + S01 heal [LISS-0254](documentation-compression-map.md) | **Keep** (D5 demotion lifted 2026-08-02) |
| Package `com.staqex…` FQN in demos | **Demote** noise (shorten); do not ban modules | Dialect D3 |
| Axiom “all Joint” taught as including city Float boards | **Demote fiction** | Two-language teaching law (D1) |
| Err world-line vs Job diagnostic vocabulary | **ADR-needed** glossary | Critique #8; not a silent cut |
| Scorecard-driven “one tree all surfaces” | **Retire-candidate** as *policy* | Replace with constellation index |

## 3. Recommended cut order (docs → samples → language)

1. **Teaching law** (done): minimal dialect Accepted; E vs H public.
2. **Sample policy**: forbid inspect floods, identity evolve, OS granularity
   claims in new PRs (dialect scoring rule).
3. **S01 redesign Issues** (separate approval): strip spine to dialect.
4. **ADR candidates** (separate Architecture Path):
   - `measure … tracing_out …` / block-scope leftover policy
   - Type-First fields vs demoted sell (pick one)
   - Failure glossary (world-line vs Job diagnostic)
5. **Only then** consider retiring syntax that exists solely for coverage
   theater (identity evolve patterns in *samples* first; language kill last).

## 4. Explicit non-cuts (do not “simplify” these away)

- Never Leave the State / terminal measure (Axiom 5)
- Rejection of classical `if` / bare `for` in Static Kernel (Class A)
- Writeable ≠ executable (capability fail-closed)
- Hamiltonian chalkboard spelling

## 5. Acceptance record

- [x] Adjudicator agrees buckets in §2 (Accepted 2026-08-02)
- [x] Sample-policy enforcement via dialect scoring authorized for **new**
      example / showcase PRs (docs gate; CI hook optional later)
- [x] ADR candidates ranked for a future Architecture Path batch:
      1. `measure … tracing_out` / leftover policy  
      2. Type-First fields vs demoted sell  
      3. Failure glossary (world-line vs Job diagnostic)
- [x] No Kernel deletion without a named ADR Issue (reconfirmed)

## 6. One-line summary

**Simplify pedagogy and showcase claims first; add LINEAR/result sugar by ADR;
delete language features last and only when they exist solely to blunt the dialect.**
