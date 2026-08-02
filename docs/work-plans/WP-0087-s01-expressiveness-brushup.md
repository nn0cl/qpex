# WP-0087: S01 expressiveness brush-up (causal spine + chapter arcs + hygiene)

| Field | Value |
|---|---|
| Status | **complete** + **post_reviewed** (2026-08-02) — Adjudicator「承認」; ADR 0175 **Accepted**; batch [execution-batch-wp-0087.json](../collaboration/reviews/execution-batch-wp-0087.json) `post_reviewed` |
| Purpose | After LISS-0243–0254 (dialect, seats, `tracing_out`, field units, Host ticket), close residual **expressiveness** and **docs hygiene** from the 2026-08-02 re-review |
| Parent program | [LISS-0222](../issues/LISS-0222-s01-quantum-disaster-response.md) / [WP-0070](WP-0070-s01-quantum-disaster-response.md) |
| Prior wave | LISS-0244–0248 (R1–R3, E0–E1), ADR 0173/0174, LISS-0250–0254 |
| Review input | [2026-08-02 expressiveness review](../collaboration/reviews/2026-08-02-s01-expressiveness-scenario-review.md); Adjudicator re-review (causal gap: domain built but not on Joint) |
| Pedagogy | [minimal dialect](../architecture/physicist-minimal-dialect.md) (**Accepted**); [redesign sketch](../specs/staqex-v1-s01-redesign-toward-minimal-dialect.md) |
| Branch (docs intake) | `docs/wp-0087-s01-expressiveness-brushup` |
| Execution branch (when approved) | `batch/wp-0087-s01-expressiveness-brushup` (or per-Issue feature branches) |
| Batch record (draft) | [execution-batch-wp-0087.json](../collaboration/reviews/execution-batch-wp-0087.json) — **`status: draft`** |
| Batch proposal | [2026-08-02-wp-0087-batch-proposal.md](../collaboration/reviews/2026-08-02-wp-0087-batch-proposal.md) |

## One-line goal

> Keep full A+B constellation coverage; make **scenario seats causally true in
> source** (especially tonight spine); sync docs; optional Host ticket semantics
> and failure glossary — without fake city optimum or live QPU.

## Product rules (binding)

| Rule | Meaning |
|---|---|
| Coverage | Scorecard **A+B** rows stay in S01 constellation; no silent demotion |
| Dialect spine | No inspect museum, no identity `evolve times`, no ritual `|0>` kill (use `tracing_out`) |
| Causal expressiveness | Classical domain objects that appear in the spine must **feed** `when` / coeffs / `H_*` / Host ticket — or be moved out of the spine path |
| Honesty | SIM-only; no optimality claim; Non-placeable chapters stay labeled |
| Language | No axiom rewrites in this WP; new surface → separate ADR Issue |

## Issue rows

| Order | ID | Title | Path | Depends | Status |
|---|---|---|---|---|---|
| 1 | [LISS-0255](../issues/LISS-0255-s01-docs-hygiene-post-0254.md) | Docs hygiene: scorecard + review Resolved sync | Fast Path / docs | — | **complete** |
| 2 | [LISS-0256](../issues/LISS-0256-s01-spine-causal-domain-joint.md) | Spine causal connect: domain → plan / H / when | Feature | 0255 optional | **complete** |
| 3 | [LISS-0257](../issues/LISS-0257-s01-chapter-story-arcs.md) | Chapter story arcs (CH-* brush-up) | Feature | 0256 recommended | **complete** |
| 4 | [LISS-0258](../issues/LISS-0258-failure-glossary-adr.md) | Failure glossary ADR (world-line vs Job) | Architecture Path / docs | — (parallel OK) | **complete** (ADR 0175 **Accepted**) |
| 5 | [LISS-0259](../issues/LISS-0259-tonight-ticket-ops-mapping.md) | TonightTicket thin ops mapping (honest) | Feature / Host | 0256 recommended | **complete** |
| 6 | [LISS-0260](../issues/LISS-0260-s01-fqn-inspect-hygiene.md) | FQN noise + residual chapter `inspect` hygiene | Fast Path / Feature | 0257 optional | **complete** (waive rename) |

## Execution order and rationale

```text
0255 docs hygiene ─────────────────────────────┐
0258 failure glossary ADR (parallel) ──────────┤
                                               ▼
                         0256 spine causal (P0 expressiveness)
                                               ▼
                         0257 chapter arcs (P1)
                          ├──► 0259 ticket ops mapping
                          └──► 0260 FQN / inspect polish
```

