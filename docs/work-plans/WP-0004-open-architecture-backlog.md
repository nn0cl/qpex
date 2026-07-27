# Work Plan: Open architecture backlog

## Goal

Create and adjudicate the local Issue/ADR surface for every known QPex
capability before beginning another implementation slice.

## Scope

- In: LISS-0010 through LISS-0019, the open-work register, and required ADR/spec
  updates produced by review.
- Out: Kernel code, parser changes, tests, provider SDKs, and live QPU submit.

## Issue Graph

Statuses synchronized 2026-07-25 against the canonical
[`open-work-register.md`](../architecture/open-work-register.md) and each
Issue's own metadata; every row below has cleared Architecture Path review.
None of this is Feature Path implementation approval — see Current Next
Issue below.

| Issue | Status | Size | Depends on | Blocks |
|---|---|---:|---|---|
| LISS-0010 QFT | Phase 3 reviewed; type/provenance boundary and official example complete (ADR 0078). Gate lowering shipped separately via LISS-0042; example supplied by LISS-0020 | L | LISS-0006 | controlled/approximate QFT follow-ups |
| LISS-0011 Density/Lindblad | Phase 3 reviewed | XL | ADR 0057 | general mixed-state/QPU follow-ups deferred |
| LISS-0012 `until` | Phase 3 reviewed; grammar/type boundary complete (ADR 0079). Runtime repetition remains deferred | L | LISS-0015 | runtime repetition implementation |
| LISS-0013 Pipeline/currying | Phase 3 reviewed (ADR 0080). Partial-application values and fusion remain deferred | L | ADR 0018/0021/0032 | fusion surface |
| LISS-0014 Trait/system | Phase 3 reviewed (ADR 0082). Dispatch and specialization remain deferred | L | ADR 0019/0024/0056/0015 | dispatch/specialization implementation |
| LISS-0015 Effects | Phase 3 reviewed (ADR 0081). Effect rows and provider-specific effects remain deferred | L | ADR 0018/0029/0030 | effect rows implementation |
| LISS-0016 Host submit | Phase 3 reviewed (ADR 0083). Provider SDK, credentials, network adapter, and automatic retry remain deferred — out of MVP scope per `AGENTS.md` project boundaries | L | ADR 0036/0059/0019 | provider workflow (post-MVP) |
| LISS-0017 Suzuki/error | Phase 3 reviewed | L | ADR 0084 | higher-accuracy QASM; S4/adaptive selection deferred |
| LISS-0018 Numerical representation | Phase 3 reviewed; numeric policy slice complete (ADR 0076). Continuous PDFs and exact arithmetic remain deferred | L | ADR 0014/0018/0037 | continuous/exact extensions |
| LISS-0019 QPU IR | Phase 3 reviewed; inspection boundary complete. Concrete opcode lowering shipped separately via LISS-0041 (ADR 0085) | L | ADR 0032/0059/0016 | multi-backend lowering |
| LISS-0021 Function returns | **Complete** (2026-07-25; historical row, see WP-0017) | XL | ADR 0018/0021/0027/0037/0054/0056/0064/0068 | composable functions and methods |
| LISS-0066 QPU observation/result integration | Phase 3 Refactor complete | L | LISS-0044/0046/0047/0065; ADR 0091/0092/0103 | provider SDK/live execution remains deferred |
| LISS-0067 Multi-register acting-space and QPU mapping | Phase 3 reviewed | L | LISS-0058; ADR 0069/0102/0105; LISS-0041/0065/0066 | named static registers, RegisterSet typing, qualified sites, and logical/flat QPU mapping reviewed; routing remains gated |

## Recommended Order

Steps 1–5 below are historical and complete as of 2026-07-25 — every Issue
in this backlog has reached Architecture Path / Phase 3 review (see table
above). They are kept for record; do not re-run them as if still pending.

1. ~~Review and accept/reject the proposed Issue scopes and dependencies,
   including LISS-0021 as the highest-priority language-surface item.~~ Done.
2. ~~Architecture decisions: LISS-0011, 0015, 0013, 0014, 0019.~~ Done.
3. ~~Feature specifications: LISS-0012 and LISS-0017.~~ Done.
4. ~~Technology/representation triage: LISS-0018 and LISS-0016.~~ Done.
5. ~~Reassess LISS-0010 QFT after the state and backend decisions.~~ Done
   (LISS-0042 shipped basic-gate lowering separately).
6. Request Feature Path Phase 1 Red for a selected deferred sub-scope from
   the table above — this is the only step still open.

## Current Next Issue

- No issue selected. LISS-0067 is now Phase 3 reviewed and complete.
- The next independent implementation slice requires a separate Issue/ADR
  selection and explicit Phase 1 approval. Provider selection and physical
  routing remain separately gated and are not implicitly selected here.

## Risks

- Premature implementation could create conflicting semantics across Python and
  future Rust generations.
- Host submit or QPU IR could leak provider policy into the Kernel.
- Grouped numerical questions may need to split after review.

## Verification Plan

- `git diff --check`.
- Cross-reference check from the open-work register and local Issue index.
- ADR/spec acceptance records before any Feature Path phase begins.
