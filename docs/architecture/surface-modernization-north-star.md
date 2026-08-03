# Surface modernization north star (de-enterprise look)

| Field | Value |
|---|---|
| Status | **Accepted** (2026-08-02) — Adjudicator「承認・起票」; gates [WP-0088](documentation-compression-map.md) aesthetic scoring; **not** axiom rewrite; **not** by itself Kernel ship approval for Wave B/C |
| Authority | Adjudicator |
| Parents | [vision](adjudicator-language-vision.md), [axioms](staqex-language-axioms.md), [minimal dialect](physicist-minimal-dialect.md) (**Accepted**), [physicist-dx-harmony](physicist-dx-harmony.md), [ADR 0095](adr/0095-design-horizon-ideal-form-first.md), [destructive simplification](staqex-destructive-simplification-sketch.md) |
| Motive | Language design re-review (2026-08-02): meaning is strong; **surface ceremony reads 2010s Java/Kotlin enterprise** |

```markdown
[DESIGN CHECK]
- Scope: name what “modern surface” means for Staqex without violating
  physicist-first or NLTS; sequence sample vs ADR work.
- Not in scope: Kernel implementation; accepting ADRs; editing .sqx in this file.
- Constraint: prefer chalk; machine convenience must not reshape physics spelling.
```

## 1. Problem (target feeling)

Today a short experiment still often looks like:

```text
package com.staqex.examples.basics.operators_hamiltonians

pub fn main() -> Unit {
    …
    Geometry.Tracker tracker = Geometry.Tracker(seg)
    …
}
```

Desired feeling (same physics, less enterprise ceremony):

```text
// experiment — transverse-field Ising
J, h = 1.0, 0.5
H = -J * (Z[0] * Z[1]) - h * (X[0] + X[1])
s0, s1 = |+>, |+>
(s0, s1) = evolve (s0, s1) under H for 0.7 using Suzuki(order = 2, steps = 6)
zz = expect(ZZ, s0, s1)
measure s0 tracing_out s1
```

**Personal / product goal:** erase the impression that Staqex is “enterprise
Kotlin with kets.” Keep the impression that Staqex is **executable chalk**.

## 2. Non-goals (operating policy)

Do **not**:

- restore Kernel `if` / `while` / exceptions / threads
- mid-program collapse or “Result unwrap” quantum style
- gate-DSL-first surface (Qiskit-shaped truncation of chalk)
- delete modules, types, or Host ports wholesale
- invent a second language semantics for “Rust-only” or “Python-only”

## 3. Modern means (allowed definitions)

| Modern | For Staqex |
|---|---|
| Short paths | Default experiment package / selective import / less FQN |
| Visible layers | Lane markers (experiment / circuit / host) without changing meaning |
| Predictable expressions | Pure classical calls participate in classical arithmetic |
| Records for data | `struct`/`enum` default; `class` only for true physical systems |
| Clear endings | `tracing_out` (shipped); optional block form later |
| Examples match dialect | basics teach the short face first |

| Not modern (for us) | Why rejected |
|---|---|
| Kernel async / try | Axioms 6–7 |
| Classical control in Joint | Axioms 3–4 |
| Silent placeability | vision honesty |

## 4. Aesthetic scorecard (how to judge PRs)

A surface-modernization change **passes** if:

1. Blackboard spelling of H / ket / evolve is unchanged or **shorter**
2. Enterprise markers decrease: `com.…` depth, `ClassName.ClassName`, `fn init`,
   `this.`, mandatory `pub fn main() -> Unit` noise in **teaching** samples
3. No new inspect museum / identity evolve / OS-scale claim
4. E vs H lanes remain honest
5. SV / seed-0 examples still run where claimed

A change **fails** if it only renames for fashion, or makes chalk longer for
compiler convenience.

## 5. Wave map

See [WP-0088](documentation-compression-map.md) (**complete** —
levers shipped). Follow-on program (adoption of shipped levers + remaining
sugars under one plan): [WP-0089](documentation-compression-map.md).

| Wave | Nature | Enterprise feel impact |
|---|---|---|
| **A** | Examples + docs only | High for learners (first impression) |
| **B** | ADRs (surface sugar / profiles) | High for all new code |
| **C** | Kernel Green after Accept | Realizes B in Shipping Kernel |
| **0089** | Adoption of A–C levers + next sugar ADRs/Kernel + re-sync | Closes “lever shipped, face still old” |

## 6. Success definition (program)

When an unfamiliar physicist opens B01/B08 (and a thin S01 spine excerpt):

- they see **physics first**, not packages and constructors
- they do **not** think “this is Java”
- they still see NLTS / when / measure as laws, not style nits
