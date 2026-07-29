# LISS-0082 Slice B follow-up 1 — Phase 1 Red

- Date: 2026-07-30
- Branch: `feature/liss-0082-slice-b-red`
- Operating path: Feature Path
- Issue: LISS-0082
- Slice/phase: Slice B follow-up 1 (gaps 1, 2, 5) / Phase 1 Red
- Approval: Adjudicator message of 2026-07-30 authorizing "B 追補-1（ギャップ
  1・2・5）の Phase 1 Red のみ", scoped to tests, trace, and minimal Issue/plan
  synchronization
- Implementation permission: **none** — `compiler/staqex/quantum_semantic_ir.py`
  is explicitly excluded
- Technology selection permission: **none**
- Post-review required: Adjudicator review of the Red failure reasons and
  assertions before Green/Refactor is decided

## Corrected framing

An earlier agent summary said these gaps would "fit inside the existing two
Slice B diagnostic codes". **That was wrong** and is corrected here: the Slice A
identity and provenance diagnostics are *extended to Slice B definition sites*.

| Gap | Code | Definition sites now in scope |
|---|---|---|
| 1 | `QSEM_IDENTITY_CONFLICT` | `ActingSpace.space_id`, `ActingFactor.factor_id`, Joint `value_id` |
| 2 | `QSEM_PROVENANCE_INCOMPLETE` | `SemanticOrigin` embedded in `ActingSpace` and Joint values |
| 5 | `QSEM_ACTING_SPACE_INVALID` | `value.resources` versus the ordered factor identities |

An identity appearing as a **reference** — `value.space_id`, `value.resources`,
`producer_id`, `JointValueUse.value_id` / `consumer_id` / `factor_id`,
`SemanticOrigin.upstream_ids` — is not a definition and must never be counted as
a duplicate.

## Scope

Added only `tests/test_quantum_semantic_ir_slice_b_followup_red.py` (10 tests).
No file under `compiler/` was changed. Existing Slice A and Slice B suites were
not edited.

## Red evidence

`python3 tests/test_quantum_semantic_ir_slice_b_followup_red.py` → exit 1,
**8 failed / 2 passed**.

The expected Red is **failing assertions**, not an import or compile failure:
the Slice B API already exists, but its verifier does not yet inspect Slice B
definition identities, embedded provenance, or resource order.

| Test | Result | Reason |
|---|---|---|
| `test_duplicate_acting_space_definitions_conflict` | FAIL | no `QSEM_IDENTITY_CONFLICT` for two spaces sharing one `space_id` |
| `test_duplicate_factor_definitions_conflict_within_and_across_spaces` | FAIL | factor identities are never inspected |
| `test_duplicate_joint_value_definitions_conflict` | FAIL | value identities are never inspected |
| `test_definition_conflict_is_detected_across_categories` | FAIL | a shared identity across a space and a value is not reported |
| `test_referenced_identities_are_not_counted_as_duplicate_definitions` | **pass** | guard: a well-formed module must stay diagnostic-free after Green |
| `test_incomplete_acting_space_origin_is_reported` | FAIL | embedded space origin is never validated |
| `test_incomplete_joint_value_origin_is_reported` | FAIL | embedded value origin is never validated |
| `test_resources_out_of_factor_order_are_reported` | FAIL | only arity is checked, so a reversed order passes |
| `test_resources_naming_unknown_factors_are_reported` | FAIL | only arity is checked, so unrelated identities pass |
| `test_resources_in_factor_order_are_accepted` | **pass** | guard: exact factor order must keep verifying |

The two passing tests are deliberate guards against over-correction in Green,
not evidence of implemented behavior.

## Other deterministic verification

- `python3 tests/test_quantum_semantic_ir_slice_a_red.py` — passed.
- `python3 tests/test_quantum_semantic_ir_slice_b_red.py` — passed.
- `python3 -m py_compile tests/test_quantum_semantic_ir_slice_b_followup_red.py`
  — passed.
- `git status --short compiler/` — empty.
- pytest is not installed in this workspace; the direct entry point is the
  deterministic check, matching the earlier LISS-0082 traces. This suite reports
  every test result before exiting non-zero, so all eight Red reasons are
  visible in one run.

## Decisions recorded, not implemented

- **Gap 4 — approved: no ordering field.** Two or more consuming uses of one
  generation are a linearity violation regardless of whether they are
  sequential or parallel. The public wording is a violation of *"one
  generation, at most one consuming path"*; use-after-consume is **not**
  described as a mere alias of fan-out. The shipped diagnostic message
  (`quantum_semantic_ir.py`) already reads "joint state generation has more than
  one consuming path", so no code change is required or authorized here. Cycle
  detection is delegated to the Slice C region graph.
- **Gap 3 — approved: option (a), deferred.** Only the bare integer
  `generation` field is to be removed; the *generation* semantics stay, carried
  by `value_id` as the identity of one immutable whole-Joint-state generation.
  `lineage_id + generation index` is rejected: it would flatten branching,
  merging, and hierarchical regions into a running number without region-graph
  justification. Because this subtracts from an approved API, it must **not** be
  mixed into this follow-up. It needs an Architecture Path update aligning
  ADR 0108, the detailed contract, and the Issue/plan, plus its own reviewed Red
  first. This trace records the decision only; no field was removed.

## Stop condition

Stop after Red evidence. Do not modify `compiler/`, do not edit these
assertions to make them pass, and do not start Green, Refactor, the gap 3
Architecture Path work, Slice C, or a PR without separate approval.
