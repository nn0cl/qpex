# LISS-0037: POVM, measurement, and channel contracts

- Status: **proposed** (Architecture Path; design only)
- Depends on: LISS-0011, ADR 0057, LISS-0028
- Blocks: general measurement and open-system semantics

## Summary

Define POVMs, measurement effects, projectors, classical result carriers, and
their relation to density matrices and CPTP maps. Terminal `measure` remains
the default language boundary. Mid-circuit measurement is owned by the Dynamic
QPU lane and must not be introduced as an implicit shortcut.

## Acceptance questions

- Which measurement forms are terminal-only and which require Dynamic QPU
  capability?
- How are outcome spaces and probabilities typed?
- How do channels compose with `State<T>` and the future density representation?
- What result DTO crosses into the Job/report boundary?

## Non-goals

This issue does not replace or split the density/Lindblad representation
decision in LISS-0011.
