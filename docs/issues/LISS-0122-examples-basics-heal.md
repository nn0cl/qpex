# LISS-0122: Examples basics heal to green (rebaseline Gate P0)

## Metadata

- Local issue ID: LISS-0122
- GitHub issue: none
- Status: **complete** — all `examples/basics/**` entries green (2026-07-31)
- Phase: Feature Path heal complete (sample-only; Kernel untouched except LISS-0125 already on branch)
- Type: examples / conformance repair (basics)
- Priority: P0
- Initial planning size: M
- Depends on: [LISS-0119](LISS-0119-examples-health-inventory.md) (**complete**),
  [LISS-0125](LISS-0125-hir-binop-expr-children.md) (**complete** — unblocks B03)
- Blocks: rebaseline Gate P0 exit (with LISS-0123)
- Related: [rebaseline](../specs/staqex-v1-representative-program-rebaseline.md),
  inventory heal list (B03–B06, B08–B09, B11–B15), language follow-ups below
- Implementation permission: **yes** (P0 authorize + 0119 exit)
- Branch: `feature/liss-0122-examples-basics-heal`

## Summary

Bring **all** `examples/basics/**` official entry points to **green**, or mark
retired with an explicit replacement pointer, per rebaseline Gate P0. Scope of
which files and which failure clusters is **defined by LISS-0119** — do not
guess heal targets before inventory.

## Acceptance (EARS)

1. **Given** LISS-0119’s basics classification, **when** this Issue completes,
   **then** every basics entry is green or retired+pointer.
2. **Given** a sample defect that is actually a language bug, **when**
   discovered, **then** open or cite a language Issue — do not hide it by
   rewriting physics meaning in the sample.
3. **Given** heal edits, **when** verified, **then** `compile.ok` and
   deterministic run hold for remaining basics entries.

## Non-goals

- Applied track (LISS-0123).
- Showcase construction.
- Inventory itself (LISS-0119).
- Kernel behavior changes (except LISS-0125 BinOp already on branch).

## Green table (verified 2026-07-31, `PYTHONPATH=.`, seed=0)

| ID | Entry | Class | Soft codes (OK) | Heal notes |
|---|---|---|---|---|
| B01 | `never_leave_the_state.sqx` | **green** | QSEM soft | unchanged |
| B02 | `when_not_if.sqx` | **green** | QSEM soft | unchanged |
| B03 | `failure_worldline.sqx` | **green** | QSEM soft | After LISS-0125: inline `when` arms `4.0/0.0` / `8.0/2.0` (Err-in-joint); drop leftover `num`/`den` |
| B04 | `evolve_not_loops.sqx` | **green** | QSEM soft | Drop unused `inspect`; same-name `evolve` bind |
| B05 | `phase_interference.sqx` | **green** | QSEM soft | Static `vacuum` uncompute of `interfer`/`phase` sources |
| B06 | `type_first_dimensions.sqx` | **green** | QSEM soft | `State<Qty>` + evolve; vacuum leftovers; classical Type-First⊕State deferred |
| B07 | `structure_visibility.sqx` | **green** | QSEM soft | `advance() -> Float` (was false `State<Float>`) |
| B08 | `operators_hamiltonians.sqx` | **green** | QSEM soft | `state s1 = \|0>` uncompute before terminal `measure s0` |
| B09 | `main_multi_file_modules.sqx` | **green** | QSEM soft | Unroll coin+shift in main; identity `step_quantum_walk` until consume-on-return |
| B10 | `main_static_qpu_lane.sqx` | **green** | QSEM soft | unchanged |
| B11 | `main_qft_registers.sqx` | **green** | QSEM soft | Uncompute `observatory` before `measure probe` |
| B12 | `main_open_systems.sqx` | **green** | QSEM soft | `state rho = vacuum` after `lindblad` |
| B13 | `main_host_job.sqx` | **green** | QSEM soft | `measure viewed` (inspect consumes) |
| B14 | `main_resource_profile.sqx` | **green** | QSEM soft | `measure viewed` |
| B15 | `main_multi_register.sqx` | **green** | QSEM soft + soft `MULTI_REGISTER_INDEX_AMBIGUOUS` | Uncompute ancilla; soft MULTI false-positive noted |

**Counts:** green **15** / red **0** / retired **0**.

## Language follow-ups (do not silent-patch in samples)

| Candidate | Symptom | Evidence from this heal | Suggested next Issue |
|---|---|---|---|
| Classical Type-First ⊕ State arithmetic | `Delta<Time>` / `Mass` treated as mix-with-State / `dt` LINEAR; dim algebra loses quantity on `+` | B06 rewrite to `State<Qty>` | **LISS-0126+** |
| Consume-on-return for product / apply chain | Intermediate `State` binds before `return c *|* x` → `LINEAR_IMPLICIT_DISCARD` | B09 `step_quantum_walk` forced to identity | **LISS-0126+** |
| `MULTI_REGISTER_INDEX_AMBIGUOUS` false positive | Qualified `Z[data[0]]` still emits soft MULTI (recursive `OpLit` check on register path) | B15 soft-only; compile.ok | **LISS-0126+** |
| `interfer` / `phase` / `lindblad` non-consume | Source wires remain live after derived state | B05 / B12 vacuum uncompute | escalate only if pedagogy needs auto-consume |
| LISS-0125 BinOp `lhs`/`rhs` | Was AttributeError crash | **done** on this branch | — |

## Exit

- [x] LISS-0119 exit recorded as dependency satisfied
- [x] Basics green-or-retired table
- [x] Language follow-ups linked / listed
- [ ] Spec verification / relevant SV paths as applicable (post-merge / Adjudicator)
- [ ] Commit / PR (Adjudicator)

## Next allowed operation

Adjudicator review → commit/PR on `feature/liss-0122-examples-basics-heal`. Open language
Issues for the follow-ups above before relying on classical Type-First evolve or
full `step_quantum_walk` apply+shift again. LISS-0123 may proceed for applied.
