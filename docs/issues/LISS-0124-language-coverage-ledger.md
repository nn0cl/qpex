# LISS-0124: Language coverage ledger (rebaseline Gate P1)

## Metadata

- Local issue ID: LISS-0124
- GitHub issue: none
- Status: **authorized** — P1 start authorized 2026-07-31; not yet started
- Phase: not started (Architecture / docs Path)
- Type: documentation / coverage ledger
- Priority: P1 (rebaseline Gate P1)
- Initial planning size: M
- Depends on:
  - [rebaseline](../specs/staqex-v1-representative-program-rebaseline.md)
    (**Accepted**; §6 P1 authorized)
  - [LISS-0119](LISS-0119-examples-health-inventory.md) **Issue ID exists**
    (may proceed in parallel with 0119 execution; heal Issues 0122/0123 are
    not blockers)
- Blocks: P2 mission lock; showcase S0
- Related: [friction ledger](../architecture/physicist-source-friction-ledger.md)
  F-01…F-10, agent-contract Open Topics, [vision](../architecture/adjudicator-language-vision.md)
- Implementation permission: **yes** — docs ledger only
- Branch (when started): `docs/liss-0124-language-coverage-ledger`
- Deliverable path (proposed): `docs/specs/staqex-v1-language-coverage-ledger.md`

## Summary

Lock an honest v1 surface boundary for any future showcase: what is shipped,
partial, or explicitly out — seeded from the physicist-source-friction ledger
and shipped Kernel surfaces. Docs-only; no showcase Red/Green.

## Acceptance (EARS)

1. **Given** friction rows F-01…F-10 and shipped surfaces, **when** the ledger
   is published, **then** each row has Status / Where proven today / In
   showcase? / Follow-up (Issue or ADR).
2. **Given** Open Topics from agent contracts, **when** the ledger is
   published, **then** each is either scheduled for implementation before
   showcase or **explicitly out** with physicist-readable rationale.
3. **Given** programmer concerns (ports, diagnostics, visibility, LINEAR),
   **when** the ledger is published, **then** they appear as rows — not only
   grammar tokens.
4. **Given** F-02/F-05, **when** recorded, **then** Status reflects
   **closed** via ADR 0114 + LISS-0121 (named Float / OpAttr), with residual
   sample debt pointed at P0 Issues.

## Non-goals

- Implementing Open Topics.
- Showcase construction or P2 mission finalization.
- Healing examples (P0 Issues).

## Exit

- [ ] Coverage ledger file under `docs/specs/` (or ADR companion if Adjudicator
      redirects)
- [ ] Open Topics all in-or-out
- [ ] Friction F-01…F-10 folded
- [ ] open-work-register + rebaseline pointers updated
- [ ] Trace filed

## Next allowed operation

P1 authorized. Open `docs/liss-0124-language-coverage-ledger` and draft the
ledger when scheduled (may parallel LISS-0119).
