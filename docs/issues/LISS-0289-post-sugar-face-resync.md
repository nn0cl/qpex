# LISS-0289: Post-sugar face re-sync (basics / S01 / A06)

## Metadata

- Local issue ID: LISS-0289
- GitHub issue: _(none yet)_
- Status: **complete** (2026-08-03)
- Phase: Feature examples (+ tiny Kernel parse fix for `import ..`)
- Type: Feature Path
- Priority: P0 (program closure)
- Program: [WP-0089](../work-plans/WP-0089-surface-adoption-and-sugar.md)

## Summary

Terminal consistency pass: official faces use shipped WP-0089 sugars.

## Done

- **B01 / B08:** default experiment profile (no marker), local inference
- **B07:** named struct `Segment { length, bc }`
- **B09:** package-relative `import .domain…`
- **S01 spine:** `import .domain…` + named leaf structs
- **S01 chapters:** parent-relative `import ..domain…` / `..physics…`
- **A06:** relative import + named leaf structs
- **Kernel:** parse `import ..path` (RANGE token) for parent-relative

## Exit

- [x] B01/B08 inference + default profile
- [x] S01 relative import + named structs
- [x] A06 updated
- [x] Aesthetic north-star first screen (B08 chalk)
- [x] seed-0 + SV
- [x] WP-0089 → complete

## Verification

```bash
python3 -m compiler.staqex run examples/basics/B08_operators_hamiltonians/operators_hamiltonians.sqx --seed 0
python3 -m compiler.staqex run examples/showcase/S01_quantum_disaster_response/main_disaster_response.sqx --seed 0
python3 tests/spec_verification/run_all.py
```
