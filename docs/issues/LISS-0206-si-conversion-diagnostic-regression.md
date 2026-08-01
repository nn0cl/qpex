# LISS-0206: Unknown SI unit-conversion pairs produce no diagnostic

## Metadata

- Local issue ID: LISS-0206
- Status: **complete** — 2026-08-01 (WP-0075)
- Phase: phase-0-design
- Type: bug
- Priority: P1
- Planning size: S
- Program: [WP-0069](../work-plans/WP-0069-operations-review-intake.md)
- Related: ADR 0124 / 0129 / 0132 / 0134–0136 (SI scale + affine `expr to unit`);
  ADR 0155 (mixed-unit canonical promote)
- Blocked by: [LISS-0202](LISS-0202-linear-discipline-regression-cluster.md)

## Intent

`expr to unit` with an unconvertible or unknown unit pair is expected to emit
`TYPE_MISMATCH` (or fail to parse). Neither happens — the conversion is
accepted silently.

## Evidence (reproduced 2026-08-01)

`tests/test_si_scale_conversion_red.py`:

```
assert "TYPE_MISMATCH" in unknown or "PARSE_ERROR" in unknown
AssertionError
```

`tests/test_si_scale_catalog_wave2_red.py` fails on the same assertion shape.

Affected files (2):

```
tests/test_si_scale_conversion_red.py
tests/test_si_scale_catalog_wave2_red.py
```

Silently accepting an unconvertible pair is worse than a wrong number: a
dimensionful physicist program keeps running with a magnitude that was never
rescaled. This is a correctness issue in the Type-First dimension surface, not
a diagnostics nicety.

Adjacent observation for the same investigation (not asserted by any suite):
the Host-side unit vocabulary in `compiler/staqex/scientific_input.py`
(`cm`, `angstrom`, `Å`, `ms`, `us`, `ns`, `Ha`, `rad`, `deg`) and the Kernel
conversion tables in `compiler/staqex/dimensions.py` (`nm`, `kHz`, `MHz`,
`GHz`, `eV`, `K`, …) are largely disjoint. Whether that is intended (two lanes)
or drift should be settled while here.

## Adjudicator decision points

1. Which unit pairs must hard-fail vs be accepted? The suites encode an
   expectation that the current tables do not honor — decide which is
   authoritative.
2. Are Host-validated units and Kernel-convertible units deliberately separate
   vocabularies? If yes, say so in the spec; if no, they must converge.

## Exit

- [x] Unconvertible / unknown pairs emit a hard diagnostic
- [x] Both suites green
- [x] Host vs Kernel unit vocabulary relationship recorded in the spec

## Non-goals

Extending the SI catalog with new units; display-unit restore
([LISS-0197](LISS-0197-display-unit-restore-deferred.md), deferred); the other
regression clusters.

## Resolution (WP-0075)

Kernel already hard-fails unknown units with `TYPE_MISMATCH`. Suites used
shipped `lb` as the "unknown" target; updated to `bob`.
