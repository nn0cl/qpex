# ADR 0156: Atomic mass unit `u` and bare `.ton` alias

## Status

**Accepted** (2026-07-31) — unlocks LISS-0188 / LISS-0189 under WP-0062.
Extends [ADR 0150](0150-us-uk-ton-mass.md) / [ADR 0151](0151-troy-ounce-mass.md).

## Decisions

1. ASCII suffix `.u` denotes the **unified atomic mass unit** (dalton) on Dim
   Mass. Conversion uses the CODATA 2022 recommended value
   \(1\,\mathrm{u} = 1.66053906892\times 10^{-27}\,\mathrm{kg}\).
2. Bare ASCII suffix `.ton` is an alias for the US short ton
   ([ADR 0150](0150-us-uk-ton-mass.md) `.ton_us`): \(1\,\mathrm{ton} = 2000\,\mathrm{lb}\).
3. Metric tonne remains `.t` only. UK long ton remains `.ton_uk` only.
4. Microsecond remains `.us` (ADR 0129); it does not collide with `.u`.
5. Display-unit restoration after canonical promote was deferred (LISS-0197);
   **shipped** by [ADR 0186](0186-display-unit-restore.md) / LISS-0314.

## Deferred

Dalton alias `.Da`; bare `.ton` meaning UK long ton (not US).
