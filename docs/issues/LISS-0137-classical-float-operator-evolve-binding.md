# LISS-0137: Classical Float binding into Operator / `evolve for`

## Metadata

- Local issue ID: LISS-0137
- Status: **ready** — filed from S1 discovery; not started
- Phase: Feature Path (awaiting Plan / batch authorize)
- Type: Kernel residual / elaboration
- Priority: P1 (S1 workaround: literals + inspect-only schedule values)
- Depends on: related to [ADR 0114](../architecture/adr/0114-classical-coefficient-elaboration-vs-linear.md) / LISS-0121 territory
- Discovered by: [LISS-0134](LISS-0134-showcase-s1-thin-slice.md)
- Implementation permission: **none** until Adjudicator Plan/Phase approve
- Branch: TBD (`feature/liss-0137-…`)

## Summary

Classical `Float` values that come from:

- struct field reads (`c.J` bound to `Float J = c.J`), or
- class method returns (`schedule.t()` → `Float duration`),

often **compile** but **fail at runtime** when used as Operator coefficients
(`unbound Operator / scalar …`) or as `evolve … for duration`
(`unbound variable duration`). Literals work. Inspecting those Floats as
observation intent works.

Namespace free functions returning Float/struct also fail differently
(`unsupported method …`, `unknown struct constructor …`), while A06-style
class methods and bare hop-builder imports succeed — track as the same
classical-elaboration / call-site binding family unless Adjudicator splits.

## Exit

- [ ] Red suite covering field→Operator, method→`evolve for`, and free-fn classical return
- [ ] Green: named classical Floats from domain/protocol packs usable in Operator and duration
- [ ] S1 / future showcase can drop literal-duration workaround
- [ ] ADR note if elaboration policy changes

## Non-goals

- Changing LINEAR consume rules for true quantum resources
- Live QPU duration binding
