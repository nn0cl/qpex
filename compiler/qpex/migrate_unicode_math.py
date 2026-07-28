"""ASCII → Unicode math spelling migrator (LISS-0069 Slice B).

Rewrites ket close, tensor, and simple ``adjoint(Primary)`` forms to the
canonical Unicode dual-accept spellings. Comments and string literals are
copied verbatim. Pipeline ``|>`` is never treated as a ket.
"""

from __future__ import annotations

_UNICODE_KET_CLOSE = "\u27e9"  # ⟩
_UNICODE_TENSOR = "\u2297"  # ⊗
_UNICODE_DAGGER = "\u2020"  # †
_DIRAC_LABEL_EXTRAS = frozenset("+-_")


def migrate_unicode_math_source(source: str) -> str:
    """Return ``source`` with M-P02–M-P04 ASCII math forms rewritten to Unicode.

    Pure and deterministic. Idempotent on already-canonical Unicode forms.
    """
    out: list[str] = []
    i = 0
    n = len(source)
    while i < n:
        if source.startswith("//", i):
            i = _copy_line_comment(source, i, out)
            continue
        if source[i] in {"'", '"'}:
            i = _copy_string_literal(source, i, out)
            continue
        if source.startswith("|>", i):
            out.append("|>")
            i += 2
            continue
        if source.startswith("*|*", i):
            out.append(_UNICODE_TENSOR)
            i += 3
            continue
        if source[i] == "|":
            i = _migrate_or_copy_ket(source, i, out)
            continue
        if _at_adjoint_keyword(source, i):
            migrated, next_i = _try_migrate_simple_adjoint(source, i)
            if migrated is not None:
                out.append(migrated)
                i = next_i
                continue
        out.append(source[i])
        i += 1
    return "".join(out)


def _copy_line_comment(source: str, i: int, out: list[str]) -> int:
    n = len(source)
    while i < n and source[i] != "\n":
        out.append(source[i])
        i += 1
    return i


def _copy_string_literal(source: str, i: int, out: list[str]) -> int:
    quote = source[i]
    out.append(quote)
    i += 1
    n = len(source)
    while i < n:
        ch = source[i]
        out.append(ch)
        i += 1
        if ch == "\\" and i < n:
            out.append(source[i])
            i += 1
            continue
        if ch == quote:
            break
    return i


def _migrate_or_copy_ket(source: str, i: int, out: list[str]) -> int:
    """Rewrite ``|label>`` to ``|label⟩``; leave other ``|`` forms unchanged."""
    n = len(source)
    label_start = i + 1
    j = label_start
    while j < n and (source[j].isalnum() or source[j] in _DIRAC_LABEL_EXTRAS):
        j += 1
    if j < n and source[j] == ">":
        out.append("|")
        out.append(source[label_start:j])
        out.append(_UNICODE_KET_CLOSE)
        return j + 1
    out.append("|")
    return i + 1


def _at_adjoint_keyword(source: str, i: int) -> bool:
    if not source.startswith("adjoint", i):
        return False
    if i > 0 and (source[i - 1].isalnum() or source[i - 1] == "_"):
        return False
    end = i + len("adjoint")
    if end < len(source) and (source[end].isalnum() or source[end] == "_"):
        return False
    return True


def _try_migrate_simple_adjoint(source: str, i: int) -> tuple[str | None, int]:
    """Rewrite ``adjoint(Primary)`` → ``Primary†`` when Primary is a bare ident."""
    n = len(source)
    j = i + len("adjoint")
    while j < n and source[j].isspace():
        j += 1
    if j >= n or source[j] != "(":
        return None, i
    j += 1
    while j < n and source[j].isspace():
        j += 1
    if j >= n or not (source[j].isalpha() or source[j] == "_"):
        return None, i
    primary_start = j
    j += 1
    while j < n and (source[j].isalnum() or source[j] == "_"):
        j += 1
    primary = source[primary_start:j]
    while j < n and source[j].isspace():
        j += 1
    if j >= n or source[j] != ")":
        return None, i
    return primary + _UNICODE_DAGGER, j + 1
