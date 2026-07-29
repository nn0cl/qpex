"""AT-TDD Phase 1 Red: LISS-0114 Slice A — pipeline hard-fail + Gherkin."""

from __future__ import annotations

import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from compiler.staqex.pipeline import compile_source


def _codes(diags: list[dict]) -> set[str]:
    return {str(d.get("code", "")) for d in diags}


def test_implicit_discard_fails_compile_source() -> None:
    """LINEAR_IMPLICIT_DISCARD must hard-fail CompileResult.ok via pipeline."""
    compiled = compile_source(
        """
        package t
        pub fn main() -> Unit {
            State<Int> leftover = coin()
            State<Int> q = coin()
            measure q
        }
        """
    )
    assert "LINEAR_IMPLICIT_DISCARD" in _codes(compiled.diagnostics), (
        f"expected LINEAR_IMPLICIT_DISCARD in compile diagnostics, "
        f"got {_codes(compiled.diagnostics)}"
    )
    assert compiled.ok is False, "linear discard must set CompileResult.ok=False"


def test_duplicate_alias_fails_compile_source() -> None:
    compiled = compile_source(
        """
        package t
        pub fn main() -> Unit {
            State<Int> q = coin()
            State<Int> alias = q
            measure alias
        }
        """
    )
    assert "LINEAR_DUPLICATE_USE" in _codes(compiled.diagnostics)
    assert compiled.ok is False


def test_acceptance_gherkin_matches_shipped_surface() -> None:
    """R8: LISS-0075 acceptance text must describe alias, not gate-twice."""
    issue = (_REPO / "docs/issues/LISS-0075-linear-quantum-usage.md").read_text(
        encoding="utf-8"
    )
    assert "alias rebinding" in issue or "State alias = q" in issue, (
        "Gherkin must describe alias rebinding surface"
    )
    assert "gate to qubit q twice without measure" not in issue, (
        "drift wording 'gate ... twice without measure' must be removed"
    )


def main() -> None:
    test_implicit_discard_fails_compile_source()
    print("PASS test_implicit_discard_fails_compile_source")
    test_duplicate_alias_fails_compile_source()
    print("PASS test_duplicate_alias_fails_compile_source")
    test_acceptance_gherkin_matches_shipped_surface()
    print("PASS test_acceptance_gherkin_matches_shipped_surface")
    print("OK - LISS-0114 Slice A Phase 1 Red")


if __name__ == "__main__":
    main()
