# ADR 0181: Named struct construction (+ no mandatory struct init)

## Status

**Accepted** (2026-08-03) — Adjudicator「承認」
([WP-0089](../../work-plans/WP-0089-surface-adoption-and-sugar.md)).
Architecture Accept freezes the decision below. Kernel Red authorized via
linked LISS Kernel children. No axiom rewrite.

Original draft companions retained; open checklist frozen in §Acceptance record.

Companions: physicist-dx-harmony (struct = parameter packs); LISS-0268;
LISS-0277 inventory (nested struct construction gap).

## Context

Positional `Segment(2.0, Open)` and class `fn init` / `this` assignment theaters
read as Java beans. Modern record languages use named fields. Separately,
LISS-0277 recorded that **nested struct construction** (`Board(leaf, leaf)`)
fails in the shipping Kernel while class boards succeed — leaf structs are
already used for CommandBoard, FieldRequest, etc.

## Dependency Adoption Evidence

Not applicable.

## Decision

### Construction forms

1. **Named form (new, preferred for teaching):**

   ```text
   Segment { length: 2.0, bc: Open }
   ```

   Field order free; all required fields must appear unless defaults are Accepted later.

2. **Positional form remains valid forever in v1:**

   ```text
   Segment(2.0, Open)
   ```

3. **Structs do not require `fn init` / `this`.** Construction is value assembly.
   `class` keeps `fn init` for true physical systems.

### Nested packs

4. Nested `struct` construction must succeed when field types are already
   constructible structs or enums (close the LISS-0277 Kernel gap).  
   Fail-closed diagnostics if a field is missing or mistyped.

### Explicit non-goals

- Mutable bean setters
- Partial construction with silent zero-fill (unless a later ADR adds defaults)
- Changing class init semantics

## Consequences

Positive:

- Parameter packs read as named coefficients
- Unblocks demoting more S01 boards from class to struct after ship

Negative:

- Parser/typechecker work; dual construction forms to maintain

## Enforcement

- Red: named construct, positional still works, nested struct Board of leaves
- S01 may migrate leaf-heavy boards in LISS-0289 after Green

## Alternatives considered

| Option | Note |
|---|---|
| Only field-sugar `Type(field = expr)` | Also acceptable if Accept prefers; must pick one primary |
| Force named only | Breaks existing positional samples |

## Acceptance checklist

- [ ] Exact surface chosen: `{ field: expr }` vs `(field = expr)` vs both
- [ ] Nested struct construction required yes/no (recommend **yes**)
- [ ] Adjudicator Accept
- [ ] Kernel child LISS-0284 unblocked only on Accept
