"""AT-TDD residual: LISS-0186 reject path superseded by ADR 0155 / LISS-0187.

Kept as a thin pointer so CI does not assert the old reject behavior.
"""

from __future__ import annotations

import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
_TESTS = Path(__file__).resolve().parent
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))
if str(_TESTS) not in sys.path:
    sys.path.insert(0, str(_TESTS))

from test_mixed_unit_canonical_promote_red import (  # noqa: E402
    test_mixed_kg_g_promotes_to_kg,
    test_type_first_mixed_vars_promote,
)


if __name__ == "__main__":
    test_mixed_kg_g_promotes_to_kg()
    print("PASS (superseded) test_mixed_kg_g_promotes_to_kg")
    test_type_first_mixed_vars_promote()
    print("PASS (superseded) test_type_first_mixed_vars_promote")