1. **0255 first** — cheap; stops agents reading stale “0254 pending.”
2. **0256 is the program core** — re-review P0-ex: domain construction must affect Joint.
3. **0257** — seats exist (E1); deepen chapter arcs without dropping surfaces.
4. **0258** — language design residual; docs ADR only until Accepted.
5. **0259** — Host C-layer meaning; depends on spine producing interpretable measure context.
6. **0260** — polish; do not block 0256.

## Granularity rationale

| Split | Why |
|---|---|
| Docs vs spine vs chapters | Different paths, risk, and approval types |
| Causal spine alone | Largest reviewable unit; must not mix with FQN renames |
| Failure glossary separate | Architecture Path; must not gate example Feature work |
| Ticket mapping after causal | Avoid inventing ops labels for pure 2-level samples without story hooks |
| FQN last | High churn, low expressiveness value |

**Out of this WP:** live QPU adapter; Kernel Continuous; scorecard row deletion; city-wide optimality; new `tracing_out` semantics (already ADR 0173).

## Out of scope (program-wide)

- Live provider SDK / CUDA
- Dropping scorecard A+B rows
- Reverting minimal dialect or stuffing full scorecard onto one `main`
- Inventing victim PII or production dispatch APIs
- Silent “optimal plan” claims on tickets

## Verification (program, after approved Issues land)

```bash
# Spine + chapters
python3 -m compiler.staqex run examples/showcase/S01_quantum_disaster_response/main_disaster_response.sqx --seed 0
python3 -m compiler.staqex run examples/showcase/S01_quantum_disaster_response/main_morning_collect.sqx --seed 0
python3 -m compiler.staqex run examples/showcase/S01_quantum_disaster_response/main_day2_recovery.sqx --seed 0
python3 -m compiler.staqex run examples/showcase/S01_quantum_disaster_response/main_fuel_search.sqx --seed 0
python3 -m compiler.staqex run examples/showcase/S01_quantum_disaster_response/main_burst_spectrum.sqx --seed 0
python3 -m compiler.staqex run examples/showcase/S01_quantum_disaster_response/main_comms_channel.sqx --seed 0
python3 -m compiler.staqex run examples/showcase/S01_quantum_disaster_response/main_tri_register.sqx --seed 0
python3 -m compiler.staqex run examples/showcase/S01_quantum_disaster_response/main_route_interference.sqx --seed 0
python3 -m compiler.staqex run examples/showcase/S01_quantum_disaster_response/main_lattice_four.sqx --seed 0
python3 -m compiler.staqex run examples/showcase/S01_quantum_disaster_response/main_fidelity_inner_check.sqx --seed 0

# Host
python3 examples/showcase/S01_quantum_disaster_response/host/export_tonight_ticket.py --seed 0 --out /tmp/tonight_ticket.json
python3 examples/showcase/S01_quantum_disaster_response/host/demand_inject.py
STAQEX_AGENCY_TOKEN=demo python3 examples/showcase/S01_quantum_disaster_response/host/agency_share.py
python3 examples/showcase/S01_quantum_disaster_response/host/rolling_replan_job.py

# Regression (when Feature Issues touch Kernel — none planned in core path)
# python3 -m pytest …  # as required by each Issue
```

**Expressiveness checks (manual / review):**

- [ ] Spine README or file header lists which domain quantities **drive** which `H_*` / `when` arms
- [ ] No major domain board is constructed solely for dead Float tags
- [ ] Each CH-* still cites locked-scenario seat; arcs improved per 0257 exit
- [ ] Scorecard residuals match shipped ADR 0173/0174 / LISS-0254 **complete**
- [ ] Ticket honesty blocks unchanged (`live_qpu: false`, no optimality)

## Approval model

| Step | Approval |
|---|---|
| This WP + Issue files | Scope / planning intake (this PR) |
| Per-Issue Feature Red/Green | Plan or batch approval per agent family |
| LISS-0258 ADR Accept | Architecture approval (separate) |
| Batch execution of 0255–0260 | Promote [execution-batch-wp-0087.json](../collaboration/reviews/execution-batch-wp-0087.json) from `draft` → `approved_for_execution` (see proposal §4) |

**This planning PR does not authorize implementation.**  
**Draft batch JSON does not authorize implementation** until Adjudicator sets
`approved_for_execution` and fills `approval_commit` / `expires_at`.

## Success definition

WP closes when all named Issues are **complete** or explicitly **deferred** by Adjudicator, and re-review P0-ex (spine causal gap) is closed or waived with recorded reason.
