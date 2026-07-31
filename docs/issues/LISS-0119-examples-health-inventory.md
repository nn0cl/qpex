# LISS-0119: Examples health inventory (rebaseline Gate P0)

## Metadata

- Local issue ID: LISS-0119
- GitHub issue: none
- Status: **complete** — inventory published 2026-07-31
- Phase: inventory complete (no heal in this Issue)
- Type: examples / conformance inventory
- Priority: P0 (rebaseline Gate P0 first slice)
- Initial planning size: M
- Depends on:
  - [rebaseline plan](../specs/staqex-v1-representative-program-rebaseline.md)
    (**Accepted**; §6 P0 authorized 2026-07-31)
- Blocks: none (unlocks heal)
- Unblocks: [LISS-0122](LISS-0122-examples-basics-heal.md),
  [LISS-0123](LISS-0123-examples-applied-heal-defer.md)
- Related: [LISS-0124](LISS-0124-language-coverage-ledger.md),
  [friction ledger](../architecture/physicist-source-friction-ledger.md),
  SV-09, raw JSON
  [`2026-07-31-liss-0119-inventory-raw.json`](../collaboration/traces/2026-07-31-liss-0119-inventory-raw.json)
- Implementation permission: consumed for inventory only
- Branch: `docs/liss-0119-p0-p1-planning`
- Kernel probe base: workspace tip without PR #171 Kernel merge (docs branch
  from `main`); re-probe after LISS-0121 merges may change named-coeff rows
  only — most LINEAR here are true quantum leftovers / other codes

## Summary

Honest green/amber/red inventory of 26 official catalog entries (B01–B15 +
A01–A11). No `.sqx` heal in this Issue.

## Judgment rules (applied)

| Class | Rule |
|---|---|
| **green** | `compile.ok` and deterministic `run`/`run_path` (`seed=0`). Soft `QSEM_*` alone does **not** demote. |
| **amber** | Runs with unclean **hard** diagnostics while still `ok` (none observed this probe). |
| **red** | `compile.ok == False`, run fail, missing entry, or probe exception. |

Multi-file entries use `compile_path` / `run_path` on the entry `.sqx`.
Single-file entries use `compile_source` / `run_source`.

## Inventory table (2026-07-31)

| Track | ID | Entry | Class | compile.ok | run.ok | Codes (abbrev) | Assign |
|---|---|---|---|---|---|---|---|
| basics | B01 | `never_leave_the_state.sqx` | **green** | True | True | QSEM soft | — |
| basics | B02 | `when_not_if.sqx` | **green** | True | True | QSEM soft | — |
| basics | B03 | `failure_worldline.sqx` | **red** | False | False | `PROBE_EXC:AttributeError` (BinOp.left) | 0122 + lang |
| basics | B04 | `evolve_not_loops.sqx` | **red** | False | False | LINEAR_IMPLICIT_DISCARD | 0122 |
| basics | B05 | `phase_interference.sqx` | **red** | False | False | LINEAR_IMPLICIT_DISCARD | 0122 |
| basics | B06 | `type_first_dimensions.sqx` | **red** | False | False | LINEAR_IMPLICIT_DISCARD | 0122 |
| basics | B07 | `structure_visibility.sqx` | **green** | True | True | QSEM soft | — |
| basics | B08 | `operators_hamiltonians.sqx` | **red** | False | False | LINEAR_IMPLICIT_DISCARD | 0122 |
| basics | B09 | `main_multi_file_modules.sqx` | **red** | False | False | LINEAR_DUPLICATE_USE, LINEAR_IMPLICIT_DISCARD | 0122 |
| basics | B10 | `main_static_qpu_lane.sqx` | **green** | True | True | QSEM soft | — |
| basics | B11 | `main_qft_registers.sqx` | **red** | False | False | LINEAR_IMPLICIT_DISCARD | 0122 |
| basics | B12 | `main_open_systems.sqx` | **red** | False | False | LINEAR_IMPLICIT_DISCARD | 0122 |
| basics | B13 | `main_host_job.sqx` | **red** | False | False | LINEAR_DUPLICATE_USE, LINEAR_IMPLICIT_DISCARD | 0122 |
| basics | B14 | `main_resource_profile.sqx` | **red** | False | False | LINEAR_DUPLICATE_USE, LINEAR_IMPLICIT_DISCARD | 0122 |
| basics | B15 | `main_multi_register.sqx` | **red** | False | False | LINEAR_IMPLICIT_DISCARD, MULTI_REGISTER_INDEX_AMBIGUOUS | 0122 + lang? |
| applied | A01 | `main_quantum_attention_toy.sqx` | **red** | False | False | `PROBE_EXC:AttributeError` (BinOp.left) | 0123 + lang |
| applied | A02 | `main_robot_graph_planner.sqx` | **red** | False | False | `PROBE_EXC:AttributeError` (BinOp.left) | 0123 + lang |
| applied | A03 | `main_h2_vqe.sqx` | **red** | False | False | LINEAR_IMPLICIT_DISCARD | 0123 |
| applied | A04 | `main_hp_protein_folding.sqx` | **red** | False | False | `PROBE_EXC:AttributeError` (BinOp.left) | 0123 + lang |
| applied | A05 | `main_qaoa_portfolio.sqx` | **red** | False | False | LINEAR_IMPLICIT_DISCARD | 0123 |
| applied | A06 | `main_topological_edge_memory.sqx` | **red** | False | False | LINEAR_DUPLICATE_USE, LINEAR_IMPLICIT_DISCARD | 0123 |
| applied | A07 | `main_open_system_sensor.sqx` | **red** | False | False | LINEAR_IMPLICIT_DISCARD | 0123 |
| applied | A08 | `main_entangled_compute_ancilla.sqx` | **red** | False | False | LINEAR_IMPLICIT_DISCARD, MULTI_REGISTER_INDEX_AMBIGUOUS | 0123 + lang? |
| applied | A09 | `main_qkd_corridor.sqx` | **red** | False | False | LINEAR_DUPLICATE_USE, LINEAR_IMPLICIT_DISCARD | 0123 |
| applied | A10 | `main_mission_observatory.sqx` | **red** | False | False | LINEAR_IMPLICIT_DISCARD | 0123 |
| applied | A11 | `main_static.sqx` | **green** | True | True | QSEM soft; catalog gap | 0123 (docs/SV) |

