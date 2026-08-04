# WP-0091: Decision theme canonicalization

## Status

**Completed — Architecture approved** (2026-08-04)

## [DESIGN CHECK]

- Scope and expected behavior: Replace the current “one large ADR/Issue/WP
  record per decision slice” reading surface with a small set of `DEC-*`
  theme documents. Each theme document is the current source for the theme;
  historical records remain recoverable through the immutable baseline tag and
  full source commit.
- Specifications and files inspected: `AGENTS.md`, ADR 0187,
  `documentation-canonicalization-policy.md`,
  `documentation-compression-map.md`, `current-decision-register.md`,
  `open-work-register.md`, `architecture/README.md`, and the 186 ADR titles.
- Component boundaries, ports/adapters, and VO/DTO candidates when applicable:
  documentation-only change; no runtime components, ports, adapters, or
  application data models. Proposed documentation value objects are
  `DecisionThemeId` (`DEC-0001` form), `SourceRecordRef` (tag + full commit +
  path), and `DecisionStatus` (`accepted`, `proposed`, `deferred`,
  `superseded`).
- Applicable constraints: No language or runtime semantics may change. Existing
  ADR identifiers remain immutable source identifiers. Normative language
  remains physicist-first and is not replaced by a shorter programmer-oriented
  summary. Unresolved records remain actionable.
- Decisions, assumptions, and unresolved ambiguities:
  - Proposed namespace: `DEC-####` for current theme documents; historical ADR
    numbers remain source identifiers.
  - Proposed source pointer: `source_tag`, `source_commit`, and `source_path`,
    with `git show <source_tag>:<source_path>` as the deterministic recovery
    command. The full commit is authoritative; the tag is the human-readable
    anchor.
  - Theme boundaries, canonical titles, and archival of settled ADR bodies were
    approved through ADR 0188.
- Included and omitted AI context: Included only the documentation policies,
  decision-register surfaces, open-work register, and ADR title inventory.
  Omitted compiler/runtime source, tests, private data, provider material, and
  full historical ADR bodies until a theme is selected for review.
- Task routing (model/assistant/tool): strong-reasoning architecture review for
  theme boundaries and policy compatibility; deterministic scripts for file
  inventory, source-reference validation, link checking, and deletion safety.
- Input/output evidence contract when AI output is involved: inputs are the
  named repository documents and title inventory; output is a reviewable theme
  matrix plus source pointers; every deleted record must have a tag, full
  commit, original path, destination, and recoverability check. No hidden
  reasoning or unverified summary becomes normative.
- Verification plan: validate one-to-one coverage of retained source records,
  no unresolved Issue deletion, no broken links, no direct references to
  deleted paths, successful spec/execution-batch checks, and `git cat-file -e`
  for every baseline source path.

## Current-tree layout

```text
docs/architecture/decision-themes/
  dec-0001-governance-and-collaboration.md
  dec-0002-state-first-semantics-and-measurement.md
  dec-0003-language-surface-and-physicist-first-dx.md
  ...
docs/architecture/decision-theme-register.md
```

The register maps each `DEC-*` theme to its current meaning, status, source
ADR/Issue/WP/Trace identifiers, and the immutable recovery coordinates. Theme
documents contain the accepted rule, rationale, consequences, open boundaries,
and links to normative specifications; they do not copy every execution log.

## Acceptance criteria for the next phase

1. Every current ADR is assigned to exactly one theme or explicitly marked
   `independent` / `unresolved`.
2. Every theme has one canonical `DEC-*` document and one register row.
3. No old ADR is deleted while it carries unique accepted or unresolved
   meaning not represented in the theme document or normative specification.
4. Every compressed source record has a full commit, baseline tag, original
   path, destination, classification, and passing recovery check.
5. Existing links are migrated to `DEC-*` or the theme register before any
   source record is removed.
6. The implementation PR must report the before/after inventory and retain
   all existing deterministic verification gates.

## Completion record

ADR 0188 accepted the seven-theme current surface and archival rule. ADRs
0001–0186 (185 files; ADR 0099 was never assigned) were deleted from the
working tree after link migration. Their bodies are recoverable from the
baseline tag and the compression map.
