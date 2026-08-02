# LISS-0234: Dirac paper spelling sugar — Red (ship ADR 0169)

## Metadata

- Local issue ID: LISS-0234
- Status: **in_progress** (WP-0081 batch approved)
- Phase: phase-1-red
- Type: feature
- Priority: P2
- Planning size: M
- Program: [WP-0081](../work-plans/WP-0081-0165-0166-red-intake.md)
- Design ADR: [0165](../architecture/adr/0165-dirac-paper-spelling-sugar.md) (**Accepted**)
- Ship ADR: [0169](../architecture/adr/0169-ship-dirac-paper-spelling-sugar.md) (**Accepted**)
- Depends on: WP-0081 execution batch

## Intent

Implement ADR 0165 / 0169: dual-accept paper inner `⟨φ|ψ⟩` and outer `|ψ⟩⟨φ|`
as sugar desugaring to `inner` / `outer` Calls; named `|psi>` remains rejected;
Call form stays the teaching default.

## Exit

- [ ] Phase 1–3 complete under approved batch
- [ ] Disambiguation suite (ket / comparison / `|>` / anticommutator / bare-block)
- [ ] Formatter + migrate round-trip
- [ ] No evaluator semantic change beyond Call desugar
- [ ] Full `pytest tests/` green

## Non-goals

Named `|psi>`; MeasureSink/SourcePort; changing ADR 0087 Call semantics.
