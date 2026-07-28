# QPex lossless CST and formatter plan (LISS-0072)

| Field | Value |
|---|---|
| Status | **Slice A–D complete** (2026-07-28); Issue closed |
| Authority | WP-0025 E1; ADR 0106 D9/D12 + Unicode scope; [`qpex-v1-compiler-blueprint.md`](../architecture/qpex-v1-compiler-blueprint.md) §3.1; [`qpex-v1-normative-rebaseline-register.md`](qpex-v1-normative-rebaseline-register.md) §7 |
| Depends on | LISS-0069 **complete**; LISS-0071 **complete**; LISS-0070 **not required** |
| Last updated | 2026-07-28 |

This companion freezes the **LISS-0072** design intake. Adjudicator plan
approval selected the recommended direction and authorized **Slice A Phase 1
Red**.

## 1. Goals

1. **Lossless frontend capture** — comments, whitespace, and token spans survive
   parsing so formatting and fix-its do not depend on re-lexing heuristics.
2. **Canonical emit** — formatter prints one Unicode spelling for M-P02–M-P04
   (ket close `⟩`, `⊗`, postfix `†`) per ADR 0106 / LISS-0069.
3. **Verifiable round-trip** — `parse → format → parse` preserves structural AST
   and comment text on a reviewed corpus.
4. **Source versioning** — optional `qpex_version` metadata declares the dialect
   window; implicit default documented until authors opt in.
5. **EBNF truth** — [`grammar/qpex.ebnf`](grammar/qpex.ebnf) catches up to the
   shipping Python lexer/parser for known gaps named in
   [`qpex-language-specification.md`](qpex-language-specification.md) Appendix A.
6. **No semantic fork** — CST/formatter changes are presentation-layer only; SV
   remains the behavior oracle (LISS-0071).

## 2. Current baseline (evidence)

| Area | Today | Gap |
|---|---|---|
| Lexer trivia | `_skip_trivia()` discards `//` comments and whitespace | No lossless capture |
| Parser | Token stream → AST directly | No CST module |
| Migrator | `migrate_unicode_math.py` text rewrite (Slice B LISS-0069) | Not CST-backed; no full pretty-print |
| CLI | `qpex migrate` (Slice C LISS-0069) | No `qpex format` |
| EBNF | Draft dated 2026-07-23 | Missing `until`, separators, scientific scopes, Unicode tokens, many shipped keywords |
| Version markers | Rebaseline register §7 draft only | No parser/validator |

Golden inputs already exist:

```text
tests/fixtures/migration/v0.1/   # ASCII / dual-accept inputs
tests/fixtures/migration/v1/     # expected Unicode-canonical outputs
```

## 3. Architecture boundary

```text
bytes (UTF-8)
  → trivia-aware token stream (+ spans)
  → lossless CST (or equivalent trivia attachment)
  → desugared AST          # unchanged semantic contract
  → … existing pipeline …
```

**Formatter path (Slice B):**

```text
AST + CST/trivia
  → canonical emit rules
  → UTF-8 text
```

Rules:

- Formatter **must not** change semantics; only spelling, spacing policy, and
  comment placement within documented tolerance.
- Migrator library remains available; formatter output **should match**
  `migrate_unicode_math_source` on M-P02–M-P04 fixtures (parity test).
- Retired-keyword **fix-its** (Slice C) are diagnostic attachments only — no
  silent rewrite during compile unless a dedicated `format`/`migrate` command runs.

### Approved CST strategy

**Phase 1:** trivia-attached `Token` stream + `GreenNode`-style CST wrapper
rather than a full hand-rolled AST mirror.

- Leading/trailing trivia stored per token (whitespace runs, `//` comments).
- Parser consumes trivia-aware tokens; AST nodes retain `Span` as today.
- Formatter walks token/CST layer for whitespace/comments, AST for structure.

A fuller CST mirroring every grammar production may follow in a later refactor
if Slice B proves insufficient; Slice A Red tests should fail if trivia is lost.

## 4. Suite taxonomy (verification)

