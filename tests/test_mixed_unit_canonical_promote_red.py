"""AT-TDD: LISS-0187 mixed-unit canonical promote (ADR 0155)."""

from __future__ import annotations

import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from compiler.staqex.pipeline import compile_source  # noqa: E402
from compiler.staqex.runtime.evaluator import Evaluator  # noqa: E402


def test_mixed_kg_g_promotes_to_kg() -> None:
    compiled = compile_source(
        """
        package t
        pub fn main() -> Unit {
            Mass a = 1.0.kg + 1.0.g
            state x = |0>
            measure x
        }
        """
    )
    codes = {d.get("code", "") for d in compiled.diagnostics}
    assert "UNIT_MIXED_ARITHMETIC_ERROR" not in codes, codes
    assert "PARSE_ERROR" not in codes, codes
    ev = Evaluator(seed=0)
    ev.run_unit(compiled.unit)
    assert abs(ev.scalars["a"] - 1.001) < 1e-12
    assert ev.scalar_units.get("a") == "kg"


def test_same_unit_addition_ok() -> None:
    compiled = compile_source(
        """
        package t
        pub fn main() -> Unit {
            Mass a = 1.0.kg + 2.0.kg
            state x = |0>
            measure x
        }
        """
    )
    codes = {d.get("code", "") for d in compiled.diagnostics}
    assert "UNIT_MIXED_ARITHMETIC_ERROR" not in codes, codes
    ev = Evaluator(seed=0)
    ev.run_unit(compiled.unit)
    assert abs(ev.scalars["a"] - 3.0) < 1e-12
    assert ev.scalar_units.get("a") == "kg"


def test_explicit_to_then_same_unit_ok() -> None:
    compiled = compile_source(
        """
        package t
        pub fn main() -> Unit {
            Mass a = (1.0.kg to g) + 1.0.g
            state x = |0>
            measure x
        }
        """
    )
    codes = {d.get("code", "") for d in compiled.diagnostics}
    assert "UNIT_MIXED_ARITHMETIC_ERROR" not in codes, codes
    ev = Evaluator(seed=0)
    ev.run_unit(compiled.unit)
    assert abs(ev.scalars["a"] - 1001.0) < 1e-9
    assert ev.scalar_units.get("a") == "g"


def test_type_first_mixed_vars_promote() -> None:
    compiled = compile_source(
        """
        package t
        pub fn main() -> Unit {
            Mass a = 1.0.kg
            Mass b = 1.0.g
            Mass c = a + b
            state x = |0>
            measure x
        }
        """
    )
    codes = {d.get("code", "") for d in compiled.diagnostics}
    assert "UNIT_MIXED_ARITHMETIC_ERROR" not in codes, codes
    ev = Evaluator(seed=0)
    ev.run_unit(compiled.unit)
    assert abs(ev.scalars["c"] - 1.001) < 1e-12
    assert ev.scalar_units.get("c") == "kg"


def test_celsius_fahrenheit_promote_to_kelvin() -> None:
    compiled = compile_source(
        """
        package t
        pub fn main() -> Unit {
            Temperature t = 0.0.C + 32.0.F
            state x = |0>
            measure x
        }
        """
    )
    codes = {d.get("code", "") for d in compiled.diagnostics}
    assert "UNIT_MIXED_ARITHMETIC_ERROR" not in codes, codes
    ev = Evaluator(seed=0)
    ev.run_unit(compiled.unit)
    # 0°C = 273.15 K; 32°F = 273.15 K → sum 546.3 K
    assert abs(ev.scalars["t"] - 546.3) < 1e-9
    assert ev.scalar_units.get("t") == "K"


if __name__ == "__main__":
    test_mixed_kg_g_promotes_to_kg()
    print("PASS test_mixed_kg_g_promotes_to_kg")
    test_same_unit_addition_ok()
    print("PASS test_same_unit_addition_ok")
    test_explicit_to_then_same_unit_ok()
    print("PASS test_explicit_to_then_same_unit_ok")
    test_type_first_mixed_vars_promote()
    print("PASS test_type_first_mixed_vars_promote")
    test_celsius_fahrenheit_promote_to_kelvin()
    print("PASS test_celsius_fahrenheit_promote_to_kelvin")
