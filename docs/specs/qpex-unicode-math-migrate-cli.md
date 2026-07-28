# QPex Unicode math migrate CLI (LISS-0069 Slice C)

| Field | Value |
|---|---|
| Status | **Phase 1 Red** (2026-07-28); plan approved; awaiting Red review → Green |
| Authority | ADR 0106; [`qpex-unicode-math-migrator.md`](qpex-unicode-math-migrator.md) (Slice B library) |
| Depends on | LISS-0069 Slice B **complete** (`migrate_unicode_math_source`) |
| Last updated | 2026-07-28 |

This companion freezes the **Slice C** CLI contract. It does not authorize
Phase 1 Red until plan approval.

## 1. Goals

1. Expose Slice B’s pure migrator as a **`qpex migrate`** subcommand.
2. Support file in-place rewrite and stdout preview without changing rewrite
   rules.
3. Keep Host/ports thin: CLI reads/writes files; all spelling policy stays in
   `migrate_unicode_math_source`.
4. Defer formatter-owned emit / CST pretty-print to **LISS-0072** (not Slice C).

## 2. CLI surface (Normative for Slice C)

```text
python3 -m compiler.qpex migrate <path.qpex> [options]
```

| Flag / arg | Meaning |
|---|---|
| `path` | Required `.qpex` (or UTF-8 text) source file |
| `--write` / `-w` | Rewrite the file in place with migrated text |
| (default, no `-w`) | Print migrated source to **stdout**; leave file unchanged |
| `--check` | Exit `0` if file already equals migrated form; else exit `1` and print nothing to stdout (diagnostics on stderr) |
| `-o PATH` | Write migrated text to `PATH` (mutually exclusive with `-w`) |

### Exit codes

| Code | When |
|---|---|
| `0` | Success (`--check` means already canonical, or migrate printed/wrote) |
| `1` | `--check` found drift, or I/O / usage error |
| `2` | Reserved (unused in Slice C) |

### Explicit non-goals

- Recursive directory walk / glob batch (may land later; Slice C is **one file**).
- Network / stdin-as-default (optional `-e` string may be deferred; prefer file).
- Changing `migrate_unicode_math_source` rewrite rules.
- Formatter / CST emit (LISS-0072).
- Bulk rewrite of `examples/` in the same Green.
- Pauli / `state` migrations (M-P01 / M-P05).

## 3. Adapter boundary

```text
cli.py  cmd_migrate
  -> read path (UTF-8)
  -> migrate_unicode_math_source(text)   # UseCase/library (Slice B)
  -> write stdout / file / compare for --check
```

No business spelling decisions in `cli.py`. File encoding errors surface as
clear stderr messages and non-zero exit.

## 4. Acceptance envelopes (Slice C)

### EARS

When `qpex migrate path` runs without `--write`, the system shall print the
migrated source to stdout and shall not modify `path`.

When `qpex migrate path --write` runs, the system shall replace `path` contents
with the migrated source (UTF-8).

When `qpex migrate path --check` runs and the file already matches the migrated
form, the system shall exit 0.

When `qpex migrate path --check` runs and migration would change the file, the
system shall exit 1.

### Gherkin

```gherkin
Feature: qpex migrate CLI

  Scenario: Preview to stdout
    Given fixture tests/fixtures/migration/v0.1/ket_basic.qpex
    When "python3 -m compiler.qpex migrate <that path>" runs
    Then stdout equals tests/fixtures/migration/v1/ket_basic.qpex
    And the input file is unchanged

  Scenario: In-place write
    Given a temp copy of ket_basic.qpex (v0.1)
    When migrate runs with "--write"
    Then the temp file equals the v1 golden

  Scenario: Check detects drift
    Given the v0.1 ket_basic fixture
    When migrate runs with "--check"
    Then the process exits with code 1
```

## 5. Verification plan

- Phase 1 Red: CLI tests invoking `compiler.qpex.cli.main([...])` (or subprocess)
  against migration fixtures; expect missing `migrate` subcommand / failures.
- Phase 2 Green: register subparser + `cmd_migrate`; wire library only.
- After Green: migrator unit tests + SV 160/160 still PASS.
- Phase 3 Refactor: readability only.

## 6. Name lock

Command name is **`migrate`** (not `migrate-unicode` / `fmt`). Help text must
state that only Unicode math dual-accept rewrites (M-P02–M-P04) are applied.
