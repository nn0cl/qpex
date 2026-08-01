"""Shared Kernel literal vocabularies (LISS-0210).

Leaf module: frozensets/sets only. Do not import typecheck, runtime, or
backend from here — consumers import this module.
"""

from __future__ import annotations

SECOND_QUANTIZED_FAMILIES = frozenset({
    "FermionOperator",
    "BosonOperator",
    "SpinOperator",
    "QubitOperator",
})

RELATIONAL = frozenset({"==", "!=", "<", "<=", ">", ">="})

DIRAC_LABEL_EXTRAS = frozenset("+-_")
