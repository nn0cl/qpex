# ADR 0173: `measure … tracing_out …` leftover LINEAR policy

## Status

**Accepted** (2026-08-02) — Adjudicator「承認」on Proposed draft
([LISS-0249](../documentation-compression-map.md)).
Architecture approval only. Kernel / HIR / S01 spine edits wait for Feature
Issue [LISS-0250](../documentation-compression-map.md) with
explicit Phase 1 Red approval.

Companions:

- [ADR 0167](0167-linear-obligation-follows-carrier-type.md) (carrier type → LINEAR)
- [ADR 0107](0107-linear-uncompute-amplitude-tolerance.md) (`|0>` / vacuum uncompute)
- [ADR 0138](0138-trace-out-gc-fn-scope.md) / [ADR 0044](0044-typed-product-state.md)
  (`Joint.trace_out` / expression `trace_out(coord)`)
- [physicist-minimal-dialect.md](../physicist-minimal-dialect.md) §3 / Class E
  LINEAR tax kill
- [S01 scorecard](../../specs/staqex-v1-s01-coverage-scorecard.md) LINEAR residual

## Context

Never Leave the State forbids silent drop of linear carriers. Today a
multi-wire notebook that measures only one site must either:

1. **Hand-kill** leftovers with `state sibling = |0>` (static uncompute witness,
   ADR 0107), or
2. Attempt expression `trace_out(coord)` — which is a Born partial trace in the
   evaluator, but is awkward under LINEAR: a `state _t = trace_out(s1)` bind
   moves `s1` (ADR 0168) yet introduces a new State-shaped placeholder that
   itself needs consumption; a Classical-typed bind of the same Call does
   **not** move `s1`, so `LINEAR_IMPLICIT_DISCARD` remains.

Pedagogy (Accepted minimal dialect) forbids teaching option (1) as the normal
story: it looks like uncomputation but is usually a ritual reset, conflating
computational-basis witness with honest discard. The dialect ideal is:

```text
measure s0 tracing_out s1
```

— one terminal observation; named leftovers leave via explicit partial trace.

Automatic Trace-Out GC (ADR 0138 / 0142 / 0153 / 0158) already drops **dead
fn-local** coordinates after Calls / blocks. It does **not** authorize unnamed
discard of still-live wires in `main` at the terminal measure boundary.

## Dependency Adoption Evidence

Not applicable. No new dependency.

## Decision

### 1. Surface (MVP)

Authorize a terminal `measure` clause:

```text
measure <primary> tracing_out <name> [, <name> ...]
```

- `<primary>` remains a single Var (unchanged terminal-measure shape).
- `tracing_out` lists one or more distinct leftover linear carrier names.
- Empty `tracing_out` lists are a parse / check error.
- Rest-sugar (`tracing_out others` / `*`) is **out of MVP**; name every leftover.

Optional sink / POVM clauses (existing `Measure` AST fields) stay orthogonal:
order is `measure <primary> [povm…] [to sink…] tracing_out …` — exact token
order is fixed in the Feature Red grammar against this ADR; do not invent a
second measure family.

### 2. Semantics (Simulator / Shipping Kernel)

At a terminal `measure … tracing_out …`:

1. For each leftover name, in source order, apply the same Born partial trace
   as `Joint.trace_out(name)` (no RNG; not `project`; not computational `|0>`
   rewrite).
2. Then sample / collapse `<primary>` under existing measure rules (RngPort,
   MeasureSinkPort unchanged).
3. HIR LINEAR: each listed leftover root is **consumed** by the clause; the
   primary is consumed by measure as today.
4. Diagnostics:
   - leftover not a live linear carrier → type / LINEAR error (fail closed).
   - leftover equals primary, already consumed, or duplicate in the list →
     `LINEAR_DUPLICATE_USE` (or a dedicated `TRACING_OUT_*` code if Red needs
     sharper messages — same obligation).
   - live linear carriers **not** measured and **not** listed remain
     `LINEAR_IMPLICIT_DISCARD` (Never Leave the State).

### 3. Not uncompute

`tracing_out` is **explicit discard / partial trace**. It:

- does **not** require ADR 0107 `|0>` / vacuum amplitude witnesses;
- does **not** imply an adjoint circuit or unitary round-trip;
- must not be taught as “uncompute to ground.”

Hand `state x = |0>` remains valid **uncompute witness** where the program
truly means that; dialect and S01 spine should prefer `tracing_out` for
leftover siblings after Accept + Green.

### 4. Relation to expression `trace_out(coord)`

- Expression `trace_out(coord)` and automatic Trace-Out GC stay.
- Pedagogical primary for leftover wires at the result boundary is the
  `measure … tracing_out …` clause.
- **Companion amendment (same Accept):** a Call to builtin `trace_out` always
  **consumes** its State argument for LINEAR, regardless of whether the bind
  head is State, Classical, or a discard placeholder. Physics remains
  `Joint.trace_out`; only the obligation bookkeeping changes. This closes the
  Classical-bind hole without requiring a measured placeholder.

### 5. Scope limits

- MVP is Shipping Kernel + HIR LINEAR only.
- QPU / OpenQASM backends: record a **backend obligation** (partial trace or
  honest non-support diagnostic). Do not invent a silent classical drop in
  emitters under this ADR.
- Density-matrix / CPTP Trace-Out (ADR 0057 lineage) is out of scope.
- Does not weaken terminal-measure / early-collapse rules (still one terminal
  measure per `main` path).

### 6. Follow-up (post-Accept)

1. Feature Issue [LISS-0250](../documentation-compression-map.md):
   grammar + AST `Measure.tracing_out` → HIR consume → evaluator order →
   SV / Red–Green–Refactor (requires separate Phase approval).
2. S01 spine / dialect samples: replace ritual `|0>` sibling kills with
   `tracing_out` where the intent is leftover discard (scorecard LINEAR Class E
   residual) — after Green, or a follow-on Issue.
3. Next ADR batch items (Type-First fields; failure glossary) remain separate.

## Consequences

Positive:

- Dialect §3 ideal becomes a real surface; kills LINEAR tax theater without
  silent discard.
- Aligns leftover policy with existing Born `trace_out` physics.
- Clarifies uncompute vs discard for reviewers and agents.

Negative / costs:

- New grammar + LINEAR paths; samples and scorecard must migrate after Green.
- Named-only MVP is slightly verbose vs `others` sugar (deferred deliberately).
- QPU lowering remains an open port obligation.

## Enforcement

Code review / Adjudicator should reject:

- Implementing Kernel `tracing_out` without [LISS-0250](../documentation-compression-map.md)
  Phase approval (Accept alone is not Red/Green authorization).
- Teaching `|0>` hand-kill as the default leftover story after Kernel Green
  on dialect / S01 spine mains.
- Silent leftover GC at terminal measure without a `tracing_out` list.
- Treating `tracing_out` as ADR 0107 uncompute (amplitude / vacuum checks).
- Rest-sugar or multi-primary measure invented outside a new ADR.
