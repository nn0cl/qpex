# LISS-0233: Residual suite green floor (post WP-0069 clusters)

## Metadata

- Local issue ID: LISS-0233
- Status: **complete** — 2026-08-02 (WP-0079)
- Phase: docs-only + suite repair (+ one-line parser LET fix)
- Type: bug
- Priority: P0
- Planning size: L
- Program: [WP-0079](../work-plans/WP-0079-green-floor-for-ci.md)
- Blocks: [LISS-0209](LISS-0209-ci-runs-test-suite.md)

## Intent

After WP-0073–0078, `pytest tests/` still reported **65 failures**, mostly
`LINEAR_IMPLICIT_DISCARD` suite drift after HARD_CODES unification. Green the
floor so blocking CI (LISS-0209) can land against a green tree.

## Exit

- [x] `pytest tests/` reports **0 failed** (1062 passed, 2026-08-02)
- [x] Kernel change limited to ADR 0153 bare-block guard: peek `TokenKind.LET`
  (WP-0075 had checked `IDENT` + `"let"`, which never matched)
- [x] LISS-0209 unblocked for a follow-on WP

## Non-goals

Enabling CI in this Issue; spec-verification report commits; xfail silence.

## Deferred Kernel (recorded, suite-softened)

- ~~Pipe into a **remaining multi-hole** Partial does not move the lhs~~
  → **closed** [LISS-0238](LISS-0238-multi-hole-partial-pipe-lhs-move.md) / WP-0085.
- ~~`apply(I)` on `State<Qutrit>` compiles but SV runtime still rejects~~
  → **closed** [LISS-0239](LISS-0239-qutrit-apply-identity-sv-noop.md) / WP-0085.
