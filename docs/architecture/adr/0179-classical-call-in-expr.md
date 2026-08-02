# ADR 0179: Pure classical Call as expression operand

## Status

**Proposed** (2026-08-02) — [LISS-0267](../../issues/LISS-0267-adr-classical-call-in-expr.md) /
[WP-0088](../../work-plans/WP-0088-surface-modernization.md).
**Not Accepted.**

Companions: evaluator Phase 2.2 value context; LISS-0256 note (`f() * x` failed).

## Context

Modern languages allow pure function results in arithmetic. Staqex currently
rejects classical Calls as operands in some value contexts:

```text
Float x = corridor.blockage_pressure() * 0.4  // may fail
// requires:
Float b = corridor.blockage_pressure()
Float x = b * 0.4
```

That is pure DX friction, not physics law.

## Decision (proposed)

1. **Allow** pure **classical** Calls (and method Calls whose type is a classical
   head: `Float` / `Int` / `Bool` / Type-First quantity heads as already
   classical-elaborated) as operands in classical binary/unary expressions and
   as classical arguments.

2. **Still reject** (fail-closed):
   - Calls that produce or require Joint/`State` mid-expression in ways that
     would imply early collapse
   - Using State-forming Calls as if they were classical Floats
   - Classical `if` / short-circuit control

3. Evaluation order: left-to-right for classical operands; document in spec.

4. Existing temp-bind style remains valid.

## Consequences

- Evaluator / typecheck changes (Wave C Red).
- Cleaner S01-style domain→coeff wiring.
- No change to NLTS.

## Alternatives

| Option | Note |
|---|---|
| Keep bind-first forever | Permanent anti-modern DX |
| Allow all Calls in expr | Unsafe for Joint |

## Acceptance checklist

- [ ] Accept classical set of types/calls
- [ ] List invalid cases in diagnostic catalog
- [ ] Kernel Red child on Accept
