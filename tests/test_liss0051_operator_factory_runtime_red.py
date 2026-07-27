"""Superseded runtime Red cases — see LISS-0107.

Parser fixes from LISS-0051 are complete; the remaining linked-module runtime
gap is tracked under LISS-0107 and tested in
``tests/test_liss0107_examples_linker_runtime_red.py``.
"""

from __future__ import annotations

from test_liss0107_examples_linker_runtime_red import (  # noqa: F401
    test_linked_hamiltonian_factory_op_space_terminates,
    test_linked_operator_factory_result_is_resolved_at_runtime,
    test_official_multifile_examples_run_without_runtime_errors,
)
