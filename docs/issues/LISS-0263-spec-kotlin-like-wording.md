# LISS-0263: Spec wording — Kotlin-like DX is secondary (not co-equal)

## Metadata

- Local issue ID: LISS-0263
- GitHub issue: https://github.com/nn0cl/staqex/issues/272
- Status: **complete** (2026-08-02)
- Type: Fast Path / docs
- Priority: P1
- Program: [WP-0088](../work-plans/WP-0088-surface-modernization.md)
- Paths: `docs/specs/staqex-language-specification.md` §1.1; optionally QUICKSTART / vision cross-links

## Problem

Spec §1.1 lists “Kotlin-like DX” as a top-level non-negotiable constraint alongside
NLTS and blackboard surface. Readers infer **co-equal** status, which feeds the
enterprise-Kotlin look and conflicts with vision (physicist primary).

## Goal

Reword so:

1. NLTS + blackboard remain primary non-negotiables
2. DX (modules, `fn`, visibility) is **secondary, non-optional**, with physics reading
3. Explicit: DX must not import enterprise ceremony that blunts chalk
4. No effective change to Kernel conformance tests (wording only)

## Exit

- [x] §1.1: primary NLTS + blackboard; secondary modules/structure DX
- [x] Cross-link surface modernization north star; Kotlin-like demoted to historical note
- [x] No `.sqx` / Kernel behavior change (wording only)

## Non-goals

- Removing `package`/`fn` from the language
- ADR for new syntax
