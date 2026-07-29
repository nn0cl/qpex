# Trace: LISS-0113 QPex → Staqex project rename

- Date: 2026-07-29
- Task: Rename project from QPex to Staqex; rename source extension `.qpex` → `.sqx`
- Agent: Cursor (Auto) + Claude (Auto)
- Phase: Architecture Path / LISS-0113 rename — **complete**
- Branch: `feature/liss-0113-palquantum-rename`

## Background

The name `QPex` conflicted with at least one existing product in the market.
Rename was timed after LISS-0080 (phase-resolved typed HIR) — the last major
structural issue before linear analysis — to minimise the churn surface.

Name selected: **Staqex** — concept coinage **St**ate + **Q**uantum +
**Ex**ecution. Zero conflicts confirmed across PyPI, crates.io, npm,
USPTO/EU/JP trademarks, GitHub orgs, YouTube channels, SNS handles, and
company registrations. Domains `staqex.org` and `staqex.com` acquired by
Adjudicator.

Language semantics, ADR content, and test logic are unchanged.

## Slices executed

| Slice | Scope | Commits |
|---|---|---|
| **A** | `compiler/qpex/` → `compiler/staqex/`; Python imports; CLI entry; QUICKSTART | `daf894f` |
| **B** | `.qpex` → `.sqx` in all `examples/`; parser/loader/cli file-extension refs | `566395f` |
| **C** | `docs/` text QPex→Staqex, .qpex→.sqx; agent instruction files | `566395f` |
| **fix-1** | Restore QPex as historical subject in LISS-0113 issue doc (over-replaced by C) | `389c6e0` |
| **fix-2** | Record rename history in `architecture/README.md` and work register | `4780870` |
| **fix-3** | Complete file renames (`qpex-*.md` → `staqex-*.md`), path refs, katakana, compiler strings | `1a2e17c` |
| **fix-4** | Restore QPex spelling in 12 pre-rename execution traces (immutable records) | `8bef5e3` |

## Scope of change

| Category | From | To | Count |
|---|---|---|---|
| Python package directory | `compiler/qpex/` | `compiler/staqex/` | — |
| Python import paths | `compiler.qpex` | `compiler.staqex` | ~136 |
| CLI entry point | `python3 -m compiler.qpex` | `python3 -m compiler.staqex` | docs / QUICKSTART |
| Source file extension | `.qpex` | `.sqx` | 43 files |
| Compiler class | `QPexCompiler` | `StaqexCompiler` | — |
| docs/architecture/ files | `qpex-*.md` | `staqex-*.md` | 17 files |
| docs/specs/ files | `qpex-*.md` | `staqex-*.md` | 48 files |
| docs/specs/grammar/ | `qpex.ebnf` | `staqex.ebnf` | 1 file |
| docs/testing/ | `qpex-*.md` | `staqex-*.md` | 1 file |
| tests/fixtures/ | `fixtures/qpex/` | `fixtures/staqex/` | dir |
| Config file | `qpex.toml` | `staqex.toml` | 1 file |
| Project name string | `QPex` | `Staqex` | ~340 doc files |
| Katakana reading | `キューペックス` | `スタケックス` | several files |
| GitHub repo | `nn0cl/qpex` | `nn0cl/staqex` | Adjudicator action |

## Intentionally preserved as QPex / .qpex

| Location | Reason |
|---|---|
| `docs/issues/LISS-0113-palquantum-rename.md` — "Why rename", From-columns | Historical record of the rename itself |
| `docs/architecture/README.md` — "QPex → Staqex" section | Same |
| `docs/collaboration/traces/2026-07-2*` files (pre-rename) | Immutable execution records; project was QPex when written |
| `compiler/staqex/parser.py` — `qpex_version` token | Language-specification keyword |
| `compiler/staqex/modules.py` — `path[0] == "qpex"` | Standard-library namespace root (language spec) |
| `compiler/staqex/stdlib/math_ops.py`, `io_ops.py` — `qpex.math`, `qpex.io` | Standard-library package names (language spec) |
| `tests/spec_verification/reports/latest.md` — `qpex check`, `qpex run` | Immutable SV execution report |

## Explicitly not changed

- Language semantics, axioms, ADR decisions
- Test assertions and test logic
- `qpex_version` / `qpex.math` / `qpex.io` language-spec keywords
- Pre-rename execution traces under `docs/collaboration/traces/`

## Verification

- `python3 -m compiler.staqex run examples/basics/B01_never_leave_the_state/never_leave_the_state.sqx --seed 0` produces correct output (confirmed in `566395f` commit message)
- All `.sqx` example files pass the compiler
- No `compiler/qpex/` import paths remain outside historical records

## Next safe action

LISS-0080 remaining open work (see `docs/issues/LISS-0080-phase-resolved-typed-hir.md`),
or proceed to the next issue in `docs/architecture/open-work-register.md`.
