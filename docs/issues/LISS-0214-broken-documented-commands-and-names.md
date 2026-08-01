# LISS-0214: Documented commands that fail and names that do not exist

## Metadata

- Local issue ID: LISS-0214
- Status: **complete** — 2026-08-01 (WP-0077)
- Phase: docs-only
- Type: bug
- Priority: P2
- Planning size: S
- Program: [WP-0069](../work-plans/WP-0069-operations-review-intake.md)

## Intent

Several copy-pasteable commands and identifiers in the READMEs and the examples
catalog do not work. A reader following them hits an error on the first step.

## Evidence (verified 2026-08-01)

**1. `compiler/README.md:19` names a symbol that does not exist.**

```
python3 -c "from compiler.staqex import QPexCompiler; print(QPexCompiler()…)"
```

The exported class is `StaqexCompiler` (`compiler/staqex/__init__.py:3,73`).
`QPexCompiler` is a leftover from the pre-rename era; the command raises
`ImportError`.

**2. Showcase README run command is missing the subcommand.**

`examples/showcase/quantum_matter_discovery/README.md:10`

```
python3 -m compiler.staqex examples/showcase/quantum_matter_discovery/main_quantum_matter_discovery.sqx
```

The CLI requires a verb (`run`, `check`, `inspect`, `dag`, `emit-qasm`, `repl`,
`migrate`, `fmt`). Every other README uses `… run <file> --seed 0`. Verified:
the program itself runs fine with `run`, so only the documented line is wrong.

**3. `examples/README.md` catalog table is stale.**

- Says `B01–B12`; `examples/basics/` contains **B01–B15**, and
  `basics/README.md` itself says "Complete: B01–B15 (catalog v2)".
- Has no `showcase/` row at all, although `examples/showcase/` exists and is
  the S1 deliverable.

**4. [`staqex-examples-catalog-v2.md`](../specs/staqex-examples-catalog-v2.md)
is stale in four ways** — and it is cited as "Authority" by both track READMEs:

- §5 header reads `Applied track (A01–A10)` and the table stops at A10;
  `A11_noether_forge` exists on disk and in `applied/README.md`.
- §2 still uses the pre-rename extension: "`main_<topic>.staqex`" /
  "`<topic>.staqex`". The extension is `.sqx`.
- Line 168 says `B01–B12` while its own §4 header says `B01–B15`.
- §11 acceptance checklist is entirely unchecked although LISS-0106/0107/0108/0109
  are all `done`.
- §5 A01 row still reads "primary attention paper TBD" while §3 policy requires
  **verified** bibliographies only.

**Not a defect:** all 26 example programs execute successfully
(`OK=26 / FAIL=0`, full CLI sweep 2026-08-01). Only the documentation is wrong.

## Adjudicator decision points

1. §11 checklist: tick it (the work is done), or is one item genuinely
   outstanding — specifically "All Applied README bibliographies use Verified
   entries only", which the A01 `TBD` contradicts?
2. A01's missing primary attention paper: supply the citation, or drop the row
   to match the verified-only policy?

## Exit

- [x] `compiler/README.md` command runs as written
- [x] Showcase README command runs as written
- [x] `examples/README.md` reflects B01–B15 and the showcase track
- [x] Catalog spec covers A11, uses `.sqx`, is internally consistent on B-range
- [x] §11 checklist resolved; A01 bibliography resolved

## Non-goals

Adding or removing example programs; restructuring the catalog; the stale
`docs/issues/inbox/` notes ([LISS-0216](LISS-0216-issue-planning-doc-drift.md)).

## Resolution (WP-0077)

Fixed `StaqexCompiler` in `compiler/README.md`, showcase `run` verb, and
examples catalog A11 / `.sqx` / B01–B15 wording. `examples/README.md` was
already current.
