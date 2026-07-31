# Trace: LISS-0121 classical coefficient vs LINEAR — complete

- Date: 2026-07-31
- Branch: `feature/liss-0121-classical-coefficient-vs-linear`
- Operating path: Feature Path (Issue-level; ADR 0114 Accepted)
- Issue: [LISS-0121](../../issues/LISS-0121-classical-coefficient-elaboration-vs-linear.md)
- Phases: Red → Green → Refactor complete; suite
  `tests/test_liss_0121_classical_coefficient_vs_linear_red.py` (10/10)
- Kernel: Type-First elaboration coefficients as Classical;
  `OpAttr` + `op_attr_elaboration.py`; `COEFFICIENT_IN_QUANTUM_POSITION`
- Docs: friction F-02/F-05 closed for named Float + field OpDSL
- Implementation permission: consumed for LISS-0121 only; P0 examples health
  still separately gated on rebaseline
