# Surface style guide (official samples)

| Field | Value |
|---|---|
| Status | **Teaching / review law** (LISS-0307) — not an axiom rewrite; not Kernel ban |
| Parents | [re-review](2026-08-03-language-design-rereview.md) P2, [minimal dialect](physicist-minimal-dialect.md), [physicist-dx-harmony](physicist-dx-harmony.md), [bind-decision-tree](bind-decision-tree.md) |

Use this when writing or reviewing official `.sqx` under `examples/`.

## 1. Constructors (P2-1)

| Prefer | When |
|---|---|
| **Named** `Type { a: e, b: f, … }` | ≥3 fields, Type-First units, or any field that is not obvious positionally |
| **Positional** `Type(a, b)` | 1–2 scalar chalk packs (`IsingCouplings(1.0, 0.5)`) |

Do not invent a third constructor form. Both remain legal Kernel surface.

## 2. Struct + free-fn vs `class` (P2-2)

| Prefer | When |
|---|---|
| `struct` + free scores / Operator factories | Pure parameter packs and pure scores |
| `class` + `fn init` / `this` | Mutable clock / true system seat, or interface `impl` receiver |
| Config harvest class (B09) | Only where ADR 0061 harvest is the teaching point |

Do not reintroduce DTO `class` forests for Float boards.

## 3. Package path depth (P2-3)

- Root stays **`examples.…`** (not reverse-DNS).
- Prefer short lane package tails: `…s01_disaster`, `…morning_lane` — avoid deeper product-style nests when a sibling package works.
- Multi-file honesty may keep `package` + `main`; that is a module lesson, not failure of chalk.

## 4. Unicode (P2-5)

- **ASCII keywords primary** in official samples (`evolve`, `measure`, `when`).
- Dirac sugar `⟨φ|ψ⟩` only where already Accepted and helpful; do not force full Unicode chalk.

## 5. Soft diagnostics (P2-4)

Soft `QSEM_*` on green runs is **honest IR**, not failure — see
[QUICKSTART](../../QUICKSTART.md) §1.

## 6. Inspect peeks

≤1 notebook `inspect` per main unless a chapter is explicitly about
diagnostics. Host owns structured logs.

## 6b. Lane markers (ADR 0178)

Every multi-file **entry** `main_*.sqx` should start with one of:

```text
// staqex-lane: experiment
// staqex-lane: circuit
// staqex-lane: open
```

Single-file basics default to experiment when unmarked. Do not mix
circuit-only constructs into unlabeled experiment spines.

## 7. PR checklist bullets (samples)

When changing official examples:

- [ ] Blackboard H / ket / evolve not longer for compiler convenience
- [ ] No new inspect museum / identity evolve theater
- [ ] New pure packs are struct + free-fn (not DTO class)
- [ ] Constructors follow §1; package depth follows §3
- [ ] seed-0 still green where claimed
- [ ] Multi-file entry has `// staqex-lane: …` (ADR 0178)
