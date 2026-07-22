"""IR package — DAG extraction (ADR 0032)."""

from .dag import Dag, IrNode, lower_source_ast

__all__ = ["Dag", "IrNode", "lower_source_ast"]
