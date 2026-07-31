# Open Topics permanent-out / no-further-ship (pre-S1)

| Field | Value |
|---|---|
| Status | **Accepted** (2026-07-31) — Adjudicator Option B §7 confirm |
| Issue | [LISS-0132](../issues/LISS-0132-open-topics-permanent-out.md) |
| Program | [open-topics-before-s1-program](staqex-v1-open-topics-before-s1-program.md) |
| Not | S1 authorize; typed-surface implementation; silent re-open of parked topics |

```markdown
[DESIGN CHECK]
- Scope: record pre-S1 permanent-out / no-further-ship for topics not in
  Option B ship set; reconcile stale agent Open Topics claims.
- Not: Kernel code; LISS-0129 Red; live QPU.
```

## 1. Decision

Before showcase **S1**, the following are **not** scheduled for further
specification or Kernel expansion. Showcase and agents must not pretend they
are unfinished “required Open Topics.”

| Topic | Classification | Notes |
|---|---|---|
| Further `\|>` / currying (fusion, partial-app values) | **no-further-ship** | Minimal surface already shipped (ADR 0080 / LISS-0013). Expansion deferred past S1. |
| Further trait `impl` / effect rows / specialization | **no-further-ship** | Core shipped (ADR 0081–0082 / LISS-0014–0015). |
| SI scale beyond $(L,M,T)$ tags | **permanent-out (pre-S1)** | Tags suffice for finite spin / quantum-matter spine. |
| Continuous PDF / Monte Carlo | **permanent-out (pre-S1)** | Continuous discretization forbidden in v1 showcase. |
| Exact rational vs `f64` masses | **permanent-out (pre-S1)** | Keep `f64` policy (ADR 0097 horizon remains separate). |
| Concrete live QPU IR / provider credentials | **permanent-out (pre-S1)** | Ports + static CH0 / SIM honesty only. |

## 2. Still scheduled under Option B (not out)

| Topic | Issue | Mode |
|---|---|---|
| Typed surface annotations | [LISS-0129](../issues/LISS-0129-typed-surface-annotations.md) | **ship** (ADR → Feature Path) |
| `evolve … until` ledger honesty | [LISS-0130](../issues/LISS-0130-evolve-until.md) | **docs reconcile** (already Runtime complete) |
| ADR 0057 showcase boundary | [LISS-0131](../issues/LISS-0131-density-lindblad-showcase-boundary.md) | **boundary doc only** (no silent full CPTP) |

## 3. Language residuals (not Open Topics; default post-S1)

Consume-on-return LINEAR, namespace `Float` return bind, soft MULTI false
positive, Type-First ⊕ State arithmetic — tracked as optional **LISS-0133**;
Adjudicator default **do not** block S1 (2026-07-31 §7).

## 4. Agent contract obligation

Update Claude “Current Open Topics” (and any mirrored stale lists) so shipped
or permanent-out items are not listed as “not yet Accepted / not shipped.”
See [LISS-0132](../issues/LISS-0132-open-topics-permanent-out.md) exit +
instruction-change trace.
