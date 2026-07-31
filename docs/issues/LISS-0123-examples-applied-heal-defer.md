# LISS-0123: Examples applied heal or defer (rebaseline Gate P0)

## Metadata

- Local issue ID: LISS-0123
- GitHub issue: none
- Status: **complete** — applied A01–A11 all green (2026-07-31)
- Phase: Feature Path heal complete (sample-only + catalog/docs; Kernel untouched)
- Type: examples / conformance repair (applied)
- Priority: P0
- Initial planning size: L
- Depends on: [LISS-0119](LISS-0119-examples-health-inventory.md) (**complete**),
  [LISS-0122](LISS-0122-examples-basics-heal.md) (**complete** — heal patterns),
  [LISS-0125](LISS-0125-hir-binop-expr-children.md) (**complete** — unblocks A01/A02/A04)
- Blocks: none (Gate P0 complete with LISS-0122)
- Related: inventory (was A01–A10 red; A11 green+catalog gap); QUICKSTART→A06
- Implementation permission: **yes** (P0 authorize + 0119 exit)
- Branch: `feature/liss-0123-examples-applied-heal`

## Summary

Bring **applied** catalog entries to **green** or **explicitly deferred** with
physicist-readable rationale. Align QUICKSTART so it links **only** to green
entries. Resolve A11 README / SV-09 registration or mark explicit defer per
LISS-0119 findings.

## Acceptance (EARS)

1. **Given** LISS-0119’s applied classification, **when** this Issue completes,
   **then** every applied entry is green or deferred-with-rationale (no silent
   broken demos in the default catalog path).
2. **Given** QUICKSTART and track READMEs, **when** this Issue completes,
   **then** linked applied demos are green only.
3. **Given** A11 (Noether Forge lineage), **when** this Issue completes,
   **then** it is either registered (README + SV-09) as green, or explicitly
   deferred — not an invisible orphan.

## Non-goals

- Basics heal (LISS-0122).
- Reclaiming LISS-0120 / showcase S*.
- Silent Kernel fixes inside samples for language bugs.

## Green / deferred table (verified 2026-07-31, `PYTHONPATH=.`, seed=0)

| ID | Entry | Class | Soft codes (OK) | Heal notes |
|---|---|---|---|---|
| A01 | `main_quantum_attention_toy.sqx` | **green** | QSEM soft | Uncompute demo wires (`\|0>`) before `measure value` |
| A02 | `main_robot_graph_planner.sqx` | **green** | QSEM soft | Oracle `-> Float`; identity `step_graph_hop` (B09); unroll hops; inspect Grover then `\|0>` leftovers |
| A03 | `main_h2_vqe.sqx` | **green** | QSEM soft | Uncompute sibling `b=\|0>` before `measure a` |
| A04 | `main_hp_protein_folding.sqx` | **green** | QSEM soft | Oracle `-> Float`; inspect Grover then `\|0>` leftovers (not `vacuum`) |
| A05 | `main_qaoa_portfolio.sqx` | **green** | QSEM soft | Uncompute sibling `q1=\|0>` before `measure q0` |
| A06 | `main_topological_edge_memory.sqx` | **green** | QSEM soft | Class methods `-> Float`; drop `inspect(psi)` before measure |
| A07 | `main_open_system_sensor.sqx` | **green** | QSEM soft | `state rho = vacuum` after `lindblad` (B12); drop unused inspect |
| A08 | `main_entangled_compute_ancilla.sqx` | **green** | QSEM soft + soft MULTI | Uncompute `compute=\|0>`; soft MULTI as B15 |
| A09 | `main_qkd_corridor.sqx` | **green** | QSEM soft | Oracle `-> Float`; no `inspect(bob)`; uncompute Alice |
| A10 | `main_mission_observatory.sqx` | **green** | QSEM soft | `advance` / witness `-> Float`; `site`/`observatory` to `\|0>` (not vacuum) |
| A11 | `main_static.sqx` | **green** | QSEM soft | Already green; README + SV-09 + catalog A01–A11 |

**Counts:** green **11** / deferred **0** / red **0**.

## QUICKSTART

- `QUICKSTART.md` / `QUICKSTART.ja.md` keep B01 + A06; both **green** after heal
  (no retarget required).

## SV-09 / catalog

- `tests/spec_verification/suites/sv09_examples.py` registers A11 `main_static.sqx`.
- `examples/README.md`, `examples/applied/README.md`: wording **A01–A11**; A11 README added.

## Language follow-ups (do not silent-patch in samples)

| Candidate | Symptom | Evidence from this heal | Suggested next Issue |
|---|---|---|---|
| Consume-on-return for product / apply chain | Intermediate `State` binds before `return c *|* x` → LINEAR | A02 `step_graph_hop` forced to identity (same as B09) | **LISS-0126+** |
| Namespace / method `Float` return as runtime bind | `Float x = Ns.fn()` unbound when used in `phase` | A02/A04 used literal mark + harvest call | **LISS-0126+** |
| `vacuum` vs `\|0>` uncompute of Grover / multi-site leftovers | `vacuum` cleared shared joint behind inspected measure | A02/A04/A10 prefer `\|0>` | escalate only if pedagogy needs auto-uncompute |
| `MULTI_REGISTER_INDEX_AMBIGUOUS` false positive | Soft MULTI on qualified sites | A08 soft-only; compile.ok (B15) | **LISS-0126+** |
| Classical Type-First ⊕ State (from 0122) | — | not re-opened here | **LISS-0126+** |

## Exit

- [x] LISS-0119 exit recorded as dependency satisfied
- [x] Applied green-or-deferred table
- [x] QUICKSTART / README / SV-09 alignment for non-deferred entries
- [x] Language follow-ups linked if any
- [x] Spec verification registration (SV-09 A11 + catalog A01–A11)
- [x] Commit / PR

## Next allowed operation

None on this Issue. Gate P0 applied half complete. Language follow-ups →
LISS-0126+.
