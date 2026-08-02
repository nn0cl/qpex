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
| LISS-0070 | Rust compiler infrastructure | **deferred** — next version (restored WP-0077 / LISS-0212) |
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
| LISS-0163 | Stepwise Partial fill | **complete** — 2026-07-31 |
| LISS-0164 | Exact SI `eV`↔`J` | **complete** — 2026-07-31 |
| LISS-0165 | Pipeline leftmost hole fill | **complete** — 2026-07-31 |
| LISS-0166 | Affine °C↔K | **complete** — 2026-07-31 |
| LISS-0167 | Affine °F↔K | **complete** — 2026-07-31 |
| LISS-0168 | Mass `g`↔`kg` | **complete** — 2026-07-31 |
| LISS-0169 | Pipeline Operator Fusion MVP | **complete** — 2026-07-31 |
| LISS-0170 | Trace-Out GC fn-scope MVP | **complete** — 2026-07-31 |
| LISS-0171 | Interference prune / support-merge MVP | **complete** — 2026-07-31 |
| LISS-0172 | Deferred Pushforward MVP | **complete** — 2026-07-31 |
| LISS-0173 | Algebraic Operator Fusion MVP | **complete** — 2026-07-31 |
| LISS-0174 | Evolve-block Trace-Out GC MVP | **complete** — 2026-07-31 |
| LISS-0175 | Call/Partial pipe Fusion MVP | **complete** — 2026-07-31 |
| LISS-0176 | Rankine affine °R ↔ K | **complete** — 2026-07-31 |
| LISS-0177 | Imperial pound mass `lb` ↔ `kg` | **complete** — 2026-07-31 |
| LISS-0178 | Imperial ounce mass `oz` | **complete** — 2026-07-31 |
| LISS-0179 | Imperial stone mass `st` | **complete** — 2026-07-31 |
| LISS-0180 | Metric tonne mass `t` | **complete** — 2026-07-31 |
| LISS-0181 | Multi-hole Partial pipe fill | **complete** — 2026-07-31 |
| LISS-0182 | US/UK ton mass `ton_us` / `ton_uk` | **complete** — 2026-07-31 |
| LISS-0183 | Troy ounce mass `oz_t` | **complete** — 2026-07-31 |
| LISS-0184 | Tuple multi-hole pipe / Fusion fill | **complete** — 2026-07-31 |
| LISS-0185 | Bare-block Trace-Out GC | **complete** — 2026-07-31 |
| LISS-0186 | Mixed-unit arithmetic reject | **superseded** — 2026-07-31 by LISS-0187 / ADR 0155 |
| LISS-0187 | Mixed-unit canonical promote | **complete** — 2026-07-31 |
| LISS-0190 | Quadratic / polynomial pipe Fusion | **complete** — 2026-07-31 |
| LISS-0191 | Interprocedural Trace-Out GC | **complete** — 2026-07-31 |
| LISS-0192 | CPU data-parallel Joint world workers | **complete** — 2026-07-31 |
| LISS-0193 | Classical Fraction literals → f64 at State | **complete** — 2026-07-31 |
| LISS-0194 | CredentialPort + Env + mock submit | **complete** — 2026-07-31 |
| LISS-0195 | Host MC → finite State inject | **complete** — 2026-07-31 (ADR 0163 / WP-0067) |
| LISS-0196 | Trait specialization surface examples (design) | **open** (design) — ADR 0128 maintained |
| LISS-0197 | Display-unit restore after promote | **deferred** — no ship this batch |
| LISS-0198 | Host MC inject consumption seam | **complete** — 2026-07-31 (ADR 0164 / WP-0068) |
| LISS-0199 | `staqex check` false-OK on hard errors | **complete** — 2026-08-01 (WP-0074) |
| LISS-0200 | Hard-code set divergence (`run` vs `pipeline`) | **complete** — 2026-08-01 (WP-0074) |
| LISS-0201 | Partial-hole `KeyError` crash | **complete** — 2026-08-01 (WP-0074) |
| LISS-0202 | Linear-discipline regression cluster (21) | **complete** — 2026-08-01 (WP-0073 / LISS-0221) |
| LISS-0203 | Qudit local-dimension typing regression (6) | **complete** — 2026-08-01 |
| LISS-0204 | Class-method return-type regression (5) | **complete** — 2026-08-01 (WP-0075) |
| LISS-0205 | Dirac block-result parse regression (2) | **complete** — 2026-08-01 (WP-0075) |
| LISS-0206 | SI conversion diagnostic regression (2) | **complete** — 2026-08-01 (WP-0075) |
| LISS-0207 | Residual regression cluster (3) | **complete** — 2026-08-01 (WP-0075) |
| LISS-0208 | Test harness hygiene (10 unrunnable suites) | **complete** — 2026-08-01 |
| LISS-0209 | CI executes the test suite | **complete** — 2026-08-02 (WP-0080) |
| LISS-0210 | Duplicated Kernel constants | **complete** — 2026-08-01 (WP-0076) |
| LISS-0211 | Batch record `schema_version` contradiction | **complete** — 2026-08-01 |
| LISS-0212 | Dangling `LISS-0070` reference | **complete** — 2026-08-01 (WP-0077) |
| LISS-0213 | Proposed ADRs with shipped Issues | **complete** — 2026-08-01 (WP-0077) |
| LISS-0214 | Broken documented commands / names | **complete** — 2026-08-01 (WP-0077) |
| LISS-0215 | Settled decisions documented as open | **complete** — 2026-08-01 (WP-0077) |
| LISS-0216 | Issue-planning document drift | **complete** — 2026-08-01 (WP-0077) |
| LISS-0217 | Dirac paper spelling sugar (design) | **complete** — 2026-08-01 (WP-0078; ADR 0165 Accepted, Red separate) |
| LISS-0218 | Kernel external-resource ports (design) | **complete** — 2026-08-01 (WP-0078; ADR 0166 Accepted, Red separate) |
| LISS-0219 | `inspect` / lane-choice guidance (design) | **complete** — 2026-08-01 (WP-0078 docs guidance) |
| LISS-0220 | QFT family infers as State, not Operator | **complete** — 2026-08-01 (WP-0069) |
| LISS-0221 | State-transforming calls must move their input root | **complete** — 2026-08-01 (WP-0073) |
| LISS-0222 | S01 Quantum Disaster Response OS | **complete** — 2026-08-01 (WP-0070) |
| LISS-0223 | S01 language beauty × physicist cognitive-load review | **complete** — 2026-08-01 (follow-ups WP-0071/0072) |
| LISS-0224 | Method-returned finite binders must lower before evolve | **complete** — 2026-08-01 (WP-0071) |
| LISS-0225 | `when` on classical enum control | **complete** — 2026-08-01 (WP-0071) |
| LISS-0226 | Nested empty `sum` must not inject undetermined OpIdentity | **complete** — 2026-08-01 (WP-0071 residual) |
| LISS-0227 | Local Operator `P`/`Q`/`N` must shadow Fock atoms | **complete** — 2026-08-01 (WP-0071 residual) |
| LISS-0228 | Joint `apply(qft/iqft/cqft, …)` runtime | **complete** — 2026-08-01 (WP-0072) |
| LISS-0229 | `inner`/`outer` Joint runtime Call | **complete** — 2026-08-01 (WP-0072) |
| LISS-0230 | S01 wire Basis / Trace-Out / Algebraic Fusion / Rankine·troy | **complete** — 2026-08-01 (WP-0072) |
| LISS-0231 | S01 `impl` interface-mediated dispatch | **complete** — 2026-08-01 (WP-0072) |
| LISS-0232 | S01 Index lattice beyond 2-wire toy | **complete** — 2026-08-01 (WP-0072) |
| LISS-0233 | Residual suite green floor | **complete** — 2026-08-02 (WP-0079) |
| LISS-0234 | Dirac paper spelling sugar Red | **complete** — 2026-08-02 (WP-0081) |
| LISS-0235 | Kernel `RngPort` Red | **complete** — 2026-08-02 (WP-0082) |
| LISS-0236 | Kernel `MeasureSinkPort` Red | **complete** — 2026-08-02 (WP-0083) |
| LISS-0237 | Kernel `SourcePort` Red | **complete** — 2026-08-02 (WP-0084) |
| LISS-0238 | Multi-hole Partial pipe lhs move | **complete** — 2026-08-02 (WP-0085) |
| LISS-0239 | Qutrit `apply(I)` Identity SV no-op | **complete** — 2026-08-02 (WP-0085) |
| LISS-0240 | observe sink `to` vs unit convert | **complete** — 2026-08-02 (WP-0086) |
| LISS-0241 | CI runs spec-verification | **complete** — 2026-08-02 (WP-0086) |
| LISS-0242 | open-work-register CI health refresh | **complete** — 2026-08-02 (WP-0086) |
| LISS-0244 | S01-R1 dialect honesty (README + scorecard) | **complete** — 2026-08-02 |
| LISS-0245 | S01 expressiveness / scenario expansion review | **triage Accepted** — 2026-08-02 |
| LISS-0246 | S01-R2 spine dialect pass | **complete** — 2026-08-02 |
| LISS-0247 | S01-E1 locked-scenario constellation seats | **complete** — 2026-08-02 |
| LISS-0248 | S01-R3 chapter align to locked seats | **complete** — 2026-08-02 |
| LISS-0249 | ADR 0173 `measure … tracing_out …` | **complete** — Accepted 2026-08-02 |
| LISS-0250 | Kernel `measure … tracing_out …` (ADR 0173) | **complete** — 2026-08-02 |
| LISS-0251 | S01 spine `|0>` → `tracing_out` | **complete** — 2026-08-02 |
| LISS-0252 | S01 chapters/satellites `|0>` → `tracing_out` | **complete** — 2026-08-02 |
| LISS-0253 | ADR 0174 Type-First field units | **complete** — Accepted 2026-08-02 |
| LISS-0254 | Kernel Type-First field units Red (ADR 0174) | **complete** — Phase 3 2026-08-02 |
| LISS-0255 | S01 docs hygiene post-0254 | **complete** — 2026-08-02 WP-0087 |
| LISS-0256 | S01 spine causal domain→Joint | **complete** — 2026-08-02 WP-0087 |
| LISS-0257 | S01 chapter story arcs | **complete** — 2026-08-02 WP-0087 |
| LISS-0258 | Failure glossary ADR | **complete** — ADR 0175 **Accepted** 2026-08-02 WP-0087 |
| LISS-0259 | TonightTicket thin ops mapping | **complete** — 2026-08-02 WP-0087 |
| LISS-0260 | S01 FQN + inspect hygiene | **complete** (waive rename) — 2026-08-02 WP-0087 |

