# QPex Quickstart (developers)

Product onboarding for humans and agents working **in this repository**.
This is **not** the collaboration-template adoption guide
(`docs/collaboration/adoption-guide.md`).

[日本語](QUICKSTART.ja.md) · [README](README.md)

## 0. Prerequisites

- Python 3.11+ recommended (stdlib only for the Kernel path used here)
- Repo root as cwd

## 1. Run an official example

```bash
python3 -m compiler.qpex run examples/basics/B01_never_leave_the_state/never_leave_the_state.qpex --seed 0
python3 -m compiler.qpex run examples/applied/A06_topological_edge_memory/main_topological_edge_memory.qpex --seed 0
```

Multi-file examples use `import` + path linking (ADR **0054**). No
`module-info.qpex` is required for local scripts (ADR **0058** revised).

## 2. Keep the conformance gate green

```bash
python3 tests/spec_verification/run_all.py
```

OOP / visibility AT-TDD:

```bash
python3 tests/test_modern_oop_and_visibility.py
python3 tests/test_enum_support.py
python3 tests/test_encapsulation_and_module_info.py
```

## 3. Minimal valid program

```qpex
package demo
public fun main() {
    state x = dirac(0)
    measure x
}
```

```bash
python3 -m compiler.qpex run path/to/file.qpex --seed 0
```

## 4. Physicist-facing structure (optional)

```qpex
package demo
namespace Topology.SSH {
  pub enum BoundaryCondition { Periodic, Open }
  pub struct SSHParams { val v: Float, val w: Float }
  pub class SSHSystem {
    var _t: Float = 0.0
    pub val params: Topology.SSH.SSHParams
    fun init(p: Topology.SSH.SSHParams) {
      this.params = p
    }
    pub fun step() {
      this._t = this._t + 0.1
      Float done = 1.0
    }
  }
}
public fun main() {
  Topology.SSH.SSHParams p = Topology.SSH.SSHParams(0.5, 1.5)
  Topology.SSH.SSHSystem s = Topology.SSH.SSHSystem(p)
  Float ok = s.step()
  measure ok
}
```

Rules of thumb: `fun` (not retired `fn`); no `new`; no `protected`; hide with
`_`; export libraries with `pub`.

## 5. Where to read next

| Need | Document |
|------|----------|
| Agent workflow | `AGENTS.md`, `docs/architecture/agent-quickstart.md` |
| Language axioms | `docs/architecture/qpex-language-axioms.md` |
| Normative syntax/semantics | `docs/specs/qpex-language-specification.md` |
| Physicist ↔ DX harmony | `docs/architecture/physicist-dx-harmony.md` |
| Architecture map | `docs/architecture/README.md` |
| Examples | `examples/README.md` |
| Template process (Adjudicator) | `docs/collaboration/adoption-guide.md` |