**Counts:** green **5** / amber **0** / red **21** (n=26).

## Catalog / SV / QUICKSTART gaps

| Gap | Evidence |
|---|---|
| A11 absent from SV-09 | `tests/spec_verification/suites/sv09_examples.py` lists A01–A10 only |
| Root / applied README “A01–A10” | `examples/README.md`, `examples/applied/README.md` omit A11 |
| Basics README “B01–B12” | `examples/README.md` still says B01–B12 though B13–B15 exist |
| A11 has no README | directory has modules only |
| QUICKSTART links A06 | A06 is **red** — violates “QUICKSTART → green only” Gate P0 rule |

## Heal assignment

### LISS-0122 (basics)

Heal red: **B03–B06, B08–B09, B11–B15** (11). Keep green: B01, B02, B07, B10.
Priority clusters: (1) LINEAR leftovers / duplicate use; (2) B03 depends on
language BinOp crash before sample-only fix; (3) B15 MULTI_REGISTER.

### LISS-0123 (applied)

Heal or defer red: **A01–A10** (10). A11 is compile/run **green** but needs
README + SV-09 registration (or explicit defer of the orphan).
QUICKSTART must stop linking A06 until green or point to a green demo (e.g. B01).
Priority clusters: (1) BinOp crash blockers A01/A02/A04; (2) LINEAR family;
(3) A06 QUICKSTART contamination; (4) A11 catalog sync.

## Language Issue candidates

| Candidate | Symptom | Entries |
|---|---|---|
| **HIR `BinOp` child walk** (`AttributeError: 'BinOp' object has no attribute 'left'`) | Compile **crashes** inside `hir._expr_children` | B03, A01, A02, A04 |
| **MULTI_REGISTER_INDEX_AMBIGUOUS** | Hard diagnostic on multi-register demos | B15, A08 |
| Widespread **LINEAR_*** on teaching samples | Often true unused/`measure` choreography debt — heal in 0122/0123 first; escalate only if verifier false-positive after rewrite | most red rows |

Do **not** silent-patch Kernel inside sample PRs; open a language Issue (suggest
**LISS-0125+**) for the BinOp crash before claiming B03/A01/A02/A04 sample-only.

## Exit

- [x] Inventory table for all 26 entries
- [x] Catalog/SV/QUICKSTART gap list
- [x] Heal assignment notes for LISS-0122 / LISS-0123
- [x] Language Issue candidates listed
- [x] Trace / raw JSON under `docs/collaboration/traces/`

## Next allowed operation

LISS-0122 / LISS-0123 may start under existing P0 authorize. Prefer language
Issue for BinOp crash before or beside those sample heals.
