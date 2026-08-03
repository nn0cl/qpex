# Trait specialization / effect-row surface examples (design draft)

**Status:** **Accepted** (Adjudicator 2026-08-03「LISS-0196 を採択」) — examples
accepted; **no ship ADR**; no Kernel Red  
**Date:** 2026-08-03  
**Authority:** ADR [0128](../architecture/adr/0128-trait-effect-expansion-boundary.md)
(design boundary); shipped core ADR [0081](../architecture/adr/0081-effect-marking-and-propagation.md) /
[0082](../architecture/adr/0082-interface-impl-and-system-boundary.md).  
**Not:** implementation authorization, Kernel Red, or a ship ADR.

Physicist-first note: interfaces name **capabilities of physical systems**
(deployable unit, haulable load, evolvable oscillator). Specialization and
effect rows must not recreate enterprise trait hierarchies or hide collapse /
Host boundaries.

---

## 1. Shipped surface (do not re-open)

### 1.1 Interface + `impl` (ADR 0082)

Official seat: S01 capabilities.

```staqex
interface Deployable {
    fn readiness() -> Float
}

class RescueSquad {
    pub val readiness_f: Float
    fn init(readiness_f: Float) { this.readiness_f = readiness_f }
}

impl Deployable for RescueSquad {
    fn readiness() -> Float { return this.readiness_f }
}

// Interface-typed free-fn receiver (LISS-0231)
fn readiness_of(unit: Deployable) -> Float {
    return unit.readiness()
}
```

Rules already normative:

- `impl Interface for Type` only (no inherent `impl Type` block).
- At most one `(Interface, Type)` per linked program (coherence).
- No `pub` inside `impl`.
- No specialization / negative bounds / inheritance.

### 1.2 Effect marking (ADR 0081)

Shipped vocabulary: `Measure`, `Snapshot`, `Inspect`, `Host`, plus linear
`Uncompute` witness path in some slices.

Accepted spelling in Kernel:

```staqex
fn peek(x: State<Float>) -> State<Float> effects { Inspect } {
    return inspect(x)
}
```

Pure `fn` by default; effects propagate through Call / method / `|>`.

---

## 2. Specialization — surface candidates

### 2.1 Problem statement (why anyone wants more)

Physicists may want:

- One interface method with **different** concrete bodies for discrete vs
  continuous carriers, or for SIM vs future QPU system tags — without writing
  two free-fn names.
- Default method bodies on interfaces (optional sugar only).

Programmer DX must not drive the spelling (ADR 0095).

### 2.2 Recommended MVP direction (for a future ship ADR)

**No overlapping specialization tables.** Prefer **named free-fns** and
**explicit interface-typed params** already shipped. If a ship ADR ever
authorizes more, the first slice should be:

| In first ship ADR (proposed) | Out of first ship ADR |
|---|---|
| Optional **default method body** on `interface` (pure only) | Overlapping `impl` with priority / specialization lattice |
| Documented **orphan free-fn** pattern for SIM/QPU forks | Negative bounds, inheritance, associated types |
| Keep coherence: still ≤1 `impl Interface for Type` | Provider-specific dispatch tables |

**Default method body (illustrative only — not Accepted):**

```staqex
// PROPOSED ONLY — not Kernel syntax until a ship ADR Accepts it.
interface Scoreable {
    fn score() -> Float {
        return 0.0   // pure default; override via impl
    }
}
```

Rejected alternatives (do not ship):

| Spelling | Why reject |
|---|---|
| `impl Deployable for RescueSquad where T: Discrete` | Bound specialization reopens coherence tables; not physicist blackboard |
| `impl Deployable for RescueSquad specialize when lane = experiment` | Lane is Host/process, not a type-level physics law |
| Rust-style specialization / overlapping impls | Hard coherence; enterprise reading |
| Implicit interface methods without `impl` | Hides the contract seat |

### 2.3 Physicist-preferred alternative (no new syntax)

When two algorithms exist, **name them** on the board:

```staqex
fn readiness_sim(unit: Deployable) -> Float { return unit.readiness() }
// future Host lane: readiness_qpu_probe(...)  — not a Kernel effect table
```

This is already legal. A ship ADR is only needed if the Adjudicator wants
defaults or more sugar; not required for S01 honesty.

---

## 3. Effect rows — surface candidates

### 3.1 Shipped fixed set vs rows

ADR 0081 deferred **extensible effect rows** and provider-specific effects.
Today: fixed set `{Measure, Snapshot, Inspect, Host}` (+ Uncompute witness).

### 3.2 Recommended MVP direction

| In first ship ADR (proposed) | Out |
|---|---|
| Keep fixed vocabulary; improve **diagnostics** when pure calls Inspect | User-defined effect names |
| Optional **effect aliases** in docs only | Provider SDK effects inside Kernel |
| Explicit `effects { Inspect, Host }` multi-set (already intended) | Infer effects from body without declaration |

**Multi-effect (already in spirit of ADR 0081):**

```staqex
fn log_and_peek(x: State<Float>) -> State<Float> effects { Inspect, Host } {
    // Host sink + non-collapsing peek — Host adapter still ports
    return inspect(x)
}
```

**Rejected:**

| Spelling | Why reject |
|---|---|
| `fn f() !Inspect` bang sugar as only form | Easy to miss; keep `effects {…}` primary |
| Effect polymorphism `effects { E }` open rows | Hides physics boundaries; provider leak |
| Silent inference of Measure from body | Collapses law must stay terminal and explicit |

### 3.3 Interaction with free-fn / pipeline face (post WP-0089)

- Free-fn pipelines (`compose_priority`, Operator free factories) stay **pure**
  unless marked.
- Transitive free-fn link under selective import (LISS-0295/0299) does **not**
  change effect sets — callees still propagate effects.
- Struct + free-fn demotion does **not** remove the need for interface seats
  where polymorphism is intentional (S01 Deployable / Haulable).

---

## 4. Minimum follow-on ship ADR outline (not filed)

If Adjudicator wants a Kernel ship later:

1. **ADR title (draft):** “Interface default method bodies (pure only)”  
   - Scope: optional default body; still one `impl` max; pure defaults only.  
   - Out: specialization, effect rows, provider effects.
2. **Red Issue:** single Gherkin — default used when no override; override wins;
   effectful default is hard reject.
3. **Effect-row expansion** remains a **separate** ADR after fixed-set
   diagnostics are enough in practice.

Recommendation: **prefer no ship ADR now.** Document free-fn + interface-typed
params as the stable face; revisit defaults only if sample friction reappears.

---

## 5. Open questions — resolved by 採択 (2026-08-03)

| Question | Decision |
|---|---|
| Interface default method bodies in v1? | **Not now** — free-fn + explicit `impl` is enough |
| Effect work: diagnostics vs new surface? | **No new surface** — fixed set remains; diagnostics optional later |
| Specialization required for physics honesty? | **No** for current program; do not invent |

---

## 6. Exit map

| Artifact | State |
|---|---|
| This draft | **Accepted** (examples; no ship ADR) |
| LISS-0196 | **complete** |
| Ship ADR | **none** |
| Kernel Red | **forbidden** until a future ship ADR is Accepted under ADR 0128 |

---

## 7. Traceability

- Issue: [LISS-0196](../issues/LISS-0196-trait-specialization-surface-design.md)
- Boundary: ADR 0128
- Shipped: ADR 0081, 0082; S01 `domain/capabilities.sqx`
