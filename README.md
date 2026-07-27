# QPex

**QPex** (*Quantum-Probabilistic Executable*) is a programming language that aims to
let you write quantum-computer programs the way you write theoretical-physics
formulas.

[Japanese README](README.ja.md) · [Quickstart](QUICKSTART.md) ·
[Architecture](docs/architecture/README.md) · [Language Spec](docs/specs/qpex-language-specification.md)

## License

Dual-licensed under **MIT OR Apache-2.0** — see [LICENSE](LICENSE),
[LICENSE-MIT](LICENSE-MIT), [LICENSE-APACHE](LICENSE-APACHE).

## Status (honest)

| Layer | Reality |
|-------|---------|
| Collaboration / AT-TDD | Adopted from `llm-project-template` (`AGENTS.md`, ADRs 0001–0012, …) |
| Normative language surface | `docs/specs/qpex-language-specification.md` + ADRs 0013+ |
| **Runnable Kernel today** | **Python** package `compiler/qpex/` (lexer → parser → typecheck → Joint evaluator) |
| Long-term runtime | Rust VM / simulator first; QPU backends later (ports, not MVP) |
| Spec verification | `python3 tests/spec_verification/run_all.py` (SV suite; keep green) |

Do **not** invent language behavior without an accepted ADR/spec and an
explicit AT-TDD phase (see `AGENTS.md`).

## Physicist DX (surface)

Programmer tools are framed as physics units — not Java ceremony:

| Surface | Physics reading |
|---------|-----------------|
| `enum` | Exclusive geometry / bases |
| `struct` | Immutable parameter packs |
| `class` + `fun init` | Physical **system** / experimental setup (`new` Forbidden) |
| `namespace` | Theory sectors |
| default / `pub` / `_` | Module-private / public API / class-private (no `protected`) |

Details: [`docs/architecture/physicist-dx-harmony.md`](docs/architecture/physicist-dx-harmony.md),
ADR **0054–0056**, **0058**.

## Run a program

```bash
python3 -m compiler.qpex run examples/basics/B01_never_leave_the_state/never_leave_the_state.qpex --seed 0
python3 -m compiler.qpex run examples/applied/A06_topological_edge_memory/main_topological_edge_memory.qpex --seed 0
```

Examples index: [`examples/README.md`](examples/README.md).

## Verify

```bash
python3 tests/spec_verification/run_all.py
python3 tests/test_modern_oop_and_visibility.py
```

## Agent / Adjudicator entry

1. `AGENTS.md` — operating contract  
2. `docs/architecture/agent-quickstart.md` — Fast / Feature / Architecture Path  
3. `docs/collaboration/session-start-and-resume.md` — resume without chat memory  
4. Stack facts live in `CLAUDE.md` / `AGENTS.md` (Tier 2; do not blind-overwrite from template)

Template sync (process docs only): keep `.collaboration-template-version`;
use `llm-project-template`’s `scripts/update-ai-collaboration-files.sh`.
Product README / language ADRs are **target-owned** — not replaced by the
template README.