| Class | Meaning | Primary oracle |
|---|---|---|
| **cst** | Trivia and spans survive lex + parse boundary | Red helpers on token/CST fixtures |
| **format-roundtrip** | parse-format-parse AST equality + comments | golden corpus + AST diff |
| **migration-parity** | formatter ≡ migrator on M-P02–M-P04 | `tests/fixtures/migration/` |
| **version** | `qpex_version` accepted/rejected | named diagnostic codes |
| **grammar-sync** | EBNF productions ⊆ lexer/parser | alignment script or Red doc test |
| **regression** | No SV behavior change | `tests/spec_verification/run_all.py` |

Numerical and runtime envelopes remain LISS-0071 catalog rows; this Issue adds
**presentation-layer** scenarios only.

## 5. Planned slices

| Slice | Deliverable | Red focus (indicative) |
|---|---|---|
| **A** | Trivia-aware lexer + CST skeleton module | comments/whitespace round-trip at lex boundary; spans stable |
| **B** | Formatter + canonical Unicode emit + corpus tests | AST equality; migration parity; optional `qpex format` CLI |
| **C** | `qpex_version` metadata + retired-keyword fix-it hints | version parse/default; `RETIRED_*` fix-it text present |
| **D** | EBNF catch-up + alignment gate | EBNF lists `until`, separators, scientific scopes, Unicode tokens |

### Slice A detail

- New module boundary (proposed): `compiler/qpex/cst.py` (or `cst/` package if
  split warranted in Green).
- Extend `Token` / lexer to optionally **retain** trivia instead of skipping.
- Parser entry accepts trivia-aware stream without changing AST shapes.
- **Non-goals in A:** pretty-print rules, EBNF edits, version markers.

### Slice B detail

- Formatter module (proposed): `compiler/qpex/format.py`.
- Emit rules (initial):
  - Unicode ket close, `⊗`, postfix `†` (LISS-0069).
  - Preserve `//` comments and logical blank lines per golden fixtures.
  - Spacing: minimal stable policy (single space where required by grammar; no
    aggressive re-wrap).
- Initial oracle corpus:
  - `tests/fixtures/migration/v0.1/` inputs;
  - `tests/fixtures/migration/v1/` expected canonical outputs;
  - selected parser-valid snippets only if migration fixtures leave a spacing
    ambiguity untested.
- Round-trip helper: `parse(format(parse(src)))` AST structurally equal to
  `parse(src)`.
- Parity: `format(src) == migrate_unicode_math_source(src)` for migration corpus
  where migrator scope applies.
- Approved: include a minimal `qpex format` CLI (`--write`, `--check`, `-o`
  mirroring migrate) in Slice B.
- Explicit non-goals in Slice B:
  - byte-identical source reproduction;
  - parser rewrite beyond what formatting entry needs;
  - `qpex_version` and EBNF sync work (Slices C/D).

### Slice C detail

- Package metadata surface (draft — Adjudicator may refine syntax in Red):

  ```qpex
  package example

  qpex_version = "1.0"
  ```

- Validator: unknown/unsupported version → named diagnostic (catalog sync on
  Green).
- Fix-its: when `RETIRED_KEYWORD` / `FORBIDDEN_KEYWORD` fires, attach suggested
  replacement text (e.g. `fun` → `fn`) without auto-editing source on compile.
- Initial Red scope:
  - accept the draft `qpex_version = "1.0"` package metadata form;
  - reject unsupported versions with a named diagnostic before semantic
    analysis;
  - preserve existing `replacement` payloads for `RETIRED_KEYWORD`;
  - do not invent new `FORBIDDEN_KEYWORD` replacements unless uniquely
    specified.
- Explicit non-goals in Slice C:
  - actual multi-version semantic switching;
  - formatter or migrator auto-rewrite during compile;
  - EBNF sync and source-layout changes.

### Slice D detail

EBNF must add at minimum (from spec Appendix A + rebaseline register):

