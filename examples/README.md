# QPex Official Examples

Physics-oriented sample programs for **QPex（キューペックス）**.

Axiom: **Never Leave the State** — every mid-program value is `State<T>`;
collapse happens only at terminal `measure`.

## Layout

| Dir | Topic |
|-----|--------|
| [`01_classical_mechanics`](01_classical_mechanics/) | Phase-space ensemble / Euler pushforward |
| [`02_quantum_basics`](02_quantum_basics/) | Double-slit + spontaneous phase cancel |
| [`03_quantum_information`](03_quantum_information/) | Bell / EPR correlation & CHSH-style project |
| [`04_quantum_algorithms`](04_quantum_algorithms/) | Grover oracle phase + `diffuse` |
| [`05_harmonic_oscillator`](05_harmonic_oscillator/) | Classical HO phase-space Euler (Type-First) |
| [`06_statistical_physics`](06_statistical_physics/) | 1D Ising + Boltzmann reweight |
| [`07_quantum_walk`](07_quantum_walk/) | Classical vs quantum walk spread |
| [`08_gauge_symmetry`](08_gauge_symmetry/) | U(1) gauge pedagogy (`phase` + Born invariant) |
| [`09_complex_simulations`](09_complex_simulations/) | Multi-file DTQW (ADR 0054 linker) |
| [`10_topological_physics`](10_topological_physics/) | SSH + `namespace` / `enum` / `struct` / `class` + `fn init` / `pub` / `_` |
| [`11_shor_rsa_toy`](11_shor_rsa_toy/) | Shor period-finding **toy** (\(N=15\); multi-file; educational) |
| [`12_city_route_search`](12_city_route_search/) | Smart-city corridor search (Grover toy; multi-file) |
| [`13_deep_space_qkd_toy`](13_deep_space_qkd_toy/) | Deep-space Bell / QKD intuition (multi-file) |
| [`14_genome_motif_grover`](14_genome_motif_grover/) | Short DNA motif Grover (alphabet size 4; multi-file) |
| [`15_orbital_mesh_walk`](15_orbital_mesh_walk/) | LEO mesh DTQW (Position = node index; multi-file) |
| [`16_quantum_observatory`](16_quantum_observatory/) | Modular capstone: topology, interference, walks, search, and an entangled link |
| [`17_static_register_foreach`](17_static_register_foreach/) | QPU static register elaboration; opaque wire handles and `forEach` |

Catalog conventions (honesty tables, multi-file layout, SV-09):  
[`docs/collaboration/examples-catalog-conventions.md`](../docs/collaboration/examples-catalog-conventions.md).  
Brush-up ledger: [LISS-0003](../docs/issues/LISS-0003-examples-driven-kernel-brush-up.md) / [WP-0003](../docs/work-plans/WP-0003-examples-driven-brush-up.md).

## Program structure

Every example is a structured compilation unit:

```qpex
package com.qpex.examples.…

pub fn main() -> Unit {
    // Type-First binds, evolve, measure — never top-level script soup
}
```

Top-level executable statements are rejected (`TOPLEVEL_EXECUTION_ERROR`, SV-16).

## Kernel note (stance a)

The evaluator is a **complex-amplitude Joint** runtime: each world carries
$c\in\mathbb{C}$ with Born weight $|c|^2$. `phase` / `cis` / `Complex.cis`
attach phases; `interfer` sums amplitudes then takes $|\sum c_i|^2$
(destructive cancel → vacuum). `diffuse` is Grover inversion-about-mean.

Surface vocabulary: `when` / `map` / `project` / `interfer` / `phase` /
`diffuse` / `inspect` / `measure` / `evolve`.

## Run

```bash
python3 -m compiler.qpex check examples/02_quantum_basics/double_slit.qpex
python3 -m compiler.qpex inspect examples/02_quantum_basics/double_slit.qpex
python3 -m compiler.qpex run --target cpu examples/02_quantum_basics/double_slit.qpex --seed 0

# Same portable source → OpenQASM sketch (ADR 0036)
python3 -m compiler.qpex emit-qasm examples/03_quantum_information/portable_bell_qpu.qpex

# all examples + backend tests (SV-09 / SV-10)
python3 tests/spec_verification/run_all.py
```

## Host Job API

QPex source does not contain `Job` or `Task` operations. A host program may
submit the same source through the provider-neutral local API; this is also the
boundary where a future simulator service or QPU adapter will connect.

```python
from compiler.qpex import submit_source

source = """
pub fn main() -> Unit {
    State<Int> answer = dirac(42)
    measure answer
}
"""

job = submit_source(source, settings={"target": "local", "seed": 0})
print(job.id, job.status())
result = job.result()  # waits for completion in a remote adapter
print(result.status, result.measurements[0].value)
```

For a blocking local or CLI-style call, use `run_source(source, settings=…)`.
`JobResult` contains measurement envelopes and host metadata; it does not
expose the Kernel's `Joint` or AST. Provider SDKs, credentials, retries, and
sessions are intentionally outside this example and remain future Host
Adapter work.
