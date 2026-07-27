# Agent sync — modern OOP + visibility (ADR 0055 / 0056 / 0058)

**Audience:** coding agents resuming Kernel work on structure / access control.  
**Normative:** ADR 0055, 0056, 0058; language spec §6.4–§6.5; `physicist-dx-harmony.md`.

## Do

- Use **`fn`** for methods; treat `fun` as Retired.
- Construct with `Type(…)` / `fn init`; never emit `new` or `protected`.
- Prefer `_name` for class-private fields; `pub` only at library boundaries.
- Keep local multi-file examples free of mandatory `module-info`.
- After visibility / linker changes: run
  `python3 tests/test_modern_oop_and_visibility.py` and
  `python3 tests/spec_verification/run_all.py`.

## Do not

- Reintroduce Java `protected` / inheritance matrices.
- Require `module-info` exports for examples 01–10.
- Copy `llm-project-template` files listed under
  `collaboration_template_exclude_paths` (template traces, `LISS-*`,
  `template-rollout.md`) or template-only research essays into this repo as
  “required” docs — they are **not** part of target adoption.

## Pointers

- Example: `examples/applied/A06_topological_edge_memory/`
- Quickstart: `QUICKSTART.md`
