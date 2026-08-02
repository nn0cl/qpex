# LISS-0264: ADR — experiment surface profile (largest de-enterprise lever)

## Metadata

- Local issue ID: LISS-0264
- GitHub issue: https://github.com/nn0cl/staqex/issues/274
- Status: **open** — ADR **0176 Proposed** (draft filed); **Accept pending** Adjudicator
- ADR: [0176-experiment-surface-profile.md](../architecture/adr/0176-experiment-surface-profile.md)
- Type: Architecture Path (ADR)
- Priority: **P0** (personal goal: kill enterprise package face)
- Program: [WP-0088](../work-plans/WP-0088-surface-modernization.md)
- Depends: [LISS-0261](LISS-0261-surface-modernization-north-star.md) **complete**

## Intent

Propose an **experiment surface profile** (name TBD) so short physics programs
need not look like:

```text
package com.staqex.examples.basics.operators_hamiltonians
pub fn main() -> Unit { … }
```

Candidates (Adjudicator picks):

| Option | Idea | Risk |
|---|---|---|
| A | Default package for `examples/` / `experiment` files | Module resolve |
| B | `experiment { … }` block elides `main -> Unit` wrapper in teaching | Parsing / entry |
| C | Edition / profile flag: `staqex experiment 1` short mode | Tooling |
| D | Allow file-level `main` without `pub fn … -> Unit` sugar | Entry ABI |

**Must preserve:** single terminal measure story; Host Job entry still clear;
no second language semantics.

## Exit

- [x] ADR **Proposed**: [`docs/architecture/adr/0176-experiment-surface-profile.md`](../architecture/adr/0176-experiment-surface-profile.md)
- [x] Concrete before/after spellings (in ADR 0176)
- [x] Migration / non-goals (in ADR 0176)
- [ ] Adjudicator Accept / revise / reject
- [ ] On Accept: follow-up Kernel Issue under LISS-0269 (not this Issue)

## Non-goals

- Kernel Green in this Issue
- Forcing S01 multi-file tree to single file
- Removing modules for large programs

## Success for “enterprise feel”

After ship (later Issue), a 10-line Ising demo can omit deep `com.…` paths and
read as chalk-first.
