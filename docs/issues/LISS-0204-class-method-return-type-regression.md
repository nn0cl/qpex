# LISS-0204: Class / namespace methods return `Classical<T>` where `State<T>` is declared

## Metadata

- Local issue ID: LISS-0204
- Status: **complete** — 2026-08-01 (WP-0075)
- Phase: phase-0-design
- Type: bug
- Priority: P1
- Planning size: M
- Program: [WP-0069](../work-plans/WP-0069-operations-review-intake.md)
- Related: ADR 0116 (classical Type-First ⊕ State arithmetic) / LISS-0133;
  ADR 0054–0056 / 0058 (namespace / class / visibility)
- Blocked by: [LISS-0202](LISS-0202-linear-discipline-regression-cluster.md)

## Intent

Methods declared to return `State<Float>` are inferred as returning
`Classical<Float>`, so the modern-OOP surface no longer typechecks.

## Evidence (reproduced 2026-08-01)

`tests/test_modern_oop_and_visibility.py`:

```
AssertionError: [{'code': 'RETURN_TYPE_MISMATCH', 'line': 9, 'col': 5,
  'message': '`step` returns Classical<Float>, declared State<Float>'}, …]
```

Affected files (5):

```
tests/test_encapsulation_and_module_info.py
tests/test_function_signatures_red.py
tests/test_modern_oop_and_visibility.py
tests/test_namespace_and_class_methods.py
tests/test_oop_namespace_enum_struct.py
```

The `Classical<…>` carrier is the ADR 0116 classical Type-First lane. The
suspicion is that classical/State arithmetic inside a method body now collapses
the result to the classical carrier rather than keeping the State pushforward —
which would be a Never-Leave-the-State violation, not merely a typing nit.

## Adjudicator decision points

1. **Physics-law question, not a typing question.** If a method body that mixes
   a classical coefficient with a `State` now yields `Classical<Float>`, the
   state was left. Confirm whether the correct fix is (a) the carrier inference
   must keep `State`, or (b) these suites were always relying on an inference
   that ADR 0116 deliberately narrowed.
2. If (b), the modern-OOP surface documentation and
   [`agent-sync-modern-oop-visibility.md`](../collaboration/agent-sync-modern-oop-visibility.md)
   need updating, because the shipped examples teach the old shape.

## Exit

- [x] Ruling on carrier inference vs suite expectation
- [x] Never-Leave-the-State confirmed preserved either way
- [x] Five suites green
- [x] Docs updated if the surface narrowed

## Non-goals

Revisiting ADR 0116; changing visibility or `fn init` / `this` semantics; the
other regression clusters.

## Resolution (WP-0075)

Adjudicator locked ADR 0116: Type-First `Float` is Classical. Suites that
declared `-> State<Float>` for pure classical method results now declare
`-> Float`. `dirac(this.x + this.x)` remains `State<Float>` in
`test_function_signatures_red.py`. Explicit `return` required on `read()`.