| Production gap | Shipping evidence |
|---|---|
| `evolve … until … max N` | `tokens.UNTIL`, `parser.py`, LISS-0012 |
| Numeric literal `_` separators | `lexer.py`, ADR 0101 |
| Scientific scopes (`theory`, `experiment`, …) | `scientific_scopes.py`, LISS-0034 |
| Unicode ket/tensor/dagger tokens | LISS-0069 lexer |
| Modern keywords (`namespace`, `enum`, `struct`, `dynamic`, …) | `tokens.py` |

Alignment gate: a deterministic check (script or Red test) fails when EBNF and
lexer keyword sets diverge.

Initial Red scope:

- assert the grammar file documents the shipped `until` / `max` surface;
- assert numeric separator forms from ADR 0101 appear in lexical productions;
- assert scientific-scope heads and modern keywords are listed;
- assert Unicode math token alternates are present;
- assert an alignment helper can compare EBNF inventory against shipping token
  maps without consulting runtime behavior.

Explicit non-goals in Slice D:

- changing runtime/parser semantics;
- source versioning or formatter policy changes;
- proving full grammar completeness beyond the named catch-up inventory.

## 6. Acceptance envelopes (planning)

### EARS — lossless capture (Slice A)

When a source file contains `//` comments and insignificant whitespace between
tokens, the system shall retain that trivia in the CST (or trivia attachment)
such that a formatter can restore comment text without re-reading the original
file.

### Gherkin — format round-trip (Slice B)

```gherkin
Given a valid program in the migration golden corpus
When the program is parsed to AST, formatted, and parsed again
Then the second AST is structurally equal to the first
And every // comment text from the source appears in the formatted output
```

### Gherkin — migration parity (Slice B)

```gherkin
Given a v0.1 migration fixture covered by M-P02–M-P04
When the formatter emits canonical source
Then the output equals migrate_unicode_math_source(fixture)
```

### EARS — version marker (Slice C)

When package metadata declares `qpex_version = "1.0"` and the compiler supports
that dialect, the system shall accept the program under the documented default
rules.

When package metadata declares an unsupported `qpex_version`, the system shall
reject compilation with a named diagnostic before semantic analysis.

### EARS — EBNF sync (Slice D)

When `grammar/qpex.ebnf` is updated for a shipped production, the system shall
document that production as normative and the alignment gate shall pass for the
keyword and operator inventory.

## 7. Explicit non-goals

- Rust formatter / CST.
- NFC normalize-on-emit (defer; LISS-0069 NFC still open).
- Pauli removal, `state` sugar, bra desugar (separate Issues).
- Numeric separator **insertion** by formatter.
- LSP, notebook, editor plugins (LISS-0105).
- Changing SV assertions or acceptance envelopes E-01–E-14 semantics.

## 8. Risks and mitigations

| Risk | Mitigation |
|---|---|
| CST scope creep duplicates AST | trivia-attached tokens first; AST shapes frozen |
| Formatter changes break SV | AST round-trip + full SV after each Refactor |
| Migrator / formatter diverge | explicit parity tests on migration corpus |
| EBNF drift recurs | Slice D alignment gate in CI |
| Two spelling authorities | formatter defers to LISS-0069 canonical table |

## 9. Adjudicator checklist (plan approval)

- [x] Slices A–D order and boundaries accepted.
- [x] CST strategy: trivia-attached tokens first.
- [x] Round-trip oracle: structural AST + comments.
- [x] NFC at format boundary: preserve source.
- [x] `qpex format` CLI: include minimal CLI in Slice B.
- [x] `qpex_version` syntax draft acceptable for Red.
- [x] Approve **Slice A Phase 1 Red** (no Green implied).

## 10. Verification plan

| Step | Command / artifact |
|---|---|
| Plan PR | docs only; markdown links resolve |
| Slice A Red | `pytest tests/test_cst_slice_a_red.py -q` (to be created) |
| Slice B Red | `pytest tests/test_formatter_slice_b_red.py -q` (to be created) |
| Migration parity | fixtures under `tests/fixtures/migration/` |
| SV regression | `python3 -m tests.spec_verification.run_all` after each Refactor |
| EBNF gate | alignment test/script in Slice D Red |
