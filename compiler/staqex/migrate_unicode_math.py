"""ASCII → Unicode math spelling migrator (LISS-0069 Slice B).

Rewrites ket close, tensor, and simple ``adjoint(Primary)`` forms to the
canonical Unicode dual-accept spellings. Comments and string literals are
copied verbatim. Pipeline ``|>`` is never treated as a ket.
"""

from __future__ import annotations

from .kernel_literals import DIRAC_LABEL_EXTRAS as _DIRAC_LABEL_EXTRAS

_UNICODE_KET_CLOSE = "\u27e9"  # ⟩
_UNICODE_TENSOR = "\u2297"  # ⊗
_UNICODE_DAGGER = "\u2020"  # †
_ADJOINT_KEYWORD = "adjoint"
_PIPELINE = "|>"
_ASCII_TENSOR = "*|*"


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
        if source.startswith(_PIPELINE, i):
            out.append(_PIPELINE)
            i += len(_PIPELINE)
            continue
        if source.startswith(_ASCII_TENSOR, i):
            out.append(_UNICODE_TENSOR)
            i += len(_ASCII_TENSOR)
            continue
        if source[i] == "|":
            i = _migrate_or_copy_ket(source, i, out)
            continue
        if _at_word(source, i, _ADJOINT_KEYWORD):
            migrated, next_i = _try_migrate_simple_adjoint(source, i)
            if migrated is not None:
                out.append(migrated)
                i = next_i
                continue
        out.append(source[i])
        i += 1
    return "".join(out)


def _copy_line_comment(source: str, i: int, out: list[str]) -> int:
    start = i
    n = len(source)
    while i < n and source[i] != "\n":
        i += 1
    out.append(source[start:i])
    return i


def _copy_string_literal(source: str, i: int, out: list[str]) -> int:
    quote = source[i]
    start = i
    i += 1
    n = len(source)
    while i < n:
        ch = source[i]
        i += 1
        if ch == "\\" and i < n:
            i += 1
            continue
        if ch == quote:
            break
    out.append(source[start:i])
    return i


def _migrate_or_copy_ket(source: str, i: int, out: list[str]) -> int:
    """Rewrite ``|label>`` to ``|label⟩``; leave other ``|`` forms unchanged."""
    label_start = i + 1
    label_end = _scan_dirac_label_end(source, label_start)
    if label_end < len(source) and source[label_end] == ">":
        out.append("|")
        out.append(source[label_start:label_end])
        out.append(_UNICODE_KET_CLOSE)
        return label_end + 1
    out.append("|")
    return i + 1


def _scan_dirac_label_end(source: str, start: int) -> int:
    j = start
    n = len(source)
    while j < n and (source[j].isalnum() or source[j] in _DIRAC_LABEL_EXTRAS):
        j += 1
    return j


def _at_word(source: str, i: int, word: str) -> bool:
    if not source.startswith(word, i):
        return False
    if i > 0 and _is_ident_continue(source[i - 1]):
        return False
    end = i + len(word)
    if end < len(source) and _is_ident_continue(source[end]):
        return False
    return True


def _is_ident_start(ch: str) -> bool:
    return ch.isalpha() or ch == "_"


def _is_ident_continue(ch: str) -> bool:
    return ch.isalnum() or ch == "_"


def _skip_spaces(source: str, j: int) -> int:
    n = len(source)
    while j < n and source[j].isspace():
        j += 1
    return j


def _try_migrate_simple_adjoint(source: str, i: int) -> tuple[str | None, int]:
    """Rewrite ``adjoint(Primary)`` → ``Primary†`` when Primary is a bare ident."""
    n = len(source)
    j = _skip_spaces(source, i + len(_ADJOINT_KEYWORD))
    if j >= n or source[j] != "(":
        return None, i
    j = _skip_spaces(source, j + 1)
    if j >= n or not _is_ident_start(source[j]):
        return None, i
    primary_start = j
    j += 1
    while j < n and _is_ident_continue(source[j]):
        j += 1
    primary = source[primary_start:j]
    j = _skip_spaces(source, j)
    if j >= n or source[j] != ")":
        return None, i
    return primary + _UNICODE_DAGGER, j + 1
