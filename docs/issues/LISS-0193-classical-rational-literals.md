# LISS-0193: Classical Fraction literals → f64 at State

## Metadata

- Local issue ID: LISS-0193
- Status: **complete**
- ADR: [0160](../architecture/adr/0160-classical-rational-literals.md)
- Program: [WP-0066](../work-plans/WP-0066-classical-rational-credentials.md)
- Tests: `tests/test_classical_rational_red.py`
- Amends: ADR 0125 (classical path only)

## Exit

- [x] Integer `/` yields `Fraction` in classical eval
- [x] Joint / State coords coerce Fraction → float
- [x] Float `/` remains IEEE; Joint masses stay f64
