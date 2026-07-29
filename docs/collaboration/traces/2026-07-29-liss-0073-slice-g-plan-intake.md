# Trace: LISS-0073 Slice F completion + Slice G plan intake

| Field | Value |
|---|---|
| Date | 2026-07-29 |
| Issue | LISS-0073 |
| Path | Feature Path — Slice F closeout + Slice G plan (docs) |
| Phase | slice-f done; slice-g phase-0-design |
| Branch | `feature/liss-0073-slice-f-red` |
| Implementation | **forbidden** for Slice G until plan approval |

## [DESIGN CHECK]

- Scope: close Slice F after Green/Refactor approval; propose Slice G only —
  freeze §4 formula→AST map; proof suite; formatter emit policy note; mark
  Issue complete on Green. No new punctuation.
- Specs: LISS-0073 acceptance notes; plan §4–5; A–F shipped surfaces.
- Boundaries: no Physics IR / NFC / M-P06 deprecate / full pretty-print.
- Decisions pending: proof-suite shape; emit-policy wording; Red authorization.
- Verification: land Slice F via PR; docs for G plan; no G Green yet.

## Slice F completion evidence

- Suites A–F PASS
- Commits: Red → Green on this branch

## Slice G requested approval

**Plan approval** for Slice G only with recommended deliverables above.

Adjudicator approved Slice G plan (“承認”). Red suite added.

## Next safe action

Adjudicator Red approval → Slice G Phase 2 Green.
