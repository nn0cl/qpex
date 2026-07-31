# LISS-0190: Quadratic / polynomial pipe Fusion

## Metadata

- Local issue ID: LISS-0190
- Status: **complete**
- ADR: [0157](../architecture/adr/0157-polynomial-operator-fusion.md)
- Program: [WP-0063](../work-plans/WP-0063-poly2-fusion.md)
- Tests: `tests/test_poly2_fusion_red.py`
- Extends: LISS-0173 / ADR 0141

## Exit

- [x] Unary pipe returns that are polynomials in the parameter fuse to one pushforward
- [x] Quadratic compose matches sequential `fn` application
- [x] Affine pipes still record `last_algebraic_fusion`; degree ≥2 records `last_poly_fusion`
- [x] Non-polynomial (`when`) keeps multi-pass fusion
