# LISS-0070: Rust compiler infrastructure (deferred — next version)

## Metadata

- Local issue ID: LISS-0070
- Status: **deferred** (next version — no implementation on the current
  Shipping Kernel track)
- Phase: phase-0-design
- Type: architecture
- Priority: deferred / L
- Planning size: L
- Program: [WP-0025](../work-plans/WP-0025-staqex-v1-north-star.md)
- Depends on: [LISS-0068](LISS-0068-staqex-v1-normative-rebaseline.md) (when
  that dependency still applies to the resumed track)
- Restored: 2026-08-01 via [LISS-0212](LISS-0212-dangling-liss-0070-reference.md)
  / [WP-0077](../work-plans/WP-0077-docs-hygiene-0212-0216.md)

## Intent

Later-generation **Rust VM / compiler infrastructure** behind the **same**
Staqex language semantics. The current Shipping Kernel remains Python
(`compiler/staqex/`). This Issue is the actionable deferred tracker for
conformance Slice D (Rust differential) and related Rust-mirror notes.

## Decision (when resumed)

Choose among:

- custom Rust IR only;
- custom high-level IR plus selective MLIR;
- broader MLIR dialect adoption.

Recommended default (WP-0025): custom Rust HIR/Physics/Quantum IR, optional
MLIR below Algorithm Plan IR.

## Required evidence (when resumed)

- minimal Physics IR and provenance POC;
- build/distribution complexity;
- dependency and vulnerability review;
- diagnostic/source-span quality;
- QIR/LLVM interoperability;
- contributor cognitive cost.

## Non-goals (current track)

Starting Rust work; changing the deferral; gating Python Kernel language-spec
work on this Issue.
