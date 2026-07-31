# LISS-0138: `when` arms with ket / prepare literals

## Metadata

- Local issue ID: LISS-0138
- Status: **ready** — filed from S1 discovery; not started
- Phase: Feature Path (awaiting Plan / batch authorize)
- Type: Kernel residual / language
- Priority: P2 (S1 uses classical `when` label arms like B02)
- Depends on: none hard; discovered by [LISS-0134](LISS-0134-showcase-s1-thin-slice.md)
- Implementation permission: **none** until Adjudicator Plan/Phase approve
- Branch: TBD (`feature/liss-0138-…`)

## Summary

Physicist-legible prepare branching wants:

```text
state prep = when (bit) {
  0 -> |0>,
  else -> |+>,
}
```

This may **parse/typecheck** but fails at runtime with
`cannot evaluate KetLit as value`. S1 workaround: classical `when` label
arms + separate `| +>` prepare (B02 pattern).

## Exit

- [ ] Red suite for ket (and optionally other State constructors) in `when` arms
- [ ] Green: prepare branching without classical label indirection
- [ ] Basics / showcase may teach ket-`when` as preferred prepare style
- [ ] Spec / axiom note if intentionally forbidden (then demote to permanent-out)

## Ambiguity (do not guess)

- Whether ket arms are in-scope for v1 or permanently classical-only `when`
  — Adjudicator decision if Red shows deep evaluator gaps.
