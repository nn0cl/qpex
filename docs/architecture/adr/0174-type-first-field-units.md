# ADR 0174: Type-First dimful fields retain units (reject permanent sell demotion)

## Status

**Accepted** (2026-08-02) — Adjudicator「承認」on Proposed draft
([LISS-0253](../../issues/LISS-0253-adr-0174-type-first-field-units.md)).
Architecture approval only. Kernel / sample heal wait for Feature Issue
[LISS-0254](../../issues/LISS-0254-type-first-field-units-red.md) with
explicit Phase 1 Red approval.

Companions:

- [ADR 0037](0037-type-first-dimensions-structured-units.md) (Type-First + dims)
- [ADR 0054](0054-user-module-import.md) (class Type-First fields authorized)
- [ADR 0116](0116-classical-quantity-state-arithmetic.md) (Classical quantity heads)
- [ADR 0155](0155-mixed-unit-canonical-promote.md) (locals track unit suffixes)
- Dialect D5 / destructive sketch §2 Type-First field units
- S01 [`domain/quantities.sqx`](../../../examples/showcase/S01_quantum_disaster_response/domain/quantities.sqx)
  (Float fields + literal-only `to` — honest Kernel limitation comment)

## Context

Physicists store stocks on structs/classes (`Mass water`, `Time window`).
ADR 0054 already allows Type-First fields on `class`. ADR 0155 requires
**locals** to track unit suffixes at runtime so `a + b` / `expr to unit` work.

Today, **field reads lose unit tracking**. Reproduced 2026-08-02 on Shipping
Kernel:

```text
class Box { pub val m: Mass; … Mass x = this.m to g … }
→ TYPE_MISMATCH: cannot convert `m` to `g` (canonical m vs kg)
```

S01 therefore stores `Float road_km` / `water_kg` and rebuilds quantities from
**literals** inside methods — Type-First sell becomes theater. Dialect D5
demoted that sell until fields carry units; destructive sketch listed
**fix or permanently demote** as ADR-needed.

Batch item ② must pick one.

## Dependency Adoption Evidence

Not applicable.

## Decision

### 1. Choose fix — reject permanent demotion

**Do not** permanently demote Type-First + SI as a teaching surface.
Permanent demotion would freeze Float-field theater as the official story and
contradict ADR 0037 / 0054 / 0155.

### 2. Field unit retention contract

1. Dimful Classical Type-First heads on **`class` and `struct` fields**
   (`Mass`, `Length`, `Time` / `Delta<Time>`, `Current`, `Temperature`, and
   other ADR 0037 / SI catalog heads) **retain** the same unit-suffix evidence
   locals already keep under ADR 0155.
2. Field **write** (`this.f = expr` / constructor / init) stores magnitude
   **and** unit (or canonical unit + dimension family) derived from `expr`.
3. Field **read** (`this.f` / `obj.f`) restores that unit into the evaluator’s
   unit-tracking path so:
   - `this.f to unit` uses the stored source unit;
   - mixed `+`/`-` promote (ADR 0155) sees known suffixes when both sides have
     them.
4. Bare `Float` / dimensionless fields remain legal; they do **not** invent
   SI units. Official Type-First sell must not present Float stock fields as
   dimensioned quantities.

### 3. Pedagogy after Accept + Green

1. Until Kernel Green for this ADR, dialect D5 demotion stays in force
   (literal-only SI demos; Float-field packs labeled honestly).
2. After Green, lift D5 demotion for samples whose stocks are dimful fields
   (heal S01 `Quantities` and similar).
3. Scorecard “Type-First + SI” may move from demoted sell to honest evidence
   only after that heal (separate sample Issue).

### 4. Scope limits

- MVP: Shipping Kernel evaluator + typecheck for `class`/`struct` field
  Attr paths used in `to` / mixed `+`/`-`.
- Does not require OOP unit *objects* (`class Meter extends Length`) —
  ADR 0037 dimensional algebra stays.
- Does not invent auto-unit for bare numeric Float fields.
- QPU / OpenQASM classical packing of units is out of scope.
- Failure glossary (batch ③) remains separate.

### 5. Follow-up (post-Accept)

1. Feature Issue [LISS-0254](../../issues/LISS-0254-type-first-field-units-red.md):
   Red/Green/Refactor for field unit maps on object/struct instances;
   regression for `this.m to g` and mixed field `+` (requires separate Phase
   approval).
2. Sample heal (under LISS-0254, 2026-08-02): S01 `quantities.sqx` (+ tonight
   spine ctor) migrated Float stocks → dimful fields; apology comment removed.
3. Dialect D5 / scorecard sync after sample heal — **done** 2026-08-02.
4. Failure glossary (batch ③) remains separate.

## Consequences

Positive:

- Closes language-design P0 from S01 expressiveness review without killing
  Type-First teaching.
- Aligns field storage with ADR 0155 locals and ADR 0054 field surface.

Negative / costs:

- Evaluator object model grows unit maps (or equivalent evidence).
- Existing Float-field samples need a heal pass after Green.

## Enforcement

Code review / Adjudicator should reject:

- Implementing Kernel field-unit retention without [LISS-0254](../../issues/LISS-0254-type-first-field-units-red.md)
  Phase approval (Accept alone is not Red/Green authorization).
- Permanently demoting Type-First sell *as the resolution of this ADR*
  without superseding it.
- Claiming Type-First field SI is “shipped” while `this.qty to unit` still
  fails or samples still rebuild from literals only.
- Introducing Meter-class OOP unit hierarchies contrary to ADR 0037.
