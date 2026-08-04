# P0/P1 current-hardware delivery rebaseline

- Date: 2026-07-30
- Branch: `codex/p0-p1-delivery-horizon-review`
- Operating path: Architecture Path
- Current phase: Phase 0 design intake
- Approved scope: review P0, plan P1 and later work, preserve ambitious future
  design, and require P0/P1 to remain meaningfully executable on current
  quantum computers
- Added scope: include planned 2026–2031 machine profiles
- Planning size: XL
- Implementation permission: **none**
- Technology selection permission: **none**
- Post-review required: ADR 0111 and WP-0029 architecture approval; every
  Feature Path phase and provider/simulator selection remains separate

## Design result

- P0 becomes an **executable foundation**, not a DTO-only milestone.
- P1 becomes a **useful current quantum workflow**, ending with one separately
  selected live provider adapter.
- Current hardware uses conservative CH0/CH1 and simulator profiles.
- 2026–2031 announcements use NH5 NISQ/modular, megaquop, gigaquop, and
  large-native synthetic profiles.
- QP-1/QP-2/QS-2 remain future capacity stress profiles.
- All profiles consume one scale-free source/Semantic IR/Algorithm Plan model.

## Priority decisions proposed

- Keep LISS-0082, 0083, 0087, 0094, 0097, 0099, 0077, and 0120 on P0 with
  current-profile evidence requirements.
- Promote LISS-0093 bounded mitigation from P2 to P1.
- Promote LISS-0100 first live provider adapter from P2 to the P1 integration
  endcap.
- Move LISS-0098 QIR/toolchain from P1 to P2 while Rust remains deferred and
  OpenQASM is the first current-machine path.
- Slice advanced fault-tolerant planner methods behind bounded current methods.

## Evidence boundary

Public vendor pages and specifications are dated primary claims, not
independent guarantees. Counts are not compared as equivalent performance
metrics across superconducting, trapped-ion, neutral-atom, analog, or
fault-tolerant systems.

No provider SDK, credentials, account, pricing, or private calibration data was
used.

## Artifacts

- [Current hardware research](../../research/2026-07-30-current-quantum-hardware-delivery-envelope.md)
- [Delivery envelope](../../architecture/current-hardware-delivery-envelope.md)
- [ADR 0111](../../architecture/decision-themes/dec-0006-host-qpu-and-external-ports.md)
- [WP-0029](../../work-plans/WP-0029-current-hardware-delivery-horizon.md)
- [Quantum Semantic IR contract](../../architecture/quantum-semantic-ir-contract.md)
- [LISS-0082](../../architecture/documentation-compression-map.md)
- [LISS-0120](../../issues/LISS-0120-representative-program-language-review-gate.md)
- [WP-0025](../../work-plans/WP-0025-staqex-v1-north-star.md)
- [Bounded execution packet](../../architecture/bounded-feature-execution-packet.md)
- P0/P1 local Issue documents for LISS-0077–0079, 0082–0097, and 0099–0104

## Verification

- all changed paths are documentation paths;
- local Markdown links resolve across all changed documents;
- `git diff --check` passes;
- branch and base are isolated at `origin/main` revision `2ca9ac0`;
- no tests or implementation were changed or executed.
- all 26 P0/P1 roadmap Issues have one local Issue document with bounded
  acceptance scenarios, Slice boundaries, model-routing stops, and phase
  gates.

## Stop condition

Stop after documentation synchronization and deterministic verification. Do
not write tests, implementation, provider adapters, simulator integrations, or
sample source.
