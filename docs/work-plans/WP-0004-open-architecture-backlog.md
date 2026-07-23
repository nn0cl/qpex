# Work Plan: Open architecture backlog

## Goal

Create and adjudicate the local Issue/ADR surface for every known QPex
capability before beginning another implementation slice.

## Scope

- In: LISS-0010 through LISS-0019, the open-work register, and required ADR/spec
  updates produced by review.
- Out: Kernel code, parser changes, tests, provider SDKs, and live QPU submit.

## Issue Graph

| Issue | Status | Size | Depends on | Blocks |
|---|---|---:|---|---|
| LISS-0010 QFT | proposed | L | LISS-0006 | real QFT implementation |
| LISS-0011 Density/Lindblad | proposed | XL | ADR 0018/0016 | mixed-state Kernel |
| LISS-0012 `until` | proposed | L | LISS-0015 | `until` implementation |
| LISS-0013 Pipeline/currying | proposed | L | ADR 0018/0021/0032 | fusion surface |
| LISS-0014 Trait/system | proposed | L | ADR 0019/0024/0056/0015 | abstraction implementation |
| LISS-0015 Effects | proposed | L | ADR 0018/0029/0030 | effect-aware features |
| LISS-0016 Host submit | proposed | L | ADR 0036/0059/0019 | provider workflow |
| LISS-0017 Suzuki/error | proposed | L | ADR 0050/0063 | higher-accuracy QASM |
| LISS-0018 Numerical representation | proposed | L | ADR 0014/0018/0037 | continuous/exact extensions |
| LISS-0019 QPU IR | proposed | L | ADR 0032/0059/0016 | multi-backend lowering |
| LISS-0021 Function returns | proposed | XL | ADR 0018/0021/0027/0037/0054/0056 | composable functions and methods |

## Recommended Order

1. Review and accept/reject the proposed Issue scopes and dependencies,
   including LISS-0021 as the highest-priority language-surface item.
2. Architecture decisions: LISS-0011, 0015, 0013, 0014, 0019.
3. Feature specifications: LISS-0012 and LISS-0017.
4. Technology/representation triage: LISS-0018 and LISS-0016.
5. Reassess LISS-0010 QFT after the state and backend decisions.
6. Only then request Feature Path Phase 1 Red for a selected Issue.

## Current Next Issue

- Issue: Adjudicator review of this Issue graph and the proposed scopes.
- Reason: all listed work is design-gated; no implementation is authorized.
- Adjudicator approval needed: scope and Architecture Path approval.

## Risks

- Premature implementation could create conflicting semantics across Python and
  future Rust generations.
- Host submit or QPU IR could leak provider policy into the Kernel.
- Grouped numerical questions may need to split after review.

## Verification Plan

- `git diff --check`.
- Cross-reference check from the open-work register and local Issue index.
- ADR/spec acceptance records before any Feature Path phase begins.