**WP-0087** (S01 expressiveness brush-up) **complete + post_reviewed**
2026-08-02 (Adjudicator「承認」). Batch
[`execution-batch-wp-0087.json`](../collaboration/reviews/execution-batch-wp-0087.json)
`status: post_reviewed`. ADR 0175 failure glossary **Accepted**.

WP-0028 (0115–0117 parallelism) is **closed**. WP-0032–0061 shipped binder /
Float / Basis / Host / cqft / permanent-out / Partial+SI / temperature+mass /
ADR 0022 MVPs / Fusion expansions / evolve+bare-block Trace-Out / Rankine /
lb/oz/st/t / multi-hole Partial / US+UK ton / troy / tuple multi-hole Fusion /
mixed-unit reject then **canonical promote**. WP-0062–0068 shipped (SI, poly≥2
Fusion, interprocedural Trace-Out, CPU data-parallel, classical Fraction +
CredentialPort, Host MC inject + consumption seam). LISS-0196 open;
LISS-0197 deferred. WP-0069 (2026-08-01 operations review) filed
LISS-0199–LISS-0219 as **investigation intake**; none is approved for
execution. **WP-0070 / LISS-0222** (S01 Disaster Response showcase) **complete**
2026-08-01 (Issue id renumbered after main claimed LISS-0220/0221).
**LISS-0223** (S01 language beauty × physicist cognitive-load review)
**complete** 2026-08-01 (follow-ups WP-0071/0072).
**WP-0071 / LISS-0224..0227** merged 2026-08-01 (#228).
**WP-0072 / LISS-0228..0232** **complete** 2026-08-01 on
`batch/wp-0072-s01-coverage-residuals`.
**WP-0073 / LISS-0221 + LISS-0202 residual** **complete** 2026-08-01 on
`batch/wp-0073-linear-transform-move` (ADR 0168; suite floor 207/25).
**WP-0074 / LISS-0199..0201** **complete** 2026-08-01 on
`batch/wp-0074-cli-check-hardcode-keyerror`.
**WP-0075 / LISS-0204..0207** **complete** 2026-08-01 on
`batch/wp-0075-regression-clusters-0204-0207`.
**WP-0076 / LISS-0210** **complete** 2026-08-01 on
`batch/wp-0076-kernel-literals`.
**WP-0077 / LISS-0212..0216** **complete** 2026-08-01 on
`batch/wp-0077-docs-hygiene-0212-0216`.
**WP-0078 / LISS-0217..0219** **complete** 2026-08-01 on
`batch/wp-0078-design-0217-0219` (design/docs; Red separate).
**WP-0079 / LISS-0233** **complete** 2026-08-02 (green floor).
**WP-0080 / LISS-0209** **complete** 2026-08-02 (blocking CI).
**WP-0081** intake (0165/0166 Red) on `docs/wp-0081-0165-0166-red-intake`.
Next free for **new** ad-hoc Issues: **LISS-0255+**.
Next free work-plan id: **WP-0082+**.

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


## Inbox (`docs/issues/inbox/`)

Scratch intake notes before a `LISS-*` file exists. When the note is promoted to
a local Issue (or the work completes / is superseded), **move** the file to
`docs/issues/inbox/archive/` (or delete if redundant with the Issue). Do not
leave closed-work notes in the live inbox.

## Status Values

Use (practice + Definition of Done):

- `proposed`
- `ready`
- `in_progress`
- `blocked`
- `review`
- `final-review-ready`
- `complete` (preferred completion spelling; historical `done` remains readable)
- `done` (legacy synonym of `complete`)
- `open` (design / backlog without an active Feature Path)
- `deferred`
- `superseded`
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

**Retired (WP-0077 / LISS-0216).** The authoritative Issue inventory is
§Active ID claims above. Do not revive a second hand-maintained index table.



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
