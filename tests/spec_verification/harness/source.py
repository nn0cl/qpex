"""Source helpers — structured `main` programs for tests."""

from __future__ import annotations


def as_main(
    body: str,
    *,
    package: str | None = None,
    imports: list[str] | None = None,
) -> str:
    """Wrap executable statements in `public fun main() { … }`."""
    lines: list[str] = []
    if package:
        lines.append(f"package {package}")
        lines.append("")
    for imp in imports or []:
        lines.append(f"import {imp}")
    if imports:
        lines.append("")
    lines.append("public fun main() {")
    for line in body.strip("\n").splitlines():
        lines.append(f"    {line}" if line.strip() else "")
    lines.append("}")
    return "\n".join(lines) + "\n"
