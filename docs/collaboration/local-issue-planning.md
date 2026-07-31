# Local Issue Planning

Issues can be managed in GitHub and as local Markdown files.

Local issue files are useful when:

- planning offline.
- preparing work before a GitHub repository is connected.
- letting AI agents reason about issue dependencies without network access.
- keeping feature-unit branch planning close to the repository.

GitHub Issues remain useful for remote collaboration, notifications, and public
review. Local issues are the repository-native planning ledger.

## Location

Store local issues under:

```text
docs/issues/
```

Store multi-issue work plans under:

```text
docs/work-plans/
```

Keep `.gitkeep` files in both folders so they exist before the first issue or
plan is created.

## Issue File Naming

Use stable local IDs:

```text
LISS-0001-short-title.md
LISS-0002-short-title.md
```

`LISS` means local issue. Do not reuse IDs.

When a GitHub Issue exists, add its number or URL in the local issue metadata.

## Active ID claims (collision avoidance)

Parallel agents must not reuse claimed IDs. As of 2026-07-29:

| ID | Topic | Notes |
|---|---|---|
| LISS-0081 | Physics IR structural boundary | **complete** 2026-07-29 |
| LISS-0082 | Quantum Semantic IR | **complete** A–F; soft `CompileResult.quantum_semantic_ir`; ADR 0108–0111 **Accepted** |
| LISS-0091 | Resource estimation and feasibility | **complete** — PR #161 (`e1e93a9`); `resource_estimate.py` |
| LISS-0092 | Layout, routing, native translation, and scheduling | **complete** — PR #163 (`afdbfa9`); `target_routing.py` |
| LISS-0099 | Target capability profile and physical target port | **complete** — PR #165 (`ad89d15`); `target_capability.py` |
| LISS-0094 | Simulator port and capability profiles | **complete** — PR #166 (`b6d2dda`); `simulator_port.py` |
| LISS-0097 | OpenQASM 3 backend (P0 static CH0) | **complete** — PR #167 (`83b34e7`); `ch0_emit.py`; D/E/F deferred |
| LISS-0077 | Dynamic QPU controller / feed-forward (P0) | **complete** — P0 package; `dynamic_qpu.py`; branch `feature/liss-0077-dynamic-qpu` pending merge; E deferred |
| LISS-0116 | Equation / Unit DTO | **complete** A–C |
| LISS-0115 | HIR→Physics IR lowering | **complete** A–D (soft `CompileResult.physics_ir`) |
| LISS-0117 | Source-backed Physics IR goldens | **complete** A–C (full six-family oracle deferred) |
| LISS-0118 | Body-level phase typing residuals | **complete** 2026-07-29 (A–C) |
| LISS-0120 | Representative program language review gate | **rejected / deferred** — rebaseline Accepted |
| LISS-0121 | Classical coefficient elaboration vs LINEAR | **complete** — Phase 3 reviewed 2026-07-31 |
| LISS-0119 | Examples health inventory (rebaseline P0) | **complete** — 2026-07-31 |
| LISS-0122 | Examples basics heal (rebaseline P0) | **complete** — 2026-07-31 |
| LISS-0123 | Examples applied heal/defer (rebaseline P0) | **complete** — 2026-07-31 |
| LISS-0124 | Language coverage ledger (rebaseline P1) | **complete** — 2026-07-31 |
| LISS-0125 | HIR BinOp `_expr_children` field mismatch | **complete** — Phase 3 2026-07-31 |
| LISS-0126 | Showcase mission lock (Gate P2) | **complete** — 2026-07-31 |
| LISS-0127 | Showcase S0 specification | **complete** — 2026-07-31 (docs) |
| LISS-0128 | Open Topics before S1 (Option B) | **complete** — 2026-07-31 |
| LISS-0129 | Typed surface annotations | **complete** — 2026-07-31 |
| LISS-0130 | `evolve until` ledger reconcile | **complete** — 2026-07-31 |
| LISS-0131 | ADR 0057 showcase boundary | **complete** — 2026-07-31 |
| LISS-0132 | Open Topics permanent-out | **complete** — 2026-07-31 |
| LISS-0133 | Expression residuals | **complete** — 2026-07-31 |
| LISS-0134 | Showcase S1 thin slice | **complete** — 2026-07-31 (merged #179) |
| LISS-0135 | QPU capability honesty | **complete** — 2026-07-31 |
| LISS-0136 | Sparse Pauli Operator return from helper `fn` | **complete** — 2026-07-31 (merged #180) |
| LISS-0137 | Classical Float → Operator / `evolve for` (+ param factory) | **complete** — 2026-07-31 (PR pending) |
| LISS-0138 | `when` ket prepare arms | **complete** — 2026-07-31 (PR pending) |
| LISS-0139 | Operator RHS method Call parse + return | **complete** — 2026-07-31 (PR pending) |
| LISS-0140 | QPU honesty catalog (WP-0032) | **complete** — 2026-07-31 (PR #184) |
| LISS-0141 | Binder `where &&` | **complete** — 2026-07-31 (PR #184) |
| LISS-0142 | Showcase S4 slice | **complete** — 2026-07-31 (PR #184) |
| LISS-0143 | `Float[N]` + `J[i]` | **complete** — 2026-07-31 (PR #184) |
| LISS-0144 | ND Float coeffs (WP-0033) | **complete** — 2026-07-31 (PR #185) |
| LISS-0145 | Binder `where \|\|` | **complete** — 2026-07-31 (PR #186) |
| LISS-0146 | Dependent / static Index endpoints | **complete** — 2026-07-31 (PR #186) |
| LISS-0147 | `rev` binder domains | **complete** — 2026-07-31 (PR #186) |
| LISS-0148 | `Basis<N>` binder expansion | **complete** — 2026-07-31 (PR pending) |
| LISS-0149 | Partial Float classical indexing | **complete** — 2026-07-31 (PR pending) |
| LISS-0150 | Host CoefficientTensor inject | **complete** — 2026-07-31 (PR pending) |
| LISS-0151 | Exact cqft / ciqft | **complete** — 2026-07-31 (PR pending) |
| LISS-0152 | Permanent-out reopen | **complete** — 2026-07-31 |
| LISS-0153 | SI base dims Current/Temperature | **complete** — 2026-07-31 |
| LISS-0154 | Pipe unary bare `\|\> f` | **complete** — 2026-07-31 |
| LISS-0155 | Function Partial `_` holes | **complete** — 2026-07-31 |
| LISS-0156 | Explicit SI `expr to unit` | **complete** — 2026-07-31 |
| LISS-0157 | Exact rational design boundary | **complete** (docs) — 2026-07-31 |
| LISS-0158 | Continuous PDF design boundary | **complete** (docs) — 2026-07-31 |
| LISS-0159 | Live QPU credentials boundary | **complete** (docs) — 2026-07-31 |
| LISS-0160 | Trait/effect expansion boundary | **complete** (docs) — 2026-07-31 |
| LISS-0161 | SI scale catalog wave-2 | **complete** — 2026-07-31 |
| LISS-0162 | User-fn State-forming Call args | **complete** — 2026-07-31 |

WP-0028 (0115–0117 parallelism) is **closed**. WP-0032–0039 shipped binder /
Float / Basis / Host / cqft / permanent-out reopen / Partial+SI / SI-wave2 slices.
Next free for **new** ad-hoc Issues: **LISS-0163+**. WP-0025 still reserves `0070`,
`0077`–`0079`, `0081`–`0105` as roadmap rows (do not invent unrelated work
under those numbers).

## Required Issue Fields

Each local issue should record:

- local issue ID.
- title.
- status.
- phase.
- type.
- priority.
- initial and current planning size.
- owner or agent.
- related GitHub issue when available.
- parent issue when any.
- depends on.
- blocks.
- related branch.
- acceptance notes.
- Adjudicator decision points.
- an AI planning record when the current planning size is `M` or larger.

## Bug Planning

Record a discovered bug in a local issue or an existing work plan before
fixing it. Use exactly one durable planning artifact as the canonical record;
other artifacts should link to its issue ID or AI planning record ID rather
than copying mutable details.

A separate issue or work plan is optional only when all of these are true:

- the bug is within the current Adjudicator-approved scope.
- its planning size is `S`.
- the expected behavior is explicit in an accepted specification, an accepted
  test, or established behavior approved by the Adjudicator.
- the correction remains within one file or one feature area.
- it does not change an architecture boundary, data model, migration,
  dependency, security policy, privacy policy, or external contract.
- a deterministic verification method exists.
- the correction succeeds in one execution attempt.

This exception waives only the separate planning artifact. It never waives
design intake, test review, phase gates, branch discipline, or verification.
Record an exempt correction in the active issue or plan, commit, trace, or
durable final report with:

```text
Minor bug; fixed within approved scope; separate plan not required
```

Use the existing approved plan when the bug is already within its scope. If an
accepted test already reproduces the bug, record the Red result and obtain
Adjudicator confirmation before Phase 2. If no accepted test reproduces it, add a
regression test in Phase 1 and wait for review before Phase 2. Create a new
issue or work-plan entry when scope, expected behavior, dependencies, or
boundaries are uncertain. Record but do not mix a bug that is outside the
current scope.

## Planning Size

Planning size describes scope, uncertainty, dependencies, and verification
effort. It is not an elapsed-time estimate or delivery commitment.

| Size | Planning criteria |
| --- | --- |
| `S` | One file or one area, explicit expected behavior, local correction, and deterministic verification |
| `M` | Related changes across multiple files, a small behavior change, or more than one execution attempt |
| `L` | Multiple modules or phases, broad verification, or meaningful uncertainty |
| `XL` | Architecture boundaries, migrations, multiple dependent issues, or high uncertainty |
| `TBD` | Investigation is still required before a reliable size can be assigned |

When criteria overlap, select the largest applicable size. Preserve both the
initial and current size. Do not rewrite the initial size after work begins.
Record a reclassification reason whenever the current size changes.

At the second execution attempt, re-triage the issue. Normally reclassify an
`S` issue to at least `M`; it may remain `S` only when the repeated attempt was
caused by an unrelated external or transient failure, with the reason recorded.

## AI Planning Records

Planning-size `M`, `L`, and `XL` work requires a vendor-neutral AI planning
record in its canonical local issue or work plan. `S` work may use one
optionally, but it becomes required when a second attempt starts.

Each record has a stable ID and records:

- status.
- the authoring agent/environment.
- model and reasoning setting exactly as displayed, or `N/A` with a reason.
- creation date.
- planning size.
- intended execution route and scope.
- estimated token range, midpoint, and metric, or `N/A` with a reason.
- estimation basis, assumptions, and confidence.
- revision links and reason when another record changes the plan.

Do not silently edit another agent's accepted estimate. Append a new record,
mark the prior record `superseded`, and connect them using `Revises` and
`Superseded by`. Planning and execution may be performed by different agents;
the execution trace references the accepted planning record ID.

See `docs/collaboration/ai-work-trace-log.md` for attempt boundaries and the
conditions that make a trace mandatory.

## Dependency Rules

Use issue dependencies to define work order before implementation.

Allowed dependency meanings:

- `depends_on`: this issue should not start before the listed issue is done or
  explicitly waived.
- `blocks`: listed issues are blocked by this issue.
- `parent`: this issue is part of a larger work item.
- `related`: useful context, but not an ordering constraint.

Agents must not start work on an issue with unresolved `depends_on` entries
unless the Adjudicator explicitly waives the dependency.

Agents must not implement issue work directly on `main` or the trunk branch.
Every local issue or GitHub Issue requires a dedicated branch before any
commit for that issue is made, per
`docs/collaboration/branch-commit-pr-discipline.md`.

## Planning Flow

Before starting planned feature or bug work:

1. create or update local issues.
2. identify issue dependencies.
3. create a work plan under `docs/work-plans/`.
4. select the next unblocked issue.
5. create a feature-unit branch for that issue or feature slice.
6. run design intake.

## Status Values

Use:

- `proposed`
- `ready`
- `in_progress`
- `blocked`
- `review`
- `done`
- `wont_do`

## Phase Values

Use:

- `phase-0-design`
- `phase-1-red`
- `phase-2-green`
- `phase-3-refactor`
- `docs-only`
- `process-only`

## Synchronization with GitHub Issues

When both local and GitHub issues exist:

- keep the local issue as the detailed planning artifact.
- keep GitHub Issue title, status, and links aligned when practical.
- include the GitHub Issue URL in the local issue.
- include the local issue ID in the GitHub Issue or PR text.

Do not require GitHub network access for local planning.

## Current Staqex local issues (index)

| ID | Title | Status |
|----|-------|--------|
| [LISS-0001](../issues/LISS-0001-language-axioms-mvp-spec.md) | Language axioms MVP | **done** |
| [LISS-0002](../issues/LISS-0002-openqasm3-codegen-backend.md) | OpenQASM 3 codegen | **done** (Trotter split to LISS-0008) |
| [LISS-0003](../issues/LISS-0003-examples-driven-kernel-brush-up.md) | Examples-driven brush-up (parent) | **done** |
| [LISS-0004](../issues/LISS-0004-joint-preservation-classical-env.md) | Joint preserve + classical env | **done** |
| [LISS-0005](../issues/LISS-0005-classical-module-config-harvest.md) | Classical config harvest | **done** |
| [LISS-0006](../issues/LISS-0006-examples-catalog-honesty.md) | Catalog honesty / SV-09 | **done** |
| [LISS-0007](../issues/LISS-0007-prelude-pi-constant.md) | Prelude `pi` / `Math.pi` | **done** |
| [LISS-0008](../issues/LISS-0008-trotter-evolve-qasm.md) | Trotterize `evolve under H` → QASM | **done** (higher-order Suzuki is tracked separately) |
| [LISS-0009](../issues/LISS-0009-chalkboard-dx.md) | Chalkboard DX / cut magic floats | **done** (bare `H` deferred) |
| [LISS-0010](../issues/LISS-0010-kernel-qft-surface.md) | Kernel QFT surface (deferred) | **proposed** |
| [LISS-0011](../issues/LISS-0011-density-matrix-lindblad.md) | Density matrix / Lindblad CPTP | **Phase 3 reviewed: numeric/runtime/source and one-qubit symbolic slices complete** |
| [LISS-0012](../issues/LISS-0012-evolve-until.md) | `evolve until` semantics | **proposed** |
| [LISS-0013](../issues/LISS-0013-pipeline-currying.md) | Pipeline / currying surface | **proposed** |
| [LISS-0014](../issues/LISS-0014-trait-impl-system.md) | Trait `impl` / `system` model | **proposed** |
| [LISS-0015](../issues/LISS-0015-effect-marking.md) | Effect marking | **proposed** |
| [LISS-0016](../issues/LISS-0016-host-qpu-submit.md) | Host-side QPU submit adapter | **proposed** |
| [LISS-0017](../issues/LISS-0017-higher-order-suzuki.md) | Higher-order Suzuki / error control | **Phase 3 reviewed** |
| [LISS-0018](../issues/LISS-0018-numerical-representation.md) | Numerical representation follow-ups | **proposed** |
| [LISS-0019](../issues/LISS-0019-qpu-ir.md) | Concrete QPU IR boundary | **proposed** |
| [LISS-0020](../issues/LISS-0020-capstone-quantum-observatory.md) | Quantum Observatory capstone example | **complete for expanded Kitchen Sink slice (P0)** |
| [LISS-0041](../issues/LISS-0041-qpu-ir-lowering.md) | Provider-neutral QPU IR lowering | **Phase 3 reviewed** |
| [LISS-0042](../issues/LISS-0042-qft-basic-gate-lowering.md) | QFT/IQFT basic-gate lowering | **Phase 3 reviewed** |
| [LISS-0120](../issues/LISS-0120-representative-program-language-review-gate.md) | Representative program language review gate | **rejected / deferred** |
| [LISS-0121](../issues/LISS-0121-classical-coefficient-elaboration-vs-linear.md) | Classical coefficient elaboration vs LINEAR | **complete** (ADR 0114; Phase 3) |
| [LISS-0119](../issues/LISS-0119-examples-health-inventory.md) | Examples health inventory (Gate P0) | **complete** |
| [LISS-0122](../issues/LISS-0122-examples-basics-heal.md) | Examples basics heal (Gate P0) | **complete** |
| [LISS-0123](../issues/LISS-0123-examples-applied-heal-defer.md) | Examples applied heal/defer (Gate P0) | **complete** |
| [LISS-0124](../issues/LISS-0124-language-coverage-ledger.md) | Language coverage ledger (Gate P1) | **complete** |
| [LISS-0125](../issues/LISS-0125-hir-binop-expr-children.md) | HIR BinOp `_expr_children` field mismatch | **complete** |
| [LISS-0126](../issues/LISS-0126-showcase-mission-lock.md) | Showcase mission lock (Gate P2) | **complete** |
| [LISS-0127](../issues/LISS-0127-showcase-s0-specification.md) | Showcase S0 specification | **complete** (docs) |
| [LISS-0128](../issues/LISS-0128-open-topics-before-s1-program.md) | Open Topics before S1 (Option B) | **complete** |
| [LISS-0129](../issues/LISS-0129-typed-surface-annotations.md) | Typed surface annotations | **complete** |
| [LISS-0130](../issues/LISS-0130-evolve-until.md) | `evolve until` ledger reconcile | **complete** |
| [LISS-0131](../issues/LISS-0131-density-lindblad-showcase-boundary.md) | ADR 0057 showcase boundary | **complete** |
| [LISS-0132](../issues/LISS-0132-open-topics-permanent-out.md) | Open Topics permanent-out | **complete** |
| [LISS-0133](../issues/LISS-0133-expression-residuals.md) | Expression residuals | **complete** |
| [LISS-0135](../issues/LISS-0135-qpu-capability-honesty.md) | QPU capability honesty | **complete** |


Work plans: [WP-0003](../work-plans/WP-0003-examples-driven-brush-up.md),
[WP-0004](../work-plans/WP-0004-open-architecture-backlog.md),
[WP-0016](../work-plans/WP-0016-quantum-observatory-capstone.md).
Default branch: `main`.

## Review Rule

Adjudicator review is required when:

- issue dependencies are unclear.
- an issue is split or merged.
- work starts despite unresolved dependencies.
- the planned branch scope does not match the issue scope.
