"""Source helpers — structured `main` programs for tests."""

from __future__ import annotations


def as_main(
    body: str,
    *,
    package: str | None = None,
    imports: list[str] | None = None,
) -> str:
    """Wrap executable statements in `pub fn main() -> Unit { … }`."""
    lines: list[str] = []
    if package:
        lines.append(f"package {package}")
        lines.append("")
    for imp in imports or []:
        lines.append(f"import {imp}")
    if imports:
        lines.append("")
    lines.append("pub fn main() -> Unit {")
    for line in body.strip("\n").splitlines():
        lines.append(f"    {line}" if line.strip() else "")
    lines.append("}")
    return "\n".join(lines) + "\n"
