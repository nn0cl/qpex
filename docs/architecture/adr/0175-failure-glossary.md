# ADR 0175: Failure glossary (world-line vs Job vs capability)

## Status

**Accepted** (2026-08-02) — Adjudicator「承認」
([LISS-0258](../../issues/LISS-0258-failure-glossary-adr.md) / [WP-0087](../../work-plans/WP-0087-s01-expressiveness-brushup.md)).
Architecture approval of the glossary only. No Kernel behavior change is
authorized by this ADR alone.

Companions:

- [staqex-language-axioms.md](../staqex-language-axioms.md) (Axiom 6 — no exceptions)
- [ADR 0025](0025-failure-worldlines.md) (if present) / B03 failure_worldline
- Host `JobResult` / `MeasurementEnvelope` (`compiler/staqex/host.py`)
- [QPU capability honesty](../../specs/staqex-v1-qpu-capability-honesty.md)
- Destructive simplification residual: failure vocabulary

## Context

Staqex rejects `throw` / `try` / `catch` in the object language. Failure can
still appear as:

1. **World-line / joint labels** inside `when` (e.g. Err arm for 0-division)
2. **Compile / Kernel diagnostics** on programs that do not typecheck or violate LINEAR
3. **Host Job outcomes** (`JobResult.status`, incomplete vacuum tickets)
4. **Capability / placeability rejects** (soft or hard QPU codes)

Learners and samples conflate these. S01 and basics need a shared glossary so
examples do not teach “Job failed ⇒ encode as when-arm” or the reverse without
honesty notes.

## Decision

### Glossary

| Kind | Lives in | Typical codes / shapes | Not for |
|---|---|---|---|
| **World-line failure** | Object language Joint / `when` arms | `Success`/`Error` basis labels; physics-orthogonal outcomes | Host queue, network, missing credentials |
| **Kernel diagnostic** | CompileResult / run diagnostics | Type errors, `FORBIDDEN_KEYWORD`, LINEAR violations | Encoding as runtime when-arms mid-program |
| **Job / Host failure** | `JobResult.status`, Host exceptions | `failed`, incomplete vacuum measure, Abort budget | Silent classical `if` recovery inside Static Kernel |
| **Capability reject** | Diagnostics / soft IR notes | `E_QPU_UNSUPPORTED_CAPABILITY`, placeability flags | Pretending SIM success is QPU success |

### Rules for samples and Host

1. **World-line labels** remain physics-facing narrative (Axiom 6).
2. **Job failures** are Host-visible; S01 tickets must **fail closed** on vacuum
   (LISS-0243) — do not invent `sample_value`.
3. **Capability rejects** must stay visible on tickets/diagnostics when present;
   do not strip soft QPU notes to fake a clean QPU story.
4. Do not map Host/credential failures into Staqex `when` arms unless the
   **scenario** explicitly models that failure as a physical/ops world-line
   (and even then, document the mapping).

### Non-decision

- Exact enum names for Success/Error beyond existing B03 patterns
- Provider-specific error taxonomies
- Changing Axiom 6 or introducing exceptions

## Consequences

- README / S01 Host docs should link this ADR once **Accepted**
- Failure glossary residual on scorecard / expressiveness review closes on Accept
- Feature work may add Host-only error DTO fields without touching Kernel

## Alternatives considered

| Option | Rejected because |
|---|---|
| One unified error type across language + Host | Violates NLTS / ports; collapses layers |
| Restore exceptions in object language | Contradicts axioms |
| Docs-only informal README without ADR | Already failed to prevent conflation |

## Acceptance

- [x] Adjudicator Accept (2026-08-02「承認」)
- [x] S01 README pointer (WP-0087)
- [x] Cross-link: axioms companion note + architecture README ADR index
- [ ] Follow-up Feature Issues only if Host/Kernel need structured codes (none required now)
