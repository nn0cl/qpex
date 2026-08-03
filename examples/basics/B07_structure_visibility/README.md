# B07 — Structure and visibility

Teaches `namespace`, `enum`, `struct`, free Operator factories, `pub`, and
module-private `_` fields (visibility seat on `IsingParams._pad`).

**WP-0088 / LISS-0262 / LISS-0300:** geometry and couplings use `struct`/`enum`;
Hamiltonian is a free-fn on the param pack (LISS-0297). Mutable systems with
private clocks stay `class` in A06 / QMD / A10 — not in this notebook face.

Legacy source: distilled from `examples/10_topological_physics/domain/`.
