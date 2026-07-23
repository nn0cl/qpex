# LISS-0033: Symbolic expression IR and lowering provenance

- Status: **proposed** (Architecture Path; design only)
- Depends on: LISS-0030/0031, LISS-0019, LISS-0017, LISS-0018
- Blocks: trustworthy theory-to-QPU lowering

## Summary

Define an expression-preserving IR between QPex source and executable QPU IR.
The IR must retain binder structure, domains, operator algebra, mappings,
discretization, approximation policy, and source provenance long enough to
support diagnostics and honest result reporting.

## Acceptance questions

- What is the stable boundary between symbolic, resolved, and executable IR?
- Which rewrites are semantics-preserving and which require an error budget?
- How are Trotter/Suzuki order, step count, mapping, and discretization
  recorded?
- Can a diagnostic point back to the original formula rather than only to a
  lowered gate?

## Non-goals

No concrete backend, QPU provider, or cloud credential policy is selected by
this LISS.
