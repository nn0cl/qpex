# Open Topics before S1 (Option B) — program plan

| Field | Value |
|---|---|
| Status | **complete** — 2026-07-31; LISS-0129/0133/0135 shipped; S1 authorize unblocked |
| Decision | Option B closed; showcase **S1** may be authorized separately |
| Mission | Still [P2 lock](staqex-v1-showcase-mission-lock.md) (quantum-matter / Noether Forge) |
| S0 | Remains valid docs; S1 authorize stays **blocked** until this program exits |
| Parent Issue | [LISS-0128](../architecture/documentation-compression-map.md) |
| Work plan | [WP-0030](../architecture/documentation-compression-map.md) |

```markdown
[DESIGN CHECK]
- Scope: Option B — selected topics get ADR/spec + ship (or honest reconcile)
  before S1; remaining get permanent-out / no-further-ship.
- Not in scope: starting S1 .sqx Red; live QPU; reclaiming LISS-0120;
  re-shipping already Runtime-complete surfaces without a named gap.
- Ambiguity: none remaining for docs children; LISS-0129 Plan still required
  before Red.
```

## 1. Why pause S1

P1 ledger marked Open Topics **out** so the showcase would not pretend they
were shipped. Option B rejects that trade-off for **selected** topics: the
Adjudicator wants specification **and** implementation complete first, then
honest required-row coverage for S*.

## 1.1 Inventory correction (must confirm before Red)

Agent “Current Open Topics” lists are **stale** vs repository evidence. Do not
re-ship what is already Accepted/Runtime complete.

| Topic | Agent Open Topics claim | Repository evidence | Option B implication |
|---|---|---|---|
| `evolve … until` | open | ADR 0079 **Accepted**; LISS-0012 **Runtime complete**; axioms **Shipped**; tests present | **LISS-0130 → docs/ledger reconcile** (not full re-implement), unless Adjudicator names a missing slice |
| `\|>` / currying | open | ADR 0080 + LISS-0013 Phase 3 reviewed | Prefer **permanent-out of further expansion** or ledger → shipped; not blank re-ship |
| Trait `impl` / effect marking | open | ADR 0081/0082 + LISS-0014/0015 reviewed | Same as above |
| ADR 0057 density/Lindblad | open | open-work: **Complete** numeric/runtime; residuals named | **LISS-0131 = showcase boundary honesty**, not silent full CPTP |
| Typed surface annotations | open | F-07 still **PARSE_ERROR** on probe | **LISS-0129 remains real ship work** |
| SI beyond / continuous PDF / exact rational / live QPU IR | open | still deferred | Keep in permanent-out (§3) |

## 2. Selected before S1 (revised recommendation)

| ID | Topic | Why | Exit (recommended) |
|---|---|---|---|
| [LISS-0129](../architecture/documentation-compression-map.md) | Typed surface `state x: State<T> = …` | F-07 real gap | ADR + Kernel parse/typecheck + Red suite (**ship**) |
| [LISS-0130](../architecture/documentation-compression-map.md) | `evolve … until` | Stale Open Topic / ledger lie | **Docs + ledger → shipped**; ship only if Adjudicator names a gap |
| [LISS-0131](../architecture/documentation-compression-map.md) | ADR 0057 showcase boundary | Mission honesty | Boundary note + optional named Kernel slices only |

## 3. Permanent-out / no-further-ship before S1

Document via [LISS-0132](../architecture/documentation-compression-map.md):

| Topic | Rationale |
|---|---|
| Further `\|>` / currying expansion | Minimal surface already shipped; fusion/partial-app deferred |
| Further trait `impl` / effect rows | Core shipped; dispatch specialization deferred |
| SI beyond (L,M,T) | Tags suffice for finite spin models |
| Continuous PDF / Monte Carlo | Continuous discretization forbidden in v1 showcase |
| Exact rational vs f64 | Keep f64 policy |
| Concrete QPU IR / live provider | Ports + static CH0/SIM honesty only |

## 4. Also tracked (not Option B Open Topics; language residuals)

From LISS-0122/0123 heals — may run **in parallel** but do not substitute for
§2:

- consume-on-return LINEAR
- namespace `Float` return bind
- soft MULTI false positive
- Type-First ⊕ State arithmetic

Suggest umbrella **LISS-0133** after §2 starts, or fold into post-S1 debt if
Adjudicator demotes.

## 5. Execution order

```text
LISS-0132 permanent-out + stale-Open-Topics reconcile (docs)
    │
    ├─► LISS-0130 evolve-until ledger/docs reconcile (docs; ship only if gap)
    ├─► LISS-0129 typed surface (ADR → Red → Green → Refactor)  ← real ship
    └─► LISS-0131 ADR 0057 boundary (docs first; ship only if gap named)
            │
            ▼
     Revise P1 coverage ledger + agent Open Topics lists
            │
            ▼
     Adjudicator authorize S1 (new Issue LISS-0134+)
```

0131 must not silently expand full Lindblad CPTP without a named ship list.

## 6. Gates this program does **not** grant

- S1/S2/S3/S4 `.sqx` implementation
- Changing P2 mission theme
- Accepting permanent-out topics by silence
- Re-implementing already-shipped surfaces without a named gap

## 7. Adjudicator confirm points (before Red)

- [x] Accept §1.1 inventory correction (esp. `evolve until` already shipped)
- [x] Confirm §2: keep **0129 ship**; **0130 docs-only** unless gap named; **0131 boundary**
- [x] Confirm §3 permanent-out / no-further-ship list
- [x] ADR 0057: **boundary doc only** (no named Kernel slices before S1)
- [x] Authorize first Issue: **LISS-0132** docs, then **0129** Plan
- [x] Fold language residuals (§4) into **LISS-0133** before S1? **No** (default)
